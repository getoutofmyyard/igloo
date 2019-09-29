# Windows command dictionary for applets which
# require os.system() to run

win_os_command_set = {
	'cls':'cls',
	'tftp':'tftp',
	'ftp':'ftp',
	'telnet':'telnet',
	'netsh':'netsh',
	'powershell policy as':'powershell Set-ExecutionPolicy -ExecutionPolicy AllSigned',
	'powershell policy open':'powershell Set-ExecutionPolicy -ExecutionPolicy Unrestricted',
	'powershell policy remote':'powershell Set-ExecutionPolicy -ExecutionPolicy RemoteSigned',
	'powershell policy restrict':'powershell Set-ExecutionPolicy -ExecutionPolicy Restricted',
	'win app':'appwiz.cpl',
	'win blu':'bthprops.cpl',
	'win cmd':'cmd.exe',
	'win dev':'devmgmt.msc',
	'win disk':'diskmgmt.msc',
	'win display':'control desk.cpl',
	'win fwall':'WF.msc',
	'win ie':'inetcpl.cpl',
	'win ir':'control irprops.cpl',
	'win perfmon':'perfmon.msc',
	'win powershell':'powershell.exe',
	'win print':'control printers',
	'win scsi':'iscsicpl.exe',
	'win services':'services.msc',
	'win taskschd':'taskschd',
	'win wev':'eventvwr.msc'
}