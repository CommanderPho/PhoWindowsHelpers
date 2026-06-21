# Download `WinNFSd`
```ps1
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
& "$HOME\bin\WinNFSd\winnfsd.exe" "L:\SlowSwap" "/NFS_L_SlowSwap"

```



https://forum.kodi.tv/showthread.php?tid=330260
```ps1
nssm install OtherMedia-NFS "~/bin/WinNFSd/winnfsd.exe" "C:\VM_Storage" "/NFS_VMs"
nssm install OtherMedia-NFS "~/bin/WinNFSd/winnfsd.exe" "L:\SlowSwap" "/NFS_L_SlowSwap"


#  E:\OtherMedia /othermedia
```

"E:\My cool Media" /media
### Firewalll Rules


```ps1
# Allow NFS (TCP/UDP 2049) and PortMapper (TCP/UDP 111)
New-NetFirewallRule -DisplayName "NFS-Server-In" -Direction Inbound -LocalPort 111,2049,1058 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "NFS-Server-In-UDP" -Direction Inbound -LocalPort 111,2049,1058 -Protocol UDP -Action Allow
```


## ESXi

### Install the `PowerCLI` PS module
```ps1
Install-Module -Name VCF.PowerCLI -AllowClobber
# Configure PowerCLI to ignore self-signed certificate warnings
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false -Scope User
```


```ps1
# 1. Connect to your ESXi host or vCenter
Connect-VIServer -Server "10.0.0.187" -User "root" -Password "athiest15"

# 2. Mount the NFS Datastore
# -NfsHost: The IP of your NAS/Server
# -Path: The export path on the server (e.g., /volume1/vmware or /nfs/share)
# New-Datastore -Nfs -VMHost "10.0.0.187" `
#               -Name "Network_VM_Storage" `
#               -Path "/volume1/vms" `
#               -NfsHost "10.0.0.248"


New-Datastore -Nfs -VMHost "10.0.0.187" `
              -Name "Network_VM_Storage" `
              -Path "/nfs/share/NFS_VMs" `
              -NfsHost "10.0.0.248"


New-Datastore -Nfs -VMHost "10.0.0.187" `
              -Name "NFS_L_SlowSwap" `
              -Path "/NFS_L_SlowSwap" `
              -NfsHost "10.0.0.248"





New-Datastore -Nfs -VMHost "10.0.0.187" `
              -Name "NFS_SERVER_HOST" `
              -Path "/mnt/host" `
              -NfsHost "10.0.0.54"



```


```ps1
# Enable the Software iSCSI Adapter (if not already enabled)
Get-VMHostStorage -VMHost "10.0.0.187" | Set-VMHostStorage -SoftwareIScenabled $true

# Add the iSCSI Target Portal (Your NAS IP)
Get-VMHost "10.0.0.187" | Get-VMHostHba -Type iScsi | New-IScsiHbaTarget -Address "192.168.1.50"

# Rescan HBAs to find the new storage device
Get-VMHost "10.0.0.187" | Get-VMHostStorage -RescanAllHba

```