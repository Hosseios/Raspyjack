# RaspyJack Theme System

## Overview

The RaspyJack now supports a comprehensive theme system that allows you to easily change the appearance of the interface. You can upload custom theme files and switch between different visual styles.

## How to Use Themes

### 1. Access Theme Menu
- Navigate to: **Options** → **Themes**
- You'll see three options:
  - **Select Theme**: Browse and apply available themes
  - **Upload Themes**: Upload a new themes.json file
  - **Export Current**: Save your current colors as a theme

### 2. Select a Theme
- Choose "Select Theme" to browse available themes
- Use UP/DOWN or LEFT/RIGHT buttons to navigate
- The interface will show a live preview of each theme
- Press the center button to apply the selected theme

### 3. Upload Custom Themes
1. Create a `themes.json` file with your theme definitions
2. Upload it to `/root/Raspyjack/themes.json`
3. Use "Upload Themes" to verify the themes are loaded
4. Use "Select Theme" to apply your custom themes

## Theme File Format

Themes are defined in JSON format. Each theme has the following color properties:

```json
{
  "theme_name": {
    "background": "rgb(15, 15, 26)",
    "text": "rgb(0, 255, 234)",
    "highlightText": "rgb(255, 0, 200)",
    "highlightBg": "rgb(85, 0, 255)",
    "border": "rgb(0, 255, 234)"
  }
}
```

### Color Properties

- **background**: Main background color
- **text**: Regular text color
- **highlightText**: Text color for selected items
- **highlightBg**: Background color for selected items
- **border**: Border color around the interface

### Color Format

Colors can be specified in RGB format:
- `"rgb(red, green, blue)"` where values are 0-255
- Example: `"rgb(0, 255, 0)"` for bright green

## Included Themes

The default `themes.json` includes these themes:

- **cyberpunk**: Neon cyan and magenta
- **hacker**: Classic green on black
- **frost**: Cool blue tones
- **matrix**: Red matrix style
- **retro**: Golden retro colors
- **spacedust**: Purple space theme
- **toxic**: Bright green toxic theme
- **synthwave**: Pink and cyan synthwave
- **noir**: Black and white
- **dragon**: Red dragon theme

## Creating Custom Themes

1. **Start with existing colors**: Use "Export Current" to save your current colors
2. **Modify the exported theme**: Edit the generated theme in themes.json
3. **Create from scratch**: Use the color format above to create new themes
4. **Test your theme**: Upload and apply to see how it looks

## Tips for Good Themes

- **Contrast**: Ensure text is readable against the background
- **Consistency**: Use related colors for a cohesive look
- **Accessibility**: Avoid very bright colors that might be hard to read
- **Testing**: Always test your theme on the actual device

## File Locations

- **Theme file**: `/root/Raspyjack/themes.json`
- **Config file**: `/root/Raspyjack/gui_conf.json`
- **Backup**: Keep a backup of your themes.json file

## Troubleshooting

- **No themes found**: Upload a themes.json file to the correct location
- **Theme not applying**: Check that the JSON format is correct
- **Colors look wrong**: Verify RGB values are between 0-255
- **System not responding**: Restart the RaspyJack interface

## Advanced Usage

### Multiple Theme Files
You can have multiple theme files by renaming them:
- `themes.json` (default)
- `themes_backup.json`
- `themes_custom.json`

### Theme Switching
Themes are applied immediately and saved to the configuration. The system will remember your last selected theme.

### Color Conversion
The system automatically converts between RGB and hex color formats as needed. 