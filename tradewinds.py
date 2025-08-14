# TradeWinds - Space Trading Game
# A text adventure space trading game

import random
from typing import Dict, List

class Player:
    """Represents the player character with their ship, inventory, and status"""
    
    def __init__(self, name: str = "Captain"):
        self.name = name
        self.credits = 1000  # Starting money
        self.current_location = "Earth Station"
        
        # Ship properties
        self.ship_name = "Starwind"
        self.max_cargo = 50  # Maximum cargo capacity
        self.current_cargo = 0  # Current cargo weight
        
        # Inventory: commodity_name -> quantity
        self.inventory: Dict[str, int] = {}
        
        # Player stats
        self.reputation = 0
        self.total_profits = 0
        self.days_elapsed = 0
    
    def add_cargo(self, commodity: str, quantity: int) -> bool:
        """Add cargo to inventory if there's space"""
        if self.current_cargo + quantity <= self.max_cargo:
            if commodity in self.inventory:
                self.inventory[commodity] += quantity
            else:
                self.inventory[commodity] = quantity
            self.current_cargo += quantity
            return True
        return False
    
    def remove_cargo(self, commodity: str, quantity: int) -> bool:
        """Remove cargo from inventory"""
        if commodity in self.inventory and self.inventory[commodity] >= quantity:
            self.inventory[commodity] -= quantity
            if self.inventory[commodity] == 0:
                del self.inventory[commodity]
            self.current_cargo -= quantity
            return True
        return False
    
    def get_cargo_space(self) -> int:
        """Get available cargo space"""
        return self.max_cargo - self.current_cargo
    
    def add_credits(self, amount: int):
        """Add credits to player's account"""
        self.credits += amount
        if amount > 0:
            self.total_profits += amount
    
    def spend_credits(self, amount: int) -> bool:
        """Spend credits if player has enough"""
        if self.credits >= amount:
            self.credits -= amount
            return True
        return False
    
    def show_status(self):
        """Display player status"""
        print(f"\n=== {self.name}'s Status ===")
        print(f"Credits: {self.credits:,}")
        print(f"Location: {self.current_location}")
        print(f"Ship: {self.ship_name}")
        print(f"Cargo: {self.current_cargo}/{self.max_cargo}")
        print(f"Days Elapsed: {self.days_elapsed}")
        print(f"Total Profits: {self.total_profits:,}")
        print(f"Reputation: {self.reputation}")
        
        if self.inventory:
            print("\nCargo Hold:")
            for commodity, quantity in self.inventory.items():
                print(f"  {commodity}: {quantity}")
        else:
            print("\nCargo Hold: Empty")

class Commodity:
    """Represents a tradeable commodity"""
    
    def __init__(self, name: str, base_price: int, volatility: float = 0.2):
        self.name = name
        self.base_price = base_price
        self.volatility = volatility  # Price variation factor
    
    def get_market_price(self, supply_demand: float = 1.0) -> int:
        """Calculate current market price based on supply/demand"""
        variation = random.uniform(-self.volatility, self.volatility)
        price = self.base_price * (1 + variation) * supply_demand
        return max(1, int(price))  # Minimum price of 1 credit

class Location:
    """Represents a space station, planet, or colony"""
    
    def __init__(self, name: str, system: str, description: str, 
                 produces: List[str] = None, consumes: List[str] = None,
                 distance_from_earth: float = 0):
        self.name = name
        self.system = system
        self.description = description
        self.produces = produces or []  # Commodities this location produces (cheaper)
        self.consumes = consumes or []  # Commodities this location needs (expensive)
        self.distance_from_earth = distance_from_earth  # Light years
        
        # Generate current market prices
        self.market_prices: Dict[str, int] = {}
        self._generate_market_prices()
    
    def _generate_market_prices(self):
        """Generate current market prices based on supply/demand"""
        for commodity_name, commodity in COMMODITIES.items():
            # Base supply/demand factor
            supply_demand = 1.0
            
            # Producers have lower prices (more supply)
            if commodity_name in self.produces:
                supply_demand = random.uniform(0.6, 0.8)
            
            # Consumers have higher prices (more demand)
            elif commodity_name in self.consumes:
                supply_demand = random.uniform(1.2, 1.6)
            
            # Normal market fluctuation for other goods
            else:
                supply_demand = random.uniform(0.9, 1.1)
            
            self.market_prices[commodity_name] = commodity.get_market_price(supply_demand)
    
    def refresh_market(self):
        """Refresh market prices (call when player visits or time passes)"""
        self._generate_market_prices()
    
    def get_distance_to(self, other_location: 'Location') -> float:
        """Calculate travel distance to another location (simplified)"""
        # Simplified calculation - in reality would use 3D coordinates
        if self.system == other_location.system:
            return 0.1  # Same system
        else:
            # Rough approximation based on distance from Earth
            return abs(self.distance_from_earth - other_location.distance_from_earth) + 1

# Define common commodities
COMMODITIES = {
    "Food": Commodity("Food", 10, 0.15),
    "Water": Commodity("Water", 5, 0.1),
    "Medicine": Commodity("Medicine", 50, 0.3),
    "Electronics": Commodity("Electronics", 100, 0.25),
    "Metals": Commodity("Metals", 25, 0.2),
    "Textiles": Commodity("Textiles", 15, 0.2),
    "Weapons": Commodity("Weapons", 200, 0.4),
    "Fuel": Commodity("Fuel", 20, 0.3),
    "Luxury Goods": Commodity("Luxury Goods", 150, 0.35),
    "Raw Materials": Commodity("Raw Materials", 8, 0.15)
}

# Define real star systems and locations
LOCATIONS = {
    # Sol System (Our Solar System)
    "Earth Station": Location(
        name="Earth Station", 
        system="Sol",
        description="Humanity's birthworld and primary trading hub. Orbital stations bustling with commerce.",
        produces=["Luxury Goods", "Electronics", "Medicine"],
        consumes=["Raw Materials", "Metals"],
        distance_from_earth=0
    ),
    
    "Mars Colony": Location(
        name="Mars Colony",
        system="Sol", 
        description="The first major off-world colony. Red rock mining operations and terraforming efforts.",
        produces=["Metals", "Raw Materials"],
        consumes=["Food", "Water", "Medicine"],
        distance_from_earth=0
    ),
    
    "Europa Station": Location(
        name="Europa Station",
        system="Sol",
        description="Ice mining facility on Jupiter's moon. Source of the solar system's water supply.",
        produces=["Water", "Fuel"],
        consumes=["Electronics", "Food", "Textiles"],
        distance_from_earth=0
    ),
    
    "Titan Refinery": Location(
        name="Titan Refinery",
        system="Sol",
        description="Hydrocarbon processing on Saturn's largest moon. Industrial complex in perpetual twilight.",
        produces=["Fuel", "Raw Materials"],
        consumes=["Electronics", "Food"],
        distance_from_earth=0
    ),
    
    # Alpha Centauri System (Closest star system - 4.37 ly)
    "Proxima Colony": Location(
        name="Proxima Colony",
        system="Alpha Centauri",
        description="Humanity's first interstellar colony orbiting Proxima Centauri. A testament to human determination.",
        produces=["Food"],
        consumes=["Electronics", "Medicine", "Luxury Goods"],
        distance_from_earth=4.37
    ),
    
    # Sirius System (8.6 ly)
    "Sirius Trade Hub": Location(
        name="Sirius Trade Hub",
        system="Sirius",
        description="Major commercial waystation in the bright Sirius system. Gateway to the outer colonies.",
        produces=["Electronics", "Weapons"],
        consumes=["Food", "Raw Materials"],
        distance_from_earth=8.6
    ),
    
    # Vega System (25.3 ly)
    "Vega Agricultural": Location(
        name="Vega Agricultural",
        system="Vega", 
        description="Vast agricultural worlds under Vega's bright light. Feeds much of human space.",
        produces=["Food", "Textiles"],
        consumes=["Electronics", "Metals", "Medicine"],
        distance_from_earth=25.3
    ),
    
    # Altair System (16.7 ly)
    "Altair Industrial": Location(
        name="Altair Industrial",
        system="Altair",
        description="Heavy industry and manufacturing. The forge worlds of human space.",
        produces=["Electronics", "Weapons", "Metals"],
        consumes=["Raw Materials", "Food", "Water"],
        distance_from_earth=16.7
    ),
    
    # Wolf 359 System (7.9 ly)
    "Wolf 359 Outpost": Location(
        name="Wolf 359 Outpost",
        system="Wolf 359",
        description="Remote mining outpost around a red dwarf star. Dangerous but profitable.",
        produces=["Raw Materials", "Metals"],
        consumes=["Food", "Water", "Medicine"],
        distance_from_earth=7.9
    ),
    
    # TRAPPIST-1 System (39.5 ly)
    "TRAPPIST Research": Location(
        name="TRAPPIST Research",
        system="TRAPPIST-1", 
        description="Scientific research station studying the seven-planet system. Knowledge is power.",
        produces=["Medicine", "Electronics"],
        consumes=["Food", "Luxury Goods"],
        distance_from_earth=39.5
    ),
    
    # Kepler-452 System (1,400 ly - distant future colony)
    "Kepler Paradise": Location(
        name="Kepler Paradise",
        system="Kepler-452",
        description="Earth-like world in the far reaches. Paradise for those who can afford the journey.",
        produces=["Luxury Goods", "Food"],
        consumes=["Electronics", "Medicine", "Weapons"],
        distance_from_earth=1400
    ),
    
    # Gliese 581 System (20.4 ly)
    "Gliese Station": Location(
        name="Gliese Station", 
        system="Gliese 581",
        description="Research and survey station in the habitable zone. Frontier science at its finest.",
        produces=["Medicine"],
        consumes=["Food", "Electronics", "Water"],
        distance_from_earth=20.4
    )
}

def create_player() -> Player:
    """Create and initialize a new player"""
    print("Welcome to TradeWinds - The Space Trading Adventure!")
    print("=" * 50)
    
    name = input("Enter your captain's name (or press Enter for 'Captain'): ").strip()
    if not name:
        name = "Captain"
    
    ship_name = input("Enter your ship's name (or press Enter for 'Starwind'): ").strip()
    if not ship_name:
        ship_name = "Starwind"
    
    player = Player(name)
    player.ship_name = ship_name  # Update the ship name
    
    print(f"\nWelcome aboard, {player.name}!")
    print(f"You command the starship '{player.ship_name}' with {player.credits:,} credits.")
    print(f"Your cargo hold can carry up to {player.max_cargo} units.")
    print(f"Ready to explore the galaxy and make your fortune!")
    
    return player

def show_location_info(location: Location):
    """Display information about the current location"""
    print(f"\n=== {location.name} ===")
    print(f"System: {location.system}")
    print(f"Distance from Earth: {location.distance_from_earth} light-years")
    print(f"Description: {location.description}")
    
    if location.produces:
        print(f"Produces: {', '.join(location.produces)}")
    if location.consumes:
        print(f"In demand: {', '.join(location.consumes)}")

def show_market_prices(location: Location):
    """Display current market prices at the location"""
    print(f"\n=== Market Prices at {location.name} ===")
    print("Commodity          | Buy Price | Notes")
    print("-" * 45)
    
    for commodity, price in location.market_prices.items():
        notes = ""
        if commodity in location.produces:
            notes = "📉 Cheap (Local Production)"
        elif commodity in location.consumes:
            notes = "📈 Expensive (High Demand)"
        
        print(f"{commodity:<18} | {price:>8} | {notes}")

def list_destinations(current_location: Location):
    """Show available travel destinations"""
    print(f"\n=== Travel Destinations from {current_location.name} ===")
    print("Destination                 | System        | Distance (ly)")
    print("-" * 60)
    
    destinations = []
    for loc_name, location in LOCATIONS.items():
        if loc_name != current_location.name:
            distance = current_location.get_distance_to(location)
            destinations.append((loc_name, location, distance))
    
    # Sort by distance
    destinations.sort(key=lambda x: x[2])
    
    for i, (name, location, distance) in enumerate(destinations, 1):
        print(f"{i:2}. {name:<25} | {location.system:<12} | {distance:.1f}")
    
    return destinations

def travel_to_location(player: Player, destination_name: str):
    """Travel to a new location"""
    if destination_name in LOCATIONS:
        old_location = LOCATIONS[player.current_location]
        new_location = LOCATIONS[destination_name]
        
        # Calculate travel time and cost
        distance = old_location.get_distance_to(new_location)
        travel_time = max(1, int(distance))
        fuel_cost = max(10, int(distance * 5))
        
        if player.spend_credits(fuel_cost):
            player.current_location = destination_name
            player.days_elapsed += travel_time
            
            # Refresh market at new location
            new_location.refresh_market()
            
            print(f"\n🚀 Traveling to {destination_name}...")
            print(f"Travel time: {travel_time} days")
            print(f"Fuel cost: {fuel_cost} credits")
            print(f"Arrived at {destination_name}!")
            
            show_location_info(new_location)
            return True
        else:
            print(f"❌ Not enough credits for fuel! Need {fuel_cost} credits.")
            return False
    else:
        print(f"❌ Unknown destination: {destination_name}")
        return False

def buy_cargo(player: Player, location: Location):
    """Buy cargo at current location"""
    print(f"\n=== Buy Cargo at {location.name} ===")
    
    # Show available commodities and prices
    available_commodities = []
    for commodity, price in location.market_prices.items():
        max_affordable = player.credits // price
        max_space = player.get_cargo_space()
        max_buyable = min(max_affordable, max_space)
        
        if max_buyable > 0:
            available_commodities.append((commodity, price, max_buyable))
    
    if not available_commodities:
        print("❌ Nothing available to buy (insufficient credits or cargo space full)")
        return
    
    print("Commodity          | Price | Max You Can Buy")
    print("-" * 50)
    for i, (commodity, price, max_qty) in enumerate(available_commodities, 1):
        notes = ""
        if commodity in location.produces:
            notes = " 📉"
        elif commodity in location.consumes:
            notes = " 📈"
        print(f"{i:2}. {commodity:<14} | {price:>5} | {max_qty:>10}{notes}")
    
    try:
        choice = input("\nSelect commodity number (or 'back'): ").strip()
        if choice.lower() == 'back':
            return
            
        choice_num = int(choice)
        if 1 <= choice_num <= len(available_commodities):
            commodity, price, max_qty = available_commodities[choice_num - 1]
            
            quantity = input(f"How many {commodity} to buy (max {max_qty}): ").strip()
            quantity = int(quantity)
            
            if 1 <= quantity <= max_qty:
                total_cost = price * quantity
                if player.spend_credits(total_cost):
                    if player.add_cargo(commodity, quantity):
                        print(f"✅ Bought {quantity} {commodity} for {total_cost} credits!")
                    else:
                        # Refund if cargo add failed
                        player.add_credits(total_cost)
                        print("❌ Cargo hold full!")
                else:
                    print("❌ Not enough credits!")
            else:
                print("❌ Invalid quantity!")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def sell_cargo(player: Player, location: Location):
    """Sell cargo at current location"""
    if not player.inventory:
        print("❌ No cargo to sell!")
        return
    
    print(f"\n=== Sell Cargo at {location.name} ===")
    print("Your Cargo         | Quantity | Sell Price | Total Value")
    print("-" * 60)
    
    sellable_items = []
    for commodity, quantity in player.inventory.items():
        sell_price = location.market_prices[commodity]
        total_value = sell_price * quantity
        sellable_items.append((commodity, quantity, sell_price, total_value))
    
    for i, (commodity, qty, price, total) in enumerate(sellable_items, 1):
        notes = ""
        if commodity in location.consumes:
            notes = " 📈"
        elif commodity in location.produces:
            notes = " 📉"
        print(f"{i:2}. {commodity:<14} | {qty:>8} | {price:>10} | {total:>11}{notes}")
    
    try:
        choice = input("\nSelect cargo to sell (or 'back'): ").strip()
        if choice.lower() == 'back':
            return
            
        choice_num = int(choice)
        if 1 <= choice_num <= len(sellable_items):
            commodity, available_qty, price, _ = sellable_items[choice_num - 1]
            
            quantity = input(f"How many {commodity} to sell (max {available_qty}): ").strip()
            quantity = int(quantity)
            
            if 1 <= quantity <= available_qty:
                total_earned = price * quantity
                if player.remove_cargo(commodity, quantity):
                    player.add_credits(total_earned)
                    print(f"✅ Sold {quantity} {commodity} for {total_earned} credits!")
                else:
                    print("❌ Error selling cargo!")
            else:
                print("❌ Invalid quantity!")
        else:
            print("❌ Invalid choice!")
    except ValueError:
        print("❌ Please enter a valid number!")

def main():
    """Main game function"""
    player = create_player()
    
    # Show starting location
    current_location = LOCATIONS[player.current_location]
    show_location_info(current_location)
    player.show_status()
    
    # Simple game loop
    print("\n" + "="*50)
    print("COMMANDS: status | location | market | buy | sell | travel | destinations | quit")
    print("="*50)
    
    while True:
        command = input("\n> ").lower().strip()
        
        if command == "quit":
            print("Thanks for playing TradeWinds! Safe travels, Captain!")
            break
            
        elif command == "status":
            player.show_status()
            
        elif command == "location":
            current_location = LOCATIONS[player.current_location]
            show_location_info(current_location)
            
        elif command == "market":
            current_location = LOCATIONS[player.current_location]
            show_market_prices(current_location)
            
        elif command == "buy":
            current_location = LOCATIONS[player.current_location]
            buy_cargo(player, current_location)
            
        elif command == "sell":
            current_location = LOCATIONS[player.current_location]
            sell_cargo(player, current_location)
            
        elif command == "destinations":
            current_location = LOCATIONS[player.current_location]
            destinations = list_destinations(current_location)
            
        elif command == "travel":
            current_location = LOCATIONS[player.current_location]
            destinations = list_destinations(current_location)
            
            try:
                choice = input("\nEnter destination number (or 'back'): ").strip()
                if choice.lower() == 'back':
                    continue
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(destinations):
                    dest_name = destinations[choice_num - 1][0]
                    travel_to_location(player, dest_name)
                else:
                    print("❌ Invalid choice!")
            except ValueError:
                print("❌ Please enter a valid number!")
                
        else:
            print("❌ Unknown command! Available: status | location | market | buy | sell | travel | destinations | quit")

if __name__ == "__main__":
    main()