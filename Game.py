import CommonLayers
import cocos
from cocos.scenes.transitions import FadeTRTransition
import pyglet
import sys


class GameController(object):
   """
   """
   default_title = "Cocosoids"
   default_window_width = 1366
   default_window_height = 700
   playLayerClass = CommonLayers.PlayLayer
   
   def __init__(self):
       """ """
       super( GameController, self ).__init__()
       
       self.game_layer = self.playLayerClass()
       self.game_layer.addAsteroids(3)
       self.ui_layer = CommonLayers.UILayer()
       self.ui_layer.add(self.game_layer)
       
       self.game_scene = cocos.scene.Scene(self.ui_layer)

   def start(self):
       """ """
       cocos.director.director.replace(FadeTRTransition(
           self.get_scene(), 2))
       self.game_layer.do(CommonLayers.PlayLayerAction())
       self.game_layer.do(CommonLayers.InteractivePlayLayerAction())
       self.game_layer.addPlayer(CommonLayers.PlayLayer.ownID)

   def get_scene(self):
       """ """
       return self.game_scene


class IntroController(object):
    """
    """
    
    def __init__(self):
        """ """
        super( IntroController, self ).__init__()

        director_width = GameController.default_window_width
        director_height = GameController.default_window_height

        caption = GameController.default_title + ' ' + \
            CommonLayers.PlayLayer.ownID
        window = cocos.director.director.init(
            director_width, director_height,
            caption = caption, fullscreen=False)
        print(window.get_viewport_size())
        
        intro_layer = CommonLayers.PlayLayer()
        intro_layer.anchor_x = director_width * 0.5
        intro_layer.anchor_y = director_height * 0.5
        intro_layer.addAsteroids(3)

        intro_menu = IntroMenu(self)
        intro_layer.add(intro_menu)
        
        self.intro_scene = cocos.scene.Scene(intro_layer)

    def run(self, host=None, port=None):
        """ """
        self.host = host
        self.port = port
        cocos.director.director.set_show_FPS(True)
        cocos.director.director.run (self.intro_scene)

    def on_join_game( self ):
        """ """
        self.on_host_game()

    def on_host_game( self ):
        """ """
        gameController = GameController()
        gameController.start()

    def on_name( self, value ):
        """ """
        self.player_name = value

    def on_quit( self ):
        """ """
        pyglet.app.exit()


class IntroMenu(cocos.menu.Menu):
    """
    """
    def __init__( self, game ):
        """ """
        super( IntroMenu, self ).__init__()
        self.game = game
        self.font_item = {
            'font_name': 'Arial',
            'font_size': 32,
            'bold': True,
            'color': (220, 200, 220, 100),
        }
        self.font_item_selected = {
            'font_name': 'Arial',
            'font_size': 42,
            'bold': True,
            'color': (255, 255, 255, 255),
        }

        menuItems = []
        menuItems.append( cocos.menu.MenuItem('Join Game',
            self.game.on_join_game ) )
        menuItems.append( cocos.menu.MenuItem('Host Game',
            self.game.on_host_game ) )
        menuItems.append( cocos.menu.EntryMenuItem('Name:',
            self.game.on_name,
            CommonLayers.PlayLayer.ownID) )
        menuItems.append( cocos.menu.MenuItem('Quit', self.game.on_quit ) )

        self.create_menu( menuItems )


if __name__ == "__main__":
    controller = IntroController()
    if len(sys.argv) == 2:
        host, port = sys.argv[1].split(":")
        print(host, port)
        controller.run(host, int(port))
    else:
        controller.run()
