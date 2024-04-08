#!/usr/bin/python3

import os, sys, subprocess, shutil, argparse, json, time
from pathlib import Path
from datetime import datetime

DEFAULT_CONFIG = {
	'time': {
		'start': '22:00',
		'end': '09:00'
	},
	'light': {
		'Mouse Pointer': 'DMZ-White',
		'Applications': 'Mint-Y-Blue',
		'Icons': 'Mint-Y-Blue',
		'Desktop': 'Mint-Y-Blue',
	},
	'dark': {
		'Mouse Pointer': 'DMZ-White',
		'Applications': 'Mint-Y-Dark-Blue',
		'Icons': 'Mint-Y-Blue',
		'Desktop': 'Mint-Y-Dark-Blue',
	},
}

PATH_HOME = Path.home().resolve()
PATH_CONFIG_FILE = PATH_HOME / '.config' / 'automatic_theme_cinnamon' / 'config'
PATH_AUTOSTART_FILE = PATH_HOME / '.config' / 'autostart' / 'automatic_theme_cinnamon.desktop'
PATH_THIS_FILE = Path(__file__).resolve()
PATH_INSTALL_FILE = PATH_HOME / '.local' / 'bin' / 'automatic_theme_cinnamon'

### Spanning multiple lines
AUTOSTART_FILE_CONTENT = f"""[Desktop Entry]
Version=1.0
Name=Automatic Theme Cinnamon
Exec={PATH_INSTALL_FILE} run
Type=Application
Categories=Utility;
X-GNOME-Autostart-enabled=true
"""

########################
### Helper functions ###
########################

def __find_number_of_other_instances_of_this_script() -> int:
	## Get all processes with the name automatic_theme
	procs = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
	procs = [proc for proc in procs.splitlines() if 'automatic_theme' in proc]
	return len(procs)-1 # -1 to account for current process

def __is_time_string_earlier_than(tstr1, tstr2) -> bool:
	''' Check if a time string is earlier than another time string
	@param tstr1 string in 'HH:MM' format
	@param tstr2 string in 'HH:MM' format
	@return True if earlier, False otherwise
	'''
	hours1 = int(tstr1[:-3])
	mins1  = int(tstr1[3:])
	hours2 = int(tstr2[:-3])
	mins2  = int(tstr2[3:])

	if hours1 > hours2:
		return False
	if hours1 < hours2:
		return True
	### Same hour
	if mins1 >= mins2:
		return False
	else:
		return True

def __get_mode_for_now(config) -> str:
	time_now = datetime.now().strftime('%H:%M')
	start = config['time']['start']
	end = config['time']['end']
	if __is_time_string_earlier_than(time_now, start): # If time is earlier than start
		if __is_time_string_earlier_than(start, end): # start is earlier than end (i.e. start 03:00 end 08:00)
			return 'light'
		else: # end is earler than start (i.e. start 22:00 end 07:00)
			if __is_time_string_earlier_than(time_now, end):
				return 'dark'
			else:
				return 'light'
	else: # Time is later than start
		if __is_time_string_earlier_than(start, end): # start is earlier than end (i.e. start 03:00 end 08:00)
			if __is_time_string_earlier_than(time_now, end):
				return 'dark'
			else:
				return 'light'
		else: # end is earler than start (i.e. start 22:00 end 07:00)
			return 'dark'

def __install():
	PATH_INSTALL_FILE.parent.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(PATH_THIS_FILE, PATH_INSTALL_FILE)
	os.system(f"chmod +x {PATH_INSTALL_FILE}")

def __uninstall():
	if PATH_INSTALL_FILE.exists():
		PATH_INSTALL_FILE.unlink()

def __turn_autostart_off():
	if PATH_AUTOSTART_FILE.exists():
		PATH_AUTOSTART_FILE.unlink()

def __turn_autostart_on():
	with open(PATH_AUTOSTART_FILE, 'w') as f:
		f.write(AUTOSTART_FILE_CONTENT)

def __turn_background_off():
	os.system('pkill automatic_theme')

def __turn_background_on():
	if __find_number_of_other_instances_of_this_script() > 0:
		print("Already running in background. Consider using 'restart' option.")
		return
	os.system(f"chmod +x {PATH_THIS_FILE}")
	os.system(f"nohup {PATH_THIS_FILE} run > /dev/null 2>&1 &")
	
def __restart_background():
	os.system(f"chmod +x {PATH_THIS_FILE}")
	os.system(f'pkill automatic_theme; nohup {PATH_THIS_FILE} run > /dev/null 2>&1 &')

def __run():
	light_or_dark = ''
	config = '' 
	### ---- Main loop ----
	while(True):
		with open(PATH_CONFIG_FILE, 'r') as f:
			new_config = json.load(f)
		new_light_or_dark = __get_mode_for_now(new_config)
		if light_or_dark != new_light_or_dark or config != new_config:
			light_or_dark = new_light_or_dark
			config = new_config
			if light_or_dark == 'light':
				os.system(f"gsettings set org.cinnamon.desktop.interface cursor-theme '{config['light']['Mouse Pointer']}'")
				os.system(f"gsettings set org.cinnamon.desktop.interface gtk-theme '{config['light']['Applications']}'")
				os.system(f"gsettings set org.cinnamon.desktop.interface icon-theme '{config['light']['Icons']}'")
				os.system(f"gsettings set org.cinnamon.theme name '{config['light']['Desktop']}'")
			else:
				os.system(f"gsettings set org.cinnamon.desktop.interface cursor-theme '{config['dark']['Mouse Pointer']}'")
				os.system(f"gsettings set org.cinnamon.desktop.interface gtk-theme '{config['dark']['Applications']}'")
				os.system(f"gsettings set org.cinnamon.desktop.interface icon-theme '{config['dark']['Icons']}'")
				os.system(f"gsettings set org.cinnamon.theme name '{config['dark']['Desktop']}'")
		time.sleep(30)

def __configure():
	with open(PATH_CONFIG_FILE, 'r') as f:
		config = json.load(f)
	print(f"#### Current config:\n{json.dumps(config, indent=4)} ####\n")
	print(f"#### New config (empty to leave unchanged):")
	config = {
		'time': {
			'start': input(f'Start time (HH:MM): ').strip() or config['time']['start'],
			'end': input(f'End time (HH:MM): ').strip() or config['time']['end']
		},
		'light': {
			'Mouse Pointer': input(f'[Light] Mouse Pointer: ').strip() or config['light']['Mouse Pointer'],
			'Applications': input(f'[Light] Applications: ').strip() or config['light']['Applications'],
			'Icons': input(f'[Light] Icons: ').strip() or config['light']['Icons'],
			'Desktop': input(f'[Light] Desktop: ').strip() or config['light']['Desktop'],
		},
		'dark': {
			'Mouse Pointer': input(f'[Dark] Mouse Pointer: ').strip() or config['dark']['Mouse Pointer'],
			'Applications': input(f'[Dark] Applications: ').strip() or config['dark']['Applications'],
			'Icons': input(f'[Dark] Icons: ').strip() or config['dark']['Icons'],
			'Desktop': input(f'[Dark] Desktop: ').strip() or config['dark']['Desktop'],
		},
	}
	# Save
	with open(PATH_CONFIG_FILE, 'w') as f:
		json.dump(config, f, indent=4)

############
### Main ###
############

if __name__=="__main__":
	### ---- Args ----
	parser = argparse.ArgumentParser(description='Automatic theme switcher for Cinnamon')
	subparsers = parser.add_subparsers(help='sub-command', dest='command')
	## Install
	parser_install = subparsers.add_parser('install', help='Install the script')
	## Uninstall
	parser_uninstall = subparsers.add_parser('uninstall', help='Uninstall the script')
	## Autostart
	parser_autostart = subparsers.add_parser('autostart', help='Whether to run the script on start (option and -h for further info)')
	parser_autostart.add_argument('on_or_off', help='on or off', choices=['on', 'off'])
	## Run (optionally in background)
	parser_run = subparsers.add_parser('run', help='Run the script (option and -h for further info)')
	## Start
	parser_start = subparsers.add_parser('start', help='Start the script in the background (option and -h for further info)')
	## Stop
	parser_stop = subparsers.add_parser('stop', help='Stop the script that is running in the background (option and -h for further info)')
	## Restart
	parser_restart = subparsers.add_parser('restart', help='Restart the script that is running in the background (option and -h for further info)')
	## Configure
	parser_configure = subparsers.add_parser('configure', help='Configure the script (option and -h for further info)')
	## Parse arguments
	args = parser.parse_args()
	## If no arguments are given, print help and exit
	if len(sys.argv) == 1:
		parser.print_help()
		exit(1)


	### ---- Config file ----
	PATH_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
	## Write default if it doesn't exist
	if not PATH_CONFIG_FILE.exists():
		with open(PATH_CONFIG_FILE, 'w') as f:
			json.dump(DEFAULT_CONFIG, f, indent=4)
	## Read config
	with open(PATH_CONFIG_FILE, 'r') as f:
		config = json.load(f)


	### ---- Handle commands ----
	if args.command == 'install':
		__install()
		exit(0)
	elif args.command == 'uninstall':
		__uninstall()
		exit(0)
	elif args.command == 'autostart':
		if args.on_or_off == 'on':
			__turn_autostart_on()
		elif args.on_or_off == 'off':
			__turn_autostart_off()
		exit(0)
	elif args.command == 'start':
		__turn_background_on()
		exit(0)
	elif args.command == 'stop':
		__turn_background_off()
		exit(0)
	elif args.command == 'restart':
		__restart_background()
		exit(0)
	elif args.command == 'run':
		## Check if already running in background
		__run()
		exit(0)
	## Configure
	elif args.command == 'configure':
		__configure()
		exit(0)