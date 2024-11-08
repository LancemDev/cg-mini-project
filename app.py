# Create terrain
min_height = -5
terrain_heights = {}

for x in range(-10, 10):
    for z in range(-10, 10):
        height = noise([x * 0.02, z * 0.02])
        height = math.floor(height * 7.5)
        terrain_heights[(x, z)] = height
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
center_position = (0, 0)
spawn_height = terrain_heights.get(center_position, 0) + 30
player.position = (center_position[0], spawn_height, center_position[1])

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
    color=color.rgba(255, 255, 255, 50)
)

moon_rotation_speed = 0.1

# Stars in the sky
stars = []
for _ in range(50):
    star = Entity(
        model="sphere",
        scale=0.1,
        position=(random.uniform(-50, 50), random.uniform(30, 60), random.uniform(-50, 50)),
        color=color.rgba(255, 255, 255, random.randint(100, 150))
    )
    stars.append(star)

# Shooting stars
def spawn_shooting_star():
    star = Entity(
        model="sphere",
        scale=0.8,
        position=(random.uniform(-50, 50), 60, random.uniform(-50, 50)),
        color=color.yellow
    )
    star.animate_position(
        (star.x + random.uniform(-10, 10), star.y - 10, star.z + random.uniform(-10, 10)),
        duration=2
    )
    invoke(destroy, star, delay=2)

invoke(spawn_shooting_star, delay=random.uniform(0, 5))
