# 🚀 TradeWinds - Space Trading Adventure

A **classic text adventure** with rich descriptions and natural language commands! Explore the galaxy, trade commodities across **real star systems**, and build your space trading empire through immersive interactive fiction.

**💰 Currency: Talents (╬) | 🏢 Business System | 🏭 Factory Automation | 🔊 TTS Accessible | 👥 Multiplayer Ready**

## 🌌 Core Features

- **💰 Talents Currency (╬)**: Enhanced economic system replacing credits
- **12 Real Star Systems**: Sol, Alpha Centauri, Sirius, Vega, Altair, Wolf 359, TRAPPIST-1, Gliese 581, and more
- **Dynamic Markets**: Supply and demand affects prices across different locations
- **Rich Descriptions**: Atmospheric text that brings each location to life
- **Natural Language Parser**: Type commands naturally like "go to mars" or "buy some food"
- **Cargo Management**: 50-unit cargo hold with strategic loading decisions
- **Fuel Economics**: Travel costs money and time based on real stellar distances

## 🏢 Business System

- **Business Incorporation**: Register your company for ╬5,000
- **Business Licenses**: Trading, Manufacturing, Mining, and Research licenses
- **Corporate Loans**: Get funding based on your business reputation
- **Reputation System**: Build credibility through successful operations
- **Factory Automation**: Build facilities that generate passive income
  - Food Processing Plants (╬50,000) - Agricultural worlds
  - Electronics Factories (╬100,000) - Industrial systems  
  - Mining Facilities (╬75,000) - Resource-rich locations

## 🔊 Accessibility Features

- **Text-to-Speech**: Full TTS support for blind/low-vision users
- **Large Fonts**: 14pt default, adjustable 10pt-24pt range
- **High Contrast**: Toggle between color schemes
- **Keyboard Navigation**: Complete keyboard accessibility
- **Screen Reader Support**: Compatible with NVDA, JAWS, Windows Narrator

## 👥 Multiplayer System

- **Friend Codes**: 8-character codes for easy connection
- **Company Collaboration**: Join friends' businesses or compete as rivals
- **Cross-Platform Ready**: Future support for web-desktop connections

## 🎮 Multiple Ways to Play

### 1. 🔊 Accessible Edition (NEW! - Recommended for All Users)
**Full accessibility features with TTS, large fonts, and multiplayer support**

```bash
python tradewinds_accessible.py
```

**🌟 ACCESSIBILITY FEATURES:**
- ✅ **Text-to-Speech (TTS)** - Full voice output for blind/low-vision users
- ✅ **Large 14pt Fonts** - Adjustable from 10pt to 24pt for visual accessibility
- ✅ **High Contrast Mode** - Switch between themes for better visibility  
- ✅ **Keyboard Navigation** - Full control via keyboard shortcuts
- ✅ **Splash Screen** - Welcome screen with feature overview
- ✅ **Screen Reader Compatible** - Works with NVDA, JAWS, and Windows Narrator

**🌐 MULTIPLAYER READY:**
- ✅ **Friend Codes** - Easy 8-character codes to connect with friends
- ✅ **Company Joining** - Work together or compete as rivals
- ✅ **Cross-Platform** - Connect with web and desktop players (coming soon)

**🏢 BUSINESS FEATURES:**
- ✅ **Full Business System** - Incorporate, get licenses, apply for loans
- ✅ **Factory Automation** - Build facilities for passive income
- ✅ **Reputation System** - Build credibility for better opportunities

**Quick Launch:** Double-click `run_accessible.bat`

### 2. 🖥️ Desktop Text Adventure (Classic Windows GUI)

**Windows desktop version with retro terminal styling**

```bash
python tradewinds_desktop.py
```

**Features:**
- ✅ **Native Windows GUI** with menu bar and proper window controls
- ✅ **Retro Terminal Look** - Classic green-on-black terminal aesthetic  
- ✅ **Rich Text Formatting** - Color-coded output for different game elements
- ✅ **Command History** - Use UP/DOWN arrows to navigate previous commands
- ✅ **Mouse Support** - Click buttons, scroll text, resize window
- ✅ **Business Integration** - Full incorporation and factory systems
- ✅ **Talents Currency (╬)** - Enhanced economic system

**Quick Launch:** Double-click `run_desktop.bat`

### 3. 📖 Pure Text Adventure (Classic Command-Line)
**For purists who want the authentic terminal experience**

```bash
python tradewinds_adventure.py
```
- Rich, atmospheric descriptions of each location
- Natural language command parser ("go to mars", "buy some food")
- Classic Infocom-style interactive fiction
- Pure command-line interface

### 2. 🌐 Progressive Web App (PWA)
**Modern web-based version that works on any device**

#### To Run:
1. Open terminal in `webui` folder
2. Run: `npm install` (first time only)
3. Run: `npm run dev`
4. Open browser to the provided URL (usually `http://localhost:5173`)

#### PWA Features:
- ✅ **Text Adventure Interface**: Classic terminal styling
- ✅ **Installable**: Add to home screen/desktop
- ✅ **Offline Support**: Cached for offline play
- ✅ **Cross-Platform**: Works on Windows, Mac, Linux, mobile
- ✅ **Modern UI**: Beautiful retro terminal interface
- ✅ **Responsive**: Adapts to different screen sizes

### 5. 🎮 Alternative Versions
**Other ways to play**

#### Quick Launchers:
- **Accessible Edition**: `run_accessible.bat` (TTS, large fonts, multiplayer)
- **Desktop Text Adventure**: `run_desktop.bat` (Windows GUI with retro styling)
- **Multi-Version Launcher**: `run_tradewinds.bat` (choose from 5 versions)
- **Original Graphical GUI**: `python tradewinds_gui.py` (visual trading interface)
- **Simple CLI**: `python tradewinds.py` (basic command-line)

#### Create Standalone Executable:
- **Easy Way**: Run `build_with_pyinstaller.bat` 
- **Alternative**: Install cx_Freeze and run `python build_exe.py`

## 🌍 Real Star Systems Included

| Location | System | Distance | Speciality |
|----------|--------|----------|------------|
| Earth Station | Sol | 0 ly | Technology Hub |
| Mars Colony | Sol | 0 ly | Mining Operations |
| Europa Station | Sol | 0 ly | Water Production |
| Proxima Colony | Alpha Centauri | 4.37 ly | First Interstellar Colony |
| Sirius Trade Hub | Sirius | 8.6 ly | Commercial Waystation |
| Vega Agricultural | Vega | 25.3 ly | Food Production |
| Altair Industrial | Altair | 16.7 ly | Heavy Manufacturing |
| Wolf 359 Outpost | Wolf 359 | 7.9 ly | Dangerous Mining |
| TRAPPIST Research | TRAPPIST-1 | 39.5 ly | Scientific Research |
| Kepler Paradise | Kepler-452 | 1,400 ly | Distant Earth-like World |

## 🎯 Text Adventure Commands

### 🧭 Movement & Exploration:
```
travel <destination>     - Travel to another star system
destinations            - Show available routes and fuel costs
look                    - Examine your current location
look location           - Get detailed location description
examine <item>          - Learn about commodities or objects
```

### 💰 Trading Commands:
```
market                  - View current market prices
buy <commodity>         - Purchase goods (e.g., "buy food")
sell <commodity>        - Sell cargo (e.g., "sell metals")
inventory               - Check your cargo hold
```

### 📊 Status & Information:
```
status                  - View credits, location, ship info
help                    - Show all available commands
```

### 🎮 Natural Language Examples:
- `go to mars` or `travel mars colony`
- `buy some electronics` or `purchase food`
- `examine luxury goods` or `look at water`
- `sell all metals` or `trade textiles`

## 💰 Trading Strategy Tips

### 🔄 Profitable Trade Routes:
- **Europa → Mars**: Water is abundant on Europa but desperately needed on Mars
- **Vega → Any Colony**: Agricultural worlds produce cheap food
- **Earth → Proxima**: Luxury goods command high prices at distant colonies
- **Wolf 359 → Altair**: Raw materials from dangerous mining feed manufacturing

### 📈 Market Indicators in Descriptions:
- **📉 "LOCAL PRODUCTION (Cheap!)"**: Buy here, prices are low
- **📈 "HIGH DEMAND (Expensive!)"**: Sell here, prices are high
- **Rich Text Clues**: Location descriptions hint at what's produced/needed

## 🛠️ Technical Requirements

### All Python Versions:
- Python 3.7+ 
- Standard library only (no additional packages required)
- Works on Windows, Mac, Linux

### Web Version:
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Node.js 16+ and npm (for development)
- React 19 + Vite

## 📁 File Structure

```
📁 openweb ui/
├── 🔊 ACCESSIBLE EDITION (RECOMMENDED FOR ALL)
│   ├── tradewinds_accessible.py    # Full accessibility + TTS + multiplayer
│   └── run_accessible.bat          # Quick launch accessible edition
├── 🖥️ DESKTOP TEXT ADVENTURES  
│   ├── tradewinds_desktop.py       # Windows GUI with business features
│   ├── tradewinds_adventure.py     # Pure command-line text adventure
│   └── tradewinds_text_gui.py      # Alternative GUI version
├── 🌐 webui/                       # Progressive Web App
│   ├── src/TradeWindsText.jsx      # React text adventure terminal
│   ├── src/TradeWindsText.css      # Terminal styling  
│   ├── src/gameLogic.js            # JavaScript game engine
│   ├── src/TradeWinds.jsx          # Original graphical version
│   └── src/TradeWinds.css          # Graphical styling
├── 🎮 OTHER VERSIONS
│   ├── tradewinds_gui.py           # Original graphical GUI
│   └── tradewinds.py               # Simple CLI version
├── ⚡ QUICK LAUNCHERS
│   ├── run_accessible.bat          # Launch accessible edition (BEST)
│   ├── run_desktop.bat             # Launch desktop text adventure
│   ├── run_tradewinds.bat          # Multi-version launcher (5 options)
│   └── build_with_pyinstaller.bat  # Create .exe files
└── 📜 TradeWinds_README.md         # This documentation
```

## 🎯 Text Adventure Commands

### 🧭 Movement & Exploration:
```
travel <destination>     - Travel to another star system
destinations            - Show available routes and fuel costs
look                    - Examine your current location
look location           - Get detailed location description
examine <item>          - Learn about commodities or objects
```

### 💰 Trading Commands:
```
market                  - View current market prices
buy <commodity>         - Purchase goods (e.g., "buy food")
sell <commodity>        - Sell cargo (e.g., "sell metals")
inventory               - Check your cargo hold
```

### 📊 Status & Information:
```
status                  - View credits, location, ship info
help                    - Show all available commands
```

### 🎮 Natural Language Examples:
- `go to mars` or `travel mars colony`
- `buy some electronics` or `purchase food`
- `examine luxury goods` or `look at water`
- `sell all metals` or `trade textiles`

## 🚀 Getting Started

### New Players (Accessible Edition - RECOMMENDED):
1. **Start New Game** - Launch accessible version, enter names when prompted
2. **Enable TTS** - Press Ctrl+T or use menu to toggle text-to-speech
3. **Type `look`** - Get oriented at Earth Station (TTS will read aloud)
4. **Try `help`** - See all commands (use F1 for accessibility help)
5. **Use Natural Language** - "go to mars" works just as well as "travel mars_colony"
6. **Navigate History** - Use UP/DOWN arrows for previous commands
7. **Business Growth** - Type `incorporate` when you have ╬5,000 talents
8. **Build Factories** - Use `factory` command to create passive income
9. **Adjust Display** - Use Ctrl+/Ctrl- to change font size
10. **Get Friend Code** - Use Multiplayer menu to connect with others

### Sample First Session:
```
> look
**EARTH STATION**
Earth Station stretches endlessly before you, a gleaming testament...
[Rich description of location]

> market  
Commodity          Price    Market Notes
--------------------------------------------------
food               12 cr    Standard pricing
electronics        85 cr    📉 LOCAL PRODUCTION (Cheap!)
luxury goods      180 cr    📉 LOCAL PRODUCTION (Cheap!)

> buy electronics
Purchased 1 units of electronics for 85 credits.

> destinations
From Earth Station, you can travel to:
  New Olympia - Mars Colony (Sol System)
    Travel time: 0.5 days
    Fuel cost: 25 credits

> travel mars
Preparing for departure to New Olympia - Mars Colony...
🚀 TRAVELING...
After 0.5 days of travel through the void, you arrive at...
```

### New Players (Graphical Versions):
1. **Start at Earth Station** - Familiar home base
2. **Check the Market** - See what's cheap/expensive
3. **Buy Low** - Purchase goods with 📉 indicator
4. **Plan Your Route** - Check destinations and fuel costs
5. **Sell High** - Find locations with 📈 demand
6. **Reinvest Profits** - Build your trading empire

### Advanced Strategies:
- **Text Adventures**: Read atmospheric descriptions for trading clues
- **All Versions**: System trading (Sol system has low fuel costs)
- **Long Haul Routes**: High-risk, high-reward distant colonies
- **Supply Chain Planning**: Chain multiple trades for maximum profit
- **Market Timing**: Prices fluctuate - timing matters!

## 🌟 Future Updates

- 🛸 **Ship Upgrades**: Better cargo capacity, faster travel
- 🏴‍☠️ **Space Pirates**: Risk vs reward mechanics
- 🪐 **More Locations**: Additional real star systems
- 📊 **Market Graphs**: Historical price tracking
- 🎖️ **Achievements**: Trading milestones and records
- 👥 **Multiplayer**: Compete with other traders

## 🎯 Game Objective

**Build the ultimate space trading empire!**
- Start with 1,000 credits and a small cargo hold
- Trade strategically across real star systems
- Master supply and demand economics
- Become the richest captain in human space!

---

**Ready to explore the galaxy? Choose your platform and begin your trading adventure!** 🌌

*Safe travels, Captain!* ⭐