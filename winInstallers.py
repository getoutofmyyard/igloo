import subprocess, asyncio
import installDict, uninstallDict

def newline():
    print('')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def install_tree(install_command):
    # Search installlDict.py for relevant command.
    newline()

    split_command = install_command.split(' ')
    if len(split_command) == 3:
        feature = split_command[2]
    elif len(split_command) == 4:
        feature == split_command[2] + ' ' + split_command[3]

    try:
        for command in installDict.install_dictionary:
            if command == install_command:
                print('notify~! Installing \'{}\'. Please wait...'.format(feature))
                install_feature = pshell_decoder(installDict.install_dictionary.get(command))
                if 'WARNING:' in install_feature:
                    print('notify~! Installed \'{}\' successfully! Use \'win reboot\' to finish the installation.'.format(feature))
                    newline()
                elif 'NoChangeNeeded' in install_feature:
                    print('notify~! Feature \'{}\' already installed.'.format(feature))
                    newline()
                elif 'ArgumentNotValid:' in install_feature:
                    print('notify~! Feature is either unknown or has unmet dependencies.')
                    newline()
                elif 'Install-WindowsFeature' in install_feature:
                    print('notify~! This command is supported only on Windows Server machines')
                    newline()
                else:
                    print('notify~! Installed \'{}\' successfully!'.format(feature))
                    newline()
            else:
                pass
    except:
        newline()
        print('error~! Operation terminated unexpectedly')
        newline()
        pass

def uninstall_tree(uninstall_command):
    # Search uninstallDict.py for relevant command.
    newline()

    split_command = uninstall_command.split(' ')
    if len(split_command) == 3:
        feature = split_command[2]
    elif len(split_command) == 4:
        feature == split_command[2] + ' ' + split_command[3]

    try:
        for command in uninstallDict.uninstall_dictionary:
            if command == uninstall_command:
                print('notify~! Uninstalling \'{}\'. Please wait...'.format(feature))
                uninstall_feature = pshell_decoder(uninstallDict.uninstall_dictionary.get(command))
                if 'WARNING:' in uninstall_feature:
                    print('notify~! Uninstalled \'{}\' successfully! Use \'win reboot\' to finish the installation'.format(feature))
                    newline()
                elif 'NoChangeNeeded' in uninstall_feature:
                    print('notify~! Feature \'{}\' is not installed'.format(feature))
                    newline()
                elif 'ArgumentNotValid:' in uninstall_feature:
                    print('notify~! Feature \'{}\' is not installed'.format(feature))
                    newline()
                elif 'Uninstall-WindowsFeature' in install_feature:
                    print('notify~! This command is supported only on Windows Server machines')
                    newline()
                else:
                    print('notify~! Uninstalled \'{}\' successfully'.format(feature))
                    newline()
            else:
                pass
    except:
        newline()
        print('error~! Operation terminated unexpectedly')
        newline()
        pass