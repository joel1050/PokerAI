# PokerAI

A Heads-Up poker bot written in Python, which aims to replicate human-like play by adapting to the user's playstyle. The game uses pot-limit Hold'em rules and has a simple GUI using tkinter. 

# Features
 - An simple and user-friendly interface in tkinter to play poker with the options of Checking, Calling, Folding and placing pot-limit bets.
 - Shuffles and deals a standard 52 card deck
 - Emulates GTO preflop play, which changes in play according to stack-size.
 - Has randomization to induce variability and emulate human-like play.
 - Evaluates hand using hand rankings from high card to full house.

# In Develelopment
 - Making the GUI have the same feature set as the main file.
 - Calculating equity for a given hand and community cards.
 - Assigning a hand-strength value to a hand based on made hand ranking and equity.
 - Assigning a hand-strength value to the opponents hand based on betting and checking frequences.
 - Tracking user statistics like 3b%, VPIP and other metrics to adjust AI betting and bluffing frequences.

# Installation

1. Clone the repository
```bash 
git clone https://github.com/joel1050/PokerAI
```

2. Navigate to the project-directory
```bash 
cd poker-game
```
### Running the game 

To start the game in the terminal:
```bash
python poker.py
```
Input is received via typing in specified letters, 'Ch' for checking, 'Ca' for calling etc.

To start the GUI version (Note: the GUI version is very primitive as of now):
```bash
python gui.py
```
Input is received via clicking buttons with the respective decision.

# Contributing

Any contributions are glady welcomed.
