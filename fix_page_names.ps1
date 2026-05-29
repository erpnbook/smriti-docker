$pageDir = "d:\Smriti_Retail_OS\apps\smriti_retail_os\smriti_retail_os\page"
$dirs = @('smriti-backup','smriti-barcode','smriti-billing','smriti-desk','smriti-inventory','smriti-loyalty','smriti-purchase','smriti-reports','smriti-shift')

foreach ($dir in $dirs) {
    $oldPath = Join-Path $pageDir $dir
    $newName = $dir -replace '-', '_'
    $newPath = Join-Path $pageDir $newName

    if (Test-Path $oldPath) {
        # Rename files inside first
        Get-ChildItem $oldPath | ForEach-Object {
            $newFile = $_.Name -replace '-', '_'
            if ($_.Name -ne $newFile) {
                Rename-Item $_.FullName $newFile
                Write-Host "  file: $($_.Name) -> $newFile"
            }
        }
        # Rename the directory itself
        Rename-Item $oldPath $newName
        Write-Host "Renamed dir: $dir -> $newName"
    } else {
        Write-Host "Already renamed or not found: $dir"
    }
}

Write-Host ""
Write-Host "Final page directory listing:"
Get-ChildItem $pageDir -Directory | Select-Object -ExpandProperty Name
