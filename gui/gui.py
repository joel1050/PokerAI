import tkinter as tk
from tkinter import messagebox
import random
from handranks import hand_rank2  # Assuming hand_rank2 is a module that contains hand rankings

ranking = hand_rank2.ranking
face_rank = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

class Card:
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit

    def __str__(self):
        return f"{self.face}{self.suit[0]}"

def generate_deck():
    faces = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    return [Card(face, suit) for suit in suits for face in faces]

def hole_cards():
    random_card_1 = random.choice(deck)
    deck.remove(random_card_1)

    random_card_2 = random.choice(deck)
    deck.remove(random_card_2)

    return random_card_1, random_card_2

def name_hand(hand):
    if face_rank[hand[0].face] < face_rank[hand[1].face]:
        hand = [hand[1], hand[0]]
    if hand[0].face == hand[1].face:
        return f"{hand[0].face}{hand[1].face}"
    else:
        return f"{hand[0].face}{hand[1].face}{isSuited(hand)}"

def isSuited(hand):
    return 's' if hand[0].suit == hand[1].suit else 'o'

def get_ranking(hand):
    so = isSuited(hand)
    try:
        return ranking[f"{hand[0].face}{hand[1].face}{so}"]
    except KeyError:
        return ranking[f"{hand[1].face}{hand[0].face}{so}"]



def deal_flop():
    global community_cards
    community_cards = [deck.pop(), deck.pop(), deck.pop()]
    update_community_cards()
    flop_button.config(state=tk.DISABLED)
    turn_button.config(state=tk.NORMAL)
    river_button.config(state=tk.DISABLED)

def update_community_cards():
    info_label.config(text="Community Cards: " + " ".join(str(card) for card in community_cards))

def update_stacks():
    user_stack_label.config(text=f"Your Stack: {user_stack}")
    ai_stack_label.config(text=f"AI Stack: {ai_stack}")

def update_pot():
    pot_label.config(text=f"Pot: {pot}")

def update_player():
    user_cards_label.config(text=f"Your Cards: {name_hand(user_cards)}")
    print(f"AI Cards: {name_hand(ai_cards)}")
    
def enable_buttons():
    call_button.config(state=tk.NORMAL)
    raise_button.config(state=tk.NORMAL)
    fold_button.config(state=tk.NORMAL)

def user_call():
    global user_action
    user_action = 'Ca'

def user_raise():
    global user_action
    user_action = 'Ra'

def user_fold():
    global user_action
    user_action = 'Fo'


# Initialize global variables
user_stack = 80
ai_stack = 80
bb = ''
sb = ''
pot = 0


def preflop():
    global deck, user_stack, ai_stack, bb, sb, pot
    pot = 0

    update_stacks()

    deck = generate_deck()

    if bb == 'u':
        bb = 'ai'
        sb = 'u'
        user_stack -= 0.5
        ai_stack -= 1
    else:
        bb = 'u'
        sb = 'ai'
        user_stack -= 1
        ai_stack -= 0.5
    
    pot = 1.5
    update_pot()

    card1, card2 = hole_cards()
    global user_cards, ai_cards
    user_cards = [card1, card2]
    card1, card2 = hole_cards()
    ai_cards = [card1, card2]

    update_player()


    user_hand_ranking = get_ranking(user_cards)
    ai_hand_ranking = get_ranking(ai_cards)

    print("User's hand ranking:", user_hand_ranking)
    print("AI's hand ranking:", ai_hand_ranking)

    

# Create the main window
root = tk.Tk()
root.title("Poker Game")

# UI Elements
info_label = tk.Label(root, text="Welcome to Poker!", font=('Helvetica', 16))
info_label.pack()

user_stack_label = tk.Label(root, text=f"Your Stack: {user_stack}")
user_stack_label.pack()
ai_stack_label = tk.Label(root, text=f"AI Stack: {ai_stack}")
ai_stack_label.pack()
pot_label = tk.Label(root, text=f"Pot: {pot}")
pot_label.pack()

deal_button = tk.Button(root, text="Deal", command=preflop)
deal_button.pack()

user_cards_label = tk.Label(root, text="Your Cards: ")
user_cards_label.pack()


# Creating buttons
call_button = tk.Button(root, text="Check/Call", state=tk.DISABLED, command=user_call)
raise_button = tk.Button(root, text="Raise", state=tk.DISABLED, command=user_raise)
fold_button = tk.Button(root, text="Fold", state=tk.DISABLED, command=user_fold)


# Placing buttons at the bottom on the same line
call_button.pack(side=tk.LEFT, anchor='s', padx=5, pady=5)
raise_button.pack(side=tk.LEFT, anchor='s', padx=5, pady=5)
fold_button.pack(side=tk.LEFT, anchor='s', padx=5, pady=5)
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

