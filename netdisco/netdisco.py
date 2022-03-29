import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

NETDISCO_URL=os.getenv('NETDISCO_URL')
USERNAME_NETDISCO=os.getenv('USERNAME_NETDISCO')
PASSWORD_NETDISCO=os.getenv('PASSWORD_NETDISCO')

def request_api_key():
    r = requests.post(NETDISCO_URL+'/login',
                    auth=(USERNAME_NETDISCO, PASSWORD_NETDISCO),
                    headers={'Accept': 'application/json'})

    api_key = r.json()['api_key']
    return api_key

menu_options = {
    1: 'Buscar equipo',
    2: 'Option 2',
    3: 'Option 3',
    4: 'Exit',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def menu_1_search_host(hostname):
    #print('\'Opción 1\' - Buscar equipo: '+hostname)
    api_key=request_api_key()
    r = requests.get(NETDISCO_URL+'/api/v1/search/node',
                    headers={'Accept': 'application/json',
                            'Authorization': api_key},
                    params={'q': hostname})
    
    # Requests to json
    data_search = r.json()
    print(data_search)
    # PARSE JSON PENDING
    # ..
    # .. (USE PANDAS?)
     

def option2():
     print('Handle option \'Option 2\'')

def option3():
     print('Handle option \'Option 3\'')

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Elige una opción: '))
        except:
            print('Opción incorrecta. Por favor, introduce un número ...')

        #Check what choice was entered and act accordingly
        if option == 1:
            try:
                hostname = str(input("Introduce el nombre del equipo: "))
            except ValueError:
                print("Formato incorrecto")
                continue
            menu_1_search_host(hostname)

        elif option == 2:
            option2()

        elif option == 3:
            option3()

        elif option == 4:
            print('Adiós')
            exit()

        else:
            print('Opción incorrecta. Por favor, introduce un número entre el 1 y el 4.')





