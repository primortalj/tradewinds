import { useState, useEffect } from 'react'
import './TradeWinds.css'

// Game Data - converted from Python
const COMMODITIES = {
  "Food": { name: "Food", basePrice: 10, volatility: 0.15 },
  "Water": { name: "Water", basePrice: 5, volatility: 0.1 },
  "Medicine": { name: "Medicine", basePrice: 50, volatility: 0.3 },
  "Electronics": { name: "Electronics", basePrice: 100, volatility: 0.25 },
  "Metals": { name: "Metals", basePrice: 25, volatility: 0.2 },
  "Textiles": { name: "Textiles", basePrice: 15, volatility: 0.2 },
  "Weapons": { name: "Weapons", basePrice: 200, volatility: 0.4 },
  "Fuel": { name: "Fuel", basePrice: 20, volatility: 0.3 },
  "Luxury Goods": { name: "Luxury Goods", basePrice: 150, volatility: 0.35 },
  "Raw Materials": { name: "Raw Materials", basePrice: 8, volatility: 0.15 }
}

const LOCATIONS = {
  "Earth Station": {
    name: "Earth Station",
    system: "Sol",
    description: "Humanity's birthworld and primary trading hub. Orbital stations bustling with commerce.",
    produces: ["Luxury Goods", "Electronics", "Medicine"],
    consumes: ["Raw Materials", "Metals"],
    distanceFromEarth: 0
  },
  "Mars Colony": {
    name: "Mars Colony",
    system: "Sol",
    description: "The first major off-world colony. Red rock mining operations and terraforming efforts.",
    produces: ["Metals", "Raw Materials"],
    consumes: ["Food", "Water", "Medicine"],
    distanceFromEarth: 0
  },
  "Europa Station": {
    name: "Europa Station",
    system: "Sol",
    description: "Ice mining facility on Jupiter's moon. Source of the solar system's water supply.",
    produces: ["Water", "Fuel"],
    consumes: ["Electronics", "Food", "Textiles"],
    distanceFromEarth: 0
  },
  "Titan Refinery": {
    name: "Titan Refinery",
    system: "Sol",
    description: "Hydrocarbon processing on Saturn's largest moon. Industrial complex in perpetual twilight.",
    produces: ["Fuel", "Raw Materials"],
    consumes: ["Electronics", "Food"],
    distanceFromEarth: 0
  },
  "Proxima Colony": {
    name: "Proxima Colony",
    system: "Alpha Centauri",
    description: "Humanity's first interstellar colony orbiting Proxima Centauri. A testament to human determination.",
    produces: ["Food"],
    consumes: ["Electronics", "Medicine", "Luxury Goods"],
    distanceFromEarth: 4.37
  },
  "Sirius Trade Hub": {
    name: "Sirius Trade Hub",
    system: "Sirius",
    description: "Major commercial waystation in the bright Sirius system. Gateway to the outer colonies.",
    produces: ["Electronics", "Weapons"],
    consumes: ["Food", "Raw Materials"],
    distanceFromEarth: 8.6
  },
  "Vega Agricultural": {
    name: "Vega Agricultural",
    system: "Vega",
    description: "Vast agricultural worlds under Vega's bright light. Feeds much of human space.",
    produces: ["Food", "Textiles"],
    consumes: ["Electronics", "Metals", "Medicine"],
    distanceFromEarth: 25.3
  },
  "Altair Industrial": {
    name: "Altair Industrial",
    system: "Altair",
    description: "Heavy industry and manufacturing. The forge worlds of human space.",
    produces: ["Electronics", "Weapons", "Metals"],
    consumes: ["Raw Materials", "Food", "Water"],
    distanceFromEarth: 16.7
  },
  "Wolf 359 Outpost": {
    name: "Wolf 359 Outpost",
    system: "Wolf 359",
    description: "Remote mining outpost around a red dwarf star. Dangerous but profitable.",
    produces: ["Raw Materials", "Metals"],
    consumes: ["Food", "Water", "Medicine"],
    distanceFromEarth: 7.9
  },
  "TRAPPIST Research": {
    name: "TRAPPIST Research",
    system: "TRAPPIST-1",
    description: "Scientific research station studying the seven-planet system. Knowledge is power.",
    produces: ["Medicine", "Electronics"],
    consumes: ["Food", "Luxury Goods"],
    distanceFromEarth: 39.5
  },
  "Kepler Paradise": {
    name: "Kepler Paradise",
    system: "Kepler-452",
    description: "Earth-like world in the far reaches. Paradise for those who can afford the journey.",
    produces: ["Luxury Goods", "Food"],
    consumes: ["Electronics", "Medicine", "Weapons"],
    distanceFromEarth: 1400
  },
  "Gliese Station": {
    name: "Gliese Station",
    system: "Gliese 581",
    description: "Research and survey station in the habitable zone. Frontier science at its finest.",
    produces: ["Medicine"],
    consumes: ["Food", "Electronics", "Water"],
    distanceFromEarth: 20.4
  }
}

// Game utility functions
const getMarketPrice = (commodity, location) => {
  const base = COMMODITIES[commodity]
  let supplyDemand = 1.0
  
  if (location.produces.includes(commodity)) {
    supplyDemand = 0.6 + Math.random() * 0.2 // 0.6-0.8
  } else if (location.consumes.includes(commodity)) {
    supplyDemand = 1.2 + Math.random() * 0.4 // 1.2-1.6
  } else {
    supplyDemand = 0.9 + Math.random() * 0.2 // 0.9-1.1
  }
  
  const variation = (Math.random() - 0.5) * 2 * base.volatility
  const price = base.basePrice * (1 + variation) * supplyDemand
  return Math.max(1, Math.floor(price))
}

const getDistance = (loc1, loc2) => {
  if (loc1.system === loc2.system) return 0.1
  return Math.abs(loc1.distanceFromEarth - loc2.distanceFromEarth) + 1
}

function TradeWinds({ onBack = null }) {
  // Game state
  const [gameStarted, setGameStarted] = useState(false)
  const [player, setPlayer] = useState({
    name: '',
    shipName: '',
    credits: 1000,
    currentLocation: 'Earth Station',
    inventory: {},
    maxCargo: 50,
    daysElapsed: 0
  })
  const [currentScreen, setCurrentScreen] = useState('location') // location, market, travel, trade
  const [marketPrices, setMarketPrices] = useState({})

  // Generate market prices when location changes
  useEffect(() => {
    const location = LOCATIONS[player.currentLocation]
    const prices = {}
    Object.keys(COMMODITIES).forEach(commodity => {
      prices[commodity] = getMarketPrice(commodity, location)
    })
    setMarketPrices(prices)
  }, [player.currentLocation])

  const startGame = (captainName, shipName) => {
    setPlayer(prev => ({
      ...prev,
      name: captainName || 'Captain',
      shipName: shipName || 'Starwind'
    }))
    setGameStarted(true)
  }

  const getCargoCount = () => {
    return Object.values(player.inventory).reduce((sum, qty) => sum + qty, 0)
  }

  const buyCargo = (commodity, quantity) => {
    const totalCost = marketPrices[commodity] * quantity
    const newCargoCount = getCargoCount() + quantity
    
    if (player.credits >= totalCost && newCargoCount <= player.maxCargo) {
      setPlayer(prev => ({
        ...prev,
        credits: prev.credits - totalCost,
        inventory: {
          ...prev.inventory,
          [commodity]: (prev.inventory[commodity] || 0) + quantity
        }
      }))
      return true
    }
    return false
  }

  const sellCargo = (commodity, quantity) => {
    if (player.inventory[commodity] >= quantity) {
      const totalEarned = marketPrices[commodity] * quantity
      setPlayer(prev => ({
        ...prev,
        credits: prev.credits + totalEarned,
        inventory: {
          ...prev.inventory,
          [commodity]: prev.inventory[commodity] - quantity
        }
      }))
      return true
    }
    return false
  }

  const travelTo = (destinationName) => {
    const currentLoc = LOCATIONS[player.currentLocation]
    const destination = LOCATIONS[destinationName]
    const distance = getDistance(currentLoc, destination)
    const fuelCost = Math.max(10, Math.floor(distance * 5))
    const travelTime = Math.max(1, Math.floor(distance))

    if (player.credits >= fuelCost) {
      setPlayer(prev => ({
        ...prev,
        credits: prev.credits - fuelCost,
        currentLocation: destinationName,
        daysElapsed: prev.daysElapsed + travelTime
      }))
      return true
    }
    return false
  }

  // Render different screens
  if (!gameStarted) {
    return <StartScreen onStart={startGame} />
  }

  const currentLocation = LOCATIONS[player.currentLocation]

  return (
    <div className="tradewinds-game">
      <Header player={player} onBack={onBack} />
      <NavigationBar currentScreen={currentScreen} setCurrentScreen={setCurrentScreen} />
      
      {currentScreen === 'location' && (
        <LocationScreen location={currentLocation} />
      )}
      
      {currentScreen === 'market' && (
        <MarketScreen 
          location={currentLocation} 
          marketPrices={marketPrices}
          player={player}
          onBuy={buyCargo}
          onSell={sellCargo}
        />
      )}
      
      {currentScreen === 'travel' && (
        <TravelScreen 
          currentLocation={currentLocation}
          player={player}
          onTravel={travelTo}
        />
      )}
    </div>
  )
}

// Component for game start screen
function StartScreen({ onStart }) {
  const [captainName, setCaptainName] = useState('')
  const [shipName, setShipName] = useState('')

  return (
    <div className="start-screen">
      <h1>🚀 TradeWinds</h1>
      <h2>The Space Trading Adventure</h2>
      
      <div className="start-form">
        <div className="form-group">
          <label>Captain's Name:</label>
          <input
            type="text"
            value={captainName}
            onChange={(e) => setCaptainName(e.target.value)}
            placeholder="Captain"
          />
        </div>
        
        <div className="form-group">
          <label>Ship Name:</label>
          <input
            type="text"
            value={shipName}
            onChange={(e) => setShipName(e.target.value)}
            placeholder="Starwind"
          />
        </div>
        
        <button 
          className="start-button"
          onClick={() => onStart(captainName, shipName)}
        >
          Begin Your Journey
        </button>
      </div>
      
      <div className="game-info">
        <p>🌌 Explore 12 real star systems</p>
        <p>💰 Buy low, sell high across the galaxy</p>
        <p>🚢 Command your own starship</p>
      </div>
    </div>
  )
}

// Header component showing player status
function Header({ player, onBack }) {
  const cargoCount = Object.values(player.inventory).reduce((sum, qty) => sum + qty, 0)
  
  return (
    <div className="header">
      <div className="header-left">
        {onBack && (
          <button className="back-button" onClick={onBack}>
            ← Back to Launcher
          </button>
        )}
        <div className="player-info">
          <h2>Captain {player.name}</h2>
          <p>Ship: <strong>{player.shipName}</strong></p>
        </div>
      </div>
      
      <div className="status-info">
        <div className="stat">
          <span className="label">Credits:</span>
          <span className="value">{player.credits.toLocaleString()}</span>
        </div>
        <div className="stat">
          <span className="label">Cargo:</span>
          <span className="value">{cargoCount}/{player.maxCargo}</span>
        </div>
        <div className="stat">
          <span className="label">Days:</span>
          <span className="value">{player.daysElapsed}</span>
        </div>
      </div>
    </div>
  )
}

// Navigation bar
function NavigationBar({ currentScreen, setCurrentScreen }) {
  const navItems = [
    { key: 'location', label: '🌍 Location', icon: '🌍' },
    { key: 'market', label: '🏪 Market', icon: '🏪' },
    { key: 'travel', label: '🚀 Travel', icon: '🚀' }
  ]

  return (
    <nav className="navigation">
      {navItems.map(item => (
        <button
          key={item.key}
          className={`nav-button ${currentScreen === item.key ? 'active' : ''}`}
          onClick={() => setCurrentScreen(item.key)}
        >
          <span className="nav-icon">{item.icon}</span>
          <span className="nav-label">{item.label}</span>
        </button>
      ))}
    </nav>
  )
}

// Location information screen
function LocationScreen({ location }) {
  return (
    <div className="location-screen">
      <div className="location-card">
        <h2>🌍 {location.name}</h2>
        <p className="system">System: <strong>{location.system}</strong></p>
        <p className="distance">Distance from Earth: <strong>{location.distanceFromEarth} light-years</strong></p>
        
        <div className="description">
          <p>{location.description}</p>
        </div>
        
        {location.produces.length > 0 && (
          <div className="produces">
            <h4>🏭 Produces:</h4>
            <div className="commodity-list">
              {location.produces.map(item => (
                <span key={item} className="commodity-tag produces">{item}</span>
              ))}
            </div>
          </div>
        )}
        
        {location.consumes.length > 0 && (
          <div className="consumes">
            <h4>📈 In Demand:</h4>
            <div className="commodity-list">
              {location.consumes.map(item => (
                <span key={item} className="commodity-tag consumes">{item}</span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Market screen for trading
function MarketScreen({ location, marketPrices, player, onBuy, onSell }) {
  const [selectedCommodity, setSelectedCommodity] = useState(null)
  const [quantity, setQuantity] = useState(1)
  const [tradeMode, setTradeMode] = useState('buy') // 'buy' or 'sell'

  const cargoCount = Object.values(player.inventory).reduce((sum, qty) => sum + qty, 0)

  const handleTrade = () => {
    if (!selectedCommodity) return

    if (tradeMode === 'buy') {
      const success = onBuy(selectedCommodity, quantity)
      if (success) {
        alert(`✅ Bought ${quantity} ${selectedCommodity}!`)
        setSelectedCommodity(null)
        setQuantity(1)
      } else {
        alert(`❌ Cannot buy - insufficient credits or cargo space!`)
      }
    } else {
      const success = onSell(selectedCommodity, quantity)
      if (success) {
        alert(`✅ Sold ${quantity} ${selectedCommodity}!`)
        setSelectedCommodity(null)
        setQuantity(1)
      } else {
        alert(`❌ Cannot sell - insufficient cargo!`)
      }
    }
  }

  return (
    <div className="market-screen">
      <h2>🏪 Market at {location.name}</h2>
      
      <div className="trade-mode">
        <button 
          className={`mode-button ${tradeMode === 'buy' ? 'active' : ''}`}
          onClick={() => setTradeMode('buy')}
        >
          Buy
        </button>
        <button 
          className={`mode-button ${tradeMode === 'sell' ? 'active' : ''}`}
          onClick={() => setTradeMode('sell')}
        >
          Sell
        </button>
      </div>

      <div className="market-grid">
        {Object.entries(COMMODITIES).map(([name, commodity]) => {
          const price = marketPrices[name]
          const isProduced = location.produces.includes(name)
          const isConsumed = location.consumes.includes(name)
          const playerHas = player.inventory[name] || 0

          return (
            <div 
              key={name}
              className={`market-item ${selectedCommodity === name ? 'selected' : ''} ${isProduced ? 'produces' : ''} ${isConsumed ? 'consumes' : ''}`}
              onClick={() => setSelectedCommodity(name)}
            >
              <h4>{name}</h4>
              <p className="price">{price} credits</p>
              {tradeMode === 'sell' && <p className="owned">You have: {playerHas}</p>}
              <div className="indicators">
                {isProduced && <span className="indicator produces">📉 Cheap</span>}
                {isConsumed && <span className="indicator consumes">📈 Expensive</span>}
              </div>
            </div>
          )
        })}
      </div>

      {selectedCommodity && (
        <div className="trade-panel">
          <h3>Trade {selectedCommodity}</h3>
          <p>Price: {marketPrices[selectedCommodity]} credits each</p>
          
          <div className="quantity-controls">
            <label>Quantity:</label>
            <input
              type="number"
              min="1"
              value={quantity}
              onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
            />
          </div>
          
          <p>Total: {(marketPrices[selectedCommodity] * quantity).toLocaleString()} credits</p>
          
          <div className="trade-buttons">
            <button onClick={handleTrade} className="trade-button">
              {tradeMode === 'buy' ? 'Buy' : 'Sell'} {quantity} {selectedCommodity}
            </button>
            <button onClick={() => setSelectedCommodity(null)} className="cancel-button">
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

// Travel screen
function TravelScreen({ currentLocation, player, onTravel }) {
  const destinations = Object.entries(LOCATIONS)
    .filter(([name]) => name !== currentLocation.name)
    .map(([name, location]) => ({
      name,
      location,
      distance: getDistance(currentLocation, location),
      fuelCost: Math.max(10, Math.floor(getDistance(currentLocation, location) * 5))
    }))
    .sort((a, b) => a.distance - b.distance)

  const handleTravel = (destinationName, fuelCost) => {
    if (player.credits >= fuelCost) {
      const success = onTravel(destinationName)
      if (success) {
        alert(`🚀 Traveled to ${destinationName}!`)
      }
    } else {
      alert(`❌ Insufficient credits for fuel! Need ${fuelCost} credits.`)
    }
  }

  return (
    <div className="travel-screen">
      <h2>🚀 Travel from {currentLocation.name}</h2>
      
      <div className="destinations-grid">
        {destinations.map(({ name, location, distance, fuelCost }) => (
          <div key={name} className="destination-card">
            <h3>{location.name}</h3>
            <p className="system">{location.system}</p>
            <p className="distance">{distance.toFixed(1)} ly</p>
            <p className="fuel-cost">Fuel: {fuelCost} credits</p>
            
            <button 
              className="travel-button"
              onClick={() => handleTravel(name, fuelCost)}
              disabled={player.credits < fuelCost}
            >
              Travel Here
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TradeWinds