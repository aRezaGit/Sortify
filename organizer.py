import os
import shutil
from pathlib import Path

# Define file categories and their extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff", ".webp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".dmg", ".apk", ".deb", ".rpm", ".appimage"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".php", ".c", ".ts", ".go", ".rs"]
}

class FileOrganizer:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir)
        if not self.target_dir.exists():
            raise FileNotFoundError(f"The directory {self.target_dir} does not exist.")

    def get_category(self, file_extension):
        """Returns the category name based on the file extension."""
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension.lower() in extensions:
                return category
        return "Others"

    def unique_path(self, path):
        """Generates a unique filename if a file with the same name already exists."""
        if not path.exists():
            return path
        
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 1
        
        while True:
            new_path = parent / f"{stem}_{counter}{suffix}"
            if not new_path.exists():
                return new_path
            counter += 1

    def organize(self):
        """Main method to start organizing files."""
        stats = {cat: 0 for cat in FILE_CATEGORIES}
        stats["Others"] = 0

        # Iterate through all items in the directory
        for item in self.target_dir.iterdir():
            # Skip system files and the script itself
            if item.is_file() and item.name != ".DS_Store" and item.name != "main.py":
                category = self.get_category(item.suffix)
                destination_folder = self.target_dir / category
                
                # Create category folder if it doesn't exist
                destination_folder.mkdir(exist_ok=True)
                
                destination_path = destination_folder / item.name
                
                # Prevent overwriting by getting a unique path
                final_path = self.unique_path(destination_path)
                
                try:
                    shutil.move(str(item), str(final_path))
                    stats[category] += 1
                except Exception as e:
                    print(f"Error moving {item.name}: {e}")
        
        return stats
