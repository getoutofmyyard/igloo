import subprocess
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


def package_install(pshell_command, feature_name):

    split_name = feature_name.split(' ')
    if len(split_name) == 3:
        f_name = split_name[2]
    elif len(split_name) == 4:
        f_name = split_name[2] + ' ' + split_name[3]

    install_package = pshell_decoder(pshell_command)
    if 'WARNING:' in install_package:
        pass
    elif 'NoChangeNeeded' in install_package:
        print('notify~! Feature \'{}\' already installed.'.format(f_name))
    elif 'ArgumentNotValid:' in install_package:
        print('notify~! Feature {} unknown or has unmet dependencies.'.format(f_name))
    else:
        print('notify~! Installed \'{}\''.format(f_name))
        pass

def install_tree(package_command):
    # Search installlDict.py for relevant command.
    newline()
    split_cmd = package_command.split(' ')
    package = split_cmd[1]

    try:
        for feature in installDict.install_dictionary:
            powershell_cmd = installDict.install_dictionary.get(feature)
            if 'iis' in feature \
            and 'iis' in package_command:
                package_install(powershell_cmd, feature)
            elif 'rsat' in feature \
            and 'rsat' in package_command:
                package_install(powershell_cmd, feature)
            elif 'ad-cs' in feature \
            and 'ad-cs' in package_command:
                package_install(powershell_cmd, feature)
            elif 'ad-rights' in feature \
            and 'ad-rights' in package_command:
                package_install(powershell_cmd, feature)
            elif 'app-server' in feature \
            and 'app-server' in package_command:
                package_install(powershell_cmd, feature)
            else:
                pass
        newline()
        print('notify~! Installed package \'{}\' successfully. Use \'win reboot\' to finish'.format(package))
        print('notify~! installation of new features, if applicable.')
        newline()
    except:
        newline()
        print('error~! Operation terminated unexpectedly')
        newline()
        pass

def package_uninstall(pshell_command, feature_name):

    split_name = feature_name.split(' ')
    if len(split_name) == 3:
        f_name = split_name[2]
    elif len(split_name) == 4:
        f_name = split_name[2] + ' ' + split_name[3]

    install_package = pshell_decoder(pshell_command)
    if 'WARNING:' in install_package:
        pass
    elif 'NoChangeNeeded' in install_package:
        print('notify~! Feature \'{}\' not installed'.format(f_name))
    elif 'ArgumentNotValid:' in install_package:
        print('notify~! Feature {} unknown or has unmet dependencies.'.format(f_name))
    else:
        print('notify~! Uninstalled \'{}\''.format(f_name))
        pass

def uninstall_tree(package_command):
    # Search installlDict.py for relevant command.
    newline()
    split_cmd = package_command.split(' ')
    package = split_cmd[1]

    try:
        for feature in uninstallDict.uninstall_dictionary:
            powershell_cmd = uninstallDict.uninstall_dictionary.get(feature)
            if 'iis' in feature \
            and 'iis' in package_command:
                package_uninstall(powershell_cmd, feature)
            elif 'rsat' in feature \
            and 'rsat' in package_command:
                package_uninstall(powershell_cmd, feature)
            elif 'ad-cs' in feature \
            and 'ad-cs' in package_command:
                package_uninstall(powershell_cmd, feature)
            elif 'ad-rights' in feature \
            and 'ad-rights' in package_command:
                package_uninstall(powershell_cmd, feature)
            elif 'app-server' in feature \
            and 'app-server' in package_command:
                package_uninstall(powershell_cmd, feature)
            else:
                pass
        newline()
        print('notify~! Uninstalled package \'{}\' successfully. Use \'win reboot\' to finish'.format(package))
        print('notify~! removal of features.')
        newline()
    except:
        newline()
        print('error~! Operation terminated unexpectedly')
        newline()
        pass