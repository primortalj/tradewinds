"""
TradeWinds Desktop Text Adventure
A clean Windows desktop text adventure with retro terminal styling
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import io
from contextlib import redirect_stdout
from tradewinds_adventure import TextAdventure

class TradeWindsDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 TradeWinds - Space Trading Adventure")
        self.root.geometry("1100x750")
        self.root.configure(bg='#000000')
        
        # Set minimum window size
        self.root.minsize(800, 600)
        
        # Create the text adventure game instance
        self.game = TextAdventure()
        
        # Game state
        self.game_started = False
        self.command_history = []
        self.history_index = -1
        
        # Create GUI elements
        self.create_widgets()
        
        # Center window on screen
        self.center_window()
        
        # Show startup screen
        self.show_startup_screen()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title bar with game info
        self.create_title_bar(main_frame)
        
        # Create text display area
        self.create_text_area(main_frame)
        
        # Create input area
        self.create_input_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Game menu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Commands", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_title_bar(self, parent):
        title_frame = tk.Frame(parent, bg='#001100', relief=tk.RAISED, bd=2)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(title_frame, 
                              text="🚀 TRADEWINDS SPACE TRADING ADVENTURE 🚀",
                              bg='#001100', fg='#00ff00', 
                              font=('Courier', 14, 'bold'))
        title_label.pack(pady=8)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, 
                                 text="Interactive Text Adventure • Real Star Systems • Dynamic Trading",
                                 bg='#001100', fg='#00ffff', 
                                 font=('Courier', 10))
        subtitle_label.pack(pady=(0, 8))
    
    def create_text_area(self, parent):
        # Frame for text area
        text_frame = tk.Frame(parent, bg='#000000')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrolled text widget
        self.text_display = scrolledtext.ScrolledText(
            text_frame,
            bg='#000000',
            fg='#00ff00',
            insertbackground='#00ff00',
            selectbackground='#003300',
            selectforeground='#00ff00',
            font=('Consolas', 11),
            wrap=tk.WORD,
            state=tk.NORMAL,
            cursor='arrow',
            relief=tk.SUNKEN,
            bd=2
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for formatting
        self.setup_text_tags()
        
        # Configure scrollbar
        scrollbar = self.text_display.vbar
        scrollbar.configure(bg='#003300', troughcolor='#001100', 
                           activebackground='#00ff00')
    
    def setup_text_tags(self):
        """Configure text formatting tags"""
        self.text_display.tag_configure('title', 
                                       foreground='#00ffff', 
                                       font=('Consolas', 12, 'bold'))
        self.text_display.tag_configure('location', 
                                       foreground='#ffff00', 
                                       font=('Consolas', 11, 'bold'))
        self.text_display.tag_configure('description', 
                                       foreground='#00ff00')
        self.text_display.tag_configure('atmosphere', 
                                       foreground='#888888', 
                                       font=('Consolas', 10, 'italic'))
        self.text_display.tag_configure('prompt', 
                                       foreground='#00ffff', 
                                       font=('Consolas', 11, 'bold'))
        self.text_display.tag_configure('input', 
                                       foreground='#ffffff', 
                                       font=('Consolas', 11, 'bold'))
        self.text_display.tag_configure('error', 
                                       foreground='#ff4444')
        self.text_display.tag_configure('success', 
                                       foreground='#44ff44')
        self.text_display.tag_configure('warning', 
                                       foreground='#ffaa00')
        self.text_display.tag_configure('separator', 
                                       foreground='#00ffff')
    
    def create_input_area(self, parent):
        # Input frame
        input_frame = tk.Frame(parent, bg='#001100', relief=tk.RAISED, bd=2)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Prompt label
        prompt_label = tk.Label(input_frame, text="Command:", 
                               bg='#001100', fg='#00ffff', 
                               font=('Consolas', 11, 'bold'))
        prompt_label.pack(side=tk.LEFT, padx=(10, 5), pady=8)
        
        # Input entry
        self.input_entry = tk.Entry(input_frame,
                                   bg='#000000', fg='#ffffff',
                                   insertbackground='#00ff00',
                                   font=('Consolas', 11),
                                   relief=tk.SUNKEN,
                                   bd=2)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, 
                             padx=(0, 10), pady=8)
        self.input_entry.bind('<Return>', self.process_command)
        self.input_entry.bind('<Up>', self.history_up)
        self.input_entry.bind('<Down>', self.history_down)
        
        # Send button
        send_button = tk.Button(input_frame, text="Send",
                               bg='#003300', fg='#00ff00',
                               font=('Consolas', 10, 'bold'),
                               relief=tk.RAISED,
                               bd=2,
                               command=self.process_command,
                               cursor='hand2')
        send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=8)
    
    def create_status_bar(self, parent):
        # Status frame
        status_frame = tk.Frame(parent, bg='#001100', relief=tk.SUNKEN, bd=2)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = tk.Label(status_frame, 
                                    text="Ready to begin your space trading adventure...",
                                    bg='#001100', fg='#888888',
                                    font=('Consolas', 9),
                                    anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=3)
    
    def show_startup_screen(self):
        """Display the game startup screen"""
        self.append_text("=" * 80, 'separator')
        self.append_text("🚀 TRADEWINDS: A SPACE TRADING ADVENTURE 🚀", 'title')
        self.append_text("=" * 80, 'separator')
        self.append_text("")
        self.append_text("Welcome to the galaxy, Captain!")
        self.append_text("In this text adventure, you'll navigate between real star")
        self.append_text("systems, trading commodities and building your fortune.")
        self.append_text("")
        self.append_text("Ready to begin? Click 'New Game' from the Game menu or")
        self.append_text("type 'start' to begin your adventure.", 'prompt')
        self.append_text("")
        self.append_text("Type 'help' at any time for available commands.", 'prompt')
        
        # Focus on input
        self.input_entry.focus()
    
    def new_game(self):
        """Start a new game"""
        if self.game_started:
            result = messagebox.askyesno("New Game", 
                                       "Start a new game? Current progress will be lost.")
            if not result:
                return
        
        self.start_new_game()
    
    def start_new_game(self):
        """Initialize and start a new game"""
        # Clear display
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        
        # Get player info
        player_name = self.get_player_name()
        ship_name = self.get_ship_name()
        
        # Initialize game
        self.game = TextAdventure()
        self.game.state.player_name = player_name
        self.game.state.ship_name = ship_name
        self.game_started = True
        
        # Display welcome
        self.append_text("=" * 80, 'separator')
        self.append_text("🚀 NEW GAME STARTED 🚀", 'title')
        self.append_text("=" * 80, 'separator')
        self.append_text("")
        self.append_text(f"Welcome aboard, Captain {player_name}!", 'success')
        self.append_text(f"You command the starship '{ship_name}'.", 'success')
        self.append_text("")
        
        # Start the game
        self.execute_game_start()
        
        # Update status
        self.update_status()
        
        # Focus input
        self.input_entry.focus()
    
    def get_player_name(self):
        """Get player name from user"""
        from tkinter import simpledialog
        name = simpledialog.askstring(
            "Captain Name",
            "Enter your captain's name:",
            initialvalue="Captain"
        )
        return name.strip() if name else "Captain"
    
    def get_ship_name(self):
        """Get ship name from user"""
        from tkinter import simpledialog
        name = simpledialog.askstring(
            "Ship Name", 
            "Enter your ship's name:",
            initialvalue="Starwind"
        )
        return name.strip() if name else "Starwind"
    
    def execute_game_start(self):
        """Execute the game startup sequence"""
        # Capture game output
        output_buffer = io.StringIO()
        
        with redirect_stdout(output_buffer):
            self.game.print_intro()
            self.game.look_around()
        
        # Display the output
        output = output_buffer.getvalue()
        self.display_game_output(output)
    
    def process_command(self, event=None):
        """Process user input"""
        if not self.game_started:
            command = self.input_entry.get().strip().lower()
            if command in ['start', 'new', 'begin']:
                self.start_new_game()
                self.input_entry.delete(0, tk.END)
                return
            elif command == 'help':
                self.show_help()
                self.input_entry.delete(0, tk.END)
                return
        
        command = self.input_entry.get().strip()
        if not command:
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Display the command
        player_name = self.game.state.player_name if self.game_started else "Player"
        self.append_text(f"\n{player_name}> {command}", 'input')
        self.input_entry.delete(0, tk.END)
        
        if not self.game_started:
            self.append_text("Please start a new game first (Game menu → New Game)", 'error')
            return
        
        # Execute the command
        self.execute_game_command(command)
        
        # Update status
        self.update_status()
        
        # Scroll to bottom
        self.text_display.see(tk.END)
    
    def execute_game_command(self, command):
        """Execute a game command and capture output"""
        try:
            # Capture printed output
            output_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer):
                # Add to game history
                self.game.command_history.append(command)
                
                # Parse and execute command
                self.game.parse_command(command)
            
            # Get the output
            output = output_buffer.getvalue()
            
            # Display the output
            if output.strip():
                self.display_game_output(output)
            
        except Exception as e:
            self.append_text(f"\nError: {e}", 'error')
    
    def display_game_output(self, output):
        """Display game output with appropriate formatting"""
        lines = output.split('\n')
        
        for line in lines:
            if not line.strip():
                self.append_text('')
                continue
            
            # Format different types of lines
            if line.startswith('**') and line.endswith('**'):
                # Location titles
                self.append_text(line, 'location')
            elif line.startswith('*') and line.endswith('*'):
                # Atmospheric descriptions
                self.append_text(line, 'atmosphere')
            elif line.startswith('='):
                # Title bars
                self.append_text(line, 'separator')
            elif '✅' in line or 'Success' in line or 'Purchased' in line or 'Sold' in line:
                # Success messages
                self.append_text(line, 'success')
            elif '⚠️' in line or 'Warning' in line or 'expensive' in line.lower():
                # Warning messages
                self.append_text(line, 'warning')
            elif '❌' in line or 'Error' in line or "don't" in line or "can't" in line:
                # Error messages
                self.append_text(line, 'error')
            elif line.startswith('🚀') or 'TRAVELING' in line:
                # Travel messages
                self.append_text(line, 'title')
            else:
                # Regular text
                self.append_text(line, 'description')
    
    def append_text(self, text, tag=None):
        """Append text to the display with optional formatting"""
        self.text_display.config(state=tk.NORMAL)
        if tag:
            self.text_display.insert(tk.END, text + '\n', tag)
        else:
            self.text_display.insert(tk.END, text + '\n')
        self.text_display.config(state=tk.DISABLED)
        self.text_display.see(tk.END)
    
    def update_status(self):
        """Update the status bar"""
        if not self.game_started:
            return
            
        loc_name = self.game.current_location_obj.name
        credits = self.game.state.talents
        cargo = self.game.get_cargo_count()
        days = self.game.state.days_elapsed
        
        # Add business info if applicable
        business_info = ""
        if hasattr(self.game, 'business_registered') and self.game.business_registered:
            factories = len(self.game.factories)
            reputation = self.game.business_reputation
            business_info = f" | Business: Rep {reputation} | Factories: {factories}"
        
        status_text = f"Location: {loc_name} | Talents: ╬{credits:,} | Cargo: {cargo}/50 | Days: {days}{business_info}"
        self.status_label.config(text=status_text)
    
    def history_up(self, event):
        """Navigate up in command history"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
    
    def history_down(self, event):
        """Navigate down in command history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
        elif self.history_index >= len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.input_entry.delete(0, tk.END)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """TRADEWINDS COMMANDS:

BASIC COMMANDS:
  look                 - Look around current location
  travel <destination> - Travel to another location
  market               - Show market prices
  buy <commodity>      - Purchase goods
  sell <commodity>     - Sell goods
  status               - Show talents, cargo, and stats
  inventory            - List your cargo
  
BUSINESS OPERATIONS:
  business             - Show business options
  incorporate          - Register your business (╬5,000)
  license              - Get business licenses
  loan                 - Apply for business loans
  reputation           - Check business reputation
  
FACTORY AUTOMATION:
  factory              - Show factory options
  build factory        - Construct automated facility
  factories            - List your factories
  automate <commodity> - Build production facility
  
EXAMPLES:
  • go to mars colony
  • buy some electronics
  • incorporate my business
  • build a factory here
  • automate food production

ADVANCED:
  • Type 'commands' for full command list
  • Use UP/DOWN arrows to navigate command history
  • Business features unlock after incorporation"""
        
        messagebox.showinfo("TradeWinds Commands", help_text)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """🚀 TradeWinds - Space Trading Adventure

A classic text adventure where you explore real star systems,
trade commodities, and build your space trading empire.

Features:
• 12 Real Star Systems with authentic details
• Rich narrative descriptions
• Natural language parser
• Dynamic trading markets
• Business incorporation system
• Automated factory construction
• Classic interactive fiction gameplay
• Full business management

Currency: Talents ╬
Starting Capital: ╬1,000
Goal: Build your galactic trading empire

Version: 0.1a
Developer: Ciderboy Games
Created with Python and Tkinter"""
        
        messagebox.showinfo("About TradeWinds", about_text)

def main():
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')  # Add an icon file if you have one
    except:
        pass
    
    app = TradeWindsDesktop(root)
    root.mainloop()

if __name__ == "__main__":
    main()