import subprocess, os
from netmiko import ConnectHandler, cisco, hp, juniper
from getpass import getpass


 #Newline function
def newline():
    print('')

 # Retrieves and splits a device list into an array
def get_file(devices):
    with open(devices,'r') as device_file:
        readFile = device_file.read()
        splitFile = readFile.split('\n')
        return splitFile

 # Prints device lists to the console
def read_file(device_list):
    newline()
    with open(device_list,'r') as device_file:
        readFile = device_file.read()
        print(readFile)
    newline()

#Decodes a given output. Useful for reading stdout from subprocess.Popen
def subprocessDecode(decodeMe):
    return decodeMe.communicate()[0].decode('iso-8859-1')

def ssh_connections(devs, cmd, usr, pwd, os_plat):

    with open(devs,'r') as file:
        read_device_file = file.read()
        split_file = read_device_file.split('\n')
        for a_device in split_file:
            network_device = {
            'device_type':os_plat,
            'host':a_device,
            'username':usr,
            'password':pwd,
            }

            try:
                net_connect = ConnectHandler(**network_device)
                output = net_connect.send_command(cmd)
                newline()
                print('-' * 50)
                print(network_device['host'] +'#'+' {}'.format(cmd))
                print('-' * 50)
                newline()
                print(output)
                newline()
                net_connect.disconnect()

            except:
                print('error~! An exception occurred. Skipping %s' % a_device)
                newline()
                continue

def ssh_show_init(ssh_command):

    newline()
    print('notify~! Your device list should be a .txt file with one'\
           + ' hostname or IP address per line.')
    newline()

    try:

        if ssh_command == 'ssh show ios':
            os_platform = 'cisco_ios'
        #elif ssh_command == 'ssh show asa':
        #    os_platform = 'cisco_asa'
        elif ssh_command == 'ssh show ios-xr':
            os_platform = 'ios_xrv'
        elif ssh_command == 'ssh show arista':
            os_platform = 'arista_eos'
        elif ssh_command == 'ssh show hp-curve':
            os_platform = 'hp_procurve'
        elif ssh_command == 'ssh show juniper':
            os_platform == 'juniper'
        elif ssh_command == 'ssh show nexus':
            os_platform = 'cisco_nxos'
        else:
            pass

        loop_keepalive = 1
        while loop_keepalive == 1:
            my_devices = input('input~! Specify the path to your device list: ')
            strip_devices = my_devices.strip(' ')
            no_quotes = strip_devices.strip('\'"') 
            if any(my_devices) == True:
                loop_keepalive = 0
                break
        
        command_keepalive = 1
        while command_keepalive == 1:
            command = input('input~! Enter a \'show\' command to run on each device: ')
            if 'show' in command:
                command_keepalive = 0
                newline()
                break

        username_keepalive = 1
        while username_keepalive == 1:
            username = input('input~! Enter a username: ')
            if any(username) == True:
                username_keepalive = 0
                newline()
                break

        password_keepalive = 1
        newline()
        while password_keepalive == 1:
            password = getpass()
            if any(password) == True:
                password_keepalive = 0
                break

        ssh_connections(no_quotes, command, username, password, os_platform)

    except:
        newline()
        print('notify~! Cancelled operation.')
        newline()
        return

    if 'show' in command:
        ssh_connections(no_quotes, command, username, password, platform)
    else:
        print('\nerror~! Command rejected. This application supports \'show\' commands only.')

def ssh_connections_write(devices, command, username, password, directory, os):
    
    sequence_number = 0
    with open(devices, 'r') as file:
        read_device_file = file.read()
        split_file = read_device_file.split('\n')

        newline()

        for device in split_file:
            network_device = {
            'device_type':os,
            'host':device,
            'username':username,
            'password':password
            }

            sequence_number = sequence_number + 1

            try:
                net_connect = ConnectHandler(**network_device)
                output = net_connect.send_command(command)
                path = directory + '\\' + device

                with open(path, 'w+') as saved_file:
                    print('notify~! Saving file '+ path +'.txt')
                    write_output = saved_file.write(output)

                net_connect.disconnect()

            except:
                newline()
                print('error~! An exception occurred. Skipping {}'.format(device))
                newline()

def ssh_write_init(ssh_write_command):
        newline()
        print('notify~! Your device list should be a .txt file with one'\
                + ' hostname or IP address per line.')
        print('notify~! Your destination path should be complete.'\
               + ' Use \'Copy as Path\'')
        newline()
        try:
            if ssh_write_command == 'ssh write ios':
                os_platform = 'cisco_ios'
            #elif ssh_write_command == 'ssh write asa':
            #    os_platform = 'cisco_asa'
            elif ssh_write_command == 'ssh write ios-xr':
                os_platform = 'ios_xrv'
            elif ssh_write_command == 'ssh write arista':
                os_platform = 'arista_eos'
            elif ssh_write_command == 'ssh write hp-curve':
                os_platform = 'hp_procurve'
            elif ssh_write_command == 'ssh write juniper':
                os_platform == 'juniper'
            elif ssh_write_command == 'ssh write nexus':
                os_platform = 'cisco_nxos'
            else:
                pass

            device_keepalive = 1
            while device_keepalive == 1:
                my_devices = input('input~! Specify the path to your device list: ')
                strip_devices = my_devices.strip(' ')
                devices_clean = strip_devices.strip('\'"') 
                if any(my_devices) == True:
                    loop_keepalive = 0
                    break

            dest_keepalive = 1
            while dest_keepalive == 1:
                my_directory = input('input~! Specify the destination directory path: ')
                strip_dir = my_directory.strip(' ')
                dir_clean = strip_dir.strip('\'"') 
                if any(my_directory) == True:
                    dest_keepalive = 0
                    break

            command_keepalive = 1
            while command_keepalive == 1:
                ssh_cmd = input('input~! Enter a \'show\' command to run on each device: ')
                if 'show' in ssh_cmd:
                    command_keepalive = 0
                    break

            username_keepalive = 1
            while username_keepalive == 1:
                user = input('input~! Enter your username: ')
                if any(user) == True:
                    username_keepalive = 0
                    break

            password_keepalive = 1
            while password_keepalive == 1:
                passwd = getpass()
                if any(passwd) == True:
                    password_keepalive = 0
                    break

            if 'show' in ssh_cmd:
                ssh_connections_write(devices_clean, ssh_cmd, user, passwd, dir_clean, os_platform)
            else:
                print('\nerror~! Command rejected. This application supports \'show\' commands only.')

        except:
            newline()
            print('notify~! Cancelled operation.')
            newline()
            pass    