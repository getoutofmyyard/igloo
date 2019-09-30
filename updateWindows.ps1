$ErrorActionPreference = "SilentlyContinue"
If ($Error) {
	$Error.Clear()
}
$Today = Get-Date

$UpdateCollection = New-Object -ComObject Microsoft.Update.UpdateColl
$Searcher = New-Object -ComObject Microsoft.Update.Searcher
$Session = New-Object -ComObject Microsoft.Update.Session

Write-Host
Write-Host "notify~! Checking for Windows updates. Please wait..."
$Result = $Searcher.Search("IsInstalled=0 and Type='Software' and IsHidden=0")

If ($Result.Updates.Count -EQ 0) {
	Write-Host "notify~! No outstanding updates were found for this device."
	Write-Host " "
}
Else {
	$ReportFile = $Env:ComputerName + "_Report.txt"
	If (Test-Path $ReportFile) {
		Remove-Item $ReportFile
	}
	New-Item $ReportFile -Type File -Force -Value "Windows Update Report For Computer: $Env:ComputerName`r`n" | Out-Null
	Add-Content $ReportFile "Report Created On: $Today`r"
	Add-Content $ReportFile "==============================================================================`r`n"
	Write-Host "notify~! Preparing list of updates..."
	Add-Content $ReportFile "List of Applicable Updates For This Computer`r"
	Add-Content $ReportFile "------------------------------------------------`r"
	For ($Counter = 0; $Counter -LT $Result.Updates.Count; $Counter++) {
		$DisplayCount = $Counter + 1
    		$Update = $Result.Updates.Item($Counter)
		$UpdateTitle = $Update.Title
		Add-Content $ReportFile "`t $DisplayCount -- $UpdateTitle"
	}
	$Counter = 0
	$DisplayCount = 0
	Add-Content $ReportFile "`r`n"
	Write-Host "notify~! Initializing updates..."
	Add-Content $ReportFile "notify~! Initialising download"
	$Downloader = $Session.CreateUpdateDownloader()
	$UpdatesList = $Result.Updates
	For ($Counter = 0; $Counter -LT $Result.Updates.Count; $Counter++) {
		$UpdateCollection.Add($UpdatesList.Item($Counter)) | Out-Null
		$ShowThis = $UpdatesList.Item($Counter).Title
		$DisplayCount = $Counter + 1
		Add-Content $ReportFile "`t $DisplayCount -- Downloading Update $ShowThis `r"
		$Downloader.Updates = $UpdateCollection
		$Track = $Downloader.Download()
		If (($Track.HResult -EQ 0) -AND ($Track.ResultCode -EQ 2)) {
			Add-Content $ReportFile "`t Download Status: SUCCESS"
		}
		Else {
			Add-Content $ReportFile "`t Download Status: FAILED With Error -- $Error()"
			$Error.Clear()
			Add-content $ReportFile "`r"
		}	
	}
	$Counter = 0
	$DisplayCount = 0
	Write-Host "notify~! Installing updates..."
	Add-Content $ReportFile "`r`n"
	Add-Content $ReportFile "Installation of Downloaded Updates"
	Add-Content $ReportFile "------------------------------------------------`r"
	$Installer = New-Object -ComObject Microsoft.Update.Installer
	For ($Counter = 0; $Counter -LT $UpdateCollection.Count; $Counter++) {
		$Track = $Null
		$DisplayCount = $Counter + 1
		$WriteThis = $UpdateCollection.Item($Counter).Title
		Add-Content $ReportFile "`t $DisplayCount -- Installing Update: $WriteThis"
		$Installer.Updates = $UpdateCollection
		Try {
			$Track = $Installer.Install()
			Add-Content $ReportFile "notify~! Windows updates were installed successfully."
		}
		Catch {
			[System.Exception]
			Add-Content $ReportFile "error~! Update failed with the following error: $Error()"
			$Error.Clear()
			Add-content $ReportFile "`r"
		}	
	}
}