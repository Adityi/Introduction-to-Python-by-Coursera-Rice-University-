# implementation of card game - Memory

import simplegui
import random

turns = 0
cards = ["A","B","C","D","E","F","G","H"]+["A","B","C","D","E","F","G","H"]
random.shuffle(cards)
position = range(0,16)
click = 0
exposed = [False]*16
turn = 0



# helper function to initialize globals
def new_game():
    global turn,click, exposed, turns
    exposed = [False]*16
    click = 0
    turns = 0# displayed
    label.set_text("Turns = " + str(turns))
    random.shuffle(cards)
    card1 = 0
    card2 = 0
 
# define event handlers
def mouseclick(pos):
    global click , cards, ind, exposed, card1, card2, turns, turn
    #first click gives card1 value and then exposed with that index is true (turn 0 to turn 1)
    #second click gives card2 value and then exposed is true (turn 1 to turn 2)
    #third click checks if two card values are same, if yes, thn exposed stays true and cards
    #remain opened, else, exposed false, cards closed and (turn 2 to turn 0)
    mouseclick = list(pos)
    click = mouseclick[0]//60
    if turn == 0:
        card1 = click
        exposed[click] = True
        print("card1",card1)
        print(exposed)
        turn = 1
    elif turn == 1:
        if not exposed[click]:
            card2 = click
            exposed[click] = True
            turns = turns+1
            turn = 2
            print("card2",card2)
            print(exposed)
        else:
            turn = 1       
        
    elif turn==2:
        if not exposed[click]:
            if cards[card1]!=cards[card2]:
                exposed[card1], exposed[card2] = False, False
                card1 = click
                exposed[click] = True
                turn = 1
            else:
                card1 = click
                exposed[click] = True
                turn = 1   
        else:
            turn =2 
        
    label.set_text("Turns = " + str(turns))
    
               
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in position:
        if exposed[i]:
            canvas.draw_text(cards[i], ((i*60), 95), 60, "Red")
        else:
            canvas.draw_polygon([(i*60,0),((i+1)*60, 0),((i+1)*60, 150), (i*60,150)], 2, "White", "Blue")
        
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 960, 150)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(turns))
frame.set_canvas_background('Pink')
labe2 = frame.add_label("Click on card, and make pairs of same values")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric