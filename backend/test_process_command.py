import sys
from cli import process_command

def test_command(command):
    """
    Prueba un comando y muestra el análisis léxico y el resultado de la ejecución
    de manera formateada
    """
    print(f"\n{'='*50}")
    print(f"Probando comando: '{command}'")
    print(f"{'='*50}\n")
    
    result = process_command(command)
    
    # Mostrar análisis léxico
    print("ANÁLISIS LÉXICO:")
    print("-" * 40)
    if result["lexical_analysis"]:
        print(f"{'#':^5} | {'Valor':^20} | {'Tipo':^15}")
        print("-" * 45)
        for token in result["lexical_analysis"]:
            print(f"{token['numero']:^5} | {str(token['valor']):^20} | {token['tipo']:^15}")
    else:
        print("No se encontraron tokens")
    
    # Mostrar resultado de la ejecución
    print("\nRESULTADO DE LA EJECUCIÓN:")
    print("-" * 40)
    print(result["execution_result"])
    print("\n")

def main():
    # Lista de comandos de prueba
    test_commands = [
        "ls",
        "pwd",
        "echo Hola Mundo",
        "ping google.com",
        "help"
    ]
    
    # Si se proporcionan argumentos en la línea de comandos, usar esos en lugar de los predefinidos
    if len(sys.argv) > 1:
        test_commands = [' '.join(sys.argv[1:])]
    
    # Ejecutar las pruebas
    for command in test_commands:
        test_command(command)

if __name__ == "__main__":
    main()