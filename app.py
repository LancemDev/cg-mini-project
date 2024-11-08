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

# Input handling
def input(key):
    global selected_block
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block)
    if key == "right mouse down" and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            destroy(mouse.hovered_entity)
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
    text="Left Mouse: Place Block | Right Mouse: Delete Block | 1: Grass | 2: Dirt | 3: Stone | F: Toggle Fullscreen | m: Make mouse visible | Esc: Quit",
    position=(0, -0.4),
    origin=(0, 0),
    scale=0.75,
    background=True
)

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

# Update function for dynamic effects
def update():
    global day_night_speed
    mini_block.texture = block_textures.get(selected_block)
    
    moon.rotation_y += moon_rotation_speed
    death_star.rotation_y += death_star_rotation_speed

    time_of_day = (time.time() * day_night_speed) % 1
    color_value = lerp(0.05, 0.8, time_of_day)
    window.color = color.rgb(color_value, color_value, 1)

# Run the application
app.run()
