import { useState, useEffect, useRef } from 'react'
import './TradeWindsText.css'

// Import the game logic (converted to JavaScript)
import { GameEngine } from './gameLogic.js'

function TradeWindsText({ onBack = null }) {
  const [gameOutput, setGameOutput] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [gameEngine] = useState(() => new GameEngine())
  const [gameStarted, setGameStarted] = useState(false)
  const [playerName, setPlayerName] = useState('')
  const [shipName, setShipName] = useState('')
  const outputRef = useRef(null)
  const inputRef = useRef(null)

  // Auto-scroll to bottom when new output is added
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight
    }
  }, [gameOutput])

  // Focus input when game starts
  useEffect(() => {
    if (gameStarted && inputRef.current) {
      inputRef.current.focus()
    }
  }, [gameStarted])

  const addOutput = (text, type = 'normal') => {
    setGameOutput(prev => [...prev, { text, type, timestamp: Date.now() }])
  }

  const startGame = () => {
    const captainName = playerName.trim() || 'Captain'
    const vesselName = shipName.trim() || 'Starwind'
    
    gameEngine.initializeGame(captainName, vesselName)
    setGameStarted(true)
    
    // Display initial game output
    addOutput('=' * 60, 'separator')
    addOutput('🚀 TRADEWINDS: A SPACE TRADING ADVENTURE 🚀', 'title')
    addOutput('=' * 60, 'separator')
    addOutput('')
    addOutput(`Welcome aboard, ${captainName}!`, 'success')
    addOutput(`You command the starship '${vesselName}'.`, 'success')
    addOutput('')
    addOutput('You begin your trading career with 1,000 credits and a cargo', 'description')
    addOutput('hold that can carry 50 units of goods. Your ship is currently', 'description')
    addOutput('docked at Earth Station in the Sol System.', 'description')
    addOutput('')
    addOutput("Type 'help' for a list of commands, or just start exploring!", 'prompt')
    addOutput('=' * 60, 'separator')
    addOutput('')
    
    // Show initial location
    const locationOutput = gameEngine.lookAround()
    locationOutput.forEach(line => {
      addOutput(line.text, line.type)
    })
  }

  const processCommand = (e) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const command = inputValue.trim()
    
    // Display the command
    addOutput(`${gameEngine.getPlayerName()}> ${command}`, 'input')
    
    // Process the command through the game engine
    const output = gameEngine.processCommand(command)
    
    // Display the output
    output.forEach(line => {
      addOutput(line.text, line.type)
    })
    
    // Clear input
    setInputValue('')
  }

  if (!gameStarted) {
    return (
      <div className="tradewinds-text-game">
        {onBack && (
          <button className="back-button" onClick={onBack}>
            ← Back to Launcher
          </button>
        )}
        
        <div className="start-screen">
          <div className="terminal-title">
            <div className="terminal-header">
              <span className="terminal-dots">●●●</span>
              <span className="terminal-title-text">TradeWinds Terminal</span>
            </div>
          </div>
          
          <div className="terminal-content">
            <div className="ascii-art">
              <pre>{`
    ████████╗██████╗  █████╗ ██████╗ ███████╗██╗    ██╗██╗███╗   ██╗██████╗ ███████╗
    ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██║    ██║██║████╗  ██║██╔══██╗██╔════╝
       ██║   ██████╔╝███████║██║  ██║█████╗  ██║ █╗ ██║██║██╔██╗ ██║██║  ██║███████╗
       ██║   ██╔══██╗██╔══██║██║  ██║██╔══╝  ██║███╗██║██║██║╚██╗██║██║  ██║╚════██║
       ██║   ██║  ██║██║  ██║██████╔╝███████╗╚███╔███╔╝██║██║ ╚████║██████╔╝███████║
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝
              `}</pre>
            </div>
            
            <div className="game-info">
              <p className="subtitle">A Space Trading Text Adventure</p>
              <p>Explore real star systems • Trade across the galaxy • Build your fortune</p>
            </div>
            
            <div className="start-form">
              <div className="form-group">
                <label>CAPTAIN'S NAME:</label>
                <input
                  type="text"
                  value={playerName}
                  onChange={(e) => setPlayerName(e.target.value)}
                  placeholder="Captain"
                  className="terminal-input"
                  onKeyDown={(e) => e.key === 'Enter' && document.getElementById('ship-name').focus()}
                />
              </div>
              
              <div className="form-group">
                <label>SHIP NAME:</label>
                <input
                  id="ship-name"
                  type="text"
                  value={shipName}
                  onChange={(e) => setShipName(e.target.value)}
                  placeholder="Starwind"
                  className="terminal-input"
                  onKeyDown={(e) => e.key === 'Enter' && startGame()}
                />
              </div>
              
              <button className="start-button" onClick={startGame}>
                >> INITIALIZE SYSTEMS <<
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="tradewinds-text-game">
      {onBack && (
        <button className="back-button" onClick={onBack}>
          ← Back to Launcher
        </button>
      )}
      
      <div className="terminal">
        <div className="terminal-header">
          <span className="terminal-dots">●●●</span>
          <span className="terminal-title-text">TradeWinds - Space Trading Terminal</span>
          <span className="terminal-status">
            Credits: {gameEngine.getCredits().toLocaleString()} | 
            Cargo: {gameEngine.getCargoCount()}/50 | 
            Days: {gameEngine.getDaysElapsed()}
          </span>
        </div>
        
        <div className="terminal-output" ref={outputRef}>
          {gameOutput.map((line, index) => (
            <div key={index} className={`output-line ${line.type}`}>
              {line.text === '' ? '\u00A0' : line.text}
            </div>
          ))}
          
          <div className="cursor-line">
            <span className="prompt">{gameEngine.getPlayerName()}> </span>
            <span className="cursor">_</span>
          </div>
        </div>
        
        <form className="terminal-input-area" onSubmit={processCommand}>
          <span className="input-prompt">{gameEngine.getPlayerName()}> </span>
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className="terminal-input"
            autoComplete="off"
            spellCheck="false"
          />
        </form>
      </div>
    </div>
  )
}

export default TradeWindsText