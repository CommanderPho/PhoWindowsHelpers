# 1. Store the raw text block from your session
$text = @"
Download any VNC viewer, RealVNC is a good option.
Copy/paste in your terminal to establish the SSH tunnel:

ssh -f -N -L 22587:gl3039.arc-ts.umich.edu:5901 halechr@greatlakes.arc-ts.umich.edu
For terminals in Windows you can use: Powershell, PuTTy and Windows Subsystem Linux distributions

Open a VNC client and connect to localhost:22587 within the client
Use the VNC password: rD35cTzZ
"@

# 2. Define regex patterns to capture the specific variables
$sshPattern = "ssh -f -N -L (?<LocalPort>\d+):(?<RemoteHost>[^:]+):(?<RemotePort>\d+) (?<User>[^@]+)@(?<Gateway>[^\s]+)"
$passPattern = "Use the VNC password:\s*(?<Password>\S+)"

# 3. Match and extract the details
if ($text -match $sshPattern) {
    $connectionInfo = [PSCustomObject]@{
        LocalPort  = $Matches['LocalPort']
        RemoteHost = $Matches['RemoteHost']
        RemotePort = $Matches['RemotePort']
        Username   = $Matches['User']
        Gateway    = $Matches['Gateway']
        VNCPassword = ""
    }

    if ($text -match $passPattern) {
        $connectionInfo.VNCPassword = $Matches['Password']
    }

    # 4. Output the extracted data cleanly
    $connectionInfo | Format-List
} else {
    Write-Warning "Could not parse connection information."
}