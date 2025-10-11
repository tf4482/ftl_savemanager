import shutil
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk


class FTLSaveManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FTL Save Manager")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        # Set up paths
        self.user_home = Path.home()
        self.ftl_folder = self.user_home / "Documents" / "My Games" / "FasterThanLight"
        self.continue_sav_path = self.ftl_folder / "continue.sav"
        self.script_folder = Path(__file__).parent
        self.saves_folder = self.script_folder / "saves"
        # Create saves folder if it doesn't exist
        self.saves_folder.mkdir(exist_ok=True)
        # Check if FTL folder and continue.sav exist
        if not self.check_prerequisites():
            return
        self.setup_ui()
        self.refresh_saves_list()

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
        if not self.continue_sav_path.exists():
            messagebox.showerror(
                "Error",
                f"continue.sav file not found!\n\nExpected location:\n{self.continue_sav_path}\n\nPlease start a game in FTL to create a save file.",
                parent=self.root
            )
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
        main_frame.rowconfigure(2, weight=1)
        # Title
        title_label = ttk.Label(main_frame, text="FTL Save Manager", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        # Current save section
        current_frame = ttk.LabelFrame(main_frame, text="Current Save", padding="10")
        current_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        current_frame.columnconfigure(1, weight=1)
        ttk.Label(current_frame, text="continue.sav:").grid(row=0, column=0, sticky=tk.W)
        # Show file info
        if self.continue_sav_path.exists():
            mod_time = datetime.fromtimestamp(self.continue_sav_path.stat().st_mtime)
            file_info = f"Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            file_info = "File not found"
        ttk.Label(current_frame, text=file_info).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        # Save current button
        save_button = ttk.Button(current_frame, text="Save Current Game", command=self.save_current)
        save_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        # Saved games section
        saves_frame = ttk.LabelFrame(main_frame, text="Saved Games", padding="10")
        saves_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        saves_frame.columnconfigure(0, weight=1)
        saves_frame.rowconfigure(1, weight=1)
        # Refresh button
        refresh_button = ttk.Button(saves_frame, text="Refresh List", command=self.refresh_saves_list)
        refresh_button.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        # Saves listbox with scrollbar
        listbox_frame = ttk.Frame(saves_frame)
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        self.saves_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE)
        self.saves_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.saves_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.saves_listbox.configure(yscrollcommand=scrollbar.set)
        # Load button
        load_button = ttk.Button(saves_frame, text="Load Selected Save", command=self.load_selected_save)
        load_button.grid(row=2, column=0, pady=(10, 0))
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def save_current(self):
        """Save the current continue.sav with a timestamp"""
        try:
            if not self.continue_sav_path.exists():
                messagebox.showerror("Error", "continue.sav file not found!")
                return
            # Generate timestamp filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_filename = f"continue_{timestamp}.sav"
            save_path = self.saves_folder / save_filename
            # Copy the file
            shutil.copy2(self.continue_sav_path, save_path)
            self.status_var.set(f"Saved: {save_filename}")
            messagebox.showinfo("Success", f"Game saved as:\n{save_filename}")
            # Refresh the list
            self.refresh_saves_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game:\n{str(e)}")
            self.status_var.set("Error saving game")

    def refresh_saves_list(self):
        """Refresh the list of saved games"""
        try:
            # Clear the listbox
            self.saves_listbox.delete(0, tk.END)
            # Get all .sav files from saves folder
            save_files = list(self.saves_folder.glob("*.sav"))
            save_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Sort by modification time, newest first
            # Add files to listbox
            for save_file in save_files:
                mod_time = datetime.fromtimestamp(save_file.stat().st_mtime)
                display_name = f"{save_file.stem} ({mod_time.strftime('%Y-%m-%d %H:%M:%S')})"
                self.saves_listbox.insert(tk.END, display_name)
            if not save_files:
                self.saves_listbox.insert(tk.END, "No saved games found")
            self.status_var.set(f"Found {len(save_files)} saved games")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh saves list:\n{str(e)}")
            self.status_var.set("Error refreshing list")

    def load_selected_save(self):
        """Load the selected save file"""
        try:
            selection = self.saves_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a save file to load.")
                return
            # Get all save files again (in same order as displayed)
            save_files = list(self.saves_folder.glob("*.sav"))
            save_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            if not save_files or selection[0] >= len(save_files):
                messagebox.showerror("Error", "Invalid selection or no save files available.")
                return
            selected_file = save_files[selection[0]]
            # Confirm the action
            result = messagebox.askyesno(
                "Confirm Load",
                f"This will overwrite your current game progress.\n\nLoad save file:\n{selected_file.name}\n\nAre you sure?"
            )
            if result:
                # Copy selected save to continue.sav
                shutil.copy2(selected_file, self.continue_sav_path)
                self.status_var.set(f"Loaded: {selected_file.name}")
                messagebox.showinfo("Success", "Save file loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load save file:\n{str(e)}")
            self.status_var.set("Error loading save")

    def run(self):
        """Start the application"""
        self.root.mainloop()


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
