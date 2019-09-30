import subprocess, os, sys, ctypes, netmiko, getpass, random
import conversion, helpDict, showDict, winOsDict, winPopenDict, installDict
from datetime import datetime
from crypto import *
from fwall import *
from tcp import *
from ipconf import *
from sshSet import *

yes = ['y', 'Y', 'yes', 'Yes'] 
no = ['n', 'N', 'no', 'No']
quit = ['exit','end','bye','quit','leave','esc']

def newline():
    print('')

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

def parse_file(filepath):
    # Reads file, splits into an array, and returns the array
    with open(filepath) as file:
        split_file = file.read().split('\n')
        return split_file

def splash_screen():
    # Displays the Igloo splash screen
    newline()
    read_file(".\\miscellaneous\\splash.txt")

# Command lists. Checked against user input for initial piping into
# the various command trees below.
crypto_general = parse_file('.\\command-sets\\cryptoCmds.txt')
crypto_ipsec = parse_file('.\\command-sets\\cryptoIpsecCmds.txt')
crypto_pptp = parse_file('.\\command-sets\\cryptoPptpCmds.txt')
fwall_general = parse_file('.\\command-sets\\fwallCmds.txt')
fwall_show = parse_file('.\\command-sets\\fwallShowCmds.txt')
install_cmds = parse_file('.\\command-sets\\installCmds.txt')
ip_cmds = parse_file('.\\command-sets\\ipCmds.txt')
show_cmds = parse_file('.\\command-sets\\showCmds.txt')
win_os_cmds = parse_file('.\\command-sets\\winOsCmds.txt')
win_popen_cmds = parse_file('.\\command-sets\\winPopenCmds.txt')
ssh_cmds = parse_file('.\\command-sets\\sshCmds.txt')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def admin_check():
    # Checks to see if user ran Igloo as admin.
    # If not, prompt user to elevate privileges.
    is_an_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if is_an_admin == 0:
        splash_screen()
        newline()
        print('notify~! You must run Igloo as Administrator!')
        try:
            input_loop = 0
            newline()
            while input_loop == 0:
                elevate_me = input('input~! Restart with elevated privileges? (y/n) ')
                if elevate_me in yes:
                    os_run('powershell Start-Process .\\igloo.exe \
                           -Verb runAs Administrator')
                    input_loop = 1
                    exit()
                elif elevate_me in no:
                    input_loop = 1
                    newline()
                    print('notify~! Exiting Igloo...')
                    newline()
                    time.sleep(1)
                    exit()
                else:
                    pass
        except:
            newline()
            newline()
            print('notify~! Exiting Igloo...')
            newline()
            time.sleep(1)
            exit()
    else:
        pass

def who_am_i():
    # Returns current username
    get_username = pshell_decoder('whoami')
    format_username = get_username.split("\\",1)[1].strip()
    return format_username

def show_tree(show_command):
    # Search showDict.py for relevant command
    newline()
    try:
        for command in showDict.show_command_set:
            if command == show_command:
                output = pshell_decoder(showDict.show_command_set.get(command))
                if command == 'show ip public':
                    newline()
                    print('notify~! Your translated address is ' + output)
                elif command == 'show ipv6 public':
                    format_output = output.split(',')[1]
                    newline()
                    print('notify~! Your translated address is ' + format_output)
                    newline()
                else:
                    print(output)

        if show_command == 'show powershell policy':
            policy_level = pshell_decoder('Get-ExecutionPolicy')
            stripped_output = policy_level.rstrip()
            print('notify~! PowerShell execution policy is {}.'.format(stripped_output))
            newline()
        else:
            pass

    except:
        newline()
        print('error~! An exception occurred. Cancelling operation.')
        newline()

def win_os_tree(win_os_command):
    # Search winOsDict.py for relevant command. Use os_run()
    # for .cpl and .msc compatibility.
    try:
        for command in winOsDict.win_os_command_set:
            if command == win_os_command:
                os.system(winOsDict.win_os_command_set.get(command))
            else:
                pass
    except:
        pass

def win_popen_tree(win_popen_command):
    # Search winPopenDict.py for relevant command.
    try:
        for command in winPopenDict.win_popen_command_set:
            if command == win_popen_command:
                subprocess.Popen(winPopenDict.win_popen_command_set.get(command))
            else:
                pass

        if win_popen_command == 'win reboot':
            reboot_loop_keepalive = 1
            newline()
            while reboot_loop_keepalive == 1:
                reboot_confirm = input("confirm~! Are you sure you want to reboot? (y/n) ")
                if reboot_confirm in yes:
                    reboot_loop_keepalive = 0
                    subprocess.Popen("shutdown /r /t 0")
                elif reboot_confirm in no:
                    reboot_loop_keepalive = 0
                    newline()
                    print('notify~! Reboot cancelled.')
                    newline()
                else:
                    pass
    except:
        pass

def crypto_tree(crypto_command):
    # User cmd is piped into this function if it matches
    # a command in 'cryptoCmds.txt'. Most functions are
    # called from crypto.py

    if crypto_command in crypto_ipsec:
        crypto_ipsec_options(crypto_command)
    elif crypto_command in crypto_pptp:
        crypto_pptp_options(crypto_command)
    elif crypto_command == 'crypto generate psk':
        generate_psk()
    elif 'crypto del' in crypto_command:
        split_command = crypto_command.split(' ')
        if len(split_command) == 3:
            vpn_name = split_command[2]
            crypto_delete(vpn_name)
        else:
            pass
    elif 'crypto connect' in crypto_command:
        split_command = crypto_command.split(' ')
        if len(split_command) == 3:
            vpn_name = split_command[2]
            crypto_go(vpn_name)
        else:
            pass

def install_tree(install_command):
    # Search winPopenDict.py for relevant command.
    newline()
    try:
        for command in installDict.install_dictionary:
            if command == install_command:
                print('notify~! Attempting installation...')
                newline()
                subprocess.call(installDict.install_dictionary.get(command))
            else:
                pass
    except:
        pass

def cli():
    # CLI prompts user for input as long as prompt_keepalive == 1
    prompt_keepalive = 1
    while prompt_keepalive == 1:
        try:
            # Terminal prompt that accepts commands from the list below
            user_cmd = input("igloo~$ ")

            # Remove whitespace from user input
            strip_cmd = user_cmd.rstrip()

            # Split user input into an array
            split_cmd = strip_cmd.split(' ')

            # Compare user input against help output triggers
            if strip_cmd in helpDict.help_dictionary:
                newline()
                for command in helpDict.help_dictionary:
                    if command == strip_cmd:
                        read_file(helpDict.help_dictionary.get(command))

            elif strip_cmd in quit:
                prompt_keepalive = 0
                newline()
                print('notify~! Exiting Igloo...')
                newline()
                time.sleep(1)
                exit()

            elif strip_cmd == 'calc':
                subprocess.call('calc')

            elif strip_cmd == 'igloo':
                try:
                    subprocess.call(['powershell.exe','Start \'C:\\Program Files\\Igloo\\igloo.exe\''])
                except:
                    newline()
                    print('error~! File not found.')
                    newline()

            # Compare user input against actionable commands. Send to
            # the appropriate command tree (a function) if there is a match.
            elif strip_cmd in show_cmds:
                show_tree(strip_cmd)

            elif strip_cmd in win_os_cmds:
                win_os_tree(strip_cmd)

            elif strip_cmd in win_popen_cmds:
                win_popen_tree(strip_cmd)

            elif strip_cmd in crypto_general:
                crypto_tree(strip_cmd)

            elif 'crypto del' in strip_cmd:
                # A redundant entry is necessary due to the variable
                # nature of certain commands.
                crypto_tree(strip_cmd)

            elif 'crypto connect' in strip_cmd:
                crypto_tree(strip_cmd)

            elif strip_cmd in fwall_show:
                fwall_display(strip_cmd)

            elif strip_cmd in fwall_general:
                fwall_toggle(strip_cmd)

            elif 'fwall entry' in strip_cmd:
                if len(split_cmd) == 7:
                    fwall_rule_config(split_cmd)
                elif len(split_cmd) == 4 and split_cmd[0] == 'no':
                    fwall_delete(split_cmd)
                else:
                    newline()
                    read_file('.\\help-files\\helpFwallEntry.txt')
                    pass

            elif strip_cmd in install_cmds:
                install_tree(strip_cmd)

            elif 'tcp connect' in strip_cmd:
                tcp_connect(strip_cmd)

            elif 'tcp scan' in strip_cmd:
                tcp_scan(strip_cmd)

            elif strip_cmd == 'tcp reset':
                net_reset()

            elif 'no ip route' in strip_cmd:
                no_ip_route(strip_cmd)

            elif 'ip route-cache' in strip_cmd:
                ip_route_cache(strip_cmd)

            elif 'ip ttl' in strip_cmd:
                ip_ttl(strip_cmd)

            elif 'ip address dhcp' in strip_cmd:
                ip_address_dhcp(strip_cmd)

            elif 'ip address' in strip_cmd:
                ip_address_config(strip_cmd)

            elif 'ip tcp window-restart' in strip_cmd \
            or 'ip tcp provider' in strip_cmd \
            or 'ip tcp port-range' in strip_cmd:
                ip_tcp_config(strip_cmd)

            elif strip_cmd in ip_cmds:
                ip_general(strip_cmd)

            elif strip_cmd in ssh_cmds:
                if 'write' in strip_cmd:
                    ssh_write_init(strip_cmd)
                elif 'show' in strip_cmd:
                    print('matched command')
                    ssh_show_init(strip_cmd)
                else:
                    pass

            # Allows newlines/returns in the terminal
            elif strip_cmd == '':
                pass

            else:
                newline()
                print('error~! Invalid command.')
                newline()

        except:
            continue

#admin_check()
splash_screen()
cli()
sys.exit()