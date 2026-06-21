function Get-SshTunnelProcesses {
    param([switch]$AllGreatLakes)

    $processes = @(Get-CimInstance Win32_Process -Filter "Name='ssh.exe'" -ErrorAction SilentlyContinue)
    $filtered = $processes | Where-Object { $_.CommandLine -match '-L\s+\d+:' }
    if ($AllGreatLakes) {
        $filtered = $filtered | Where-Object { $_.CommandLine -match '-L\s+\d+:[^:\s]+\.arc-ts\.umich\.edu:\d+' }
    }
    return @($filtered)
}


function Get-ActiveSshTunnels {
    $tunnels = @()
    foreach ($proc in (Get-SshTunnelProcesses)) {
        if ($proc.CommandLine -match '-L\s+(?<LocalPort>\d+):(?<RemoteHost>[^:]+):(?<RemotePort>\d+)') {
            $tunnels += [PSCustomObject]@{
                LocalPort = [int]$Matches['LocalPort']
                RemoteHost = $Matches['RemoteHost']
                RemotePort = [int]$Matches['RemotePort']
                ProcessId = $proc.ProcessId
                CommandLine = $proc.CommandLine
            }
        }
    }
    return $tunnels
}


function Stop-SshTunnelOnPort {
    param([int]$LocalPort)

    $connections = @(Get-NetTCPConnection -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue)
    if (-not $connections) { return $false }
    foreach ($conn in $connections) {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 1
    return $true
}


function Start-SshTunnelInteractive {
    param([string]$SshCommand)

    Write-Host ""
    Write-Host "=== SSH login required ==="
    Write-Host "Enter your password, then complete Okta 2FA (push/passcode + number challenge)."
    Write-Host "Command: $SshCommand"
    Write-Host ""
    & cmd.exe /c $SshCommand
    if ($LASTEXITCODE -ne 0) {
        Write-Error "SSH tunnel failed (exit code $LASTEXITCODE). Check credentials/VPN and retry."
        exit 1
    }
}


function Start-SshTunnelViaCmd {
    param([string]$SshCommand, [switch]$ShowWindow)

    $tunnelScript = Join-Path $PSScriptRoot "start_supercomputer_ssh_tunnel.cmd"
    if (-not (Test-Path $tunnelScript)) {
        Write-Error "SSH tunnel CMD script not found: $tunnelScript"
        exit 1
    }
    if ($ShowWindow) {
        Start-Process -FilePath $tunnelScript -ArgumentList @("--normal", $SshCommand)
    } else {
        Start-Process -FilePath $tunnelScript -ArgumentList @($SshCommand)
    }
}

function Wait-SshTunnelReady {
    param([int]$LocalPort, [int]$TimeoutSeconds = 15)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $connection = Get-NetTCPConnection -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue
        if ($connection) { return $true }
        Start-Sleep -Milliseconds 500
    }
    return $false
}
