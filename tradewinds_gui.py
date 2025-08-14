"""
TradeWinds GUI - Windows Desktop Version
A space trading game with real star systems
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from typing import Dict, List
import json

# Game Data Classes (same as CLI version)
class Commodity:
    def __init__(self, name: str, base_price: int, volatility: float):
        self.name = name
        self.base_price = base_price
        self.volatility = volatility
    
    def get_market_price(self, supply_demand: float) -> int:
        variation = random.uniform(-self.volatility, self.volatility)
        price = self.base_price * (1 + variation) * supply_demand
        return max(1, int(price))

class Location:
    def __init__(self, name: str, system: str, description: str, 
                 produces: List[str] = None, consumes: List[str] = None,
                 distance_from_earth: float = 0):
        self.name = name
        self.system = system
        self.description = description
        self.produces = produces or []
        self.consumes = consumes or []
        self.distance_from_earth = distance_from_earth
        
        self.market_prices: Dict[str, int] = {}
        self._generate_market_prices()
    
    def _generate_market_prices(self):
        for commodity_name, commodity in COMMODITIES.items():
            supply_demand = 1.0
            if commodity_name in self.produces:
                supply_demand = random.uniform(0.6, 0.8)
            elif commodity_name in self.consumes:
                supply_demand = random.uniform(1.2, 1.6)
            else:
                supply_demand = random.uniform(0.9, 1.1)
            
            self.market_prices[commodity_name] = commodity.get_market_price(supply_demand)
    
    def refresh_market(self):
        self._generate_market_prices()
    
    def get_distance_to(self, other_location: 'Location') -> float:
        if self.system == other_location.system:
            return 0.1
        else:
            return abs(self.distance_from_earth - other_location.distance_from_earth) + 1

class Player:
    def __init__(self, name: str):
        self.name = name
        self.ship_name = "Starwind"
        self.credits = 1000
        self.current_location = "Earth Station"
        self.inventory: Dict[str, int] = {}
        self.max_cargo = 50
        self.days_elapsed = 0
    
    def get_cargo_count(self) -> int:
        return sum(self.inventory.values())
    
    def get_cargo_space(self) -> int:
        return self.max_cargo - self.get_cargo_count()
    
    def add_cargo(self, commodity: str, quantity: int) -> bool:
        if self.get_cargo_count() + quantity <= self.max_cargo:
            self.inventory[commodity] = self.inventory.get(commodity, 0) + quantity
            return True
        return False
    
    def remove_cargo(self, commodity: str, quantity: int) -> bool:
        if self.inventory.get(commodity, 0) >= quantity:
            self.inventory[commodity] -= quantity
            if self.inventory[commodity] == 0:
                del self.inventory[commodity]
            return True
        return False
    
    def spend_credits(self, amount: int) -> bool:
        if self.credits >= amount:
            self.credits -= amount
            return True
        return False
    
    def add_credits(self, amount: int):
        self.credits += amount

# Game Data
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

LOCATIONS = {
    "Earth Station": Location(
        "Earth Station", "Sol",
        "Humanity's birthworld and primary trading hub. Orbital stations bustling with commerce.",
        ["Luxury Goods", "Electronics", "Medicine"], ["Raw Materials", "Metals"], 0
    ),
    "Mars Colony": Location(
        "Mars Colony", "Sol", 
        "The first major off-world colony. Red rock mining operations and terraforming efforts.",
        ["Metals", "Raw Materials"], ["Food", "Water", "Medicine"], 0
    ),
    "Europa Station": Location(
        "Europa Station", "Sol",
        "Ice mining facility on Jupiter's moon. Source of the solar system's water supply.",
        ["Water", "Fuel"], ["Electronics", "Food", "Textiles"], 0
    ),
    "Titan Refinery": Location(
        "Titan Refinery", "Sol",
        "Hydrocarbon processing on Saturn's largest moon. Industrial complex in perpetual twilight.",
        ["Fuel", "Raw Materials"], ["Electronics", "Food"], 0
    ),
    "Proxima Colony": Location(
        "Proxima Colony", "Alpha Centauri",
        "Humanity's first interstellar colony orbiting Proxima Centauri. A testament to human determination.",
        ["Food"], ["Electronics", "Medicine", "Luxury Goods"], 4.37
    ),
    "Sirius Trade Hub": Location(
        "Sirius Trade Hub", "Sirius",
        "Major commercial waystation in the bright Sirius system. Gateway to the outer colonies.",
        ["Electronics", "Weapons"], ["Food", "Raw Materials"], 8.6
    ),
    "Vega Agricultural": Location(
        "Vega Agricultural", "Vega", 
        "Vast agricultural worlds under Vega's bright light. Feeds much of human space.",
        ["Food", "Textiles"], ["Electronics", "Metals", "Medicine"], 25.3
    ),
    "Altair Industrial": Location(
        "Altair Industrial", "Altair",
        "Heavy industry and manufacturing. The forge worlds of human space.",
        ["Electronics", "Weapons", "Metals"], ["Raw Materials", "Food", "Water"], 16.7
    ),
    "Wolf 359 Outpost": Location(
        "Wolf 359 Outpost", "Wolf 359",
        "Remote mining outpost around a red dwarf star. Dangerous but profitable.",
        ["Raw Materials", "Metals"], ["Food", "Water", "Medicine"], 7.9
    ),
    "TRAPPIST Research": Location(
        "TRAPPIST Research", "TRAPPIST-1", 
        "Scientific research station studying the seven-planet system. Knowledge is power.",
        ["Medicine", "Electronics"], ["Food", "Luxury Goods"], 39.5
    ),
    "Kepler Paradise": Location(
        "Kepler Paradise", "Kepler-452",
        "Earth-like world in the far reaches. Paradise for those who can afford the journey.",
        ["Luxury Goods", "Food"], ["Electronics", "Medicine", "Weapons"], 1400
    ),
    "Gliese Station": Location(
        "Gliese Station", "Gliese 581",
        "Research and survey station in the habitable zone. Frontier science at its finest.",
        ["Medicine"], ["Food", "Electronics", "Water"], 20.4
    )
}

class TradeWindsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 TradeWinds - Space Trading Adventure")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a3e')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.player = None
        self.current_location = None
        
        # Create main container
        self.main_frame = tk.Frame(root, bg='#1a1a3e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.show_start_screen()
    
    def configure_styles(self):
        # Configure ttk styles for space theme
        self.style.configure('Title.TLabel', 
                           background='#1a1a3e', 
                           foreground='#00d4ff', 
                           font=('Helvetica', 24, 'bold'))
        
        self.style.configure('Heading.TLabel', 
                           background='#1a1a3e', 
                           foreground='#00d4ff', 
                           font=('Helvetica', 16, 'bold'))
        
        self.style.configure('Info.TLabel', 
                           background='#1a1a3e', 
                           foreground='#e0e0e0', 
                           font=('Helvetica', 10))
        
        self.style.configure('Space.TButton',
                           background='#00d4ff',
                           foreground='white',
                           font=('Helvetica', 12, 'bold'))
        
        self.style.map('Space.TButton',
                      background=[('active', '#4ecdc4')])
    
    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_start_screen(self):
        self.clear_screen()
        
        # Title
        title_frame = tk.Frame(self.main_frame, bg='#1a1a3e')
        title_frame.pack(pady=50)
        
        ttk.Label(title_frame, text="🚀 TradeWinds", style='Title.TLabel').pack()
        ttk.Label(title_frame, text="Space Trading Adventure", 
                 background='#1a1a3e', foreground='#b0b0b0', 
                 font=('Helvetica', 14)).pack(pady=(10, 30))
        
        # Input form
        form_frame = tk.Frame(self.main_frame, bg='#2d1b4e', relief='ridge', bd=2)
        form_frame.pack(pady=20, padx=50, ipadx=30, ipady=30)
        
        ttk.Label(form_frame, text="Captain's Name:", 
                 background='#2d1b4e', foreground='#00d4ff', 
                 font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(10, 5))
        
        self.captain_entry = tk.Entry(form_frame, font=('Helvetica', 12), 
                                     bg='#1a1a3e', fg='#e0e0e0', 
                                     insertbackground='#00d4ff', width=30)
        self.captain_entry.pack(pady=(0, 15))
        self.captain_entry.insert(0, "Captain")
        
        ttk.Label(form_frame, text="Ship Name:", 
                 background='#2d1b4e', foreground='#00d4ff', 
                 font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        self.ship_entry = tk.Entry(form_frame, font=('Helvetica', 12), 
                                  bg='#1a1a3e', fg='#e0e0e0', 
                                  insertbackground='#00d4ff', width=30)
        self.ship_entry.pack(pady=(0, 20))
        self.ship_entry.insert(0, "Starwind")
        
        start_btn = tk.Button(form_frame, text="🚀 Begin Your Journey",
                             font=('Helvetica', 14, 'bold'),
                             bg='#00d4ff', fg='white', 
                             relief='flat', pady=10,
                             command=self.start_game)
        start_btn.pack(pady=10)
        
        # Game info
        info_frame = tk.Frame(self.main_frame, bg='#1a1a3e')
        info_frame.pack(pady=30)
        
        info_text = [
            "🌌 Explore 12 real star systems",
            "💰 Buy low, sell high across the galaxy", 
            "🚢 Command your own starship",
            "🌍 Trade between actual planets and stations"
        ]
        
        for info in info_text:
            ttk.Label(info_frame, text=info, 
                     background='#1a1a3e', foreground='#b0b0b0', 
                     font=('Helvetica', 11)).pack(pady=2)
    
    def start_game(self):
        captain_name = self.captain_entry.get().strip() or "Captain"
        ship_name = self.ship_entry.get().strip() or "Starwind"
        
        self.player = Player(captain_name)
        self.player.ship_name = ship_name
        self.current_location = LOCATIONS[self.player.current_location]
        
        self.show_main_game()
    
    def show_main_game(self):
        self.clear_screen()
        
        # Create main game layout
        # Header with player status
        self.create_header()
        
        # Main content area with notebook tabs
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg='#0a0a23', relief='ridge', bd=2)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        # Player info on left
        player_frame = tk.Frame(header_frame, bg='#0a0a23')
        player_frame.pack(side='left', padx=20, pady=10)
        
        ttk.Label(player_frame, text=f"Captain {self.player.name}", 
                 style='Heading.TLabel').pack(anchor='w')
        ttk.Label(player_frame, text=f"Ship: {self.player.ship_name}", 
                 background='#0a0a23', foreground='#b0b0b0', 
                 font=('Helvetica', 10)).pack(anchor='w')
        
        # Status info on right
        status_frame = tk.Frame(header_frame, bg='#0a0a23')
        status_frame.pack(side='right', padx=20, pady=10)
        
        self.credits_label = ttk.Label(status_frame, text=f"Credits: {self.player.credits:,}", 
                                      background='#0a0a23', foreground='#00d4ff', 
                                      font=('Helvetica', 12, 'bold'))
        self.credits_label.pack(side='left', padx=(0, 20))
        
        self.cargo_label = ttk.Label(status_frame, text=f"Cargo: {self.player.get_cargo_count()}/{self.player.max_cargo}", 
                                    background='#0a0a23', foreground='#4ecdc4', 
                                    font=('Helvetica', 12, 'bold'))
        self.cargo_label.pack(side='left', padx=(0, 20))
        
        self.days_label = ttk.Label(status_frame, text=f"Days: {self.player.days_elapsed}", 
                                   background='#0a0a23', foreground='#ff6b6b', 
                                   font=('Helvetica', 12, 'bold'))
        self.days_label.pack(side='left')
    
    def create_main_content(self):
        # Create notebook for different screens
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Location tab
        location_frame = tk.Frame(notebook, bg='#1a1a3e')
        notebook.add(location_frame, text='🌍 Location')
        self.create_location_tab(location_frame)
        
        # Market tab  
        market_frame = tk.Frame(notebook, bg='#1a1a3e')
        notebook.add(market_frame, text='🏪 Market')
        self.create_market_tab(market_frame)
        
        # Travel tab
        travel_frame = tk.Frame(notebook, bg='#1a1a3e')
        notebook.add(travel_frame, text='🚀 Travel')
        self.create_travel_tab(travel_frame)
        
        self.notebook = notebook
    
    def create_location_tab(self, parent):
        # Location information
        location_info = tk.Frame(parent, bg='#2d1b4e', relief='ridge', bd=2)
        location_info.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_text = f"🌍 {self.current_location.name}"
        ttk.Label(location_info, text=title_text, style='Title.TLabel').pack(pady=(20, 10))
        
        # System and distance
        info_frame = tk.Frame(location_info, bg='#2d1b4e')
        info_frame.pack(pady=10)
        
        ttk.Label(info_frame, text=f"System: {self.current_location.system}", 
                 background='#2d1b4e', foreground='#4ecdc4', 
                 font=('Helvetica', 12, 'bold')).pack()
        
        ttk.Label(info_frame, text=f"Distance from Earth: {self.current_location.distance_from_earth} light-years", 
                 background='#2d1b4e', foreground='#b0b0b0', 
                 font=('Helvetica', 11)).pack(pady=5)
        
        # Description
        desc_frame = tk.Frame(location_info, bg='#1a1a3e', relief='sunken', bd=2)
        desc_frame.pack(fill='x', padx=20, pady=20)
        
        desc_label = tk.Label(desc_frame, text=self.current_location.description, 
                             bg='#1a1a3e', fg='#e0e0e0', 
                             font=('Helvetica', 11), wraplength=800, justify='center')
        desc_label.pack(pady=15)
        
        # Produces and Consumes
        trade_frame = tk.Frame(location_info, bg='#2d1b4e')
        trade_frame.pack(fill='x', padx=20, pady=10)
        
        if self.current_location.produces:
            produces_frame = tk.Frame(trade_frame, bg='#2d1b4e')
            produces_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            ttk.Label(produces_frame, text="🏭 Produces:", 
                     background='#2d1b4e', foreground='#4ecdc4', 
                     font=('Helvetica', 12, 'bold')).pack(anchor='w')
            
            for item in self.current_location.produces:
                ttk.Label(produces_frame, text=f"• {item}", 
                         background='#2d1b4e', foreground='#4ecdc4', 
                         font=('Helvetica', 10)).pack(anchor='w')
        
        if self.current_location.consumes:
            consumes_frame = tk.Frame(trade_frame, bg='#2d1b4e')
            consumes_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
            
            ttk.Label(consumes_frame, text="📈 In Demand:", 
                     background='#2d1b4e', foreground='#ff6b6b', 
                     font=('Helvetica', 12, 'bold')).pack(anchor='w')
            
            for item in self.current_location.consumes:
                ttk.Label(consumes_frame, text=f"• {item}", 
                         background='#2d1b4e', foreground='#ff6b6b', 
                         font=('Helvetica', 10)).pack(anchor='w')
    
    def create_market_tab(self, parent):
        market_frame = tk.Frame(parent, bg='#1a1a3e')
        market_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(market_frame, text=f"🏪 Market at {self.current_location.name}", 
                 style='Title.TLabel').pack(pady=(10, 20))
        
        # Trade mode buttons
        mode_frame = tk.Frame(market_frame, bg='#1a1a3e')
        mode_frame.pack(pady=10)
        
        self.trade_mode = tk.StringVar(value="buy")
        
        buy_btn = tk.Radiobutton(mode_frame, text="Buy", variable=self.trade_mode, value="buy",
                               bg='#1a1a3e', fg='#00d4ff', selectcolor='#2d1b4e',
                               font=('Helvetica', 12, 'bold'), 
                               command=self.refresh_market_display)
        buy_btn.pack(side='left', padx=20)
        
        sell_btn = tk.Radiobutton(mode_frame, text="Sell", variable=self.trade_mode, value="sell",
                                bg='#1a1a3e', fg='#00d4ff', selectcolor='#2d1b4e',
                                font=('Helvetica', 12, 'bold'),
                                command=self.refresh_market_display)
        sell_btn.pack(side='left', padx=20)
        
        # Market display frame with scrollbar
        market_display_frame = tk.Frame(market_frame, bg='#1a1a3e')
        market_display_frame.pack(fill='both', expand=True, pady=10)
        
        self.market_canvas = tk.Canvas(market_display_frame, bg='#1a1a3e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(market_display_frame, orient="vertical", command=self.market_canvas.yview)
        self.market_scrollable_frame = tk.Frame(self.market_canvas, bg='#1a1a3e')
        
        self.market_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.market_canvas.configure(scrollregion=self.market_canvas.bbox("all"))
        )
        
        self.market_canvas.create_window((0, 0), window=self.market_scrollable_frame, anchor="nw")
        self.market_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.market_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_market_display()
    
    def create_travel_tab(self, parent):
        travel_frame = tk.Frame(parent, bg='#1a1a3e')
        travel_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(travel_frame, text=f"🚀 Travel from {self.current_location.name}", 
                 style='Title.TLabel').pack(pady=(10, 20))
        
        # Destinations with scrollbar
        dest_frame = tk.Frame(travel_frame, bg='#1a1a3e')
        dest_frame.pack(fill='both', expand=True)
        
        self.travel_canvas = tk.Canvas(dest_frame, bg='#1a1a3e', highlightthickness=0)
        travel_scrollbar = ttk.Scrollbar(dest_frame, orient="vertical", command=self.travel_canvas.yview)
        self.travel_scrollable_frame = tk.Frame(self.travel_canvas, bg='#1a1a3e')
        
        self.travel_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.travel_canvas.configure(scrollregion=self.travel_canvas.bbox("all"))
        )
        
        self.travel_canvas.create_window((0, 0), window=self.travel_scrollable_frame, anchor="nw")
        self.travel_canvas.configure(yscrollcommand=travel_scrollbar.set)
        
        self.travel_canvas.pack(side="left", fill="both", expand=True)
        travel_scrollbar.pack(side="right", fill="y")
        
        self.refresh_travel_display()
    
    def create_status_bar(self):
        status_frame = tk.Frame(self.main_frame, bg='#0a0a23', relief='sunken', bd=1)
        status_frame.pack(fill='x', side='bottom')
        
        ttk.Label(status_frame, text=f"Currently at: {self.current_location.name} | {self.current_location.system} System", 
                 background='#0a0a23', foreground='#b0b0b0', 
                 font=('Helvetica', 9)).pack(side='left', padx=10, pady=5)
    
    def refresh_market_display(self):
        # Clear existing market items
        for widget in self.market_scrollable_frame.winfo_children():
            widget.destroy()
        
        mode = self.trade_mode.get()
        
        row = 0
        for commodity_name in COMMODITIES:
            price = self.current_location.market_prices[commodity_name]
            
            # Create commodity frame
            comm_frame = tk.Frame(self.market_scrollable_frame, bg='#2d1b4e', relief='ridge', bd=1)
            comm_frame.pack(fill='x', padx=5, pady=2)
            
            # Commodity info
            info_frame = tk.Frame(comm_frame, bg='#2d1b4e')
            info_frame.pack(side='left', fill='x', expand=True, padx=10, pady=10)
            
            # Commodity name and price
            name_label = tk.Label(info_frame, text=commodity_name, 
                                bg='#2d1b4e', fg='#e0e0e0', 
                                font=('Helvetica', 12, 'bold'))
            name_label.pack(anchor='w')
            
            price_text = f"Price: {price} credits"
            if commodity_name in self.current_location.produces:
                price_text += " 📉 (Cheap)"
                price_color = '#4ecdc4'
            elif commodity_name in self.current_location.consumes:
                price_text += " 📈 (Expensive)"
                price_color = '#ff6b6b'
            else:
                price_color = '#b0b0b0'
            
            price_label = tk.Label(info_frame, text=price_text, 
                                 bg='#2d1b4e', fg=price_color, 
                                 font=('Helvetica', 10))
            price_label.pack(anchor='w')
            
            # Show inventory for sell mode
            if mode == 'sell':
                owned = self.player.inventory.get(commodity_name, 0)
                owned_label = tk.Label(info_frame, text=f"You have: {owned}", 
                                     bg='#2d1b4e', fg='#b0b0b0', 
                                     font=('Helvetica', 9))
                owned_label.pack(anchor='w')
            
            # Trade button
            button_frame = tk.Frame(comm_frame, bg='#2d1b4e')
            button_frame.pack(side='right', padx=10, pady=10)
            
            if mode == 'buy':
                max_affordable = self.player.credits // price
                max_space = self.player.get_cargo_space()
                max_buyable = min(max_affordable, max_space)
                
                if max_buyable > 0:
                    buy_btn = tk.Button(button_frame, text=f"Buy (max {max_buyable})",
                                      bg='#00d4ff', fg='white', 
                                      font=('Helvetica', 10, 'bold'),
                                      command=lambda c=commodity_name: self.buy_commodity(c))
                    buy_btn.pack()
                else:
                    disabled_btn = tk.Button(button_frame, text="Can't Buy",
                                           bg='#666', fg='#999', 
                                           font=('Helvetica', 10),
                                           state='disabled')
                    disabled_btn.pack()
            
            else:  # sell mode
                owned = self.player.inventory.get(commodity_name, 0)
                if owned > 0:
                    sell_btn = tk.Button(button_frame, text=f"Sell ({owned})",
                                       bg='#4ecdc4', fg='white', 
                                       font=('Helvetica', 10, 'bold'),
                                       command=lambda c=commodity_name: self.sell_commodity(c))
                    sell_btn.pack()
                else:
                    disabled_btn = tk.Button(button_frame, text="None to Sell",
                                           bg='#666', fg='#999', 
                                           font=('Helvetica', 10),
                                           state='disabled')
                    disabled_btn.pack()
            
            row += 1
    
    def refresh_travel_display(self):
        # Clear existing destinations
        for widget in self.travel_scrollable_frame.winfo_children():
            widget.destroy()
        
        destinations = []
        for loc_name, location in LOCATIONS.items():
            if loc_name != self.current_location.name:
                distance = self.current_location.get_distance_to(location)
                fuel_cost = max(10, int(distance * 5))
                destinations.append((loc_name, location, distance, fuel_cost))
        
        # Sort by distance
        destinations.sort(key=lambda x: x[2])
        
        for loc_name, location, distance, fuel_cost in destinations:
            dest_frame = tk.Frame(self.travel_scrollable_frame, bg='#2d1b4e', relief='ridge', bd=1)
            dest_frame.pack(fill='x', padx=5, pady=5)
            
            # Destination info
            info_frame = tk.Frame(dest_frame, bg='#2d1b4e')
            info_frame.pack(side='left', fill='x', expand=True, padx=15, pady=15)
            
            name_label = tk.Label(info_frame, text=location.name, 
                                bg='#2d1b4e', fg='#00d4ff', 
                                font=('Helvetica', 14, 'bold'))
            name_label.pack(anchor='w')
            
            system_label = tk.Label(info_frame, text=f"System: {location.system}", 
                                  bg='#2d1b4e', fg='#4ecdc4', 
                                  font=('Helvetica', 11))
            system_label.pack(anchor='w')
            
            distance_label = tk.Label(info_frame, text=f"Distance: {distance:.1f} ly", 
                                    bg='#2d1b4e', fg='#b0b0b0', 
                                    font=('Helvetica', 10))
            distance_label.pack(anchor='w')
            
            fuel_label = tk.Label(info_frame, text=f"Fuel Cost: {fuel_cost} credits", 
                                bg='#2d1b4e', fg='#ff6b6b', 
                                font=('Helvetica', 10))
            fuel_label.pack(anchor='w')
            
            # Travel button
            button_frame = tk.Frame(dest_frame, bg='#2d1b4e')
            button_frame.pack(side='right', padx=15, pady=15)
            
            if self.player.credits >= fuel_cost:
                travel_btn = tk.Button(button_frame, text="🚀 Travel Here",
                                     bg='#00d4ff', fg='white', 
                                     font=('Helvetica', 12, 'bold'),
                                     command=lambda dest=loc_name, cost=fuel_cost: self.travel_to(dest, cost))
                travel_btn.pack()
            else:
                disabled_btn = tk.Button(button_frame, text="Not Enough Credits",
                                       bg='#666', fg='#999', 
                                       font=('Helvetica', 10),
                                       state='disabled')
                disabled_btn.pack()
    
    def buy_commodity(self, commodity_name):
        price = self.current_location.market_prices[commodity_name]
        max_affordable = self.player.credits // price
        max_space = self.player.get_cargo_space()
        max_buyable = min(max_affordable, max_space)
        
        if max_buyable <= 0:
            messagebox.showerror("Can't Buy", "Not enough credits or cargo space!")
            return
        
        quantity = simpledialog.askinteger(
            "Buy Commodity",
            f"How many {commodity_name} to buy?\nPrice: {price} credits each\nMax you can buy: {max_buyable}",
            minvalue=1, maxvalue=max_buyable
        )
        
        if quantity:
            total_cost = price * quantity
            if self.player.spend_credits(total_cost):
                if self.player.add_cargo(commodity_name, quantity):
                    messagebox.showinfo("Success!", f"Bought {quantity} {commodity_name} for {total_cost:,} credits!")
                    self.update_display()
                else:
                    self.player.add_credits(total_cost)  # Refund
                    messagebox.showerror("Error", "Cargo hold full!")
            else:
                messagebox.showerror("Error", "Not enough credits!")
    
    def sell_commodity(self, commodity_name):
        owned = self.player.inventory.get(commodity_name, 0)
        if owned <= 0:
            messagebox.showerror("Can't Sell", f"You don't have any {commodity_name}!")
            return
        
        price = self.current_location.market_prices[commodity_name]
        
        quantity = simpledialog.askinteger(
            "Sell Commodity",
            f"How many {commodity_name} to sell?\nPrice: {price} credits each\nYou have: {owned}",
            minvalue=1, maxvalue=owned
        )
        
        if quantity:
            if self.player.remove_cargo(commodity_name, quantity):
                total_earned = price * quantity
                self.player.add_credits(total_earned)
                messagebox.showinfo("Success!", f"Sold {quantity} {commodity_name} for {total_earned:,} credits!")
                self.update_display()
            else:
                messagebox.showerror("Error", "Failed to sell cargo!")
    
    def travel_to(self, destination_name, fuel_cost):
        if not self.player.spend_credits(fuel_cost):
            messagebox.showerror("Can't Travel", "Not enough credits for fuel!")
            return
        
        old_location = self.current_location
        new_location = LOCATIONS[destination_name]
        
        distance = old_location.get_distance_to(new_location)
        travel_time = max(1, int(distance))
        
        self.player.current_location = destination_name
        self.player.days_elapsed += travel_time
        self.current_location = new_location
        
        # Refresh market at new location
        self.current_location.refresh_market()
        
        messagebox.showinfo("Travel Complete!", 
                          f"🚀 Traveled to {destination_name}!\n"
                          f"Travel time: {travel_time} days\n"
                          f"Fuel cost: {fuel_cost:,} credits")
        
        self.update_display()
    
    def update_display(self):
        # Update header info
        self.credits_label.config(text=f"Credits: {self.player.credits:,}")
        self.cargo_label.config(text=f"Cargo: {self.player.get_cargo_count()}/{self.player.max_cargo}")
        self.days_label.config(text=f"Days: {self.player.days_elapsed}")
        
        # Refresh all tabs
        self.clear_screen()
        self.show_main_game()

def main():
    root = tk.Tk()
    
    # Set icon and window properties
    root.iconname("TradeWinds")
    root.minsize(800, 600)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    pos_x = (root.winfo_screenwidth() // 2) - (width // 2)
    pos_y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    app = TradeWindsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()