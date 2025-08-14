// TradeWinds Game Logic - JavaScript version
// Converted from Python text adventure

// Game data structures
const COMMODITIES = {
  food: { name: "food", basePrice: 10, volatility: 0.15, description: "Nutritious sustenance for colonists and crews" },
  water: { name: "water", basePrice: 5, volatility: 0.10, description: "Pure H2O, essential for all life" },
  medicine: { name: "medicine", basePrice: 50, volatility: 0.30, description: "Advanced pharmaceuticals and medical supplies" },
  electronics: { name: "electronics", basePrice: 100, volatility: 0.25, description: "Computers, sensors, and electronic components" },
  metals: { name: "metals", basePrice: 25, volatility: 0.20, description: "Refined metals for construction and manufacturing" },
  textiles: { name: "textiles", basePrice: 15, volatility: 0.20, description: "Fabrics and clothing materials" },
  weapons: { name: "weapons", basePrice: 200, volatility: 0.40, description: "Military hardware and defensive systems" },
  fuel: { name: "fuel", basePrice: 20, volatility: 0.30, description: "Hydrogen fuel for spacecraft propulsion" },
  luxury: { name: "luxury goods", basePrice: 150, volatility: 0.35, description: "Fine art, jewelry, and exotic delicacies" },
  materials: { name: "raw materials", basePrice: 8, volatility: 0.15, description: "Unprocessed ores and basic materials" }
};

const LOCATIONS = {
  earth_station: {
    id: 'earth_station',
    name: 'Earth Station',
    system: 'Sol System',
    shortDesc: 'A massive orbital complex above humanity\'s birthworld',
    longDesc: `Earth Station stretches endlessly before you, a gleaming testament to human 
ingenuity orbiting the blue marble of Earth below. Through the vast transparisteel 
viewports, you can see the ancient continents and swirling clouds of humanity's 
homeworld. The station buzzes with activity - cargo haulers, passenger liners, 
and luxury yachts dock at numerous bays while holographic advertisements flash 
in dozens of languages. The air hums with the sound of commerce and conversation.`,
    atmosphere: 'The recycled air carries hints of coffee, ozone, and the metallic tang of recycling systems.',
    produces: ['luxury', 'electronics', 'medicine'],
    consumes: ['materials', 'metals'],
    distanceFromEarth: 0,
    connections: { mars_colony: 0.5, europa_station: 1.0, titan_refinery: 1.5 },
    visited: false
  },
  
  mars_colony: {
    id: 'mars_colony',
    name: 'New Olympia - Mars Colony',
    system: 'Sol System',
    shortDesc: 'The first permanent settlement on the Red Planet',
    longDesc: `New Olympia spreads across the rust-colored landscape of Mars, its domed 
structures gleaming in the pale sunlight filtering through the thin atmosphere. 
Massive atmospheric processors churn continuously, slowly thickening the air 
that future generations might breathe freely. Mining vehicles crawl across 
the horizon like metallic insects, harvesting the mineral wealth buried in 
Martian soil. The colony's main dome houses thousands of settlers, their lives 
dedicated to the great terraforming project that may take centuries to complete.`,
    atmosphere: 'The air tastes of iron oxide and recycled oxygen, with an underlying hint of hope.',
    produces: ['metals', 'materials'],
    consumes: ['food', 'water', 'medicine'],
    distanceFromEarth: 0,
    connections: { earth_station: 0.5, europa_station: 0.8 },
    visited: false
  },
  
  europa_station: {
    id: 'europa_station',
    name: 'Europan Deep Station',
    system: 'Sol System',
    shortDesc: 'An ice-mining facility beneath Europa\'s frozen surface',
    longDesc: `Deep beneath Europa's icy shell, Europan Deep Station exists in a cathedral 
of carved ice and metal. Brilliant lights illuminate the walls of the vast 
cavern, revealing the strange beauty of Jupiter's moon's interior. The station's 
massive thermal extractors crack through kilometers of ice, tapping into the 
subsurface ocean that may harbor life. Workers in heated environment suits 
tend to the machinery that processes thousands of tons of ice daily, converting 
it to the precious water that sustains human civilization throughout the system.`,
    atmosphere: 'The air is crisp and clean, with a faint taste of ozone from the ice processors.',
    produces: ['water', 'fuel'],
    consumes: ['electronics', 'food', 'textiles'],
    distanceFromEarth: 0,
    connections: { earth_station: 1.0, mars_colony: 0.8, titan_refinery: 1.2 },
    visited: false
  },
  
  proxima_colony: {
    id: 'proxima_colony',
    name: 'Port Centauri - Proxima Colony',
    system: 'Alpha Centauri',
    shortDesc: 'Humanity\'s first interstellar outpost',
    longDesc: `Port Centauri represents the pinnacle of human achievement - the first 
permanent settlement beyond the Solar System. The colony orbits Proxima 
Centauri b, a world of endless storms and crimson skies. The settlement 
itself is a marvel of engineering, its bio-domes and habitation modules 
arranged in a spiral pattern to maximize efficiency and beauty. Gardens 
of Earth plants grow under artificial suns, while colonists work tirelessly 
to make this alien world a home. The red dwarf star casts everything in 
a perpetual sunset glow.`,
    atmosphere: 'The recycled air carries scents of growing things and the ozone of atmosphere processors.',
    produces: ['food'],
    consumes: ['electronics', 'medicine', 'luxury'],
    distanceFromEarth: 4.37,
    connections: { sirius_hub: 2.0, wolf359_outpost: 1.5 },
    visited: false
  },
  
  sirius_hub: {
    id: 'sirius_hub',
    name: 'Sirius Commercial Station',
    system: 'Sirius System',
    shortDesc: 'The bright star system\'s major trading post',
    longDesc: `Sirius Commercial Station floats in the brilliant light of the binary star 
system, its reflective hull gleaming like a jewel. This is the crossroads of 
interstellar commerce, where trade routes from dozens of systems converge. 
The station's massive docking bays accommodate everything from small courier 
ships to enormous bulk freighters. Holographic displays show commodity prices 
from across human space, while traders from every corner of civilization 
haggle over deals that span light-years.`,
    atmosphere: 'The air hums with energy and ambition, carrying traces of exotic atmospheres.',
    produces: ['electronics', 'weapons'],
    consumes: ['food', 'materials'],
    distanceFromEarth: 8.6,
    connections: { proxima_colony: 2.0, vega_agricultural: 3.0, altair_industrial: 2.5 },
    visited: false
  },
  
  vega_agricultural: {
    id: 'vega_agricultural',
    name: 'Vegan Breadbasket Worlds',
    system: 'Vega System',
    shortDesc: 'Vast agricultural colonies under a brilliant blue star',
    longDesc: `The Vegan agricultural worlds stretch endlessly under the brilliant blue-white 
light of Vega, their surfaces transformed into the galaxy's greatest breadbasket. 
Endless fields of genetically modified crops sway in artificial breezes, tended 
by autonomous harvesters that work around the clock. Bio-domes house delicate 
Earth crops, while open fields grow hardy varieties designed for the intense 
stellar radiation.`,
    atmosphere: 'The air is sweet with growing plants and rich soil, almost intoxicating after sterile ships.',
    produces: ['food', 'textiles'],
    consumes: ['electronics', 'metals', 'medicine'],
    distanceFromEarth: 25.3,
    connections: { sirius_hub: 3.0, altair_industrial: 2.8 },
    visited: false
  }
};

export class GameEngine {
  constructor() {
    this.state = {
      playerName: 'Captain',
      shipName: 'Starwind',
      credits: 1000,
      currentLocation: 'earth_station',
      inventory: {},
      maxCargo: 50,
      daysElapsed: 0,
      visitedLocations: new Set()
    };
    
    // Business and factory systems
    this.businessRegistered = false;
    this.businessName = "";
    this.businessReputation = 0;
    this.businessLicenses = [];
    this.factories = {};
    this.corporateContracts = [];
    this.businessLoans = [];
    
    this.commandHistory = [];
    this.currentLocationObj = null;
    this.marketPrices = {};
    
    // Command patterns
    this.movementCommands = new Set(['travel', 'go', 'move', 'journey', 'fly', 'depart', 'leave']);
    this.examineCommands = new Set(['look', 'examine', 'describe', 'check', 'inspect', 'l']);
    this.inventoryCommands = new Set(['inventory', 'i', 'cargo', 'goods', 'items']);
    this.buyCommands = new Set(['buy', 'purchase', 'acquire', 'get']);
    this.sellCommands = new Set(['sell', 'trade', 'unload']);
    this.marketCommands = new Set(['market', 'prices', 'trading', 'commerce']);
    this.statusCommands = new Set(['status', 'stats', 'info', 'credits', 'money']);
    this.businessCommands = new Set(['business', 'incorporate', 'register', 'license', 'loan', 'contract', 'reputation']);
    this.factoryCommands = new Set(['factory', 'factories', 'build', 'construct', 'facility', 'automate']);
  }
  
  initializeGame(playerName, shipName) {
    this.state.playerName = playerName;
    this.state.shipName = shipName;
    this.currentLocationObj = LOCATIONS[this.state.currentLocation];
    this.generateMarketPrices();
    this.state.visitedLocations.add(this.state.currentLocation);
  }
  
  generateMarketPrices() {
    const location = this.currentLocationObj;
    this.marketPrices = {};
    
    for (const [commId, comm] of Object.entries(COMMODITIES)) {
      let supplyDemand = 1.0;
      
      if (location.produces.includes(commId)) {
        supplyDemand = 0.6 + Math.random() * 0.2; // 0.6-0.8
      } else if (location.consumes.includes(commId)) {
        supplyDemand = 1.2 + Math.random() * 0.4; // 1.2-1.6
      } else {
        supplyDemand = 0.9 + Math.random() * 0.2; // 0.9-1.1
      }
      
      const variation = (Math.random() - 0.5) * 2 * comm.volatility;
      const price = comm.basePrice * (1 + variation) * supplyDemand;
      this.marketPrices[commId] = Math.max(1, Math.floor(price));
    }
  }
  
  processCommand(command) {
    const words = command.toLowerCase().split(/\s+/);
    const verb = words[0];
    const args = words.slice(1);
    
    this.commandHistory.push(command);
    
    if (verb === 'help' || verb === '?') {
      return this.showHelp();
    } else if (this.movementCommands.has(verb)) {
      return this.travelTo(args.join(' '));
    } else if (verb === 'destinations' || verb === 'exits' || verb === 'routes') {
      return this.showDestinations();
    } else if (this.examineCommands.has(verb)) {
      return this.examine(args);
    } else if (this.inventoryCommands.has(verb)) {
      return this.showInventory();
    } else if (this.statusCommands.has(verb)) {
      return this.showStatus();
    } else if (this.marketCommands.has(verb)) {
      return this.showMarket();
    } else if (this.buyCommands.has(verb)) {
      return this.buyCommodity(args.join(' '));
    } else if (this.sellCommands.has(verb)) {
      return this.sellCommodity(args.join(' '));
    } else if (this.businessCommands.has(verb)) {
      return this.handleBusinessCommand(verb, args);
    } else if (this.factoryCommands.has(verb)) {
      return this.handleFactoryCommand(verb, args);
    } else {
      return this.unknownCommand(command);
    }
  }
  
  lookAround() {
    const loc = this.currentLocationObj;
    const output = [];
    
    if (!loc.visited) {
      output.push({ text: `**${loc.name.toUpperCase()}**`, type: 'location' });
      output.push({ text: this.formatDescription(loc.longDesc), type: 'description' });
      output.push({ text: '', type: 'normal' });
      output.push({ text: `*${loc.atmosphere}*`, type: 'atmosphere' });
      loc.visited = true;
    } else {
      output.push({ text: `**${loc.name}** (${loc.system})`, type: 'location' });
      output.push({ text: loc.shortDesc, type: 'description' });
      output.push({ text: '', type: 'normal' });
      output.push({ text: `*${loc.atmosphere}*`, type: 'atmosphere' });
    }
    
    if (loc.produces.length > 0 || loc.consumes.length > 0) {
      output.push({ text: '', type: 'normal' });
      output.push({ text: 'You notice significant commercial activity here.', type: 'description' });
      if (loc.produces.length > 0) {
        output.push({ text: `Local production: ${loc.produces.join(', ')}`, type: 'success' });
      }
      if (loc.consumes.length > 0) {
        output.push({ text: `High demand for: ${loc.consumes.join(', ')}`, type: 'warning' });
      }
    }
    
    output.push({ text: '', type: 'normal' });
    output.push({ text: "Type 'destinations' to see where you can travel.", type: 'prompt' });
    output.push({ text: "Type 'market' to check commodity prices.", type: 'prompt' });
    
    return output;
  }
  
  showHelp() {
    return [
      { text: 'TRADEWINDS COMMANDS:', type: 'title' },
      { text: '', type: 'normal' },
      { text: 'BASIC COMMANDS:', type: 'title' },
      { text: '  look                 - Look around current location', type: 'description' },
      { text: '  travel <destination> - Travel to another location', type: 'description' },
      { text: '  market               - Show market prices', type: 'description' },
      { text: '  buy <commodity>      - Purchase goods', type: 'description' },
      { text: '  sell <commodity>     - Sell goods', type: 'description' },
      { text: '  status               - Show credits, cargo, and stats', type: 'description' },
      { text: '  inventory            - List your cargo', type: 'description' },
      { text: '', type: 'normal' },
      { text: 'BUSINESS OPERATIONS:', type: 'title' },
      { text: '  business             - Show business options', type: 'description' },
      { text: '  incorporate          - Register your business (5,000 cr)', type: 'description' },
      { text: '  license              - Get business licenses', type: 'description' },
      { text: '  loan                 - Apply for business loans', type: 'description' },
      { text: '  reputation           - Check business reputation', type: 'description' },
      { text: '', type: 'normal' },
      { text: 'FACTORY AUTOMATION:', type: 'title' },
      { text: '  factory              - Show factory options', type: 'description' },
      { text: '  build factory        - Construct automated facility', type: 'description' },
      { text: '  factories            - List your factories', type: 'description' },
      { text: '  automate <commodity> - Build production facility', type: 'description' },
      { text: '', type: 'normal' },
      { text: 'EXAMPLES:', type: 'title' },
      { text: '  • go to mars colony', type: 'prompt' },
      { text: '  • buy some electronics', type: 'prompt' },
      { text: '  • incorporate my business', type: 'prompt' },
      { text: '  • build a factory here', type: 'prompt' },
      { text: '  • automate food production', type: 'prompt' },
      { text: '', type: 'normal' },
      { text: 'TIPS:', type: 'title' },
      { text: '  - Business features unlock advanced gameplay', type: 'prompt' },
      { text: '  - Factories provide passive income over time', type: 'prompt' },
      { text: '  - Higher reputation = better loan terms', type: 'prompt' },
    ];
  }
  
  showDestinations() {
    const loc = this.currentLocationObj;
    const output = [];
    
    output.push({ text: `From ${loc.name}, you can travel to:`, type: 'title' });
    output.push({ text: '', type: 'normal' });
    
    const destinations = [];
    for (const [destId, travelTime] of Object.entries(loc.connections)) {
      const destLoc = LOCATIONS[destId];
      const fuelCost = this.calculateFuelCost(travelTime);
      destinations.push([destLoc, travelTime, fuelCost]);
    }
    
    destinations.sort((a, b) => a[1] - b[1]);
    
    for (const [destLoc, travelTime, fuelCost] of destinations) {
      output.push({ text: `  ${destLoc.name} (${destLoc.system})`, type: 'location' });
      output.push({ text: `    Travel time: ${travelTime} days`, type: 'description' });
      output.push({ text: `    Fuel cost: ${fuelCost} credits`, type: 'description' });
      if (this.state.credits < fuelCost) {
        output.push({ text: '    ⚠️  Insufficient credits for fuel!', type: 'error' });
      }
      output.push({ text: '', type: 'normal' });
    }
    
    return output;
  }
  
  showMarket() {
    const loc = this.currentLocationObj;
    const output = [];
    
    output.push({ text: `**MARKET PRICES AT ${loc.name.toUpperCase()}**`, type: 'title' });
    output.push({ text: '', type: 'normal' });
    output.push({ text: 'Commodity          Price    Market Notes', type: 'description' });
    output.push({ text: '-'.repeat(50), type: 'description' });
    
    for (const [commId, comm] of Object.entries(COMMODITIES)) {
      const price = this.marketPrices[commId];
      let notes = '';
      let type = 'description';
      
      if (loc.produces.includes(commId)) {
        notes = '📉 LOCAL PRODUCTION (Cheap!)';
        type = 'success';
      } else if (loc.consumes.includes(commId)) {
        notes = '📈 HIGH DEMAND (Expensive!)';
        type = 'warning';
      } else {
        notes = 'Standard pricing';
      }
      
      const line = `${comm.name.padEnd(18)} ${price.toString().padStart(3)} cr   ${notes}`;
      output.push({ text: line, type });
    }
    
    output.push({ text: '', type: 'normal' });
    output.push({ text: "Type 'buy <commodity>' to purchase goods", type: 'prompt' });
    output.push({ text: "Type 'sell <commodity>' to sell goods", type: 'prompt' });
    
    return output;
  }
  
  showInventory() {
    const cargoCount = this.getCargoCount();
    const output = [];
    
    output.push({ text: `**CARGO MANIFEST - ${this.state.shipName.toUpperCase()}**`, type: 'title' });
    output.push({ text: `Used: ${cargoCount}/50 units`, type: 'description' });
    output.push({ text: '', type: 'normal' });
    
    if (Object.keys(this.state.inventory).length === 0) {
      output.push({ text: 'Your cargo hold is empty.', type: 'description' });
    } else {
      output.push({ text: 'Current cargo:', type: 'description' });
      let totalValue = 0;
      
      for (const [commId, quantity] of Object.entries(this.state.inventory)) {
        if (quantity > 0) {
          const commName = COMMODITIES[commId].name;
          const currentPrice = this.marketPrices[commId];
          const value = quantity * currentPrice;
          totalValue += value;
          output.push({ 
            text: `  ${quantity.toString().padStart(2)} units of ${commName} (worth ${value.toLocaleString()} cr here)`, 
            type: 'description' 
          });
        }
      }
      
      output.push({ text: `\nEstimated total value: ${totalValue.toLocaleString()} credits`, type: 'success' });
    }
    
    output.push({ text: `Available cargo space: ${50 - cargoCount} units`, type: 'description' });
    
    return output;
  }
  
  showStatus() {
    return [
      { text: `**CAPTAIN ${this.state.playerName.toUpperCase()}**`, type: 'title' },
      { text: `Ship: ${this.state.shipName}`, type: 'description' },
      { text: `Credits: ${this.state.credits.toLocaleString()}`, type: 'success' },
      { text: `Current location: ${this.currentLocationObj.name}`, type: 'description' },
      { text: `System: ${this.currentLocationObj.system}`, type: 'description' },
      { text: `Days elapsed: ${this.state.daysElapsed}`, type: 'description' },
      { text: `Cargo: ${this.getCargoCount()}/50 units`, type: 'description' },
      { text: `Locations visited: ${this.state.visitedLocations.size}`, type: 'description' }
    ];
  }
  
  examine(args) {
    if (args.length === 0 || args[0] === 'around' || args[0] === 'here') {
      return this.lookAround();
    } else if (args[0] === 'location' || args[0] === 'station' || args[0] === 'place') {
      return this.describeLocation();
    } else {
      const commodity = args.join(' ');
      return this.examineCommodity(commodity);
    }
  }
  
  describeLocation() {
    const loc = this.currentLocationObj;
    return [
      { text: `**${loc.name.toUpperCase()}**`, type: 'title' },
      { text: `System: ${loc.system}`, type: 'description' },
      { text: `Distance from Earth: ${loc.distanceFromEarth} light-years`, type: 'description' },
      { text: '', type: 'normal' },
      { text: this.formatDescription(loc.longDesc), type: 'description' },
      { text: '', type: 'normal' },
      { text: `*${loc.atmosphere}*`, type: 'atmosphere' }
    ];
  }
  
  examineCommodity(commodityName) {
    const commId = this.findCommodity(commodityName);
    if (!commId) {
      return [
        { text: `I don't recognize '${commodityName}'.`, type: 'error' },
        { text: `Available commodities: ${Object.values(COMMODITIES).map(c => c.name).join(', ')}`, type: 'description' }
      ];
    }
    
    const comm = COMMODITIES[commId];
    const price = this.marketPrices[commId];
    const loc = this.currentLocationObj;
    const owned = this.state.inventory[commId] || 0;
    
    const output = [
      { text: `**${comm.name.toUpperCase()}**`, type: 'title' },
      { text: '', type: 'normal' },
      { text: comm.description, type: 'description' },
      { text: '', type: 'normal' },
      { text: `Current price here: ${price} credits per unit`, type: 'description' },
      { text: `Base market value: ${comm.basePrice} credits`, type: 'description' }
    ];
    
    if (loc.produces.includes(commId)) {
      output.push({ text: '✅ Locally produced - prices are LOW', type: 'success' });
    } else if (loc.consumes.includes(commId)) {
      output.push({ text: '🔥 High local demand - prices are HIGH', type: 'warning' });
    } else {
      output.push({ text: '💰 Standard market pricing', type: 'description' });
    }
    
    if (owned > 0) {
      output.push({ text: `You currently have ${owned} units in your cargo hold`, type: 'description' });
    }
    
    return output;
  }
  
  travelTo(destination) {
    if (!destination.trim()) {
      return [
        { text: "Travel where? Try 'travel <destination>' or 'destinations' to see options.", type: 'error' }
      ];
    }
    
    const destId = this.findDestination(destination);
    if (!destId) {
      return [
        { text: `I don't know how to get to '${destination}'.`, type: 'error' },
        { text: "Type 'destinations' to see available routes.", type: 'prompt' }
      ];
    }
    
    if (!(destId in this.currentLocationObj.connections)) {
      return [
        { text: `There's no direct route to ${LOCATIONS[destId].name} from here.`, type: 'error' },
        { text: "Type 'destinations' to see available routes.", type: 'prompt' }
      ];
    }
    
    const travelTime = this.currentLocationObj.connections[destId];
    const fuelCost = this.calculateFuelCost(travelTime);
    
    if (this.state.credits < fuelCost) {
      return [
        { text: `You need ${fuelCost} credits for fuel, but you only have ${this.state.credits}.`, type: 'error' },
        { text: 'Sell some cargo first to raise funds.', type: 'prompt' }
      ];
    }
    
    // Execute travel
    const destLoc = LOCATIONS[destId];
    this.state.credits -= fuelCost;
    this.state.daysElapsed += Math.floor(travelTime);
    this.state.currentLocation = destId;
    this.currentLocationObj = destLoc;
    this.state.visitedLocations.add(destId);
    
    // Regenerate market prices
    this.generateMarketPrices();
    
    const output = [
      { text: `Preparing for departure to ${destLoc.name}...`, type: 'description' },
      { text: `Fuel cost: ${fuelCost} credits`, type: 'description' },
      { text: `Travel time: ${travelTime} days`, type: 'description' },
      { text: '', type: 'normal' },
      { text: '🚀 TRAVELING...', type: 'title' },
      { text: '', type: 'normal' }
    ];
    
    if (!destLoc.visited) {
      output.push({ text: `After ${travelTime} days of travel through the void, you arrive at`, type: 'description' });
      output.push({ text: `${destLoc.name} in the ${destLoc.system}.`, type: 'description' });
    } else {
      output.push({ text: `You arrive at the familiar sight of ${destLoc.name}.`, type: 'description' });
    }
    
    output.push({ text: '', type: 'normal' });
    output.push(...this.lookAround());
    
    return output;
  }
  
  buyCommodity(commodityName) {
    if (!commodityName.trim()) {
      return [
        { text: "Buy what? Try 'buy <commodity>' or 'market' to see available goods.", type: 'error' }
      ];
    }
    
    const commId = this.findCommodity(commodityName);
    if (!commId) {
      return [
        { text: `I don't recognize '${commodityName}'.`, type: 'error' },
        { text: "Type 'market' to see available commodities.", type: 'prompt' }
      ];
    }
    
    // For now, default to buying 1 unit (could be enhanced to parse quantity)
    const quantity = 1;
    const comm = COMMODITIES[commId];
    const price = this.marketPrices[commId];
    const totalCost = price * quantity;
    const cargoSpace = 50 - this.getCargoCount();
    
    if (this.state.credits < totalCost) {
      return [
        { text: `You can't afford ${quantity} units of ${comm.name}. You need ${totalCost} credits but only have ${this.state.credits}.`, type: 'error' }
      ];
    }
    
    if (cargoSpace < quantity) {
      return [
        { text: 'Your cargo hold is full! Sell something first.', type: 'error' }
      ];
    }
    
    // Execute purchase
    this.state.credits -= totalCost;
    this.state.inventory[commId] = (this.state.inventory[commId] || 0) + quantity;
    
    const output = [
      { text: `Purchased ${quantity} units of ${comm.name} for ${totalCost.toLocaleString()} credits.`, type: 'success' },
      { text: `Credits remaining: ${this.state.credits.toLocaleString()}`, type: 'description' }
    ];
    
    const loc = this.currentLocationObj;
    if (loc.produces.includes(commId)) {
      output.push({ text: '💡 Good buy! This commodity is produced locally, so prices are low.', type: 'success' });
    } else if (loc.consumes.includes(commId)) {
      output.push({ text: '⚠️  Expensive here! Consider selling this elsewhere for better profit.', type: 'warning' });
    }
    
    return output;
  }
  
  sellCommodity(commodityName) {
    if (!commodityName.trim()) {
      return [
        { text: "Sell what? Try 'sell <commodity>' or 'inventory' to see what you have.", type: 'error' }
      ];
    }
    
    const commId = this.findCommodity(commodityName);
    if (!commId) {
      return [
        { text: `I don't recognize '${commodityName}'.`, type: 'error' },
        { text: "Type 'inventory' to see what you have.", type: 'prompt' }
      ];
    }
    
    const owned = this.state.inventory[commId] || 0;
    if (owned <= 0) {
      return [
        { text: `You don't have any ${COMMODITIES[commId].name} to sell.`, type: 'error' }
      ];
    }
    
    // For now, sell 1 unit (could be enhanced)
    const quantity = Math.min(1, owned);
    const price = this.marketPrices[commId];
    const totalEarned = price * quantity;
    
    // Execute sale
    this.state.credits += totalEarned;
    this.state.inventory[commId] -= quantity;
    if (this.state.inventory[commId] <= 0) {
      delete this.state.inventory[commId];
    }
    
    const output = [
      { text: `Sold ${quantity} units of ${COMMODITIES[commId].name} for ${totalEarned.toLocaleString()} credits.`, type: 'success' },
      { text: `Credits available: ${this.state.credits.toLocaleString()}`, type: 'description' }
    ];
    
    const loc = this.currentLocationObj;
    if (loc.consumes.includes(commId)) {
      output.push({ text: '💰 Excellent sale! This commodity is in high demand here.', type: 'success' });
    } else if (loc.produces.includes(commId)) {
      output.push({ text: '📉 Low prices here since it\'s locally produced. Consider selling elsewhere.', type: 'warning' });
    }
    
    return output;
  }
  
  unknownCommand(command) {
    const responses = [
      `I don't understand '${command}'. Type 'help' for available commands.`,
      `'${command}' isn't a command I recognize. Try 'help' to see what you can do.`,
      `I'm not sure what you mean by '${command}'. Type 'help' for assistance.`,
      `Unknown command: '${command}'. Use 'help' to see available actions.`
    ];
    
    const output = [
      { text: responses[Math.floor(Math.random() * responses.length)], type: 'error' }
    ];
    
    // Suggest alternatives
    if (command.includes('go') || command.includes('move') || command.includes('travel')) {
      output.push({ text: "💡 Try 'travel <destination>' or 'destinations' to see where you can go.", type: 'prompt' });
    } else if (command.includes('buy') || command.includes('purchase')) {
      output.push({ text: "💡 Try 'buy <commodity>' or 'market' to see what's available.", type: 'prompt' });
    } else if (command.includes('sell') || command.includes('trade')) {
      output.push({ text: "💡 Try 'sell <commodity>' or 'inventory' to see what you have.", type: 'prompt' });
    }
    
    return output;
  }
  
  // Utility methods
  findCommodity(name) {
    const lowerName = name.toLowerCase();
    for (const [id, comm] of Object.entries(COMMODITIES)) {
      if (lowerName.includes(comm.name) || lowerName === id) {
        return id;
      }
    }
    return null;
  }
  
  findDestination(destination) {
    const dest = destination.toLowerCase();
    for (const [id, loc] of Object.entries(LOCATIONS)) {
      if (dest.includes(loc.name.toLowerCase()) || 
          dest.includes(loc.system.toLowerCase()) || 
          dest === id) {
        return id;
      }
      // Common abbreviations
      if ((dest.includes('earth') && id === 'earth_station') ||
          (dest.includes('mars') && id === 'mars_colony') ||
          (dest.includes('europa') && id === 'europa_station') ||
          (dest.includes('proxima') && id === 'proxima_colony') ||
          (dest.includes('sirius') && id === 'sirius_hub') ||
          (dest.includes('vega') && id === 'vega_agricultural')) {
        return id;
      }
    }
    return null;
  }
  
  calculateFuelCost(travelTime) {
    return Math.max(10, Math.floor(travelTime * 25));
  }
  
  formatDescription(desc) {
    // Break long descriptions into multiple lines for better readability
    return desc.replace(/\s+/g, ' ').trim();
  }
  
  getCargoCount() {
    return Object.values(this.state.inventory).reduce((sum, qty) => sum + qty, 0);
  }
  
  // Business and factory command handlers (basic implementation)
  handleBusinessCommand(verb, args) {
    if (verb === 'business') {
      return this.showBusinessOptions();
    } else if (verb === 'incorporate' || verb === 'register') {
      return this.incorporateBusiness();
    } else {
      return [
        { text: `Business command '${verb}' not yet implemented in web version.`, type: 'warning' },
        { text: 'Try the desktop version for full business features!', type: 'prompt' }
      ];
    }
  }
  
  handleFactoryCommand(verb, args) {
    if (verb === 'factory') {
      return this.showFactoryOptions();
    } else if (verb === 'factories') {
      return this.listFactories();
    } else {
      return [
        { text: `Factory command '${verb}' not yet implemented in web version.`, type: 'warning' },
        { text: 'Try the desktop version for full factory features!', type: 'prompt' }
      ];
    }
  }
  
  showBusinessOptions() {
    const output = [
      { text: '🏢 BUSINESS OPERATIONS', type: 'title' },
      { text: '', type: 'normal' }
    ];
    
    if (!this.businessRegistered) {
      output.push(
        { text: 'You are operating as an individual trader.', type: 'description' },
        { text: 'Consider incorporating your business for benefits:', type: 'description' },
        { text: '  • Access to corporate contracts', type: 'description' },
        { text: '  • Better loan terms', type: 'description' },
        { text: '  • Build automated factories', type: 'description' },
        { text: '', type: 'normal' },
        { text: 'Commands:', type: 'title' },
        { text: '  incorporate          - Register your business (5,000 credits)', type: 'description' }
      );
    } else {
      output.push(
        { text: `Business: ${this.businessName}`, type: 'success' },
        { text: `Reputation: ${this.businessReputation}/100`, type: 'description' },
        { text: '', type: 'normal' },
        { text: 'Full business features coming soon to web version!', type: 'prompt' },
        { text: 'Try the desktop version for complete functionality.', type: 'prompt' }
      );
    }
    
    return output;
  }
  
  incorporateBusiness() {
    if (this.businessRegistered) {
      return [{ text: 'You already have a registered business.', type: 'warning' }];
    }
    
    const cost = 5000;
    if (this.state.credits < cost) {
      return [{ text: `Incorporation costs ${cost.toLocaleString()} credits. You only have ${this.state.credits.toLocaleString()}.`, type: 'error' }];
    }
    
    // Simple incorporation (no name input in web version for now)
    this.state.credits -= cost;
    this.businessRegistered = true;
    this.businessName = `${this.state.playerName} Trading Corp`;
    this.businessReputation = 10;
    
    return [
      { text: '🎉 Congratulations! Your business has been incorporated.', type: 'success' },
      { text: `Business Name: ${this.businessName}`, type: 'description' },
      { text: '', type: 'normal' },
      { text: 'Benefits unlocked:', type: 'title' },
      { text: '  ✅ Business status activated', type: 'success' },
      { text: '  ✅ Foundation for future features', type: 'success' },
      { text: '', type: 'normal' },
      { text: 'Note: Full business features available in desktop version!', type: 'prompt' }
    ];
  }
  
  showFactoryOptions() {
    return [
      { text: '🏭 FACTORY AUTOMATION SYSTEM', type: 'title' },
      { text: '', type: 'normal' },
      { text: 'Factory automation is coming soon to the web version!', type: 'description' },
      { text: '', type: 'normal' },
      { text: 'For full factory features, try the desktop version:', type: 'prompt' },
      { text: '  • Build automated production facilities', type: 'description' },
      { text: '  • Generate passive income over time', type: 'description' },
      { text: '  • Food, Electronics, and Mining factories', type: 'description' },
      { text: '  • Location-based suitability bonuses', type: 'description' }
    ];
  }
  
  listFactories() {
    if (Object.keys(this.factories).length === 0) {
      return [
        { text: '🏭 YOUR FACTORIES', type: 'title' },
        { text: '', type: 'normal' },
        { text: "You don't own any factories yet.", type: 'description' },
        { text: 'Factory construction coming soon to web version!', type: 'prompt' }
      ];
    }
    
    return [
      { text: '🏭 YOUR FACTORIES', type: 'title' },
      { text: 'Factory management coming soon!', type: 'description' }
    ];
  }

  // Getter methods for the UI
  getPlayerName() { return this.state.playerName; }
  getCredits() { return this.state.credits; }
  getDaysElapsed() { return this.state.daysElapsed; }
}