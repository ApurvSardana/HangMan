# Hangman Game

A modern implementation of the classic Hangman game with a beautiful GUI interface.

## Features

- Modern, sleek GUI design
- Dark theme with vibrant accents
- Real-time game state updates
- Easy-to-use interface
- Word list support

## Requirements

- Python 3.x
- C++ compiler (for building the game engine)
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ApurvSardana/HangMan.git
cd HangMan
```

2. Compile the C++ game engine:
```bash
g++ hangman.cpp -o hangman.exe
```

3. Run the game:
```bash
python gui.py
```

## How to Play

1. The game will randomly select a word from the word list
2. Enter one letter at a time to guess the word
3. You have 5 turns to guess the word correctly
4. Correct guesses will reveal the letter in the word
5. Incorrect guesses will reduce your remaining turns

## Project Structure

- `gui.py` - Python GUI implementation
- `hangman.cpp` - C++ game engine
- `list.txt` - Word list for the game

## Contributing

Feel free to submit issues and enhancement requests!
