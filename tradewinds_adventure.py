"""
TradeWinds: A Space Trading Text Adventure
Classic parser-based interactive fiction with rich descriptions
"""

import random
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Game state and data structures
@dataclass
class GameState:
    player_name: str = "Captain"
    ship_name: str = "Starwind"
    talents: int = 1000  # Changed from credits to talents (╬)
    current_location: str = "earth_station"
    inventory: Dict[str, int] = None
    max_cargo: int = 50
    days_elapsed: int = 0
    visited_locations: set = None
    
    def __post_init__(self):
        if self.inventory is None:
            self.inventory = {}
        if self.visited_locations is None:
            self.visited_locations = {self.current_location}

class CommodityType(Enum):
    FOOD = "food"
    WATER = "water"
    MEDICINE = "medicine"
    ELECTRONICS = "electronics"
    METALS = "metals"
    TEXTILES = "textiles"
    WEAPONS = "weapons"
    FUEL = "fuel"
    LUXURY = "luxury goods"
    MATERIALS = "raw materials"

@dataclass
class Commodity:
    name: str
    base_price: int
    volatility: float
    description: str

@dataclass
class Location:
    id: str
    name: str
    system: str
    short_desc: str
    long_desc: str
    atmosphere: str  # Atmospheric description
    produces: List[str]
    consumes: List[str]
    distance_from_earth: float
    connections: Dict[str, float]  # location_id -> travel_time
    market_prices: Dict[str, int] = None
    visited: bool = False
    
    def __post_init__(self):
        if self.market_prices is None:
            self.market_prices = {}
            self._generate_prices()
    
    def _generate_prices(self):
        for commodity_id, commodity in COMMODITIES.items():
            base_price = commodity.base_price
            volatility = commodity.volatility
            
            # Supply and demand modifiers
            if commodity_id in self.produces:
                supply_demand = random.uniform(0.6, 0.8)  # Cheaper where produced
            elif commodity_id in self.consumes:
                supply_demand = random.uniform(1.2, 1.6)  # Expensive where needed
            else:
                supply_demand = random.uniform(0.9, 1.1)  # Normal price
            
            # Add volatility
            price_variation = random.uniform(-volatility, volatility)
            final_price = int(base_price * supply_demand * (1 + price_variation))
            self.market_prices[commodity_id] = max(1, final_price)

# Game data
COMMODITIES = {
    "food": Commodity("food", 10, 0.15, "Nutritious sustenance for colonists and crews"),
    "water": Commodity("water", 5, 0.10, "Pure H2O, essential for all life"),
    "medicine": Commodity("medicine", 50, 0.30, "Advanced pharmaceuticals and medical supplies"),
    "electronics": Commodity("electronics", 100, 0.25, "Computers, sensors, and electronic components"),
    "metals": Commodity("metals", 25, 0.20, "Refined metals for construction and manufacturing"),
    "textiles": Commodity("textiles", 15, 0.20, "Fabrics and clothing materials"),
    "weapons": Commodity("weapons", 200, 0.40, "Military hardware and defensive systems"),
    "fuel": Commodity("fuel", 20, 0.30, "Hydrogen fuel for spacecraft propulsion"),
    "luxury": Commodity("luxury goods", 150, 0.35, "Fine art, jewelry, and exotic delicacies"),
    "materials": Commodity("raw materials", 8, 0.15, "Unprocessed ores and basic materials")
}

LOCATIONS = {
    "earth_station": Location(
        "earth_station", "Earth Station", "Sol System",
        "A massive orbital complex above humanity's birthworld",
        """Earth Station stretches endlessly before you, a gleaming testament to human 
        ingenuity orbiting the blue marble of Earth below. Through the vast transparisteel 
        viewports, you can see the ancient continents and swirling clouds of humanity's 
        homeworld. The station buzzes with activity - cargo haulers, passenger liners, 
        and luxury yachts dock at numerous bays while holographic advertisements flash 
        in dozens of languages. The air hums with the sound of commerce and conversation.""",
        "The recycled air carries hints of coffee, ozone, and the metallic tang of recycling systems.",
        ["luxury", "electronics", "medicine"], 
        ["materials", "metals"], 
        0, 
        {"mars_colony": 0.5, "europa_station": 1.0, "titan_refinery": 1.5}
    ),
    
    "mars_colony": Location(
        "mars_colony", "New Olympia - Mars Colony", "Sol System", 
        "The first permanent settlement on the Red Planet",
        """New Olympia spreads across the rust-colored landscape of Mars, its domed 
        structures gleaming in the pale sunlight filtering through the thin atmosphere. 
        Massive atmospheric processors churn continuously, slowly thickening the air 
        that future generations might breathe freely. Mining vehicles crawl across 
        the horizon like metallic insects, harvesting the mineral wealth buried in 
        Martian soil. The colony's main dome houses thousands of settlers, their lives 
        dedicated to the great terraforming project that may take centuries to complete.""",
        "The air tastes of iron oxide and recycled oxygen, with an underlying hint of hope.",
        ["metals", "materials"], 
        ["food", "water", "medicine"], 
        0,
        {"earth_station": 0.5, "europa_station": 0.8}
    ),
    
    "europa_station": Location(
        "europa_station", "Europan Deep Station", "Sol System",
        "An ice-mining facility beneath Europa's frozen surface",
        """Deep beneath Europa's icy shell, Europan Deep Station exists in a cathedral 
        of carved ice and metal. Brilliant lights illuminate the walls of the vast 
        cavern, revealing the strange beauty of Jupiter's moon's interior. The station's 
        massive thermal extractors crack through kilometers of ice, tapping into the 
        subsurface ocean that may harbor life. Workers in heated environment suits 
        tend to the machinery that processes thousands of tons of ice daily, converting 
        it to the precious water that sustains human civilization throughout the system.""",
        "The air is crisp and clean, with a faint taste of ozone from the ice processors.",
        ["water", "fuel"], 
        ["electronics", "food", "textiles"], 
        0,
        {"earth_station": 1.0, "mars_colony": 0.8, "titan_refinery": 1.2}
    ),
    
    "titan_refinery": Location(
        "titan_refinery", "Titan Hydrocarbon Processing", "Sol System",
        "Industrial complex on Saturn's largest moon",
        """Titan Refinery squats like a mechanical beast on the surface of Saturn's 
        largest moon, its towers and stacks disappearing into the thick, orange atmosphere. 
        The facility processes the moon's abundant hydrocarbons, converting methane lakes 
        and hydrocarbon rain into the fuel that powers interplanetary commerce. Giant 
        storage tanks dot the landscape, and the distant rings of Saturn provide a 
        spectacular backdrop to this monument to industrial capability. The facility 
        operates in perpetual twilight, as the thick atmosphere filters out most sunlight.""",
        "The atmosphere tastes of hydrocarbons and industrial solvents, thick and heavy.",
        ["fuel", "materials"], 
        ["electronics", "food"], 
        0,
        {"earth_station": 1.5, "europa_station": 1.2}
    ),
    
    "proxima_colony": Location(
        "proxima_colony", "Port Centauri - Proxima Colony", "Alpha Centauri",
        "Humanity's first interstellar outpost",
        """Port Centauri represents the pinnacle of human achievement - the first 
        permanent settlement beyond the Solar System. The colony orbits Proxima 
        Centauri b, a world of endless storms and crimson skies. The settlement 
        itself is a marvel of engineering, its bio-domes and habitation modules 
        arranged in a spiral pattern to maximize efficiency and beauty. Gardens 
        of Earth plants grow under artificial suns, while colonists work tirelessly 
        to make this alien world a home. The red dwarf star casts everything in 
        a perpetual sunset glow.""",
        "The recycled air carries scents of growing things and the ozone of atmosphere processors.",
        ["food"], 
        ["electronics", "medicine", "luxury"], 
        4.37,
        {"sirius_hub": 2.0, "wolf359_outpost": 1.5}
    ),
    
    "sirius_hub": Location(
        "sirius_hub", "Sirius Commercial Station", "Sirius System",
        "The bright star system's major trading post",
        """Sirius Commercial Station floats in the brilliant light of the binary star 
        system, its reflective hull gleaming like a jewel. This is the crossroads of 
        interstellar commerce, where trade routes from dozens of systems converge. 
        The station's massive docking bays accommodate everything from small courier 
        ships to enormous bulk freighters. Holographic displays show commodity prices 
        from across human space, while traders from every corner of civilization 
        haggle over deals that span light-years. The intense stellar radiation requires 
        heavy shielding, giving the interior a distinctly blue-tinged artificial lighting.""",
        "The air hums with energy and ambition, carrying traces of exotic atmospheres.",
        ["electronics", "weapons"], 
        ["food", "materials"], 
        8.6,
        {"proxima_colony": 2.0, "vega_agricultural": 3.0, "altair_industrial": 2.5}
    ),
    
    "vega_agricultural": Location(
        "vega_agricultural", "Vegan Breadbasket Worlds", "Vega System",
        "Vast agricultural colonies under a brilliant blue star",
        """The Vegan agricultural worlds stretch endlessly under the brilliant blue-white 
        light of Vega, their surfaces transformed into the galaxy's greatest breadbasket. 
        Endless fields of genetically modified crops sway in artificial breezes, tended 
        by autonomous harvesters that work around the clock. Bio-domes house delicate 
        Earth crops, while open fields grow hardy varieties designed for the intense 
        stellar radiation. The agricultural stations process millions of tons of food 
        daily, feeding the expanding human civilization. Gardens of incredible beauty 
        surround the residential areas, making this one of the most pleasant destinations 
        in human space.""",
        "The air is sweet with growing plants and rich soil, almost intoxicating after sterile ships.",
        ["food", "textiles"], 
        ["electronics", "metals", "medicine"], 
        25.3,
        {"sirius_hub": 3.0, "altair_industrial": 2.8}
    ),
    
    "altair_industrial": Location(
        "altair_industrial", "Altair Manufacturing Complex", "Altair System",
        "The forge worlds of human space",
        """Altair's industrial worlds burn with the fires of human ambition, their 
        surfaces covered in vast manufacturing complexes that produce everything from 
        starships to household appliances. The orbital factories float in formation 
        around the star, their solar collectors drinking in energy to power the forges 
        below. Massive automated assembly lines stretch for kilometers, while precision 
        fabricators craft components to tolerances measured in atoms. The night side 
        of the worlds glow with industrial fires, and streams of cargo vessels ferry 
        finished products to every corner of human space.""",
        "The air tastes of hot metal and industrial processes, but also of human achievement.",
        ["electronics", "weapons", "metals"], 
        ["materials", "food", "water"], 
        16.7,
        {"sirius_hub": 2.5, "vega_agricultural": 2.8, "wolf359_outpost": 2.2}
    ),
    
    "wolf359_outpost": Location(
        "wolf359_outpost", "Wolf's Den Mining Station", "Wolf 359",
        "A dangerous but profitable mining operation",
        """Wolf's Den clings to a barren asteroid in the crimson light of Wolf 359, 
        a red dwarf star that barely illuminates this remote outpost. The station is 
        rough and utilitarian, built for function rather than comfort. Massive mining 
        rigs chew through asteroid rock, extracting precious metals and rare elements 
        that command high prices in civilized space. The miners are a tough breed, 
        drawn by high wages and the frontier spirit. Radiation storms from the unstable 
        red dwarf make this a dangerous posting, but the mineral wealth extracted here 
        fuels human expansion across the galaxy.""",
        "The air tastes of recycled atmosphere and barely-contained danger.",
        ["materials", "metals"], 
        ["food", "water", "medicine"], 
        7.9,
        {"proxima_colony": 1.5, "altair_industrial": 2.2}
    ),
    
    "trappist_research": Location(
        "trappist_research", "TRAPPIST-1 Science Station", "TRAPPIST-1",
        "Cutting-edge research in a seven-planet system",
        """TRAPPIST Research Station orbits in the habitable zone of the ultra-cool 
        dwarf star TRAPPIST-1, surrounded by seven Earth-sized worlds in a cosmic 
        dance of gravitational harmony. The station's laboratories buzz with scientific 
        activity as researchers study the unique planetary system and conduct experiments 
        impossible anywhere else. The tidal forces between the closely-packed worlds 
        create fascinating phenomena that push the boundaries of human understanding. 
        Scientists from across human space compete for positions here, making it a 
        hub of intellectual achievement as well as scientific discovery.""",
        "The air carries the clean scent of scientific precision and boundless curiosity.",
        ["medicine", "electronics"], 
        ["food", "luxury"], 
        39.5,
        {"gliese_station": 2.0, "kepler_paradise": 8.0}
    ),
    
    "gliese_station": Location(
        "gliese_station", "Gliese Frontier Observatory", "Gliese 581",
        "Humanity's far reach into the galaxy",
        """Gliese Frontier Observatory represents humanity's reach into the distant 
        galaxy, a lonely outpost orbiting in the habitable zone of the red dwarf 
        Gliese 581. The station serves as both research facility and waystation for 
        the few brave souls who venture this far from Earth. Long-range sensors scan 
        the galaxy for signs of life and habitable worlds, while the station's crew 
        maintains the delicate balance between scientific mission and basic survival. 
        The isolation here is profound - messages to Earth take over 20 years to arrive, 
        making the station's inhabitants truly pioneers of human space.""",
        "The air tastes thin and precious, carrying the weight of distance and solitude.",
        ["medicine"], 
        ["food", "electronics", "water"], 
        20.4,
        {"trappist_research": 2.0}
    ),
    
    "kepler_paradise": Location(
        "kepler_paradise", "New Eden Colony - Kepler-452b", "Kepler-452",
        "An Earth-like paradise in the far reaches",
        """New Eden Colony on Kepler-452b is humanity's crown jewel, a world so similar 
        to Earth that colonists call it humanity's second Eden. The planet's blue skies, 
        rolling green hills, and crystal-clear oceans provide a stunning backdrop to 
        the most beautiful colony in human space. Ancient alien ruins dot the landscape, 
        their mysterious builders long gone, leaving only questions and wonder. The 
        colony attracts the wealthy and influential, who build magnificent estates among 
        gardens that rival anything on Earth. The thousand-year journey here is worth 
        it for those who can afford the ultimate luxury of a perfect world.""",
        "The air is sweet and clean, carrying scents of unknown flowers and endless possibility.",
        ["luxury", "food"], 
        ["electronics", "medicine", "weapons"], 
        1400,
        {"trappist_research": 8.0}
    )
}

class TextAdventure:
    def __init__(self):
        self.state = GameState()
        self.running = True
        self.current_location_obj = LOCATIONS[self.state.current_location]
        
        # Command history
        self.command_history = []
        self.help_shown = False
        
        # Parser patterns
        self.movement_commands = {
            'travel', 'go', 'move', 'journey', 'fly', 'depart', 'leave'
        }
        self.examine_commands = {
            'look', 'examine', 'describe', 'check', 'inspect', 'l'
        }
        self.inventory_commands = {
            'inventory', 'i', 'cargo', 'goods', 'items'
        }
        self.buy_commands = {
            'buy', 'purchase', 'acquire', 'get'
        }
        self.sell_commands = {
            'sell', 'trade', 'unload'
        }
        self.market_commands = {
            'market', 'prices', 'trading', 'commerce'
        }
        self.status_commands = {
            'status', 'stats', 'info', 'talents', 'money', 'credits'
        }
    
    def start_game(self):
        self.print_title()
        self.get_player_info()
        self.print_intro()
        self.look_around()
        
        while self.running:
            try:
                command = self.get_input()
                if command.strip():
                    self.command_history.append(command)
                    self.parse_command(command)
                    print()  # Add space between commands
            except KeyboardInterrupt:
                self.quit_game()
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")
    
    def print_title(self):
        print("=" * 60)
        print("🚀 TRADEWINDS: A SPACE TRADING ADVENTURE 🚀")
        print("=" * 60)
        print()
        print("Welcome to the galaxy, Captain!")
        print("In this text adventure, you'll navigate between real star")
        print("systems, trading commodities and building your fortune.")
        print()
    
    def get_player_info(self):
        name = input("Enter your captain's name (or press Enter for 'Captain'): ").strip()
        if name:
            self.state.player_name = name
        
        ship = input("Enter your ship's name (or press Enter for 'Starwind'): ").strip()
        if ship:
            self.state.ship_name = ship
        
        print()
        print(f"Welcome aboard, {self.state.player_name}!")
        print(f"You command the starship '{self.state.ship_name}'.")
        print()
    
    def print_intro(self):
        print("You begin your trading career with 1,000 talents (╬) and a cargo")
        print("hold that can carry 50 units of goods. Your ship is currently")
        print("docked at Earth Station in the Sol System.")
        print()
        print("Type 'help' for a list of commands, or just start exploring!")
        print("=" * 60)
        print()
    
    def get_input(self) -> str:
        return input(f"{self.state.player_name}> ").strip().lower()
    
    def parse_command(self, command: str):
        words = command.split()
        if not words:
            return
        
        verb = words[0]
        args = words[1:] if len(words) > 1 else []
        
        # Help system
        if verb in ['help', '?']:
            self.show_help()
        
        # Movement commands
        elif verb in self.movement_commands:
            if args:
                destination = ' '.join(args)
                self.travel_to(destination)
            else:
                print("Travel where? Try 'travel <destination>' or 'destinations' to see options.")
        
        elif verb in ['destinations', 'exits', 'routes']:
            self.show_destinations()
        
        # Examination commands
        elif verb in self.examine_commands:
            if not args or args[0] in ['around', 'here']:
                self.look_around()
            elif args[0] in ['location', 'station', 'place']:
                self.describe_location()
            elif args[0] in ['market', 'prices']:
                self.show_market()
            elif args[0] in ['ship', 'starship']:
                self.describe_ship()
            elif ' '.join(args) in COMMODITIES:
                self.examine_commodity(' '.join(args))
            else:
                commodity = ' '.join(args)
                self.examine_commodity(commodity)
        
        # Inventory and status
        elif verb in self.inventory_commands:
            self.show_inventory()
        
        elif verb in self.status_commands:
            self.show_status()
        
        # Trading commands
        elif verb in self.market_commands:
            self.show_market()
        
        elif verb in self.buy_commands:
            if args:
                commodity = ' '.join(args)
                self.buy_commodity(commodity)
            else:
                print("Buy what? Try 'buy <commodity>' or 'market' to see available goods.")
        
        elif verb in self.sell_commands:
            if args:
                commodity = ' '.join(args)
                self.sell_commodity(commodity)
            else:
                print("Sell what? Try 'sell <commodity>' or 'inventory' to see what you have.")
        
        # System commands
        elif verb in ['quit', 'exit', 'q']:
            self.quit_game()
        
        elif verb in ['save']:
            print("Save game feature not implemented yet.")
        
        elif verb in ['load']:
            print("Load game feature not implemented yet.")
        
        # Unknown command
        else:
            self.unknown_command(command)
    
    def show_help(self):
        print("🚀 TRADEWINDS - BASIC COMMANDS")
        print("=" * 50)
        print()
        print("BASIC COMMANDS:")
        print("  look                 - Look around current location")
        print("  travel <destination> - Travel to another location")
        print("  market               - Show market prices")
        print("  buy <commodity>      - Purchase goods")
        print("  sell <commodity>     - Sell goods")
        print("  status               - Show your stats")
        print("  inventory            - List your cargo")
        print()
        print("ADVANCED:")
        print("  commands             - Show FULL command list")
        print("  business             - Business incorporation options")
        print("  factory              - Build automated facilities")
        print("  destinations         - Show travel routes")
        print()
        print("EXAMPLES:")
        print("  'go to mars', 'buy some food', 'examine electronics'")
        print()
        print("💡 TIP: The parser understands natural language!")
        self.help_shown = True
    
    def show_full_commands(self):
        print()
        print("=" * 70)
        print("🚀 TRADEWINDS - COMPLETE COMMAND REFERENCE")
        print("=" * 70)
        print()
        print("📍 MOVEMENT & TRAVEL:")
        print("  travel <destination>      - Travel to another star system")
        print("  go to <destination>       - Same as travel")
        print("  fly to <destination>      - Same as travel")
        print("  destinations             - Show available routes & costs")
        print()
        print("🔍 EXPLORATION & INFORMATION:")
        print("  look                     - Examine current location")
        print("  look around              - Same as look")
        print("  examine <item>           - Get details about commodities")
        print("  describe <location>      - Get location details")
        print("  look ship                - Examine your ship")
        print()
        print("💰 TRADING & COMMERCE:")
        print("  market                   - View market prices")
        print("  prices                   - Same as market")
        print("  buy <commodity>          - Purchase goods")
        print("  purchase <commodity>     - Same as buy")
        print("  sell <commodity>         - Sell goods from cargo")
        print("  trade <commodity>        - Same as sell")
        print()
        print("📊 STATUS & INVENTORY:")
        print("  status                   - Show credits, location, stats")
        print("  stats                    - Same as status")
        print("  inventory                - List cargo contents")
        print("  cargo                    - Same as inventory")
        print()
        print("🏢 BUSINESS OPERATIONS:")
        print("  business                 - Show business options")
        print("  incorporate              - Register your business")
        print("  license                  - Get business licenses")
        print("  loan                     - Apply for business loans")
        print("  contract                 - View corporate contracts")
        print("  reputation               - Check business reputation")
        print()
        print("🏭 FACTORY & AUTOMATION:")
        print("  factory                  - Show factory options")
        print("  factories                - List your factories")
        print("  build factory            - Construct automated facility")
        print("  construct <type>         - Build specific facility type")
        print("  automate <commodity>     - Build production facility")
        print()
        print("🎮 NATURAL LANGUAGE EXAMPLES:")
        print("  'go to mars colony'")
        print("  'buy some electronics'")
        print("  'sell all my food'")
        print("  'examine luxury goods'")
        print("  'build a factory on europa'")
        print("  'incorporate my business'")
        print("  'check my business reputation'")
        print()
        print("💡 TIPS:")
        print("  • The parser understands many ways to phrase commands")
        print("  • Business features unlock advanced gameplay")
        print("  • Factories provide passive income over time")
        print("  • Higher reputation = better contracts & loan rates")
    
    def look_around(self):
        loc = self.current_location_obj
        if not loc.visited:
            print(f"**{loc.name.upper()}**")
            print(loc.long_desc)
            print()
            print(f"*{loc.atmosphere}*")
            loc.visited = True
        else:
            print(f"**{loc.name}** ({loc.system})")
            print(loc.short_desc)
            print()
            print(f"*{loc.atmosphere}*")
        
        # Mention market activity
        if loc.produces or loc.consumes:
            print()
            print("You notice significant commercial activity here.")
            if loc.produces:
                produces_str = ", ".join(loc.produces)
                print(f"Local production: {produces_str}")
            if loc.consumes:
                consumes_str = ", ".join(loc.consumes)
                print(f"High demand for: {consumes_str}")
        
        print()
        print("Type 'destinations' to see where you can travel.")
        print("Type 'market' to check commodity prices.")
    
    def describe_location(self):
        loc = self.current_location_obj
        print(f"**{loc.name.upper()}**")
        print(f"System: {loc.system}")
        print(f"Distance from Earth: {loc.distance_from_earth} light-years")
        print()
        print(loc.long_desc)
        print()
        print(f"*{loc.atmosphere}*")
    
    def describe_ship(self):
        print(f"**{self.state.ship_name.upper()}**")
        print()
        print("Your trusty starship is a medium-class trading vessel, built for")
        print("reliability and cargo capacity rather than speed or luxury. The")
        print("cockpit is cramped but functional, with nav displays showing your")
        print("current location and fuel reserves. The cargo bay can hold up to")
        print("50 units of goods, currently organized in secure containers.")
        print()
        print(f"Current cargo: {self.get_cargo_count()}/50 units")
        print(f"Talents available: ╬{self.state.talents:,}")
        print(f"Days traveled: {self.state.days_elapsed}")
    
    def show_destinations(self):
        loc = self.current_location_obj
        print(f"From {loc.name}, you can travel to:")
        print()
        
        destinations = []
        for dest_id, travel_time in loc.connections.items():
            dest_loc = LOCATIONS[dest_id]
            fuel_cost = self.calculate_fuel_cost(travel_time)
            destinations.append((dest_loc, travel_time, fuel_cost))
        
        # Sort by travel time
        destinations.sort(key=lambda x: x[1])
        
        for dest_loc, travel_time, fuel_cost in destinations:
            print(f"  {dest_loc.name} ({dest_loc.system})")
            print(f"    Travel time: {travel_time} days")
            print(f"    Fuel cost: {fuel_cost} talents")
            if self.state.talents < fuel_cost:
                print("    ⚠️  Insufficient talents for fuel!")
            print()
        
        if not destinations:
            print("No direct routes available from this location.")
    
    def show_market(self):
        loc = self.current_location_obj
        print(f"**MARKET PRICES AT {loc.name.upper()}**")
        print()
        print("Commodity          Price    Market Notes")
        print("-" * 50)
        
        for comm_id, comm in COMMODITIES.items():
            price = loc.market_prices[comm_id]
            notes = ""
            
            if comm_id in loc.produces:
                notes = "📉 LOCAL PRODUCTION (Cheap!)"
            elif comm_id in loc.consumes:
                notes = "📈 HIGH DEMAND (Expensive!)"
            else:
                notes = "Standard pricing"
            
            print(f"{comm.name:<18} {price:>3} cr   {notes}")
        
        print()
        print("Type 'buy <commodity>' to purchase goods")
        print("Type 'sell <commodity>' to sell goods")
        print("Type 'examine <commodity>' to learn more about an item")
    
    def examine_commodity(self, commodity_name: str):
        # Try to find the commodity
        comm_id = None
        for cid, comm in COMMODITIES.items():
            if commodity_name in comm.name or commodity_name == cid:
                comm_id = cid
                break
        
        if not comm_id:
            print(f"I don't recognize '{commodity_name}'.")
            print("Available commodities:", ", ".join([c.name for c in COMMODITIES.values()]))
            return
        
        comm = COMMODITIES[comm_id]
        loc = self.current_location_obj
        price = loc.market_prices[comm_id]
        
        print(f"**{comm.name.upper()}**")
        print()
        print(comm.description)
        print()
        print(f"Current price here: ╬{price} per unit")
        print(f"Base market value: ╬{comm.base_price}")
        
        if comm_id in loc.produces:
            print("✅ Locally produced - prices are LOW")
        elif comm_id in loc.consumes:
            print("🔥 High local demand - prices are HIGH")
        else:
            print("💰 Standard market pricing")
        
        # Show inventory
        owned = self.state.inventory.get(comm_id, 0)
        if owned > 0:
            print(f"You currently have {owned} units in your cargo hold")
    
    def show_inventory(self):
        cargo_count = self.get_cargo_count()
        print(f"**CARGO MANIFEST - {self.state.ship_name.upper()}**")
        print(f"Used: {cargo_count}/50 units")
        print()
        
        if not self.state.inventory:
            print("Your cargo hold is empty.")
        else:
            print("Current cargo:")
            total_value = 0
            for comm_id, quantity in self.state.inventory.items():
                comm_name = COMMODITIES[comm_id].name
                # Estimate value at current location
                current_price = self.current_location_obj.market_prices[comm_id]
                value = quantity * current_price
                total_value += value
                print(f"  {quantity:>2} units of {comm_name} (worth {value:,} cr here)")
            print(f"\nEstimated total value: {total_value:,} credits")
        
        print(f"Available cargo space: {50 - cargo_count} units")
    
    def show_status(self):
        print(f"**CAPTAIN {self.state.player_name.upper()}**")
        print(f"Ship: {self.state.ship_name}")
        print(f"Talents: ╬{self.state.talents:,}")
        print(f"Current location: {self.current_location_obj.name}")
        print(f"System: {self.current_location_obj.system}")
        print(f"Days elapsed: {self.state.days_elapsed}")
        print(f"Cargo: {self.get_cargo_count()}/50 units")
        print(f"Locations visited: {len(self.state.visited_locations)}")
    
    def travel_to(self, destination: str):
        # Find matching destination
        dest_id = self.find_destination(destination)
        if not dest_id:
            print(f"I don't know how to get to '{destination}'.")
            print("Type 'destinations' to see available routes.")
            return
        
        if dest_id not in self.current_location_obj.connections:
            print(f"There's no direct route to {LOCATIONS[dest_id].name} from here.")
            print("Type 'destinations' to see available routes.")
            return
        
        travel_time = self.current_location_obj.connections[dest_id]
        fuel_cost = self.calculate_fuel_cost(travel_time)
        
        if self.state.talents < fuel_cost:
            print(f"You need {fuel_cost} talents for fuel, but you only have ╬{self.state.talents}.")
            print("Sell some cargo first to raise funds.")
            return
        
        # Execute travel
        dest_loc = LOCATIONS[dest_id]
        print(f"Preparing for departure to {dest_loc.name}...")
        print(f"Fuel cost: {fuel_cost} talents")
        print(f"Travel time: {travel_time} days")
        print()
        
        self.state.talents -= fuel_cost
        self.state.days_elapsed += int(travel_time)
        self.state.current_location = dest_id
        self.current_location_obj = dest_loc
        self.state.visited_locations.add(dest_id)
        
        # Process factory income during travel
        if self.factories and int(travel_time) > 0:
            self.process_factory_income()
        
        # Regenerate market prices at destination
        dest_loc._generate_prices()
        
        print("🚀 TRAVELING...")
        print()
        
        # Arrival description
        if not dest_loc.visited:
            print(f"After {travel_time} days of travel through the void, you arrive at")
            print(f"{dest_loc.name} in the {dest_loc.system}.")
        else:
            print(f"You arrive at the familiar sight of {dest_loc.name}.")
        
        print()
        self.look_around()
    
    def find_destination(self, destination: str) -> Optional[str]:
        """Find a location ID that matches the destination string"""
        destination = destination.lower()
        
        for loc_id, loc in LOCATIONS.items():
            if destination in loc.name.lower():
                return loc_id
            if destination in loc.system.lower():
                return loc_id
            if destination.replace(' ', '_') == loc_id:
                return loc_id
            # Check for common abbreviations
            if 'earth' in destination and 'earth_station' == loc_id:
                return loc_id
            if 'mars' in destination and 'mars_colony' == loc_id:
                return loc_id
            if 'europa' in destination and 'europa_station' == loc_id:
                return loc_id
            if 'titan' in destination and 'titan_refinery' == loc_id:
                return loc_id
            if 'proxima' in destination and 'proxima_colony' == loc_id:
                return loc_id
            if 'sirius' in destination and 'sirius_hub' == loc_id:
                return loc_id
            if 'vega' in destination and 'vega_agricultural' == loc_id:
                return loc_id
            if 'altair' in destination and 'altair_industrial' == loc_id:
                return loc_id
            if 'wolf' in destination and 'wolf359_outpost' == loc_id:
                return loc_id
            if 'trappist' in destination and 'trappist_research' == loc_id:
                return loc_id
            if 'gliese' in destination and 'gliese_station' == loc_id:
                return loc_id
            if 'kepler' in destination and 'kepler_paradise' == loc_id:
                return loc_id
        
        return None
    
    def calculate_fuel_cost(self, travel_time: float) -> int:
        return max(10, int(travel_time * 25))
    
    def buy_commodity(self, commodity_name: str):
        # Parse quantity if specified
        words = commodity_name.split()
        quantity = 1
        
        # Look for quantity words
        if words[0].isdigit():
            quantity = int(words[0])
            commodity_name = ' '.join(words[1:])
        elif 'some' in words:
            quantity = 5
            commodity_name = commodity_name.replace('some ', '')
        elif 'all' in words:
            commodity_name = commodity_name.replace('all ', '')
        
        # Find the commodity
        comm_id = None
        for cid, comm in COMMODITIES.items():
            if commodity_name in comm.name or commodity_name == cid:
                comm_id = cid
                break
        
        if not comm_id:
            print(f"I don't recognize '{commodity_name}'.")
            print("Type 'market' to see available commodities.")
            return
        
        comm = COMMODITIES[comm_id]
        price = self.current_location_obj.market_prices[comm_id]
        
        # Calculate max affordable
        max_affordable = self.state.talents // price
        max_space = 50 - self.get_cargo_count()
        max_buyable = min(max_affordable, max_space)
        
        if max_buyable <= 0:
            if max_affordable <= 0:
                print(f"You can't afford any {comm.name}. Each unit costs ╬{price}.")
            else:
                print("Your cargo hold is full! Sell something first.")
            return
        
        # Handle 'all' quantity
        if 'all' in commodity_name or quantity > max_buyable:
            quantity = max_buyable
            print(f"Buying maximum possible: {quantity} units")
        
        if quantity > max_buyable:
            print(f"You can only buy {max_buyable} units (limited by talents or cargo space).")
            return
        
        # Execute purchase
        total_cost = price * quantity
        self.state.talents -= total_cost
        self.state.inventory[comm_id] = self.state.inventory.get(comm_id, 0) + quantity
        
        print(f"Purchased {quantity} units of {comm.name} for ╬{total_cost:,}.")
        print(f"Talents remaining: ╬{self.state.talents:,}")
        
        # Market commentary
        if comm_id in self.current_location_obj.produces:
            print("💡 Good buy! This commodity is produced locally, so prices are low.")
        elif comm_id in self.current_location_obj.consumes:
            print("⚠️  Expensive here! Consider selling this elsewhere for better profit.")
    
    def sell_commodity(self, commodity_name: str):
        # Parse quantity if specified
        words = commodity_name.split()
        quantity = None
        
        if words[0].isdigit():
            quantity = int(words[0])
            commodity_name = ' '.join(words[1:])
        elif 'some' in words:
            quantity = None  # Will ask for specific amount
            commodity_name = commodity_name.replace('some ', '')
        elif 'all' in words:
            quantity = -1  # Sell all
            commodity_name = commodity_name.replace('all ', '')
        
        # Find the commodity
        comm_id = None
        for cid, comm in COMMODITIES.items():
            if commodity_name in comm.name or commodity_name == cid:
                comm_id = cid
                break
        
        if not comm_id:
            print(f"I don't recognize '{commodity_name}'.")
            print("Type 'inventory' to see what you have.")
            return
        
        comm = COMMODITIES[comm_id]
        owned = self.state.inventory.get(comm_id, 0)
        
        if owned <= 0:
            print(f"You don't have any {comm.name} to sell.")
            return
        
        price = self.current_location_obj.market_prices[comm_id]
        
        # Determine quantity to sell
        if quantity is None:
            print(f"You have {owned} units of {comm.name} worth ╬{price} each.")
            try:
                quantity = int(input("How many units would you like to sell? ").strip())
            except ValueError:
                print("Please enter a valid number.")
                return
        elif quantity == -1:  # Sell all
            quantity = owned
            print(f"Selling all {quantity} units")
        
        if quantity > owned:
            print(f"You only have {owned} units of {comm.name}.")
            return
        
        if quantity <= 0:
            print("Invalid quantity.")
            return
        
        # Execute sale
        total_earned = price * quantity
        self.state.talents += total_earned
        self.state.inventory[comm_id] -= quantity
        if self.state.inventory[comm_id] <= 0:
            del self.state.inventory[comm_id]
        
        print(f"Sold {quantity} units of {comm.name} for ╬{total_earned:,}.")
        print(f"Talents available: ╬{self.state.talents:,}")
        
        # Market commentary
        if comm_id in self.current_location_obj.consumes:
            print("💰 Excellent sale! This commodity is in high demand here.")
        elif comm_id in self.current_location_obj.produces:
            print("📉 Low prices here since it's locally produced. Consider selling elsewhere.")
    
    def get_cargo_count(self) -> int:
        return sum(self.state.inventory.values())
    
    def unknown_command(self, command: str):
        responses = [
            f"I don't understand '{command}'. Type 'help' for available commands.",
            f"'{command}' isn't a command I recognize. Try 'help' to see what you can do.",
            f"I'm not sure what you mean by '{command}'. Type 'help' for assistance.",
            f"Unknown command: '{command}'. Use 'help' to see available actions."
        ]
        print(random.choice(responses))
        
        # Suggest alternatives based on partial matches
        if any(word in command for word in ['go', 'move', 'travel']):
            print("💡 Try 'travel <destination>' or 'destinations' to see where you can go.")
        elif any(word in command for word in ['buy', 'purchase']):
            print("💡 Try 'buy <commodity>' or 'market' to see what's available.")
        elif any(word in command for word in ['sell', 'trade']):
            print("💡 Try 'sell <commodity>' or 'inventory' to see what you have.")
        elif any(word in command for word in ['look', 'see', 'examine']):
            print("💡 Try 'look around', 'look location', or 'market'.")
    
    def handle_business_command(self, verb: str, args: List[str]):
        """Handle business-related commands"""
        if verb == 'business':
            self.show_business_options()
        elif verb in ['incorporate', 'register']:
            self.incorporate_business()
        elif verb == 'license':
            self.get_business_license()
        elif verb == 'loan':
            self.apply_business_loan()
        elif verb == 'contract':
            self.view_contracts()
        elif verb == 'reputation':
            self.check_reputation()
        else:
            print("Business command not recognized. Type 'business' for options.")
    
    def show_business_options(self):
        """Show business system options"""
        print()
        print("🏢 BUSINESS OPERATIONS")
        print("=" * 50)
        
        if not self.business_registered:
            print("You are operating as an individual trader.")
            print("Consider incorporating your business for benefits:")
            print("  • Access to corporate contracts")
            print("  • Better loan terms")
            print("  • Tax advantages")
            print("  • Build business reputation")
            print()
            print("Commands:")
            print("  incorporate          - Register your business (╬5,000)")
            print("  license              - Get required licenses")
            print()
        else:
            print(f"Business: {self.business_name}")
            print(f"Reputation: {self.business_reputation}/100")
            print(f"Licenses: {len(self.business_licenses)}")
            print(f"Active Contracts: {len(self.corporate_contracts)}")
            print(f"Business Loans: {len(self.business_loans)}")
            print()
            print("Commands:")
            print("  license              - Get additional licenses")
            print("  loan                 - Apply for business loans")
            print("  contract             - View available contracts")
            print("  reputation           - Check reputation details")
    
    def incorporate_business(self):
        """Incorporate the player's business"""
        if self.business_registered:
            print("You already have a registered business.")
            return
        
        cost = 5000
        if self.state.talents < cost:
            print(f"Incorporation costs ╬{cost:,}. You only have ╬{self.state.talents:,}.")
            return
        
        print("Incorporating your business...")
        business_name = input("Enter your business name: ").strip()
        if not business_name:
            business_name = f"{self.state.player_name} Trading Corp"
        
        self.state.talents -= cost
        self.business_registered = True
        self.business_name = business_name
        self.business_reputation = 10  # Starting reputation
        
        print()
        print("🎉 Congratulations! Your business has been incorporated.")
        print(f"Business Name: {self.business_name}")
        print("Benefits unlocked:")
        print("  ✅ Corporate contracts available")
        print("  ✅ Business loans available")
        print("  ✅ Factory construction available")
        print("  ✅ Tax advantages on large trades")
    
    def get_business_license(self):
        """Get business licenses"""
        if not self.business_registered:
            print("You must incorporate your business first.")
            return
        
        licenses = {
            "Trading License": {"cost": 2000, "benefit": "Reduced trading fees"},
            "Manufacturing License": {"cost": 10000, "benefit": "Build advanced factories"},
            "Mining License": {"cost": 15000, "benefit": "Build mining facilities"},
            "Research License": {"cost": 25000, "benefit": "Access to tech contracts"}
        }
        
        print()
        print("🏛️ AVAILABLE BUSINESS LICENSES")
        print("=" * 50)
        
        for license_name, info in licenses.items():
            if license_name not in self.business_licenses:
                print(f"{license_name}: ╬{info['cost']:,}")
                print(f"  Benefit: {info['benefit']}")
                print()
        
        if len(self.business_licenses) == len(licenses):
            print("You have all available licenses!")
            return
        
        choice = input("Which license would you like to purchase? ").strip()
        for license_name, info in licenses.items():
            if license_name.lower() in choice.lower() and license_name not in self.business_licenses:
                if self.state.talents >= info['cost']:
                    self.state.talents -= info['cost']
                    self.business_licenses.append(license_name)
                    self.business_reputation += 5
                    print(f"✅ Purchased {license_name}!")
                    print(f"Reputation increased to {self.business_reputation}")
                else:
                    print(f"Insufficient talents. Need ╬{info['cost']:,}, have ╬{self.state.talents:,}.")
                return
        
        print("License not found or already owned.")
    
    def apply_business_loan(self):
        """Apply for business loans"""
        if not self.business_registered:
            print("You must incorporate your business first.")
            return
        
        print()
        print("🏦 BUSINESS LOAN OPTIONS")
        print("=" * 50)
        
        # Loan terms based on reputation
        if self.business_reputation < 20:
            max_loan = 50000
            interest = 0.15
        elif self.business_reputation < 50:
            max_loan = 200000
            interest = 0.10
        else:
            max_loan = 1000000
            interest = 0.05
        
        print(f"Based on your reputation ({self.business_reputation}), you qualify for:")
        print(f"Maximum loan: ╬{max_loan:,}")
        print(f"Interest rate: {interest*100:.1f}%")
        print()
        
        if len(self.business_loans) >= 3:
            print("You already have the maximum number of loans (3).")
            return
        
        amount = input("Loan amount (or 'cancel'): ").strip()
        if amount.lower() == 'cancel':
            return
        
        try:
            loan_amount = int(amount.replace(',', ''))
            if loan_amount > max_loan:
                print(f"Loan amount too high. Maximum: {max_loan:,}")
                return
            if loan_amount < 1000:
                print("Minimum loan amount is ╬1,000.")
                return
            
            # Add loan
            self.business_loans.append({
                'amount': loan_amount,
                'interest': interest,
                'remaining': int(loan_amount * (1 + interest))
            })
            self.state.talents += loan_amount
            
            print(f"✅ Loan approved! ╬{loan_amount:,} added to your account.")
            print(f"Total to repay: ╬{int(loan_amount * (1 + interest)):,}")
            
        except ValueError:
            print("Invalid amount entered.")
    
    def view_contracts(self):
        """View available corporate contracts"""
        if not self.business_registered:
            print("You must incorporate your business first.")
            return
        
        print()
        print("📋 CORPORATE CONTRACTS")
        print("=" * 50)
        
        # Generate some sample contracts based on location and reputation
        if self.business_reputation > 30:
            print("High-value contracts available due to your reputation!")
        
        print("(Contract system coming in future update)")
    
    def check_reputation(self):
        """Check detailed business reputation"""
        if not self.business_registered:
            print("You must incorporate your business first.")
            return
        
        print()
        print("⭐ BUSINESS REPUTATION")
        print("=" * 50)
        print(f"Company: {self.business_name}")
        print(f"Current Reputation: {self.business_reputation}/100")
        
        if self.business_reputation < 25:
            print("Status: New Business")
            print("  • Basic loan terms available")
            print("  • Limited contract access")
        elif self.business_reputation < 50:
            print("Status: Established Business")
            print("  • Better loan terms available")
            print("  • Access to standard contracts")
        elif self.business_reputation < 75:
            print("Status: Reputable Corporation")
            print("  • Excellent loan terms")
            print("  • High-value contracts available")
        else:
            print("Status: Elite Trading House")
            print("  • Premium loan terms")
            print("  • Exclusive contracts available")
        
        print()
        print("Ways to improve reputation:")
        print("  • Complete successful trades")
        print("  • Get business licenses")
        print("  • Complete contracts")
        print("  • Build profitable factories")
    
    def handle_factory_command(self, verb: str, args: List[str]):
        """Handle factory-related commands"""
        if verb == 'factory':
            self.show_factory_options()
        elif verb == 'factories':
            self.list_factories()
        elif verb in ['build', 'construct']:
            self.build_factory(args)
        elif verb == 'automate':
            if args:
                self.build_commodity_factory(args[0])
            else:
                print("Automate what? Try 'automate food' or 'automate electronics'")
        else:
            print("Factory command not recognized. Type 'factory' for options.")
    
    def show_factory_options(self):
        """Show factory system options"""
        print()
        print("🏭 FACTORY AUTOMATION SYSTEM")
        print("=" * 50)
        
        if not self.business_registered:
            print("❌ You must incorporate your business before building factories.")
            print("Use 'incorporate' command first.")
            return
        
        print("Build automated factories to generate passive income!")
        print()
        print("AVAILABLE FACTORY TYPES:")
        print("  Food Processing Plant    - ╬50,000")
        print("    • Generates food every few days")
        print("    • Best built on agricultural worlds")
        print()
        print("  Electronics Factory      - ╬100,000")
        print("    • Generates electronics every few days")
        print("    • Requires materials input")
        print()
        print("  Mining Facility         - ╬75,000")
        print("    • Generates metals and materials")
        print("    • Best built on mining worlds")
        print()
        print("COMMANDS:")
        print("  build factory           - Choose factory type and location")
        print("  automate <commodity>    - Build specific commodity factory")
        print("  factories               - List your factories")
        print()
        print("REQUIREMENTS:")
        print("  • Must have business incorporated")
        print("  • Different locations have different suitability")
        print("  • Factories generate income every few game days")
    
    def list_factories(self):
        """List player's factories"""
        print()
        print("🏭 YOUR FACTORIES")
        print("=" * 50)
        
        if not self.factories:
            print("You don't own any factories yet.")
            print("Use 'build factory' to construct automated facilities.")
            return
        
        total_value = 0
        for location_id, factory in self.factories.items():
            location = LOCATIONS[location_id]
            print(f"📍 {location.name} ({location.system})")
            print(f"   Type: {factory['type']}")
            print(f"   Produces: {factory['produces']}")
            print(f"   Daily Income: ~╬{factory['income']:,}")
            print(f"   Days Operating: {factory['days_active']}")
            total_value += factory['income']
            print()
        
        print(f"Total Daily Passive Income: ~╬{total_value:,}/day")
    
    def build_factory(self, args: List[str]):
        """Build a factory"""
        if not self.business_registered:
            print("You must incorporate your business first.")
            return
        
        # Check if current location is suitable for factories
        loc = self.current_location_obj
        
        factory_types = {
            'food': {'cost': 50000, 'produces': 'food', 'income': 5000},
            'electronics': {'cost': 100000, 'produces': 'electronics', 'income': 12000},
            'mining': {'cost': 75000, 'produces': 'materials', 'income': 8000}
        }
        
        print()
        print(f"🏭 FACTORY CONSTRUCTION AT {loc.name.upper()}")
        print("=" * 50)
        
        # Location suitability
        suitability = []
        if 'food' in loc.produces or 'textiles' in loc.produces:
            suitability.append('food')
        if 'electronics' in loc.produces or 'metals' in loc.produces:
            suitability.append('electronics')
        if 'materials' in loc.produces or 'metals' in loc.produces:
            suitability.append('mining')
        
        if suitability:
            print(f"✅ This location is suitable for: {', '.join(suitability)} factories")
        else:
            print("⚠️  This location is not optimal for factories, but you can still build here.")
        
        print()
        print("Available factory types:")
        for f_type, info in factory_types.items():
            bonus = " (👍 Suitable)" if f_type in suitability else ""
            print(f"  {f_type.title()} Factory: ╬{info['cost']:,}{bonus}")
            print(f"    Daily income: ~╬{info['income']:,}")
            print()
        
        if self.current_location_obj.id in self.factories:
            print("❌ You already have a factory at this location.")
            return
        
        choice = input("Which type of factory? (food/electronics/mining): ").strip().lower()
        
        if choice in factory_types:
            factory_info = factory_types[choice]
            if self.state.talents >= factory_info['cost']:
                self.state.talents -= factory_info['cost']
                
                # Bonus income for suitable locations
                income = factory_info['income']
                if choice in suitability:
                    income = int(income * 1.5)
                    print("💰 Suitability bonus: +50% income!")
                
                self.factories[self.current_location_obj.id] = {
                    'type': f"{choice.title()} Factory",
                    'produces': factory_info['produces'],
                    'income': income,
                    'days_active': 0
                }
                
                self.business_reputation += 10
                print(f"✅ {choice.title()} Factory constructed!")
                print(f"Daily income: ~╬{income:,}")
                print(f"Business reputation increased to {self.business_reputation}")
            else:
                print(f"Insufficient talents. Need ╬{factory_info['cost']:,}, have ╬{self.state.talents:,}.")
        else:
            print("Invalid factory type.")
    
    def build_commodity_factory(self, commodity: str):
        """Build a factory for a specific commodity"""
        commodity_map = {
            'food': 'food',
            'electronics': 'electronics',
            'materials': 'mining',
            'metals': 'mining'
        }
        
        # Find matching commodity
        factory_type = None
        for comm_id, comm in COMMODITIES.items():
            if commodity.lower() in comm.name.lower() or commodity.lower() == comm_id:
                if comm_id in commodity_map:
                    factory_type = commodity_map[comm_id]
                    break
        
        if factory_type:
            self.build_factory([factory_type])
        else:
            print(f"Cannot build a factory for '{commodity}'. Try food, electronics, or materials.")
    
    def process_factory_income(self):
        """Process factory income (called during travel/time passage)"""
        if not self.factories:
            return
        
        total_income = 0
        for location_id, factory in self.factories.items():
            daily_income = factory['income']
            total_income += daily_income
            factory['days_active'] += 1
        
        if total_income > 0:
            self.state.talents += total_income
            self.business_reputation += 1
            print(f"💰 Your factories generated ╬{total_income:,} in passive income!")
    
    def quit_game(self):
        print()
        print("Thanks for playing TradeWinds!")
        print(f"Final stats for Captain {self.state.player_name}:")
        print(f"  Talents earned: ╬{self.state.talents:,}")
        print(f"  Days traveled: {self.state.days_elapsed}")
        print(f"  Locations visited: {len(self.state.visited_locations)}")
        
        profit = self.state.talents - 1000
        if profit > 0:
            print(f"  Net profit: ╬{profit:,}! 💰")
        else:
            print(f"  Net loss: ╬{abs(profit):,} 📉")
        
        print()
        print("May the stars guide you safely home! 🌟")
        self.running = False

def main():
    game = TextAdventure()
    game.start_game()

if __name__ == "__main__":
    main()