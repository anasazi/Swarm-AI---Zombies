import pygame, sys, time
from pygame.locals import *
from random import randint, choice, random
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
RED = (210, 10, 10)
GREEN = (15, 155, 15)
GRAY = (100, 100, 100)

# set up the block data structure
agents = []
agentDots = []
tMAX = 2000
t1 = time.time()


for i in range(170):
    massi = 5
    positioni = Vector(randint(10, 790), randint(10, 790))
    speedi = 2
    max_forcei = 1
    max_speedi = 3
    orientationi = Vector(random()-.5,random()-.5)
    sightAngle = 120
    sightRadius = 50
    tempAgent = HumanAgent(massi, positioni, orientationi, speedi, sightRadius, sightAngle, max_speedi, False, 35.0, 0, 10, 10)
    agents.append(tempAgent)
    tempBall = {'x':positioni.x,'y':positioni.y,'rad':3, 'color':GRAY}
    agentDots.append(tempBall)

for i in range(25):
    massi = 5
    positioni = Vector(randint(10, 790), randint(10, 790))
    speedi = .5
    max_forcei = 1
    max_speedi = 2
    orientationi = Vector(random()-.5,random()-.5)
    sightAngle = 160
    sightRadius = 120
    tempAgent = ZombieAgent(massi, positioni, orientationi, speedi, sightRadius, sightAngle, max_speedi, 25, 10, 10)
    agents.append(tempAgent)
    tempBall = {'x':positioni.x,'y':positioni.y,'rad':3, 'color':GREEN}
    agentDots.append(tempBall)


for w in range(50):    
    l = Vector(random()*750+25,random()*750+25)
    r = Vector(l.x-random()*40,l.y-random()*40)
    n = (r - l).normal()
    n = n / n.magnitude()
    wall = WallAgent(l, r, n)
    agents.append(wall)

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







            

