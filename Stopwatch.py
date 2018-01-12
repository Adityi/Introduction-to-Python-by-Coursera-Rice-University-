# template for "Stopwatch: The Game"
import simplegui

# define global variables
t = 0
total_correct = 0
total_attemps = 0
D = 0
timeron = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def start_timer():
    global timeron
    timer.start()
    timeron = True
    
    
def reset_t():
    global t
    global total_correct
    global total_attemps
    t=0
    total_correct = 0
    total_attemps = 0
    #print("0/0")
    
def stopt():

    global D
    global total_attemps
    global total_correct
    global timeron
    out = ""
    if timeron is False:
       
        timer.stop()
        pass
    if timeron is True:
       
        timer.stop()
        timeron = False
        total_attemps = total_attemps+1
        if D==0:
            total_correct = total_correct+1
        out = out+str(total_correct)+"/"+str(total_attemps)
        #print (out)
    return out
        
    
    
def format(x):
    global t
    global D
    x=t
    if x<6000:
        A = x//600
        t2 = x-(A*600)
        x = t2
        BC = x/10
        D = t2 - ((BC*10))
        if BC<=9:
            BC = str(0)+str(BC)
    return str(A)+":"+str(BC)+"."+str(D)


def tick():
    global t
    t = t+1
    #print(format(t))
    
# Handler to draw on canvas
def draw(canvas):   
    canvas.draw_text(str(format(t)),(100,110) , 36, "Red")
    canvas.draw_text(str(total_correct)+"/"+str(total_attemps), [240, 20], 25, "White")
    
    

# Create a frame 
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)
frame.set_canvas_background('Orange')

# Register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100,tick)
label = frame.add_label('Stop when last digit (y), i.e. x:xx.y is 0')
label2 = frame.add_label('')

button1 = frame.add_button('Start Timer',start_timer, 100)
button2 = frame.add_button('Stop Timer',stopt, 100)
button3 = frame.add_button('Reset Timer',reset_t, 100)

# Start the frame animation
frame.start()
timer.start()
timer.stop()


