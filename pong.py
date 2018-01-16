# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0]
X = "RIGHT"
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(X):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if X == "RIGHT":
        ball_vel[1] = -random.randrange(60, 180)/60
        ball_vel[0] = random.randrange(120, 240)/60
    else:
        ball_vel[1] = -random.randrange(60, 180)/60
        ball_vel[0] = -random.randrange(120, 240)/60
       


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_vel, ball_pos  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    score1 = 0
    score2 = 0
    paddle1_vel = 0
    paddle2_vel = 0
    for n in range(0,6):
        if n%2==0:
            X = "LEFT"
            spawn_ball(X)
        else: 
            X = "RIGHT"
    spawn_ball(X)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, acc
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Blue")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Blue")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "Blue")
    
     # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "#9B59B6")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if ball_pos[1]<=20:
        ball_vel[1] = -ball_vel[1]
        
    if ball_pos[1]>=380:
        ball_vel[1] = -ball_vel[1]
        
    if ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS):
        if ball_pos[1] > (paddle1_pos + HALF_PAD_HEIGHT) or ball_pos[1] < (paddle1_pos - HALF_PAD_HEIGHT):
            X = "RIGHT"
            spawn_ball(X)
            score2+=1
        else:
            ball_vel[0] =-ball_vel[0] * 1.1
            ball_vel[1] =-ball_vel[1] * 1.1
    
    if ball_pos[0] >= ((WIDTH-PAD_WIDTH) - BALL_RADIUS):
        if ball_pos[1] > (paddle2_pos + HALF_PAD_HEIGHT) or ball_pos[1] < (paddle2_pos - HALF_PAD_HEIGHT):
            X = "LEFT"
            spawn_ball(X)
            score1+=1
        else:
            ball_vel[0] =-ball_vel[0] * 1.1
            ball_vel[1] =-ball_vel[1] * 1.1

    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos+paddle1_vel)<=PAD_HEIGHT/2:
        paddle1_pos = PAD_HEIGHT/2
        paddle1_vel = 0
    if (paddle1_pos+paddle1_vel)>=HEIGHT-PAD_HEIGHT/2:
        paddle1_pos = HEIGHT-PAD_HEIGHT/2
        paddle1_vel = 0
    if (paddle2_pos+paddle2_vel)<=PAD_HEIGHT/2:
        paddle2_pos = PAD_HEIGHT/2
        paddle2_vel = 0
    if (paddle2_pos+paddle2_vel)>=HEIGHT-PAD_HEIGHT/2:
        paddle2_pos = HEIGHT-PAD_HEIGHT/2
        paddle2_vel = 0
        
    paddle1_pos = paddle1_pos+paddle1_vel
    paddle2_pos = paddle2_pos+paddle2_vel   
    
    
    # draw paddles
    canvas.draw_polygon(((0,paddle1_pos-HALF_PAD_HEIGHT),(8,paddle1_pos-HALF_PAD_HEIGHT),(8,paddle1_pos+HALF_PAD_HEIGHT),(0,paddle1_pos+HALF_PAD_HEIGHT)), 4, "#7B241C", "Red")
    canvas.draw_polygon(((WIDTH-PAD_WIDTH,paddle2_pos-HALF_PAD_HEIGHT),(WIDTH,paddle2_pos-HALF_PAD_HEIGHT),(WIDTH,paddle2_pos+HALF_PAD_HEIGHT),(WIDTH-PAD_WIDTH,paddle2_pos+HALF_PAD_HEIGHT)), 4, "#7B241C", "Red")

        
    # determine whether paddle and ball collide    
    
    # draw scores
    if ball_pos[0] < PAD_WIDTH:
        score2+=1
    if ball_pos[0] > (WIDTH-PAD_WIDTH):
        score1+=1
    canvas.draw_text(str(score1), [150, 80], 40, "Black")
    canvas.draw_text(str(score2), [450, 80], 40, "Black")
          
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc=4
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel+=acc
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel-=acc
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel+=acc
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel-=acc
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel=0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel=0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel=0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel=0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("#F5B041")
button = frame.add_button("Restart", new_game, 70)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
