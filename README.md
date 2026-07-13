# ShapeWars

A Python-based game project using Pygame.

## Prerequisites

- Python 3.12 or higher
- Package manager: pip (usually included with Python) or uv (a fast alternative: https://github.com/astral-sh/uv)

## Installation

1. **Install Python**: Download and install Python 3.12 or later from the official website: https://www.python.org/downloads/

2. **Clone or download the repository**: Place the project files in a directory on your computer.

3. **Navigate to the project directory**:
   - Open a terminal/command prompt and change to the project directory.

4. **Create a virtual environment** (recommended):
   ```
   python -m venv my_venv
   ```

5. **Activate the virtual environment**:
   - On Windows:
     ```
     my_venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```
     source my_venv/bin/activate
     ```

6. **Install dependencies**:
   - Using pip:
     ```
     pip install pygame==2.6.1 pygame-menu>=4.5.2
     ```
   - Using uv:
     ```
     uv install pygame==2.6.1 pygame-menu>=4.5.2
     ```

## Running the Program

With the virtual environment activated, run:
```
python main.py
```

## Controls

This game uses wasd constrols to move, and has a random chance to trigger an encounter. You can use mouse or keyboard during combat.


## Notes

- The game uses Pygame for graphics and user interface.
- No additional programs are required beyond Python and the listed dependencies.
- The installation process is the same across Windows, Linux, and Mac, except for the virtual environment activation command.

## New Features coming:
- 5 levels with RNG maps
- Abilities for each class
- 1 Boss
- Added action queue in combat
- Better game balance
- Back button in combat menu
- Bug fixes
