import installDict, conversion
import subprocess
from decimal import Decimal
from common import pshell_decoder, newline, yes, no


# Install RRAS with BGP features only
def bgp_install():
    print('notify~! Enabling BGP routing')
    install_routing_daemon = pshell_decoder('Install-RemoteAccess -VpnType RoutingOnly | Out-Null')
    if 'The term \'Install-RemoteAccess\' is not recognized as the name of a cmdlet' in install_routing_daemon:
        newline()
        print('notify~! RSAT features are not installed, or are not finished installing.')
        print('notify~! If you just installed RSAT, reload this server and run \'bgp enable\' again.')
        newline()
    else:
        newline()
        print('notify~!  Dependencies installed successfully.'\
        +' Use \'win reboot\' to enable BGP routing features.')
        newline()
        return

# BGP options
def bgp_routing(bgp_command):
    split_cmd = bgp_command.split(' ')

    if split_cmd[1] == 'hold-time'\
    and len(split_cmd) == 4:
        peer_name = split_cmd[3]
        hold_time = split_cmd[2]
        set_holdtime = pshell_decoder('Set-BgpPeer -Name {} -HoldTimeSec {}'.format(peer_name, hold_time))
        if 'Set-BgpPeer' in set_holdtime:
            newline()
            print('notify~! Peer does not exist. Use \'bgp peer\'')
            newline()
        else:
            newline()
            print('notify~! BGP hold timer for peer {} set to {}s'.format(peer_name, hold_time))
            newline()

    elif split_cmd[1] == 'weight'\
    and len(split_cmd) == 4:
        peer_name = split_cmd[3]
        weight = split_cmd[2]
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
                    print('notify~! Peer does not exist. Use \'bgp peer\'')
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

    # BGP initialization script
    elif split_cmd[1] == 'enable':
        newline()
        input_loop = 1
        while input_loop == 1:
            pre_reqs = input('notify~! RSAT and RRAS are required to enable BGP.'\
            + ' Install now? (y/n) ')

            if pre_reqs in yes:

                input_loop = 0

                routing_lookup = installDict.install.get('install feature routing')
                rsat_lookup = installDict.install.get('install feature rsat')

                print('notify~! Installing RRAS routing features')

                install_routing = pshell_decoder(routing_lookup)

                if 'The term \'Install-WindowsFeature\' is not recognized' in install_routing:
                
                    print('notify~! This command is supported only on Windows Server machines')
                    newline()
                    return

                if 'NoChangeNeeded' in install_routing:
                    print('notify~! Dependency already met: routing')
                    pass

                print('notify~! Installing RSAT')

                install_rsat = pshell_decoder(rsat_lookup)

                if 'NoChangeNeeded' in install_rsat:
                    print('notify~! Dependency already met: rsat')
                    pass

                if 'ArgumentNotValid:' in install_routing\
                    or 'ArgumentNotValid' in install_rsat:
                    print('notify~! Feature is either unknown or has unmet dependencies.')
                    newline()

                else:
                    bgp_install()

            elif pre_reqs in no:
                input_loop = 0
                bgp_install()

            else:
                pass

    elif split_cmd[1] == 'advertise'\
    and '.' in split_cmd[2]\
    and '/' in split_cmd [2]:
        # Add-BgpCustomRoute
        advertise_route = pshell_decoder('Add-BgpCustomRoute -Network {}'.format(split_cmd[2]))

        if 'The term \'Add-BgpCustomRoute\' is not recognized' in advertise_route:
            newline()
            print('notify~! BGP is not enabled on this machine. Use \'bgp enable\' and \'bgp id\' first.')
            newline()
        elif 'Add-BgpCustomRoute' in advertise_route:
            newline()
            print('error~! Invalid prefix.')
            newline()
        else:
            pass

    elif split_cmd[1] == 'advertise'\
    and '.' in split_cmd[2]\
    and '.' in split_cmd[3]:
        # Add-BgpCustomRoute

        network_address = split_cmd[2]
        subnet_mask = split_cmd[3]

        split_net = network_address.split('.')
        split_mask = subnet_mask.split('.')

        for octet in split_net:
            numberize = Decimal(octet)
            if numberize < 0 \
            or numberize > 255:
                newline()
                print('error~! Invalid network address') 
                newline()
                return

            else:
                pass

        for octet in split_mask:
            numberize = Decimal(octet)
            if numberize < 0 \
            or numberize > 255:
                newline()
                print('error~! Invalid subnet mask') 
                newline()
                return

            else:
                pass


        mask_to_prefix_lookup = conversion.cidr_dictionary.get(subnet_mask)

        advertise_route = pshell_decoder('Add-BgpCustomRoute -Network {}/{}'.format(network_address,mask_to_prefix_lookup))

        if 'The term \'Add-BgpCustomRoute\' is not recognized' in advertise_route:
            newline()
            print('notify~! BGP is not enabled on this machine. Use \'bgp enable\' and \'bgp id\' first.')
            newline()
        else:
            pass

    elif split_cmd[2] == 'advertise'\
    and '.' in split_cmd[3]\
    and '/' in split_cmd [3]\
    and split_cmd[0] == 'no':
        # Add-BgpCustomRoute
        remove_route = pshell_decoder('Remove-BgpCustomRoute -Network {} -Force'.format(split_cmd[3]))

        if 'The term \'Remove-BgpCustomRoute\' is not recognized' in remove_route:
            newline()
            print('notify~! BGP is not enabled on this machine. Use \'bgp enable\' and \'bgp id\' first.')
            newline()
        elif 'Remove-BgpCustomRoute' in remove_route:
            newline()
            print('error~! Invalid prefix.')
            newline()
        else:
            pass

    elif split_cmd[2] == 'advertise'\
    and '.' in split_cmd[3]\
    and '.' in split_cmd[4]\
    and split_cmd[0] == 'no':
        # Add-BgpCustomRoute

        network_address = split_cmd[3]
        subnet_mask = split_cmd[4]

        split_net = network_address.split('.')
        split_mask = subnet_mask.split('.')

        for octet in split_net:
            numberize = Decimal(octet)
            if numberize < 0 \
            or numberize > 255:
                newline()
                print('error~! Invalid network address') 
                newline()
                return

            else:
                pass

        for octet in split_mask:
            numberize = Decimal(octet)
            if numberize < 0 \
            or numberize > 255:
                newline()
                print('error~! Invalid subnet mask') 
                newline()
                return

            else:
                pass


        mask_to_prefix_lookup = conversion.cidr_dictionary.get(subnet_mask)

        remove_route = pshell_decoder('Remove-BgpCustomRoute -Network {}/{} -Force'.format(network_address,mask_to_prefix_lookup))

        if 'The term \'Remove-BgpCustomRoute\' is not recognized' in advertise_route:
            newline()
            print('notify~! BGP is not enabled on this machine. Use \'bgp enable\' and \'bgp id\' first.')
            newline()
        else:
            pass

    elif split_cmd[1] == 'aggregate' \
    and '.' in split_cmd[2]:
        # bgp aggregate 172.16.1.0/24
        prefix = split_cmd[2]
        if len(split_cmd) == 3:
            advertise_prefix = pshell_decoder('Add-BgpRouteAggregate -Prefix {} -SummaryOnly Disabled -Force'.format(prefix))
        elif len(split_cmd) == 4 \
        and split_cmd[3] == 'summary-only':
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
            print('notify~! BGP is not enabled for this machine. Use \'bgp id\'')
            newline()
        elif 'Add-BgpRouteAggregate' in advertise_prefix:
            newline()
            print('notify~! This machine has unmet dependencies for BGP routing. Use \'bgp enable\'')
            newline()
        else:
            newline()
            print('notify~! Route to prefix {} is being advertised to peers'.format(prefix))
            newline()

    # Option for removal of BGP router id ("no bgp id x.x.x.x")
    elif split_cmd[2] == 'id' \
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

    # Configure local BGP identity
    elif split_cmd[1] == 'id'\
    and '.' in split_cmd[2]:
        # bgp id 10.0.0.33 64512
        router_id = split_cmd[2]
        local_as = split_cmd[3]
        if int(local_as) > 65535\
        or int(local_as) < 1:
            print('notify~! Invalid autonomous system number')
            newline()
        else:
            check_for_bgp = pshell_decoder('Get-BgpRouter | Out-Null')

            if 'Get-BgpRouter ' in check_for_bgp:

                newline()
                print('notify~! Creating BGP routing instance')
                pshell_cmd = 'Add-BgpRouter -BgpIdentifier {} -LocalASN {}'.format(router_id, local_as)
                init_bgp = pshell_decoder(pshell_cmd)
                if ' LAN Routing not configured.' in init_bgp:
                    print('error~! Missing dependencies. Use \'bgp enable\'')
                    newline()
                    return
                else:
                    with open('.\\miscellaneous\\asn.txt', 'w') as file:
                        file.write(local_as)

                    print('notify~! BGP routing identity created. RID={} AS={}'.format(router_id, local_as))
                    newline()

            else:
                newline()
                print('notify~! Modifying BGP routing instance')

                pshell_cmd = 'Set-BgpRouter -BgpIdentifier {} -LocalASN {}'.format(router_id, local_as)
                init_bgp = pshell_decoder(pshell_cmd)

                with open('.\\miscellaneous\\asn.txt', 'w') as file:
                    file.write(local_as)

                print('notify~! BGP routing identity has been modifed. RID={} AS={}'.format(router_id, local_as))
                newline()



    elif split_cmd[2] == 'aggregate' \
    and split_cmd[0] == 'no' \
    and '.' in split_cmd[3]:
        # no bgp network 172.16.1.0/24
        prefix = split_cmd[3]
        remove_prefix = pshell_decoder('Remove-BgpRouteAggregate -Prefix {} -Force'.format(prefix))
        if ' The parameter is incorrect.' in remove_prefix:
            newline()
            print('notify~! Invalid prefix. Use CIDR notation (e.g. \'172.16.1.0/24\') and')
            print('notify~! keep the entered network address on bit boundaries.')
            newline()
        elif ' BGP is not configured.' in remove_prefix:
            newline()
            print('notify~! BGP is not enabled for this machine. Use \'bgp id\'')
            newline()
        elif ' Aggregate' in remove_prefix:
            newline()
            print('notify~! This prefix is not being advertised')
            newline()
        elif 'Remove-BgpRouteAggregate' in remove_prefix:
            newline()
            print('notify~! This machine has unmet dependencies for BGP routing. Use \'bgp enable\'')
            newline()
        else:
            newline()
            print('notify~! Aggregate {} no longer advertised'.format(prefix))
            newline()      

    elif split_cmd[2] == 'peer' \
    and split_cmd[0] == 'no':
        peer_name = split_cmd[3]
        rm_peer = pshell_decoder('Remove-BgpPeer -Name {} -Force'.format(peer_name))
        if 'Remove-BgpPeer' in rm_peer:
            newline()
            print('notify~! Peer {} does not exist.'.format(peer_name))
            newline()
        else:
            newline()
            print('notify~! Peer profile {} was deleted'.format(peer_name))
            newline()

    elif split_cmd[1] == 'peer' \
    and len(split_cmd) <= 6:

        check_for_id = pshell_decoder('Get-BgpRouter | Out-Null')

        if 'Get-BgpRouter' in check_for_id:
            newline()
            print('notify~! You must create a BGP identity first. Use \'bgp id\'')
            newline()
            pass
        # bgp peer OK-Site 10.0.0.1 64512 192.168.1.1
        # bgp peer mypeer 10.0.0.254
        else:
            if len(split_cmd) == 6 \
            and '.' in split_cmd[3]:
                peer_name = split_cmd[2]
                peer_address = split_cmd[3]
                remote_as = split_cmd[4]
                local_address = split_cmd[5]

                if int(remote_as) > 65535 \
                or int(remote_as) < 1:
                    newline()
                    print('notify~! Invalid autonomous system number')
                    newline()
                else:
                    try:
                        with open('.\\miscellaneous\\asn.txt','r') as file:
                            read_asn = file.read()
                            newline()
                            print('notify~! Configuring BGP peer...')
                            pshell_cmd = 'Add-BgpPeer -Name {} -PeerIPAddress {} -PeerASN {} -LocalIPAddress {} -LocalASN {}'.format(peer_name, peer_address, remote_as, local_address, read_asn)
                            add_peer = pshell_decoder(pshell_cmd)
                            print('notify~! BGP peering with {} (AS {}) has been enabled'.format(peer_address, remote_as))
                            newline()
                    except:
                        newline()
                        print('error~! Local ASN has not been configured. Use \'bgp id\'')
                        newline()


            elif len(split_cmd) == 4 \
            and '.' in split_cmd[3]:
                peer_name = split_cmd[2]
                peer_address = split_cmd[3]
                set_peer_ip = pshell_decoder('Set-BgpPeer -Name {} -PeerIPAddress {} -Force'.format(peer_name, peer_address))
                if 'Set-BgpPeer' in set_peer_ip:
                    newline()
                    print('notify~! Peer does not exist. Use \'bgp peer\'')
                    newline()
                else:
                    newline()
                    print('notify~! Address for peer {} set to {}'.format(peer_name, peer_address))
                    newline()

            elif len(split_cmd) == 4 \
            and '.' not in split_cmd[3]:
                peer_name = split_cmd[2]
                remote_as = split_cmd[3]
                set_peer_as = pshell_decoder('Set-BgpPeer -Name {} -PeerASN {} -Force'.format(peer_name, remote_as))
                if 'Set-BgpPeer' in set_peer_ip:
                    newline()
                    print('notify~! Peer does not exist. Use \'bgp peer\'')
                    newline()
                else:
                    newline()
                    print('notify~! ASN for peer {} set to {}'.format(peer_name, remote_as))
                    newline()

            elif len(split_cmd) == 5 \
            and '.' in split_cmd[3] \
            and split_cmd[4] == 'local':
                # bgp peer mypeer 10.0.0.1 local
                peer_name = split_cmd[2]
                local_ip = split_cmd[3]
                set_local_ip = pshell_decoder('Set-BgpPeer -Name {} -LocalIPAddress {} -Force'.format(peer_name, local_ip))
                if 'Set-BgpPeer' in set_local_ip:
                    newline()
                    print('notify~! Peer does not exist. Use \'bgp peer\'')
                    newline()
                else:
                    newline()
                    print('notify~! Local IP set to {} for peer {}'.format(local_ip, peer_name))
                    newline()

            else:
                newline()
                print('error~! Invalid command.')
                newline()
