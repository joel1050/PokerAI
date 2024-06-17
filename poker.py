import random
from handranks import hand_rank2

ranking = hand_rank2.ranking

class Card:
    def __init__(self, face, suit):
        self.face = face
        self.suit = suit
    
    def __repr__(self): #returns string repr of object
        return f"Card({self.face}, {self.suit})"
    
    def __eq__(self, other): #define how the == operator works for the object
        if isinstance(other, Card):
            return self.face == other.face and self.suit == other.suit
        return False
    
    def __hash__(self): 
        return hash((self.face, self.suit))
    
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
             
    #returns user card with face and number
    def user_card(card):
        # Ensure the higher face value is first
        return f"{card.face}{Card.getSymbol(card.suit)}"

    face_rank = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

class Deck:
    #generates deck of 52 cards and shuffles them
    def generate_deck():
        faces = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']  
        og_deck = [Card(face, suit) for suit in suits for face in faces]
        #random.shuffle(og_deck)  # Shuffle the deck in place
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
    def user_hand(hand):
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
                                Game.flop()
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
                                    Game.flop()
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
                                            Game.flop()
                                        case 'fold':
                                            print('AI Folds. Restarting hand...')
                                            print ('------------------------------------------------------------------------------- ')
                                            user_stack += pot
                                            Game.preflop()
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
                                Game.flop()
                            case '3bet':
                                ai_stack -= 8
                                pot += 8
                                user_action = input('AI has 3-Bet to 9BB. What will you do (Ca, Fo)')
                                match user_action:
                                    case 'Ca':
                                        user_stack -= 6
                                        pot += 6
                                        print('You call')
                                        Game.flop()
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
                            Game.flop()
                        case 'Ra':
                            user_stack -= 2
                            pot += 2
                            ai_action = ai_facing_preflop_raise(range)
                            match ai_action:
                                case 'call':
                                    ai_stack -= 2
                                    pot += 2
                                    print('AI Calls')
                                    Game.flop()
                                case '3bet':
                                    ai_stack -= 8
                                    pot += 8
                                    user_action = input('AI has 3-Bet to 9BB. What will you do (Ca, Fo)')
                                    match user_action:
                                        case 'Ca':
                                            user_stack -= 6
                                            pot += 6
                                            print('You call')
                                            Game.flop()
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
                        Game.flop()
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
                                Game.flop()
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
        print(f"Your Cards: {Hand.user_hand(user_cards)} || AI Cards: {Hand.user_hand(ai_cards)}")

        if not Eval.get_hand(flop) == False:
            print(f"There is an {Eval.get_hand(flop)} on the board")
        
        if not Eval.get_hand(flop + ai_cards) == False:
            print(f"AI Hand: {Eval.get_hand(flop + ai_cards)}")
        else:
            Eval.highest_value_face(ai_cards)
        
        print(f"Outs: {Eval.get_outs(flop + ai_cards)}")

class Eval: 
    #returns whether there is a pair, two pair, three of a kind, full house or four of a kind in given list of cards, if nothing, returns false
    hand_ranking = {'high card': 0, 'one pair': 1, 'two pair': 2, 'three of a kind': 3, 'straight': 4, 'flush': 5, 'full house': 6, 'four of a kind': 7}
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
                
    def sf_check(cards):
        def check_flush(suits):
            from collections import Counter
            suit_counts = Counter(suits)
            for count in suit_counts.values():
                if count >= 5:
                    return True
            return False
        
        def check_straight(ranks):
            ranks = sorted(set(ranks))
            if len(ranks) < 5:
                return False
            for i in range(len(ranks) - 4):
                if ranks[i+4] - ranks[i] == 4:
                    return True
            if set([14, 2, 3, 4, 5]).issubset(ranks):
                return True
            return False

        if len(cards) < 5:
            return False

        suits = [card.suit for card in cards]
        ranks = [Card.face_rank[card.face] for card in cards]
        
        if check_flush(suits):
            return 'flush'
        elif check_straight(ranks):
            return 'straight'
        return False

    def highest_value_face(cards):
        # Sort the cards based on their face rank in descending order
        cards.sort(key=lambda card: Card.face_rank[card.face], reverse=True)
        # Return the face of the highest value card
        return f"{cards[0].face} high"

    #checks for hand if present on board, and if there is a hand when combining AI hole and community cards, checks for draws as well
    def get_hand(cards):
        # First, check for full house and four of a kind
        pair_result = Eval.pair_check(cards)
        if pair_result in ['four of a kind', 'full house']:
            return pair_result
        
        # If no full house or four of a kind, check for flushes and straights
        sf_result = Eval.sf_check(cards)
        if sf_result:
            return sf_result
        
        # If no flush or straight, return the result of pair check
        if pair_result:
            return pair_result
        
        return False

    class Outs:
        def __init__(self, hand_type, outs):
            self.hand_type = hand_type 
            self.outs = outs
        def __repr__(self):
            output = [Card.user_card(card) for card in self.outs]
            return f"{self.hand_type},{output})"

    def get_outs(cards):
        # Generate the full deck
        deck = Deck.generate_deck()
        #finds current hand of given cards and sets them to high card if given false
        current_hand = Eval.get_hand(cards)
        if current_hand == False:
            current_hand == 'high card'
        # Remove all input elements from the deck
        deck = [card for card in deck if card not in cards]
        outs_dict = {}
        for card in deck:
            # Create a new list that includes the current card without modifying the original cards list
            new_hand = cards + [card]
            # Get the hand type
            hand_type = Eval.get_hand(new_hand)
            #checks if there is a returned hand, the hand_type is not the same as without the added card, and the the resulting hand type is of greater value than the current hand of the cards without the added card
            if hand_type and hand_type != current_hand and Eval.hand_ranking[current_hand] < Eval.hand_ranking[hand_type]:
                if hand_type not in outs_dict:
                    outs_dict[hand_type] = []
                outs_dict[hand_type].append(card)

        # Convert the dictionary to a list of Outs objects
        outs = [Eval.Outs(hand_type, cards) for hand_type, cards in outs_dict.items()]
        
        return outs

# Initialize the game by declaring initial stack and blinds
user_stack = 100
ai_stack = 100
bb = ''
sb = ''

#for testing: print(Eval.get_outs([Card('A','s'), Card('A','s'), Card('A','h'), Card('4','s'), Card('4','s'), Card('3','s') ]))

# Start the game by calling preflop
Game.preflop()