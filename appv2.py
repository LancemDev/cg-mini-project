from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import time
import math

# Set up the game and Perlin noise for terrain generation
app = Ursina()
noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000))

window.size = (1280, 720)
window.position = Vec2(350,108)

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
    def __init__(self, position, block_type):
        super().__init__(
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

# Initialize player
player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100)
    # position=(0, 50, 0)
)
camera.rotation_x = 30

# Create terrain
min_height = -5
terrain_heights = {}

for x in range(-10, 10):
    for z in range(-10, 10):
        height = noise([x * 0.02, z * 0.02])
        height = math.floor(height * 7.5)
        terrain_heights[(x,z)] = height
        for y in range(height, min_height - 1, -1):
            if y == min_height:
                block = Block((x, y + min_height, z), "bedrock")
            elif y == height:
                block = Block((x, y + min_height, z), "grass")
            elif height - y > 2:
                block = Block((x, y + min_height, z), "stone")
            else:
                block = Block((x, y + min_height, z), "dirt")
                
# Set player's position above the terrain at the center
center_position = (0, 0)  # Adjust this to a nearby location if needed
spawn_height = terrain_heights.get(center_position, 0) + 50  # Spawn a bit above the ground
player.position = (center_position[0], spawn_height+5, center_position[1])

# Defining a boundary to prevent player from getting out of bounds
boundary_thickness = 1
boundary_height = 15
terrain_size = 10

# Left boundary
left_wall = Entity(
    position=(-terrain_size - boundary_thickness, 0, 0),
    model="cube",
    scale=(boundary_thickness + 2, boundary_height, terrain_size * 2),
    color=color.clear,  # Makes it invisible
    collider="box"
)

# Right boundary
right_wall = Entity(
    position=(terrain_size + boundary_thickness, 0, 0),
    model="cube",
    scale=(boundary_thickness + 2, boundary_height, terrain_size * 2),
    color=color.clear,
    collider="box"
)

# Front boundary
front_wall = Entity(
    position=(0, 0, terrain_size + boundary_thickness),
    model="cube",
    scale=(terrain_size * 2 + 2, boundary_height, boundary_thickness + 2),
    color=color.clear,
    collider="box"
)

# Back boundary
back_wall = Entity(
    position=(0, 0, -terrain_size - boundary_thickness),
    model="cube",
    scale=(terrain_size * 2 + 2, boundary_height, boundary_thickness + 1),
    color=color.clear,
    collider="box"
)

# Add a rotating moon with glow effect
moon = Entity(
    model="sphere",
    scale=5,
    position=(0, 50, 0),
    color=color.rgb(200, 200, 255)
)

# Moon glow effect
moon_glow = Entity(
    model="sphere",
    scale=6,
    position=(0, 50, 0),
    color=color.rgba(255, 255, 255, 50)  # Soft semi-transparent white
)

moon_rotation_speed = 0.1

# Stars in the sky
stars = []
for _ in range(500):
    star = Entity(
        model="sphere",
        scale=0.2,
        position=(random.uniform(-50, 50), random.uniform(30, 60), random.uniform(-50, 50)),
        color=color.rgba(255, 255, 255, random.randint(100, 150))
    )
    stars.append(star)

# Shooting stars
def spawn_shooting_star():
    star = Entity(
        model="sphere",
        scale=0.8,
        position=(random.uniform(-50, 50), 60, random.uniform(0, 50)),
        color=color.yellow
    )
    star.animate_position(
        (star.x + random.uniform(-10, 10), star.y - 10, star.z + random.uniform(-10, 10)),
        duration=3
    )
    invoke(destroy, star, delay=2)  # Destroy star after animation completes

# Invoke a shooting star periodically
invoke(spawn_shooting_star, delay=random.uniform(0, 1))

# Day-night cycle variables
day_night_speed = 0.005

# Add Death Star
death_star = Entity(
    model="sphere",
    scale=7,
    position=(30, 35, -30),
    color=color.rgba(0, 0, 0, .85)  # Darker gray for Death Star
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

death_star_rotation_speed = 0.5  # Slower rotation than the moon for subtlety

# Variables for the up-and-down motion
initial_height = 35             # Starting height (same as moon)
lowest_height = -30              # Approximate height of the player
movement_speed = 1             # Speed of the vertical movement
time_offset = 0                 # Offset for the sine wave

# Orbit variables for the circular motion
orbit_radius = 15               # Radius of the circular orbit around the moon
orbit_speed = 0.5               # Speed of rotation
orbit_angle = 0                 # Initial angle

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
    if key == "f":
        window.fullscreen = not window.fullscreen
    if key == "m":
        mouse.visible = not mouse.visible
        mouse.locked = not mouse.locked
    if key == "escape":
        application.quit()
        print("Closing application safely")
        
    
        
instruction_text = Text(
    text = "Left Mouse: Place Block     |    Right Mouse: Delete Block   |   1: Grass    |   2: Dirt     |   3: Stone   |    F: Toggle Fullscreen   |   m: Make mouse visible   |    Esc: Quit",
    position = (0,-0.4),
    origin = (0,0),
    scale = 0.75,
    background = True
)

# Update function for dynamic effects
def update():
    global day_night_speed, time_offset,orbit_angle
    mini_block.texture = block_textures.get(selected_block)
    time_offset += time.dt * movement_speed 
    
    # Rotate the moon
    moon.rotation_y += moon_rotation_speed

    # Rotate the Death Star
    death_star.rotation_y += death_star_rotation_speed
    
    death_star.y = initial_height + math.sin(time_offset) * (initial_height - lowest_height) / 2
    
    orbit_angle += orbit_speed * time.dt       # Increment orbit angle for circular movement
    
    # Circular orbit around the moon
    death_star.x = moon.x + math.cos(orbit_angle) * orbit_radius
    death_star.z = moon.z + math.sin(orbit_angle) * orbit_radius

    # Day-night cycle
    time_of_day = (time.time() * day_night_speed) % 1  # Oscillate between 0 and 1
    color_value = lerp(0.05, 0.8, time_of_day)  # Transition between night and day
    window.color = color.rgb(color_value, color_value, 1)  # Blueish tint for sky

# Run the application
app.run()
