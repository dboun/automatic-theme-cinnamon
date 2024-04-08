# Automatic theme switch for the linux cinnamon desktop
Automatic light/dark theme switcher for cinnamon. Only needs python3, no other dependencies.

### Setup

##### Edit the configuration

Choose what to show in light theme and what in dark and what time to trigger:

```bash
python3 automatic_theme_cinnamon.py configure
```

Alternatively, manually edit the config at `~/.config/automatic_theme_cinnamon/config` after running once.

### Run simply in the terminal (checks every 30 seconds)

```bash
python3 automatic_theme_cinnamon.py run
```

### Run in the background and autostart on boot (checks every 30 seconds)

```bash
python3 automatic_theme_cinnamon.py install
python3 automatic_theme_cinnamon.py autostart on
python3 automatic_theme_cinnamon.py start
```

It is now installed (at `~/.local/bin/automatic_theme_cinnamon`) so this repo can be removed

### Uninstall if running in the background or boot

```bash
python3 automatic_theme_cinnamon.py stop
python3 automatic_theme_cinnamon.py autostart off
python3 automatic_theme_cinnamon.py uninstall
# Alterinatively, if you don't have this repo anymore:
# ~/.local/bin/automatic_theme_cinnamon stop
# ~/.local/bin/automatic_theme_cinnamon autostart off
# ~/.local/bin/automatic_theme_cinnamon uninstall
```
