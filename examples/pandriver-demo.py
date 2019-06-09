#!/usr/bin/env python
import os
import sys

import pandevice
import pandevice.firewall
import pandevice.device


# set global variables
# you can leave these blank because we will check for them
hostname = '3.84.225.171'
username = 'admin'
password = 'badmin'

# Clear the screen and print information
os.system('clear')
print('Palo Alto Pandevice automation demo - W Embrey - ePlus')
print('\n *** WARNING - getpass doesnt work in Windows so make sure'
      ' you modify the script to add your password')

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


def get_firewall(hostname, username, password):
    try:
        fw = pandevice.firewall.Firewall(hostname=hostname, api_username=username, api_password=password)
        print(fw.refresh_system_info())
        print('Connection to firewall successfull')
        return fw
    except Exception as e:
        print(f'get_firewall failed with error: {e}')


def get_settings(fw):
    try:
        settings = pandevice.device.SystemSettings.refreshall(fw, add=True)
        systemsettings = settings[0].about()
        print(f'Current System Settings:\n')
        for item in systemsettings:
            print(f'{item:>20}:{systemsettings[item]}')
        return settings
    except Exception as e:
        print(f'get_settings failed with error: {e}')

def update_settings(fw, settings):
    try:
        settings[0].hostname = input('Enter new hostname: ')
        settings[0].apply()
        dns_primary = input('Enter Primary DNS Server: ')
        fw.set_dns_servers(dns_primary)
        status = fw.commit()
        job = int(status)
        print(f'Firewall commit job id {job} complete!')
    except Exception as e:
        print(f'update_settings failed with error: {e}')

def main():
    get_creds()
    fw = get_firewall(hostname, username, password)
    input('Enter to continue')
    settings = get_settings(fw)

    while True:
        command = input('\nUpdate firewall settings? (y/n)')
        if str.lower(command) != 'y':
            print('OK, closing script!')
            sys.exit()
        else:
            update_settings(fw, settings)
            get_settings(fw)
    print('\nClosing Script')


if __name__ == "__main__":
    main()
