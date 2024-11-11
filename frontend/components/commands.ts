// commands.ts
export type Command = {
  id: string
  description: string
  example: string
  category: string  // Añadimos la categoría como nueva propiedad
  isExpanded?: boolean
  popupExpanded?: boolean
}

export const commands: Command[] = [
  // Comandos de ayuda y sistema
  {
      id: "help",
      description: "Muestra la lista completa de comandos disponibles con sus descripciones.",
      example: "help",
      category: "system",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "clear",
      description: "Limpia la pantalla del terminal.",
      example: "clear",
      category: "system",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "history",
      description: "Muestra el historial de comandos ejecutados en la sesión actual.",
      example: "history",
      category: "system",
      isExpanded: false,
      popupExpanded: false
  },

  // Comandos de navegación y listado
  {
      id: "pwd",
      description: "Muestra la ruta del directorio actual de trabajo.",
      example: "pwd",
      category: "navigation",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "ls",
      description: "Lista archivos y directorios en el directorio actual.",
      example: "ls",
      category: "navigation",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "cd",
      description: "Cambia el directorio actual. Usar '..' para subir un nivel o '~' para ir al directorio home.",
      example: "cd /ruta/destino",
      category: "navigation",
      isExpanded: false,
      popupExpanded: false
  },

  // Comandos de manipulación de archivos
  {
      id: "cat",
      description: "Muestra el contenido de un archivo de texto.",
      example: "cat archivo.txt",
      category: "file",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "echo",
      description: "Muestra texto en la terminal.",
      example: 'echo "Hola Mundo"',
      category: "file",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "mkdir",
      description: "Crea un nuevo directorio en la ubicación actual.",
      example: "mkdir nuevo_directorio",
      category: "file",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "rm",
      description: "Elimina archivos o directorios. Usa -r para directorios y -f para forzar la eliminación.",
      example: "rm archivo.txt | rm -rf directorio",
      category: "file",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "mv",
      description: "Mueve o renombra archivos y directorios.",
      example: "mv origen.txt destino.txt",
      category: "file",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "cp",
      description: "Copia archivos y directorios. Usa -r para copiar directorios de forma recursiva.",
      example: "cp archivo1.txt archivo2.txt | cp -r dir1 dir2",
      category: "file",
      isExpanded: false,
      popupExpanded: false
  },

  // Comandos de compresión
  {
      id: "zip",
      description: "Comprime archivos en formato ZIP. Usa -r para comprimir directorios de forma recursiva.",
      example: "zip archivo.zip archivo.txt | zip -r archivo.zip directorio",
      category: "compression",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "unzip",
      description: "Extrae archivos de un archivo ZIP. Opcionalmente especifica un directorio de destino con -d.",
      example: "unzip archivo.zip -d directorio_destino",
      category: "compression",
      isExpanded: false,
      popupExpanded: false
  },

  // Comandos de red
  {
      id: "ping",
      description: "Verifica la conectividad con un servidor mediante paquetes ICMP.",
      example: "ping google.com",
      category: "network",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "ipconfig",
      description: "Muestra la configuración de red del sistema (usa 'ip addr' en sistemas Unix).",
      example: "ipconfig",
      category: "network",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "netstat",
      description: "Muestra información de conexiones de red activas y puertos en escucha.",
      example: "netstat -an",
      category: "network",
      isExpanded: false,
      popupExpanded: false
  },
  {
      id: "dig",
      description: "Realiza búsquedas DNS. Soporta diferentes tipos de registros (A, MX, NS, TXT).",
      example: "dig google.com A",
      category: "network",
      isExpanded: false,
      popupExpanded: false
  }
]

// Definición de categorías para referencia
export const commandCategories = {
  system: "Sistema",
  navigation: "Navegación",
  file: "Archivos",
  compression: "Compresión",
  network: "Red"
}