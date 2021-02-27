import arcade
import logging

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

HALF_SCALE = 0.5
QUARTER_SCALE = 0.25
GAME_SPEED = 1
ENEMY_SPEED_Y = 6
ENEMY_SPEED_X = 0.5
PLAYER_SPEED_Y = 6
PLAYER_SPEED_X = 4
BULLET_SPEED = -1
SCREEN_TITLE = "Game Test"
LOG = logging.getLogger('arcade')

INITIAL_FIRING_INTERVAL = 1.2

class Boss(arcade.Sprite):
    def __init__(self, image_file, scale, bullet_list, time_between_firing):
        super().__init__(image_file, scale)

        self.time_since_last_firing = 0.0
        self.time_between_firing = time_between_firing
        self.bullet_list = bullet_list
        self.direction = 1

    # if hp lower than n percent, increase firing frequency ?

    def on_update(self, delta_time: float = 1/60):
        self.center_x += self.change_x

        if self.left < 0:
            self.left = 0
            self.direction = 2
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
            self.direction = 1

        if self.direction == 1:
            self.change_x = -ENEMY_SPEED_X
        else:
            self.change_x = ENEMY_SPEED_X

        self.time_since_last_firing += delta_time
        if self.time_since_last_firing >= self.time_between_firing:
            self.time_since_last_firing = 0
            bullet = arcade.Sprite("sprite/bullet_128.png",0.1)
            bullet.center_x = self.center_x
            bullet.top = self.bottom
            bullet.color = arcade.csscolor.RED
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)

class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1



class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player = None
        self.my_bullet_list = None    
        self.enemy = None
        self.enemy_bullet_list = None
        self.screen_bullet_list = None
        self.background_layer1 = None
        self.background_layer2 = None
        self.background_layer3 = None
        self.background_layer4 = None

        self.player_ship = None
    
        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

    def setup(self):
        
        logging.basicConfig(level=logging.DEBUG)

        self.player = arcade.SpriteList()
        self.my_bullet_list = arcade.SpriteList()    
        self.enemy = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.screen_bullet_list = arcade.SpriteList()
        self.background_layer1 = arcade.SpriteList()
        self.background_layer2 = arcade.SpriteList()
        self.background_layer3 = arcade.SpriteList()
        self.background_layer4 = arcade.SpriteList()

        menemy = Boss("sprite/boss.png",1,self.enemy_bullet_list,INITIAL_FIRING_INTERVAL)
        menemy.center_x = SCREEN_WIDTH/2
        menemy.center_y = 550
        menemy.angle = 180
        self.enemy.append(menemy)

        self.player_ship = Player("sprite/player.png",QUARTER_SCALE)
        self.player_ship.center_x = SCREEN_WIDTH/2
        self.player_ship.center_y = 100
        self.player.append(self.player_ship)
        
        # ebullet = arcade.Sprite("images/sprite/bullet_128.png",HALF_SCALE)
        # pbullet = arcade.Sprite("images/sprite/bullet_nice.png",HALF_SCALE)

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.enemy.draw()
        self.enemy_bullet_list.draw()
        arcade.draw_text("Score: NaN", 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.player.update()
        self.enemy.on_update(delta_time)

        for bullet in self.enemy_bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.enemy_bullet_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_ship.change_y = PLAYER_SPEED_Y
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_ship.change_x = -PLAYER_SPEED_X
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_ship.change_x = PLAYER_SPEED_X
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_ship.change_y = -PLAYER_SPEED_Y

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_ship.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
            self.player_ship.change_y = 0



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.configure_logging()
    arcade.run()


if __name__ == "__main__":
    main()
