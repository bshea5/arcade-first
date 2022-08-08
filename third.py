# Basic arcade shooter

import arcade
import random

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
SCREEN_TITLE: str = "Arcade Space Shooter"
SCALING: float = 1.5


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

        # SpriteList come with update/draw/check behaviors.
        self.enemies_list: arcade.SpriteList | None = None
        self.clouds_list: arcade.SpriteList | None = None

        self.player: arcade.Sprite | None = None

        self.physics_engine: arcade.PhysicsEngineSimple | None = None

        self.setup()

    # Have a seperate setup() for managing multiple levels & re-init'ing.
    def setup(self):
        """Get the game ready!"""

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.enemies_list: arcade.SpriteList = arcade.SpriteList()
        self.clouds_list: arcade.SpriteList = arcade.SpriteList()

        self.player = arcade.Sprite("images/jet.png", SCALING, center_y=self.height / 2)
        self.player.left = 10

        # Spawn new enemy every 0.25s
        arcade.schedule(self.add_enemy, 0.25)

        # Spawn a new cloud every 1s
        arcade.schedule(self.add_cloud, 1.0)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        self.player.update()

        for enemy in self.enemies_list:
            enemy.update()

        for cloud in self.clouds_list:
            cloud.update()

    def on_draw(self):
        """Called whenever you need to draw your window"""

        # Clear the screen and start drawing
        arcade.start_render()
        self.player.draw()
        self.enemies_list.draw()
        self.clouds_list.draw()

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        # First, create the new enemy sprite
        enemy: FlyingSprite = FlyingSprite("images/missile.png", SCALING)

        # Set its position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        enemy.velocity = (random.randint(-20, -5), 0)

        # Add it to the enemies list
        self.enemies_list.append(enemy)

    def add_cloud(self, delta_time: float):
        """Adds a new cloud to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        # First, create the new cloud sprite
        cloud: FlyingSprite = FlyingSprite("images/cloud.png", SCALING)

        # Set its position to a random height and off screen right
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        cloud.velocity = (random.randint(-10, -5), 0)

        # Add it to the enemies list
        self.clouds_list.append(cloud)

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause/Unpause the game
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol in [arcade.key.W, arcade.key.UP]:
            self.player.change_y = 5

        if symbol in [arcade.key.S, arcade.key.DOWN]:
            self.player.change_y = -5

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
