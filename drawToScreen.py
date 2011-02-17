import pygame, sys, time
from pygame.locals import *
from random import randint, choice, random, sample
from vector import *
#from movingAgent import *
from agent import *
from math import sin, cos, pi
import threading

class Box:
    def __init__(self, thing):
        self.thing = thing
    def alter(self, thing):
        self.thing = thing
    def peek(self):
        return self.thing

class UpdateThread(threading.Thread):
    def __init__(self, agent, everyone, box):
        threading.Thread.__init__(self)
        self.agent = agent
        self.everyone = everyone
        self.box = box
    def run(self):
        self.box.alter(self.agent.getTotalForce(self.everyone))
        



# set up pygame
pygame.init()

#are we rendering to a file?
RENDERTOFILE = 1
FILENAME = 'Outbreak\\'

# set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

# set up direction variables
PIover2 = pi/2
# set up the colors
BLACK = (0, 0, 0)
RED = (170, 100, 100)
GREEN = (15, 155, 15)
GRAY = (100, 100, 100)
BLUE = (0, 128, 255)

# set up the block data structure
agents = []
agentDots = []
tMAX = 3000
t1 = time.time()


##x = HumanAgent(5, Vector(170,150), Vector(1,1), 0.5, 20, 180, 1, False, 35.0, 0, 5, 10)
##agents += [x]
##agentDots += [{'x':180,'y':150,'rad':3,'color':GRAY}]
##
##x = ZombieAgent(5, Vector(220,190), Vector(1,0), 1, 20, 180, 1, 25, 5, 10)
##agents += [x]
##agentDots += [{'x':190,'y':150,'rad':3,'color':GREEN}]

for i in range(140):
    massi = 5
    positioni = Vector(randint(10, 790), randint(10, 790))
    speedi = 2
    max_forcei = 1
    max_speedi = 1
    orientationi = Vector(random()-.5,random()-.5)
    sightAngle = 120
    sightRadius = 100
    tempAgent = HumanAgent(massi, positioni, orientationi, speedi, sightRadius, sightAngle, max_speedi, False, 35.0, 0, 5, 10)
    agents.append(tempAgent)
    tempBall = {'x':positioni.x,'y':positioni.y,'rad':3, 'color':GRAY}
    agentDots.append(tempBall)

for i in range(30):
    massi = 5
    positioni = Vector(randint(10, 790), randint(10, 790))
    speedi = .5
    max_forcei = 1
    max_speedi = .85
    orientationi = Vector(random()-.5,random()-.5)
    sightAngle = 160
    sightRadius = 120
    tempAgent = ZombieAgent(massi, positioni, orientationi, speedi, sightRadius, sightAngle, max_speedi, 25, 10, 10)
    agents.append(tempAgent)
    tempBall = {'x':positioni.x,'y':positioni.y,'rad':3, 'color':GREEN}
    agentDots.append(tempBall)

# initialize the building types
def draw_wall(nums_list, x, y):
    nums_list = nums_list[0]
    for nums in nums_list:
        l = Vector(nums[0]+x, nums[1]+y)
        r = Vector(nums[2]+x, nums[3]+y)
        n = (r - l).normal()
        n = n / n.magnitude()
        wall = WallAgent(l, r, n)
        agents.append(wall)

##agents += [WallAgent(Vector(160,140), Vector(160,180), Vector(1,0))]
##agents += [WallAgent(Vector(230,140), Vector(230,200), Vector(-1,0))]
##agents += [WallAgent(Vector(160,140), Vector(230,140), Vector(0,1))]
##agents += [WallAgent(Vector(160,200), Vector(230,200), Vector(0,-1))]

w1 = [(50, 50, 50,100), (50, 100, 100, 100), (50, 50, 100, 50), (100, 50, 100, 80)]
w2 = [(50, 50, 50,100), (50, 100, 80, 100), (50, 50, 100, 50), (100, 50, 100, 100)]
w3 = [(100, 0, 100, 100)]
w4 = [(0, 100, 100, 100)]
w5 = [(0, 0, 0, 100)]
w6 = [(0, 0, 100, 0)]
w7 = [(25, 25, 25, 40), (25, 40, 40, 40), (25, 25, 40, 25), (85, 65, 65, 85)]
w8 = [(10, 10, 75, 10), (10, 10, 10, 45), (10, 45, 45, 45), (45, 45, 45, 65), (75, 10, 75, 65), (65, 65, 75, 65)]
w9 = [(3, 3, 15, 3), (35, 3, 85, 3), (3, 3, 3, 25), (3, 25, 55, 25), (55, 25, 55, 85), (55, 85, 60, 95), (85, 3, 85, 95),(85, 95, 75, 95)]
w10 = [(25, 10, 25, 45), (25, 45, 5, 45), (5, 45, 5, 75), (5, 75, 35, 75), (65, 75, 85, 75), (85, 75, 85, 45), (85, 45, 45, 45), (45, 45, 45, 10)] 
building_list = [w1, w2, w3, w4, w5, w6, w7, w8, w9, w10]
for x in range(25, 725, 100):
    for y in range(25, 725, 100):
        draw_wall(sample(building_list, 1), x, y)
        
    


#draw outer edges
l = Vector(0,0)
r = Vector(800,0)
n = (r - l).normal()
n = n / n.magnitude()
wall = WallAgent(l, r, n)
agents.append(wall)
l = Vector(800,0)
r = Vector(799,799)
n = (r - l).normal()
n = n / n.magnitude()
wall = WallAgent(l, r, n)
agents.append(wall)
l = Vector(0,800)
r = Vector(800,800)
n = (r - l).normal()
n = n / n.magnitude()
wall = WallAgent(l, r, n)
agents.append(wall)
l = Vector(0,0)
r = Vector(0,800)
n = (r - l).normal()
n = n / n.magnitude()
wall = WallAgent(l, r, n)
agents.append(wall)

for c in range(4):
    pos = Vector(random()*750+25,random()*750+25)
    guns = random()*3
    cache = GunCacheAgent(pos, guns)
    agents.append(cache)

# run the game loop
t = 0
while t < tMAX:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    
    # draw the black background onto the surface
    windowSurface.fill(BLACK)

    
        

    threads = [ UpdateThread(x, agents, Box(0.0)) for x in agents ]
    boxes = [ t.box for t in threads ]
    [ t.start() for t in threads ]
    [ t.join() for t in threads ]

    for i in range(len(agents)):
        agents[i].update(boxes[i].peek())
        if(agents[i].isHuman() and agents[i].incubating):
            b = agentDots[i]
            b['color'] = (15, round((100-agents[i].health)/100 * 155), 15)
        if(agents[i].isWall()):
            pygame.draw.line(windowSurface, (220, 220, 220), agents[i].left_point.vec2tuple(), agents[i].right_point.vec2tuple(), 2)
        if(agents[i].isGunCache()):
            pygame.draw.rect(windowSurface, BLUE, (agents[i].left_point.x, agents[i].left_point.y, 5+agents[i].guns, 5+agents[i].guns ), 0)
        if(agents[i].isHuman() and agents[i].has_gun and not agents[i].incubating):
            a = agentDots[i]
            a['color'] = RED
        if(agents[i].isHuman() and agents[i].has_gun and agents[i].firing):
            pygame.draw.line(windowSurface, (240, 240, 240), agents[i].position.vec2tuple(), agents[i].firing_target.vec2tuple())
            agents[i].firing = 0


    agentLimit = len(agentDots)
    i = 0
    while i < agentLimit:    
        if(agents[i].position.x < 0):
            agents[i].position.x = WINDOWWIDTH
        elif (agents[i].position.x > WINDOWWIDTH):
            agents[i].position.x = 0
        if(agents[i].position.y < 0):
            agents[i].position.y = WINDOWHEIGHT
        elif (agents[i].position.y > WINDOWHEIGHT):
            agents[i].position.y = 0

        b = agentDots[i]
        b['x'] = agents[i].position.x
        b['y'] = agents[i].position.y
        if (agents[i].isHuman() and agents[i].health <= 0):
            print('t:' + str(t) + ' ', agents[i], 'has died and risen as a zombie!')
            agents = agents[:i] + [ZombieAgent(agents[i].mass, agents[i].position, agents[i].orientation, 0.00001, 120, 160, 2, 25, 15, 10)] + agents[i+1:]
            agentDots = agentDots[:i] + [{'x':positioni.x,'y':positioni.y,'rad':3, 'color':GREEN}] + agentDots[i+1:]
        elif (agents[i].isZombie() and agents[i].health <= 0):
            print('t:' + str(t) + ' ', 'The survivors slew ', agents[i]) 
            agents = agents[:i] + agents[i+1:]
            agentDots = agentDots[:i] + agentDots[i+1:]
            i -= 1
            agentLimit -= 1
        else:
            pygame.draw.line(windowSurface, GRAY, (b['x'], b['y']),(b['x']+agents[i].orientation.x*6,b['y']+agents[i].orientation.y*6))
            pygame.draw.circle(windowSurface, b['color'], (round(b['x']), round(b['y'])), b['rad'])
        i += 1
    # draw the window onto the screen
    if(RENDERTOFILE):
        pygame.image.save(windowSurface, FILENAME + str(t)+'.png')
    else:
        pygame.display.update()
        time.sleep(0.02)
    t += 1
pygame.quit()
t2 = time.time()
print('It took ' + str((t2-t1)) + ' per frame: ' + str((t2-t1)/tMAX))
sys.exit()







            

