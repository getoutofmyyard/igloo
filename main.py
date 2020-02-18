import ctypes
import os
import subprocess
import sys
import webbrowser

sys.path.insert(1, '.\\scripts')

from bgpRouting import *
from common import *
from crypto import *
from deploy import *
from fping import *
from fwall import *
from interfaces import *
from ipconf import *
from showExcept import *
from sshSet import *
from tcp import *
from updateWindows import *
from winInstallers import *
import helpDict
import manual
import showDict
import webDict
import winOsDict
import winPopenDict


def parse_file(filepath):
    with open(filepath) as file:
        split_file = file.read().split('\n')
        return split_file

# Command lists

CRYPTO_GENERAL = parse_file('.\\command-sets\\cryptoCmds.txt')
CRYPTO_IPSEC = parse_file('.\\command-sets\\cryptoIpsecCmds.txt')
CRYPTO_PPTP = parse_file('.\\command-sets\\cryptoPptpCmds.txt')
FWALL_GENERAL = parse_file('.\\command-sets\\fwallCmds.txt')
FWALL_SHOW = parse_file('.\\command-sets\\fwallShowCmds.txt')
INSTALL_CMDS = parse_file('.\\command-sets\\installCmds.txt')
UNINSTALL_CMDS = parse_file('.\\command-sets\\uninstallCmds.txt')
IP_CMDS = parse_file('.\\command-sets\\ipCmds.txt')
SHOW_CMDS = parse_file('.\\command-sets\\showCmds.txt')
WIN_OS_CMDS = parse_file('.\\command-sets\\winOsCmds.txt')
WIN_POPEN_CMDS = parse_file('.\\command-sets\\winPopenCmds.txt')
SSH_CMDS = parse_file('.\\command-sets\\sshCmds.txt')


# Check to see if user ran Igloo as admin
def admin_check():

    is_an_admin = ctypes.windll.shell32.IsUserAnAdmin()

    if is_an_admin == False:
        with open('.\\miscellaneous\\no_admin.txt', 'r') as file:
            print(file.read())
            cli()
            sys.exit()


# Return current username
def who_am_i():
    get_username = pshell_decoder('whoami')
    format_username = get_username.split("\\", 1)[1].strip()
    return format_username


def check_pshell_profile():
    # creates powershell alias for igloo upon launch.
    # skip this process if execution policy is resrictive.

    try:
        exec_policy = pshell_decoder('Get-ExecutionPolicy')

        with open('C:\\Windows\\System32\\\
            WindowsPowerShell\\v1.0\\profile.ps1', 'r') as file:
            # format the file
            read_file = file.read()
            split_file = read_file.split('\n')

            ticker = 1

            for line in split_file:
                ticker = ticker + 1

                if line == 'Set-Alias -Name igloo -Value \'.\\igloo.exe\'':
                    ps_file = 0
                    break

                else:
                    ps_file = 1

                    if len(split_file) == ticker - 1 and ps_file == 1:
                        with open('C:\\Windows\\System32\\WindowsPowerShell\
                            \\v1.0\\profile.ps1', 'a') as file:

                            file.write('\nSet-Alias -Name igloo -Value \
                                \'.\\igloo.exe\'')

                    else:
                        pass

    except FileNotFoundError:

        if 'Restricted' in exec_policy:
            pass

        else:
            with open('C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\\
                profile.ps1', 'w+') as file:

                file.write('Set-Alias -Name igloo -Value \'.\\igloo.exe\'')


# Search winOsDict.py for relevant command
def win_os_tree(win_os_command):

    try:
        for command in winOsDict.win_os_command_set:
            if command == win_os_command:
                os.system(winOsDict.win_os_command_set.get(command))
            else:
                pass
    except:
        pass


# Search winPopenDict.py for relevant command.
def win_popen_tree(win_popen_command):
    
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

                reboot_confirm = input('confirm~! Are you sure you' \
                    + 'want to reboot? (y/n) ')

                if reboot_confirm in yes:
                    reboot_loop_keepalive = 0

                    subprocess.Popen('shutdown /r /t 0')

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

    if crypto_command in CRYPTO_IPSEC:
        crypto_ipsec_options(crypto_command)
    elif crypto_command in CRYPTO_PPTP:
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

def cli():

    prompt_keepalive = 1

    while prompt_keepalive == 1:

        try:

            if len(sys.argv) > 1:
                user_cmd = ' '.join(sys.argv[1:])
                prompt_keepalive = 0

            else:
                user_cmd = input("igloo~$ ")

            strip_cmd = user_cmd.rstrip()
            split_cmd = strip_cmd.split(' ')

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

            elif strip_cmd == 'igloo':
                try:
                    newline()
                    try_exe = pshell_decoder('Start \'C:\\Program Files\
                        \\Igloo\\igloo.exe\'')
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
                        print('notify~! Opening {} with default browser.\
                            '.format(key))
                        webbrowser.open_new(key)
                        newline()

            elif strip_cmd == 'deploy ad-ds':
                active_directory_deployment(strip_cmd)
            elif strip_cmd == 'deploy bgp':
                deploy_bgp()
            elif strip_cmd in SHOW_CMDS:
                show_tree(strip_cmd)
            elif strip_cmd in WIN_OS_CMDS:
                win_os_tree(strip_cmd)
            elif strip_cmd in WIN_POPEN_CMDS:
                win_popen_tree(strip_cmd)
            elif strip_cmd in CRYPTO_GENERAL:
                crypto_tree(strip_cmd)
            elif 'bgp' in strip_cmd:
                bgp_routing(strip_cmd)
            elif 'crypto del' in strip_cmd:
                crypto_tree(strip_cmd)
            elif 'crypto connect' in strip_cmd:
                crypto_tree(strip_cmd)
            elif strip_cmd in FWALL_SHOW:
                fwall_display(strip_cmd)
            elif strip_cmd in FWALL_GENERAL:
                fwall_toggle(strip_cmd)
            elif 'fwall entry' in strip_cmd:
                if len(split_cmd) == 7:
                    fwall_rule_config(split_cmd)
                elif len(split_cmd) == 4 and split_cmd[0] == 'no':
                    fwall_delete(split_cmd)
                else:
                    newline()
                    read_file('.\\help-files\\helpFwallEntry.txt')
            elif strip_cmd in INSTALL_CMDS:
                install_tree(strip_cmd)
            elif strip_cmd in UNINSTALL_CMDS:
                uninstall_tree(strip_cmd)
            elif 'int' in strip_cmd:
                int_tree(strip_cmd)
            elif 'tcp scan' in strip_cmd:
                tcp_scan(strip_cmd)
            elif 'tcp ping' in strip_cmd:
                tcp_ping(strip_cmd)
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
            elif ('ip tcp window-restart' in strip_cmd
                   or 'ip tcp provider' in strip_cmd
                   or 'ip tcp port-range' in strip_cmd):
                ip_tcp_config(strip_cmd)
            elif strip_cmd in IP_CMDS:
                ip_general(strip_cmd)
            elif strip_cmd in SSH_CMDS:
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
                        print('notify~! Opening {} with default browser.\
                            '.format(key))
                        webbrowser.open_new(key)
                        newline()
                    else:
                        pass
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

            elif split_cmd[0] in pshell_exe_options:
                try:
                    subprocess.call(['powershell.exe', strip_cmd])
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
check_pshell_profile()
if len(sys.argv) <= 1:
    splash_screen()

cli()
sys.exit()
