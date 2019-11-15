import subprocess, asyncio, installDict, uninstallDict
from getpass import getpass

letters_lower = 'abcdefghijklmnopqrstuvwxyz'
letters_upper = letters_lower.upper()
symbols = '!@#$%^&*()_+=-`~'
numbers = '1234567890'


def newline():
    print('')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode],\
    stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def active_directory_deployment(command):

    try:

        domain_loop = 1
        newline()

        while domain_loop == 1:
            domain = input('input~! Enter a domain name: ')
            if any(domain) == True:
                domain_loop = 0
                break
            else:
                pass

        ip_loop = 1
        newline()

        while ip_loop == 1:
            ip = input('input~! Enter a static IP address for the DNS server: ')

            if any(ip) == True \
            and '.' in ip:

                octets = ip.split('.')

                for decimal in octets:

                    integer = int(decimal)

                    if integer < 0 \
                    or integer > 255:
                        newline()
                        print('error~! Invalid IP address.')
                        newline()
                        ip_loop = 0
                        return

                    else:
                        pass

                newline()
                print('notify~! Checking static IP addresses for entry')

                check_ip = pshell_decoder('Get-NetIPAddress -AddressFamily IPv4 | Select-Object -Property IPAddress | Format-Table -HideTableHeaders')

                clean_output = check_ip.replace('\r','')
                cleaner_output = clean_output.lstrip(' ')
                ip_address_list = cleaner_output.split('\n')

                ticker = 1

                for ip_address in ip_address_list:
                    ticker = ticker + 1
                    if ip == ip_address.strip(' '):
                        print('notify~! Static IP validated')
                        ip_loop = 0
                        break
                    else:
                        if len(ip_address_list) == ticker - 1:
                            newline()
                            print('error~! This IP address is not configured. Use \'show ip address\' for a list')
                            newline()
                            ip_loop = 0
                            return
                        else:
                            pass


                ip_loop = 0

            else:
                pass

        pass_loop = 1
        newline()

        try:
            while pass_loop == 1:

                smap = getpass('input~! Enter a Safemode Administrator Password: ')

                if any(smap) == True:

                    pass_loop2 = 1

                    while pass_loop2 == 1:
                        smap_confirmed = getpass('input~! Confirm the Safemode Administrator Password: ')

                        if any(smap_confirmed) == True:

                            if smap == smap_confirmed:
                                if len(smap_confirmed) >= 10:

                                    nums = False
                                    lower = False
                                    upper = False
                                    syms = False

                                    ticker = 1

                                    for char in smap_confirmed:
                                        ticker = ticker + 1

                                        if char in numbers:
                                            nums = True
                                        if char in letters_lower:
                                            lower = True
                                        if char in letters_upper:
                                            upper = True
                                        if char in symbols:
                                            syms = True

                                        if len(smap_confirmed) == ticker - 1:

                                            if nums == True \
                                            and lower == True \
                                            and upper == True \
                                            and syms == True:

                                                pass_loop2 = 0
                                                pass_loop = 0

                                            else:
                                                newline()
                                                print('error~! Your password must be at least 10 characters and contain uppercase, lowercase, symbols, and numbers')
                                                newline()
                                                pass_loop2 = 0

                                else:
                                    newline()
                                    print('error~! Your password must be at least 10 characters and contain uppercase, lowercase, symbols, and numbers')
                                    newline()
                                    pass_loop2 = 0

                            else:
                                newline()
                                print('error~! Password mismatch. Try again.')
                                newline()
                                pass_loop2 = 0

        except:
            newline()
            print('error~! Operation has been terminated')
            newline()
            return

    except:
        newline()
        print('error~! Operation terminated unexpectedly')
        newline()
        return

    newline()
    print('notify~! Checking for existing AD-DS installation')

    check_adds_install = pshell_decoder('Get-WindowsFeature -Name AD-Domain-Services | Format-Table -HideTableHeaders')

    if 'Get-WindowsFeature' in check_adds_install:
        newline()
        print('error~! This command requires Windows Server OS')
        newline()
        return

    else:

        clean_output = check_adds_install.replace('\r\n', '')
        split_output = clean_output.split()
        install_state = split_output[6]

        if install_state == 'Installed':
            print('notify~! AD-DS is installed. Skipping...')
            pass

        else:
            print('notify~! AD-DS not found. Installing...')
            subprocess.call(['powershell.exe','Install-WindowsFeature -Name AD-Domain-Services -IncludeAllSubFeature | Out-Null'])
            print('notify~! AD-DS installed successfully')
        
        print('notify~! Checking for existing DNS installation')

        check_dns_install = pshell_decoder('Get-WindowsFeature -Name DNS | Format-Table -HideTableHeaders')
        clean_output = check_dns_install.replace('\r\n', '')
        split_output = clean_output.split()

        if split_output[4] == 'Installed':
            print('notify~! DNS is installed. Skipping...')
            pass
        else:
            print('notify~! DNS not found. Installing...')
            pshell_decoder('Install-WindowsFeature -Name DNS -IncludeAllSubFeature | Out-Null')
            print('notify~! DNS installed successfully')

    # install the ADDSDeployment module

    print('notify~! Installing AD-DS deployment module')
    subprocess.call(['powershell.exe','Import-Module ADDSDeployment'])

    print('notify~! Configuring DNS forward lookup zone')
    create_fwd_zone = pshell_decoder('Add-DnsServerPrimaryZone -Name {} -ReplicationScope Forest -PassThru'.format(domain))
    print('notify~! Creating AD-DS forest')
    install_forest = pshell_decoder('Install-ADDSForest -DomainName “{}” -SafemodeAdministratorPassword (ConvertTo-SecureString "{}" -AsPlainText -Force)'.format(domain, smap_confirmed))
    newline()
    parse_output = install_forest.split('.')
    for item in parse_output:
        if item == ' Role change is in progress or this computer needs to be restarted':
            newline()
            print('error~! Incomplete installations detected. Use \'win reboot\' and run this command again.')
            newline()
            return

    