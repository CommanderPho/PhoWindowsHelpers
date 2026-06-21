param(
    [int]$LocalPort = 0,
    [switch]$AllGreatLakes
)

. "$PSScriptRoot\_supercomputer_VNC_tunnel_helpers.ps1"

if ($LocalPort -gt 0) {
    if (Stop-SshTunnelOnPort -LocalPort $LocalPort) {
        Write-Host "Stopped SSH tunnel on port $LocalPort."
    } else {
        Write-Host "No SSH tunnel listening on port $LocalPort."
    }
    exit 0
}

if ($AllGreatLakes) {
    $processes = Get-SshTunnelProcesses -AllGreatLakes
    if (-not $processes) {
        Write-Host "No Great Lakes SSH tunnels found."
        exit 0
    }
    foreach ($proc in $processes) {
        Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
        Write-Host "Stopped PID $($proc.ProcessId): $($proc.CommandLine)"
    }
    exit 0
}

$tunnels = Get-ActiveSshTunnels
if (-not $tunnels) {
    Write-Host "No active SSH tunnels found."
} else {
    $tunnels | Format-Table LocalPort, RemoteHost, RemotePort, ProcessId -AutoSize
}
