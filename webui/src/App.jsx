import { useState } from 'react'
import TradeWindsText from './TradeWindsText'
import './App.css'

function App() {
  const [currentApp, setCurrentApp] = useState('home')

  if (currentApp === 'tradewinds') {
    return <TradeWindsText onBack={() => setCurrentApp('home')} />
  }

  return (
    <div className="app-launcher">
      <div className="launcher-header">
        <h1>🌌 OpenWeb UI</h1>
        <p>Your Gateway to Space Adventures</p>
      </div>
      
      <div className="app-grid">
        <div className="app-card" onClick={() => setCurrentApp('tradewinds')}>
          <div className="app-icon">🚀</div>
          <h3>TradeWinds</h3>
          <p>Interactive Text Adventure</p>
          <div className="app-features">
            <span>📖 Rich Descriptions</span>
            <span>⌨️ Command Parser</span>
            <span>🌌 Space Trading</span>
          </div>
        </div>
        
        <div className="app-card coming-soon">
          <div className="app-icon">🌍</div>
          <h3>BlobWorld</h3>
          <p>Coming Soon...</p>
        </div>
        
        <div className="app-card coming-soon">
          <div className="app-icon">🔧</div>
          <h3>More Apps</h3>
          <p>Stay Tuned!</p>
        </div>
      </div>
      
      <footer className="launcher-footer">
        <p>Built with React + Vite</p>
      </footer>
    </div>
  )
}

export default App
