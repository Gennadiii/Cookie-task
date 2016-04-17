import json
from os.path import expanduser
from time import sleep
from sys import argv
from cookie import prepared_for_float, json_load, json_dump

name = argv[1]
if ':' in name:
	reader_log = expanduser( r'' + name )
else:
	reader_log = expanduser( r'~\Desktop\\' + name + '.txt' )

def display_help():
	print("""First argument - name of log file without extention like - Gennadii_Mishchevskii
Or full path to the file		
Flags:
How to display:
n - displays user's inputs in a standard way like - 1.50
r - displays user's inputs as is like - 1,.50
What to display:
f - works with flow of cookie.py script - waits for user's inputs there and displays in cookie_reader.py window
a - reads log file and displays everything then exits
c - reads log file and displays everything then continues working with flow of cookie.py script like f flag
""")
	exit()
if argv[1] == 'help': display_help()

if len(argv) == 2: argv.append('nf')
how_to_display = False
if 'r' in argv[2]: how_to_display = 'raw'
if 'n' in argv[2]: how_to_display = 'nice'
what_to_display = False
if 'f' in argv[2]: what_to_display = 'flow'
if 'a' in argv[2]: what_to_display = 'all'
if 'c' in argv[2]: what_to_display = 'continue'

if not what_to_display:	print("You didn't choose what to display")
if not how_to_display: print("You didn't choose how to display")
if not (what_to_display and how_to_display):
	print('Please look for help by "cookie_reader help" command')
	exit()

def print_result(result, number_of_tries, how_to_display):
	invalid_input = result[3]
	inserted_money = result[0]
	cookie_price = result[1]
	output = result[2]
	if how_to_display == 'nice':
		if not invalid_input:
			inserted_money = prepared_for_float(result[0])
			cookie_price = prepared_for_float(result[1])
		else:
			inserted_money = ''
			cookie_price = ''		
	print( '| ' + 'attempt # ' + str(number_of_tries) + ' '*( 7 - len(inserted_money) ) + '| ' + \
		inserted_money + ' '*( 5 - len(inserted_money) ) + ' | ' + \
		cookie_price + ' '*( 5 - len(cookie_price) ) + ' | ' + output )
	print_line()

def print_line():
	print('-'*150)

print_line()
data = json_load(reader_log)

def display_flow():
	while True:	
		sleep(0.5)
		data = json_load(reader_log)
		if data["reader_is_updated"] == False:
			print_result( data["try_number_" + str( data["number_of_tries"] ) ], data["number_of_tries"], how_to_display )
			data["reader_is_updated"] = True
			json_dump(data, reader_log)

def display_all():
	for j in range( data["number_of_tries"] + 1 ):
		print_result( data[ "try_number_" + str(j) ], str(j), how_to_display )
	data["reader_is_updated"] = True
	json_dump(data, reader_log)

if what_to_display == 'continue':
	display_all()
	display_flow()

if what_to_display == 'all':
	display_all()
	
if what_to_display == 'flow':
	display_flow()
