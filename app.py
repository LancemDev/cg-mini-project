from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import time

# Set up the game and Perlin noise for terrain generation
app = Ursina()
noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000))
