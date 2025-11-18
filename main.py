import argparse
import sys
from colorama import init, Fore, Style
from organizer import FileOrganizer

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + "=" * 40)
    print(Fore.YELLOW + "      📂 SORTIFY - File Organizer      ")
    print(Fore.CYAN + "=" * 40 + "\n")

def main():
    print_banner()

    # Setup command line arguments
    parser = argparse.ArgumentParser(description="Organize your messy folders instantly.")
    parser.add_argument("directory", type=str, nargs="?", default=".", help="The path to the directory you want to organize")
    
    args = parser.parse_args()
    target_path = args.directory

    print(f"{Fore.BLUE}Scanning directory: {Style.BRIGHT}{target_path}...\n")

    try:
        organizer = FileOrganizer(target_path)
        stats = organizer.organize()
        
        print(Fore.GREEN + "✅ Organization Complete!\n")
        print(Fore.WHITE + "Summary:")
        total_moved = 0
        for category, count in stats.items():
            if count > 0:
                print(f"  - {category}: {Fore.YELLOW}{count}{Fore.WHITE} files moved")
                total_moved += 1
        
        if total_moved == 0:
            print(Fore.RED + "  No files needed moving.")
            
    except FileNotFoundError:
        print(Fore.RED + "❌ Error: The specified directory does not exist.")
    except Exception as e:
        print(Fore.RED + f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
