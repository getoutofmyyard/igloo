import subprocess, os, sys, ctypes, netmiko, getpass, random, webbrowser
import asyncio, re
import conversion, helpDict, showDict, winOsDict, winPopenDict, installDict
import webDict, uninstallDict, manual
from datetime import datetime
from crypto import *
from fwall import *
from tcp import *
from ipconf import *
from sshSet import *
from updateWindows import *
from winInstallers import *
from fping import *
from bgpRouting import *

yes = ['y', 'Y', 'yes', 'Yes']
no = ['n', 'N', 'no', 'No']
quit = ['exit','end','bye','quit','leave','esc']


#Common cmd.exe commands. Checked against user input
#and invokes cmd.exe when these terms are discovered
cmd_exe_options = ['tftp','ftp','telnet','netsh','nslookup',\
                   'ping','tracert']

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
uninstall_cmds = parse_file('.\\command-sets\\uninstallCmds.txt')
ip_cmds = parse_file('.\\command-sets\\ipCmds.txt')
show_cmds = parse_file('.\\command-sets\\showCmds.txt')
win_os_cmds = parse_file('.\\command-sets\\winOsCmds.txt')
win_popen_cmds = parse_file('.\\command-sets\\winPopenCmds.txt')
ssh_cmds = parse_file('.\\command-sets\\sshCmds.txt')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode],\
    stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def admin_check():
    # Checks to see if user ran Igloo as admin.
    # If not, prompt user to elevate privileges.
    is_an_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if is_an_admin == 0:
        with open('.\\miscellaneous\\no_admin.txt','r') as file:
            print(file.read())
            cli()
            sys.exit()

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
                elif 'Get-BgpPeer' in output \
                or 'Get-BgpRouter' in output:
                    print('notify~! BGP routing is not enabled for this machine')
                    newline()
                elif 'Get-BgpRouteAggregate' in output:
                    newline()
                    print('notify~! This machine has unmet dependencies for BGP routing. Use \'router bgp enable\'')
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
    elif crypto_command == 'crypto generate rsa':
        generate_rsa()
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

def int_tree(int_command):

    split_cmd = int_command.split(' ')
    int_index = split_cmd[1]

    if 'on' in int_command:
        get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | Select-Object Name | Format-Table -AutoSize'.format(int_index))

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
            print('notify~! Interface does not exist. Use \'show int\' and \'int ?\' for help')
            newline()
        else:
            newline()
            print('notify~! Interface {} has been enabled'.format(int_name))
            newline()

    elif 'off' in int_command:

        split_cmd = int_command.split(' ')
        int_index = split_cmd[1]

        get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | Select-Object Name | Format-Table -AutoSize'.format(int_index))

        split_list = get_int_list.split('----')
        get_name = split_list[1]
        int_name = '\'' + get_name.strip() + '\''

        disable_adapter = pshell_decoder('Disable-NetAdapter -Name {} -Confirm:$False'.format(int_name))


        if 'Disable-NetAdapter : Access is denied.' in disable_adapter:
            newline()
            print('error~! This action requires admin rights!')
            newline()
        elif 'No MSFT_NetAdapter objects found' in disable_adapter:
            newline()
            print('notify~! Interface does not exist. Use \'show int\' and \'int ?\' for help')
            newline()
        else:
            newline()
            print('notify~! Interface {} has been disabled'.format(int_name))
            newline()

def router_tree(router_command):
    if 'bgp' in router_command:
        bgp_routing(router_command)
    elif 'rip' in router_command:
        rip_routing()
    elif 'ospf' in router_command:
        ospf_routing()
    else:
        return

def cli():
    prompt_keepalive = 1

    # CLI prompts user for input as long as prompt_keepalive == 1
    while prompt_keepalive == 1:
        try:
            if len(sys.argv) > 1:
                user_cmd = ' '.join(sys.argv[1:])
                prompt_keepalive = 0
            else:
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
                    newline()
                    try_exe = pshell_decoder('Start \'C:\\Program Files\\Igloo\\igloo.exe\'')
                    if 'Start' in try_exe:
                        print('error~! File not found!')
                    newline()
                except:
                    newline()
                    print('error~! File not found.')
                    newline()

            elif 'man' in strip_cmd:
                for line in manual.manual_dictionary:
                    if line == strip_cmd:
                        key = manual.manual_dictionary.get(line)
                        newline()
                        print('notify~! Opening {} with default browser.'.format(key))
                        webbrowser.open_new(key)
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

            elif 'router' in strip_cmd:
                router_tree(strip_cmd)

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

            elif strip_cmd in uninstall_cmds:
                uninstall_tree(strip_cmd)

            elif 'int' in strip_cmd:
                int_tree(strip_cmd)

            elif 'tcp connect' in strip_cmd:
                tcp_connect(strip_cmd)

            elif 'tcp scan' in strip_cmd:
                tcp_scan(strip_cmd)

            elif strip_cmd == 'tcp reset':
                net_reset()

            elif 'no ip route' in strip_cmd:
                no_ip_route(strip_cmd)

            elif 'ip route' in strip_cmd:
                ip_route(strip_cmd)

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
                    ssh_show_init(strip_cmd)
                else:
                    pass

            elif 'web' in strip_cmd:
                for line in webDict.web_dictionary:
                    if line == strip_cmd:
                        key = webDict.web_dictionary.get(line)
                        newline()
                        print('notify~! Opening {} with default browser.'.format(key))
                        webbrowser.open_new(key)
                        newline()
                    else:
                        pass

            elif strip_cmd == 'notepad':
                subprocess.call(['notepad.exe'])

            elif strip_cmd == 'update':
                update_windows()

            elif 'fping' in strip_cmd:
                fping_script()

            elif split_cmd[0] in cmd_exe_options:
                try:
                    os.system(strip_cmd)
                    newline()
                except KeyboardInterrupt:
                    newline()
                    newline()

            # Allows newlines/returns in the terminal
            elif strip_cmd == '':
                pass

            else:
                newline()
                print('error~! Invalid command.')
                newline()

        except:
            continue

admin_check()

if len(sys.argv) <= 1:
    splash_screen()

cli()
sys.exit()
