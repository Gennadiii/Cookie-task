import json
from os.path import expanduser
from re import match
from sys import argv
from time import time
from time import sleep
import pyperclip

if len(argv) == 1: print('Please enter the name of log file as flag like - cookie Gennadii_Mishchevskii'); exit()

name = argv[1]
log = expanduser( r'~\Desktop\\' + name + '.txt' )
log_api = {
    "number_of_tries" : -1,
    "reader_is_updated": True,
    "mistakes": 0,
    "start_time": int( time() ),
    "test_result": 'Task is NOT solved!'
}
invalid_input_message = 'Invalid input. Try again.'

def display_task_description():
    print("""It's a standard vending machine. You insert money, choose product - get what you ordered.
All prices in machine are divisible by 0.5 and so are money you have
You get only 1 cookie per transaction
You choose not cookie but the price of cookie, expensive cookies are just better ;)
""")

def json_load(log):
    while True:
        try:
            return json.load(open(log, 'r'))
        except Exception:
            sleep(0.5)

def json_dump(data, log):
    json.dump(data, open(log, 'w'))

def replace_separate_symbol_with_dot(value, position):
    float_value = False
    if len(value) > 2: float_value = match( '\D', value[position] )
    if float_value: return value.replace( value[position], '.' )
    return False

def prepared_for_float(value):
    prepared_value = replace_separate_symbol_with_dot(value, -3)
    if not prepared_value: prepared_value = replace_separate_symbol_with_dot(value, -2)
    if not prepared_value: prepared_value = value
    return "{:.2f}".format( float(prepared_value) )

def validated(purpose, value=''):
    if len(value) == 0: return False
    if value[0] == '-': return False
    try:
        print( purpose + prepared_for_float(value) )
        return True
    except Exception:
        return False

def validate_inserted_money(value):
    if value % 0.5 != 0:
        return 'Only 1, 2, 5 hryvnas and 50 cops are accepted'

def validate_chosen_cookie(value):
    if value % 0.5 != 0 or value <= 0:
        return 'There\'s no such price'

def game(inserted_money, chosen_cookie):
    inserted_money = float( prepared_for_float(inserted_money) )
    chosen_cookie = float( prepared_for_float(chosen_cookie) )

    if validate_inserted_money(inserted_money): 
        return validate_inserted_money(inserted_money)
    if validate_chosen_cookie(chosen_cookie): 
        return validate_chosen_cookie(chosen_cookie)

    if chosen_cookie > inserted_money and not ( validate_inserted_money(inserted_money) or validate_chosen_cookie(chosen_cookie) ):
        return 'Not enough money'
    if str(chosen_cookie)[-2:] == '.5' and inserted_money % chosen_cookie == 0 and inserted_money > chosen_cookie:
        return str( int( inserted_money / chosen_cookie ) ) + ' cookies returned' 
    return  '1 cookie returned and your change is: ' + str( inserted_money - chosen_cookie ) + '0'

if __name__ == '__main__':
    display_task_description()
    json_dump(log_api, log)
    while True:
        pyperclip.copy('*')
        invalid_input = False
        data = json_load(log)
        inserted_money = input('\n'*2 +'Insert money:                    ')
        if len(inserted_money) == 0: print( "You've gotta put something..." )
        chosen_cookie = input('Choose the price of your cookie: ')
        if len(inserted_money) == 0: print( "You've gotta choose something..." )
        try:
            if '+' in pyperclip.paste():
                data['test_result'] = 'Task is SOLVED ! ! !'
                json_dump(data, log)
                break
            if pyperclip.paste() in 'Choose the price of your cookie: ' or pyperclip.paste() in 'Insert money:':
                data['mistakes'] += 1
            if not validated('\n' + 'You paid          ', inserted_money):
                invalid_input = True
            if not invalid_input and not validated('Your cookie costs ', chosen_cookie):
                invalid_input = True
            if invalid_input:
                result = invalid_input_message
            if not invalid_input: result = game(inserted_money, chosen_cookie)
            print(result)
            if ( len(inserted_money) != 0 and len(chosen_cookie) != 0 ) and ( inserted_money[0] == '-' or chosen_cookie[0] == '-' ): \
            print('What are you doing? It\'s a real vending machine. You can\'t insert less than 0 money or order cheaper than 0 cookie ) But nice try ;))')
        except:
            result = invalid_input_message
            invalid_input = True
        data[ 'try_number_' + str( data['number_of_tries'] + 1 ) ] = [ inserted_money, chosen_cookie, result, invalid_input ]
        data['number_of_tries'] += 1
        data['reader_is_updated'] = False
        data['finish_time'] = int( time() )
        json_dump(data, log)
