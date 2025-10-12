import ctypes
import json
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk


class FTLSaveManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FTL Save Manager")
        self.root.resizable(True, True)
        # Set up paths
        self.user_home = Path.home()
        self.ftl_folder = self.user_home / "Documents" / "My Games" / "FasterThanLight"
        self.continue_sav_path = self.ftl_folder / "continue.sav"

        # Get the correct script folder for both .py and .exe execution
        if getattr(sys, 'frozen', False):
            # Running as executable (PyInstaller)
            self.script_folder = Path(sys.executable).parent
        else:
            # Running as script
            self.script_folder = Path(__file__).parent

        self.saves_folder = self.script_folder / "saves"
        # Create saves folder if it doesn't exist
        self.saves_folder.mkdir(exist_ok=True)

        # Path for descriptions file
        self.descriptions_file = self.saves_folder / "descriptions.json"
        self.descriptions = self.load_descriptions()

        # Path for config file
        self.config_file = self.script_folder / "config.json"
        self.config = self.load_config()
        
        # Variable for maximize window checkbox
        self.maximize_window_var = tk.BooleanVar(value=self.config.get("maximize_window", False))
        
        # Auto-refresh timer ID
        self.refresh_timer_id = None
        # Check if FTL folder and continue.sav exist
        if not self.check_prerequisites():
            return
        self.setup_ui()
        self.refresh_saves_list()

        # Initial window sizing
        self.update_window_size()
        
        # Start auto-refresh of current save info
        self.start_auto_refresh()

    def check_prerequisites(self):
        """Check if FTL folder and continue.sav exist"""
        if not self.ftl_folder.exists():
            messagebox.showerror(
                "Error",
                f"FTL folder not found!\n\nExpected location:\n{self.ftl_folder}\n\nPlease make sure FasterThanLight is installed and has been run at least once.",
                parent=self.root
            )
            self.root.destroy()
            return False
            self.root.destroy()
            return False
        return True

    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        # Title
        title_label = ttk.Label(main_frame, text="FTL Save Manager", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Game control frame
        game_control_frame = ttk.LabelFrame(main_frame, text="Game Controls", padding="10")
        game_control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        game_control_frame.columnconfigure(0, weight=1)
        game_control_frame.columnconfigure(1, weight=1)
        game_control_frame.columnconfigure(2, weight=1)

        # Launch game button
        launch_button = ttk.Button(game_control_frame, text="Launch Game", command=self.launch_game)
        launch_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        # Launch via Steam button
        launch_steam_button = ttk.Button(game_control_frame, text="Launch via Steam", command=self.launch_via_steam)
        launch_steam_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))

        # Change game path button
        change_path_button = ttk.Button(game_control_frame, text="Change Game Path", command=self.change_game_path)
        change_path_button.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Maximize window checkbox
        maximize_checkbox = ttk.Checkbutton(
            game_control_frame,
            text="Maximize Window",
            variable=self.maximize_window_var,
            command=self.on_maximize_window_changed
        )
        maximize_checkbox.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))

        # Current save section
        current_frame = ttk.LabelFrame(main_frame, text="Current Save", padding="10")
        current_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        current_frame.columnconfigure(1, weight=1)
        ttk.Label(current_frame, text="continue.sav:").grid(row=0, column=0, sticky=tk.W)
        # Show file info - create a label that will be updated
        self.current_save_info_label = ttk.Label(current_frame, text="")
        self.current_save_info_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        self.update_current_save_info()
        # Save current button
        save_button = ttk.Button(current_frame, text="Save Current Game", command=self.save_current)
        save_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        # Simple frame for save buttons - directly in main window
        self.saves_frame = ttk.Frame(main_frame)
        self.saves_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.saves_frame.columnconfigure(0, weight=1)  # Load button column expands
        self.saves_frame.columnconfigure(1, weight=0)  # Delete button column fixed width
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def save_current(self):
        """Save the current continue.sav with a timestamp"""
        try:
            if not self.continue_sav_path.exists():
                messagebox.showerror("Error", "continue.sav file not found!")
                return

            # Ask for optional description
            description = simpledialog.askstring(
                "Save Description",
                "Enter an optional description for this save file:\n(Leave blank for no description)",
                parent=self.root
            )

            # Generate timestamp filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_filename = f"continue_{timestamp}.sav"
            save_path = self.saves_folder / save_filename

            # Copy the file
            shutil.copy2(self.continue_sav_path, save_path)

            # Save description if provided
            if description and description.strip():
                self.descriptions[save_filename] = description.strip()
                self.save_descriptions()

            self.status_var.set(f"Saved: {save_filename}")
            success_msg = f"Game saved as:\n{save_filename}"
            if description and description.strip():
                success_msg += f"\n\nDescription: {description.strip()}"

            # Refresh the list
            self.refresh_saves_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game:\n{str(e)}")
            self.status_var.set("Error saving game")

    def refresh_saves_list(self):
        """Refresh the list of saved games"""
        try:
            # Clear existing buttons
            for widget in self.saves_frame.winfo_children():
                widget.destroy()

            # Get all .sav files from saves folder
            save_files = list(self.saves_folder.glob("*.sav"))
            save_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Sort by modification time, newest first

            # Create buttons for each save file
            if save_files:
                for i, save_file in enumerate(save_files):
                    mod_time = datetime.fromtimestamp(save_file.stat().st_mtime)
                    # More readable date format: "Monday, January 15, 2025 at 2:30 PM"
                    readable_date = mod_time.strftime("%A, %B %d, %Y at %I:%M %p")

                    # Create button text with date and description if available
                    button_text = readable_date
                    if save_file.name in self.descriptions:
                        description = self.descriptions[save_file.name]
                        button_text = f"{description}\n{readable_date}"

                    # Create button that loads this specific save
                    load_button = ttk.Button(
                        self.saves_frame,
                        text=button_text,
                        command=lambda sf=save_file: self.load_save_file(sf)
                    )
                    load_button.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2, padx=(5, 2))

                    # Create small delete button
                    delete_button = ttk.Button(
                        self.saves_frame,
                        text="×",
                        width=3,
                        command=lambda sf=save_file: self.delete_save_file(sf)
                    )
                    delete_button.grid(row=i, column=1, sticky=tk.E, pady=2, padx=(2, 5))
            else:
                # Show message when no saves found
                no_saves_label = ttk.Label(self.saves_frame, text="No saved games found")
                no_saves_label.grid(row=0, column=0, pady=20)

            self.status_var.set(f"Found {len(save_files)} saved games")

            # Update window size to fit new content
            self.update_window_size()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh saves list:\n{str(e)}")
            self.status_var.set("Error refreshing list")

    def load_save_file(self, save_file):
        """Load a specific save file"""
        try:
            if not save_file.exists():
                messagebox.showerror("Error", f"Save file not found: {save_file.name}")
                return

            # Get readable date for confirmation
            mod_time = datetime.fromtimestamp(save_file.stat().st_mtime)
            readable_date = mod_time.strftime("%A, %B %d, %Y at %I:%M %p")

            # Confirm the action
            result = messagebox.askyesno(
                "Confirm Load",
                f"This will overwrite your current game progress.\n\nLoad save:\n{save_file.stem}\nSaved: {readable_date}\n\nAre you sure?"
            )

            if result:
                # Copy selected save to continue.sav
                shutil.copy2(save_file, self.continue_sav_path)

                self.status_var.set(f"Loaded: {save_file.name}")
                messagebox.showinfo("Success", f"Save file loaded successfully!\n\n{save_file.stem}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load save file:\n{str(e)}")
            self.status_var.set("Error loading save")

    def delete_save_file(self, save_file):
        """Delete a specific save file"""
        try:
            if not save_file.exists():
                messagebox.showerror("Error", f"Save file not found: {save_file.name}")
                return

            # Get readable date for confirmation
            mod_time = datetime.fromtimestamp(save_file.stat().st_mtime)
            readable_date = mod_time.strftime("%A, %B %d, %Y at %I:%M %p")

            # Confirm the deletion
            result = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete this save file?\n\n{save_file.stem}\nSaved: {readable_date}\n\nThis action cannot be undone!"
            )

            if result:
                # Delete the file
                save_file.unlink()

                # Remove description if it exists
                if save_file.name in self.descriptions:
                    del self.descriptions[save_file.name]
                    self.save_descriptions()

                self.status_var.set(f"Deleted: {save_file.name}")

                # Refresh the list to remove the deleted file
                self.refresh_saves_list()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete save file:\n{str(e)}")
            self.status_var.set("Error deleting save")

    def update_window_size(self):
        """Update window size to fit content"""
        self.root.update_idletasks()

        # Calculate optimal size based on content
        content_width = self.root.winfo_reqwidth()
        content_height = self.root.winfo_reqheight()

        # Add some padding
        width = content_width + 100
        height = content_height + 50

        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_descriptions(self):
        """Load save file descriptions from JSON file"""
        try:
            if self.descriptions_file.exists():
                with open(self.descriptions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading descriptions: {e}")
            return {}

    def save_descriptions(self):
        """Save descriptions to JSON file"""
        try:
            with open(self.descriptions_file, 'w', encoding='utf-8') as f:
                json.dump(self.descriptions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving descriptions: {e}")

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default config
                default_config = {
                    "game_exe_path": "",
                    "maximize_window": False
                }
                self.save_config(default_config)
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return {"game_exe_path": ""}

    def save_config(self, config=None):
        """Save configuration to JSON file"""
        try:
            if config is None:
                config = self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")

    def browse_game_exe(self):
        """Open file dialog to locate game executable"""
        file_path = filedialog.askopenfilename(
            title="Locate FTL Game Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
            parent=self.root
        )

        if file_path:
            # Convert to Path object and verify it exists
            exe_path = Path(file_path)
            if exe_path.exists() and exe_path.is_file():
                self.config["game_exe_path"] = str(exe_path)
                self.save_config()
                messagebox.showinfo("Success", f"Game path set to:\n{exe_path}")
                return True
            else:
                messagebox.showerror("Error", "Selected file does not exist or is not a valid file.")
                return False
        return False

    def launch_game(self):
        """Launch the game executable"""
        try:
            game_path = self.config.get("game_exe_path", "")

            # Check if path exists in config
            if not game_path or not Path(game_path).exists():
                result = messagebox.askyesno(
                    "Game Path Not Found",
                    "The game executable path is not set or the file cannot be found.\n\nWould you like to locate it now?"
                )

                if result:
                    if not self.browse_game_exe():
                        return
                    game_path = self.config.get("game_exe_path", "")
                else:
                    return

            # Launch the game
            if game_path and Path(game_path).exists():
                self.status_var.set("Launching game...")
                # Set working directory to the game folder
                game_dir = Path(game_path).parent
                subprocess.Popen([game_path], cwd=str(game_dir), shell=True)
                self.status_var.set("Game launched successfully")
                
                # Maximize window if checkbox is checked
                if self.maximize_window_var.get():
                    self.wait_and_maximize_window()
            else:
                messagebox.showerror("Error", "Unable to launch game. Please set a valid game path.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game:\n{str(e)}")
            self.status_var.set("Error launching game")

    def on_maximize_window_changed(self):
        """Handle maximize window checkbox state change"""
        self.config["maximize_window"] = self.maximize_window_var.get()
        self.save_config()
    
    def change_game_path(self):
        """Allow user to change the game executable path"""
        self.browse_game_exe()
    
    def wait_and_maximize_window(self):
        """Wait for the FTL window and maximize it"""
        def maximize_worker():
            try:
                # Wait up to 30 seconds for the window to appear
                for _ in range(60):  # 60 attempts * 0.5 seconds = 30 seconds
                    time.sleep(0.5)
                    hwnd = self.find_window_by_title("FTL: Faster Than Light")
                    if hwnd:
                        # Wait a bit more for the window to fully initialize
                        time.sleep(1)
                        # Maximize the window
                        ctypes.windll.user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE = 3
                        self.status_var.set("Game window maximized")
                        break
            except Exception as e:
                print(f"Error maximizing window: {e}")
        
        # Run in a separate thread to not block the UI
        thread = threading.Thread(target=maximize_worker, daemon=True)
        thread.start()
    
    def find_window_by_title(self, title):
        """Find a window by its title using Windows API"""
        try:
            result_hwnd = [None]  # Use list to allow modification in nested function
            
            # EnumWindows callback
            def enum_callback(hwnd, lparam):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buff = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                        if title in buff.value:
                            result_hwnd[0] = hwnd
                            return False  # Stop enumeration
                return True  # Continue enumeration
            
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
            ctypes.windll.user32.EnumWindows(EnumWindowsProc(enum_callback), 0)
            
            return result_hwnd[0]
        except Exception as e:
            print(f"Error finding window: {e}")
            return None

    def launch_via_steam(self):
        """Launch the game via Steam URL"""
        try:
            steam_url = "steam://rungameid/212680"
            self.status_var.set("Launching game via Steam...")
            subprocess.Popen(["cmd", "/c", "start", steam_url], shell=True)
            self.status_var.set("Game launched via Steam")
            
            # Maximize window if checkbox is checked
            if self.maximize_window_var.get():
                self.wait_and_maximize_window()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game via Steam:\n{str(e)}")
            self.status_var.set("Error launching game via Steam")

    def update_current_save_info(self):
        """Update the current save file information display"""
        try:
            if self.continue_sav_path.exists():
                mod_time = datetime.fromtimestamp(self.continue_sav_path.stat().st_mtime)
                file_info = f"Last modified: {mod_time.strftime('%A, %B %d, %Y at %I:%M %p')}"
            else:
                file_info = "File not found"
            self.current_save_info_label.config(text=file_info)
        except Exception as e:
            print(f"Error updating current save info: {e}")
    
    def start_auto_refresh(self):
        """Start automatic refresh of current save info every 0.5 seconds"""
        self.update_current_save_info()
        # Schedule next refresh in 500ms (0.5 seconds)
        self.refresh_timer_id = self.root.after(500, self.start_auto_refresh)
    
    def stop_auto_refresh(self):
        """Stop the automatic refresh timer"""
        if self.refresh_timer_id is not None:
            self.root.after_cancel(self.refresh_timer_id)
            self.refresh_timer_id = None

    def run(self):
        """Start the application"""
        # Ensure cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing event"""
        self.stop_auto_refresh()
        self.root.destroy()


def main():
    """Main entry point"""
    try:
        app = FTLSaveManager()
        app.run()
    except Exception as e:
        # Handle any unexpected errors
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Fatal Error", f"An unexpected error occurred:\n{str(e)}")


if __name__ == "__main__":
    main()
