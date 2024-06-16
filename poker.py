import random
from handranks import hand_rank2

ranking = hand_rank2.ranking

class Card:
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit
    
    #returns unicode symbol of suit name
    def getSymbol(suit): #sym = ['♥', '♦', '♣', '♠']
        match suit:
            case 'h':
                return '♥'
            case 'd':
                return '♦'
            case 's':
                return '♠'
            case 'c':
                return '♣'   

    face_rank = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

class Deck:
    #generates deck of 52 cards and shuffles them
    def generate_deck():
        faces = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']  
        og_deck = [Card(face, suit) for suit in suits for face in faces]
        random.shuffle(og_deck)  # Shuffle the deck in place
        return og_deck  # Return the shuffled deck

    #chooses two random cards and deals them
    def deal_hole_cards():
        random_card_1 = random.choice(deck)
        deck.remove(random_card_1)
        random_card_2 = random.choice(deck)
        deck.remove(random_card_2)
        return random_card_1, random_card_2
    
    #returns an array containing n community cards
    def deal_card(deck, n):
        flop = random.sample(deck, n)  # Select 3 random cards from the deck
        for card in flop:
            deck.remove(card)  # Remove the selected cards from the deck
        return flop
    
class Hand: #a hand is defined as two cards held by the player
    #returns s if hand is suited, returns o of hand is offsuit
    def isSuited(hand):
        if (hand[0].suit == hand[1].suit):
            return 's'
        elif (hand[0].face == hand[1].face):
            return ''
        else:
            return 'o'
        
    #returns name of hand, eg: J8s AKo
    def name_hand(hand):
        # Ensure the higher face value is first
        if Card.face_rank[hand[0].face] < Card.face_rank[hand[1].face]:
            hand = [hand[1], hand[0]]
        
        # Check if it's a pocket pair
        if hand[0].face == hand[1].face:
            return f"{hand[0].face}{hand[1].face}"
        else:
            so = Hand.isSuited(hand)
            return f"{hand[0].face}{hand[1].face}{so}"
    
    #returns value from ranking dict
    def get_ranking(hand):
        so = Hand.isSuited(hand)
        try:
            return ranking[f"{hand[0].face}{hand[1].face}{so}"]
        except KeyError:
            return ranking[f"{hand[1].face}{hand[0].face}{so}"]
    
    #returns user hand with face and number
    def user_card(hand):
        # Ensure the higher face value is first
        if Card.face_rank[hand[0].face] < Card.face_rank[hand[1].face]:
            hand = [hand[1], hand[0]]
        return f"{hand[0].face}{Card.getSymbol(hand[0].suit)}  {hand[1].face}{Card.getSymbol(hand[1].suit)}"

class Game: 
    #returns what stack size is left (Low, Mid, Deep)
    def get_stacksize():
        if (ai_stack < 10):
            return 'jamtime'
        elif (ai_stack < 20):
            return 'low'
        elif (ai_stack < 50):
            return 'mid'
        else:
            return 'deep'
        
    #entire preflop action, start here after fold
    def preflop():
        #used for when ai is first to act preflop
        def ai_preflop_action_sb(range):
            stacksize = Game.get_stacksize()
            if stacksize == 'low':
                if range < 144:
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
                if range < 130:
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
                if range < 120:
                    if random.random() < 0.25:
                        return 'call'
                    else:
                        return 'raise'
                else:
                    if random.random() < 0.10:
                        return 'call'
                    else:
                        return 'fold'

        #used for when ai is bb and faces a call
        def sb_against_bb_call(range):
            if range < 120:
                return 'raise'
            else:
                return 'check'

        #used for when ai is faced with a preflop raise
        def ai_facing_preflop_raise(range):
            stacksize = Game.get_stacksize()
            cm = .5
            rm = .15
            if stacksize == 'low':
                if 100 <= range <= 140:
                    if random.random() < 0.20:
                        return '3bet'
                    elif random.random() < 0.15:
                        return 'fold'
                    else:
                        return 'call'
                elif range < 100:
                    if random.random() < 0.25:
                        return 'call'
                    else:
                        return '3bet'
                else:
                    if random.random() < 0.30:
                        return 'call'
                    else:
                        return 'fold'
            elif stacksize == 'mid':
                if 90 <= range <= 130:
                    if random.random() < 0.25:
                        return '3bet'
                    elif random.random() < 0.10:
                        return 'fold'
                    else:
                        return 'call'
                elif range < 90:
                    if random.random() < 0.25:
                        return 'call'
                    else:
                        return '3bet'
                else:
                    if random.random() < 0.10:
                        return 'call'
                    else:
                        return 'fold'
            else:
                if 80 <= range <= 120:
                    if random.random() < 0.25:
                        return '3bet'
                    elif random.random() < 0.12:
                        return 'fold'
                    else:
                        return 'call'
                elif range < 80:
                    if random.random() < 0.25:
                        return 'call'
                    else:
                        return '3bet'
                else:
                    if random.random() < 0.10:
                        return 'call'
                    else:
                        return 'fold'

        #used for when ai is faced with a preflop 3bet
        def ai_preflop_facing_3b(range):
            stacksize = Game.get_stacksize()
            match stacksize:
                case 'low':
                    if range < 100:
                        return 'call'
                    else:
                        if random.random() < .2:
                            return 'call'
                        else:
                            return 'fold'       
                case 'mid':
                        if range < 90:
                            return 'call'
                        else:
                            if random.random() < .2:
                                return 'call'
                            else:
                                return 'fold'  
                case 'deep':
                        if range < 80:
                            return 'call'
                        else:
                            if random.random() < .15:
                                return 'call'
                            else:
                                return 'fold'

        global deck, user_stack, ai_stack, bb, sb, pot

        print(user_stack)
        print(ai_stack)

        # generate a new deck for each hand
        deck = Deck.generate_deck()

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
        card1, card2 = Deck.deal_hole_cards()
        global user_cards, ai_cards
        user_cards = [card1, card2]
        card1, card2 = Deck.deal_hole_cards()
        ai_cards = [card1, card2]

        # Print names of hands
        print("You are Dealt:", Hand.name_hand(user_cards))
        print("AI's hand:", Hand.name_hand(ai_cards))
        # Get hand rankings
        user_hand_ranking = Hand.get_ranking(user_cards)
        ai_hand_ranking = Hand.get_ranking(ai_cards)

        print("User's hand ranking:", user_hand_ranking)
        print("AI's hand ranking:", ai_hand_ranking)

        range = ai_hand_ranking

        # 
        match sb:
            case 'u':
                user_action = input('You are first to act (Ca, Ra, Fo): ')
                match user_action:
                    case 'Ca':
                        user_stack -= .5                
                        pot += .5
                        ai_action = sb_against_bb_call(range)
                        match ai_action:
                            case 'check':
                                print('AI Checks')
                                flop()
                            case 'raise':
                                print('AI Raises to 3BB')
                                ai_stack -= 2
                                pot += 2
                                user_action = input('Enter your action (Ca, 3b, Fo): ')
                                if user_action == 'Fo':
                                    print('User folds. Restarting hand...')
                                    print ('------------------------------------------------------------------------------- ')
                                    ai_stack += pot
                                    Game.preflop()
                                elif user_action == 'Ca':
                                    user_stack -= .5                
                                    pot += .5
                                    print('You call')
                                    flop()
                                else:
                                    print('You 3-bet to 9BB')
                                    user_stack -=8.5
                                    pot += 8.5
                                    ai_action = ai_preflop_facing_3b(range)
                                    match ai_action:
                                        case 'call':
                                            print('AI Calls')
                                            ai_stack -= 6
                                            pot += 6
                                            flop()
                                        case 'fold':
                                            print('AI Folds. Restarting hand...')
                                            print ('------------------------------------------------------------------------------- ')
                                            user_stack += pot
                                            preflop
                    case 'Ra':
                        print('You raise to 3BB')
                        user_stack -= 2.5
                        pot += 2.5
                        ai_action = ai_facing_preflop_raise(range)
                        match ai_action:
                            case 'call':
                                ai_stack -= 2
                                pot += 2
                                print('AI Calls')
                                flop()
                            case '3bet':
                                ai_stack -= 8
                                pot += 8
                                user_action = input('AI has 3-Bet to 9BB. What will you do (Ca, Fo)')
                                match user_action:
                                    case 'Ca':
                                        user_stack -= 6
                                        pot += 6
                                        print('You call')
                                        flop()
                                    case 'Fo':
                                        print('You Fold. Restarting Hand...')
                                        print ('------------------------------------------------------------------------------- ')
                                        ai_stack += pot
                                        Game.preflop()
                            case 'fold':
                                print('AI Folds. Restarting Hand...')
                                print ('------------------------------------------------------------------------------- ')
                                user_stack += pot
                                Game.preflop()
                    case 'Fo':
                        print('You Fold. Restarting Hand...')
                        print ('------------------------------------------------------------------------------- ')
                        ai_stack += pot
                        Game.preflop()
            case 'ai':
                ai_action = ai_preflop_action_sb(ai_hand_ranking)
                # Ask for user action based on AI action
                if ai_action == 'call':
                    print('AI calls')
                    user_action = input('Enter your action (Ch, Ra): ')
                    ai_stack -= .5                
                    pot += .5
                    match user_action:
                        case 'Ch':
                            print('You Check')
                            flop()
                        case 'Ra':
                            user_stack -= 2
                            pot += 2
                            ai_action = ai_facing_preflop_raise(range)
                            match ai_action:
                                case 'call':
                                    ai_stack -= 2
                                    pot += 2
                                    print('AI Calls')
                                    flop()
                                case '3bet':
                                    ai_stack -= 8
                                    pot += 8
                                    user_action = input('AI has 3-Bet to 9BB. What will you do (Ca, Fo)')
                                    match user_action:
                                        case 'Ca':
                                            user_stack -= 6
                                            pot += 6
                                            print('You call')
                                            flop()
                                        case 'Fo':
                                            print('You Fold. Restarting Hand...')
                                            print ('------------------------------------------------------------------------------- ')
                                            ai_stack += pot
                                            Game.preflop()
                                case 'fold':
                                    user_stack += pot
                                    print('AI Folds. Restarting hand...')
                                    Game.preflop()
                elif ai_action == 'raise':
                    print('AI raises to 3BB')
                    ai_stack -= 2.5
                    pot += 2.5
                    user_action = input('Enter your action (Ca, 3b, Fo): ')
                    if user_action == 'Fo':
                        print('You folds. Restarting hand...')
                        print ('------------------------------------------------------------------------------- ')
                        ai_stack += pot
                        Game.preflop()
                    elif user_action == 'Ca':
                        user_stack -= 2                
                        pot += 2
                        print('You call')
                        flop()
                    else:
                        print('You 3-bet to 9BB')
                        user_stack -=8.5
                        pot += 8.5
                        ai_action = ai_preflop_facing_3b(range)
                        match ai_action:
                            case 'call':
                                print('AI Calls')
                                ai_stack -= 6
                                pot += 6
                                flop()
                            case 'fold':
                                print('AI Folds. Restarting hand...')
                                print ('------------------------------------------------------------------------------- ')
                                user_stack += pot
                                Game.preflop()
                else:
                    print('AI folds. Restarting hand...')
                    print ('------------------------------------------------------------------------------- ')
                    user_stack += pot
                    Game.preflop()
    def flop():
        #infodump
        print ('Pre-flop Action Over:')
        print ('------------------------------------------------------------------------------- ')
        print('AI Stack: ' + str(ai_stack))
        print('Your Stack: ' + str(user_stack))
        print('Pot: ' + str(pot))
        print ('------------------------------------------------------------------------------- ')
        
        #dealing flop
        flop = Deck.deal_card(deck,3)

        print('Flop Comes: ' + ' '.join(f"{card.face}{Card.getSymbol(card.suit)}" for card in flop))# printing flop cards in one line
        print(f"Your Cards: {Hand.user_card(user_cards)} || AI Cards: {Hand.user_card(ai_cards)}")

        if not Eval.get_hand(flop).endswith('high'):
            print(f"There is an {Eval.get_hand(flop)} on the board")
        
        print(f"AI Hand: {Eval.get_hand(flop + ai_cards)}")

class Eval: 
    #checks for hand if present on board, and if there is a hand when combining AI hole and community cards, checks for draws as well
    def get_hand(cards):
        #returns whether there is a pair, two pair, three of a kind, full house or four of a kind in given list of cards, if nothing, returns false
        def pair_check(cards):
            from collections import Counter
            # Extract face values from Card objects
            faces = [card.face for card in cards]
            
            # Count the occurrences of each face value
            face_counts = Counter(faces)
            
            # Initialize the pair and three-of-a-kind counters
            pair_count = 0
            toak = 0
            foak = 0
            
            # Check the counts
            for count in face_counts.values():
                if count == 2:
                    pair_count += 1
                elif count == 3:
                    toak += 1
                elif count == 4:
                    foak += 1
            
            # Determine the result based on the counts
            if foak == 1:
                return 'four of a kind'
            elif (toak == 1) & (pair_count == 1):
                return 'full house'
            elif toak == 1:
                return 'three of a kind' #works
            elif pair_count == 2:
                return 'two pair' #works
            elif pair_count == 1:
                return 'one pair' #works 
            else:
                return False #works

        def checkFlush(suitlistt):
            class flushacc:
                def __init__(self):
                    self.suit = ''
                    self.cc = 0

            acc = flushacc()
            
            for suit in suitlistt:
                if acc.cc == 5:
                    return True
                elif acc.cc == 0:
                    acc.suit = suit
                    acc.cc += 1
                else:
                    if acc.suit == suit:
                        acc.cc += 1
                    else:
                        acc.cc = 1
                        acc.suit = suit
            return acc.cc == 5
            
        def checkStraight(valList):
            class stracc:
                def __init__(self):
                    self.cc = 0
                    self.num = None

            acc = stracc()
            
            for value in valList:
                if acc.cc == 5:
                    return True
                if acc.num is None or acc.num == value - 1:
                    acc.cc += 1
                    acc.num = value
                elif acc.num == value:
                    # Skip the same number
                    continue
                else:
                    acc.cc = 1
                    acc.num = value
            
            return acc.cc == 5
                    
        def sf_check(cards):
            if len(cards) < 5:
                return
            else:
                #checking for flush
                suitlist = []
                for card in cards:
                    suitlist.append(card.suit)
                if checkFlush(sorted(suitlist)):
                    return 'flush'
                #checking for straight
                ranklist = []
                for card in cards:
                    ranklist.append(Card.face_rank[card.face])
                if checkStraight((sorted(ranklist))):
                    return 'straight'

        def highest_value_face(cards):
            # Sort the cards based on their face rank in descending order
            cards.sort(key=lambda card: Card.face_rank[card.face], reverse=True)
            # Return the face of the highest value card
            return f"{cards[0].face} high"

        if pair_check(cards) != False:
            if (pair_check(cards) != 'full house') and (pair_check(cards) != 'four of a kind') and (sf_check(cards)):
                return sf_check(cards)
            else:
                return pair_check(cards)
        else:
            return highest_value_face(cards)

# Initialize the game by declaring initial stack and blinds
user_stack = 100
ai_stack = 100
bb = ''
sb = ''

# Start the game by calling preflop
Game.preflop()