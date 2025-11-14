"""
Minesweeper Game Module
Handles the game GUI and logic
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from collections import deque
import os

from board_generator import BoardGenerator


class MinesweeperGame:
    """Main game class with GUI"""
    
    # Cell states
    STATE_DEFAULT = 0
    STATE_CLICKED = 1
    STATE_FLAGGED = 2
    
    def __init__(self, rows, cols, mines, difficulty, highscore_manager, on_close=None):
        """
        Initialize the game
        
        Args:
            rows: Number of rows
            cols: Number of columns
            mines: Number of mines
            difficulty: Difficulty name (for highscore tracking)
            highscore_manager: HighscoreManager instance
            on_close: Callback function when game window closes
        """
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.difficulty = difficulty
        self.highscore_manager = highscore_manager
        self.on_close_callback = on_close
        
        # Game state
        self.board = None  # Will be generated on first click
        self.cell_states = [[self.STATE_DEFAULT for _ in range(cols)] for _ in range(rows)]
        self.revealed_count = 0
        self.flag_count = 0
        self.game_over = False
        self.game_won = False
        self.start_time = None
        self.first_click = True
        
        # Create window FIRST
        self.root = tk.Toplevel()
        self.root.title(f"Minesweeper - {difficulty}")
        self.root.resizable(False, False)
        
        # Try to load images AFTER window is created
        self.use_images = self.load_images()
        
        # Create UI
        self.create_ui()
        
        # Center window
        self.center_window()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.close_game)
    
    def load_images(self):
        """Try to load tile images, return True if successful"""
        try:
            # Load images with the root window as master
            self.images = {
                "plain": tk.PhotoImage(file="images/tile_plain.gif", master=self.root),
                "clicked": tk.PhotoImage(file="images/tile_clicked.gif", master=self.root),
                "mine": tk.PhotoImage(file="images/tile_mine.gif", master=self.root),
                "flag": tk.PhotoImage(file="images/tile_flag.gif", master=self.root),
                "wrong": tk.PhotoImage(file="images/tile_wrong.gif", master=self.root),
                "numbers": []
            }
            for i in range(1, 9):
                self.images["numbers"].append(
                    tk.PhotoImage(file=f"images/tile_{i}.gif", master=self.root)
                )
            return True
        except Exception as e:
            print(f"Warning: Could not load images, using text mode. Error: {e}")
            return False
    
    def create_ui(self):
        """Create the game UI"""
        # Main frame
        self.frame = tk.Frame(self.root, bg='#2c3e50')
        self.frame.pack(padx=10, pady=10)
        
        # Top info panel
        info_frame = tk.Frame(self.frame, bg='#34495e')
        info_frame.grid(row=0, column=0, columnspan=self.cols, pady=5, sticky='ew')
        
        # Timer
        self.timer_label = tk.Label(
            info_frame,
            text="00:00:00",
            font=("Arial", 14, "bold"),
            width=10,
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.timer_label.pack(side='left', padx=20)
        
        # Mines remaining counter (changed from mine counter)
        self.mine_label = tk.Label(
            info_frame,
            text=f"💣 Remaining: {self.total_mines}",
            font=("Arial", 12),
            width=18,
            bg='#34495e',
            fg='#e74c3c'
        )
        self.mine_label.pack(side='left', padx=10)
        
        # Flag counter (shows how many flags placed)
        self.flag_label = tk.Label(
            info_frame,
            text=f"🚩 Flags: {self.flag_count}",
            font=("Arial", 12),
            width=12,
            bg='#34495e',
            fg='#f39c12'
        )
        self.flag_label.pack(side='left', padx=10)
        
        # Create game board
        self.buttons = []
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                if self.use_images:
                    btn = tk.Button(
                        self.frame,
                        image=self.images["plain"],
                        width=30,
                        height=30
                    )
                else:
                    btn = tk.Button(
                        self.frame,
                        text=" ",
                        width=3,
                        height=1,
                        font=("Courier", 10, "bold"),
                        bg='#95a5a6',
                        fg='#2c3e50'
                    )
                
                btn.grid(row=row+1, column=col, padx=1, pady=1)
                btn.bind("<Button-1>", lambda e, r=row, c=col: self.left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=row, c=col: self.right_click(r, c))
                btn.bind("<Button-2>", lambda e, r=row, c=col: self.right_click(r, c))  # Mac
                
                button_row.append(btn)
            self.buttons.append(button_row)
        
        # Bottom button panel
        button_frame = tk.Frame(self.frame, bg='#2c3e50')
        button_frame.grid(row=self.rows+1, column=0, columnspan=self.cols, pady=10)
        
        tk.Button(
            button_frame,
            text="New Game",
            command=self.restart_game,
            width=12,
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Main Menu",
            command=self.close_game,
            width=12,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=5)
        
        # Start timer update
        self.update_timer()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def update_timer(self):
        """Update the timer display"""
        if self.start_time and not self.game_over:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        if not self.game_over:
            self.root.after(100, self.update_timer)
    
    def update_mine_counter(self):
        """Update the mines remaining counter"""
        remaining = self.total_mines - self.flag_count
        self.mine_label.config(text=f"💣 Remaining: {remaining}")
        self.flag_label.config(text=f"🚩 Flags: {self.flag_count}")
    
    def left_click(self, row, col):
        """Handle left click on a cell"""
        if self.game_over:
            return
        
        # Ignore clicks on flagged cells
        if self.cell_states[row][col] == self.STATE_FLAGGED:
            return
        
        # Ignore already revealed cells
        if self.cell_states[row][col] == self.STATE_CLICKED:
            return
        
        # Generate board on first click (safe first click)
        if self.first_click:
            self.generate_board(row, col)
            self.first_click = False
            self.start_time = datetime.now()
        
        # Check if mine
        if self.board[row][col] == -1:
            self.reveal_cell(row, col)
            self.end_game(won=False)
            return
        
        # Reveal cell
        self.reveal_cell(row, col)
        
        # If cell is 0, reveal surrounding cells
        if self.board[row][col] == 0:
            self.reveal_surrounding(row, col)
        
        # Check win condition
        if self.check_win():
            self.end_game(won=True)
    
    def right_click(self, row, col):
    ###Handle right click (flag/unflag)###
        if self.game_over:
            return
        
        # Ignore already revealed cells
        if self.cell_states[row][col] == self.STATE_CLICKED:
            return
        
        # Start timer on first action
        if self.first_click and not self.start_time:
            self.start_time = datetime.now()
        
        # Toggle flag
        if self.cell_states[row][col] == self.STATE_FLAGGED:
            # Unflag - always allowed
            self.cell_states[row][col] = self.STATE_DEFAULT
            if self.use_images:
                self.buttons[row][col].config(image=self.images["plain"])
            else:
                self.buttons[row][col].config(text=" ", bg="#95a5a6", fg="#2c3e50")
            self.flag_count -= 1
        else:
            # Check if we've reached the flag limit
            if self.flag_count >= self.total_mines:
                # Show a warning message
                messagebox.showwarning(
                    "Flag Limit Reached",
                    f"You cannot place more than {self.total_mines} flags!\n\nRemove a flag first to place a new one."
                )
                return
            
            # Place flag - only if under the limit
            self.cell_states[row][col] = self.STATE_FLAGGED
            if self.use_images:
                self.buttons[row][col].config(image=self.images["flag"])
            else:
                # Show flag emoji
                self.buttons[row][col].config(text="🚩", fg="red", bg="#f39c12", font=("Arial", 16))
            self.flag_count += 1
        
        # Update mine counter
        self.update_mine_counter()


    
    def generate_board(self, exclude_row, exclude_col):
        """Generate the board, excluding first click and neighbors"""
        # Get cells to exclude (first click + neighbors)
        exclude_cells = set()
        exclude_cells.add((exclude_row, exclude_col))
        neighbors = BoardGenerator.get_neighbors(
            exclude_row, exclude_col, self.rows, self.cols
        )
        exclude_cells.update(neighbors)
        
        # Generate board
        self.board = BoardGenerator.generate_board(
            self.rows, self.cols, self.total_mines, exclude_cells
        )
    
    def reveal_cell(self, row, col):
        """Reveal a single cell"""
        if self.cell_states[row][col] == self.STATE_CLICKED:
            return
        
        self.cell_states[row][col] = self.STATE_CLICKED
        self.revealed_count += 1
        
        value = self.board[row][col]
        
        if self.use_images:
            if value == -1:
                self.buttons[row][col].config(image=self.images["mine"])
            elif value == 0:
                self.buttons[row][col].config(image=self.images["clicked"])
            else:
                self.buttons[row][col].config(image=self.images["numbers"][value-1])
        else:
            if value == -1:
                self.buttons[row][col].config(text="💣", fg="red", bg="#e74c3c", font=("Arial", 16))
            elif value == 0:
                self.buttons[row][col].config(text=" ", bg="#ecf0f1")
            else:
                colors = ["#3498db", "#27ae60", "#e74c3c", "#9b59b6", "#e67e22", "#1abc9c", "#34495e", "#95a5a6"]
                self.buttons[row][col].config(
                    text=str(value),
                    fg=colors[value-1],
                    bg="#ecf0f1",
                    font=("Courier", 12, "bold")
                )
    
    def reveal_surrounding(self, row, col):
        """Reveal surrounding cells using BFS"""
        queue = deque([(row, col)])
        visited = set()
        
        while queue:
            r, c = queue.popleft()
            
            if (r, c) in visited:
                continue
            visited.add((r, c))
            
            # Get neighbors
            neighbors = BoardGenerator.get_neighbors(r, c, self.rows, self.cols)
            
            for nr, nc in neighbors:
                if self.cell_states[nr][nc] != self.STATE_CLICKED:
                    self.reveal_cell(nr, nc)
                    
                    # If neighbor is also 0, add to queue
                    if self.board[nr][nc] == 0 and (nr, nc) not in visited:
                        queue.append((nr, nc))
    
    def check_win(self):
        """Check if the player has won"""
        # Win condition: all non-mine cells revealed
        total_cells = self.rows * self.cols
        non_mine_cells = total_cells - self.total_mines
        return self.revealed_count == non_mine_cells
    
    def end_game(self, won):
        """End the game"""
        self.game_over = True
        self.game_won = won
        
        if not won:
            # Reveal all mines
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.board[row][col] == -1:
                        if self.cell_states[row][col] == self.STATE_FLAGGED:
                            # Correctly flagged mine
                            if self.use_images:
                                self.buttons[row][col].config(image=self.images["flag"])
                            else:
                                self.buttons[row][col].config(text="🚩", bg="#27ae60", font=("Arial", 16))
                        else:
                            # Unrevealed mine
                            if self.use_images:
                                self.buttons[row][col].config(image=self.images["mine"])
                            else:
                                self.buttons[row][col].config(text="💣", bg="#e74c3c", font=("Arial", 16))
                    elif self.cell_states[row][col] == self.STATE_FLAGGED:
                        # Wrong flag
                        if self.use_images:
                            self.buttons[row][col].config(image=self.images["wrong"])
                        else:
                            self.buttons[row][col].config(text="❌", bg="#e67e22", font=("Arial", 16))
            
            messagebox.showinfo("Game Over", "You hit a mine!\n\nBetter luck next time!")
        
        else:
            # Calculate time
            elapsed = (datetime.now() - self.start_time).total_seconds()
            time_str = f"{int(elapsed//60):02d}:{int(elapsed%60):02d}"
            
            # Check if highscore
            config_key = self.highscore_manager.get_config_key(
                self.rows, self.cols, self.total_mines
            )
            
            if self.highscore_manager.is_highscore(config_key, elapsed):
                rank = self.highscore_manager.get_rank(config_key, elapsed)
                
                msg = f"Congratulations! You won!\n\nTime: {time_str}\n\n"
                msg += f"This is a TOP 10 score (Rank #{rank})!\n"
                msg += "Enter your name for the highscore table:"
                
                messagebox.showinfo("Victory!", msg)
                
                # Ask for name
                player_name = simpledialog.askstring(
                    "Highscore!",
                    "Enter your name:",
                    parent=self.root
                )
                
                if player_name:
                    self.highscore_manager.add_highscore(
                        self.rows, self.cols, self.total_mines,
                        player_name, elapsed
                    )
                    messagebox.showinfo(
                        "Saved!",
                        f"Your score has been saved!\n\nRank: #{rank}"
                    )
            else:
                messagebox.showinfo(
                    "Victory!",
                    f"Congratulations! You won!\n\nTime: {time_str}"
                )
    
    def restart_game(self):
        """Restart the current game"""
        # Reset game state
        self.board = None
        self.cell_states = [[self.STATE_DEFAULT for _ in range(self.cols)] 
                           for _ in range(self.rows)]
        self.revealed_count = 0
        self.flag_count = 0
        self.game_over = False
        self.game_won = False
        self.start_time = None
        self.first_click = True
        
        # Reset UI
        self.update_mine_counter()
        self.timer_label.config(text="00:00:00")
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.use_images:
                    self.buttons[row][col].config(image=self.images["plain"])
                else:
                    self.buttons[row][col].config(
                        text=" ",
                        bg="#95a5a6",
                        fg="#2c3e50",
                        font=("Courier", 10, "bold")
                    )
        
        # Restart timer
        self.update_timer()
    
    def close_game(self):
        """Close the game window"""
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()


if __name__ == "__main__":
    # Test the game
    from highscores import HighscoreManager
    
    # Need a root window for testing
    root = tk.Tk()
    root.withdraw()
    
    hs_manager = HighscoreManager()
    game = MinesweeperGame(9, 9, 10, "Easy", hs_manager)
    
    root.mainloop()
