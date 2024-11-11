"use client"

import * as React from "react"
import { 
  Github, 
  Home, 
  Layout, 
  Terminal as TerminalIcon, 
  Settings2, 
  Plus, 
  X, 
  ChevronRight, 
  ChevronDown, 
  Moon, 
  Sun,
  FolderTree,
  FileCode,
  Timer
} from "lucide-react"
import { cn } from "@/lib/utils"

type Command = {
  id: string
  description: string
  example: string
  isExpanded?: boolean
  popupExpanded?: boolean
}

type TabContent = {
  command: string
  output: string
  timestamp: string
}

type Tab = {
  id: string
  content: TabContent[]
}

type Suggestion = {
  id: string
  icon: React.ElementType
  label: string
  type: "command" | "directory"
}

export function Terminal() {
  const [activeTab, setActiveTab] = React.useState("pruebas")
  const [windowsExpanded, setWindowsExpanded] = React.useState(true)
  const [patternsExpanded, setPatternsExpanded] = React.useState(true)
  const [commandsExpanded, setCommandsExpanded] = React.useState(true)
  const [showConfigPopup, setShowConfigPopup] = React.useState(false)
  const [showCommandsPopup, setShowCommandsPopup] = React.useState(false)
  const [isDarkMode, setIsDarkMode] = React.useState(false)
  const [commandInput, setCommandInput] = React.useState("")
  const [showSuggestions, setShowSuggestions] = React.useState(false)
  
  const suggestions: Suggestion[] = [
    { id: "mkdir", icon: FolderTree, label: "mkdir", type: "command" },
    { id: "mkfs", icon: FileCode, label: "mkfs", type: "command" },
    { id: "mktemp", icon: Timer, label: "mktemp", type: "command" },
    { id: "mkdado", icon: FolderTree, label: "mkdado", type: "directory" },
  ]

  const [commands, setCommands] = React.useState<Command[]>([
    {
      id: "cd",
      description: "Cambia el directorio actual.",
      example: "cd Documents",
      isExpanded: false,
      popupExpanded: false
    },
    {
      id: "ping",
      description: "Envía paquetes ICMP a un host específico.",
      example: "ping google.com",
      isExpanded: false,
      popupExpanded: false
    },
    {
      id: "mkdir",
      description: "Crea un nuevo directorio.",
      example: "mkdir nuevo_directorio",
      isExpanded: false,
      popupExpanded: false
    },
    {
      id: "ls",
      description: "Lista el contenido del directorio actual.",
      example: "ls -la",
      isExpanded: false,
      popupExpanded: false
    },
    {
      id: "mv",
      description: "Mueve o renombra archivos y directorios.",
      example: "mv archivo.txt nuevo_nombre.txt",
      isExpanded: false,
      popupExpanded: false
    },
    {
      id: "echo",
      description: "Muestra un mensaje en la terminal.",
      example: "echo 'Hola Mundo'",
      isExpanded: false,
      popupExpanded: false
    },
    {
      id: "history",
      description: "Muestra el historial de comandos.",
      example: "history",
      isExpanded: false,
      popupExpanded: false
    }
  ])
  
  const [tabs, setTabs] = React.useState<Tab[]>([
    { id: "pruebas", content: [] },
    { id: "data", content: [] },
    { id: "game", content: [] },
  ])

  const filteredSuggestions = React.useMemo(() => {
    if (!commandInput) return []
    return suggestions.filter(s => 
      s.label.toLowerCase().startsWith(commandInput.toLowerCase())
    )
  }, [commandInput, suggestions])

  const toggleCommandExpanded = (commandId: string, isPopup: boolean = false) => {
    setCommands(prevCommands =>
      prevCommands.map(cmd =>
        cmd.id === commandId
          ? { 
              ...cmd, 
              isExpanded: isPopup ? cmd.isExpanded : !cmd.isExpanded,
              popupExpanded: isPopup ? !cmd.popupExpanded : cmd.popupExpanded
            }
          : cmd
      )
    )
  }

  const addCommand = (tabId: string, command: string) => {
    setTabs(prevTabs =>
      prevTabs.map(tab =>
        tab.id === tabId
          ? {
              ...tab,
              content: [
                ...tab.content,
                { command, output: `Output for: ${command}`, timestamp: new Date().toISOString() },
              ],
            }
          : tab
      )
    )
  }

  const closeTab = (tabId: string) => {
    if (tabs.length > 1) {
      const newTabs = tabs.filter(tab => tab.id !== tabId)
      setTabs(newTabs)
      if (activeTab === tabId) {
        setActiveTab(newTabs[0].id)
      }
    }
  }

  const addNewTab = () => {
    const newTabId = `tab${tabs.length + 1}`
    setTabs(prev => [...prev, { id: newTabId, content: [] }])
    setActiveTab(newTabId)
  }

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
    document.documentElement.classList.toggle('dark')
  }

  return (
    <div className="flex min-h-screen bg-white text-zinc-900 dark:bg-zinc-900 dark:text-zinc-100 font-sans">
      {/* Left Sidebar */}
      <div className="w-64 border-r border-zinc-200 dark:border-zinc-800">
        <div className="p-4">
          <a
            href="https://github.com/yourusername/linux-cli"
            className="group flex items-center gap-2 rounded-full bg-lime-100 px-4 py-2 dark:bg-lime-900"
          >
            <Github className="h-5 w-5 text-black dark:text-white" />
            <span className="font-mono font-bold text-black dark:text-white">Linux CLI</span>
          </a>
        </div>
        <nav className="space-y-1 p-2">
          <button className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800">
            <Home className="h-4 w-4" />
            Inicio
          </button>
          <div>
            <button
              className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
              onClick={() => setWindowsExpanded(!windowsExpanded)}
            >
              <div className="flex items-center gap-2">
                <Layout className="h-4 w-4" />
                Ventanas
              </div>
              <ChevronDown className={cn("h-4 w-4 transition-transform", windowsExpanded && "rotate-180")} />
            </button>
            {windowsExpanded && (
              <div className="ml-4 space-y-1 pt-1">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    className={cn(
                      "flex w-full items-center gap-2 rounded-lg px-3 py-2",
                      activeTab === tab.id
                        ? "bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-zinc-100"
                        : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
                    )}
                    onClick={() => setActiveTab(tab.id)}
                  >
                    <ChevronRight className="h-4 w-4" />
                    {tab.id.charAt(0).toUpperCase() + tab.id.slice(1)}
                  </button>
                ))}
              </div>
            )}
          </div>
          <button 
            className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
            onClick={() => setShowCommandsPopup(true)}
          >
            <TerminalIcon className="h-4 w-4" />
            Comandos
          </button>
          <button
            className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
            onClick={() => setShowConfigPopup(true)}
          >
            <Settings2 className="h-4 w-4" />
            Configuración
          </button>
        </nav>
      </div>

      {/* Main Terminal Area */}
      <div className="flex-1">
        <div className="border-b border-zinc-200 p-4 dark:border-zinc-800">
          <h1 className="mb-4 text-2xl font-semibold">Terminal</h1>
          <div className="flex gap-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                className={cn(
                  "flex items-center gap-2 rounded-lg border px-3 py-1.5",
                  activeTab === tab.id
                    ? "border-zinc-200 bg-white text-zinc-900 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-100"
                    : "border-transparent text-zinc-600 hover:border-zinc-200 hover:bg-zinc-50 dark:text-zinc-400 dark:hover:border-zinc-800 dark:hover:bg-zinc-800"
                )}
                onClick={() => setActiveTab(tab.id)}
              >
                <ChevronRight className="h-4 w-4" />
                {tab.id.charAt(0).toUpperCase() + tab.id.slice(1)}
                <button
                  className="ml-2 p-0.5 hover:bg-zinc-200 rounded-full dark:hover:bg-zinc-700"
                  onClick={(e) => {
                    e.stopPropagation()
                    closeTab(tab.id)
                  }}
                >
                  <X className="h-3 w-3" />
                </button>
              </button>
            ))}
            <button 
              className="rounded-lg p-1.5 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
              onClick={addNewTab}
            >
              <Plus className="h-4 w-4" />
            </button>
          </div>
        </div>
        <div className="p-4">
          <div className="font-mono space-y-4">
            {tabs.find(tab => tab.id === activeTab)?.content.map((entry, i) => (
              <div key={i} className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="text-red-600 dark:text-red-400">User ></span>
                  <span className="text-blue-600 dark:text-blue-400">{entry.command}</span>
                </div>
                {entry.output && (
                  <div className="rounded-lg bg-zinc-100 p-3 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400">
                    {entry.output}
                  </div>
                )}
              </div>
            ))}
            <div className="relative flex items-center gap-2">
              <span className="text-red-600 dark:text-red-400">User ></span>
              <input
                type="text"
                value={commandInput}
                onChange={(e) => {
                  setCommandInput(e.target.value)
                  setShowSuggestions(e.target.value.length > 0)
                }}
                className="flex-1 bg-transparent font-mono outline-none"
                placeholder="Escribe un comando..."
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    addCommand(activeTab, commandInput)
                    setCommandInput('')
                    setShowSuggestions(false)
                  }
                }}
              />
              {showSuggestions && filteredSuggestions.length > 0 && (
                <div className="absolute left-0 top-full mt-1 w-64 rounded-lg border border-zinc-200 bg-white shadow-lg dark:border-zinc-700 dark:bg-zinc-800">
                  {filteredSuggestions.map((suggestion) => (
                    <button
                      key={suggestion.id}
                      className="flex w-full items-center gap-2 px-3 py-2 hover:bg-zinc-100 dark:hover:bg-zinc-700"
                      onClick={() => {
                        setCommandInput(suggestion.label)
                        setShowSuggestions(false)
                      }}
                    >
                      <span className={cn(
                        "flex h-8 w-8 items-center justify-center rounded-full",
                        suggestion.type === "command" ? "bg-blue-500" : "bg-red-500"
                      )}>
                        <suggestion.icon className="h-4 w-4 text-white" />
                      </span>
                      <span>{suggestion.label}</span>
                      <span className="ml-auto text-xs text-zinc-400">{suggestion.type}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar */}
      <div className="w-80 border-l border-zinc-200 dark:border-zinc-800">
        <div className="border-b border-zinc-200 p-4 dark:border-zinc-800">
          <button
            className="flex w-full items-center justify-between"
            onClick={() => setPatternsExpanded(!patternsExpanded)}
          >
            <div className="flex items-center gap-2">
              <Layout className="h-4 w-4" />
              <span className="font-medium">Patrones</span>
            </div>
            <ChevronDown className={cn("h-4 w-4 transition-transform", patternsExpanded && "rotate-180")} />
          </button>
        </div>
        {patternsExpanded && (
          <div className="p-4">
            <table className="w-full">
              <thead>
                <tr className="text-left text-sm text-zinc-500 dark:text-zinc-400">
                  <th className="pb-2 font-medium">N.</th>
                  <th className="pb-2 font-medium">Token</th>
                  <th className="pb-2 font-medium">Descripción</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                <tr>
                  <td className="py-1">1</td>
                  <td className="py-1 text-blue-600 dark:text-blue-400">cat</td>
                  <td className="py-1">Comando</td>
                </tr>
                <tr>
                  <td className="py-1">2</td>
                  <td className="py-1">hola</td>
                  <td className="py-1">Texto</td>
                </tr>
                <tr>
                  <td className="py-1">3</td>
                  <td className="py-1">.</td>
                  <td className="py-1">Símbolo</td>
                </tr>
                <tr>
                  <td className="py-1">4</td>
                  <td className="py-1">txt</td>
                  <td className="py-1">Texto</td>
                </tr>
              </tbody>
            </table>
          </div>
        )}
        <div className="border-t border-zinc-200 p-4 dark:border-zinc-800">
          <button
            className="flex w-full items-center justify-between"
            onClick={() => setCommandsExpanded(!commandsExpanded)}
          >
            <div className="flex items-center gap-2">
              <TerminalIcon className="h-4 w-4" />
              <span className="font-medium">Comandos</span>
            </div>
            <ChevronDown className={cn("h-4 w-4 transition-transform", commandsExpanded && "rotate-180")} />
          </button>
          {commandsExpanded && (
            <div className="mt-2 space-y-1">
              {commands.map((cmd) => (
                <div key={cmd.id} className="rounded-lg">
                  <button
                    className={cn(
                      "flex w-full items-center justify-between rounded-lg px-3 py-2 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800",
                      cmd.isExpanded && "bg-zinc-100 dark:bg-zinc-800"
                    )}
                    onClick={() => toggleCommandExpanded(cmd.id)}
                  >
                    <div className="flex items-center gap-2">
                      <ChevronRight className={cn(
                        "h-4 w-4 transition-transform",
                        cmd.isExpanded && "rotate-90"
                      )} />
                      {cmd.id}
                    </div>
                    <ChevronDown className={cn(
                      "h-4 w-4 transition-transform",
                      cmd.isExpanded && "rotate-180"
                    )} />
                  </button>
                  {cmd.isExpanded && (
                    <div className="px-9 py-2 text-sm text-zinc-600 dark:text-zinc-400">
                      <p>{cmd.description}</p>
                      <p className="mt-1">Ejemplo: {cmd.example}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Commands Popup */}
      {showCommandsPopup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="w-[600px] max-h-[80vh] rounded-lg bg-white p-6 dark:bg-zinc-800">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Lista de Comandos</h2>
              <button
                className="rounded-lg p-2 hover:bg-zinc-100 dark:hover:bg-zinc-700"
                onClick={() => setShowCommandsPopup(false)}
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="overflow-y-auto max-h-[calc(80vh-8rem)]">
              <div className="space-y-2">
                {commands.map((cmd) => (
                  <div key={cmd.id} className="rounded-lg">
                    <button
                      className={cn(
                        "flex w-full items-center justify-between rounded-lg px-3 py-2 text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800",
                        cmd.popupExpanded && "bg-zinc-100 dark:bg-zinc-800"
                      )}
                      onClick={() => toggleCommandExpanded(cmd.id, true)}
                    >
                      <div className="flex items-center gap-2">
                        <ChevronRight className={cn(
                          "h-4 w-4 transition-transform",
                          cmd.popupExpanded && "rotate-90"
                        )} />
                        {cmd.id}
                      </div>
                      <ChevronDown className={cn(
                        "h-4 w-4 transition-transform",
                        cmd.popupExpanded && "rotate-180"
                      )} />
                    </button>
                    {cmd.popupExpanded && (
                      <div className="px-9 py-2 text-sm text-zinc-600 dark:text-zinc-400">
                        <p>{cmd.description}</p>
                        <p className="mt-1">Ejemplo: {cmd.example}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Configuration Popup */}
      {showConfigPopup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className="w-96 rounded-lg bg-white p-6 dark:bg-zinc-800">
            <h2 className="mb-4 text-xl font-semibold">Configuración</h2>
            <div className="flex items-center justify-between">
              <span>Tema</span>
              <button
                className="rounded-full bg-zinc-200 p-2 dark:bg-zinc-700"
                onClick={toggleDarkMode}
              >
                {isDarkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </button>
            </div>
            <button
              className="mt-4 w-full rounded-lg bg-zinc-200 px-4 py-2 text-zinc-800 hover:bg-zinc-300 dark:bg-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-600"
              onClick={() => setShowConfigPopup(false)}
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  )
}