# 💣 Minesweeper Game

A feature-rich implementation of the classic Minesweeper game built with Python and Tkinter, featuring multiple difficulty levels, custom game modes, highscore tracking, and statistical analytics.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Game Rules](#game-rules)
- [Development](#development)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

---

## ✨ Features

### 🎮 Core Gameplay
- **Classic Minesweeper mechanics** with modern GUI
- **Safe first click** - First click is guaranteed to be safe
- **Auto-reveal** - Empty cells automatically reveal surrounding areas
- **Flag system** with intelligent limiting (can't place more flags than mines)
- **Real-time timer** tracking game duration
- **Mine counter** showing remaining mines

### 🎯 Game Modes
- **Easy**: 9×9 grid with 10 mines
- **Intermediate**: 16×16 grid with 40 mines
- **Expert**: 16×30 grid with 99 mines
- **Custom**: Create your own board size and mine count (with smart validation)

### 🏆 Advanced Features
- **Highscore System**: Top 10 scores saved for each configuration
- **Persistent Storage**: Highscores saved in JSON format
- **Board Analytics**: Statistical analysis of randomly generated boards
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Modern UI**: Dark theme with custom styling

### 🛡️ Smart Validation
- Prevents impossible board configurations
- Blocks instant-win scenarios on small boards
- Clear error messages for invalid inputs
- Automatic density calculations

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- tkinter (usually included with Python)

### Setup

1. **Clone the repository**
https://github.com/Puneeth-Prabhakara/sweeper-sandbox.git

2. **Verify Python installation**

3. **Run the game**

---

## 🔧 Technical Details

### Technologies Used
- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (built-in)
- **Data Storage**: JSON for highscore persistence
- **Algorithms**: 
  - Breadth-First Search (BFS) for flood-fill
  - Random board generation with constraints
  - Statistical sampling for analytics

## 🐛 Bug Fixes & Changelog

### v1.1 (Current)
- ✅ Fixed instant-win bug on small boards with extreme mine counts
- ✅ Improved macOS button styling compatibility
- ✅ Added flag limit enforcement
- ✅ Enhanced error messages for validation

### v1.0 (Initial Release)
- ✅ Core Minesweeper gameplay
- ✅ Three standard difficulty levels
- ✅ Custom game mode
- ✅ Highscore system
- ✅ Board analytics feature

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see below for details:

MIT License
Copyright (c) 2025 Puneeth Prabhakara
Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated documentation files (the “Software”), to dealin the Software without restriction, including without limitation the rightsto use, copy, modify, merge, publish, distribute, sublicense, and/or sellcopies of the Software, and to permit persons to whom the Software isfurnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in allcopies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS ORIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THEAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHERLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THESOFTWARE.

## 🙏 Acknowledgments

- Inspired by Microsoft Minesweeper
- Built as part of MSc Business Analytics coursework at UCD
- Thanks to the Python and Tkinter communities for documentation
- Color palette inspired by modern dark themes

---

**Happy Mining! 💣**

---

*Last Updated: November 2025*