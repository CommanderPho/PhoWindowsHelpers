<#
.SYNOPSIS
    FastCopy Post-Process script to delete sources and replace them with symlinks to the new destinations.
#>
param (
    [Parameter(Mandatory=$true, Position=0)]
    [string]$SourceString,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$DestinationDir
)

# FastCopy passes multiple sources separated by semicolons
$sources = $SourceString -split ';'

# Clean up the destination path formatting
$DestinationDir = $DestinationDir.Trim('"').TrimEnd('\')

foreach ($sourcePath in $sources) {
    $sourcePath = $sourcePath.Trim().Trim('"').TrimEnd('\')
    
    if (Test-Path -Path $sourcePath) {
        $itemName = Split-Path -Path $sourcePath -Leaf
        $targetDest = Join-Path -Path $DestinationDir -ChildPath $itemName

        # Verify that the item was successfully copied to the destination
        if (Test-Path -Path $targetDest) {
            # 1. Delete the source file/folder
            Remove-Item -Path $sourcePath -Recurse -Force

            # 2. Create the symlink in place of the old source
            New-Item -ItemType SymbolicLink -Path $sourcePath -Target $targetDest | Out-Null
            
            Write-Host "Replaced '$sourcePath' with symlink to '$targetDest'."
        } else {
            Write-Warning "Destination not found for '$sourcePath'. Skipping deletion and symlink creation."
        }
    }
}