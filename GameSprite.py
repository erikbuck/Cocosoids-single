import cocos
import random


class GameSpriteAction(cocos.actions.Action):
    """
    This class exists to forward the step(dt) method call to the
    receiver's target object. It is a hook that enables targets to
    perform logic each time the display is updated.
    """
    
    def step(self, dt):
        """ """
        self.target.step(dt)


class GameSprite(cocos.sprite.Sprite):
    """
    This class exists to provide several features shared by almost
    every game object.
    
    Each instance has the following:
    A unique identifier
    A motion vector to describe how the instances should move.
    A radius used to detect collisions with other GameSprite
        instances
    A flag, shouldDie, used to signal when the instance should be
    removed from the game.
    
    Instances automatically move according to each instance's
    motion vector. Positions "wrap" meaning that if an instance moves
    off the screen, it reappears on the opposite side of the screen.
    """
    next_unique_id = 1
    live_instances = {} # map unique_id to instance with that id

    @staticmethod
    def handleCollisions():
        """ """
        objects = GameSprite.live_instances.values()
        opjectsCopy = list(objects)
        for object in opjectsCopy:
            for other_object in opjectsCopy:
                if other_object.id != object.id and \
                        object.isHitByCircle(other_object.position,\
                        other_object.radius):
                    object.onCollision(other_object)
    @staticmethod
    def getInstances(klass):
        """ """
        result = []
        for object in GameSprite.live_instances.values():
            if isinstance(object, klass):
                result.append(object)
        return result

    def __init__(self, image, id=None, position=(0, 0), rotation=0,
            scale=1, opacity = 255, color=(255, 255, 255),
            anchor=None):
        """ """
        super( GameSprite, self ).__init__( image, position, rotation,
            scale, opacity, color, anchor)
        if not id:
            self.id = GameSprite.next_unique_id
        else:
            self.id = id
        
        GameSprite.next_unique_id += 1
        self.motion_vector = (0,0)  # No motion by default
        self.radius = 3             # Small default radius
        self.shouldDie = False
        self.type = '_'
        GameSprite.live_instances[self.id] = self

    def start(self):
        """ """
        self.do(GameSpriteAction())
        
    def getInfo(self):
        """ """
        x, y = self.position
        rot_deg = self.rotation
        return {'id':self.id,
            'type':self.type,
            'pos':(int(x), int(y)),
            'rot_deg': int(rot_deg),
            'shouldDie' : self.shouldDie }
    
    def updateWithInfo(self, info):
        """ """
        self.position = info['pos']
        self.rotation = info['rot_deg']
        self.shouldDie = info['shouldDie']
    
    def getVelocityMultiplier(self):
        """ Return a multiplier for use when calculating motion per
            unit time.
        """
        return 1
    
    def setRandomPosition(self):
        width, height = cocos.director.director.get_window_size()
        self.position = (random.random() * width,
            random.random() * height)
    
    def markForDeath(self):
        """ """
        self.shouldDie = True
    
    def isHitByCircle(self, center, radius):
        """ Returns True if and only if the receiver's circle
            calculated using the receiver's position and radius
            overlaps the circle calculated using the center and radius
            arguments to this method.
        """
        total_radius = self.radius + radius
        total_radius_squared = total_radius * total_radius
        x, y = self.position
        delta_x = center[0] - x
        delta_y = center[1] - y
        distance_squared = delta_x * delta_x + delta_y * delta_y
        
        return distance_squared < total_radius_squared

    def processCollision(self, other_object):
        """ Override this method to perform custom logic in response to
        collsions. This implementation does nothing and returns False. """
        return False
    
    def onRespawn(self):
        """ Adds the receiver back into collision detection set after
            receiver has respawned """
        GameSprite.live_instances[self.id] = self
        self.do(GameSpriteAction())
    
    def onCollision(self, other_object):
        """ """
        if self.processCollision(other_object):
            self.markForDeath()

    def step(self, dt):
        """ Perform any updates that should occur after dt seconds
            from the last update.
        """
        if self.shouldDie:
            self.stop()
            self.kill()
                
            if self.id in GameSprite.live_instances:
                del GameSprite.live_instances[self.id];
        else:
            width, height = cocos.director.director.get_window_size()
            dx = self.motion_vector[0] * self.getVelocityMultiplier()
            dy = self.motion_vector[1] * self.getVelocityMultiplier()
            x = self.position[0] + dx * dt
            y = self.position[1] + dy * dt
            
            if x < 0: x += width
            elif x > width: x -= width
            
            if y < 0: y += height
            elif y > height: y -= height
            
            self.position = (x, y)



