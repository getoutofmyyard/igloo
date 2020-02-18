import subprocess, os, socket
from socket import SOCK_STREAM, AF_INET
from datetime import datetime
from common import *

def tcp_scan(tcp_arg):
    command_parse = tcp_arg.split(' ')
    remote_device = command_parse[2]
    remote_device_ip  = socket.gethostbyname(remote_device)
    socket.setdefaulttimeout(0.02)
    newline()
    print ('notify~! Scanning remote host {}...'.format(remote_device_ip))
    newline()
    try:
        for port_number in range(1,1025):
            start_scan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_tcp_syns = start_scan.connect_ex((remote_device_ip, port_number))
            if send_tcp_syns == 0:
                print('Port {}:     Open'.format(port_number))
            else:
                pass
        sock.close()
    except KeyboardInterrupt:
        newline()
        print ('notify~! Scan has been terminated.')
        newline()
    except socket.gaierror:
        newline()
        print ('notify~! DNS lookup failure.')
        newline()
    except socket.error:
        newline()
        print ('notify~! Couldn\'t connect to remote host.')
        newline()
    newline()
    newline()


def tcp_ping(tcp_ping_arg):
    command_parse = tcp_ping_arg.split(' ')
    if len(command_parse) == 4:
        remote_device = command_parse[2]
        port_number = int(command_parse[3])
        remote_device_ip  = socket.gethostbyname(remote_device)
        socket.setdefaulttimeout(0.02)
        newline()

        count = 0
        ack_count = 0
        try:
            for ping in range(5):
                count = count + 1
                start_scan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_tcp_syns = start_scan.connect_ex((remote_device_ip, port_number))
                if send_tcp_syns == 0:
                    ack_count = ack_count + 1
                    print('!', end = '')
                    start_scan.shutdown(1)
                    start_scan.close()
                else:
                    print('.', end = '')
                    pass

                if count == 5:
                    print('\n\nnotify~! {}/5 TCP SYN+ACKs received.\n'.format(ack_count, port_number))

        except socket.gaierror:
            newline()
            print ('notify~! DNS lookup failure.')
            newline()

    else:
        pass
        newline()
        with open('./help-files/helpTcpPing.txt','r') as help_file:
            print(help_file.read())
        newline()

def net_reset():
    get_nics = pshell_decoder('Restart-NetAdapter -Name \'*\' -WhatIf | sort-object')
    strip_nics = get_nics.strip()
    newline()
    print(strip_nics.replace("What if: Restart-NetAdapter", "notify~! Restarting network adapter"))
    resetNics = subprocess.call(['powershell.exe', 'Restart-NetAdapter -Name \'*\''], stdout=open(os.devnull, 'wb'))
    newline()
    print('notify~! Network adapters restarted successfully')
    newline()