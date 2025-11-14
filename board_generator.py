"""
Board Generator Module
Handles generation of Minesweeper boards with mine placement
"""

import random


class BoardGenerator:
    """Generates Minesweeper boards with proper mine placement"""
    
    @staticmethod
    def generate_board(rows, cols, mines, exclude_cells=None):
        """
        Generate a minesweeper board
        
        Args:
            rows: Number of rows
            cols: Number of columns
            mines: Number of mines to place
            exclude_cells: Set of (row, col) tuples to exclude from mine placement
            
        Returns:
            2D list representing the board, where:
            - -1 represents a mine
            - 0-8 represents the number of adjacent mines
        """
        if exclude_cells is None:
            exclude_cells = set()
            
        # Initialize empty board
        board = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # Get all possible positions for mines
        all_positions = [(r, c) for r in range(rows) for c in range(cols)]
        available_positions = [pos for pos in all_positions if pos not in exclude_cells]
        
        # Validate that we have enough positions
        if len(available_positions) < mines:
            raise ValueError(f"Cannot place {mines} mines with {len(available_positions)} available positions")
        
        # Randomly select mine positions
        mine_positions = random.sample(available_positions, mines)
        
        # Place mines
        for row, col in mine_positions:
            board[row][col] = -1
        
        # Calculate numbers for non-mine cells
        for row in range(rows):
            for col in range(cols):
                if board[row][col] != -1:  # If not a mine
                    board[row][col] = BoardGenerator.count_adjacent_mines(board, row, col, rows, cols)
        
        return board
    
    @staticmethod
    def count_adjacent_mines(board, row, col, rows, cols):
        """Count the number of mines adjacent to a cell"""
        count = 0
        
        # Check all 8 adjacent cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Skip the cell itself
                    continue
                    
                new_row = row + dr
                new_col = col + dc
                
                # Check if in bounds and is a mine
                if (0 <= new_row < rows and 
                    0 <= new_col < cols and 
                    board[new_row][new_col] == -1):
                    count += 1
        
        return count
    
    @staticmethod
    def get_neighbors(row, col, rows, cols):
        """Get all valid neighboring cell coordinates"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row = row + dr
                new_col = col + dc
                if 0 <= new_row < rows and 0 <= new_col < cols:
                    neighbors.append((new_row, new_col))
        return neighbors
    
    @staticmethod
    def count_white_cells(board):
        """Count cells with 0 adjacent mines (white cells)"""
        count = 0
        for row in board:
            for cell in row:
                if cell == 0:
                    count += 1
        return count
    
    @staticmethod
    def get_number_distribution(board):
        """
        Get the distribution of numbers on the board
        Returns a dict with keys 0-8 and counts as values
        """
        distribution = {i: 0 for i in range(9)}
        
        for row in board:
            for cell in row:
                if cell >= 0:  # Not a mine
                    distribution[cell] += 1
        
        return distribution
    
    @staticmethod
    def count_mine_clusters(board):
        """
        Count the number of mine clusters using Union-Find algorithm
        A cluster is a group of mines that touch each other
        (horizontally, vertically, or diagonally)
        """
        rows = len(board)
        cols = len(board[0])
        
        # Find all mine positions
        mines = set()
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == -1:
                    mines.add((r, c))
        
        if not mines:
            return 0
        
        # Use DFS to find connected components
        visited = set()
        clusters = 0
        
        def dfs(row, col):
            """Depth-first search to explore a cluster"""
            if (row, col) in visited:
                return
            visited.add((row, col))
            
            # Check all 8 adjacent cells
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row, new_col = row + dr, col + dc
                    if (new_row, new_col) in mines and (new_row, new_col) not in visited:
                        dfs(new_row, new_col)
        
        # Count clusters
        for mine_pos in mines:
            if mine_pos not in visited:
                dfs(mine_pos[0], mine_pos[1])
                clusters += 1
        
        return clusters
    
    @staticmethod
    def calculate_mine_heatmap(boards):
        """
        Calculate a heatmap of average mine counts in 3x3 regions
        
        Args:
            boards: List of board configurations
            
        Returns:
            2D array with average mine counts for each position
        """
        if not boards:
            return None
        
        rows = len(boards[0])
        cols = len(boards[0][0])
        
        # Initialize heatmap
        heatmap = [[0.0 for _ in range(cols)] for _ in range(rows)]
        
        # Sum up mine counts for each position across all boards
        for board in boards:
            for r in range(rows):
                for c in range(cols):
                    # Count mines in 3x3 region around (r, c)
                    mine_count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if board[nr][nc] == -1:
                                    mine_count += 1
                    heatmap[r][c] += mine_count
        
        # Average the counts
        num_boards = len(boards)
        for r in range(rows):
            for c in range(cols):
                heatmap[r][c] /= num_boards
        
        return heatmap


if __name__ == "__main__":
    # Test the board generator
    print("Testing Board Generator...")
    
    # Generate a simple board
    board = BoardGenerator.generate_board(10, 10, 15)
    
    print("Board generated successfully!")
    print(f"White cells: {BoardGenerator.count_white_cells(board)}")
    print(f"Number distribution: {BoardGenerator.get_number_distribution(board)}")
    print(f"Mine clusters: {BoardGenerator.count_mine_clusters(board)}")
    
    # Display board (for testing)
    print("\nBoard visualization:")
    for row in board:
        print(' '.join([('*' if cell == -1 else str(cell)) for cell in row]))