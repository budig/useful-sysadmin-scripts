#### STILL IN PROGRESS ####
'''
    Option 1 - Buscar equipo: 
        * Have to parse json variable to show data
    Option 2 - Equipos conectados a switch:
        * Filtering with active status = 1 it is not running on pandas
    Option 3 - Ver puertos VLAN en switch:
        * Must check the pandas result. I see more registers that must be
    API_KEY:
        * We retreive the api key using .env file that is not uploaded on git. Anyway it is not the best option to store a password in plain text.
          We should implement the use of the operating system keyring.
'''

import requests
import os
import json
import pandas as pd
import socket
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
    2: 'Equipos conectados a switch',
    3: 'Ver puertos VLAN en switch',
    4: 'Exit',
}

def resolve_name_to_ip(device):
    return socket.gethostbyname(device)

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def menu_1_search_host(hostname):
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
     
def menu_2_get_nodes_on_device(device):
    api_key=request_api_key()
    r = requests.get(NETDISCO_URL + '/api/v1/object/device/' + resolve_name_to_ip(device) + '/nodes',
                    headers={'Accept': 'application/json',
                            'Authorization': api_key})
                            
    # pretty print the JSON stucture
    #print(json.dumps(r.json(), indent=2, sort_keys=True))
    data_search = r.json()
    df = pd.DataFrame(data_search)
    activos = df.loc[df['active']==1]
    print(activos)

def menu_3_get_port_vlans_switch(device):
    api_key=request_api_key()
    r = requests.get(NETDISCO_URL + '/api/v1/object/device/' + resolve_name_to_ip(device) + '/port_vlans',
                    headers={'Accept': 'application/json',
                            'Authorization': api_key})
                            
    # pretty print the JSON stucture
    #print(json.dumps(r.json(), indent=2, sort_keys=True))
    data_search = r.json()
    df = pd.DataFrame(data_search)
    print(df)

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
            try:
                device = str(input("Introduce el nombre del switch ['XXXXXX.sufijoDNS']: "))
            except ValueError:
                print("Formato incorrecto")
                continue
            menu_2_get_nodes_on_device(device)

        elif option == 3:
            try:
                device = str(input("Introduce el nombre del switch ['XXXXXX.sufijoDNS']: "))
            except ValueError:
                print("Formato incorrecto")
                continue
            menu_3_get_port_vlans_switch(device)

        elif option == 4:
            print('Adiós')
            exit()

        else:
            print('Opción incorrecta. Por favor, introduce un número entre el 1 y el 4.')





