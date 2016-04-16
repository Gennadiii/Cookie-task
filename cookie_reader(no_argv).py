import json
from os.path import expanduser
from time import sleep

def json_load():
    return json.load(open(log, 'r'))

def json_dump(data):
    json.dump(data, open(log, 'w'))

def print_result(result, number_of_tries):
	print( '| ' + 'attempt # ' + str(number_of_tries) + ' '*( 7 - len(result[0]) ) + '| ' + \
		result[0] + ' '*( 5 - len(result[0]) ) + ' | ' + \
		result[1] + ' '*( 5 - len(result[1]) ) + ' | ' + result[2] )

def print_line():
	print('-'*150)

log = input('Input log path: ')

print_line()

while True:	
	data = json_load()
	if data["reader_is_updated"] == False:
		print_result( data["try_number_" + str( data["number_of_tries"] ) ], data["number_of_tries"] )
		print_line()
		data["reader_is_updated"] = True
		json_dump(data)
	sleep(0.5)
