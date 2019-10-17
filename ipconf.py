import subprocess, os, re
from re import *
from conversion import *

def newline():
    print('')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode], stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

def os_error_message():
    newline()
    print('error~! Command not supported for this OS.'\
    +' Enterprise or Server edition required.')
    newline()

def provider_announcement(tcp_provider):
    newline()
    print('notify~! TCP congestion provider has been set to {}.'.format(tcp_provider))
    newline()

def no_ip_route(delete_this_route):
    split_arg = delete_this_route.split(' ')
    dest_prefix = split_arg[3]
    rm_route = pshell_decoder('Remove-NetRoute -DestinationPrefix '+dest_prefix +' -Confirm:$false')
    if 'No MSFT_NetRoute objects found' in rm_route:
        newline()
        print('error~! Route does not exist in table.')
        newline()
    else:
        newline()
        print('notify~! Route to prefix %s has been deleted.' \
               % dest_prefix)
        newline()

def ip_route(add_this_route):
    split_arg = add_this_route.split(' ')

    if len(split_arg) == 7 \
    and 'metric' in split_arg:

        dest_prefix = split_arg[2]
        next_hop = split_arg[3]
        int_index = split_arg[4]
        route_metric = split_arg[6]
        add_route = pshell_decoder('new-netroute -DestinationPrefix '+dest_prefix+' -ifIndex ' +int_index + ' -NextHop '+ next_hop +' -RouteMetric ' + route_metric)
        if 'Instance MSFT_NetRoute already exists' in add_route:
            newline()
            print('error~! Route to destination prefix %s already in table.'\
                   % dest_prefix)
            newline()
        else:
            newline()
            print('notify~! Route to prefix %s created. M=%s.'\
                   % (dest_prefix, route_metric))
            newline()

    elif len(split_arg) == 5 \
    and 'metric' not in split_arg:

        dest_prefix = split_arg[2]
        next_hop = split_arg[3]
        int_index = split_arg[4]

        add_route = pshell_decoder('new-netroute -DestinationPrefix '+dest_prefix+' -ifIndex '+int_index+' -NextHop '+next_hop+' | Out-Null')

        if 'Instance MSFT_NetRoute already exists' in add_route:
            newline()
            print('error~! Route to destination prefix %s already in table.'\
                   % dest_prefix)
            newline()
        else:
            newline()
            print('notify~! Route to destination prefix %s has been created.'\
                   % dest_prefix)
            newline()

def ip_route_cache(route_cache_arg):
    number_present = bool(re.search(r'\d', route_cache_arg))
    split_arg = route_cache_arg.split(' ')
    cache_limit = split_arg[3]
    if len(split_arg) == 4 \
    or len(split_arg) == 5 \
    and number_present == True:

        subprocess.call(['powershell.exe','Set-NetIpv4Protocol ' \
                          + '-RouteCacheLimitEntries ' + cache_limit])
        newline()
        print('notify~! Maximum number of route cache entries set to %s.'\
               % cache_limit)
        newline()
    else:
        pass

def ip_ttl(ip_ttl_arg):
    number_present = bool(re.search(r'\d', ip_ttl_arg))
    split_arg = ip_ttl_arg.split(' ')

    if number_present == True:
        packet_ttl = split_arg[2]
        ttl_as_integer = int(packet_ttl)

        if ttl_as_integer <= 255 \
        and ttl_as_integer > 0:
            subprocess.call(['powershell.exe','Set-NetIpv4Protocol -DefaultHopLimit '+ packet_ttl])
            newline()
            print('notify~! TTL for outgoing packets set to %s.' % packet_ttl)
            newline()
        else:
            newline()
            print('error~! Invalid TTL. Valid range is 1 to 255.')
            newline()
    else:
        pass

def ip_address_config(ip_address_arg):
    split_arg = ip_address_arg.split(' ')

    if len(split_arg) == 6:
        ip_address = split_arg[2]
        subnet_mask = split_arg[3]
        default_gateway = split_arg[4]
        interface_index = split_arg[5]
        cidr_lookup = cidr_dictionary.get(subnet_mask)

        newline()
        print('notify~! Initializing route table lookup')

        route_lookup = pshell_decoder('get-netroute -addressfamily ipv4 | '\
                       +'select-object -property destinationprefix')

        print('notify~! Route lookup succeeded')

        if '0.0.0.0/0' in route_lookup.split('\n'):
            print('notify~! Flushing old default route from table')
            subprocess.call(['powershell', 'Remove-NetRoute -InterfaceIndex '\
            +interface_index+' -destinationprefix 0.0.0.0/0 -Confirm:$False'\
            + ' | Out-Null'])

        remove_address = pshell_decoder('Remove-NetIpAddress -InterfaceIndex '\
                       +interface_index+' -AddressFamily IPv4 -Confirm:$False | '\
                       + 'Out-Null')

        if 'Default loopback address cannot be deleted' in remove_address:
            newline()
            print('error~! Cannot change the default loopback address.')
            newline()

        else:
            print('notify~! Configuring address')

            subprocess.call(['powershell.exe','Set-NetIPInterface -InterfaceIndex'\
            ' ' + interface_index + ' -Dhcp Disabled | Out-Null'])

            print('notify~! Disabling DHCP')

            gateway_config = pshell_decoder('New-NetIPAddress -InterfaceIndex '\
                             + interface_index +' -IPAddress '+ip_address \
                             +' -PrefixLength '+ cidr_lookup +' -DefaultGateway '\
                             + default_gateway)

            print('notify~! Restarting adapter')
            get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | Select-Object Name | Format-Table -AutoSize'.format(interface_index))
            split_list = get_int_list.split('----')
            get_name = split_list[1]
            int_name = '\'' + get_name.strip() + '\''
            reset_adapter = pshell_decoder('Restart-NetAdapter -Name'\
            +' {}'.format(int_name))


            if 'Instance DefaultGateway already exists' in gateway_config:

                assign_address = pshell_decoder('New-NetIPAddress -InterfaceIndex '\
                + interface_index +' -IPAddress ' + ip_address + ' -PrefixLength ' \
                + cidr_lookup + ' | Out-Null')

                if 'Inconsistent parameters PolicyStore' in assign_address:
                    newline()
                    print('error~! Interface \'{}\' is disabled. Please enable it and try again.'.format(interface_index))
                    newline()

                elif 'The object already exists.' in assign_address:
                    newline()
                    print('error~! Address overlaps with another interface.')
                    newline()
                else:
                    newline()
                    print('notify~! IP address {}/{} has been configured for the interface. GW={}'.format(ip_address,cidr_lookup, default_gateway))
                    newline()
            else:
                pass

    elif len(split_arg) == 5 \
    and '255' in split_arg[3]:
        ip_address = split_arg[2]
        subnet_mask = split_arg[3]
        interface_index = split_arg[4]

        cidr_lookup = cidr_dictionary.get(subnet_mask,\
                      '\nnotify~! Invalid subnet mask.\n')
        newline()
        print('notify~! Clearing interface IP config')
        subprocess.call(['powershell.exe', 'Remove-NetIpAddress'\
        + ' -InterfaceIndex '+interface_index+' -AddressFamily '\
        + 'IPv4 -Confirm:$False | Out-Null'])

        print('notify~! Configuring interface IP')
        assign_address = pshell_decoder('New-NetIPAddress '+ '-InterfaceIndex'\
        + ' '  + interface_index + ' -IPAddress ' + ip_address + ' -PrefixLength'\
        + ' ' + cidr_lookup + ' | Out-Null')

        if 'The object already exists.' in assign_address:
            newline()
            print('error~! Address overlaps with another interface.')
            newline()

        else:
            print('notify~! Restarting adapter')

            get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | Select-Object Name | Format-Table -AutoSize'.format(interface_index))
            split_list = get_int_list.split('----')
            get_name = split_list[1]
            int_name = '\'' + get_name.strip() + '\''
            reset_adapter = pshell_decoder('Restart-NetAdapter -Name {}'.format(int_name))

            print('notify~! Address {}/{} has been configured.'.format(ip_address, cidr_dictionary.get(subnet_mask)))
            newline()

    elif len(split_arg) == 4 \
    and '/' in split_arg[2]:
        prefix = split_arg[2]
        split_prefix = prefix.split('/')
        prefix_length = split_prefix[1]
        ip_address = split_prefix[0]
        interface_index = split_arg[3]

        if int(prefix_length) < 1 \
        or int(prefix_length) > 32:
            newline()
            print('error~! Invalid prefix length. Range = 1 - 32')
            newline()
            pass

        else:
            newline()
            print('notify~! Clearing interface IP config')
            subprocess.call(['powershell.exe', 'Remove-NetIpAddress'\
            + ' -InterfaceIndex '+interface_index+' -AddressFamily '\
            + 'IPv4 -Confirm:$False | Out-Null'])

            print('notify~! Configuring interface IP')
            assign_address = pshell_decoder('New-NetIPAddress '+ '-InterfaceIndex'\
            + ' '  + interface_index + ' -IPAddress ' + ip_address + ' -PrefixLength'\
            + ' ' + prefix_length + ' | Out-Null')

            if 'The object already exists.' in assign_address:
                newline()
                print('error~! Address overlaps with another interface.')
                newline()

            else:
                print('notify~! Restarting adapter')

                get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | Select-Object Name | Format-Table -AutoSize'.format(interface_index))
                split_list = get_int_list.split('----')
                get_name = split_list[1]
                int_name = '\'' + get_name.strip() + '\''
                reset_adapter = pshell_decoder('Restart-NetAdapter -Name {}'.format(int_name))
                print('notify~! Address {}/{} has been configured.'.format(ip_address, prefix_length))
                newline()

    elif len(split_arg) == 5 \
    and '/' in split_arg[2] \
    and '.' in split_arg[3]:
        default_gateway = split_arg[3]
        interface_index = split_arg[4]
        prefix = split_arg[2]
        split_prefix = prefix.split('/')
        prefix_length = split_prefix[1]
        ip_address = split_prefix[0]

        if int(prefix_length) < 8 \
        or int(prefix_length) > 32:
            newline()
            print('error~! Invalid prefix length. Range = 1 - 32')
            newline()
            pass
        else:

            newline()
            print('notify~! Initializing route table lookup')

            route_lookup = pshell_decoder('get-netroute -addressfamily ipv4 | '\
                           +'select-object -property destinationprefix')

            print('notify~! Route lookup succeeded')

            if '0.0.0.0/0' in route_lookup.split('\n'):
                print('notify~! Flushing old default route from table')
                subprocess.call(['powershell', 'Remove-NetRoute -InterfaceIndex '\
                +interface_index+' -destinationprefix 0.0.0.0/0 -Confirm:$False'\
                + ' | Out-Null'])

            remove_address = pshell_decoder('Remove-NetIpAddress -InterfaceIndex '\
                           +interface_index+' -AddressFamily IPv4 -Confirm:$False | '\
                           + 'Out-Null')

            if 'Default loopback address cannot be deleted' in remove_address:
                newline()
                print('error~! Cannot change the default loopback address.')
                newline()

            else:
                print('notify~! Disabling DHCP')
                subprocess.call(['powershell.exe','Set-NetIPInterface -InterfaceIndex'\
                ' ' + interface_index + ' -Dhcp Disabled | Out-Null'])

                print('notify~! Configuring address')
                gateway_config = pshell_decoder('New-NetIPAddress -InterfaceIndex '\
                                 + interface_index +' -IPAddress '+ip_address \
                                 +' -PrefixLength '+ prefix_length +' -DefaultGateway '\
                                 + default_gateway)

                print('notify~! Restarting adapter')
                get_int_list = pshell_decoder('Get-NetAdapter -InterfaceIndex {} | Select-Object Name | Format-Table -AutoSize'.format(interface_index))
                split_list = get_int_list.split('----')
                get_name = split_list[1]
                int_name = '\'' + get_name.strip() + '\''
                reset_adapter = pshell_decoder('Restart-NetAdapter -Name {}'.format(int_name))

                if 'Instance DefaultGateway already exists' in gateway_config:

                    assign_address = pshell_decoder('New-NetIPAddress -InterfaceIndex '\
                    + interface_index +' -IPAddress ' + ip_address + ' -PrefixLength ' \
                    + prefix_length + ' | Out-Null')

                    if 'Inconsistent parameters PolicyStore' in assign_address:
                        newline()
                        print('error~! Interface \'{}\' is disabled. Please enable it and try again.'.format(interface_index))
                        newline()

                    elif 'The object already exists.' in assign_address:
                        newline()
                        print('error~! Address overlaps with another interface.')
                        newline()
                    else:
                        newline()
                        print('notify~! IP address {}/{} has been configured for the interface. GW={}'.format(ip_address,prefix_length, default_gateway))
                        newline()
                else:
                    pass
   # else:
    #    pass

def ip_address_dhcp(dhcp_arg):

    split_arg = dhcp_arg.split(' ')

    if len(split_arg) == 4 \
    and split_arg[2] == 'dhcp':

        interface_index = split_arg[3]

        subprocess.call(['powershell.exe','Set-NetIPInterface -InterfaceIndex'\
        ' ' + interface_index + ' -Dhcp Enabled | Out-Null'])

        newline()
        print('notify~! DHCP has been enabled for the interface.'\
        + ' Use \'show ip address\' for address information.')
        newline()

    else:
        pass

def ip_general(ip_arg):

    ip_general_dictionary = {
        'ip icmp redirect enable':'Set-NetIpv4Protocol -IcmpRedirects Enabled',
        'ip icmp redirect disable':'Set-NetIpv4Protocol -IcmpRedirects Disabled',
        'ip igmp version 1':'Set-NetIpv4Protocol -IGMPVersion Version1',
        'ip igmp version 2':'Set-NetIpv4Protocol -IGMPVersion Version2',
        'ip igmp version 3':'Set-NetIpv4Protocol -IGMPVersion Version3',
        'ip multicast enable':'Set-NetIpv4Protocol -MulticastForwarding Enabled',
        'ip multicast disable':'Set-NetIpv4Protocol -MulticastForwarding Disabled',
        'ip source-route forward':'Set-NetIpv4Protocol -SourceRoutingBehavior Forward',
        'ip source-route receive-only':'Set-NetIpv4Protocol -SourceRoutingBehavior DontForward',
        'ip source-route drop':'Set-NetIpv4Protocol -SourceRoutingBehavior Drop',
        'ip tcp timestamp enable':'set-nettcpsetting -Timestamps Enabled',
        'ip tcp timestamp disable':'set-nettcpsetting -Timestamps Disabled',
        'ip tcp ecn enable':'set-nettcpsetting -ecncapability enabled',
        'ip tcp ecn disable':'set-nettcpsetting -ecncapability disabled',
        'ip tcp mpp enable':'set-nettcpsetting -MemoryPressureProtection Enabled',
        'ip tcp mpp disable':'set-nettcpsetting -MemoryPressureProtection Disabled',
        'ip tcp auto-tune disable':'set-nettcpsetting -AutoTuningLevelLocal Disabled',
        'ip tcp auto-tune restrict':'set-nettcpsetting -AutoTuningLevelLocal Restricted',
        'ip tcp auto-tune normal':'set-nettcpsetting -AutoTuningLevelLocal Normal'
        }

    ip_help_dictionary = {
        'ip icmp redirect enable':'notify~! ICMP redirects are now enabled.',
        'ip icmp redirect disable':'notify~! ICMP redirects are now disabled',
        'ip igmp version 1':'notify~! IGMP has been set to version 1.',
        'ip igmp version 2':'notify~! IGMP has been set to version 2.',
        'ip igmp version 3':'notify~! IGMP has been set to version 3.',
        'ip multicast enable':'notify~! Multicast forwarding has been enabled.',
        'ip multicast disable':'notify~! Multicast forwarding has been disabled.',
        'ip source-route forward':'notify~! Forwarding source-routed packets.',
        'ip source-route receive-only':'notify~! Listening for source-routed packets.',
        'ip source-route drop':'notify~! Dropping source-routed packets.',
        'ip tcp timestamp enable':'notify~! TCP timestamps have been enabled.',
        'ip tcp timestamp disable':'notify~! TCP timestamps have been disabled.',
        'ip tcp ecn enable':'notify~! ECN has been enabled for the local host.',
        'ip tcp ecn disable':'notify~! ECN has been disabled for the local host.',
        'ip tcp mpp enable':'notify~! TCP Memory Pressure Protection has been enabled.',
        'ip tcp mpp disable':'notify~! TCP Memory Pressure Protection has been disabled.',
        'ip tcp auto-tune disable':'notify~! TCP auto-tuning has been disabled.',
        'ip tcp auto-tune restrict':'notify~! TCP auto-tuning has been enabled. Rx wdw increased.',
        'ip tcp auto-tune normal':'notify~! TCP auto-tuning has been enabled. Receive window size increased.'
        }

    for line in ip_general_dictionary:
        if line == ip_arg:
            pshell_decoder(ip_general_dictionary.get(line))
    for line in ip_help_dictionary:
        if line == ip_arg:
            newline()
            print(ip_help_dictionary.get(line))
            newline()

def ip_tcp_config(ip_tcp_arg):

    if 'ip tcp port-range' in ip_tcp_arg:
        split_arg = ip_tcp_arg.split(' ')
        if split_arg[4] == 'to':
            range_begin = split_arg[3]
            range_end = split_arg[5]
            begin_integer = int(range_begin)
            end_integer = int(range_end)
            dif = end_integer - begin_integer
            str_dif = str(dif)
            subprocess.call(['powershell.exe','set-nettcpsetting '\
            + '-DynamicPortRangeStartPort ' + range_begin \
            + ' -DynamicPortRangeNumberOfPorts '+str_dif+' '])
            newline()
            print('notify~! Ephemeral port range for client tcp connections'\
            +' changed to %s - %s.' % (range_begin,range_end))
            newline()
        else:
            pass

    elif ip_tcp_arg == 'ip tcp window-restart enable':

        set_tcp_provider = pshell_decoder('set-nettcpsetting -CwndRestart true')

        if 'Property CwndRestart is read-only' in set_tcp_provider:
            print('error~! Command not supported for this OS.'\
            +' Enterprise or Server edition required.')
        else:
            print('notify~! TCP congestion window restart has'\
            +' been enabled for the local host.')

    elif ip_tcp_arg == 'ip tcp window-restart disable':

        set_tcp_provider = pshell_decoder('set-nettcpsetting -CwndRestart false')

        if 'Property CwndRestart is read-only' in set_tcp_provider:
            os_error_message()
        else:
            newline()
            print('notify~! TCP congestion window restart has'\
            +' been disabled for the local host.')
            newline()

    elif 'ip tcp provider' in ip_tcp_arg:

        split_arg = ip_tcp_arg.split(' ')
        provider_type = split_arg[3]

        if 'ctcp' in provider_type:
            newline()
            print('notify~! Checking provider compatibility')
            set_tcp_provider = pshell_decoder('set-nettcpsetting '\
            +'-CongestionProvider CTCP')
            if 'Property CongestionProvider is read-only' in set_tcp_provider:
                os_error_message()
            else:
                provider_announcement('CTCP')

        elif 'dctcp' in provider_type:
            newline()
            print('notify~! Checking provider compatibility')
            set_tcp_provider = pshell_decoder('set-nettcpsetting -CongestionProvider DCTCP')
            if 'Property CongestionProvider is read-only' in set_tcp_provider:
                os_error_message()
            else:
                provider_announcement('DCTCP')

        elif 'new-reno' in provider_type:
            newline()
            print('notify~! Checking provider compatibility')
            set_tcp_provider = pshell_decoder('set-nettcpsetting -CongestionProvider Default')
            if 'Property CongestionProvider is read-only' in set_tcp_provider:
                os_error_message()
            else:
                provider_announcement('NewReno')
        else:
            pass