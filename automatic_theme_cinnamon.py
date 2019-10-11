#!/usr/bin/python3

import os, sys, time, pathlib, fcntl, subprocess
from datetime import datetime

modes = ['on', 'on_s', 'off', 'configure']
cache_dir   = str(pathlib.Path.home()) + '/.cache/automatic_theme_cinnamon'
config_file = cache_dir + '/config'
if not os.path.isdir(cache_dir):
	os.mkdir(cache_dir)
if not os.path.exists(config_file):
	with open(config_file, 'w') as conf_file:
		### Fill with some sensible defaults
		conf_file.write('22:00\n09:00\n' + 
		                'Mint-Y\nMint-Y-Blue\nMint-Y-Blue\nDMZ-White\nMint-Y-Blue\n' + 
		                'Mint-Y-Dark\nMint-Y-Blue\nMint-Y-Dark-Blue\nDMZ-Black\nMint-Y-Blue')

### Global theme variables
light_or_dark = ''
start    = ''
end      = ''
light_wb = ''
light_ic = ''
light_ct = ''
light_mp = ''
light_ds = ''
dark_wb  = ''
dark_ic  = ''
dark_ct  = ''
dark_mp  = ''
dark_ds  = ''

### ---- Helper functions ----

def show_usage_and_exit():
	print('Usage: ')
	for m in modes:
		if m == 'on_s': continue # This mode is used to run in background
		print(sys.argv[0] + ' --' + m)
	exit(1)

def arguments_parser():
	args = sys.argv[1:]
	if len(args) != 1:
		show_usage_and_exit()
	mode = args[0]
	if mode not in ['--' + m for m in modes]:
		show_usage_and_exit()
	return mode[2:] # Without the --

def get_time():
	return datetime.now().strftime('%H:%M')

def is_time_string_earlier_than(tstr1, tstr2):
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


def get_mode_for_now():
	time_now = get_time()

	if is_time_string_earlier_than(time_now, start): # If time is earlier than start
		if is_time_string_earlier_than(start, end): # start is earlier than end (i.e. start 03:00 end 08:00)
			return 'light'
		else: # end is earler than start (i.e. start 22:00 end 07:00)
			if is_time_string_earlier_than(time_now, end):
				return 'dark'
			else:
				return 'light'
	else: # Time is later than start
		if is_time_string_earlier_than(start, end): # start is earlier than end (i.e. start 03:00 end 08:00)
			if is_time_string_earlier_than(time_now, end):
				return 'dark'
			else:
				return 'light'
		else: # end is earler than start (i.e. start 22:00 end 07:00)
			return 'dark'

def find_number_of_other_instances_of_this_script():
	procs = subprocess.Popen("ps -p $(pgrep -d, automatic_theme) -o state", 
	             shell=True, 
	             stdout=subprocess.PIPE).stdout.read().decode('UTF-8')
	procs = procs[2:][:-1] # Remove first 'S' (means state) and first and last endl
	other_alive_found = -1 # So that it doesn't count self
	for proc_state in procs.splitlines():
		if proc_state != 'T':
			other_alive_found += 1
	return other_alive_found

def set_theme(type, value):
	if type == 'Window borders':
		command = 'gsettings set org.cinnamon.desktop.wm.preferences theme '
	elif type == 'Icons':
		command = 'gsettings set org.cinnamon.desktop.interface icon-theme '
	elif type == 'Controls':
		command = 'gsettings set org.cinnamon.desktop.interface gtk-theme '
	elif type == 'Mouse Pointer':
		command = 'gsettings set org.cinnamon.desktop.interface cursor-theme '
	elif type == 'Desktop':
		command = 'gsettings set org.cinnamon.theme name '
	else:
		raise ValueError('Wrong theme type')
	os.system(command + value)

def configure():
	global start
	global end
	global light_wb
	global light_ic
	global light_ct
	global light_mp
	global light_ds
	global dark_wb
	global dark_ic
	global dark_ct
	global dark_mp
	global dark_ds
	start = input('Dark start time (format=HH:MM): ') or '22:00'
	end   = input('Dark end   time (format=HH:MM): ') or '09:00'
	print('/!\\ You can leave whichever of the following settings ' + 
	      'you want empty and the script will not attempt ' + 
	      'to change theme when switching to that theme')
	print('===Light theme settings===')
	light_wb = input('\tWindow borders: ') or '-'
	light_ic = input('\tIcons:          ') or '-'
	light_ct = input('\tControls:       ') or '-'
	light_mp = input('\tMouse Pointer:  ') or '-'
	light_ds = input('\tDesktop:        ') or '-'
	print('===Dark theme settings===')
	dark_wb  = input('\tWindow borders: ') or '-'
	dark_ic  = input('\tIcons:          ') or '-'
	dark_ct  = input('\tControls:       ') or '-'
	dark_mp  = input('\tMouse Pointer:  ') or '-'
	dark_ds  = input('\tDesktop:        ') or '-'

def write_config_to_file():
	with open(config_file, 'w') as conf_file:
		conf_file.write(
			start    + '\n' +
			end      + '\n' +
			light_wb + '\n' +
			light_ic + '\n' +
			light_ct + '\n' +
			light_mp + '\n' +
			light_ds + '\n' +
			dark_wb  + '\n' +
			dark_ic  + '\n' +
			dark_ct  + '\n' +
			dark_mp  + '\n' +
			dark_ds)

def load_config():
	global start
	global end
	global light_wb
	global light_ic
	global light_ct
	global light_mp
	global light_ds
	global dark_wb
	global dark_ic
	global dark_ct
	global dark_mp
	global dark_ds
	with open(config_file, 'r') as conf_file:
		c = conf_file.read().splitlines()
		start    = c[0]
		end      = c[1]
		light_wb = c[2]
		light_ic = c[3]
		light_ct = c[4]
		light_mp = c[5]
		light_ds = c[6]
		dark_wb  = c[7]
		dark_ic  = c[8]
		dark_ct  = c[9]
		dark_mp  = c[10]
		dark_ds  = c[11]


### ---- Operations on launch

mode = arguments_parser()

if mode == 'off':
	os.system('pkill automatic_theme')
	exit(0)

if mode == 'configure':
	configure()
	write_config_to_file()
	if find_number_of_other_instances_of_this_script() == 0:
		print('\nConfigured! Please run using: \n' + 
		      sys.argv[0] + ' --on')
	exit(0)

if mode == 'on':
	### See if it's already running
	if find_number_of_other_instances_of_this_script() > 0:
		print('Already running. If you want to restart, please run in order: ')
		print(sys.argv[0] + ' --off')
		print(sys.argv[0] + ' --on')
		exit(0)
	os.system(sys.argv[0] + ' --on_s &') # Run on_s in background
	exit(0)

### on_s below

load_config()

### ---- Main loop ----
while(True):
	load_config() # So that it gets updated
	new_light_or_dark = get_mode_for_now()
	print('New iteration, mode=' + new_light_or_dark)
	if light_or_dark != new_light_or_dark:
		light_or_dark = new_light_or_dark
		if light_or_dark == 'light':
			if light_wb != '-': set_theme('Window borders', light_wb)
			if light_ic != '-': set_theme('Icons', light_ic)
			if light_ct != '-': set_theme('Controls', light_ct)
			if light_mp != '-': set_theme('Mouse Pointer', light_mp)
			if light_ds != '-': set_theme('Desktop', light_ds)
		else:
			if light_wb != '-': set_theme('Window borders', dark_wb)
			if light_ic != '-': set_theme('Icons', dark_ic)
			if light_ct != '-': set_theme('Controls', dark_ct)
			if light_mp != '-': set_theme('Mouse Pointer', dark_mp)
			if light_ds != '-': set_theme('Desktop', dark_ds)

	time.sleep(30)