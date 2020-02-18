import subprocess
import os
from common import pshell_decoder, newline

def fping_script():
    newline()
    print('notify~! Your device list should be a .txt file with one'\
           + ' hostname or IP address per line.')
    newline()
    try:
        loop_keepalive = 1
        while loop_keepalive == 1:
            my_devices = input('input~! Specify the full path to your device list: ')
            strip_devices = my_devices.strip(' ')
            no_quotes = strip_devices.strip('\'"') 
            if any(my_devices) == True:
                loop_keepalive = 0
                break

        newline()
        print('notify~! Pinging device list...')
    except:
        newline()
        print('notify~! Terminating operation...')
        newline()

    with open(no_quotes,'r') as file:

        newline()

        for line in file:

            target = pshell_decoder('ping -n 1 ' + line)
            stripped_target = target.strip()
            split_target = stripped_target.split('\n')
            stripped_line = line.rstrip()

            try:
                if 'Reply' in split_target[1]:
                    print('{} OK'.format(stripped_line))
                else:
                    print('{} FAIL'.format(stripped_line))
            except:
                pass

        newline()