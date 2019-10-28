import installDict, subprocess

# Routing operations supported on Windows Server

def newline():
    print('')

def pshell_decoder(command_to_decode):
    # Runs pshell command and decodes the output
    get_output = subprocess.Popen(['powershell.exe', command_to_decode],\
    stdout=subprocess.PIPE)
    decoded_output = get_output.communicate()[0].decode('iso-8859-1')
    return decoded_output

yes = ['y', 'Y', 'yes', 'Yes']
no = ['n', 'N', 'no', 'No']

def bgp_install():
    print('notify~! Enabling BGP routing')
    install_bgp = pshell_decoder('Install-RemoteAccess -VpnType RoutingOnly')
    newline()
    print('notify~!  Dependencies installed successfully.'\
    +' Use \'win reboot\' to enable BGP routing features.')
    newline()

def bgp_routing(bgp_command):
    split_cmd = bgp_command.split(' ')

    if split_cmd[2] == 'hold-time'\
    and len(split_cmd) == 5:
        peer_name = split_cmd[4]
        hold_time = split_cmd[3]
        set_holdtime = pshell_decoder('Set-BgpPeer -Name {} -HoldTimeSec {}'.format(peer_name, hold_time))
        if 'Set-BgpPeer' in set_holdtime:
            newline()
            print('notify~! Peer does not exist. Use \'router bgp peer\'')
            newline()
        else:
            newline()
            print('notify~! BGP hold timer for peer {} set to {}s'.format(peer_name, hold_time))
            newline()

    elif split_cmd[2] == 'weight'\
    and len(split_cmd) == 5:
        peer_name = split_cmd[4]
        weight = split_cmd[3]
        input_loop = 1
        newline()

        while input_loop == 1:
            reset_accept = input('notify~! Adjusting BGP metrics will cause a'\
            +' BGP session reset. Continue? (y/n) ')

            if reset_accept in yes:
                input_loop = 0
                pshell_cmd = 'Set-BgpPeer -Name {} -Weight {} -Force '.format(peer_name, weight)
                set_metric = pshell_decoder(pshell_cmd)
                if 'Set-BgpPeer' in set_metric:
                    newline()
                    print('notify~! Peer does not exist. Use \'router bgp peer\'')
                    newline()
                else:
                    newline()
                    print('notify~! Peer {} configured with weight {}'.format(peer_name, weight))
                    newline()

            elif reset_accept in no:
                newline()
                print('Terminating operation...')
                newline()
            else:
                pass

    elif split_cmd[2] == 'enable':
        newline()
        input_loop = 1
        while input_loop == 1:
            pre_reqs = input('notify~! RSAT and RRAS are required to enable BGP.'\
            + ' Install now? (y/n) ')

            if pre_reqs in yes:

                input_loop = 0

                routing_lookup = installDict.install_dictionary.get('install feature routing')
                rsat_lookup = installDict.install_dictionary.get('install feature rsat')

                print('notify~! Installing RRAS routing features')
                install_routing = pshell_decoder(routing_lookup)

                if 'NoChangeNeeded' in install_routing:
                    print('notify~! Dependency already met: routing')
                    pass

                print('notify~! Installing RSAT')
                install_rsat = pshell_decoder(rsat_lookup)

                if 'NoChangeNeeded' in install_rsat:
                    print('notify~! Dependency already met: rsat')
                    bgp_install()
                    pass

                if 'ArgumentNotValid:' in install_routing\
                or 'ArgumentNotValid' in install_rsat:
                    print('notify~! Feature is either unknown or has unmet dependencies.')
                    newline()

                elif 'Install-WindowsFeature' in install_routing\
                or 'Install-WindowsFeature' in install_rsat:
                    print('notify~! This command is supported only on Windows Server machines')
                    newline()
                    pass

                else:
                    pass

            elif pre_reqs in no:
                input_loop = 0
                newline()

            else:
                pass

    elif split_cmd[2] == 'advert' \
    and '.' in split_cmd[3]:
        # router bgp advert 172.16.1.0/24
        prefix = split_cmd[3]
        if len(split_cmd) == 4:
            advertise_prefix = pshell_decoder('Add-BgpRouteAggregate -Prefix {} -SummaryOnly Disabled -Force'.format(prefix))
        elif len(split_cmd) == 5 \
        and split_cmd[4] == 'summary':
            advertise_prefix = pshell_decoder('Add-BgpRouteAggregate -Prefix {} -SummaryOnly Enabled -Force'.format(prefix))
        if ' A More or Less specific prefix' in advertise_prefix:
            newline()
            print('notify~! Prefix is already advertised.')
            newline()
        elif ' The parameter is incorrect.' in advertise_prefix:
            newline()
            print('notify~! Invalid prefix. Use CIDR notation (e.g. \'172.16.1.0/24\') and')
            print('notify~! keep the entered network address on bit boundaries.')
            newline()
        elif ' BGP is not configured' in advertise_prefix:
            newline()
            print('notify~! BGP is not enabled for this machine. Use \'router bgp id\'')
            newline()
        elif 'Add-BgpRouteAggregate' in advertise_prefix:
            newline()
            print('notify~! This machine has unmet dependencies for BGP routing. Use \'router bgp enable\'')
            newline()
        else:
            newline()
            print('notify~! Route to prefix {} is being advertised to peers'.format(prefix))
            newline()
            
    elif split_cmd[3] == 'id' \
    and split_cmd[0] == 'no':
        remove_router = pshell_decoder('Remove-BgpRouter -Force')
        if 'Remove-BgpRouter' in remove_router:
            newline()
            print('notify~! BGP is not enabled for this machine')
            newline()
        else:
            newline()
            print('notify~! The local BGP routing instance has been deleted')
            newline()

    elif split_cmd[2] == 'id'\
    and '.' in split_cmd[3]:
        # router bgp id 10.0.0.33 64512
        router_id = split_cmd[3]
        local_as = split_cmd[4]
        if int(local_as) > 65535\
        or int(local_as) < 1:
            print('notify~! Invalid autonomous system number')
            newline()
        else:
            pshell_cmd = 'Add-BgpRouter -BgpIdentifier {} -LocalASN {}'.format(router_id, local_as)
            newline()
            print('notify~! Creating BGP routing instance')
            init_bgp = pshell_decoder(pshell_cmd)
            if 'Add-BgpRouter' in init_bgp:
                print('notify~! This machine has unmet dependencies for BGP routing. Use \'router bgp enable\'')
                newline()
            else:
                with open('.\\miscellaneous\\asn.txt', 'w') as file:
                    file.write(local_as)
                print('notify~! BGP routing instance created. RID={} AS={}'.format(router_id, local_as))
                newline()


    elif split_cmd[3] == 'advert' \
    and split_cmd[0] == 'no' \
    and '.' in split_cmd[4]:
        # no router bgp network 172.16.1.0/24
        prefix = split_cmd[4]
        remove_prefix = pshell_decoder('Remove-BgpRouteAggregate -Prefix {} -Force'.format(prefix))
        if ' The parameter is incorrect.' in remove_prefix:
            newline()
            print('notify~! Invalid prefix. Use CIDR notation (e.g. \'172.16.1.0/24\') and')
            print('notify~! keep the entered network address on bit boundaries.')
            newline()
        elif ' BGP is not configured.' in remove_prefix:
            newline()
            print('notify~! BGP is not enabled for this machine. Use \'router bgp id\'')
            newline()
        elif ' Aggregate' in remove_prefix:
            newline()
            print('notify~! This prefix is not being advertised')
            newline()
        elif 'Remove-BgpRouteAggregate' in remove_prefix:
            newline()
            print('notify~! This machine has unmet dependencies for BGP routing. Use \'router bgp enable\'')
            newline()
        else:
            newline()
            print('notify~! Route for prefix {} is now pruned from routing updates'.format(prefix))
            newline()      

    elif split_cmd[3] == 'peer' \
    and split_cmd[0] == 'no':
        peer_name = split_cmd[4]
        rm_peer = pshell_decoder('Remove-BgpPeer -Name {} -Force'.format(peer_name))
        if 'Remove-BgpPeer' in rm_peer:
            newline()
            print('notify~! Peer {} does not exist.'.format(peer_name))
            newline()
        else:
            newline()
            print('notify~! Peer profile {} was deleted'.format(peer_name))
            newline()

    elif split_cmd[2] == 'peer' \
    and len(split_cmd) <= 7:

        check_for_id = pshell_decoder('Get-BgpRouter | Out-Null')

        if 'Get-BgpRouter' in check_for_id:
            newline()
            print('notify~! You must create a BGP identity first. Use \'router bgp id\'')
            newline()
            pass
        # router bgp peer OK-Site 10.0.0.1 64512 192.168.1.1
        # router bgp peer mypeer 10.0.0.254
        else:
            if len(split_cmd) == 7 \
            and '.' in split_cmd[4]:
                peer_name = split_cmd[3]
                peer_address = split_cmd[4]
                remote_as = split_cmd[5]
                local_address = split_cmd[6]

                if int(remote_as) > 65535:
                    newline()
                    print('notify~! Invalid autonomous system number')
                    newline()
                else:
                    newline()
                    print('notify~! Configuring BGP peer...')
                    with open('.\\miscellaneous\\asn.txt','r') as file:
                        read_asn = file.read()

                        pshell_cmd = 'Add-BgpPeer -Name {} -PeerIPAddress {} -PeerASN {} -LocalIPAddress {} -LocalASN {}'.format(peer_name, peer_address, remote_as, local_address, read_asn)
                        add_peer = pshell_decoder(pshell_cmd)
                        print('notify~! BGP peering with {} (AS {}) has been enabled'.format(peer_address, remote_as))
                        newline()

            elif len(split_cmd) == 5 \
            and '.' in split_cmd[4]:
                peer_name = split_cmd[3]
                peer_address = split_cmd[4]
                set_peer_ip = pshell_decoder('Set-BgpPeer -Name {} -PeerIPAddress {} -Force'.format(peer_name, peer_address))
                if 'Set-BgpPeer' in set_peer_ip:
                    newline()
                    print('notify~! Peer does not exist. Use \'router bgp peer\'')
                    newline()
                else:
                    newline()
                    print('notify~! Address for peer {} set to {}'.format(peer_name, peer_address))
                    newline()

            elif len(split_cmd) == 5 \
            and '.' not in split_cmd[4]:
                peer_name = split_cmd[3]
                remote_as = split_cmd[4]
                set_peer_as = pshell_decoder('Set-BgpPeer -Name {} -PeerASN {} -Force'.format(peer_name, remote_as))
                if 'Set-BgpPeer' in set_peer_ip:
                    newline()
                    print('notify~! Peer does not exist. Use \'router bgp peer\'')
                    newline()
                else:
                    newline()
                    print('notify~! ASN for peer {} set to {}'.format(peer_name, remote_as))
                    newline()

            elif len(split_cmd) == 6 \
            and '.' in split_cmd[4] \
            and split_cmd[5] == 'local':
                # router bgp peer mypeer 10.0.0.1 local
                peer_name = split_cmd[3]
                local_ip = split_cmd[4]
                set_local_ip = pshell_decoder('Set-BgpPeer -Name {} -LocalIPAddress {} -Force'.format(peer_name, local_ip))
                if 'Set-BgpPeer' in set_local_ip:
                    newline()
                    print('notify~! Peer does not exist. Use \'router bgp peer\'')
                    newline()
                else:
                    newline()
                    print('notify~! Local IP set to {} for peer {}'.format(local_ip, peer_name))
                    newline()
