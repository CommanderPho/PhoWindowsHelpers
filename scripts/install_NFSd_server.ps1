# 1. Create the tool directory (~/bin/WinNFSd)
# PowerShell understands "~/" as the current user's home directory.
New-Item -Path "~/bin/WinNFSd" -ItemType Directory -Force

# 2. Download WinNFSd executable into that folder
$url = "https://github.com/winnfsd/winnfsd/releases/download/2.4.0/winnfsd.exe"
$toolPath = "~/bin/WinNFSd/winnfsd.exe"
Invoke-WebRequest -Uri $url -OutFile $toolPath

# 3. Create the DATA folder you want to share (e.g., C:\VM_Storage)
# (Keeping this separate from the tool folder is best practice)
New-Item -Path "C:\VM_Storage" -ItemType Directory -Force

# 4. Start the NFS Server
# Note: We use '&' (Call Operator) because the path contains a tilde
Write-Host "Starting NFS Server. Press Ctrl+C to stop."
& "$HOME\bin\WinNFSd\winnfsd.exe" "C:\VM_Storage" "/NFS_VMs"




# C:\path\to\a\mount > /alias
# C:\path\to\another\mount > /another-alias
# WinNFSd.exe -pathFile C:\path\to\your\pathfile