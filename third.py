# Basic arcade shooter

from enum import Enum
from time import sleep
from typing import List
import arcade
import random

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE: str = "Arcade Space Shooter"
SCALING: float = 1.5


class SpritesEnum(str, Enum):
    PLAYER = "player"
    ENEMIES = "enemies"
    CLOUDS = "clouds"


class FlyingSprite(arcade.Sprite):
    """Base class for all flying sprites
    Flying sprites include enemies and clouds
    """

    def update(self):
        """Update the position of the sprite
        When it moves off screen to the left, remove it
        """
        super().update()

        # Remove if off screen
        if self.right < 0:
            self.remove_from_sprite_lists()


class SpaceShooter(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.paused: bool = False
        self.scene: arcade.Scene | None = None

        # SpriteList come with update/draw/check behaviors.
        self.enemies_list: arcade.SpriteList | None = None
        self.clouds_list: arcade.SpriteList | None = None
        self.player: arcade.Sprite | None = None
        self.physics_engine: arcade.PhysicsEngineSimple | None = None
        self.collision_sound: arcade.Sound | None = None
        self.move_up_sound: arcade.Sound | None = None
        self.move_down_sound: arcade.Sound | None = None
        self.background_music: arcade.Sound | None = None
        self.debug: bool = False
        self.setup()

    # Have a seperate setup() for managing multiple levels & re-init'ing.
    def setup(self):
        """Get the game ready!"""

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.paused = False
        self.debug = False

        self.scene = arcade.Scene()

        self.player = arcade.Sprite("images/jet.png", SCALING, center_y=self.height / 2)
        self.player.left = 10

        enemies_list: arcade.SpriteList = arcade.SpriteList()
        clouds_list: arcade.SpriteList = arcade.SpriteList()

        self.scene.add_sprite(SpritesEnum.PLAYER, sprite=self.player)
        self.scene.add_sprite_list(SpritesEnum.ENEMIES, sprite_list=enemies_list)
        self.scene.add_sprite_list(SpritesEnum.CLOUDS, sprite_list=clouds_list)

        # Spawn new enemy every 0.25s
        arcade.schedule(self.add_enemy, 0.25)

        # Spawn a new cloud every 1s
        arcade.schedule(self.add_cloud, 1.0)

        # Load your sounds
        # Sound sources: Jon Fincher
        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.move_up_sound = arcade.load_sound("sounds/Rising_putter.wav")
        self.move_down_sound = arcade.load_sound("sounds/Falling_putter.wav")

        # Load your background music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        arcade.play_sound(
            arcade.load_sound("sounds/Apoxode_-_Electric_1.wav"), looping=True
        )

    def keep_player_in_bounds(self):
        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        # If paused, don't update anything
        if self.paused:
            return

        # enemies_list: arcade.SpriteList = self.scene.get_sprite_list(
        #     SpritesEnum.ENEMIES
        # )
        # Dictionary method to get sprite list in scene
        enemies_list: arcade.SpriteList = self.scene[SpritesEnum.ENEMIES]

        # Check for collisions before updates
        if self.player.collides_with_list(enemies_list):
            arcade.play_sound(self.collision_sound)
            sleep(1)
            arcade.close_window()

        for sprite_list in self.scene.sprite_lists:
            for sprite in sprite_list:
                sprite.set_position = (
                    int(sprite.center_x + sprite.change_x * delta_time),
                    int(sprite.center_y + sprite.change_y * delta_time),
                )
                sprite.update()

        # Keep this after player update.
        self.keep_player_in_bounds()

    def on_draw(self):
        """Called whenever you need to draw your window"""

        # Clear the screen and start drawing
        arcade.start_render()
        self.scene.draw()

        if self.debug:
            self.scene.draw_hit_boxes()

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        if self.paused:
            return

        # First, create the new enemy sprite
        enemy: FlyingSprite = FlyingSprite("images/missile.png", SCALING)

        # Set its position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        enemy.velocity = (random.randint(-15, -5), 0)

        # Add it to the enemies list
        self.scene.add_sprite(SpritesEnum.ENEMIES, sprite=enemy)

    def add_cloud(self, delta_time: float):
        """Adds a new cloud to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        if self.paused:
            return

        # First, create the new cloud sprite
        cloud: FlyingSprite = FlyingSprite(
            "images/cloud.png", SCALING, flipped_horizontally=random.randint(0, 1)
        )

        # Set its position to a random height and off screen right
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        cloud.velocity = (random.randint(-10, -5), 0)

        # Add it to the clouds list
        self.scene.add_sprite(SpritesEnum.CLOUDS, sprite=cloud)

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        ESC: Quit the game
        P: Pause/Unpause the game
        O: Debug
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.ESCAPE:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.O:
            self.debug = not self.debug

        if symbol in [arcade.key.W, arcade.key.UP]:
            self.player.change_y = 5
            arcade.play_sound(self.move_up_sound)

        if symbol in [arcade.key.S, arcade.key.DOWN]:
            self.player.change_y = -5
            arcade.play_sound(self.move_down_sound)

        if symbol in [arcade.key.A, arcade.key.LEFT]:
            self.player.change_x = -5

        if symbol in [arcade.key.D, arcade.key.RIGHT]:
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol in [arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0
        if symbol in [arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0


if __name__ == "__main__":
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    print("Starting Game...")
    arcade.run()
