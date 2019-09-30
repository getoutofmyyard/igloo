import subprocess

def newline():
    print('')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def update_windows():
    newline()
    print('notify~! Checking local execution policy')
    execution_policy = pshell_decoder('Get-ExecutionPolicy')

    if 'Restricted' in execution_policy \
    or 'AllSigned' in execution_policy:
        newline()
        print('error~! Your pshell execution policy is preventing this action. Try \'powershell policy ?\'')
        newline()

    else:
        print('notify~! Unblocking file path')
        unblock = pshell_decoder('Unblock-File -Path .\\updateWindows.ps1 | Out-Null')
        error = "cannot be loaded"
        print('notify~! Searching for updates')
        subprocess.call(['powershell.exe', '.\\updateWindows.ps1'])
        newline()