 # Command dictionary for the server uninstall command set
uninstall_dictionary = {
	'uninstall ad-cs cert-authority':'Uninstall-WindowsFeature -Name ADCS-Cert-Authority | Out-Null',
	'uninstall ad-cs enrollment ca-service':'Uninstall-WindowsFeature -Name ADCS-Web-Enrollment | Out-Null',
	'uninstall ad-cs enrollment web-service':'Uninstall-WindowsFeature -Name ADCS-Enroll-Web-Svc | Out-Null',
	'uninstall ad-cs enrollment dev-service':'Uninstall-WindowsFeature -Name ADCS-Device-Enrollment | Out-Null',
	'uninstall ad-cs enrollment policy-web-service':'Uninstall-WindowsFeature -Name ADCS-Enroll-Web-Pol  | Out-Null',
	'uninstall ad-cs responder':'Uninstall-WindowsFeature -Name ADCS-Online-Cert | Out-Null',
	'uninstall ad-rights id':'Uninstall-WindowsFeature -Name ADRMS-Identity | Out-Null',
	'uninstall ad-rights server':'Uninstall-WindowsFeature -Name ADRMS-Server | Out-Null',
	'uninstall app-server com':'Uninstall-WindowsFeature -Name AS-Ent-Services | Out-Null',
	'uninstall app-server http':'Uninstall-WindowsFeature -Name AS-HTTP-Activation | Out-Null',
	'uninstall app-server msmq':'Uninstall-WindowsFeature -Name AS-MSMQ-Activation | Out-Null',
	'uninstall app-server named-pipes':'Uninstall-WindowsFeature -Name AS-Named-Pipes | Out-Null',
	'uninstall app-server dotnet45':'Uninstall-WindowsFeature -Name AS-NET-Framework | Out-Null',
	'uninstall app-server tcp':'Uninstall-WindowsFeature -Name AS-TCP-Activation | Out-Null',
	'uninstall app-server tcp-sharing':'Uninstall-WindowsFeature -Name AS-TCP-Port-Sharing | Out-Null',
	'uninstall app-server transaction atomic':'Uninstall-WindowsFeature -Name AS-WS-Atomic | Out-Null',
	'uninstall app-server transaction distributed':'Uninstall-WindowsFeature -Name AS-Dist-Transaction | Out-Null',
	'uninstall app-server transaction incoming':'Uninstall-WindowsFeature -Name AS-Incoming-Trans | Out-Null',
	'uninstall app-server transaction outgoing':'Uninstall-WindowsFeature -Name AS-Outgoing-Trans | Out-Null',
	'uninstall app-server was':'Uninstall-WindowsFeature -Name AS-WAS-Support | Out-Null',
	'uninstall app-server web-support':'Uninstall-WindowsFeature -Name AS-Web-Support | Out-Null',
	'uninstall bitlocker network-unlock':'Uninstall-WindowsFeature -Name BitLocker-NetworkUnlock  | Out-Null',
	'uninstall bits compact-server':'Uninstall-WindowsFeature -Name BITS-Compact-Server  | Out-Null',
	'uninstall bits iis':'Uninstall-WindowsFeature -Name BITS-IIS-Ext  | Out-Null',
	'uninstall dotnet http-activation':'Uninstall-WindowsFeature -Name NET-HTTP-Activation  | Out-Null',
	'uninstall dotnet nonhttp-activation':'Uninstall-WindowsFeature -Name NET-Non-HTTP-Activ  | Out-Null',
	'uninstall dotnet45 aspnet ':'Uninstall-WindowsFeature -Name NET-Framework-45-ASPNET  | Out-Null',
	'uninstall dotnet45 http-activation':'Uninstall-WindowsFeature -Name NET-WCF-HTTP-Activation45  | Out-Null',
	'uninstall dotnet45 msmq-activation':'Uninstall-WindowsFeature -Name NET-WCF-MSMQ-Activation45  | Out-Null',
	'uninstall dotnet45 pipe-activation':'Uninstall-WindowsFeature -Name NET-WCF-Pipe-Activation45  | Out-Null',
	'uninstall dotnet45 tcp-activation':'Uninstall-WindowsFeature -Name NET-WCF-TCP-Activation45  | Out-Null',
	'uninstall dotnet45 tcp-port-sharing':'Uninstall-WindowsFeature -Name NET-WCF-TCP-PortSharing45  | Out-Null',
	'uninstall dotnet45 wcf':'Uninstall-WindowsFeature -Name NET-WCF-Services45  | Out-Null',
	'uninstall feature ad-cs':'Uninstall-WindowsFeature -Name AD-Certificate | Out-Null',
	'uninstall feature ad-ds':'Uninstall-WindowsFeature -Name AD-Domain-Services | Out-Null',
	'uninstall feature ad-fs':'Uninstall-WindowsFeature -Name ADFS-Federation | Out-Null',
	'uninstall feature ad-rights':'Uninstall-WindowsFeature -Name ADRMS | Out-Null',
	'uninstall feature adlds':'Uninstall-WindowsFeature -Name ADLDS | Out-Null',
	'uninstall feature app-server':'Uninstall-WindowsFeature -Name Application-Server  | Out-Null',
	'uninstall feature biometrics':'Uninstall-WindowsFeature -Name Biometric-Framework  | Out-Null',
	'uninstall feature bitlocker':'Uninstall-WindowsFeature -Name BitLocker  | Out-Null',
	'uninstall feature bits':'Uninstall-WindowsFeature -Name BITS  | Out-Null',
	'uninstall feature branch-cache':'Uninstall-WindowsFeature -Name BranchCache  | Out-Null',
	'uninstall feature cmak':'Uninstall-WindowsFeature -Name CMAK  | Out-Null',
	'uninstall feature dc-bridge':'Uninstall-WindowsFeature -Name Data-Center-Bridging  | Out-Null',
	'uninstall feature desktop-experience':'Uninstall-WindowsFeature -Name Desktop-Experience  | Out-Null',
	'uninstall feature dhcp-server':'Uninstall-WindowsFeature -Name DHCP | Out-Null',
	'uninstall feature direct-access':'Uninstall-WindowsFeature -Name DirectAccess-VPN | Out-Null',
	'uninstall feature direct-play':'Uninstall-WindowsFeature -Name Direct-Play  | Out-Null',
	'uninstall feature dns-server':'Uninstall-WindowsFeature -Name DNS | Out-Null',
	'uninstall feature dotnet':'Uninstall-WindowsFeature -Name NET-Framework-Features | Out-Null',
	'uninstall feature dotnet-core':'Uninstall-WindowsFeature -Name NET-Framework-Core  | Out-Null',
	'uninstall feature dotnet45':'Uninstall-WindowsFeature -Name NET-Framework-45-Features | Out-Null',
	'uninstall feature dotnet45-core':'Uninstall-WindowsFeature -Name NET-Framework-45-Core  | Out-Null',
	'uninstall feature dsc-service':'Uninstall-WindowsFeature -Name DSC-Service  | Out-Null',
	'uninstall feature enhanced-storage':'Uninstall-WindowsFeature -Name EnhancedStorage  | Out-Null',
	'uninstall feature failover-clustering':'Uninstall-WindowsFeature -Name Failover-Clustering  | Out-Null',
	'uninstall feature fax':'Uninstall-WindowsFeature -Name Fax | Out-Null',
	'uninstall feature gpmc':'Uninstall-WindowsFeature -Name GPMC  | Out-Null',
	'uninstall feature handwriting-services':'Uninstall-WindowsFeature -Name InkAndHandwritingServices  | Out-Null',
	'uninstall feature hyperv':'Uninstall-WindowsFeature -Name Hyper-V | Out-Null',
	'uninstall feature iis':'Uninstall-WindowsFeature -Name Web-Server | Out-Null',
	'uninstall feature internet-print-client':'Uninstall-WindowsFeature -Name Internet-Print-Client  | Out-Null',
	'uninstall feature ipam':'Uninstall-WindowsFeature -Name IPAM  | Out-Null',
	'uninstall feature ipam-client':'Uninstall-WindowsFeature -Name IPAM-Client-Feature  | Out-Null',
	'uninstall feature iscsi':'Uninstall-WindowsFeature -Name File-Services | Out-Null',
	'uninstall feature isns':'Uninstall-WindowsFeature -Name ISNS  | Out-Null',
	'uninstall feature lpr-port-monitor':'Uninstall-WindowsFeature -Name LPR-Port-Monitor  | Out-Null',
	'uninstall feature msmq':'Uninstall-WindowsFeature -Name MSMQ  | Out-Null',
	'uninstall feature multipath-io':'Uninstall-WindowsFeature -Name Multipath-IO  | Out-Null',
	'uninstall feature nfs-client':'Uninstall-WindowsFeature -Name NFS-Client  | Out-Null',
	'uninstall feature nlb':'Uninstall-WindowsFeature -Name NLB  | Out-Null',
	'uninstall feature npas':'Uninstall-WindowsFeature -Name NPAS | Out-Null',
	'uninstall feature pnrp':'Uninstall-WindowsFeature -Name PNRP  | Out-Null',
	'uninstall feature print-internet':'Uninstall-WindowsFeature -Name Print-Internet | Out-Null',
	'uninstall feature print-lpd':'Uninstall-WindowsFeature -Name Print-LPD-Service | Out-Null',
	'uninstall feature print-services':'Uninstall-WindowsFeature -Name Print-Services | Out-Null',
	'uninstall feature pshell':'Uninstall-WindowsFeature -Name PowerShell  | Out-Null',
	'uninstall feature pshell-ise':'Uninstall-WindowsFeature -Name PowerShell-ISE  | Out-Null',
	'uninstall feature pshell-root':'Uninstall-WindowsFeature -Name PowerShellRoot  | Out-Null',
	'uninstall feature pshell-v2':'Uninstall-WindowsFeature -Name PowerShell-V2  | Out-Null',
	'uninstall feature pshell-web-access':'Uninstall-WindowsFeature -Name WindowsPowerShellWebAccess  | Out-Null',
	'uninstall feature qwave':'Uninstall-WindowsFeature -Name qWave  | Out-Null',
	'uninstall feature rdc':'Uninstall-WindowsFeature -Name RDC  | Out-Null',
	'uninstall feature rdp-server':'Uninstall-WindowsFeature -Name Remote-Desktop-Services | Out-Null',
	'uninstall feature remote-access':'Uninstall-WindowsFeature -Name RemoteAccess | Out-Null',
	'uninstall feature remote-assist':'Uninstall-WindowsFeature -Name Remote-Assistance  | Out-Null',
	'uninstall feature routing':'Uninstall-WindowsFeature -Name DirectAccess-VPN | Out-Null',
	'uninstall feature routing':'Uninstall-WindowsFeature -Name Routing | Out-Null',
	'uninstall feature rpc-over-http-proxy':'Uninstall-WindowsFeature -Name RPC-over-HTTP-Proxy | Out-Null',
	'uninstall feature rsat':'Uninstall-WindowsFeature -Name RSAT  | Out-Null',
	'uninstall feature scan-server':'Uninstall-WindowsFeature -Name Print-Scan-Server | Out-Null',
	'uninstall feature search-service':'Uninstall-WindowsFeature -Name Search-Service  | Out-Null',
	'uninstall feature server-backup':'Uninstall-WindowsFeature -Name Windows-Server-Backup  | Out-Null',
	'uninstall feature server-essentials':'Uninstall-WindowsFeature -Name ServerEssentialsRole  | Out-Null',
	'uninstall feature server-gui-mgmt':'Uninstall-WindowsFeature -Name Server-Gui-Mgmt-Infra | Out-Null',
	'uninstall feature server-gui-shell':'Uninstall-WindowsFeature -Name Server-Gui-Shell  | Out-Null',
	'uninstall feature server-media-foundation':'Uninstall-WindowsFeature -Name Server-Media-Foundation  | Out-Null',
	'uninstall feature server-migration':'Uninstall-WindowsFeature -Name Migration  | Out-Null',
	'uninstall feature simple-tcpip':'Uninstall-WindowsFeature -Name Simple-TCPIP  | Out-Null',
	'uninstall feature smb-1':'Uninstall-WindowsFeature -Name FS-SMB1  | Out-Null',
	'uninstall feature smb-bandwidth-limit':'Uninstall-WindowsFeature -Name FS-SMBBW  | Out-Null',
	'uninstall feature smtp-server':'Uninstall-WindowsFeature -Name SMTP-Server  | Out-Null',
	'uninstall feature smtp-services':'Uninstall-WindowsFeature -Name SNMP-Service  | Out-Null',
	'uninstall feature snmp-wmi-provider':'Uninstall-WindowsFeature -Name SNMP-WMI-Provider  | Out-Null',
	'uninstall feature storage':'Uninstall-WindowsFeature -Name FileAndStorage-Services | Out-Null',
	'uninstall feature telnet-client':'Uninstall-WindowsFeature -Name Telnet-Client  | Out-Null',
	'uninstall feature telnet-server':'Uninstall-WindowsFeature -Name Telnet-Server  | Out-Null',
	'uninstall feature tftp':'Uninstall-WindowsFeature -Name TFTP-Client  | Out-Null',
	'uninstall feature update-services':'Uninstall-WindowsFeature -Name UpdateServices  | Out-Null',
	'uninstall feature user-interfaces':'Uninstall-WindowsFeature -Name User-Interfaces-Infra  | Out-Null',
	'uninstall feature volume-activation':'Uninstall-WindowsFeature -Name VolumeActivation | Out-Null',
	'uninstall feature was api':'Uninstall-WindowsFeature -Name WAS-Config-APIs | Out-Null',
	'uninstall feature was':'Uninstall-WindowsFeature -Name WAS  | Out-Null',
	'uninstall feature was-dotnet-env':'Uninstall-WindowsFeature -Name WAS-NET-Environment  | Out-Null',
	'uninstall feature was-proc-model':'Uninstall-WindowsFeature -Name WAS-Process-Model  | Out-Null',
	'uninstall feature wds':'Uninstall-WindowsFeature -Name WDS  | Out-Null',
	'uninstall feature wds-admin-pack':'Uninstall-WindowsFeature -Name WDS-AdminPack  | Out-Null',
	'uninstall feature web-proxy':'Uninstall-WindowsFeature -Name Web-Application-Proxy | Out-Null',
	'uninstall feature wff':'Uninstall-WindowsFeature -Name WFF  | Out-Null',
	'uninstall feature win-identity-foundation':'Uninstall-WindowsFeature -Name Windows-Identity-Foundation  | Out-Null',
	'uninstall feature win-internal-database':'Uninstall-WindowsFeature -Name Windows-Internal-Database  | Out-Null',
	'uninstall feature win-storage-mgmt':'Uninstall-WindowsFeature -Name WindowsStorageManagementService  | Out-Null',
	'uninstall feature win-tiff-ifilter':'Uninstall-WindowsFeature -Name Windows-TIFF-IFilter  | Out-Null',
	'uninstall feature wins':'Uninstall-WindowsFeature -Name WINS  | Out-Null',
	'uninstall feature wireless-networking':'Uninstall-WindowsFeature -Name Wireless-Networking  | Out-Null',
	'uninstall feature wow64-support':'Uninstall-WindowsFeature -Name WoW64-Support  | Out-Null',
	'uninstall feature xps-viewer':'Uninstall-WindowsFeature -Name XPS-Viewer | Out-Null',
	'uninstall hypverv pshell':'Uninstall-WindowsFeature -Name Hyper-V-PowerShell  | Out-Null',
	'uninstall hypverv tools':'Uninstall-WindowsFeature -Name Hyper-V-Tools  | Out-Null',
	'uninstall iis app-dev':'Uninstall-WindowsFeature -Name Web-App-Dev  | Out-Null',
	'uninstall iis app-init':'Uninstall-WindowsFeature -Name Web-AppInit  | Out-Null',
	'uninstall iis asp':'Uninstall-WindowsFeature -Name Web-ASP  | Out-Null',
	'uninstall iis asp-net':'Uninstall-WindowsFeature -Name Web-Asp-Net  | Out-Null',
	'uninstall iis asp-net45':'Uninstall-WindowsFeature -Name Web-Asp-Net45  | Out-Null',
	'uninstall iis auto-compression':'Uninstall-WindowsFeature -Name Web-Dyn-Compression | Out-Null',
	'uninstall iis basic-auth':'Uninstall-WindowsFeature -Name Web-Basic-Auth | Out-Null',
	'uninstall iis cgi':'Uninstall-WindowsFeature -Name Web-CGI  | Out-Null',
	'uninstall iis client-cert-auth':'Uninstall-WindowsFeature -Name Web-Cert-Auth  | Out-Null',
	'uninstall iis client-hash-auth':'Uninstall-WindowsFeature -Name Web-Digest-Auth | Out-Null',
	'uninstall iis default-doc':'Uninstall-WindowsFeature -Name Web-Default-Doc | Out-Null',
	'uninstall iis dir-browser':'Uninstall-WindowsFeature -Name Web-Dir-Browsing | Out-Null',
	'uninstall iis ftp-ext':'Uninstall-WindowsFeature -Name Web-Ftp-Ext  | Out-Null',
	'uninstall iis ftp-server':'Uninstall-WindowsFeature -Name Web-Ftp-Server  | Out-Null',
	'uninstall iis ftp-service':'Uninstall-WindowsFeature -Name Web-Ftp-Service  | Out-Null',
	'uninstall iis health':'Uninstall-WindowsFeature -Name Web-Health | Out-Null',
	'uninstall iis http-common':'Uninstall-WindowsFeature -Name Web-Common-Http | Out-Null',
	'uninstall iis http-errors':'Uninstall-WindowsFeature -Name Web-Http-Errors | Out-Null',
	'uninstall iis http-redirect':'Uninstall-WindowsFeature -Name Web-Http-Redirect | Out-Null',
	'uninstall iis http-tracing':'Uninstall-WindowsFeature -Name Web-Http-Tracing | Out-Null',
	'uninstall iis hwc':'Uninstall-WindowsFeature -Name Web-HWC  | Out-Null',
	'uninstall iis ip-security':'Uninstall-WindowsFeature -Name Web-IP-Security | Out-Null',
	'uninstall iis isapi':'Uninstall-WindowsFeature -Name Web-ISAPI-Ext  | Out-Null',
	'uninstall iis isapi-filter':'Uninstall-WindowsFeature -Name Web-ISAPI-Filter  | Out-Null',
	'uninstall iis legacy-scripting':'Uninstall-WindowsFeature -Name Web-Lgcy-Scripting  | Out-Null',
	'uninstall iis logging custom':'Uninstall-WindowsFeature -Name Web-Custom-Logging | Out-Null',
	'uninstall iis logging http':'Uninstall-WindowsFeature -Name Web-Http-Logging | Out-Null',
	'uninstall iis logging libs':'Uninstall-WindowsFeature -Name Web-Log-Libraries | Out-Null',
	'uninstall iis logging odbc':'Uninstall-WindowsFeature -Name Web-ODBC-Logging | Out-Null',
	'uninstall iis metabase':'Uninstall-WindowsFeature -Name Web-Metabase  | Out-Null',
	'uninstall iis mgmt-compatibility':'Uninstall-WindowsFeature -Name Web-Mgmt-Compat  | Out-Null',
	'uninstall iis mgmt-console':'Uninstall-WindowsFeature -Name Web-Mgmt-Console  | Out-Null',
	'uninstall iis mgmt-console-legacy':'Uninstall-WindowsFeature -Name Web-Lgcy-Mgmt-Console  | Out-Null',
	'uninstall iis mgmt-service':'Uninstall-WindowsFeature -Name Web-Mgmt-Service  | Out-Null',
	'uninstall iis mgmt-tools':'Uninstall-WindowsFeature -Name Web-Mgmt-Tools  | Out-Null',
	'uninstall iis net':'Uninstall-WindowsFeature -Name Web-Net-Ext  | Out-Null',
	'uninstall iis net-45':'Uninstall-WindowsFeature -Name Web-Net-Ext45  | Out-Null',
	'uninstall iis odata':'Uninstall-WindowsFeature -Name ManagementOdata  | Out-Null',
	'uninstall iis performance':'Uninstall-WindowsFeature -Name Web-Performance | Out-Null',
	'uninstall iis request-mon':'Uninstall-WindowsFeature -Name Web-Request-Monitor | Out-Null',
	'uninstall iis scripting':'Uninstall-WindowsFeature -Name Web-Scripting-Tools  | Out-Null',
	'uninstall iis security':'Uninstall-WindowsFeature -Name Web-Security | Out-Null',
	'uninstall iis ssi':'Uninstall-WindowsFeature -Name Web-Includes  | Out-Null',
	'uninstall iis ssl-provider':'Uninstall-WindowsFeature -Name Web-CertProvider | Out-Null',
	'uninstall iis static-compression':'Uninstall-WindowsFeature -Name Web-Stat-Compression | Out-Null',
	'uninstall iis static-content':'Uninstall-WindowsFeature -Name Web-Static-Content | Out-Null',
	'uninstall iis url-auth':'Uninstall-WindowsFeature -Name Web-Url-Auth | Out-Null',
	'uninstall iis web-filter':'Uninstall-WindowsFeature -Name Web-Filtering | Out-Null',
	'uninstall iis web-server':'Uninstall-WindowsFeature -Name Web-WebServer | Out-Null',
	'uninstall iis web-sockets':'Uninstall-WindowsFeature -Name Web-WebSockets  | Out-Null',
	'uninstall iis webdav-publishing':'Uninstall-WindowsFeature -Name Web-DAV-Publishing | Out-Null',
	'uninstall iis windows-auth':'Uninstall-WindowsFeature -Name Web-Windows-Auth | Out-Null',
	'uninstall iis winrm':'Uninstall-WindowsFeature -Name WinRM-IIS-Ext  | Out-Null',
	'uninstall iis wmi':'Uninstall-WindowsFeature -Name Web-WMI  | Out-Null',
	'uninstall iscsi branch-cache':'Uninstall-WindowsFeature -Name FS-BranchCache  | Out-Null',
	'uninstall iscsi dedup':'Uninstall-WindowsFeature -Name FS-Data-Deduplication | Out-Null',
	'uninstall iscsi dfs-replicate':'Uninstall-WindowsFeature -Name FS-DFS-Replication | Out-Null',
	'uninstall iscsi dfs-resource-mgmt':'Uninstall-WindowsFeature -Name FS-Resource-Manager | Out-Null',
	'uninstall iscsi dfs-space':'Uninstall-WindowsFeature -Name FS-DFS-Namespace | Out-Null',
	'uninstall iscsi nfs-service':'Uninstall-WindowsFeature -Name FS-NFS-Service | Out-Null',
	'uninstall iscsi server':'Uninstall-WindowsFeature -Name FS-FileServer | Out-Null',
	'uninstall iscsi sync-share':'Uninstall-WindowsFeature -Name FS-SyncShareService | Out-Null',
	'uninstall iscsi target-server':'Uninstall-WindowsFeature -Name FS-iSCSITarget-Server | Out-Null',
	'uninstall iscsi target-vss':'Uninstall-WindowsFeature -Name iSCSITarget-VSS-VDS | Out-Null',
	'uninstall iscsi vss':'Uninstall-WindowsFeature -Name FS-VSS-Agent | Out-Null',
	'uninstall feature linux-subsystem':'Enable-WindowsOptionalFeature -online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart | Out-Null',
	'uninstall msmq dcom':'Uninstall-WindowsFeature -Name MSMQ-DCOM  | Out-Null',
	'uninstall msmq directory':'Uninstall-WindowsFeature -Name MSMQ-Directory  | Out-Null',
	'uninstall msmq http-support':'Uninstall-WindowsFeature -Name MSMQ-HTTP-Support  | Out-Null',
	'uninstall msmq multicast':'Uninstall-WindowsFeature -Name MSMQ-Multicasting  | Out-Null',
	'uninstall msmq routing':'Uninstall-WindowsFeature -Name MSMQ-Routing  | Out-Null',
	'uninstall msmq server':'Uninstall-WindowsFeature -Name MSMQ-Server  | Out-Null',
	'uninstall msmq services':'Uninstall-WindowsFeature -Name MSMQ-Services  | Out-Null',
	'uninstall msmq triggers':'Uninstall-WindowsFeature -Name MSMQ-Triggers  | Out-Null',
	'uninstall npas health':'Uninstall-WindowsFeature -Name NPAS-Health | Out-Null',
	'uninstall npas host-authorization':'Uninstall-WindowsFeature -Name NPAS-Host-Cred | Out-Null',
	'uninstall npas policy-server':'Uninstall-WindowsFeature -Name NPAS-Policy-Server | Out-Null',
	'uninstall rdp connection-broker':'Uninstall-WindowsFeature -Name RDS-Connection-Broker | Out-Null',
	'uninstall rdp gateway':'Uninstall-WindowsFeature -Name RDS-Gateway | Out-Null',
	'uninstall rdp licensing':'Uninstall-WindowsFeature -Name RDS-Licensing | Out-Null',
	'uninstall rdp session-host':'Uninstall-WindowsFeature -Name RDS-RD-Server | Out-Null',
	'uninstall rdp virtual':'Uninstall-WindowsFeature -Name RDS-Virtualization | Out-Null',
	'uninstall rdp web-access':'Uninstall-WindowsFeature -Name RDS-Web-Access | Out-Null',
	'uninstall rsat ad-admin-center':'Uninstall-WindowsFeature -Name RSAT-AD-AdminCenter  | Out-Null',
	'uninstall rsat ad-cs':'Uninstall-WindowsFeature -Name RSAT-ADCS  | Out-Null',
	'uninstall rsat ad-cs-mgmt':'Uninstall-WindowsFeature -Name RSAT-ADCS-Mgmt  | Out-Null',
	'uninstall rsat ad-ds':'Uninstall-WindowsFeature -Name RSAT-ADDS  | Out-Null',
	'uninstall rsat ad-ds-tools':'Uninstall-WindowsFeature -Name RSAT-ADDS-Tools  | Out-Null',
	'uninstall rsat ad-lds':'Uninstall-WindowsFeature -Name RSAT-ADLDS  | Out-Null',
	'uninstall rsat ad-pshell':'Uninstall-WindowsFeature -Name RSAT-AD-PowerShell  | Out-Null',
	'uninstall rsat ad-rights':'Uninstall-WindowsFeature -Name RSAT-ADRMS  | Out-Null',
	'uninstall rsat ad-tools':'Uninstall-WindowsFeature -Name RSAT-AD-Tools  | Out-Null',
	'uninstall rsat bitlocker-admin':'Uninstall-WindowsFeature -Name RSAT-Feature-Tools-BitLocker | Out-Null',
	'uninstall rsat bitLocker-encryption':'Uninstall-WindowsFeature -Name RSAT-Feature-Tools-BitLocker-RemoteAdminTool  | Out-Null',
	'uninstall rsat bitlocker-recovery':'Uninstall-WindowsFeature -Name RSAT-Feature-Tools-BitLocker-BdeAducExt  | Out-Null',
	'uninstall rsat bits-server':'Uninstall-WindowsFeature -Name RSAT-Bits-Server  | Out-Null',
	'uninstall rsat clustering command-int':'Uninstall-WindowsFeature -Name RSAT-Clustering-CmdInterface  | Out-Null',
	'uninstall rsat clustering':'Uninstall-WindowsFeature -Name RSAT-Clustering  | Out-Null',
	'uninstall rsat clustering-automation':'Uninstall-WindowsFeature -Name RSAT-Clustering-AutomationServer  | Out-Null',
	'uninstall rsat clustering-mgmt':'Uninstall-WindowsFeature -Name RSAT-Clustering-Mgmt  | Out-Null',
	'uninstall rsat clustering-pshell':'Uninstall-WindowsFeature -Name RSAT-Clustering-PowerShell  | Out-Null',
	'uninstall rsat core-file-mgmt':'Uninstall-WindowsFeature -Name RSAT-CoreFile-Mgmt  | Out-Null',
	'uninstall rsat dfs-mgmt':'Uninstall-WindowsFeature -Name RSAT-DFS-Mgmt-Con  | Out-Null',
	'uninstall rsat dhcp':'Uninstall-WindowsFeature -Name RSAT-DHCP  | Out-Null',
	'uninstall rsat dns':'Uninstall-WindowsFeature -Name RSAT-DNS-Server | Out-Null',
	'uninstall rsat fax':'Uninstall-WindowsFeature -Name RSAT-Fax  | Out-Null',
	'uninstall rsat feature-tools':'Uninstall-WindowsFeature -Name RSAT-Feature-Tools  | Out-Null',
	'uninstall rsat file-services':'Uninstall-WindowsFeature -Name RSAT-File-Services  | Out-Null',
	'uninstall rsat fsrm-mgmt':'Uninstall-WindowsFeature -Name RSAT-FSRM-Mgmt  | Out-Null',
	'uninstall rsat hyperv':'Uninstall-WindowsFeature -Name RSAT-Hyper-V-Tools | Out-Null',
	'uninstall rsat license-check':'Uninstall-WindowsFeature -Name RSAT-RDS-Licensing-Diagnosis-UI  | Out-Null',
	'uninstall rsat license-ui':'Uninstall-WindowsFeature -Name RDS-Licensing-UI  | Out-Null',
	'uninstall rsat nfs-admin':'Uninstall-WindowsFeature -Name RSAT-NFS-Admin  | Out-Null',
	'uninstall rsat nis':'Uninstall-WindowsFeature -Name RSAT-NIS  | Out-Null',
	'uninstall rsat nlb':'Uninstall-WindowsFeature -Name RSAT-NLB  | Out-Null',
	'uninstall rsat npas':'Uninstall-WindowsFeature -Name RSAT-NPAS  | Out-Null',
	'uninstall rsat print-services':'Uninstall-WindowsFeature -Name RSAT-Print-Services  | Out-Null',
	'uninstall rsat rds-gateway':'Uninstall-WindowsFeature -Name RSAT-RDS-Gateway  | Out-Null',
	'uninstall rsat rds-tools':'Uninstall-WindowsFeature -Name RSAT-RDS-Tools  | Out-Null',
	'uninstall rsat remote-access':'Uninstall-WindowsFeature -Name RSAT-RemoteAccess  | Out-Null',
	'uninstall rsat remote-access-mgmt':'Uninstall-WindowsFeature -Name RSAT-RemoteAccess-Mgmt  | Out-Null',
	'uninstall rsat remote-access-pshell':'Uninstall-WindowsFeature -Name RSAT-RemoteAccess-PowerShell  | Out-Null',
	'uninstall rsat responder':'Uninstall-WindowsFeature -Name RSAT-Online-Responder  | Out-Null',
	'uninstall rsat role-tools':'Uninstall-WindowsFeature -Name RSAT-Role-Tools  | Out-Null',
	'uninstall rsat smtp':'Uninstall-WindowsFeature -Name RSAT-SMTP  | Out-Null',
	'uninstall rsat snmp':'Uninstall-WindowsFeature -Name RSAT-SNMP  | Out-Null',
	'uninstall rsat va-tools':'Uninstall-WindowsFeature -Name RSAT-VA-Tools  | Out-Null',
	'uninstall rsat wins':'Uninstall-WindowsFeature -Name RSAT-WINS  | Out-Null',
	'uninstall update-service ui':'Uninstall-WindowsFeature -Name UpdateServices-UI  | Out-Null',
	'uninstall update-services api':'Uninstall-WindowsFeature -Name UpdateServices-API  | Out-Null',
	'uninstall update-services database':'Uninstall-WindowsFeature -Name UpdateServices-DB  | Out-Null',
	'uninstall update-services rsat':'Uninstall-WindowsFeature -Name UpdateServices-RSAT  | Out-Null',
	'uninstall update-services services':'Uninstall-WindowsFeature -Name UpdateServices-Services  | Out-Null',
	'uninstall update-services widdb':'Uninstall-WindowsFeature -Name UpdateServices-WidDB  | Out-Null',
	'uninstall wds deployment':'Uninstall-WindowsFeature -Name WDS-Deployment  | Out-Null',
	'uninstall wds transport':'Uninstall-WindowsFeature -Name WDS-Transport | Out-Null',
	'uninstall wds admin-pack':'Uninstall-WindowsFeature -Name WDS-AdminPack | Out-Null',
}