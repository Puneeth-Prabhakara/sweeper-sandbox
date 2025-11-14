"""
Highscore Management Module
Handles persistent storage and retrieval of highscores
"""

import json
import os
from datetime import datetime


class HighscoreManager:
    """Manages highscores with persistent storage"""
    
    def __init__(self, filename="highscores.json"):
        """
        Initialize the highscore manager
        
        Args:
            filename: Name of the file to store highscores
        """
        self.filename = filename
        self.highscores = self.load_highscores()
    
    def load_highscores(self):
        """Load highscores from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print(f"Warning: Could not load highscores from {self.filename}")
                return {}
        return {}
    
    def save_highscores(self):
        """Save highscores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.highscores, f, indent=2)
        except IOError:
            print(f"Warning: Could not save highscores to {self.filename}")
    
    def get_config_key(self, rows, cols, mines):
        """Generate a unique key for a configuration"""
        return f"{rows}x{cols}x{mines}"
    
    def get_highscores(self, config_key, limit=10):
        """
        Get highscores for a specific configuration
        
        Args:
            config_key: Configuration key (e.g., "9x9x10")
            limit: Maximum number of scores to return
            
        Returns:
            List of highscore dictionaries, sorted by time
        """
        if config_key not in self.highscores:
            return []
        
        scores = self.highscores[config_key]
        # Sort by time (ascending) and return top scores
        scores.sort(key=lambda x: self.parse_time(x['time']))
        return scores[:limit]
    
    @staticmethod
    def parse_time(time_str):
        """
        Parse a time string (HH:MM:SS) to seconds
        
        Args:
            time_str: Time string in format "HH:MM:SS"
            
        Returns:
            Total seconds as float
        """
        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except (ValueError, IndexError):
            return float('inf')  # Invalid time goes to end
    
    @staticmethod
    def format_time(seconds):
        """
        Format seconds to time string (HH:MM:SS)
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:05.2f}"
    
    def is_highscore(self, config_key, time_seconds):
        """
        Check if a time qualifies as a highscore
        
        Args:
            config_key: Configuration key
            time_seconds: Time in seconds
            
        Returns:
            True if this is a top 10 time, False otherwise
        """
        scores = self.get_highscores(config_key, limit=10)
        
        # If less than 10 scores, it's automatically a highscore
        if len(scores) < 10:
            return True
        
        # Check if better than the worst top 10 score
        worst_time = self.parse_time(scores[-1]['time'])
        return time_seconds < worst_time
    
    def add_highscore(self, rows, cols, mines, player_name, time_seconds):
        """
        Add a new highscore
        
        Args:
            rows: Number of rows
            cols: Number of columns
            mines: Number of mines
            player_name: Name of the player
            time_seconds: Time in seconds
            
        Returns:
            True if added successfully, False otherwise
        """
        config_key = self.get_config_key(rows, cols, mines)
        
        # Check if it qualifies as a highscore
        if not self.is_highscore(config_key, time_seconds):
            return False
        
        # Initialize config if doesn't exist
        if config_key not in self.highscores:
            self.highscores[config_key] = []
        
        # Create score entry
        score_entry = {
            'name': player_name,
            'time': self.format_time(time_seconds),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'rows': rows,
            'cols': cols,
            'mines': mines
        }
        
        # Add to highscores
        self.highscores[config_key].append(score_entry)
        
        # Keep only top 10
        self.highscores[config_key] = self.get_highscores(config_key, limit=10)
        
        # Save to file
        self.save_highscores()
        
        return True
    
    def get_rank(self, config_key, time_seconds):
        """
        Get the rank for a given time
        
        Args:
            config_key: Configuration key
            time_seconds: Time in seconds
            
        Returns:
            Rank (1-10) or None if not in top 10
        """
        scores = self.get_highscores(config_key, limit=10)
        
        # Add the new time and sort
        times = [self.parse_time(score['time']) for score in scores]
        times.append(time_seconds)
        times.sort()
        
        # Find rank
        try:
            rank = times.index(time_seconds) + 1
            return rank if rank <= 10 else None
        except ValueError:
            return None
    
    def clear_highscores(self, config_key=None):
        """
        Clear highscores
        
        Args:
            config_key: Specific configuration to clear, or None to clear all
        """
        if config_key:
            if config_key in self.highscores:
                del self.highscores[config_key]
        else:
            self.highscores = {}
        
        self.save_highscores()
    
    def export_highscores(self, filename="highscores_export.txt"):
        """Export highscores to a readable text file"""
        try:
            with open(filename, 'w') as f:
                f.write("MINESWEEPER HIGHSCORES\n")
                f.write("=" * 60 + "\n\n")
                
                for config_key, scores in sorted(self.highscores.items()):
                    if scores:
                        f.write(f"Configuration: {config_key}\n")
                        f.write("-" * 60 + "\n")
                        for i, score in enumerate(scores, 1):
                            f.write(f"{i}. {score['name']:20s} {score['time']:12s} ({score['date']})\n")
                        f.write("\n")
            return True
        except IOError:
            return False


if __name__ == "__main__":
    # Test the highscore manager
    print("Testing Highscore Manager...")
    
    manager = HighscoreManager("test_highscores.json")
    
    # Add some test scores
    manager.add_highscore(9, 9, 10, "Alice", 45.5)
    manager.add_highscore(9, 9, 10, "Bob", 52.3)
    manager.add_highscore(9, 9, 10, "Charlie", 38.7)
    
    # Get highscores
    scores = manager.get_highscores("9x9x10")
    print("\nHighscores for 9x9x10:")
    for i, score in enumerate(scores, 1):
        print(f"{i}. {score['name']:15s} {score['time']}")
    
    # Test rank
    rank = manager.get_rank("9x9x10", 40.0)
    print(f"\nRank for 40.0 seconds: {rank}")
    
    # Clean up test file
    if os.path.exists("test_highscores.json"):
        os.remove("test_highscores.json")
    
    print("\nHighscore Manager test complete!")