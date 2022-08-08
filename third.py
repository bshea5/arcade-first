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
        # arcade.schedule(self.add_cloud, 1.0)

    def on_update(self, delta_time: float):
        super().on_update(delta_time)

        for enemy in self.enemies_list:
            enemy.update()

    def on_draw(self):
        """Called whenever you need to draw your window"""

        # Clear the screen and start drawing
        arcade.start_render()
        self.player.draw()
        self.enemies_list.draw()

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


if __name__ == "__main__":
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    print("Starting Game...")
    arcade.run()
