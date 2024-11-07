# 🎮 Minecraft Clone

A voxel-based world builder created with the Ursina engine, featuring dynamic terrain generation, interactive block manipulation, and atmospheric effects.

## ✨ Features

- 🌍 **Dynamic Terrain Generation**: Procedurally generated landscapes using Perlin noise
- 🏗️ **Block Interaction**: Place and destroy blocks to shape your world
- 🌓 **Day-Night Cycle**: Experience time progression with rotating celestial bodies
- ⭐ **Shooting Stars**: Watch the night sky come alive with periodic meteor showers
- 🎨 **Multiple Block Types**: Choose from various materials to build your creation

## 🎯 Controls

- **Movement**:
  - `W` - Move forward
  - `A` - Move left
  - `S` - Move backward
  - `D` - Move right
  - `Space` - Jump
- **Interaction**:
  - `Left Mouse` - Place block
  - `Right Mouse` - Remove block
- **Block Selection**:
  - `1` - Grass block
  - `2` - Dirt block
  - `3` - Stone block

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Git (for cloning)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/LancemDev/cg-mini-project.git
cd cg-mini-project
```

2. Set up virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Launch the game:
```bash
python app.py
```

## 📁 Project Structure

```
minecraft-clone/
├── app.py              # Main game file
├── assets/            # Game resources
│   ├── models/       # 3D models
│   │   └── block_model.obj
│   └── textures/     # Texture files
├── README.md
└── requirements.txt
```

## 🔧 Technical Requirements

- Python 3.7+
- Ursina Engine
- Perlin Noise Generator
- Modern GPU with OpenGL support

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## 🌟 Acknowledgments

- Ursina Engine community
- Minecraft for inspiration
- All contributors and testers

---
Made with ❤️ by CG-GRP1