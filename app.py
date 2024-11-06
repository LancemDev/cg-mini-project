from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import time

# Set up the game and Perlin noise for terrain generation
app = Ursina()
noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000))


# Define game variables and textures
selected_block = "grass"
block_textures = {
    "grass": load_texture("assets/textures/groundEarth.png"),
    "dirt": load_texture("assets/textures/groundMud.png"),
    "stone": load_texture("assets/textures/wallStone.png"),
    "bedrock": load_texture("assets/textures/stone07.png")
}
# Define block class
class Block(Entity):
    def _init_(self, position, block_type):
        super()._init_(
            position=position,
            model="assets/models/block_model",
            scale=1,
            origin_y=-0.5,
            texture=block_textures.get(block_type),
            collider="box"
        )
        self.block_type = block_type

# Create block in hand
mini_block = Entity(
    parent=camera,
    model="assets/models/block_model",
    scale=0.2,
    texture=block_textures.get(selected_block),
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -30, -5)
)
Commit Message: "Create Block class for terrain blocks and add in-hand block representation."# Define block class
# Initialize player
player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0)
)



# Shooting stars
def spawn_shooting_star():
    star = Entity(
        model="sphere",
        scale=0.2,
        position=(random.uniform(-50, 50), 60, random.uniform(-50, 50)),
        color=color.yellow
    )
    star.animate_position(
        (star.x + random.uniform(-10, 10), star.y - 10, star.z + random.uniform(-10, 10)),
        duration=2
    )
    invoke(destroy, star, delay=2)  # Destroy star after animation completes

# Invoke a shooting star periodically
invoke(spawn_shooting_star, delay=random.uniform(5, 15))

# Day-night cycle variables
day_night_speed = 0.005

# Add Death Star
death_star = Entity(
    model="sphere",
    scale=7,
    position=(30, 55, -30),
    color=color.rgb(100, 100, 100)  # Darker gray for Death Star
)
death_star.rotation_y = 45  # Tilted for effect

# Death Star trench (simulating the equatorial trench)
trench = Entity(
    parent=death_star,
    model="cube",
    scale=(1, 0.1, 1.1),  # Flattened along the y-axis for a trench effect
    position=(0, 0, 0),
    color=color.rgb(50, 50, 50)  # Darker color for trench contrast
)

death_star_rotation_speed = 0.05  # Slower rotation than the moon for subtlety

# Input handling
def input(key):
    global selected_block
    # Place block
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block)
    # Delete block
    if key == "right mouse down" and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            destroy(mouse.hovered_entity)
    # Change block type
    if key == "1":
        selected_block = "grass"
    if key == "2":
        selected_block = "dirt"
    if key == "3":
        selected_block = "stone"

# Update function for dynamic effects
def update():
    global day_night_speed
    mini_block.texture = block_textures.get(selected_block)
    
    # Rotate the moon
    moon.rotation_y += moon_rotation_speed

    # Rotate the Death Star
    death_star.rotation_y += death_star_rotation_speed

    # Day-night cycle
    time_of_day = (time.time() * day_night_speed) % 1  # Oscillate between 0 and 1
    color_value = lerp(0.05, 0.8, time_of_day)  # Transition between night and day
    window.color = color.rgb(color_value, color_value, 1)  # Blueish tint for sky

# Run the application
app.run()