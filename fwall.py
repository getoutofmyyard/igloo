import subprocess, os 

def newline():
    print('')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def fwall_rule_config(rule_arg):
    # Assigns firewall variables and pipes them into fwall_rule_build
    fwall_rule_name = rule_arg[2]
    fwall_rule_action = rule_arg[3]
    transport_protocol = rule_arg[4]
    port_number = rule_arg[5]
    direction = rule_arg[6]

    if fwall_rule_action == 'permit':
        fwall_rule_action = 'Allow'
    elif fwall_rule_action == 'deny':
        fwall_rule_action = 'Block'
    else:
        pass

     # Executes powershell command to create a new firewall rule with vars provided.
    newline()
    print('notify~! Creating firewall rule \'{}\'...'.format(fwall_rule_name))

    os.system('powershell New-NetFirewallRule -DisplayName ' + fwall_rule_name + \
              ' -Direction ' + direction + ' -LocalPort ' + port_number + \
              ' -Protocol ' + transport_protocol + ' -Action ' + fwall_rule_action + \
              ' -Enabled True > nul 2>&1')

    print('notify~! Firewall rule \'{}\' created: {}ing {} {} {}bound.'.format(fwall_rule_name, \
           fwall_rule_action, transport_protocol, port_number, direction.lower()))
    newline()

def fwall_display(show_fwall_command):
    # Record the traffic direction.
    if show_fwall_command == 'show fwall out': 
        direction = 'Outbound'
    elif show_fwall_command == 'show fwall in':
        direction = 'Inbound'
    # Fetch and sort firewall data using PowerShell.
    newline()
    print('notify~! Fetching...')
    newline()
    subprocess.call(['powershell.exe','Get-NetFirewallRule -Direction '+direction+\
                    ' -Enabled True | Sort-Object -Property DisplayName | ' + \
                    'Select-Object -Property DisplayName,Profile,Action,Direction'])

def fwall_toggle(fwall_cmd):
    #Firewall configuration commands.

    fwall_profile_dictionary = {
        'fwall on':'Set-NetFirewallProfile -Profile Domain,Private,Public -Enabled True',
        'fwall off':'Set-NetFirewallProfile -Profile Domain,Private,Public -Enabled False',
        'fwall dom on':'Set-NetFirewallProfile -Profile Domain -Enabled True',
        'fwall dom off':'Set-NetFirewallProfile -Profile Domain -Enabled False',
        'fwall pub on':'Set-NetFirewallProfile -Profile Public -Enabled True',
        'fwall pub off':'Set-NetFirewallProfile -Profile Public -Enabled False',
        'fwall priv on':'Set-NetFirewallProfile -Profile Private -Enabled True',
        'fwall priv off':'Set-NetFirewallProfile -Profile Private -Enabled False'
    }

    for line in fwall_profile_dictionary:
        if line == fwall_cmd:
            pshell_decoder(fwall_profile_dictionary.get(line))

    if fwall_cmd == 'fwall on':
        newline()
        print ('notify~! Firewall enabled globally')
        newline()
    elif fwall_cmd == 'fwall off':
        newline()
        print ('notify~! Firewall disabled globally')
        newline()
    elif fwall_cmd == 'fwall dom on':
        newline()
        print ('notify~! Firewall enabled for domain networks')
        newline()
    elif fwall_cmd == 'fwall dom off':
        newline()
        print ('notify~! Firewall disabled for domain networks')
        newline()
    elif fwall_cmd == 'fwall pub on':
        newline()
        print ('notify~! Firewall enabled for public networks')
        newline()
    elif fwall_cmd == 'fwall pub off':
        newline()
        print ('notify~! Firewall disabled for public networks')
        newline()
    elif fwall_cmd == 'fwall priv on':
        newline()
        print ('notify~! Firewall enabled for private networks')
        newline()
    elif fwall_cmd == 'fwall priv off':
        newline()
        print ('notify~! Firewall disabled for private networks')
        newline()

def fwall_delete(delete_statement):
        # if firewall rule exists, delete. if not
        fwall_rule_name = delete_statement[3]
        newline()
        print('notify~! Attempting to delete firewall rule \'{}\'...'.format(fwall_rule_name))
        not_found_error = "ObjectNotFound"
        remove_rule = pshell_decoder('Remove-NetFirewallRule -DisplayName ' + fwall_rule_name)
        if not_found_error in remove_rule:
            print("notify~! Rule does not exist.")
            newline()
        else:
            print('notify~! Firewall rule \'{}\' was deleted.'.format(fwall_rule_name))
            newline()