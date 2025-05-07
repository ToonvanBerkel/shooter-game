# 🔫 Simple Shooting Game

A fullscreen 2D top-down shooting game built using Python and Pygame. You control a green square player that shoots bullets at red square enemies. Eliminate all enemies to complete the level!

---

## 🎮 Features

- 🖥️ Fullscreen gameplay experience  
- ⌨️ WASD movement controls  
- 🖱️ Mouse click shooting  
- ❤️ Health bars for player and enemies  
- 🤖 Enemy movement using simple AI (bounce logic)  
- 💥 Bullet collision system with damage  
- 🏁 "Level Complete" screen when all enemies are defeated  
- 📁 Modular code structure (separated logic for player, enemies, levels)

---

## 🕹️ Controls

| Action            | Input              |
|-------------------|--------------------|
| Move Up           | `W`                |
| Move Down         | `S`                |
| Move Left         | `A`                |
| Move Right        | `D`                |
| Shoot Bullet      | Left Mouse Click   |
| Start / Restart   | `SPACE`            |
| Quit Game         | `ESC` / Close Window |

---

## 📁 Folder Structure

shooter-game/
├── Logic/
│ ├── player.py # Player movement logic
│ └── enemy.py # Enemy creation and movement logic
├── levels/
│ └── level1.py # Level 1 enemy loader
├── shooting_game.py # Main game script
├── requirements.txt # Python dependencies
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🚀 Getting Started

### 1. Clone or Download the Project

```bash
git clone https://github.com/your-username/shooter-game.git
cd shooter-game
```

### 2. Install Required Dependencies

```bash
pip install -r requirements.txt
```

If that doesn't work, install Pygame manually:

```bash
pip install pygame
```

### 3. Run the Game

```bash
python shooting_game.py
```

## 🧾 Requirements

- Python 3.10 or later
- Pygame 2.6 or later

## 👨‍💻 Author
Toon van Berkel
💼 toonvb.com
🧠 Software Developer | Creative Technologist | Student

## 📄 License
This project is open-source and free to use under the MIT License.
