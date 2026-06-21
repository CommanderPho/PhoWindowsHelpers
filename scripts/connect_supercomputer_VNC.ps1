param(
    [Parameter(Mandatory = $true)]
    [string]$SshCommand,
    [Parameter(Mandatory = $true)]
    [int]$LocalPort,
    [Parameter(Mandatory = $true)]
    [string]$VncPassword,
    [string]$VncViewerPath = "${env:ProgramFiles}\RealVNC\VNC Viewer\vncviewer.exe"
)

. "$PSScriptRoot\_supercomputer_VNC_tunnel_helpers.ps1"

$sshPattern = 'ssh -f -N -L (?<LocalPort>\d+):(?<RemoteHost>[^:]+):(?<RemotePort>\d+) (?<User>[^@]+)@(?<Gateway>\S+)'

if ($SshCommand -notmatch $sshPattern) {
    Write-Error "Could not parse SSH command: $SshCommand"
    exit 1
}

$remoteHost = $Matches['RemoteHost']
$remotePort = $Matches['RemotePort']
$username = $Matches['User']
$gateway = $Matches['Gateway']

if ([int]$Matches['LocalPort'] -ne $LocalPort) {
    Write-Warning "LocalPort parameter ($LocalPort) differs from SSH command ($($Matches['LocalPort'])); using parameter value."
}

if (Stop-SshTunnelOnPort -LocalPort $LocalPort) {
    Write-Host "Stopped existing SSH tunnel on port $LocalPort."
}

Write-Host "Starting SSH tunnel on port $LocalPort -> ${remoteHost}:${remotePort} via ${username}@${gateway} ..."
Start-SshTunnelInteractive -SshCommand $SshCommand

if (-not (Wait-SshTunnelReady -LocalPort $LocalPort -TimeoutSeconds 10)) {
    Write-Error "SSH tunnel did not become ready on port $LocalPort after authentication. Auth may have succeeded but the tunnel failed to bind; retry or run manually in CMD: $SshCommand"
    exit 1
}

Write-Host "SSH tunnel is listening on port $LocalPort."

if (-not (Test-Path $VncViewerPath)) {
    Write-Error "RealVNC Viewer not found at '$VncViewerPath'. Install from https://www.realvnc.com/en/connect/download/viewer/"
    exit 1
}

Set-Clipboard -Value $VncPassword
Write-Host "VNC password copied to clipboard. Paste it when RealVNC prompts for authentication."
Write-Host "Launching RealVNC Viewer to localhost:$LocalPort ..."
Start-Process $VncViewerPath -ArgumentList "localhost:$LocalPort"

Write-Host "Done. SSH tunnel on port $LocalPort; VNC viewer launched."
