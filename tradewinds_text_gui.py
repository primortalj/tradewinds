"""
TradeWinds Text Adventure GUI
Classic text adventure interface with scrolling text and command input
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, font
import sys
import io
from contextlib import redirect_stdout
from tradewinds_adventure import TextAdventure

class TextAdventureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 TradeWinds - Text Adventure")
        self.root.geometry("1000x700")
        self.root.configure(bg='#000000')
        
        # Create the text adventure game instance
        self.game = TextAdventure()
        
        # Override the game's input/output methods
        self.setup_io_redirection()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start the game
        self.start_game()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="🚀 TRADEWINDS: A SPACE TRADING ADVENTURE 🚀",
                              bg='#000000', fg='#00ff00', 
                              font=('Courier', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Create text display area
        self.create_text_area(main_frame)
        
        # Create input area
        self.create_input_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
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
            selectbackground='#333333',
            selectforeground='#00ff00',
            font=('Courier', 11),
            wrap=tk.WORD,
            state=tk.NORMAL,
            cursor='arrow'
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different colors
        self.text_display.tag_configure('title', foreground='#00ffff', font=('Courier', 12, 'bold'))
        self.text_display.tag_configure('location', foreground='#ffff00', font=('Courier', 11, 'bold'))
        self.text_display.tag_configure('description', foreground='#00ff00')
        self.text_display.tag_configure('atmosphere', foreground='#888888', font=('Courier', 10, 'italic'))
        self.text_display.tag_configure('prompt', foreground='#00ffff', font=('Courier', 11, 'bold'))
        self.text_display.tag_configure('input', foreground='#ffffff', font=('Courier', 11, 'bold'))
        self.text_display.tag_configure('error', foreground='#ff4444')
        self.text_display.tag_configure('success', foreground='#44ff44')
        self.text_display.tag_configure('warning', foreground='#ffaa00')
    
    def create_input_area(self, parent):
        # Input frame
        input_frame = tk.Frame(parent, bg='#000000')
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Prompt label
        prompt_label = tk.Label(input_frame, text="Command:", 
                               bg='#000000', fg='#00ffff', 
                               font=('Courier', 11, 'bold'))
        prompt_label.pack(side=tk.LEFT)
        
        # Input entry
        self.input_entry = tk.Entry(input_frame,
                                   bg='#111111', fg='#ffffff',
                                   insertbackground='#00ff00',
                                   font=('Courier', 11),
                                   relief=tk.FLAT,
                                   bd=2)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        self.input_entry.bind('<Return>', self.process_command)
        self.input_entry.focus()
        
        # Send button
        send_button = tk.Button(input_frame, text="Send",
                               bg='#333333', fg='#00ff00',
                               font=('Courier', 10, 'bold'),
                               relief=tk.FLAT,
                               bd=1,
                               command=self.process_command)
        send_button.pack(side=tk.RIGHT)
    
    def create_status_bar(self, parent):
        # Status frame
        status_frame = tk.Frame(parent, bg='#111111', relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = tk.Label(status_frame, 
                                    text="Ready to begin adventure...",
                                    bg='#111111', fg='#888888',
                                    font=('Courier', 9),
                                    anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    def setup_io_redirection(self):
        # Create string buffers
        self.output_buffer = io.StringIO()
        
        # Override game methods
        self.game.get_input = self.get_game_input
        self.original_print = print
        
        # Input queue for the game
        self.input_queue = []
        self.waiting_for_input = False
    
    def get_game_input(self) -> str:
        """Custom input method for the game"""
        self.waiting_for_input = True
        self.root.wait_variable(self.input_received)
        self.waiting_for_input = False
        
        if self.input_queue:
            return self.input_queue.pop(0)
        return ""
    
    def process_command(self, event=None):
        """Process user input"""
        command = self.input_entry.get().strip()
        if not command:
            return
        
        # Display the command in the text area
        self.append_text(f"\n{self.game.state.player_name}> {command}", 'input')
        self.input_entry.delete(0, tk.END)
        
        # Add command to queue and notify game
        self.input_queue.append(command)
        if hasattr(self, 'input_received'):
            self.input_received.set(True)
        else:
            # If game isn't waiting for input yet, process immediately
            self.execute_game_command(command)
        
        # Scroll to bottom
        self.text_display.see(tk.END)
    
    def execute_game_command(self, command):
        """Execute a game command and capture output"""
        try:
            # Capture printed output
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            # Execute the command
            if command.strip():
                self.game.command_history.append(command)
                self.game.parse_command(command)
            
            # Get the output
            output = captured_output.getvalue()
            sys.stdout = old_stdout
            
            # Display the output
            if output.strip():
                self.display_formatted_output(output)
            
            # Update status
            self.update_status()
            
        except Exception as e:
            sys.stdout = old_stdout
            self.append_text(f"\nError: {e}", 'error')
    
    def display_formatted_output(self, output):
        """Display game output with appropriate formatting"""
        lines = output.split('\n')
        
        for line in lines:
            if not line.strip():
                self.append_text('\n')
                continue
            
            # Format different types of lines
            if line.startswith('**') and line.endswith('**'):
                # Location titles
                self.append_text(f"\n{line}\n", 'location')
            elif line.startswith('*') and line.endswith('*'):
                # Atmospheric descriptions
                self.append_text(f"{line}\n", 'atmosphere')
            elif line.startswith('='):
                # Title bars
                self.append_text(f"{line}\n", 'title')
            elif '✅' in line or 'Success' in line or 'Purchased' in line or 'Sold' in line:
                # Success messages
                self.append_text(f"{line}\n", 'success')
            elif '⚠️' in line or 'Warning' in line or 'expensive' in line.lower():
                # Warning messages
                self.append_text(f"{line}\n", 'warning')
            elif '❌' in line or 'Error' in line or "don't" in line or "can't" in line:
                # Error messages
                self.append_text(f"{line}\n", 'error')
            elif line.startswith('🚀') or 'TRAVELING' in line:
                # Travel messages
                self.append_text(f"{line}\n", 'title')
            else:
                # Regular text
                self.append_text(f"{line}\n", 'description')
    
    def append_text(self, text, tag=None):
        """Append text to the display with optional formatting"""
        self.text_display.config(state=tk.NORMAL)
        if tag:
            self.text_display.insert(tk.END, text, tag)
        else:
            self.text_display.insert(tk.END, text)
        self.text_display.config(state=tk.DISABLED)
        self.text_display.see(tk.END)
    
    def update_status(self):
        """Update the status bar"""
        loc_name = self.game.current_location_obj.name
        credits = self.game.state.credits
        cargo = self.game.get_cargo_count()
        days = self.game.state.days_elapsed
        
        status_text = f"Location: {loc_name} | Credits: {credits:,} | Cargo: {cargo}/50 | Days: {days}"
        self.status_label.config(text=status_text)
    
    def start_game(self):
        """Start the text adventure game"""
        # Initialize the input received variable
        self.input_received = tk.BooleanVar()
        
        # Capture the game startup
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            # Run the game initialization
            self.game.print_title()
            
            # Get the startup output
            output = captured_output.getvalue()
            sys.stdout = old_stdout
            
            # Display initial output
            self.display_formatted_output(output)
            
            # Get player info through GUI
            self.get_player_info_gui()
            
        except Exception as e:
            sys.stdout = old_stdout
            self.append_text(f"Error starting game: {e}", 'error')
    
    def get_player_info_gui(self):
        """Get player information through dialog boxes"""
        from tkinter import simpledialog
        
        # Get captain name
        captain_name = simpledialog.askstring(
            "Captain Name",
            "Enter your captain's name:",
            initialvalue="Captain"
        )
        if captain_name:
            self.game.state.player_name = captain_name.strip()
        
        # Get ship name
        ship_name = simpledialog.askstring(
            "Ship Name", 
            "Enter your ship's name:",
            initialvalue="Starwind"
        )
        if ship_name:
            self.game.state.ship_name = ship_name.strip()
        
        # Display welcome message
        self.append_text(f"\nWelcome aboard, {self.game.state.player_name}!", 'success')
        self.append_text(f"You command the starship '{self.game.state.ship_name}'.\n", 'success')
        
        # Continue with game initialization
        self.continue_game_start()
    
    def continue_game_start(self):
        """Continue the game startup after getting player info"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            # Run the intro and first look
            self.game.print_intro()
            self.game.look_around()
            
            # Get the output
            output = captured_output.getvalue()
            sys.stdout = old_stdout
            
            # Display the output
            self.display_formatted_output(output)
            
            # Update status
            self.update_status()
            
            # Set up command processing loop
            self.setup_command_loop()
            
        except Exception as e:
            sys.stdout = old_stdout
            self.append_text(f"Error: {e}", 'error')
    
    def setup_command_loop(self):
        """Set up the main command processing loop"""
        # Override the game's main loop since we handle input differently
        self.game.running = True
        
        # Focus on input
        self.input_entry.focus()
        
        # Ready to accept commands
        self.append_text("\nReady for commands! Type 'help' if you need assistance.\n", 'prompt')

def main():
    root = tk.Tk()
    
    # Set window icon and properties
    root.iconname("TradeWinds")
    root.minsize(800, 600)
    
    # Center window on screen
    root.update_idletasks()
    width = 1000
    height = 700
    pos_x = (root.winfo_screenwidth() // 2) - (width // 2)
    pos_y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    app = TextAdventureGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()