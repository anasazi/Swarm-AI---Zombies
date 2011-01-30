from vector import *

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
        return (self.position - other.position).magnitude() <= self.sight_range
    def isFacing(self, other):
        '''Returns True if the other agent is inside the angle of sight of this agent'''
        return abs(self.orientation.angleBetween(other.position)) <= self.sight_angle
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
        for o in others:
            res += self.getForce(o)
        return res
    def update(self, force):
        '''Updates the position, orientation, and speed of this agent based on a force'''
        if(self.isHuman() and self.incubating):
            self.health -= .1
            
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
                if(dist <= self.attack_range and self.isFacing(other)):
                    other.health -= self.damage
                if(dist > 0):
                    g = (self.position - other.position) / dist # unit vector points away from other
                    g *= self.personal_space / dist # increases the more personal space is violated
                f += g
                if not self.isFacing(other):
                    f *= 0.5 # halve influence TODO extract constant
            if other.isWall():
                pass
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
                g *= dist / 10 # increases the farther they are from me
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
                pass #wall code here
        return f

class WallAgent(Agent):
    def __init__(self, left_point, right_point):
        Agent.__init__(self, 1, left_point, right_point - left_point, 0, 0.0, 0.0, 0)
        self.left_point = left_point
        self.right_point = right_point
        temp = left_point - right_point
        self.normal = Vector(-temp.y, temp.x)/ temp.magnitude();
    def isWall(self):
        return True

class GunCacheAgent(Agent):
    def __init__(self, position):
        Agent.__init__(self, position, Vector(0,0), 0.0, 0.0, 0.0, 0.0)
    def isGunCache(self):
        return True
