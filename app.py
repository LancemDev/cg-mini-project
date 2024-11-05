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

# Initialize player
player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0)
)