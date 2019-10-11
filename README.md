# automatic-theme-cinnamon
Automatic light/dark theme switcher for cinnamon 

1. Place this script in a directory where it won't be moved from.
2. Open terminal and navigate inside the directory and run ```./automatic_theme_cinnamon.py --configure``` to fill in your preferences. See 'Preference selection' section below for help with choosing preferences.
3. In the cinnamon application menu search for ```Startup Applications```, press ```+``` and then ```Custom command```. Put ```automatic_theme_cinnamon``` in the name, and ```/path/to/automatic_theme_cinnamon.py --on``` in the command, where /path/to/ is the full path to where you placed the script (don't use env variables like $HOME).

### Preference selection

For seeing the available theme options on your system and to install new theme, search for ```Themes``` in the cinnamon application menu. The categories presented are the same that are queried by the script.

The defaults, if you never configure, are:

###### Dark theme start/end:
- 22:00
- 09:00

###### Light mode configuration:
- Mint-Y
- Mint-Y-Blue
- Mint-Y-Blue
- DMZ-White
- Mint-Y-Blue

###### Dark mode configuration:
- Mint-Y-Dark
- Mint-Y-Blue
- Mint-Y-Dark-Blue
- DMZ-Black
- Mint-Y-Dark-Blue