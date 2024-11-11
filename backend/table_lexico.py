import ply.lex as lex

# Lista expandida de tokens
tokens = [
    'COMANDO',           # Comandos del sistema
    'FLAG',             # Opciones que comienzan con -
    'ARGUMENTO',        # Argumentos generales
    'RUTA',            # Rutas de directorios y archivos
    'RUTA_ABSOLUTA',   # Rutas que comienzan con /
    'RUTA_RELATIVA',   # Rutas relativas (./,../)
    'ARCHIVO',         # Nombres de archivo con extensión
    'EXTENSION',       # Extensiones de archivo
    'NUMERO',          # Valores numéricos
    'IP',             # Direcciones IP
    'MASCARA_RED',     # Máscaras de red (255.255.255.0 o /24)
    'PUERTO',          # Números de puerto
    'PROTOCOLO',       # Protocolos de red (TCP, UDP)
    'MAC',            # Direcciones MAC
    'DOMINIO',        # Nombres de dominio
    'URL',            # URLs completas
    'SIMBOLO',        # Símbolos especiales
    'OPERADOR',       # Operadores como > < |
    'VARIABLE',       # Variables que comienzan con $
    'STRING',         # Cadenas entre comillas
    'COMODIN',        # Caracteres comodín (* ? [])
    'PIPE',           # Operador de tubería |
    'REDIRECCION',    # Operadores de redirección > >> <
    'HOST_USUARIO',   # Formato usuario@host
    'TIMESTAMP',      # Marcas de tiempo para history
    'PERMISOS'        # Permisos de archivo (ejemplo: 755, rwxr-xr-x)
]

# Lista de comandos válidos
commands_list = [
    'cat', 'ls', 'echo', 'mkdir', 'pwd', 'cd', 'help', 
    'history', 'clear', 'cls', 'unzip', 'rm', 'mv', 'cp', 'zip',
    'ping', 'ipconfig', 'netstat', 'dig'
]

# Patrones de expresiones regulares
def t_COMANDO(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value.lower() in commands_list:
        return t
    # Si no es un comando reconocido, será procesado por otras reglas
    t.type = 'ARGUMENTO'
    return t

def t_FLAG(t):
    r'-[a-zA-Z]+|--[a-zA-Z][a-zA-Z0-9-]*'
    return t

def t_IP(t):
    r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    # Validación básica de IP
    octetos = [int(num) for num in t.value.split('.')]
    if all(0 <= num <= 255 for num in octetos):
        return t
    t.type = 'ARGUMENTO'
    return t

def t_MASCARA_RED(t):
    r'/\d{1,2}|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    return t

def t_PUERTO(t):
    r':\d{1,5}'
    t.value = t.value[1:]  # Eliminar los dos puntos
    return t

def t_PROTOCOLO(t):
    r'(?:TCP|UDP|ICMP|HTTP|HTTPS|FTP|SSH|TELNET)'
    t.value = t.value.upper()  # Convertir a mayúsculas para consistencia
    return t

def t_MAC(t):
    r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}'
    return t

def t_URL(t):
    r'https?://[\w\-.]+(:\d+)?(/[\w\-./?%&=]*)?'
    return t

def t_DOMINIO(t):
    r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
    if not any(t.value.startswith(prefix) for prefix in ['http://', 'https://']):
        return t
    t.type = 'ARGUMENTO'
    return t

def t_HOST_USUARIO(t):
    r'[a-zA-Z0-9_-]+@[a-zA-Z0-9.-]+'
    return t

def t_TIMESTAMP(t):
    r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\d{10}'
    return t

def t_PERMISOS(t):
    r'[0-7]{3,4}|[rwx-]{9}'
    return t

def t_RUTA_ABSOLUTA(t):
    r'/(?:[a-zA-Z0-9._-]+/)*[a-zA-Z0-9._-]*'
    return t

def t_RUTA_RELATIVA(t):
    r'\.{1,2}/(?:[a-zA-Z0-9._-]+/)*[a-zA-Z0-9._-]*'
    return t

def t_ARCHIVO(t):
    r'[a-zA-Z0-9_-]+\.[a-zA-Z0-9]+'
    return t

def t_EXTENSION(t):
    r'\.[a-zA-Z0-9]+'
    return t

def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_STRING(t):
    r'\"[^\"]*\"|\'[^\']*\''
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_PIPE(t):
    r'\|'
    return t

def t_REDIRECCION(t):
    r'>>|>|<'
    return t

def t_COMODIN(t):
    r'\*|\?|\[\^?\]?[^\]]*\]'
    return t

def t_OPERADOR(t):
    r'[><|&;]+'
    return t

def t_SIMBOLO(t):
    r'[./\-_@:~#$%^&*()+={}[\]\\]'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

def analyze_command(command_string):
    """
    Analiza un comando y retorna una lista de tuplas (valor, tipo)
    """
    lexer.input(command_string)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.value, tok.type))
    return tokens

def print_token_table(tokens):
    """
    Imprime una tabla formateada con los tokens y sus tipos, incluyendo numeración
    """
    # Encontrar el ancho máximo para cada columna
    max_token_width = max(len(str(t[0])) for t in tokens)
    max_type_width = max(len(t[1]) for t in tokens)
    num_width = len(str(len(tokens)))  # Ancho para la columna de numeración
    
    # Asegurarse de que los encabezados quepan
    max_token_width = max(max_token_width, len("Token"))
    max_type_width = max(max_type_width, len("Tipo"))
    num_width = max(num_width, len("N."))
    
    # Crear la línea de separación
    separator = "-" * (max_token_width + max_type_width + num_width + 11)  # +11 por los espacios y separadores
    
    # Imprimir encabezados
    print(f"N.{' ' * (num_width - len('N.'))} | Token{' ' * (max_token_width - len('Token'))} | Tipo")
    print(separator)
    
    # Imprimir cada token con su número
    for i, (token_value, token_type) in enumerate(tokens, 1):
        # Ajustar el espaciado para alinear las columnas
        num_space = " " * (num_width - len(str(i)))
        token_space = " " * (max_token_width - len(str(token_value)))
        print(f"{i}{num_space} | {token_value}{token_space} | {token_type}")
        print(separator)

def process_command_input(command_string):
    """
    Procesa un comando de entrada y muestra el análisis en una tabla
    """
    tokens = analyze_command(command_string)
    print("\nAnálisis del comando:")
    print_token_table(tokens)
    return tokens

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplos de prueba con diferentes tipos de tokens
    test_commands = [
        "ping google.com -n 5",
        "cd /home/user/documents",
        "rm -rf temp_dir/*.txt",
        "cp file1.txt /path/to/destination/",
        "curl https://api.example.com:8080/data",
        "ssh user@192.168.1.100",
        "netstat -an | grep TCP",
        'echo "Hello World" > output.txt',
        "tar -czf archive.tar.gz /path/to/files/*.dat",
        "ipconfig /all",
        "dig @8.8.8.8 example.com"
    ]
    
    for cmd in test_commands:
        print(f"\nProcesando comando: {cmd}")
        process_command_input(cmd)