# FTL Save Manager

A Python GUI application for managing save files in **FTL: Faster Than Light**, the popular indie space strategy game.

## Overview

FTL Save Manager allows you to easily backup and restore your game progress in FTL: Faster Than Light. The game only supports a single save slot (`continue.sav`), making it impossible to maintain multiple game runs simultaneously. This tool solves that problem by letting you save and load different game states.

## Features

- **Save Management**: Backup your current game progress with timestamped filenames
- **Game Restoration**: Load any previously saved game state back to your active save slot
- **User-Friendly GUI**: Clean, intuitive interface built with tkinter
- **Automatic Validation**: Checks for FTL installation and existing save files
- **Safe Operations**: Confirmation dialogs prevent accidental overwrites
- **No Dependencies**: Uses only Python standard library components

## Requirements

- **Windows 10/11**
- **Python 3.13+**
- **FTL: Faster Than Light** installed and run at least once
- **uv** package manager (optional, but recommended)

## Installation

1. **Clone or download this repository**
2. **Ensure you have Python 3.13+ installed**
3. **Install uv** (if not already installed):
   ```bash
   pip install uv
   ```

## Usage

### Running the Application

**Option 1: Using uv (recommended)**
```bash
uv run main.py
```

**Option 2: Direct Python execution**
```bash
python main.py
```

### How It Works

1. **Launch the application** - It will automatically check for:
   - FTL installation folder: `%USERPROFILE%\Documents\My Games\FasterThanLight`
   - Active save file: `continue.sav`

2. **If validation fails**, you'll see an error dialog explaining what's missing

3. **If validation succeeds**, the main interface opens with:
   - **Current Save Info**: Shows when your current game was last saved
   - **Save Current Game**: Creates a timestamped backup of your current progress
   - **Saved Games List**: Shows all your backed-up saves with timestamps
   - **Load Selected Save**: Restores a selected backup to your active save slot

### Saving Your Progress

1. Click **"Save Current Game"**
2. Your current `continue.sav` is copied to the `saves/` folder with a timestamp
3. Format: `continue_YYYY-MM-DD_HH-MM-SS.sav`

### Loading a Previous Save

1. Select a save from the **Saved Games** list
2. Click **"Load Selected Save"**
3. Confirm the operation when prompted
4. The selected save overwrites your current `continue.sav`

## File Structure

```
ftl_savemanager/
├── main.py                 # Main application
├── saves/                  # Auto-created folder for save backups
│   ├── continue_2025-01-15_14-30-22.sav
│   ├── continue_2025-01-15_16-45-10.sav
│   └── ...
├── pyproject.toml         # Project configuration
└── README.md             # This file
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

## Troubleshooting

### "FTL folder not found" Error
- Ensure FTL: Faster Than Light is installed
- Run FTL at least once to create the save folder
- Check if the game folder exists at the expected path

### "continue.sav file not found" Error
- Start a new game in FTL to create the initial save file
- The game must have an active save to manage

### Permission Issues with uv
- Try running directly with `python main.py`
- Ensure Python is properly installed and in your PATH

## Safety Notes

- **Always backup important saves**: While this tool is designed to be safe, always keep important saves backed up
- **Close FTL before using**: Don't modify saves while the game is running
- **Confirmation dialogs**: The app shows confirmation before overwriting your current save

## Game Information

**FTL: Faster Than Light** is a spaceship simulation real-time strategy roguelike game created by Subset Games. The game features permadeath and a single save slot, making save management tools like this particularly useful for players who want to:

- Experiment with different strategies
- Maintain multiple concurrent playthroughs  
- Share interesting game states with friends
- Practice difficult encounters

## License

This tool is provided as-is for personal use. FTL: Faster Than Light is property of Subset Games.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.
