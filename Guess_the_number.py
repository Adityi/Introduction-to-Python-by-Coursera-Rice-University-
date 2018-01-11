# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

preference = False
num = 0
guesses = 0
# helper function to start and restart the game
def new_game():
    range100()
    
        
# define event handlers for control panel
def range100():
    global preference
    preference=True
    global num
    global guesses
    guesses = 7
    num = random.randrange(0, 100)
    print("New Game. Range is from 0 to 100")
    print ("Number of remaining guesses is 7")
    print("")
    
   

def range1000():
    global preference
    preference=False
    global num
    global guesses
    guesses = 10
    num = random.randrange(0, 1000)
    print("New Game. Range is from 0 to 1000")
    print ("Number of remaining guesses is 10")
    print("")
    
def start_new_game():
    if preference:
        range100()
    else:
        range1000()
    
def input_guess(guess):
    global num
    n = int(guess)
    print("Guess was " + str(n))
    global guesses
    if guesses>1:
        guesses = guesses-1
        print("Number of remaining guesses is " + str(guesses))
        if n>num:
            print("Higher!")
            print("")
        if n<num:
            print("Lower!")
            print("")
        if n==num:
            print("Correct!")
            print( " ")
            start_new_game()
            
            
            
    else: 
        print ("Number of remaining guesses is 0")
        print("you ran out of guesses. The number was " + str(num))
        print("")
        start_new_game()
        
        
          
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)


# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 100)


new_game()



# always remember to check your completed program against the grading rubric
frame.start()

