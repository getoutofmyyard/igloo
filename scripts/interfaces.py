import os
import sys

sys.path.insert(1, '.\\')

from common import *

def int_tree(int_command):

    split_cmd = int_command.split(' ')
    int_index = split_cmd[2]

    if int_command == 'int reset *':
        get_nics = pshell_decoder('Restart-NetAdapter -Name \'*\' \
            -WhatIf | sort-object')

        strip_nics = get_nics.strip()

        newline()

        print(strip_nics.replace("What if: Restart-NetAdapter", \
            "notify~! Restarting network adapter"))

        reset_nics = subprocess.call(['powershell.exe', 'Restart-NetAdapter \
            -Name \'*\''], stdout=open(os.devnull, 'wb'))

        newline()
        print('notify~! Network adapters restarted successfully')
        newline()

    elif 'enable' in int_command:
        get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | \
            Select-Object Name | Format-Table -AutoSize'.format(int_index))

        split_list = get_int_list.split('----')
        get_name = split_list[1]
        int_name = '\'' + get_name.strip() + '\''

        enable_adapter = pshell_decoder('Enable-NetAdapter -Name {}'.format(int_name))

        if 'Enable-NetAdapter : Access is denied.' in enable_adapter:
            newline()
            print('error~! This action requires admin rights!')
            newline()
        elif 'No MSFT_NetAdapter objects found' in enable_adapter:
            newline()
            print('notify~! Interface does not exist. Use \'show int\' \
                and \'int ?\' for help')
            newline()
        else:
            newline()
            print('notify~! Interface {} has been enabled'.format(int_name))
            newline()

    elif 'disable' in int_command:

        split_cmd = int_command.split(' ')
        int_index = split_cmd[2]

        get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | \
            Select-Object Name | Format-Table -AutoSize'.format(int_index))

        split_list = get_int_list.split('----')
        get_name = split_list[1]
        int_name = '\'' + get_name.strip() + '\''

        disable_adapter = pshell_decoder('Disable-NetAdapter -Name {} \
            -Confirm:$False'.format(int_name))


        if 'Disable-NetAdapter : Access is denied.' in disable_adapter:
            newline()
            print('error~! This action requires admin rights!')
            newline()
        elif 'No MSFT_NetAdapter objects found' in disable_adapter:
            newline()
            print('notify~! Interface does not exist. Use \'show int\' \
                and \'int ?\' for help')
            newline()
        else:
            newline()
            print('notify~! Interface {} has been disabled'.format(int_name))
            newline()

    elif 'reset' in int_command:

        split_cmd = int_command.split(' ')
        int_index = split_cmd[2]

        get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | \
            Select-Object Name | Format-Table -AutoSize'.format(int_index))

        split_list = get_int_list.split('----')
        get_name = split_list[1]
        int_name = '\'' + get_name.strip() + '\''

        disable_adapter = pshell_decoder('Disable-NetAdapter -Name {} \
            -Confirm:$False'.format(int_name))
        enable_adapter = pshell_decoder('Enable-NetAdapter -Name {}\
            '.format(int_name))


        if 'Disable-NetAdapter : Access is denied.' in disable_adapter:
            newline()
            print('error~! This action requires admin rights!')
            newline()
        elif 'No MSFT_NetAdapter objects found' in disable_adapter:
            newline()
            print('notify~! Interface does not exist. \
                Use \'show int\' and \'int ?\' for help')
            newline()
        else:
            newline()
            print('notify~! Interface {} has been reset'.format(int_name))
            newline()