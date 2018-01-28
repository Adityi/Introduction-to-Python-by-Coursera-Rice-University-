# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
player_score = 0
dealer_score = 0
score = 0
message = ""
message2 = ""



# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    def draw2(self, canvas, pos):
        card_loc = (CARD_CENTER[0],CARD_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            
        
# define hand class
class Hand:
    def __init__(self):
        self.value = []
        self.cards = ["a", "b"]

    def __str__(self):
        ans = "Hand contains "
        
        for i in range(len(self.value)):
            ans = ans + str(self.value[i]) + " "
        return ans
            
    def add_card(self, card):
        self.value.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        ace = False
               
        for card in self.value:
            print(card.get_rank())
            hand_value+=VALUES[card.get_rank()]
            if card.get_rank()=="A":
                 ace = True
        if ace == False:
            return hand_value
        else:
            if hand_value+10<=21:
                return hand_value+10
            else:
                return hand_value
            
    def draw(self, canvas, pos1):
        for card in self.value:
            card.draw(canvas, pos1)
            pos1[0] = pos1[0]+80
    def draw2(self, canvas, pos2):  
        for card in self.value:
            card.draw2(canvas, pos2)
    def draw(self, canvas, pos1):
        for card in self.value:
            card.draw(canvas, pos1)
            pos1[0] = pos1[0]+80
        #card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        #canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE)

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                card = Card(s,r)
                
                self.deck.append(card)
                 
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        
        return random.choice(self.deck)
        
    def __str__(self):
        decks = ""
        for i in range(len(self.deck)):
            decks+=str(self.deck[i]) + " "
        return decks
     
#define event handlers for buttons
def deal():
    global player_hand, dealer_hand, player_score, dealer_score, in_play, test_deck, message, message2
    message ="Hit or Stand??"
    test_deck = Deck()
    test_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(test_deck.deal_card())
    player_hand.add_card(test_deck.deal_card())
    player_score = player_hand.get_value()
    print(player_score)
    
    print(player_hand)
    dealer_hand.add_card(test_deck.deal_card())
    dealer_hand.add_card(test_deck.deal_card())
    dealer_score = dealer_hand.get_value()
    print(dealer_score)
    print(dealer_hand)
    
    message2 = ""
    in_play = True

def hit():
    global player_hand, dealer_hand, player_score, dealer_score, in_play, test_deck, score, message, message2,s
    if player_score<21:
        player_hand.add_card(test_deck.deal_card())
        player_score = player_hand.get_value()
        print(player_hand)
        print(player_score)
        if player_score>21:
            message2 = "You have busted!!!"
            message = "New deal??"
            score-=1
            
    if player_score==21:
        message = "New deal??"
        message2 = "You won!!!"
        score+=1
        
        
        
       
def stand():
    global player_hand, dealer_hand, player_score, dealer_score, in_play, test_deck, score, message, message2
    in_play = False
    while dealer_score<17:
        dealer_hand.add_card(test_deck.deal_card())
        dealer_score = dealer_hand.get_value()
        print(dealer_hand)
        print(dealer_score)
    if player_score>dealer_score:
        score+=1
        message2 = "You won!!!"
        message = "New deal??"
       
    elif dealer_score>player_score or dealer_score==player_score:
        message2 = "You lost!!!"
        message = "New deal??"
        score-=1
       

# draw handler    
def draw(canvas):
    global player_hand, dealer_hand
    if in_play:
        dealer_hand.value[0].draw2(canvas,[75,100]) 
    else:
        dealer_hand.value[0].draw(canvas,[75,100])
    for i, card in enumerate(dealer_hand.value[1:]):
        card.draw(canvas,[155+80*i,100])
    player_hand.draw(canvas,[75,300])
    canvas.draw_text("Score: " + str(score), [420, 50],30, "Blue")
    canvas.draw_text("Dealer", [80, 80], 25, "Black")
    canvas.draw_text("Player: "+str(player_score), [80, 250], 25, "Black")
    canvas.draw_text(message, [200, 250],25, "Red")
    canvas.draw_text(message2, [350, 250],25, "Red")
    canvas.draw_text("BLACKJACK", [150, 500], 50, "Maroon")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Pink")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric