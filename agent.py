from vector import *
from math import sqrt, pi, exp
from random import random
from geometry import calculateIntersectPoint

class Agent:
    def __init__(self, mass, position, orientation, speed, sight_range, sight_angle, max_speed):
        self.mass = mass
        self.position = position
        self.orientation = orientation / orientation.magnitude()
        self.speed = speed
        self.sight_range = sight_range
        self.sight_angle = sight_angle
        self.max_speed = max_speed
    def velocity(self):
        '''The velocity of the agent'''
        return self.orientation * self.speed
    def inRangeOf(self, other):
        '''Returns True if the other agent is in range of this agent'''
        if(other.isWall()):
            return other.perpDist(self) <= self.sight_range
        else:
            return (self.position - other.position).magnitude() <= self.sight_range
    def isFacing(self, other):
        '''Returns True if the other agent is inside the angle of sight of this agent'''        
        return self.orientation.angleBetween(other.position)*180/pi <= self.sight_angle
    def isHuman(self):
        return False
    def isZombie(self):
        return False
    def isWall(self):
        return False
    def isGunCache(self):
        return False
    def getForce(self, other):
        '''Returns the force extered on this agent by the other agent'''
        return Vector(0,0)
    def getTotalForce(self, others):
        '''Computes the net force on this agent by all other agents'''
        res = Vector(0,0)
        walls = [ o for o in others if o.isWall() and self.inRangeOf(o) ]
        for o in others:
            if self.inRangeOf(o):
                los = True
                for w in walls:
                    if not o.isWall() and w.intersectsWall(self, o):
                        los = False
                        break
##                    if o.isWall():
##                        if w != o and w.intersectsWall(self, o):
##                            los = False
##                            break
##                    else:
##                        if w.intersectsWall(self, o):
##                            los = False
##                            break
                if los:
                    res += self.getForce(o)
        return res
        
    def update(self, force):
        '''Updates the position, orientation, and speed of this agent based on a force'''
        if(self.isHuman() and self.incubating):
            self.health -= .1
        if force.magnitude() != 0.0:    
            a = force / self.mass
            v = (a + self.velocity()).truncate(self.max_speed)
            self.speed = v.magnitude()
            self.orientation = v / self.speed
        self.position += self.velocity()
        

class HumanAgent(Agent):
    def __init__(self, mass, position, orientation, speed, sight_range, sight_angle, max_speed, has_gun, personal_space, incubating, attack_range, damage):
        Agent.__init__(self, mass, position, orientation, speed, sight_range, sight_angle, max_speed)
        self.has_gun = has_gun
        self.personal_space = personal_space
        self.incubating = incubating
        self.health = 100;
        self.attack_range = attack_range
        self.damage = damage
        self.firing = 0
        self.firing_target = Vector(0,0)
    def isHuman(self):
        return True
    def getForce(self, other):
        f = Vector(0,0)
        if self is not other and self.inRangeOf(other): # if they are close enough and not myself
            if other.isHuman():     # if they are human
                dist = (self.position - other.position).magnitude()
                #if dist < self.personal_space:  # if I think they are too close to me
                g = (self.position - other.position) / dist # unit vector points away from other
                if(dist > 0):
                    g *= self.personal_space / dist # increases the more personal space is violated
                f += g
                #elif dist > self.personal_space: # if I think they are too far from me
                if(dist > 0):
                    g = (other.position - self.position) / dist # unit vector points towards self
                g *= dist / self.personal_space # increases the farther they are from me
                f += g
                # handle alignment with superposition
                f += (other.velocity() - self.velocity()) * 0.1 # TODO extract constant
                # handle outside of sight-angle
                if not self.isFacing(other):
                    f *= 0.5 # halve influence TODO extract constant      
            if other.isZombie():
                dist = (self.position - other.position).magnitude()
                if (self.has_gun and not self.firing and dist <= self.sight_range and self.isFacing(other)):
                    accuracy = 6 + dist / (self.sight_range / 4) #adjusts bounds of damage sig function based on distance from target
                    rand = random()*16 - accuracy
                    gunDamage = (1 / (1 + exp(rand))) * 100
                    #print('POW - ', gunDamage, ' Damage')
                    self.firing = 1
                    self.firing_target = other.position
                    other.health -= gunDamage
                if(dist <= self.attack_range and self.isFacing(other)):
                    other.health -= self.damage
                if(dist > 0):
                    g = (self.position - other.position) / dist # unit vector points away from other
                    g *= self.personal_space / dist # increases the more personal space is violated
                f += g
                if not self.isFacing(other) or self.has_gun:
                    f *= 0.5 # halve influence TODO extract constant

            if other.isWall():
                g = Vector(0,0)
                if other.insideBounds(self):
                    dst = other.perpDist(self)
                    temp = other.closestPoint(self, True)
                    temp = temp - self.position
                    #if(temp.magnitude() != 0):
                     #   temp = temp/temp.magnitude()
                    if(dst != 0):
                        x = max(dst, 0.01)
                        g += (temp / dst) * exp(1 / x) * -1
                        #g += (temp / (dst ** 3)) * -1
                        #g += temp * (-30 / dst / dst) 
                f += g
            if other.isGunCache():
                g = Vector(0,0)
                dist = (self.position - other.position).magnitude()
                if not self.has_gun and other.guns > 0: #attracted to the caches if unarmed and the cache is not empty
                    if other.insideBounds(self):
                        self.has_gun = True
                        other.guns = other.guns-1
                    else:
                        g = (other.position - self.position) / dist
                    g *= 150 / dist #increases the closer they are to the cache
                f+=g
                if not self.isFacing(other):
                    f *= 0.5 # halve influence TODO extract constant


        return f

class ZombieAgent(Agent):
    def __init__(self, mass, position, orientation, speed, sight_range, sight_angle, max_speed, personal_space, attack_range, damage):
        Agent.__init__(self, mass, position, orientation, speed, sight_range, sight_angle, max_speed)
        self.personal_space = personal_space
        self.attack_range = attack_range
        self.damage = damage
        self.health = 100
    def isZombie(self):
        return True
    def getForce(self, other):
        f = Vector(0,0)
        if self is not other and self.inRangeOf(other): # if they are close enough and not myself
            if other.isHuman():     # if they are human
                dist = (self.position - other.position).magnitude()
                if(dist <= self.attack_range and self.isFacing(other)):
                    other.incubating = 1;
                    other.health -= self.damage
                #seek human agents, I AM HUNGRY FOR BRAINS
                if(dist > 0):
                    g = (other.position - self.position) / dist # unit vector points towards self
                g *= 150 / dist  # increases the farther they are from me
                f += g
                # handle alignment with superposition
                f += (other.velocity() - self.velocity()) * 0.1 # TODO extract constant
                # handle outside of sight-angle
                if not self.isFacing(other):
                    f *= 0.1 # halve influence TODO extract constant
            if other.isZombie():
                dist = (self.position - other.position).magnitude()
                #if dist < self.personal_space:  # if I think they are too close to me
                if(dist > 0):
                    g = (self.position - other.position) / dist # unit vector points away from other
                    g *= self.personal_space / dist # increases the more personal space is violated
                f += g
                if not self.isFacing(other):
                    f *= 0.5 # halve influence TODO extract constant
            if other.isWall():
                g = Vector(0,0)
                if other.insideBounds(self):
                    dst = other.perpDist(self)
                    temp = other.closestPoint(self, True)
                    temp = temp - self.position
##                    if(temp.magnitude() != 0):
##                        temp = temp/temp.magnitude()
                    if(dst != 0):
                        x = max(dst, 0.01)
                        g += (temp / dst) * exp(1 / x) * -1
                        #g += (temp / (dst ** 3)) * -1
##                        g += temp * (-30 / dst / dst)
                f += g
        return f

class WallAgent(Agent):
    def __init__(self, left_point, right_point, normal):
        Agent.__init__(self, 1, left_point + right_point / 2, normal / normal.magnitude(), 0, 0.0, 0.0, 0)
        self.left_point = left_point
        self.right_point = right_point
        self.normal = normal / normal.magnitude()
    def __eq__(self, other):
        return other.isWall() and \
               self.left_point == other.left_point and \
               self.right_point == other.right_point
    def isWall(self):
        return True
    def onNormalSide(self, other): 
        temp = self.closestPoint(other, 1)
        temp = temp/temp.magnitude()
        temp = temp - other.position
        print(self.normal.angleBetweenAtan(temp)* 180 / pi)
        print(self.normal)
        return abs(self.normal.angleBetween(temp)) < pi
    def insideBounds(self, other):
        inx = self.left_point.x < other.position.x < self.right_point.x or self.left_point.x > other.position.x > self.right_point.x
        iny = self.left_point.y < other.position.y < self.right_point.y or self.left_point.y > other.position.y > self.right_point.y
        return inx or iny
    def perpDist(self, other):
        area = abs((1 / 2) * (self.left_point.x * self.right_point.y + self.right_point.x * other.position.y + other.position.x * self.left_point.y \
                              - self.right_point.x * self.left_point.y - other.position.x * self.right_point.y - self.left_point.x * other.position.y))
        base = (self.left_point - self.right_point).magnitude()
        return area * 2 / base
    def closestPoint(self, other, segmentRestriction):
        dP = other.position - self.left_point
        dB = self.right_point - self.left_point
        t = dP.dotProduct(dB) / dB.dotProduct(dB)
        if(segmentRestriction):
            if(t < 0):
                t = 0;
            elif (t > 1):
                t = 1;
        return self.left_point + dB * t
    def intersectsWall(self, C,D):
        
        p1 = self.left_point.vec2tuple()
        p2 = self.right_point.vec2tuple()
        p3 = C.position.vec2tuple()
        p4 = D.position.vec2tuple()
        x = calculateIntersectPoint(p1,p2,p3,p4)
        if not x:
            return False
        else:
            return True

class GunCacheAgent(Agent):
    def __init__(self, position, guns):
        Agent.__init__(self, 1, position, Vector(1,1), 0.0, 0.0, 0.0, 0.0)
        self.position = position
        #10x10 box when empty; increases in size proportional to the number of guns inside
        self.left_point = Vector(self.position.x-2-guns, self.position.y-2-guns)
        self.right_point = Vector(self.position.x+2+guns, self.position.y+2+guns)
        self.guns = guns
    def isGunCache(self):
        return True
    def insideBounds(self, other):
        inx = self.left_point.x < other.position.x < self.right_point.x or self.left_point.x > other.position.x > self.right_point.x
        iny = self.left_point.y < other.position.y < self.right_point.y or self.left_point.y > other.position.y > self.right_point.y
        return inx and iny
