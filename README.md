# FTL Save Manager

A Python GUI application for managing save files in **FTL: Faster Than Light**, the popular indie space strategy game.

## Overview

FTL Save Manager allows you to easily backup and restore your game progress in FTL: Faster Than Light. The game only supports a single save slot (`continue.sav`), making it impossible to maintain multiple game runs simultaneously. This tool solves that problem by letting you save and load different game states with optional custom descriptions.

## Features

- **Game Launcher**: Launch FTL directly from the save manager with automatic working directory setup
- **Steam Integration**: Launch FTL through Steam using the Steam protocol URL
- **Auto-Maximize Window**: Optional feature to automatically maximize the game window after launch
- **Configurable Game Path**: Easily set and change the game executable path
- **Save Management with Descriptions**: Backup your current game progress with optional custom descriptions
- **One-Click Loading**: Click any save button to instantly load that game state
- **Individual File Deletion**: Delete specific saves with small × buttons
- **Dynamic Interface**: Window automatically resizes based on content
- **Readable Timestamps**: All dates displayed in natural language format
- **Standalone Executable**: No Python installation required for end users
- **Automatic Validation**: Checks for FTL installation and existing save files
- **Safe Operations**: Confirmation dialogs prevent accidental overwrites
- **No Dependencies**: Uses only Python standard library components

## Requirements

- **Windows 10/11**
- **Python 3.13+** (for source code execution)
- **FTL: Faster Than Light** installed and run at least once
- **uv** package manager (optional, for development)

## Installation

1. **Clone or download this repository**
2. **For standalone use**: Simply run `FTL Save Manager.exe` from the `dist/` folder
3. **For development**: Ensure you have Python 3.13+ installed

## Usage

### Running the Application

**Option 1: Standalone Executable (Easiest)**
Simply double-click `FTL Save Manager.exe` located in the `dist/` folder. This executable includes all dependencies and doesn't require Python to be installed.

**Option 2: Direct Python execution**
```bash
python main.py
```

**Option 3: Using uv**
```bash
uv run main.py
```

> **Note**: If you encounter permission errors with uv on Windows, use the direct Python method above.

### How It Works

1. **Launch the application** - It will automatically check for:
   - FTL installation folder: `%USERPROFILE%\Documents\My Games\FasterThanLight`
   - Active save file: `continue.sav`

2. **If validation fails**, you'll see an error dialog explaining what's missing

3. **If validation succeeds**, the main interface opens with:
   - **Game Controls**: Launch FTL directly, via Steam, or change the game executable path
   - **Current Save Info**: Shows when your current game was last saved (readable format)
   - **Save Current Game**: Creates a timestamped backup with optional description
   - **Individual Save Buttons**: Each save displays as a clickable button
   - **Delete Buttons**: Small × buttons next to each save for deletion

### Launching the Game

**Option 1: Launch via Steam (Recommended for Steam users)**
1. Click **"Launch via Steam"** to start FTL through Steam
2. This uses the Steam protocol URL (`steam://rungameid/212680`) to launch the game
3. No configuration needed - works automatically if Steam is installed
4. Ideal for Steam users as it tracks play time and achievements

**Option 2: Direct Launch**
1. Click **"Launch Game"** to start FTL directly from the save manager
2. **First-time setup**: If the game path isn't configured, you'll be prompted to locate the game executable (usually `FTLGame.exe`)
3. The game launches with its installation directory as the working directory for proper resource loading
4. Use **"Change Game Path"** to update the executable location if needed (e.g., after reinstalling)
5. Game path is stored in `config.json` and remembered between sessions

**Maximize Window Feature**
- Check the **"Maximize Window"** checkbox in the Game Controls section to automatically maximize the FTL window after launch
- Works with both launch methods (direct and Steam)
- The application waits up to 30 seconds for the game window to appear, then maximizes it automatically
- Setting is saved in `config.json` and persists between sessions
- Uncheck the box to launch the game normally without maximization

### Saving Your Progress

1. Click **"Save Current Game"**
2. **Optional**: Enter a description for your save (e.g., "Before boss fight", "Good weapon loadout")
3. Your current `continue.sav` is copied to the `saves/` folder with timestamp
4. Format: `continue_YYYY-MM-DD_HH-MM-SS.sav`

### Loading a Previous Save

1. **Simply click any save button** in the list
2. Each button shows:
   - Your custom description (if provided)
   - Readable timestamp (e.g., "Monday, January 15, 2025 at 2:30 PM")
3. Confirm the operation when prompted
4. The selected save overwrites your current `continue.sav`

### Deleting a Save

1. Click the **×** button next to any save
2. Confirm the deletion when prompted
3. The save file and its description are permanently removed

## File Structure

```
ftl_savemanager/
├── dist/
│   └── FTL Save Manager.exe    # Standalone executable (~8.8 MB)
├── main.py                     # Main application source
├── config.json                 # Stores game settings (auto-created)
├── saves/                      # Auto-created folder for save backups
│   ├── continue_2025-01-15_14-30-22.sav
│   ├── continue_2025-01-15_16-45-10.sav
│   ├── descriptions.json       # Save file descriptions
│   └── ...
├── build_exe.bat              # Build script for creating executable
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Expected FTL Installation Path

The application looks for FTL saves in the standard location:
```
%USERPROFILE%\Documents\My Games\FasterThanLight\continue.sav
```

**Example full path:**
```
C:\Users\YourUsername\Documents\My Games\FasterThanLight\continue.sav
```

## Interface Features

### Game Controls Section
- **Launch Game**: Start FTL directly from the save manager using the configured executable path
- **Launch via Steam**: Start FTL through Steam (requires Steam to be installed)
- **Change Game Path**: Update the game executable location for direct launches
- **Maximize Window**: Checkbox to automatically maximize the game window after launch (works with both launch methods)
- **Auto-Configuration**: Prompts for game path on first direct launch if not set
- **Working Directory**: Direct game launches use proper directory for resource loading

### Save File Display
- **With Description**: Shows custom description above the timestamp
- **Without Description**: Shows only the readable timestamp
- **Format Examples**:
  - `"Before final boss\nMonday, January 15, 2025 at 2:30 PM"`
  - `"Monday, January 15, 2025 at 2:30 PM"`

### Dynamic Layout
- **Content-Based Width**: Window width adjusts to fit button content
- **No Minimum Size**: Window can be as small as needed
- **Auto-Resize**: Window automatically resizes when saves are added/removed
- **No Scrollbars**: Clean interface without clutter

## Troubleshooting

### Game Launch Issues
- **Game doesn't start**: Verify the game path is correct using "Change Game Path"
- **Wrong game launches**: Update the executable path to point to the correct `FTLGame.exe`
- **Can't locate game**: Common locations:
  - Steam: `C:\Program Files (x86)\Steam\steamapps\common\FTL Faster Than Light\FTLGame.exe`
  - GOG: `C:\GOG Games\FTL\FTLGame.exe`

### "FTL folder not found" Error
- Ensure FTL: Faster Than Light is installed
- Run FTL at least once to create the save folder
- Check if the game folder exists at the expected path

### "continue.sav file not found" Error
- Start a new game in FTL to create the initial save file
- The game must have an active save to manage

### Permission Issues with uv
- **Recommended solution**: Use `python main.py` instead
- **Root cause**: Windows security policies may prevent uv from creating virtual environments
- **Alternative**: Run terminal as administrator, then try `uv run main.py`
- **Verify Python**: Ensure Python is properly installed and accessible via `python --version`

### Antivirus/Windows Security Warnings
- **Standalone executable**: Windows Defender or antivirus software may flag the executable as suspicious
- **This is normal**: PyInstaller executables often trigger false positives
- **Solution**: Add the `dist/` folder to your antivirus exclusions or approve the file when prompted
- **Alternative**: Use the Python source code directly (`python main.py`)

## Safety Notes

- **Always backup important saves**: While this tool is designed to be safe, always keep important saves backed up
- **Close FTL before switching saves**: Don't modify saves while the game is running
- **Launch after loading**: You can safely launch the game after loading a save
- **Confirmation dialogs**: The app shows confirmation before overwriting your current save
- **Persistent configuration**: Game path and descriptions are stored locally and preserved between sessions

## Game Information

**FTL: Faster Than Light** is a spaceship simulation real-time strategy roguelike game created by Subset Games. The game features permadeath and a single save slot, making save management tools like this particularly useful for players who want to:

- Experiment with different strategies
- Maintain multiple concurrent playthroughs  
- Share interesting game states with friends
- Practice difficult encounters
- Keep saves at key decision points
- Organize saves by ship type or strategy

## Technical Details

### Save File Management
- **Automatic Path Detection**: Works with both Python script and standalone executable
- **JSON Configuration**: Game path, window settings, and descriptions stored in UTF-8 encoded JSON format
- **Error Handling**: Graceful handling of missing files and corrupted data
- **File Validation**: Comprehensive checks before operations
- **Working Directory**: Game launches with proper working directory for resource loading
- **Window Management**: Uses Windows API to detect and maximize the game window automatically

### User Interface
- **tkinter-based**: Uses Python's built-in GUI framework
- **Responsive Design**: Interface adapts to content size
- **Accessible**: Clear labels and confirmation dialogs
- **Professional**: Clean, modern appearance

## License

This tool is provided as-is for personal use. FTL: Faster Than Light is property of Subset Games.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.