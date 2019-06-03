#!/usr/bin/env python
# import the modules we need for this script
import requests
import xml.etree.ElementTree as xt
import json
import sys
import os
import getpass

# set global variables
# you can leave these blank because we will check for them
hostname = '192.168.0.100'
username = 'admin'
password = 'admin'


# check we have the hostname and credentials
def get_creds():
    # set the variables to global so we adjust the globals
    global hostname
    global username
    global password

    # gather the hostname and credentials if they were not set
    if not bool(hostname):
        hostname = input('Enter the hostname')
    if not bool(username):
        username = input('Enter the API username')
    if not bool(password):
        password = getpass.getpass('Enter the password')
    return


# Clear the screen and print information
os.system('clear')
print('Palo Alto REST API automation demo - W Embrey - ePlus')
print('\n *** WARNING - getpass doesnt work in Windows so make sure'
      ' you modify the script to add your password')

# use the XML api to gather the API key for the user.
def get_key():
    url = 'https://' + hostname + '/api/'
    querystring = {"type":"keygen","user":username,"password":password}
    response = requests.request("GET", url, params=querystring, verify=False)
    xml_response = xt.fromstring(response.text)
    apikey = xml_response[0][0].text
    return apikey


# this function will get a list of addresses on the firewall
def get_addresses(apikey):
    url = 'https://' + hostname + '/restapi/9.0/Objects/Addresses'
    querystring = {"location":"vsys","vsys":"vsys1","key":apikey}
    response = requests.request("GET", url, verify=False, params=querystring)

    # process the response if it was a success
    if response.status_code is 200:

        # convert the bytes payload into a python dictionary
        json_data = response.json()

        # find the address entries and add to a list
        address_list = json_data['result']['entry']

        # count the number of address entries
        address_count = int(json_data['result']['@count'])
        print(f'\nConnection success. {str(address_count)} entries found')

        # loop through the addresses
        for address in address_list:
            print(f'\n{address["@name"]}')
            print(f'{address["ip-netmask"]}')
            try:
                print(f'{address["description"]}')
            except:
                print('No description found')

    # notify is the request did not response with 200
    else:
        print(f'Unable to process response. Status code {response.status_code}')


# this function will add an address to the firewall in vsys1
def set_address(apikey):
    # get the information for the new address
    entry_name = input('Enter the name of the address entry: ')
    ip_netmask = input('Enter the ip/netmask: ')
    description = input('Enter a description: ')
    tags = input('Enter tags separated with commas and no spaces: ').split(',')

    # build the JSON payload
    payload = {"entry": \
              {"@name":entry_name, "description":description, \
               "ip-netmask":ip_netmask, \
               "tag":{"member":tags} \
              }
              }

    # build the request
    url = "https://" + hostname + "/restapi/9.0/Objects/Addresses"
    querystring = {"name":entry_name,"location":"vsys","vsys":"vsys1", \
                   "key":apikey}
    response = requests.request("POST", url, verify=False, \
                                json=payload, params=querystring)
    if response.status_code is 200:
        print(f'Request successfully sent')
    else:
        print(f'Update failed: {response.text}, {response.reason}')

# this is the standard starting point where you call the functions to begin
def main():
    # call the function to check credentials
    get_creds()
    print(f'\nCredentials confirmed')

    # call the function to get the API key
    apikey = get_key()
    print(f'Gathered API from {hostname}\nKey:{apikey}\n\n')
    input('Hit [Enter] to get addresses\n\n')

    # call the function to get the addresses
    get_addresses(apikey)

    # add a loop to offer the option to add an address
    while True:
        command = input('\nAdd an address to the firewall? (y/n)')
        if str.lower(command) != 'y':
            print('OK, closing script!')
            sys.exit()
        else:
            set_address(apikey)
            get_addresses(apikey)


# this boilerplate function works if the script was called directly.
# if the script was imported into another script, it will wait to be called.
if __name__ == "__main__":
    main()
