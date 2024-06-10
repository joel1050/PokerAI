import random
ranking = {
    'AA': 1,
    'KK': 2,
    'QQ': 3,
    'AKs': 4,
    'JJ': 4,
    'AQs': 5,
    'KQs': 5,
    'AJs': 6,
    'KJs': 7,
    'TT': 7,
    'AKo': 8,
    'ATs': 8,
    'KTs': 9,
    'QJs': 9,
    'QTs': 10,
    '99': 11,
    'JTs': 11,
    'A9s': 12,
    'AQo': 12,
    'KQo': 13,
    '88': 14,
    'K9s': 14,
    'A8s': 15,
    'T9s': 15,
    'Q9s': 16,
    'AJo': 17,
    'J9s': 17,
    '77': 18,
    'A5s': 18,
    'A7s': 19,
    'A4s': 20,
    'KJo': 20,
    'A3s': 21,
    'A6s': 21,
    'QJo': 22,
    '66': 23,
    'K8s': 23,
    'A2s': 24,
    'T8s': 24,
    '98s': 25,
    'J8s': 25,
    'ATo': 26,
    'K7s': 27,
    'Q8s': 27,
    'KTo': 28,
    '55': 28,
    'JTo': 29,
    'QTo': 30,
    '87s': 30,
    '44': 31,
    '22': 32,
    'K6s': 33,
    '97s': 33,
    '76s': 34,
    'K5s': 34,
    'T7s': 35,
    'K3s': 36,
    'K4s': 36,
    'K2s': 37,
    'Q7s': 37,
    '65s': 38,
    '86s': 38,
    'J7s': 39,
    '54s': 40,
    'Q6s': 40,
    '33': 41,
    '75s': 41,
    '96s': 41,
    'Q5s': 42,
    'Q4s': 43,
    '64s': 43,
    'T9o': 44,
    'Q3s': 44,
    'T6s': 45,
    'Q2s': 45,
    'A9o': 46,
    '85s': 47,
    '53s': 47,
    'J6s': 48,
    'J9o': 49,
    'K9o': 49,
    'J5s': 50,
    'Q9o': 50,
    '43s': 51,
    'J4s': 52,
    '74s': 52,
    '95s': 53,
    'J3s': 53,
    '63s': 54,
    'J2s': 54,
    'A8o': 55,
    'T5s': 56,
    '52s': 56,
    '84s': 57,
    'T4s': 57,
    'T3s': 58,
    '42s': 59,
    'T2s': 59,
    '98o': 60,
    'T8o': 60,
    'A5o': 61,
    'A7o': 62,
    '73s': 62,
    'A4o': 63,
    '32s': 63,
    '94s': 64,
    'J8o': 65,
    '93s': 65,
    'T7o': 65,
    'A3o': 66,
    '62s': 66,
    'K8o': 67,
    '92s': 67,
    'A6o': 68,
    'Q8o': 69,
    '87o': 69,
    '83s': 70,
    'A2o': 70,
    '82s': 71,
    '72s': 72,
    '97o': 72,
    'K7o': 73,
    '76o': 73,
    '65o': 74,
    'K6o': 75,
    '54o': 76,
    '86o': 76,
    'K5o': 77,
    '75o': 78,
    'J7o': 78,
    'K4o': 79,
    'Q7o': 79,
    'K2o': 80,
    'K3o': 80,
    '96o': 81,
    '64o': 82,
    'Q6o': 82,
    '53o': 83,
    '85o': 83,
    'T6o': 84,
    '43o': 85,
    'Q5o': 85,
    'Q3o': 86,
    'Q4o': 86,
    'Q2o': 87,
    '74o': 88,
    'J6o': 88,
    '63o': 89,
    'J5o': 89,
    '95o': 90,
    '52o': 91,
    'J4o': 91,
    '42o': 92,
    'J3o': 92,
    'J2o': 93,
    '84o': 94,
    'T5o': 94,
    '32o': 95,
    'T4o': 95,
    '73o': 96,
    'T3o': 96,
    'T2o': 97,
    '62o': 98,
    '94o': 98,
    '92o': 99,
    '93o': 99,
    '83o': 100,
    '72o': 101,
    '82o': 101
}

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


















