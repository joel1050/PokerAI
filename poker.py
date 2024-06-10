import random
import hand_rank

ranking = hand_rank.ranking

class Card:
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit

#generates deck of 
def generate_deck():
    faces = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = []

    for suit in suits:
        for face in faces:
            card = Card(face, suit)
            deck.append(card)

    return deck

deck = generate_deck()

#declaring initial stack as 100bbs for user and AI
user_stack = 100
ai_stack = 100


#used for dealing hole cards to user and AI
def hole_cards():
    random_card_1 = random.choice(deck)
    deck.remove(random_card_1)

    random_card_2 = random.choice(deck)
    deck.remove(random_card_2)

    return random_card_1, random_card_2

def isSuited(hand):
    if (hand[0].suit == hand[1].suit):
        return 's'
    elif (hand[0].face == hand[1].face):
        return ''
    else:
        return 'o'
    
    
#returns name of hand, eg: J8s AKo
def name_hand(hand):
    so = isSuited(hand)
    return f"{hand[0].face}{hand[1].face}{so}"

#returns value from ranking dict
def get_ranking(hand):
    so = isSuited(hand)
    try:
        return ranking[f"{hand[0].face}{hand[1].face}{so}"]
    except KeyError:
        return ranking[f"{hand[1].face}{hand[0].face}{so}"]

def get_stacksize():
    if (ai_stack < 20):
        return 'low'
    elif (ai_stack < 50):
        return 'mid'
    else:
        return 'deep'


#setting blinds
bb = 'u'
sb = 'ai'

#dealing cards
card1, card2 = hole_cards()
user_cards = [card1,card2]
card1, card2 = hole_cards()
ai_cards = [card1,card2]

#printing names of hands
print(name_hand(user_cards))
print(name_hand(ai_cards))

print(get_ranking(user_cards))
print(get_ranking(ai_cards))

#assigns hand ranking to ai hand
ai_hand_ranking = get_ranking(ai_cards)

pot = 1.5
user_stack -= 1
ai_stack -= .5

# Determines preflop action considering stacksize and hand ranking
def ai_preflop_action_sb(range):
    stacksize = get_stacksize()
    if stacksize == 'low':
        if 50 <= range <= 86:
            if random.random() < 0.20:
                return 'raise'
            elif random.random() < 0.15:
                return 'fold'
            else:
                return 'call'
        elif range < 50:
            if random.random() < 0.25:
                return 'call'
            else:
                return 'raise'
        else:
            if random.random() < 0.20:
                return 'call'
            else:
                return 'fold'
    elif stacksize == 'mid':
        if 45 <= range <= 70:
            if random.random() < 0.25:
                return 'raise'
            elif random.random() < 0.10:
                return 'fold'
            else:
                return 'call'
        elif range < 45:
            if random.random() < 0.25:
                return 'call'
            else:
                return 'raise'
        else:
            if random.random() < 0.10:
                return 'call'
            else:
                return 'fold'
    else:
        if 40 <= range <= 60:
            if random.random() < 0.25:
                return 'raise'
            elif random.random() < 0.12:
                return 'fold'
            else:
                return 'call'
        elif range < 40:
            if random.random() < 0.25:
                return 'call'
            else:
                return 'raise'
        else:
            if random.random() < 0.10:
                return 'call'
            else:
                return 'fold'


ai_action = ai_preflop_action_sb(ai_hand_ranking)
print(ai_action)


# Ask for user action based on AI action
if ai_action == 'call':
    uinp = input('Enter your action (Ch, Ra): ')
elif ai_action == 'raise':
    uinp = input('Enter your action (Ca, 3b, Fo): ')
else:
    print('restart hand')