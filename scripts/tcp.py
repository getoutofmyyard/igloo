import subprocess, os, socket
from socket import SOCK_STREAM, AF_INET
from datetime import datetime

def newline():
    print('')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def read_file(filepath):
    # Reads a file. Used most often for help files.
    try:
        with open(filepath,'r') as file:
            print(file.read())
            newline()
    except:
        newline()
        print('error~! Help file ' + filepath + ' is missing.')
        newline()

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

def tcp_connect(tcp_conn_arg):
    command_parse = tcp_conn_arg.split(' ')
    if len(command_parse) == 5:
        destination_host = command_parse[2]
        destination_port = command_parse[4]

        send_syn = pshell_decoder('test-netconnection -ComputerName ' + destination_host + ' -Port ' + destination_port)

        # Find the line with the TcpTestSucceeded result
        send_syn_lines = send_syn.splitlines()
        for line in send_syn_lines:
            if 'TcpTestSucceeded' in line:
                # Check if there is true in that line's output
                if 'True' in line:
                    newline()
                    print('notify~! Success: SYN+ACK received from remote host %s:%s.' %  (destination_host,destination_port))
                    newline()
                    return
                else :        
                    newline()
                    print('notify~! Failure: No SYN+ACK received from remote host %s:%s.' % (destination_host,destination_port))
                    newline()
                    return
    else:
        newline()
        read_file('.\\help-files\\helpTcpConnect.txt')


def net_reset():
    get_nics = pshell_decoder('Restart-NetAdapter -Name \'*\' -WhatIf | sort-object')
    strip_nics = get_nics.strip()
    newline()
    print(strip_nics.replace("What if: Restart-NetAdapter", "notify~! Restarting network adapter"))
    resetNics = subprocess.call(['powershell.exe', 'Restart-NetAdapter -Name \'*\''], stdout=open(os.devnull, 'wb'))
    newline()
    print('notify~! Network adapters restarted successfully')
    newline()