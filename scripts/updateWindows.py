import subprocess
from common import pshell_decoder, newline

def update_windows():
    newline()

    print('notify~! Checking local execution policy...')

    execution_policy = pshell_decoder('Get-ExecutionPolicy')

    if 'Restricted' in execution_policy \
    or 'AllSigned' in execution_policy:
        newline()
        print('error~! Your pshell execution policy is preventing '\
            + 'this action. Try \'powershell policy ?\'')
        newline()

    else:
        print('notify~! Unblocking file path...')

        unblock = pshell_decoder('Unblock-File -Path \'C:\\Program Files'\
            + ' (x86)\\igloo\\scripts\\updateWindows.ps1\' | Out-Null')

        error = "cannot be loaded"

        print('notify~! Searching for updates...')

        get_current_dir = pshell_decoder('Get-Location')

        clean_up = get_current_dir.replace('\r\n', '').replace(' ', '')

        split_it = clean_up.split('----')

        subprocess.call(['powershell.exe', 'Set-Location -Path \"C:\\Program Files'\
            + ' (x86)\" | powershell .\\igloo\\scripts\\updateWindows.ps1'])

        subprocess.call(['powershell.exe', 'Set-Location -Path ' \
            + split_it[1]] + ' | Out-Null')
