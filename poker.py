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

#returns what stack size is left (Low, Mid, Deep)
def get_stacksize():
    if (ai_stack < 20):
        return 'low'
    elif (ai_stack < 50):
        return 'mid'
    else:
        return 'deep'

#used for when ai is first to act preflop
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

def preflop():
    global deck, user_stack, ai_stack, bb, sb, pot

    print(user_stack)
    print(ai_stack)

    # generate a new deck for each hand
    deck = generate_deck()

    # Alternate blinds and subtract from stack
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

    # Deal hole cards
    card1, card2 = hole_cards()
    user_cards = [card1, card2]
    card1, card2 = hole_cards()
    ai_cards = [card1, card2]

    # Print names of hands
    print("You are Dealt:", name_hand(user_cards))
    print("AI's hand:", name_hand(ai_cards))

    # Get hand rankings
    user_hand_ranking = get_ranking(user_cards)
    ai_hand_ranking = get_ranking(ai_cards)

    print("User's hand ranking:", user_hand_ranking)
    print("AI's hand ranking:", ai_hand_ranking)

    range = ai_hand_ranking

    # 
    match sb:
        case 'u':
            user_action = input('You are first to act (Ca, Ra, Fo): ')
            match user_action:
                case 'Ca':
                    print('flop()')#//////////////
                    user_stack -= .5                
                    pot += .5
                case 'Ra':
                    print('You raise to 3BB')
                    user_stack -= 2.5
                    pot += 2.5
                    print('ai_preflop_facing_raise()')#/////////////
                case 'Fo':
                    ai_stack += pot
                    preflop()
        case 'ai':
            ai_action = ai_preflop_action_sb(ai_hand_ranking)
            print("AI's action:", ai_action)
            # Ask for user action based on AI action
            if ai_action == 'call':
                user_action = input('Enter your action (Ch, Ra): ')
                ai_stack -= .5                
                pot += .5
                print('flop()')#//////////////
            elif ai_action == 'raise':
                print('AI raises to 3BB')
                ai_stack -= 2.5
                pot += 2.5
                user_action = input('Enter your action (Ca, 3b, Fo): ')
                if user_action == 'Fo':
                    print('User folds. Restarting hand...')
                    user_stack += pot
                    preflop()
                elif user_action == 'Ca':
                    user_stack -= .5                
                    pot += .5
                    print('flop()')#//////////////
                else:
                    print('You 3-bet to 9BB')
                    user_stack -=8.5
                    pot += 8.5
                    print('ai_preflop_facing_3b()')#/////////////
            else:
                print('AI folds. Restarting hand...')
                preflop()
            

# Initialize the game by declaring initial stack and blinds
user_stack = 100
ai_stack = 100
bb = ''
sb = ''

# Start the game by calling preflop
preflop()