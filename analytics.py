"""
Analytics Module
Generates and displays analytics for Minesweeper boards
"""

import matplotlib.pyplot as plt
import numpy as np
from board_generator import BoardGenerator
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading


class AnalyticsGenerator:
    """Generates analytics visualizations for Minesweeper boards"""
    
    def __init__(self):
        self.boards = []
        self.rows = 0
        self.cols = 0
        self.mines = 0
        self.num_boards = 0
    
    def generate_boards(self, rows, cols, mines, num_boards, progress_callback=None):
        """
        Generate multiple boards for analytics
        
        Args:
            rows: Number of rows
            cols: Number of columns
            mines: Number of mines
            num_boards: Number of boards to generate
            progress_callback: Optional callback function for progress updates
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.num_boards = num_boards
        self.boards = []
        
        for i in range(num_boards):
            board = BoardGenerator.generate_board(rows, cols, mines)
            self.boards.append(board)
            
            if progress_callback:
                progress = (i + 1) / num_boards * 100
                progress_callback(progress)
    
    def plot_white_cells(self, ax):
        """Plot histogram of white cells (cells with 0 adjacent mines)"""
        white_cell_counts = []
        
        for board in self.boards:
            count = BoardGenerator.count_white_cells(board)
            white_cell_counts.append(count)
        
        ax.hist(white_cell_counts, bins=30, color='skyblue', edgecolor='black')
        ax.set_xlabel('Number of White Cells', fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        ax.set_title('Distribution of White Cells', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        mean_white = np.mean(white_cell_counts)
        ax.axvline(mean_white, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_white:.1f}')
        ax.legend()
    
    def plot_number_distribution(self, ax):
        """Plot distribution of numbers shown in cells"""
        # Aggregate counts across all boards
        total_distribution = {i: 0 for i in range(9)}
        
        for board in self.boards:
            dist = BoardGenerator.get_number_distribution(board)
            for num, count in dist.items():
                total_distribution[num] += count
        
        # Create bar chart
        numbers = list(range(9))
        counts = [total_distribution[i] for i in numbers]
        
        colors = ['lightgray', 'blue', 'green', 'red', 'darkblue', 
                 'darkred', 'cyan', 'black', 'gray']
        
        bars = ax.bar(numbers, counts, color=colors, edgecolor='black')
        ax.set_xlabel('Number in Cell', fontsize=10)
        ax.set_ylabel('Total Count', fontsize=10)
        ax.set_title('Distribution of Numbers in Cells', fontsize=12, fontweight='bold')
        ax.set_xticks(numbers)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=8)
    
    def plot_mine_clusters(self, ax):
        """Plot distribution of mine clusters per board"""
        cluster_counts = []
        
        for board in self.boards:
            count = BoardGenerator.count_mine_clusters(board)
            cluster_counts.append(count)
        
        # Create histogram
        max_clusters = max(cluster_counts) if cluster_counts else 1
        bins = range(1, max_clusters + 2)
        
        ax.hist(cluster_counts, bins=bins, color='orange', edgecolor='black', align='left')
        ax.set_xlabel('Number of Mine Clusters', fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        ax.set_title('Distribution of Mine Clusters per Board', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        mean_clusters = np.mean(cluster_counts)
        ax.axvline(mean_clusters, color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {mean_clusters:.1f}')
        ax.legend()
    
    def plot_mine_heatmap(self, ax):
        """Plot heatmap of average mine counts in 3x3 regions"""
        heatmap = BoardGenerator.calculate_mine_heatmap(self.boards)
        
        if heatmap is None:
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', transform=ax.transAxes)
            return
        
        # Create heatmap
        im = ax.imshow(heatmap, cmap='YlOrRd', aspect='auto', interpolation='nearest')
        
        ax.set_xlabel('Column', fontsize=10)
        ax.set_ylabel('Row', fontsize=10)
        ax.set_title('Average Mine Count in 3×3 Neighborhood', fontsize=12, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Average Mines', fontsize=9)
        
        # Add grid
        ax.set_xticks(np.arange(self.cols))
        ax.set_yticks(np.arange(self.rows))
        ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    
    def generate_and_display(self, rows, cols, mines, num_boards):
        """Generate boards and display analytics in a window"""
        # Create progress window
        progress_window = tk.Toplevel()
        progress_window.title("Generating Boards...")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        progress_window.transient()
        progress_window.grab_set()
        
        # Center window
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - 200
        y = (progress_window.winfo_screenheight() // 2) - 75
        progress_window.geometry(f'+{x}+{y}')
        
        tk.Label(
            progress_window,
            text=f"Generating {num_boards} boards...",
            font=("Arial", 12)
        ).pack(pady=20)
        
        progress_bar = ttk.Progressbar(
            progress_window,
            length=300,
            mode='determinate'
        )
        progress_bar.pack(pady=10)
        
        progress_label = tk.Label(progress_window, text="0%", font=("Arial", 10))
        progress_label.pack()
        
        # Flag to track completion
        generation_complete = [False]
        
        def update_progress(value):
            progress_bar['value'] = value
            progress_label.config(text=f"{int(value)}%")
            progress_window.update()
        
        def generate_in_thread():
            try:
                self.generate_boards(rows, cols, mines, num_boards, update_progress)
                generation_complete[0] = True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate boards: {str(e)}")
                progress_window.destroy()
        
        # Start generation in separate thread
        thread = threading.Thread(target=generate_in_thread)
        thread.daemon = True
        thread.start()
        
        # Wait for generation to complete
        def check_completion():
            if generation_complete[0]:
                progress_window.destroy()
                self.display_analytics()
            else:
                progress_window.after(100, check_completion)
        
        progress_window.after(100, check_completion)
    
    def display_analytics(self):
        """Display all analytics plots in a window"""
        # Create window
        window = tk.Toplevel()
        window.title(f"Analytics - {self.rows}×{self.cols} ({self.mines} mines, {self.num_boards} boards)")
        window.geometry("1200x800")
        
        # Create matplotlib figure with 2x2 subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(
            f'Minesweeper Analytics\n{self.rows}×{self.cols} board, {self.mines} mines, {self.num_boards} boards analyzed',
            fontsize=14,
            fontweight='bold'
        )
        
        # Generate plots
        self.plot_white_cells(ax1)
        self.plot_number_distribution(ax2)
        self.plot_mine_clusters(ax3)
        self.plot_mine_heatmap(ax4)
        
        plt.tight_layout()
        
        # Embed matplotlib figure in tkinter window
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Add buttons frame
        button_frame = tk.Frame(window)
        button_frame.pack(pady=10)
        
        def save_figure():
            filename = f"analytics_{self.rows}x{self.cols}x{self.mines}_{self.num_boards}boards.png"
            try:
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Saved", f"Analytics saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
        
        tk.Button(
            button_frame,
            text="Save as PNG",
            command=save_figure,
            width=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=window.destroy,
            width=15
        ).pack(side='left', padx=5)
        
        # Center window
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    # Test analytics
    print("Testing Analytics Generator...")
    
    # Create a simple tkinter root for testing
    root = tk.Tk()
    root.withdraw()
    
    generator = AnalyticsGenerator()
    generator.generate_and_display(rows=10, cols=10, mines=15, num_boards=100)
    
    root.mainloop()