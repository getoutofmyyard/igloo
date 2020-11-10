import os
import sys

sys.path.insert(1, '.\\')

import showDict
from common import *


def show_tree(show_command):
    newline()

    try:
        for command in showDict.show_command_set:
            if command == show_command:
                output = pshell_decoder(showDict.show_command_set.get(command))

                if command == 'show ip public':
                    print('notify~! Your translated address is ' + output)

                elif command == 'show ipv6 public':
                    format_output = output.split(',')[1]
                    print('notify~! Your translated address is ' + format_output)
                    newline()

                elif 'Get-BgpPeer' in output:
                    print('notify~! No BGP peers are configured. Use \'bgp peer\'.')
                    newline()

                elif 'Get-BgpRouter' in output:
                    print('notify~! BGP ID is not configured. Use \'bgp id\'.')
                    newline()

                elif 'Get-BgpRouteAggregate' in output:
                    print('notify~! No BGP aggregates are advertised.')
                    newline()

                elif 'Get-BgpCustomRoute' in output:
                    print('notify~! No BGP prefixes are advertised.')
                    newline()
                elif 'Get-BgpStatistics' in output:
                    print('notify~! No BGP statistics available.')
                    newline()
                else:
                    print(output)

        if show_command == 'show powershell policy':
            policy_level = pshell_decoder('Get-ExecutionPolicy')
            stripped_output = policy_level.rstrip()
            print('notify~! PowerShell execution policy is {}.\
                '.format(stripped_output))
            newline()

        elif show_command == 'show cidr-table':
            read_file("C:\\Users\\Jesus Christ\\Desktop\\igloo-dev\\ \
                help-files\\helpCidrTable.txt")

        elif show_command == 'show log app':

            pshell_decoder('Get-EventLog -LogName Application -Newest 5000 | \
                Select-Object Index,TimeGenerated,Source,Message |  \
                Format-Table -AutoSize -Wrap > ./applog.txt')

            pshell_decoder('notepad.exe .\\applog.txt')

            os.system('del applog.txt')

        elif show_command == 'show log sec':

            pshell_decoder('Get-EventLog -LogName Security -Newest 5000 | \
                Format-Table  -Wrap -AutoSize > seclog.txt')

            pshell_decoder('notepad.exe ./seclog.txt')

            os.system('del seclog.txt')

        elif show_command == 'show log sys':

            pshell_decoder('get-eventlog -LogName System -Newest 5000 | \
                Select-Object Index,TimeGenerated,EntryType,Message | \
                Format-Table -Wrap -AutoSize > syslog.txt')

            pshell_decoder('notepad.exe ./syslog.txt')
            os.system('del seclog.txt')
        else:
            pass

    except:
        newline()
        print('error~! An exception occurred. Cancelling operation.')
        newline()