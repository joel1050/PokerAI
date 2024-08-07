# PokerAI

A Heads-Up poker bot written in Python, which aims to replicate human-like play by adapting to the user's playstyle. The game uses pot-limit Hold'em rules and has a simple GUI using tkinter. 

# Features
 - An simple and user-friendly interface in tkinter to play poker with the options of Checking, Calling, Folding and placing pot-limit bets.
 - Shuffles and deals a standard 52 card deck
 - Emulates GTO preflop play, which changes according to stack-size.
 - Has randomization to induce variability and emulate human-like play.
 - Evaluates hand using hand rankings from high card to full house.
 - Can calculate all outs for a given hand.
 - Can calculate equity for given hand.
 - Can calculate killer cards (cards which beat your hand) for a given board and uses it to determine range of opponent.
 - Creates a hand-strength value for evaluating strength of hands. Uses made hands, and equity to determine this. Also reduces strength according to draws and pairs in community cards. 

# In Develelopment
 ~~- Calculating equity for a given hand and community cards by evaluating draws and finding their outs.~~
 
 ~~- Finding Killer Cards (list of cards which, if possessed by either player, completes a draw or hand).~~
 
 ~~- Assigning a hand-strength value to a hand based on made hand ranking and equity.~~
 
 - Assigning a hand-strength value to the opponents hand based on betting and checking frequences.
 - Finishing turn and river play
 - Ability to evaluate strength of 'kickers' in one pair.
 - Recognizing which hand types are higher (eg. pair of aces are higher than a pair of 2s).
 - Tracking user statistics like 3b%, VPIP and other metrics to adjust AI betting and bluffing frequences.
 - Making the GUI have the same feature set as the main file.

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

Any contributions are gladly welcomed.
