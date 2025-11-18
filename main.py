"""
Minesweeper Game with Analytics
Main Menu and Program Entry Point
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import re

# Import our modules
try:
    from game import MinesweeperGame
    from analytics import AnalyticsGenerator
    from highscores import HighscoreManager
except ImportError:
    print("Error: Make sure all required files are in the same directory:")
    print("- game.py")
    print("- analytics.py")
    print("- highscores.py")
    print("- board_generator.py")
    sys.exit(1)


class MainMenu:
    """Main menu for the Minesweeper application"""
    
    # Modern color scheme
    COLORS = {
        'bg': '#1a1a2e',
        'secondary_bg': '#16213e',
        'accent': '#0f3460',
        'primary': '#e94560',
        'success': '#00d4aa',
        'text': '#eaeaea',
        'text_secondary': '#a0a0a0',
        'button_easy': '#2d6a4f',
        'button_intermediate': '#d68910',
        'button_expert': '#c0392b',
        'button_custom': '#7d3c98',
        'button_secondary': '#2c3e50',
        'button_hover': '#f6e58d'
    }
    
    # Standard game configurations
    CONFIGURATIONS = {
        'Easy': {'rows': 9, 'cols': 9, 'mines': 10},
        'Intermediate': {'rows': 16, 'cols': 16, 'mines': 40},
        'Expert': {'rows': 16, 'cols': 30, 'mines': 99}
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper - Main Menu")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS['bg'])
        
        # Setup ttk styles for colored buttons (macOS fix)
        self.button_style = ttk.Style(self.root)
        self.setup_styles()
        
        self.center_window()
        self.highscore_manager = HighscoreManager()
        self.create_widgets()
    
    def setup_styles(self):
        """Setup ttk button styles for colored buttons on macOS"""
        # Use clam theme - works best for custom colors
        self.button_style.theme_use('clam')
        
        # Main difficulty buttons
        self.button_style.configure('Easy.TButton', 
            font=('Helvetica', 12, 'bold'), 
            foreground='white', 
            background=self.COLORS['button_easy'], 
            borderwidth=0, 
            relief='flat', 
            padding=15
        )
        self.button_style.configure('Intermediate.TButton', 
            font=('Helvetica', 12, 'bold'), 
            foreground='white', 
            background=self.COLORS['button_intermediate'], 
            borderwidth=0, 
            relief='flat', 
            padding=15
        )
        self.button_style.configure('Expert.TButton', 
            font=('Helvetica', 12, 'bold'), 
            foreground='white', 
            background=self.COLORS['button_expert'], 
            borderwidth=0, 
            relief='flat', 
            padding=15
        )
        
        # Secondary buttons
        self.button_style.configure('Custom.TButton', 
            font=('Helvetica', 10, 'bold'), 
            foreground='white', 
            background=self.COLORS['button_custom'], 
            relief='flat', 
            padding=10
        )
        self.button_style.configure('Highscore.TButton', 
            font=('Helvetica', 10, 'bold'), 
            foreground='white', 
            background=self.COLORS['accent'], 
            relief='flat', 
            padding=10
        )
        self.button_style.configure('Analytics.TButton', 
            font=('Helvetica', 10, 'bold'), 
            foreground='white', 
            background=self.COLORS['button_secondary'], 
            relief='flat', 
            padding=10
        )
        self.button_style.configure('Exit.TButton', 
            font=('Helvetica', 10, 'bold'), 
            foreground='white', 
            background='#c0392b', 
            relief='flat', 
            padding=10
        )
        
        # Dialog button style
        self.button_style.configure('DialogButton.TButton',
            font=('Helvetica', 11, 'bold'),
            foreground='white',
            background=self.COLORS['success'],
            relief='flat',
            padding=10
        )
        
        # Hover effects for all buttons
        for style_name, color in [
            ('Easy', self.COLORS['button_easy']),
            ('Intermediate', self.COLORS['button_intermediate']),
            ('Expert', self.COLORS['button_expert']),
            ('Custom', self.COLORS['button_custom']),
            ('Highscore', self.COLORS['accent']),
            ('Analytics', self.COLORS['button_secondary']),
            ('Exit', '#c0392b'),
            ('DialogButton', self.COLORS['success'])
        ]:
            self.button_style.map(
                f'{style_name}.TButton',
                background=[('active', self.COLORS['button_hover']), ('!active', color)],
                foreground=[('active', self.COLORS['bg']), ('!active', 'white')]
            )
        
        # Highscore combobox style
        self.button_style.configure('Highscore.TCombobox',
            fieldbackground='#34495e',
            background='#2c3e50',
            foreground='white',
            arrowcolor='white',
            bordercolor='#3498db',
            selectbackground='#3498db',
            selectforeground='white',
            font=('Helvetica', 10)
        )
        self.button_style.map('Highscore.TCombobox',
            fieldbackground=[('readonly', '#34495e')],
            selectbackground=[('readonly', '#34495e')],
            selectforeground=[('readonly', 'white')],
            foreground=[('readonly', 'white')]
        )
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create the main menu widgets"""
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        title_frame = tk.Frame(main_frame, bg=self.COLORS['bg'])
        title_frame.pack(pady=(0, 10))
        
        title = tk.Label(
            title_frame,
            text="💣 MINESWEEPER",
            font=("Helvetica", 36, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Select Your Challenge",
            font=("Helvetica", 14),
            fg=self.COLORS['text_secondary'],
            bg=self.COLORS['bg']
        )
        subtitle.pack(pady=(5, 0))
        
        difficulty_frame = tk.Frame(main_frame, bg=self.COLORS['bg'])
        difficulty_frame.pack(pady=20, fill='x')
        difficulty_frame.columnconfigure(0, weight=1)
        
        # Difficulty buttons using ttk.Button with styles
        ttk.Button(
            difficulty_frame,
            text="🟢 EASY\n9×9 | 10 mines",
            command=lambda: self.start_game('Easy'),
            style='Easy.TButton'
        ).grid(row=0, column=0, padx=10, pady=8, sticky='ew')
        
        ttk.Button(
            difficulty_frame,
            text="🟡 INTERMEDIATE\n16×16 | 40 mines",
            command=lambda: self.start_game('Intermediate'),
            style='Intermediate.TButton'
        ).grid(row=1, column=0, padx=10, pady=8, sticky='ew')
        
        ttk.Button(
            difficulty_frame,
            text="🔴 EXPERT\n16×30 | 99 mines",
            command=lambda: self.start_game('Expert'),
            style='Expert.TButton'
        ).grid(row=2, column=0, padx=10, pady=8, sticky='ew')
        
        separator = tk.Frame(main_frame, height=2, bg=self.COLORS['accent'])
        separator.pack(fill='x', pady=20)
        
        # Additional options frame
        options_frame = tk.Frame(main_frame, bg=self.COLORS['bg'])
        options_frame.pack(fill='x')
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
        ttk.Button(
            options_frame,
            text="⚙️ Custom",
            command=self.custom_game,
            style='Custom.TButton'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        ttk.Button(
            options_frame,
            text="🏆 Highscores",
            command=self.view_highscores,
            style='Highscore.TButton'
        ).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Button(
            options_frame,
            text="📊 Analytics",
            command=self.generate_analytics,
            style='Analytics.TButton'
        ).grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        
        ttk.Button(
            options_frame,
            text="❌ Exit",
            command=self.root.quit,
            style='Exit.TButton'
        ).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    def start_game(self, config_name):
        """Start a game with the selected configuration"""
        config = self.CONFIGURATIONS[config_name]
        self.root.withdraw()
        
        game = MinesweeperGame(
            rows=config['rows'],
            cols=config['cols'],
            mines=config['mines'],
            difficulty=config_name,
            highscore_manager=self.highscore_manager,
            on_close=self.show_menu
        )
           
    def custom_game(self):
        """Open dialog for custom game configuration"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Configuration")
        dialog.geometry("350x280")
        dialog.resizable(False, False)
        dialog.configure(bg=self.COLORS['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (175)
        y = (dialog.winfo_screenheight() // 2) - (140)
        dialog.geometry(f'350x280+{x}+{y}')
        
        tk.Label(
            dialog,
            text="⚙️ Custom Configuration",
            font=("Helvetica", 14, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['primary']
        ).pack(pady=15)
        
        input_frame = tk.Frame(dialog, bg=self.COLORS['bg'])
        input_frame.pack(pady=10)
        
        labels = ["Rows:", "Columns:", "Mines:"]
        default_values = ["10", "10", "15"]
        entries = []
        
        for i, (label, default) in enumerate(zip(labels, default_values)):
            tk.Label(
                input_frame,
                text=label,
                font=("Helvetica", 11),
                bg=self.COLORS['bg'],
                fg=self.COLORS['text']
            ).grid(row=i, column=0, sticky='e', padx=10, pady=8)
            
            var = tk.StringVar(value=default)
            entry = tk.Entry(
                input_frame,
                textvariable=var,
                width=12,
                font=("Helvetica", 11),
                bg=self.COLORS['secondary_bg'],
                fg=self.COLORS['text'],
                insertbackground=self.COLORS['text'],
                relief='flat',
                bd=2
            )
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries.append(var)
        
        def start_custom():
            try:
                rows = int(entries[0].get())
                cols = int(entries[1].get())
                mines = int(entries[2].get())
                
                # Basic range validation
                if rows < 5 or rows > 30:
                    messagebox.showerror("Invalid Input", "Rows must be between 5 and 30")
                    return
                if cols < 5 or cols > 50:
                    messagebox.showerror("Invalid Input", "Columns must be between 5 and 50")
                    return
                
                # Calculate total cells
                total_cells = rows * cols
                
                # Maximum mines (leave safe starting area)
                max_mines = total_cells - 10
                
                # Minimum mines validation
                if mines < 1:
                    messagebox.showerror(
                        "Invalid Input", 
                        "You must have at least 1 mine!"
                    )
                    return
                
                # Maximum mines validation (can't fill entire board)
                if mines >= total_cells:
                    messagebox.showerror(
                        "Invalid Input", 
                        f"Too many mines!\n\n"
                        f"Board has {total_cells} cells.\n"
                        f"You entered {mines} mines.\n\n"
                        f"Mines must be less than total cells.\n"
                        f"Maximum: {total_cells - 1}"
                    )
                    return
                
                # Reasonable maximum validation
                if mines > max_mines:
                    messagebox.showerror(
                        "Invalid Input", 
                        f"Too many mines for this board size!\n\n"
                        f"Board: {rows}×{cols} ({total_cells} cells)\n"
                        f"Mines: {mines}\n"
                        f"Recommended maximum: {max_mines}\n\n"
                        f"Tip: Mines should be 10-20% of total cells\n"
                        f"for a balanced game."
                    )
                    return
                
                # ✨ NEW FIX: Prevent instant-win on small boards
                if total_cells < 36:  # Smaller than 6×6
                    max_safe_mines = int(total_cells * 0.15)  # Max 15% mines for small boards
                    if mines > max_safe_mines:
                        messagebox.showerror(
                            "Board Too Small",
                            f"⚠️ Configuration may cause instant wins!\n\n"
                            f"For a {rows}×{cols} board ({total_cells} cells):\n"
                            f"• Recommended max: {max_safe_mines} mines (15%)\n"
                            f"• You entered: {mines} mines ({int(mines/total_cells*100)}%)\n\n"
                            f"Small boards need fewer mines to prevent instant wins.\n"
                            f"Use a larger board or reduce mines to {max_safe_mines}."
                        )
                        return
                
                # Warning for very high mine density
                mine_percentage = (mines / total_cells) * 100
                if mine_percentage > 60:
                    response = messagebox.askyesno(
                        "High Mine Density Warning",
                        f"Your board has {mine_percentage:.1f}% mines!\n\n"
                        f"This will make the game extremely difficult.\n"
                        f"Recommended: 10-25% mine density.\n\n"
                        f"Continue anyway?",
                        icon='warning'
                    )
                    if not response:
                        return
                    
                dialog.destroy()
                self.root.withdraw()
                
                game = MinesweeperGame(
                    rows=rows,
                    cols=cols,
                    mines=mines,
                    difficulty="Custom",
                    highscore_manager=self.highscore_manager,
                    on_close=self.show_menu
                )
                
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers")
        
        # FIXED: Using ttk.Button with style
        ttk.Button(
            dialog,
            text="🚀 Start Game",
            command=start_custom,
            style='DialogButton.TButton'
        ).pack(pady=15)

    def view_highscores(self):
        """Show highscores window"""
        hs_window = tk.Toplevel(self.root)
        hs_window.title("🏆 Highscores")
        hs_window.geometry("650x550")
        hs_window.resizable(False, False)
        hs_window.configure(bg=self.COLORS['bg'])
        hs_window.transient(self.root)
        
        tk.Label(
            hs_window,
            text="🏆 HIGHSCORES",
            font=("Helvetica", 18, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['primary']
        ).pack(pady=15)
        
        config_frame = tk.Frame(hs_window, bg=self.COLORS['bg'])
        config_frame.pack(pady=10)
        
        tk.Label(
            config_frame,
            text="Configuration:",
            font=("Helvetica", 11),
            bg=self.COLORS['bg'],
            fg=self.COLORS['text']
        ).pack(side='left', padx=10)
        
        available_configs = self.get_available_configurations()
        config_var = tk.StringVar(value=available_configs[0] if available_configs else 'Easy')
        
        config_dropdown = ttk.Combobox(
            config_frame,
            textvariable=config_var,
            values=available_configs,
            state='readonly',
            width=25,
            style='Highscore.TCombobox'
        )
        config_dropdown.pack(side='left', padx=10)
        
        text_frame = tk.Frame(hs_window, bg=self.COLORS['bg'])
        text_frame.pack(pady=15, padx=30, fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, bg=self.COLORS['accent'])
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(
            text_frame,
            width=60,
            height=18,
            yscrollcommand=scrollbar.set,
            bg=self.COLORS['secondary_bg'],
            fg=self.COLORS['text'],
            font=("Courier", 10),
            relief='flat',
            bd=0,
            padx=15,
            pady=15
        )
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)
        
        def update_display():
            config_name = config_var.get()
            
            if config_name in self.CONFIGURATIONS:
                config = self.CONFIGURATIONS[config_name]
                key = f"{config['rows']}x{config['cols']}x{config['mines']}"
            else:
                key = self.parse_config_name(config_name)
            
            scores = self.highscore_manager.get_highscores(key)
            
            text_widget.config(state='normal')
            text_widget.delete('1.0', 'end')
            
            text_widget.insert('end', f"  {config_name}\n", 'title')
            text_widget.insert('end', "  " + "="*58 + "\n\n", 'separator')
            
            if scores:
                text_widget.insert('end', f"  {'Rank':<8}{'Player':<28}{'Time':<15}\n", 'header')
                text_widget.insert('end', "  " + "-"*58 + "\n", 'separator')
                for i, score in enumerate(scores, 1):
                    rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f" {i}."
                    text_widget.insert('end', f"  {rank_emoji:<8}{score['name']:<28}{score['time']:<15}\n")
            else:
                text_widget.insert('end', "\n  No highscores yet for this configuration.\n", 'empty')
            
            text_widget.tag_config('title', font=('Helvetica', 12, 'bold'), foreground=self.COLORS['success'])
            text_widget.tag_config('header', font=('Courier', 10, 'bold'), foreground=self.COLORS['primary'])
            text_widget.tag_config('separator', foreground=self.COLORS['accent'])
            text_widget.tag_config('empty', font=('Helvetica', 11, 'italic'), foreground=self.COLORS['text_secondary'])
            
            text_widget.config(state='disabled')
        
        config_dropdown.bind('<<ComboboxSelected>>', lambda e: update_display())
        update_display()
        
        # FIXED: Using ttk.Button with style
        ttk.Button(
            hs_window,
            text="Close",
            command=hs_window.destroy,
            style='Exit.TButton'
        ).pack(pady=15)

    def get_available_configurations(self):
        """Get all configurations that have highscores"""
        configs = []
        for name in ['Easy', 'Intermediate', 'Expert']:
            configs.append(name)
        
        all_scores = self.highscore_manager.highscores
        for key in all_scores.keys():
            try:
                parts = key.split('x')
                if len(parts) == 3:
                    rows, cols, mines = int(parts[0]), int(parts[1]), int(parts[2])
                    is_standard = False
                    for standard_config in self.CONFIGURATIONS.values():
                        if (standard_config['rows'] == rows and 
                            standard_config['cols'] == cols and 
                            standard_config['mines'] == mines):
                            is_standard = True
                            break
                    
                    if not is_standard:
                        config_name = f"Custom ({rows}×{cols}, {mines} mines)"
                        if config_name not in configs:
                            configs.append(config_name)
            except:
                pass
        return configs

    def parse_config_name(self, config_name):
        """Parse a config name back to a key"""
        try:
            numbers = re.findall(r'\d+', config_name)
            if len(numbers) >= 3:
                return f"{numbers[0]}x{numbers[1]}x{numbers[2]}"
        except:
            pass
        return ""

    def generate_analytics(self):
        """Open analytics generation dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Generate Analytics")
        dialog.geometry("380x320")
        dialog.resizable(False, False)
        dialog.configure(bg=self.COLORS['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (190)
        y = (dialog.winfo_screenheight() // 2) - (160)
        dialog.geometry(f'380x320+{x}+{y}')
        
        tk.Label(
            dialog,
            text="📊 Analytics Configuration",
            font=("Helvetica", 14, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['primary']
        ).pack(pady=15)
        
        input_frame = tk.Frame(dialog, bg=self.COLORS['bg'])
        input_frame.pack(pady=10)
        
        labels = ["Rows:", "Columns:", "Mines:", "Number of Boards:"]
        defaults = ["10", "10", "15", "100"]
        entries = []
        
        for i, (label, default) in enumerate(zip(labels, defaults)):
            tk.Label(
                input_frame,
                text=label,
                font=("Helvetica", 11),
                bg=self.COLORS['bg'],
                fg=self.COLORS['text']
            ).grid(row=i, column=0, sticky='e', padx=10, pady=8)
            
            var = tk.StringVar(value=default)
            entry = tk.Entry(
                input_frame,
                textvariable=var,
                width=12,
                font=("Helvetica", 11),
                bg=self.COLORS['secondary_bg'],
                fg=self.COLORS['text'],
                insertbackground=self.COLORS['text'],
                relief='flat',
                bd=2
            )
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries.append(var)
        
        def start_analytics():
            try:
                rows = int(entries[0].get())
                cols = int(entries[1].get())
                mines = int(entries[2].get())
                num_boards = int(entries[3].get())
                
                if rows < 5 or rows > 30:
                    messagebox.showerror("Invalid Input", "Rows must be between 5 and 30")
                    return
                if cols < 5 or cols > 50:
                    messagebox.showerror("Invalid Input", "Columns must be between 5 and 50")
                    return
                if mines < 1 or mines >= rows * cols:
                    messagebox.showerror("Invalid Input", f"Mines must be between 1 and {rows * cols - 1}")
                    return
                if num_boards < 10 or num_boards > 10000:
                    messagebox.showerror("Invalid Input", "Number of boards must be between 10 and 10000")
                    return
                    
                dialog.destroy()
                
                generator = AnalyticsGenerator()
                generator.generate_and_display(rows, cols, mines, num_boards)
                
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers")
        
        # FIXED: Using ttk.Button with style
        ttk.Button(
            dialog,
            text="🚀 Generate Analytics",
            command=start_analytics,
            style='DialogButton.TButton'
        ).pack(pady=15)
        
    def show_menu(self):
        """Show the main menu again"""
        self.root.deiconify()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainMenu()
    app.run()
