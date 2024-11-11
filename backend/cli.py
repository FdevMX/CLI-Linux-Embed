import subprocess
import os
import shutil
import socket
import platform
import re
from datetime import datetime

from ply import lex, yacc

# Lexer for command parsing
tokens = (
    'COMMAND',
    'ARGUMENT'
)

# Lista de comandos válidos actualizada
commands_list = [
    'cat', 'ls', 'echo', 'mkdir', 'pwd', 'cd', 'help', 
    'history', 'clear', 'cls', 'unzip', 'rm', 'mv', 'cp', 'zip',
    'ping', 'ipconfig', 'netstat', 'dig'  # Agregados comandos de red
]

# Define the command tokens
def t_COMMAND(t):
    r'[a-zA-Z][a-zA-Z0-9]*'  # Permite letras y números, pero debe comenzar con letra
    if t.value in commands_list:
        return t
    else:
        t.type = 'ARGUMENT'  # Si no es un comando válido, debe ser un argumento
        return t

# Define the argument tokens
t_ARGUMENT = r'[a-zA-Z0-9./_\-~@:]+|"[^"]*"|\'[^\']*\''  # Cualquier secuencia no separada por espacios (incluye puntos, guiones, etc.)

# Ignored characters
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parsing rules
def p_command(p):
    '''
    command : COMMAND
            | COMMAND ARGUMENTS
    '''
    if len(p) > 2:
        print(f"Command: {p[1]}, Arguments: {p[2]}")
        p[0] = (p[1], p[2])
    else:
        print(f"Command: {p[1]}, No arguments")
        p[0] = (p[1], [])

def p_arguments(p):
    '''
    ARGUMENTS : ARGUMENT
              | ARGUMENT ARGUMENTS
    '''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Lista global para almacenar el historial de comandos
command_history = []

def execute_command(parsed_command):
    command, args = parsed_command
    full_command = f"{command} {' '.join(args)}"
    
    # Guardar el comando en el historial
    command_history.append(full_command)
    
    try:
        if command == "cd":
            if not args:
                # Si no hay argumentos, ir al directorio home del usuario
                home_dir = os.path.expanduser("~")
                os.chdir(home_dir)
                return f"Changed directory to {home_dir}"
            
            path = args[0]
            # Manejar cd .. y otras rutas relativas
            if path == "..":
                os.chdir("..")
            elif path.startswith("~"):
                # Expandir ~ al directorio home del usuario
                expanded_path = os.path.expanduser(path)
                os.chdir(expanded_path)
            else:
                os.chdir(path)
            return f"Changed directory to {os.getcwd()}"
        
        elif command == "ping":
            if not args:
                return "Error: Debe especificar un host"
                
            # Unir todos los argumentos para formar el nombre del host completo
            host = ''.join(args)
            
            try:
                # Ejecutar el comando ping
                if platform.system().lower() == "windows":
                    process = subprocess.Popen(['ping', host], 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
                else:
                    # En sistemas Unix/Linux, usar -c 4 para limitar a 4 pings
                    process = subprocess.Popen(['ping', '-c', '4', host], 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
                    
                output, error = process.communicate()
                
                if process.returncode == 0:
                    return output.decode('utf-8', errors='ignore')
                else:
                    return f"Error al hacer ping a {host}: {error.decode('utf-8', errors='ignore')}"
                    
            except Exception as e:
                return f"Error al ejecutar ping: {str(e)}"

        elif command == "ipconfig":
            try:
                # Adaptar el comando según el sistema operativo
                if os.name == "nt":  # Windows
                    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
                else:  # Linux/Unix
                    # Intentar ifconfig primero, si no está disponible usar ip addr
                    try:
                        result = subprocess.run(["ifconfig"], capture_output=True, text=True)
                    except FileNotFoundError:
                        result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Formatear la salida para que sea más legible
                    output = result.stdout
                    # Eliminar líneas vacías múltiples
                    output = re.sub(r'\n\s*\n', '\n\n', output)
                    return output
                else:
                    return f"Error al obtener información de red: {result.stderr}"
            except Exception as e:
                return f"Error al ejecutar el comando: {str(e)}"

        elif command == "netstat":
            try:
                # Adaptar el comando según el sistema operativo
                if os.name == "nt":  # Windows
                    result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
                else:  # Linux/Unix
                    # En Linux, añadimos -tulpn para mostrar servicios y PID
                    result = subprocess.run(["netstat", "-tulpn"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Formatear la salida para que sea más legible
                    output = result.stdout
                    # Filtrar y ordenar la información más relevante
                    lines = output.split('\n')
                    # Mantener el encabezado y las conexiones activas
                    filtered_lines = [line for line in lines if line.strip() and 
                                    ('Proto' in line or 'ESTABLISHED' in line or 'LISTEN' in line)]
                    return '\n'.join(filtered_lines)
                else:
                    return f"Error al obtener estadísticas de red: {result.stderr}"
            except Exception as e:
                return f"Error al ejecutar netstat: {str(e)}"

        elif command == "dig":
            if not args:
                return "Error: Debe especificar un dominio. Ejemplo: dig google.com"
            
            # Unir todos los argumentos para formar el nombre del host completo
            domain = ''.join(args)
            record_type = "A"  # Tipo de registro predeterminado
            
            # Si se especifica un tipo de registro
            if len(args) > 1 and args[-1].upper() in ["A", "AAAA", "MX", "NS", "TXT", "SOA"]:
                record_type = args[-1].upper()
                domain = ''.join(args[:-1])
            
            try:
                # En Windows, no existe dig, usamos nslookup
                if os.name == "nt":
                    if record_type == "A":
                        result = subprocess.run(["nslookup", domain], capture_output=True, text=True)
                    else:
                        result = subprocess.run(["nslookup", "-type=" + record_type, domain], 
                                                capture_output=True, text=True)
                else:
                    # En Linux/Unix, intentar usar dig
                    try:
                        result = subprocess.run(["dig", domain, record_type], 
                                                capture_output=True, text=True)
                    except FileNotFoundError:
                        # Si dig no está disponible, usar nslookup como alternativa
                        result = subprocess.run(["nslookup", "-type=" + record_type, domain], 
                                                capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Formatear la salida para que sea más legible
                    output = result.stdout
                    # Filtrar las líneas más relevantes
                    lines = output.split('\n')
                    filtered_lines = [line for line in lines if line.strip() and 
                                    not line.startswith(';') and 
                                    not line.startswith('_')]
                    return '\n'.join(filtered_lines)
                else:
                    return f"Error al realizar la búsqueda DNS: {result.stderr}"
            except Exception as e:
                return f"Error al ejecutar la búsqueda DNS: {str(e)}"
        
        elif command == "mv":
            if len(args) < 2:
                return "Error: mv requiere origen y destino"
            
            # Procesar argumentos para origen y destino
            source_args = []
            dest_args = []
            found_source = False
            
            for i, arg in enumerate(args):
                if not found_source:
                    source_args.append(arg)
                    if '.' in ''.join(source_args):  # Buscamos si encontramos una extensión
                        found_source = True
                else:
                    dest_args.append(arg)
            
            # Unir los argumentos para formar los nombres completos
            source = ''.join(source_args)
            destination = ''.join(dest_args)
            
            try:
                # Expandir ~ si está presente en las rutas
                if source.startswith('~'):
                    source = os.path.expanduser(source)
                if destination.startswith('~'):
                    destination = os.path.expanduser(destination)
                
                # Realizar el movimiento/renombrado
                shutil.move(source, destination)
                return f"Movido/renombrado: {source} -> {destination}"
            except FileNotFoundError:
                return f"Error: Archivo o directorio no encontrado: {source}"
            except PermissionError:
                return "Error: Sin permisos suficientes"
            except shutil.Error as e:
                return f"Error al mover/renombrar: {str(e)}"
                
        elif command == "cp":
            if len(args) < 2:
                return "Error: cp requiere origen y destino"
            
            recursive = False
            start_idx = 0
            
            # Verificar si hay flag -r
            if args[0].startswith('-') and 'r' in args[0]:
                recursive = True
                start_idx += 1
                
            if len(args) < start_idx + 2:
                return "Error: cp requiere origen y destino"
            
            # Procesar argumentos para origen y destino
            source_args = []
            dest_args = []
            found_source = False
            
            for i, arg in enumerate(args[start_idx:], start=start_idx):
                if not found_source:
                    source_args.append(arg)
                    if '.' in ''.join(source_args):  # Buscamos si encontramos una extensión
                        found_source = True
                else:
                    dest_args.append(arg)
            
            # Unir los argumentos para formar los nombres completos
            source = ''.join(source_args)
            destination = ''.join(dest_args)
            
            if not '.' in destination:
                return "Error: El archivo destino debe tener una extensión"
            
            try:
                # Expandir ~ si está presente
                if source.startswith('~'):
                    source = os.path.expanduser(source)
                if destination.startswith('~'):
                    destination = os.path.expanduser(destination)
                
                if os.path.isdir(source):
                    if not recursive:
                        return "Error: Para copiar directorios use -r"
                    shutil.copytree(source, destination)
                    return f"Directorio copiado: {source} -> {destination}"
                else:
                    shutil.copy2(source, destination)
                    return f"Archivo copiado: {source} -> {destination}"
            except FileNotFoundError:
                return f"Error: Archivo o directorio no encontrado: {source}"
            except PermissionError:
                return "Error: Sin permisos suficientes"
            except shutil.Error as e:
                return f"Error al copiar: {str(e)}"
                        
        elif command == "zip":
            if not args:
                return "Error: Debe especificar nombre del archivo zip y archivos a comprimir"
            
            # Procesar argumentos
            recursive = False
            start_idx = 0
            
            # Verificar flags si existen
            if args[0].startswith('-'):
                if 'r' in args[0]:
                    recursive = True
                start_idx += 1
            
            # Necesitamos al menos el nombre del zip y un archivo para comprimir
            if len(args) < start_idx + 2:
                return "Error: Debe especificar nombre del archivo zip y archivos a comprimir"
            
            # Obtener el nombre del archivo zip (primer argumento o segundo si hay flag)
            zip_args = []
            file_args = []
            found_zip = False
            
            for i, arg in enumerate(args[start_idx:], start=start_idx):
                if not found_zip:
                    zip_args.append(arg)
                    if '.zip' in ''.join(zip_args):
                        found_zip = True
                else:
                    file_args.append(arg)
            
            # Unir los argumentos para formar los nombres completos
            zip_name = ''.join(zip_args)
            if not zip_name.endswith('.zip'):
                zip_name += '.zip'
            
            # Unir los argumentos para el archivo a comprimir
            files_to_zip = ''.join(file_args)
            
            try:
                import zipfile
                
                with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                    if os.path.isdir(files_to_zip):
                        if not recursive:
                            return f"Error: {files_to_zip} es un directorio. Use -r para comprimir directorios"
                        for root, dirs, files in os.walk(files_to_zip):
                            for file in files:
                                full_path = os.path.join(root, file)
                                arcname = os.path.relpath(full_path, os.path.dirname(files_to_zip))
                                zipf.write(full_path, arcname)
                    else:
                        if os.path.exists(files_to_zip):
                            zipf.write(files_to_zip, os.path.basename(files_to_zip))
                        else:
                            return f"Error: Archivo no encontrado: {files_to_zip}"
                
                return f"Archivo zip creado exitosamente: {zip_name}"
                
            except FileNotFoundError:
                return "Error: Uno o más archivos no encontrados"
            except PermissionError:
                return "Error: Sin permisos suficientes"
            except Exception as e:
                return f"Error al crear el archivo zip: {str(e)}"
        
        elif command == "unzip":
            if not args:
                return "Error: Debe especificar un archivo zip"
            
            # Procesar argumentos para manejar la opción -d
            zip_file = None
            extract_dir = None
            i = 0
            temp_args = []  # Para almacenar temporalmente los argumentos del nombre del archivo
            
            while i < len(args):
                if args[i] == '-d':
                    # Si encontramos -d, procesamos el directorio y salimos del bucle
                    if i + 1 >= len(args):
                        return "Error: La opción -d requiere especificar un directorio"
                    extract_dir = ''.join(args[i+1:])
                    break
                else:
                    # Acumulamos los argumentos hasta encontrar -d
                    temp_args.append(args[i])
                i += 1
            
            # Unir todos los argumentos acumulados para formar el nombre del archivo
            zip_file = ''.join(temp_args) if temp_args else None
            
            if not zip_file:
                return "Error: Debe especificar un archivo zip"
            
            if not zip_file.endswith('.zip'):
                return "Error: El archivo debe tener extensión .zip"
            
            try:
                import zipfile
                
                # Si se especificó un directorio de destino, verificar/crear el directorio
                if extract_dir:
                    # Expandir ~ si está presente
                    if extract_dir.startswith('~'):
                        extract_dir = os.path.expanduser(extract_dir)
                    
                    # Crear el directorio si no existe
                    os.makedirs(extract_dir, exist_ok=True)
                
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    # Extraer al directorio especificado o al actual si no se especificó
                    zip_ref.extractall(path=extract_dir)
                
                extract_location = extract_dir if extract_dir else "directorio actual"
                return f"Archivo {zip_file} descomprimido exitosamente en {extract_location}"
                
            except zipfile.BadZipFile:
                return "Error: Archivo zip corrupto o inválido"
            except FileNotFoundError:
                return "Error: Archivo zip no encontrado"
            except PermissionError:
                return "Error: Sin permisos suficientes para extraer en el directorio especificado"
                
        elif command == "rm":
            if not args:
                return "Error: Debe especificar al menos un archivo o directorio"
            
            # Procesar flags
            recursive = False
            force = False
            targets = []
            
            for arg in args:
                if arg.startswith('-'):
                    if 'r' in arg:
                        recursive = True
                    if 'f' in arg:
                        force = True
                else:
                    targets.append(arg)
            
            if not targets:
                return "Error: Debe especificar al menos un archivo o directorio para eliminar"
            
            # Unir los argumentos para formar los nombres completos
            targets = [''.join(targets)]
            
            results = []
            for target in targets:
                try:
                    if os.path.isdir(target):
                        if not recursive:
                            results.append(f"Error: {target} es un directorio. Use -r para eliminar directorios")
                            continue
                        shutil.rmtree(target, ignore_errors=force)
                    else:
                        os.remove(target)
                    results.append(f"Eliminado: {target}")
                except FileNotFoundError:
                    if not force:
                        results.append(f"Error: {target} no encontrado")
                except PermissionError:
                    if not force:
                        results.append(f"Error: Sin permisos para eliminar {target}")
            
            return "\n".join(results)
        
        elif command == "help":
            return (
                "Comandos disponibles:\n"
                "help - Muestra la lista de comandos.\n"
                "ls - Lista archivos en el directorio actual.\n"
                "echo - Muestra texto. Ejemplo: echo \"Hola Mundo\"\n"
                "cat - Muestra el contenido de un archivo. Ejemplo: cat archivo.txt\n"
                "mkdir - Crea un nuevo directorio.\n"
                "pwd - Muestra el directorio actual.\n"
                "cd - Cambia el directorio actual. Ejemplo: cd /ruta/destino\n"
                "unzip - Extrae archivos de un zip. Ejemplo: unzip archivo.zip [-d directorio]\n"
                "rm - Elimina archivos o directorios. Ejemplo: rm archivo.txt o rm -rf directorio\n"
                "mv - Mueve o renombra archivos y directorios. Ejemplo: mv origen destino\n"
                "cp - Copia archivos y directorios. Ejemplo: cp archivo1.txt archivo2.txt o cp -r dir1 dir2\n"
                "zip - Comprime archivos en formato ZIP. Ejemplo: zip archivo.zip archivo.txt o zip -r archivo.zip directorio\n"
                "history - Muestra el historial de comandos ejecutados.\n"
                "clear - Limpia la pantalla del terminal.\n"
                "ping - Verifica la conectividad con un servidor. Ejemplo: ping google.com\n"
                "ipconfig - Muestra la configuración de red del sistema\n"
                "netstat - Muestra información de conexiones de red activas\n"
                "dig - Realiza búsquedas DNS. Ejemplo: dig google.com [A|MX|NS|TXT]\n"
            )
            
        elif command == "ls":
            result = subprocess.run("dir" if os.name == "nt" else "ls", shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        elif command == "echo":
            return ' '.join(args)
        elif command == "cat":
            if not args:
                return "Error: No se especificó un archivo."
            try:
                filename = ''.join(args)  # Une los argumentos para formar el nombre completo del archivo
                with open(filename, 'r') as file:
                    return file.read()
            except FileNotFoundError:
                return "Archivo no encontrado."
        elif command == "mkdir":
            try:
                os.mkdir(args[0])
                return "Directorio creado."
            except FileExistsError:
                return "El directorio ya existe."
        elif command == "pwd":
            return os.getcwd()
        elif command == "history":
            history_output = ["  Id CommandLine", "  -- -----------"]
            for idx, cmd in enumerate(command_history, start=1):
                history_output.append(f"   {idx} {cmd}")
            return "\n".join(history_output)
        elif command == "clear" or command == "cls":
            return "CLEAR_SCREEN"  # Special signal to clear the screen
        else:
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# Ejemplo de uso
if __name__ == "__main__":
    while True:
        try:
            command_input = input(f"{os.getcwd()}> ")
            if command_input.lower() == 'exit':
                break
            
            parsed_command = parser.parse(command_input)
            if parsed_command:
                result = execute_command(parsed_command)
                if result == "CLEAR_SCREEN":
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    print(result)
            else:
                print("Error: No se pudo parsear el comando correctamente.")
        except KeyboardInterrupt:
            print("\nPara salir, escriba 'exit'")
        except Exception as e:
            print(f"Error: {str(e)}")