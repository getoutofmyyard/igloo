# igloo v4

Igloo simplifies Windows administration by offering pre-made aliases for lengthy PowerShell commands. For example, displaying outbound firewall rules in PowerShell uses the following syntax:
```
Get-NetFirewallRule -Direction Out -Enabled True | Sort-Object -Property DisplayName
```
This is unwieldy and unnecessarily long, and further piping into Select-Object would be required for clean output. The equivalent command in Igloo is as follows:
```
igloo~$ show fwall out
```
In addition to Windows aliases, Igloo offers a variety of admin tools to help automate your workflows. For example, SSH output can be captured into dynamically-named files - perfect for config backups on compatible operating systems:
```
igloo~$ ssh write ios
input~! Specify the path to your device list: C:\Users\myuser\dev.txt
input~!  Specify the destination directory path: C:\Device Files\
input~! Enter a 'show' command: show version | in Version
input~! Enter a username: ssh-username
Password: [This is the SSH password prompt]

notify~! Saving file 10.0.0.1.txt...
notify~! Saving file 10.0.0.254.txt...
notify~! Saving file my-router.txt...
notify~! Saving file your-router.txt...
```

Igloo was created with sysadmins in mind. Grab your NAT’d IP address or configure your routing table with ease:
```
igloo~$ show ip public
notify~! Your translated address is [Output Omitted]

igloo~$ ip route 172.16.1.0/24 10.0.0.1 9 metric 15
igloo~$ ip route 10.200.0.0/16 192.168.1.254 9
```
Igloo also enables granular client VPN configuration without the fuss of GUIs or lengthy PowerShell commands:

```
igloo~$ crypto ipsec aes256 sha256 group14
conf~$ Name the vpn connection: myvpn
conf~$ Enter the IP address of your vpn server: 1.1.1.1

notify~! Creating VPN adapter...
notify~! Configuring encryption, hash, and DH group options...
notify~! IPSec VPN 'myvpn' has been created: [Output Omitted]
```

# Running with Python
1. Install Python 3.7.2 from the official Python website. Be sure to check the option to include Python in your PATH.
2. Run cmd.exe or PowerShell as an administrator.
3. Update pip to the latest version and install the NetMiko library with the following commands:
```
pip install --upgrade pip
pip install netmiko
```
# Running the exe
For the Windows installer, visit https://easyigloo.org.

For more info, please refer to the docs at https://easyigloo.org/getting-started.



