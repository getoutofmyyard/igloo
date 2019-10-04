$ErrorActionPreference = "SilentlyContinue"
If ($Error) {
	$Error.Clear()
}
$Today = Get-Date

$UpdateCollection = New-Object -ComObject Microsoft.Update.UpdateColl
$Searcher = New-Object -ComObject Microsoft.Update.Searcher
$Session = New-Object -ComObject Microsoft.Update.Session

Write-Host "notify~! Checking for Windows updates."
$Result = $Searcher.Search("IsInstalled=0 and Type='Software' and IsHidden=0")

If ($Result.Updates.Count -EQ 0) {
	Write-Host "notify~! No outstanding updates were found for this device."
	Write-Host " "
}
Else {
	Write-Host "notify~! Preparing list of updates..."
	$Counter = 0
	$DisplayCount = 0
	Add-Content $ReportFile "`r`n"
	Write-Host "notify~! Initializing updates. Please wait..."
	Add-Content $ReportFile "notify~! Initializing download..."
	$Downloader = $Session.CreateUpdateDownloader()
	$UpdatesList = $Result.Updates
	For ($Counter = 0; $Counter -LT $Result.Updates.Count; $Counter++) {
		$UpdateCollection.Add($UpdatesList.Item($Counter)) | Out-Null
		$ShowThis = $UpdatesList.Item($Counter).Title
		$DisplayCount = $Counter + 1
		Write-Host "notify~! Downloading $ShowThis `r"
		$Downloader.Updates = $UpdateCollection
		$Track = $Downloader.Download()
		If (($Track.HResult -EQ 0) -AND ($Track.ResultCode -EQ 2)) {
			Write-Host" Download succeeded!"
		}
		Else {
			Add-Content $ReportFile "error~! Download failed with error $Error()"
			$Error.Clear()
			Add-content $ReportFile "`r"
		}	
	}
	$Counter = 0
	$DisplayCount = 0
	Write-Host "notify~! Installing updates..."
	$Installer = New-Object -ComObject Microsoft.Update.Installer
	For ($Counter = 0; $Counter -LT $UpdateCollection.Count; $Counter++) {
		$Track = $Null
		$DisplayCount = $Counter + 1
		$WriteThis = $UpdateCollection.Item($Counter).Title
		Write-Host "notify~! Installing $WriteThis"
		$Installer.Updates = $UpdateCollection
		Try {
			$Track = $Installer.Install()
			Write-Host "notify~! Windows updates were installed successfully."
		}
		Catch {
			[System.Exception]
			Write-Host "error~! Update failed with the following error: $Error()"
			$Error.Clear()
		}	
	}
}