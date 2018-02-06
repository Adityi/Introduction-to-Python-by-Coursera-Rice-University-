# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
pos = [0,0]
vel = [0,0]
started = False
a_rock_group = set([])
a_missile_group = set([])
explosion = set([])



class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_center2 = [135,45]
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if self.thrust is False:
            ship_thrust_sound.pause()
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
        if self.thrust:
            ship_thrust_sound.play()
            canvas.draw_image(self.image,self.image_center2,self.image_size,self.pos,self.image_size,self.angle)
    def get_pos(self):
        return self.pos
    def get_radius(self):
        return self.radius
    def update(self):
        self.angle+=self.angle_vel
        if self.thrust==False:
            self.vel[0]*=0.99
            self.vel[1]*=0.99
            
        self.pos[0]=(self.pos[0]+self.vel[0])%800
        self.pos[1]=(self.pos[1]+self.vel[1])%600
        if not started:
            self.pos = [WIDTH / 2, HEIGHT / 2]
            self.angle = 0
            self.vel = [0, 0]
            
    def shoot(self):
        global a_missile, pos, vel,a_missile_group
        pos[0] = my_ship.pos[0] + angle_to_vector(my_ship.angle)[0]*45
        pos[1] = my_ship.pos[1] + angle_to_vector(my_ship.angle)[1]*45
        vel[0] = my_ship.vel[0] + 6*angle_to_vector(my_ship.angle)[0]
        vel[1] = my_ship.vel[1] + 6*angle_to_vector(my_ship.angle)[1]
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_sound.play()
        a_missile_group.add(a_missile)

        

def keydown(key):
    global fire
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel-=0.05
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel+=0.05
    if simplegui.KEY_MAP["up"]== key:
        my_ship.thrust = True
        my_ship.vel[0] += (-0.99)*my_ship.vel[0]+5*(math.cos(my_ship.angle))
        my_ship.vel[1] += (-0.99)*my_ship.vel[1]+5*(math.sin(my_ship.angle))
    if simplegui.KEY_MAP["space"] == key:
        my_ship.shoot()
        
        
        
def keyup(key):
    global fire
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel+=0.05
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel-=0.05
    if simplegui.KEY_MAP["up"]== key:
        my_ship.thrust = False
    
  
# Sprite class
class Sprite:
    global fire, time
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    def get_pos(self):
        return self.pos
    def get_radius(self):
        return self.radius
    def collide(self,objects):
        if dist(self.pos, objects.get_pos())<self.radius+objects.get_radius():
            return True
        else:
            return False
        
    def draw(self, canvas):
        if self.animated is False:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
        if self.animated:
            sprite_dim = [self.image_center[0] + self.image_size[0] * self.age, self.image_size[1] // 2]
            canvas.draw_image(explosion_image, sprite_dim, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle+=self.angle_vel
        self.pos[0]=(self.pos[0]+self.vel[0])%800
        self.pos[1]=(self.pos[1]+self.vel[1])%600
        self.age+=0.5
        if self.age>self.lifespan:
            #print(self.age)
            #print(self.lifespan)
            return True
        else:
            return False

            
def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score= 0
        lives= 3
        soundtrack.play()
        
def draw(canvas):
    global time,started, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(a_rock_group, canvas)
    process_sprite_group(a_missile_group, canvas)
    process_sprite_group(explosion, canvas)
   
    canvas.draw_text("Lives: "+str(lives), (10,30), 30, "Red")
    if group_collide(a_rock_group, my_ship):
        if lives>=1:
            lives-=1
    if lives==0:
        started = False
        soundtrack.pause()
        canvas.draw_text("GAME OVER", [250,100], 50, "Red")
        
            
    score += group_group_collide(a_rock_group, a_missile_group)
    canvas.draw_text("Score: "+str(score), (670,30), 30, "White")
    # update ship and sprites
    my_ship.update()   
 
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
   
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock_group, a_rock
    a_rock.pos = [random.choice([0,50,100,150,500,550,600]), random.choice([0,50,100,350,400])]
    a_rock.vel = [random.choice([0.5,-0.5,0.25,-0.25]), random.choice([0.5,-0.5,0.25,-0.25])]
    a_rock.angle_vel = random.choice([0.01,0.011, 0.012, 0.013])
    if started:
        a_rock = Sprite(a_rock.pos, a_rock.vel,1, a_rock.angle_vel, asteroid_image, asteroid_info)
        if len(a_rock_group)<12:
            a_rock_group.add(a_rock)
    else:
        a_rock_group = set([])
    
def process_sprite_group(s, canvas):
    for r in list(s):
        r.update()
        if r.update():
            s.remove(r)
        r.draw(canvas)
        
def group_collide(rock_group, my_ship):
    global explosion
    for i in list(rock_group):
        if i.collide(my_ship):
            explosion_int = Sprite(i.get_pos(), [0,0], 0,0,explosion_image, explosion_info, explosion_sound)
            explosion.add(explosion_int)
            rock_group.remove(i)
            return True

def group_group_collide(rock_group,missile_group):
    count = 0
    for missile in list(missile_group):
        if group_collide(rock_group,missile):
            missile_group.remove(missile)
            count += 1
    return count       

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
lable = frame.add_label("Hit SPACE to Shoot, RIGHT and LEFT arrows to turn the ship and UP arrow to accelerate")

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([0,0], [0,0], 2, 0, asteroid_image, asteroid_info)
a_missile = Sprite([0,0],[0,0],0, 0, missile_image,missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
    
timer.start()
frame.start()