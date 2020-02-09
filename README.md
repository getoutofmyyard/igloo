# What's igloo?

Igloo is a terminal application which combines Python and PowerShell to simplify network and Windows administration tasks. 

AUTOMATE SSH OUTPUT COLLECTION:
```
igloo~$ ssh write ios

input~! Specify the path to your device list: C:\Users\myuser\dev.txt
input~! Specify the destination directory path: C:\Device Files\
input~! Enter a 'show' command: show version | in Version
input~! Enter a username: ssh-username
Password: [ssh-password]
notify~! Saving file 10.0.0.1.txt...
notify~! Saving file 10.0.0.254.txt...
notify~! Saving file my-router.txt...
notify~! Saving file your-router.txt...
```
CREATE AND MANAGE COMPLEX VPN PROFILES:
```
igloo~$ crypto ipsec aes256 sha256 group14

conf~$ Name the vpn connection: myvpn
conf~$ Enter the IP address of your vpn server: 1.1.1.1
notify~! Creating VPN adapter...
notify~! Configuring encryption, hash, and DH group options...
notify~! IPSec VPN 'myvpn' has been created: [Output Omitted]
```
INSTALL OR UNINSTALL WINDOWS SERVER FEATURES:
```
igloo~$ install feature iis

notify~! Installing feature 'iis'. Please wait...
notify~! Installed 'iis' successfully! Use 'win reboot' to finish the installation
```
MANAGE BGP ROUTING, PEERING, AND ADVERTISEMENTS:
```
igloo~$ router bgp enable

notify~! RSAT and RRAS are required to enable BGP. Install now? (y/n) y
notify~! Installing RRAS routing features
notify~! Installing RSAT
notify~! Enabling BGP routing
notify~! Dependencies installed successfully. Use 'win reboot' to enable BGP routing features.

igloo~$ router bgp id 10.0.0.33 64513

notify~! Creating BGP routing instance
notify~! BGP routing identity created. RID=10.0.0.33 AS=64513

igloo~$ router bgp peer mypeer 10.0.0.1 64513 10.0.0.33

notify~! Configuring BGP peer...
notify~! BGP peering with 10.0.0.1 (AS 64513) has been enabled

igloo~$ show bgp peer

PeerName             : mypeer
LocalIPAddress       : 10.0.0.33
PeerIPAddress        : 10.0.0.1
LocalASN             : 64513
PeerASN              : 64513
OperationMode        : Mixed
PeeringMode          : Automatic
Weight               : 32768
HoldTime(s)          : 180
IdleHoldTime(s)      : 10
ConnectivityStatus   : Connecting
```

HOW TO USE IGLOO:

Igloo can be used with Python 3.7+ and the GitHub source code, or installed using the Windows installer.

RUN THE EXE:

Download and run the Windows installer.
Complete the setup wizard and run igloo as Administrator for full functionality

RUN FROM POWERSHELL:

Upon first launch, Igloo creates a PowerShell alias (igloo) which allows users to run commands from any directory. If the local PowerShell script execution policy is set to Restricted, this process is skipped. To modify the execution policy, run Igloo as a Python script or exe and use the powershell policy [policy-level] command to change it to a less restrictive mode.
```
PS C:\Users\MyUser\> igloo win ?
win app             - programs and features
win aux             - sounds and audio devices
win blu             - bluetooth devices
win cleanmgr        - disk cleanup
win cmd             - cmd.exe
win defrag          - disk defragmentation
win dev             - device manager
win disk            - disk management
[Output Omitted]
```
THE IGLOO CLI:

Igloo has a lot in common with other context-based CLIs like Cisco IOS or JunOS. For example, commands are organized into a tree-like structure, where top-level commands beget a number of sub-commands, and further sub-commands below those:
```
igloo~$ show ?
show arp               - show the arp table for the local host
show bgp               - show bgp routing information
show cidr-table        - show cidr conversion table
show crypto            - show all VPN connections
show dns               - show dns information
show drives            - show storage volumes
[Output Omitted]

igloo~$ show bgp ?

advert              - display bgp routes advertised to peers
id                  - display local bgp configuration
peer                - display bgp peer configuration
Igloo includes a great deal of help output, which can be triggered by entering an incomplete command or using the ? character after an incomplete command. Igloo does not support autocomplete at this time.

igloo~$ ip address ?

Syntax:  ip address {prefix | address | dhcp} [subnet mask] [default gateway] {interface index}
Example: ip address 10.0.0.200/24 10.0.0.1 23
Example: ip address 10.0.0.200 255.255.255.0 10.0.0.1 23
Example: ip address dhcp 23
```
