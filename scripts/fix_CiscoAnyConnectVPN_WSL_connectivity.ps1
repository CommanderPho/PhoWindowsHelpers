# Fix-WSL-CiscoVPN.ps1
# Restores WSL2 connectivity after connecting to Cisco Secure Client
# by increasing the Cisco VPN interface metric.

$ErrorActionPreference = 'Stop'

# Require Administrator privileges.
$currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($currentIdentity)

if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Administrator privileges are required. Requesting elevation..." -ForegroundColor Yellow

    $scriptPath = $PSCommandPath
    Start-Process pwsh `
        -Verb RunAs `
        -ArgumentList @(
            '-NoProfile'
            '-ExecutionPolicy', 'Bypass'
            '-File', "`"$scriptPath`""
        )

    exit
}

Write-Host "Checking for Cisco Secure Client adapter..." -ForegroundColor Cyan

$ciscoAdapters = @(Get-NetAdapter |
    Where-Object {
        $_.InterfaceDescription -match 'Cisco AnyConnect'
    })

if ($ciscoAdapters.Count -eq 0) {
    Write-Host ""
    Write-Host "No Cisco AnyConnect network adapter was found." -ForegroundColor Red
    Write-Host "Make sure Cisco Secure Client is connected, then run this script again."
    exit 1
}

foreach ($adapter in $ciscoAdapters) {
    Write-Host ""
    Write-Host "Found: $($adapter.InterfaceAlias)" -ForegroundColor Green
    Write-Host "  Description: $($adapter.InterfaceDescription)"
    Write-Host "  ifIndex:     $($adapter.ifIndex)"
    Write-Host "  Status:      $($adapter.Status)"

    $ipInterfaces = @(Get-NetIPInterface -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4)

    if ($ipInterfaces.Count -eq 0) {
        Write-Host "  No IPv4 interface found; skipping." -ForegroundColor Yellow
        continue
    }

    foreach ($ipInterface in $ipInterfaces) {
        Write-Host "  Current metric: $($ipInterface.InterfaceMetric)"

        if ($ipInterface.InterfaceMetric -eq 6000) {
            Write-Host "  Already set to 6000; no change needed." -ForegroundColor Green
            continue
        }

        Set-NetIPInterface `
            -InterfaceIndex $adapter.ifIndex `
            -AddressFamily IPv4 `
            -InterfaceMetric 6000

        $newMetric = (Get-NetIPInterface `
            -InterfaceIndex $adapter.ifIndex `
            -AddressFamily IPv4).InterfaceMetric

        Write-Host "  New metric:     $newMetric" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "WSL/Cisco VPN workaround applied." -ForegroundColor Green
Write-Host "You can now retry your WSL network connection."