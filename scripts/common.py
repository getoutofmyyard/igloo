import subprocess

yes = ['y', 'Y', 'yes', 'Yes']
no = ['n', 'N', 'no', 'No']

quit = ['exit','end','bye','quit','leave','esc']

#invoke cmd.exe when these terms are discovered
cmd_exe_options = ['tftp','ftp','telnet','netsh','nslookup',\
                   'ping','tracert','ipconfig', 'dir', \
                   'whoami']

pshell_exe_options = ['ls','pwd', 'rm', 'rmdir', 'mkdir', \
                      'xcopy','copy','robocopy','cat']

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

def splash_screen():
    # Displays the Igloo splash screen
    newline()
    read_file('.\\miscellaneous\\splash.txt')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode],\
    stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output