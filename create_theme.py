#!/usr/bin/env python3
"""
Theme Creator for RaspyJack
This script helps you create custom themes for the RaspyJack interface.
"""

import json
import os
import sys

def rgb_to_hex(r, g, b):
    """Convert RGB values to hex color."""
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    """Convert hex color to RGB."""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgb({r}, {g}, {b})"
    return hex_color

def get_color_input(color_name):
    """Get RGB color input from user."""
    while True:
        try:
            print(f"\nEnter {color_name} color (RGB values 0-255):")
            r = int(input("Red (0-255): "))
            g = int(input("Green (0-255): "))
            b = int(input("Blue (0-255): "))
            
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                return f"rgb({r}, {g}, {b})"
            else:
                print("Values must be between 0 and 255!")
        except ValueError:
            print("Please enter valid numbers!")

def create_theme():
    """Create a new theme interactively."""
    print("=== RaspyJack Theme Creator ===\n")
    
    theme_name = input("Enter theme name: ").strip()
    if not theme_name:
        print("Theme name cannot be empty!")
        return None
    
    print(f"\nCreating theme: '{theme_name}'")
    print("You'll be asked to enter RGB values for each color component.")
    
    theme = {
        "background": get_color_input("background"),
        "text": get_color_input("text"),
        "highlightText": get_color_input("highlight text"),
        "highlightBg": get_color_input("highlight background"),
        "border": get_color_input("border")
    }
    
    return {theme_name: theme}

def preview_theme(theme):
    """Show a preview of the theme colors."""
    print("\n=== Theme Preview ===")
    for color_name, rgb_value in theme.items():
        print(f"{color_name:15}: {rgb_value}")
    print()

def save_theme(theme, themes_file="themes.json"):
    """Save theme to themes.json file."""
    # Load existing themes
    existing_themes = {}
    if os.path.exists(themes_file):
        try:
            with open(themes_file, 'r') as f:
                existing_themes = json.load(f)
        except:
            print(f"Warning: Could not read existing {themes_file}")
    
    # Add new theme
    existing_themes.update(theme)
    
    # Save themes
    try:
        with open(themes_file, 'w') as f:
            json.dump(existing_themes, f, indent=2)
        print(f"Theme saved to {themes_file}")
        return True
    except Exception as e:
        print(f"Error saving theme: {e}")
        return False

def main():
    """Main function."""
    print("RaspyJack Theme Creator")
    print("=======================")
    
    while True:
        print("\nOptions:")
        print("1. Create new theme")
        print("2. Preview existing themes")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            theme = create_theme()
            if theme:
                theme_name = list(theme.keys())[0]
                theme_data = theme[theme_name]
                
                preview_theme(theme_data)
                
                save = input("Save this theme? (y/n): ").strip().lower()
                if save == 'y':
                    if save_theme(theme):
                        print(f"Theme '{theme_name}' created successfully!")
                    else:
                        print("Failed to save theme!")
                else:
                    print("Theme creation cancelled.")
        
        elif choice == "2":
            if os.path.exists("themes.json"):
                try:
                    with open("themes.json", 'r') as f:
                        themes = json.load(f)
                    
                    print(f"\nFound {len(themes)} themes:")
                    for theme_name in themes.keys():
                        print(f"  - {theme_name}")
                    
                    theme_name = input("\nEnter theme name to preview (or press Enter to skip): ").strip()
                    if theme_name in themes:
                        preview_theme(themes[theme_name])
                    elif theme_name:
                        print(f"Theme '{theme_name}' not found!")
                except Exception as e:
                    print(f"Error reading themes: {e}")
            else:
                print("No themes.json file found!")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main() 