import installDict
import uninstallDict
from common import pshell_decoder, newline

def install_tree(install_command):
    # Search installlDict.py for relevant command.
    newline()

    split_command = install_command.split(' ')

    if len(split_command) == 3:
        feature = split_command[2]

    elif len(split_command) == 4:
        feature == split_command[2] + ' ' + split_command[3]

    else:
        pass

    for command in installDict.install:

        if command == install_command:

            print('notify~! Installing \'{}\'...'.format(feature))

            install_feature = pshell_decoder(installDict.install.get(command))

            if 'WARNING:' in install_feature:
                print('notify~! Installed \'{}\' successfully!'.format(feature))
                print('notify~! Use \'win reboot\' to complete the install.')
                newline()

            elif 'NoChangeNeeded' in install_feature:
                print('notify~! Feature \'{}\' already installed.'.format(feature))
                newline()

            elif 'ArgumentNotValid:' in install_feature:
                print('notify~! Feature is either unknown or '\
                    + 'has unmet dependencies.')
                newline()

            elif ('The target' in install_feature
                  or 'is not recognized' in install_feature):

                print('notify~! This command is supported only on '\
                    + 'Windows Server machines')
                newline()

            else:
                newline()
                print('error~! An unknown exception occurred.')
                newline()
        else:
            pass

def uninstall_tree(uninstall_command):
    # Search uninstallDict.py for relevant command.
    newline()

    split_command = uninstall_command.split(' ')

    if len(split_command) == 3:
        feature = split_command[2]

    elif len(split_command) == 4:
        feature == split_command[2] + ' ' + split_command[3]

    for command in uninstallDict.uninstall:
        if command == uninstall_command:

            print('notify~! Uninstalling \'{}\'. Please wait...\
                '.format(feature))

            uninstall_feature = (pshell_decoder(
                uninstallDict.uninstall.get(command)))

            if 'WARNING:' in uninstall_feature:
                print('notify~! Uninstalled \'{}\' successfully!'.format(feature))
                print('notify~! Use \'win reboot\' to finish the uninstall.')
                newline()

            elif 'NoChangeNeeded' in uninstall_feature:
                print('notify~! Feature \'{}\' is not installed.'.format(feature))
                newline()

            elif 'ArgumentNotValid:' in uninstall_feature:
                print('notify~! Feature is either unknown or '\
                    + 'has unmet dependencies.')
                newline()

            elif ('The target' in uninstall_feature
                  or 'is not recognized' in uninstall_feature):

                print('notify~! This command is supported only on '\
                    + 'Windows Server machines')
                newline()

            else:
                newline()
                print('error~! An unknown exception occurred.')
                newline()

        else:
            pass
