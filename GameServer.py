"""
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * AUTHOR: Erik M. Buck
 *
 """
import CommonLayers
import cocos
import pyglet

class ServerPlayLayerAction(cocos.actions.Action):
    """ 
    """
    
    def handleLocalKeyboard(self):
        """ """
        if pyglet.window.key.LEFT in self.target.keys_being_pressed:
            self.target.rotatePlayer(self.target.ownID, -5)
        if pyglet.window.key.RIGHT in self.target.keys_being_pressed:
            self.target.rotatePlayer(self.target.ownID, 5)
        if pyglet.window.key.UP in self.target.keys_being_pressed:
            self.target.thrustPlayer(self.target.ownID)

    def step(self, dt):
        """ """
        self.handleLocalKeyboard()
        CommonLayers.GameSprite.handleCollisions()
        self.spawnAsteroids()

    def spawnAsteroids(self):
        """ """
        if not self.target.isWaitingToSpawnAsteroids:
            asteroids = CommonLayers.GameSprite.getInstances(\
                CommonLayers.Asteroid)
            if 0 == len(asteroids):
                self.target.isWaitingToSpawnAsteroids = True
                self.target.do(cocos.actions.Delay(5) + \
                    cocos.actions.CallFuncS(\
                    ServerGamePlayLayer.addAsteroids))


class ServerPlayLayer(CommonLayers.PlayLayer):
    """
    """
    
    def on_key_press(self, key, modifiers):
        """ """
        super( ServerPlayLayer, self ).on_key_press(\
            key, modifiers)
        if pyglet.window.key.SPACE == key:
            self.fireBulletForPlayer(self.ownID)


class ServerGamePlayLayer(ServerPlayLayer):
    """
    """

    def __init__(self):
        """ """
        # Delete all existing asteroids before initializing a new
        # play layer
        asteroids = CommonLayers.GameSprite.getInstances(\
                CommonLayers.Asteroid)
        for asteroid in asteroids:
            asteroid.markForDeath()
        
        super( ServerGamePlayLayer, self ).__init__()
        self.isWaitingToSpawnAsteroids = True

    def addAsteroids(self, count=8):
        """ """
        super( ServerGamePlayLayer, self ).addAsteroids(count)
        self.isWaitingToSpawnAsteroids = False

    def getInfo(self):
        """ """
        return [x.getInfo() for x in
            CommonLayers.GameSprite.live_instances.values()]


class GameServer(object):
    """
    """
    def __init__(self):
        """ """
        super( GameServer, self ).__init__()
        
        self.game_layer = ServerGamePlayLayer()
        self.game_layer.addAsteroids(3)
        self.ui_layer = CommonLayers.UILayer()
        self.ui_layer.add(self.game_layer)
        
        self.game_scene = cocos.scene.Scene(self.ui_layer)

    def start(self):
        """ """
        # setup to handle asynchronous network messages
        self.game_layer.do(ServerPlayLayerAction())
        self.game_layer.addPlayer(\
            CommonLayers.PlayLayer.ownID)

    def get_scene(self):
        """ """
        return self.game_scene


if __name__ == "__main__":
    assert False
