import subprocess
import os
from ply import lex, yacc

# Lexer for command parsing
tokens = (
    'COMMAND',
    'ARGUMENT'
)

# Lista de comandos válidos
commands_list = ['cat', 'ls', 'echo', 'mkdir', 'pwd', 'cd', 'help']

# Define the command tokens
def t_COMMAND(t):
    r'[a-zA-Z]+'
    if t.value in commands_list:
        return t
    else:
        t.type = 'ARGUMENT'  # Si no es un comando válido, debe ser un argumento
        return t

# Define the argument tokens
t_ARGUMENT = r'[^\s]+'  # Cualquier secuencia no separada por espacios (incluye puntos, guiones, etc.)

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

def execute_command(parsed_command):
    command, args = parsed_command
    full_command = f"{command} {' '.join(args)}"
    
    try:
        if command == "cd":
            path = args[0] if args else ""
            os.chdir(path)
            return f"Changed directory to {os.getcwd()}"
        elif command == "help":
            return (
                "Comandos disponibles:\n"
                "help - Muestra la lista de comandos.\n"
                "ls - Lista archivos en el directorio actual.\n"
                "echo - Muestra texto. Ejemplo: echo \"Hola Mundo\"\n"
                "cat - Muestra el contenido de un archivo. Ejemplo: cat archivo.txt\n"
                "mkdir - Crea un nuevo directorio.\n"
                "pwd - Muestra el directorio actual.\n"
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
        else:
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# Tokeniza y depura el comando
command_input = 'cat hola.txt'

# Tokenizing
lexer.input(command_input)
print("Lexing input...")
for token in lexer:
    print(token)

# Parsing
print("Parsing input...")
parsed_command = parser.parse(command_input)

if parsed_command:
    print(f"Parsed command: {parsed_command}")
    result = execute_command(parsed_command)
    print(f"Execution result: {result}")
else:
    print("Error: No se pudo parsear el comando correctamente.")