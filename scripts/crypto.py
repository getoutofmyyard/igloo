import sys, string, os, subprocess, random, ctypes, hashlib
import socket, datetime, re
from common import *

def crypto_ipsec_build(vpn_auth, vpn_encrypt, vpn_group):
    # Receives var from cryptoConfig(cryptoArg), gathers info, and then executes a powershell command which creates an ipsec vpn
    try:
        vpn_name = input('\nconf~$ Name the vpn connection: ')
        vpn_server = input('conf~$ Enter the IP address of your vpn server: ')
        newline()
        print('notify~! Creating VPN adapter...')
        os.system('powershell Add-VpnConnection -Name '+vpn_name+' -ServerAddress '+vpn_server+' -TunnelType Ikev2 -EncryptionLevel Required -SplitTunneling -PassThru > nul 2>&1')
        print('notify~! Configuring encryption, hash, and DH group options...')
        os.system('powershell Set-VpnConnectionIPsecConfiguration -ConnectionName '+vpn_name+' -AuthenticationTransformConstants '+vpn_auth+' -CipherTransformConstants '+vpn_encrypt+' -EncryptionMethod '+vpn_encrypt+' -IntegrityCheckMethod '+vpn_auth+' -PfsGroup None -DHGroup '+vpn_group+' -PassThru -Force > nul 2>&1')
        print('notify~! IPSec VPN \'{}\' has been created: Encryption={}, Hash={}, Group={}'.format(vpn_name, vpn_encrypt, vpn_auth, vpn_group))
        newline()
    except:
        newline()
        print('error~! Operation terminated unexpectedly.')
        newline()

def crypto_ipsec_options(ipsec_arg):
    # Retrieves ipsec arguments from command and pipes them
    # into crypto_ipsec_build() for processing.
    try:
        if 'des' in ipsec_arg:
            encrypt = 'des'
        if '3des' in ipsec_arg:
            encrypt = '3des'
        if 'aes128' in ipsec_arg:
            encrypt = 'aes128'
        if 'aes256' in ipsec_arg:
            encrypt = 'aes256'
        if 'md5' in ipsec_arg:
            auth = 'md5'
        if 'sha256' in ipsec_arg:
            auth = 'sha256'
        if 'group1' in ipsec_arg:
            group = 'group1'
        if 'group2' in ipsec_arg:
            group = 'group2'
        if 'group14' in ipsec_arg:
            group = 'group14'
        crypto_ipsec_build(auth, encrypt, group)
    except:
        newline()
        newline()

def crypto_pptp_build(vpn_auth):
    # Receives var from cryptoConfig(cryptoArg), gathers info, and then executes a powershell command which creates a pptp vpn
    vpn_name = input('\nconf~$ Name the vpn connection: ')
    vpn_server = input('conf~$ Enter the IP address of your vpn server: ')
    newline()
    print('notify~! Creating VPN adapter...')
    os.system('powershell Add-VpnConnection -Name '+vpn_name+' -ServerAddress '+vpn_server+' -TunnelType Pptp -AuthenticationMethod '+vpn_auth+' -SplitTunneling -PassThru > nul 2>&1')
    print('notify~! PPTP VPN \'{}\' has been created: Auth={}'.format(vpn_name, vpn_auth))
    newline()

def crypto_pptp_options(pptp_arg):
    if pptp_arg == 'crypto pptp pap':
        auth = 'Pap'
    if pptp_arg == 'crypto pptp chap':
        auth = 'Chap'
    if pptp_arg == 'crypto pptp mschap':
        auth = 'MSChapv2'
    crypto_pptp_build(auth)

def crypto_delete(delete_this_vpn):
    # Split command arguments into an array. delete_this_vpn[2] should be
    # the vpn name.
    newline()
    try:
        print('notify~! Finding VPN adapter \'{}\'...'.format(delete_this_vpn))
        delete_vpn = pshell_decoder('Remove-VpnConnection -Name '+delete_this_vpn+' -Force -PassThru')
        if 'ObjectNotFound' in delete_vpn:
            print('notify~! VPN adapter \'{}\' does not exist.'.format(delete_this_vpn))
            newline()
        else:
            print('notify~! VPN profile \'{}\' was deleted.'.format(delete_this_vpn))
            newline()
    except:
        newline()
        print('error~! Operation terminated unexpectedly.')
        newline()
        pass

def generate_psk():
    alphabet = 'abcdefghijklmnopqrstuvwxyz!@$&'
    upper_alphabet = alphabet.upper()
    pw_len = 16
    pw_list = []
    for i in range(pw_len//3):
        pw_list.append(alphabet[random.randrange(len(alphabet))])
        pw_list.append(upper_alphabet[random.randrange(len(upper_alphabet))])
        pw_list.append(str(random.randrange(10)))
    for i in range(pw_len-len(pw_list)):
        pw_list.append(alphabet[random.randrange(len(alphabet))])
    random.shuffle(pw_list)
    pw_string = "".join(pw_list)
    newline()
    print(pw_string)
    newline()


def format_certificate(dc, san):

    for item in dc:
        dc_formatted = 'DC={}'.format(item)
        for another_item in san:
            san_formatted = 'upn={}'.format(another_item)
            return dc_formatted, san_formatted

def generate_rsa():
    try:
        newline()
        print('notify~! Use commas to separate multiple entries')
        newline()
        cn = input('input~! DNS common name: ')
        ou = input('input~! Active Directory OU: ')
        san = input('input~! SAN: ')
        dc =  input('input~! DC: ')

        strip_cn = cn.rstrip(' ')
        strip_ou = ou.rstrip(' ')
        strip_dc = dc.rstrip(' ')
        split_dc = strip_dc.split(',')
        strip_san = san.rstrip(' ')
        split_san = strip_san.split(',')

        dc_format, san_format = format_certificate(split_dc, split_san)

        create_cert = pshell_decoder('New-SelfSignedCertificate -Type Custom -Subject \
        \"CN={},OU={},{}\" -TextExtension @(\"2.5.29.37={}1.3.6.1.5.5.7.3.2\"\
        ,\"2.5.29.17={}{}\") -KeyUsage DigitalSignature -KeyAlgorithm\
         RSA -KeyLength 2048 -CertStoreLocation \"Cert:\\LocalMachine\\My\"'.format(strip_cn, \
        strip_ou, dc_format, '{text}', '{text}', san_format))

        if '   PSParentPath:' in create_cert:
            newline()
            print('notify~! Self-signed certificate created and stored in \"Cert:\\LocalMachine\\My\" (Computer Certificates > Personal)')
            newline()
        else:
            newline()
            print('error~! Failed to create certificate')
            newline()

    except:
        newline()
        print('error~! Operation terminated')
        newline()

def crypto_go(vpn_to_connect):
    newline()
    subprocess.Popen('rasphone -d ' + vpn_to_connect)
    newline()