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
LEFT = False
RIGHT = True

paddle1_pos=HEIGHT/2 -HALF_PAD_HEIGHT
paddle2_pos=HEIGHT/2 -HALF_PAD_HEIGHT
paddle_vel=5
paddle1_vel=0
paddle2_vel=0

score1=0
score2=0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left

def spawn_ball(direction):
    global ball_pos, ball_vel 
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    vx=random.randrange(120, 240)/60.0
    vy=random.randrange(60, 180)/60.0
    
    if direction == RIGHT:
        ball_vel = [vx, -vy]    
    if direction == LEFT:        
        ball_vel = [-vx, -vy]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1=0
    score2=0
    
    R=random.randrange(0, 2)
    if R==0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
    
    if ball_pos[1] <= BALL_RADIUS:  
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT-BALL_RADIUS-1: 
        ball_vel[1] = - ball_vel[1]
        
   
    if ball_pos[0] <= BALL_RADIUS+PAD_WIDTH:  
        if ((ball_pos[1]>=paddle1_pos) and (ball_pos[1]<=paddle1_pos+PAD_HEIGHT)):
            ball_vel[0] = - 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            spawn_ball(RIGHT)
            score2+=1

    if ball_pos[0] >= WIDTH-BALL_RADIUS-1-PAD_WIDTH: 
        if ((ball_pos[1]>=paddle2_pos) and (ball_pos[1]<=paddle2_pos+PAD_HEIGHT)):
            ball_vel[0] = - 1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]
        else:
            spawn_ball(LEFT)
            score1+=1

    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos+=paddle1_vel
    paddle2_pos+=paddle2_vel
    
    if paddle1_pos<0:
       paddle1_pos=0
    if paddle1_pos>HEIGHT-PAD_HEIGHT-1:
       paddle1_pos=HEIGHT-PAD_HEIGHT-1
        
    if paddle2_pos<0:
       paddle2_pos=0
    if paddle2_pos>HEIGHT-PAD_HEIGHT-1:
       paddle2_pos=HEIGHT-PAD_HEIGHT-1
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos],[HALF_PAD_WIDTH, paddle1_pos+PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos],[WIDTH - HALF_PAD_WIDTH, paddle2_pos+PAD_HEIGHT], PAD_WIDTH, "White")

    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/2 -40, 20), 24, 'Red')
    canvas.draw_text(str(score2), (WIDTH/2 +26, 20), 24, 'Red')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = -paddle_vel
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle_vel
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel = -paddle_vel
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle_vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if ((key==simplegui.KEY_MAP["up"]) or (key==simplegui.KEY_MAP["down"])):
        paddle2_vel = 0
    elif ((key==simplegui.KEY_MAP["w"]) or (key==simplegui.KEY_MAP["s"])):
        paddle1_vel = 0
        
def reset_handler():
    new_game()   

        

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', reset_handler)


# start frame
new_game()
frame.start()
