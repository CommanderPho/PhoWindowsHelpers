# --- UAC BYPASS SHORTCUT CREATOR ---
# This script creates a desktop shortcut that runs applications with administrator privileges
# without showing the UAC prompt each time.

# 1. --- PARAMETERS ---
param(
    [string]$ProgramPath,
    [string]$Arguments,
    [string]$TaskName,
    [string]$ShortcutName,
    [ValidateSet("Desktop","StartMenu","Custom")]
    [string]$ShortcutLocation = "Desktop",
    [string]$CustomShortcutDirectory,
    [string]$WorkingDirectory,
    [switch]$Hidden,
    [switch]$Force,
    [switch]$Test,
    [switch]$NoPause
)

# 2. --- CONFIGURATION ---
$TaskNamePrefix = "BypassUAC"
$ScriptVersion = "1.2"

# 3. --- FUNCTIONS ---
function Write-ColoredText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Test-Administrator {
    return ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Invoke-PauseIfInteractive {
    param([string]$Prompt = "Press Enter to continue")
    if (-not $NoPause) {
        Read-Host $Prompt | Out-Null
    }
}

function Get-ShortHash {
    param([string]$Text)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Text)
        $hash = $sha.ComputeHash($bytes)
        return ([BitConverter]::ToString($hash)).Replace("-", "").Substring(0, 8)
    }
    finally {
        $sha.Dispose()
    }
}

function Get-SafeTaskName {
    param(
        [string]$ProgramName,
        [string]$PathForHash
    )
    # Remove invalid characters for task names
    $SafeName = $ProgramName -replace '[<>:"/\\|?*]', '_'
    if ($PathForHash) {
        $hash = Get-ShortHash -Text $PathForHash
        $SafeName = "$TaskNamePrefix-$SafeName-$hash"
    }
    else {
        $SafeName = "$TaskNamePrefix-$SafeName"
    }
    # Task name length practical limit ~238 chars
    if ($SafeName.Length -gt 238) { $SafeName = $SafeName.Substring(0, 238) }
    return $SafeName
}

# Registry helpers for created tasks
function Get-ScriptDirectory {
    if ($PSScriptRoot) { return $PSScriptRoot }
    return (Split-Path -Parent $MyInvocation.MyCommand.Path)
}

function Get-RegistryPath {
    $dir = Get-ScriptDirectory
    return (Join-Path $dir "created tasks.json")
}

function Get-TaskRegistry {
    $path = Get-RegistryPath
    if (-not (Test-Path -LiteralPath $path)) { return @() }
    try {
        $raw = Get-Content -LiteralPath $path -Raw -ErrorAction Stop
        if ([string]::IsNullOrWhiteSpace($raw)) { return @() }
        $data = $raw | ConvertFrom-Json -ErrorAction Stop
        if ($data -is [System.Array]) { return ,@($data) }
        return ,@($data)
    }
    catch { return @() }
}

function Set-TaskRegistry {
    param([Parameter(Mandatory=$true)] $Items)
    $path = Get-RegistryPath
    try {
        ($Items | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $path -Encoding UTF8
        return $true
    }
    catch { return $false }
}

function Update-TaskRegistryEntry {
    param([Parameter(Mandatory=$true)] $Entry)
    $items = Get-TaskRegistry
    # remove any existing by TaskName
    $items = @($items | Where-Object { $_.TaskName -ne $Entry.TaskName })
    $items += $Entry
    [void](Set-TaskRegistry -Items $items)
}

# 4. --- SCRIPT HEADER ---
Clear-Host
Write-ColoredText "═══════════════════════════════════════════════════════════" "Cyan"
Write-ColoredText "    UAC BYPASS SHORTCUT CREATOR v$ScriptVersion" "Cyan"
Write-ColoredText "═══════════════════════════════════════════════════════════" "Cyan"
Write-ColoredText ""
Write-ColoredText "This script will:" "Yellow"
Write-ColoredText "  1. Create a scheduled task to run your program as admin" "White"
Write-ColoredText "  2. Create a shortcut (Desktop/Start Menu/Custom) that bypasses UAC prompts" "White"
Write-ColoredText ""

# 5. --- ADMINISTRATIVE CHECK ---
if (-NOT (Test-Administrator)) {
    Write-ColoredText "⚠️  ADMINISTRATOR PRIVILEGES REQUIRED" "Red"
    Write-ColoredText ""
    Write-ColoredText "This script must be run as Administrator to create scheduled tasks." "Yellow"
    Write-ColoredText "Please:" "Yellow"
    Write-ColoredText "  1. Right-click this script file" "White"
    Write-ColoredText "  2. Select 'Run as Administrator'" "White"
    Write-ColoredText "  3. Click 'Yes' when prompted by UAC" "White"
    Write-ColoredText ""
    Invoke-PauseIfInteractive "Press Enter to exit"
    exit 1
}

Write-ColoredText "✅ Running with Administrator privileges" "Green"
Write-ColoredText ""

# 6. --- LOAD REQUIRED ASSEMBLIES ---
try {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
}
catch {
    Write-ColoredText "❌ Failed to load required Windows Forms assemblies: $_" "Red"
    Invoke-PauseIfInteractive "Press Enter to exit"
    exit 1
}

# 7. --- FILE SELECTION ---
if (-not $PSBoundParameters.ContainsKey('ProgramPath')) {
    Write-ColoredText "📁 Please select a file to run elevated (exe, bat, cmd, ps1, lnk)..." "Yellow"
    Write-ColoredText ""
    $FileBrowser = New-Object System.Windows.Forms.OpenFileDialog
    $FileBrowser.Filter = "Programs/Shortcuts (*.exe;*.bat;*.cmd;*.ps1;*.lnk)|*.exe;*.bat;*.cmd;*.ps1;*.lnk|All Files (*.*)|*.*"
    $FileBrowser.Title = "Select the program's executable or script"
    $FileBrowser.InitialDirectory = [Environment]::GetFolderPath("ProgramFiles")
    $DialogResult = $FileBrowser.ShowDialog()
    if ($DialogResult -ne [System.Windows.Forms.DialogResult]::OK) {
        Write-ColoredText "❌ No file selected. Operation cancelled." "Red"
        Invoke-PauseIfInteractive "Press Enter to exit"
        exit 1
    }
    $ProgramPath = $FileBrowser.FileName
}

# Validate and normalize the selected file
try {
    $ProgramPath = (Resolve-Path -Path $ProgramPath -ErrorAction Stop).Path
}
catch {
    Write-ColoredText "❌ Selected file does not exist: $ProgramPath" "Red"
    Invoke-PauseIfInteractive "Press Enter to exit"
    exit 1
}

# If a .lnk file was provided, resolve it to the real target
if ([System.IO.Path]::GetExtension($ProgramPath).ToLowerInvariant() -eq '.lnk') {
    try {
        $ws = New-Object -ComObject WScript.Shell
        $lnk = $ws.CreateShortcut($ProgramPath)
        $resolvedTarget = $lnk.TargetPath
        $resolvedArgs = $lnk.Arguments
        $resolvedWorkDir = $lnk.WorkingDirectory

        if (-not (Test-Path -LiteralPath $resolvedTarget)) {
            throw "Shortcut target does not exist: $resolvedTarget"
        }

        $ProgramPath = $resolvedTarget
        if (-not $PSBoundParameters.ContainsKey('Arguments') -and -not [string]::IsNullOrWhiteSpace($resolvedArgs)) {
            $Arguments = $resolvedArgs
        }
        if (-not $PSBoundParameters.ContainsKey('WorkingDirectory') -and -not [string]::IsNullOrWhiteSpace($resolvedWorkDir)) {
            $WorkingDirectory = $resolvedWorkDir
        }
    }
    catch {
        Write-ColoredText "❌ Failed to resolve shortcut: $_" "Red"
        Invoke-PauseIfInteractive "Press Enter to exit"
        exit 1
    }
}

$ProgramName = [System.IO.Path]::GetFileNameWithoutExtension($ProgramPath)
if ([string]::IsNullOrWhiteSpace($TaskName)) {
    $TaskName = Get-SafeTaskName -ProgramName $ProgramName -PathForHash $ProgramPath
}
else {
    $TaskName = Get-SafeTaskName -ProgramName $TaskName
}

# Optional arguments and working directory
# If a .lnk was provided, its arguments were already copied earlier.
# Otherwise, if not provided, assume none (no prompt).
$ProgramArgs = $Arguments
if (-not $PSBoundParameters.ContainsKey('Arguments') -and [string]::IsNullOrWhiteSpace($ProgramArgs)) {
    $ProgramArgs = ""
}
if (-not $PSBoundParameters.ContainsKey('WorkingDirectory') -or [string]::IsNullOrWhiteSpace($WorkingDirectory)) {
    $WorkingDirectory = [System.IO.Path]::GetDirectoryName($ProgramPath)
}

# Basic safety warnings
try {
    if ($ProgramPath -match '^[\\/]{2}') {
        Write-ColoredText "⚠️  Selected path is a network (UNC) location. This is not recommended for elevated tasks." "Yellow"
    }
    $zoneInfo = Get-Item -Path $ProgramPath -Stream Zone.Identifier -ErrorAction SilentlyContinue
    if ($zoneInfo) {
        Write-ColoredText "⚠️  File appears downloaded from the internet (Zone.Identifier present). Consider 'Unblock-File' if trusted." "Yellow"
    }
}
catch {}

Write-ColoredText "✅ Program selected: $ProgramPath" "Green"
Write-ColoredText "📋 Task name will be: $TaskName" "Cyan"
Write-ColoredText ""

# 8. --- CREATE THE SCHEDULED TASK ---
Write-ColoredText "🔧 Creating scheduled task..." "Yellow"

# Ensure Task Scheduler service is running
try {
    $schedSvc = Get-Service -Name Schedule -ErrorAction Stop
    if ($schedSvc.Status -ne 'Running') {
        Start-Service -Name Schedule
    }
}
catch {
    Write-ColoredText "❌ Task Scheduler service not available: $_" "Red"
    Invoke-PauseIfInteractive "Press Enter to exit"
    exit 1
}

try {
    # Check if task already exists and optionally remove it
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        if (-not $Force) {
            Write-ColoredText "⚠️  Task '$TaskName' already exists." "Yellow"
            $overwrite = Read-Host "Replace existing task? (Y/n)"
            if ($overwrite -match '^[Nn]') { throw "User cancelled to avoid overwriting existing task." }
        }
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Determine how to run based on file type
    $execPath = $ProgramPath
    $argLine = $ProgramArgs
    $ext = [System.IO.Path]::GetExtension($ProgramPath).ToLowerInvariant()
    switch ($ext) {
        '.ps1' {
            $execPath = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
            $argLine = "-NoProfile -ExecutionPolicy Bypass -File `"$ProgramPath`" $ProgramArgs"
        }
        '.bat' { $execPath = Join-Path $env:WINDIR 'System32\cmd.exe'; $argLine = "/c `"$ProgramPath`" $ProgramArgs" }
        '.cmd' { $execPath = Join-Path $env:WINDIR 'System32\cmd.exe'; $argLine = "/c `"$ProgramPath`" $ProgramArgs" }
        default { }
    }

    # Action: What program to run?
    if ([string]::IsNullOrWhiteSpace($argLine)) {
        $taskAction = New-ScheduledTaskAction -Execute $execPath -WorkingDirectory $WorkingDirectory
    } else {
        $taskAction = New-ScheduledTaskAction -Execute $execPath -Argument $argLine -WorkingDirectory $WorkingDirectory
    }

    # Principal: Run with highest privileges as current user
    $CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    $taskPrincipal = New-ScheduledTaskPrincipal -UserId $CurrentUser -RunLevel Highest -LogonType Interactive

    # Settings: Configure task behavior
    $useHidden = $true
    if ($PSBoundParameters.ContainsKey('Hidden')) { $useHidden = [bool]$Hidden }
    $settingsParams = @{ AllowStartIfOnBatteries = $true; DontStopIfGoingOnBatteries = $true; ExecutionTimeLimit = [TimeSpan]::Zero }
    if ($useHidden) { $settingsParams.Hidden = $true }
    $taskSettings = New-ScheduledTaskSettingsSet @settingsParams

    # Register the Task
    Register-ScheduledTask -TaskName $TaskName -Action $taskAction -Principal $taskPrincipal -Settings $taskSettings -Force | Out-Null
    
    Write-ColoredText "✅ Successfully created scheduled task" "Green"
}
catch {
    Write-ColoredText "❌ Failed to create scheduled task: $_" "Red"
    Write-ColoredText ""
    Write-ColoredText "Common causes:" "Yellow"
    Write-ColoredText "  • Insufficient permissions" "White"
    Write-ColoredText "  • Task Scheduler service not running" "White"
    Write-ColoredText "  • Invalid characters in program path" "White"
    Pause-IfInteractive "Press Enter to exit"
    exit 1
}

# 9. --- CREATE THE DESKTOP SHORTCUT ---
Write-ColoredText "🔗 Creating desktop shortcut..." "Yellow"

try {
    $WshShell = New-Object -ComObject WScript.Shell
    $ShortcutPath = $null

    # Determine shortcut directory
    switch ($ShortcutLocation) {
        'Desktop'   { $shortcutDir = [Environment]::GetFolderPath('Desktop') }
        'StartMenu' { $shortcutDir = Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs' }
        'Custom'    {
            if (-not $CustomShortcutDirectory) { throw "CustomShortcutDirectory is required when ShortcutLocation is 'Custom'." }
            $shortcutDir = $CustomShortcutDirectory
        }
    }

    # Ensure directory exists
    if (-not (Test-Path -LiteralPath $shortcutDir)) {
        New-Item -ItemType Directory -Path $shortcutDir -Force | Out-Null
    }

    # Shortcut name
    if ([string]::IsNullOrWhiteSpace($ShortcutName)) { $ShortcutName = "$ProgramName (Admin - No UAC)" }
    $ShortcutPath = Join-Path $shortcutDir ("$ShortcutName.lnk")

    # Remove existing shortcut if it exists
    if (Test-Path -LiteralPath $ShortcutPath) {
        Remove-Item -LiteralPath $ShortcutPath -Force
        Write-ColoredText "⚠️  Replaced existing shortcut" "Yellow"
    }

    # Create the shortcut object
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)

    # Configure the shortcut to run the scheduled task
    $Shortcut.TargetPath = "schtasks.exe"
    $Shortcut.Arguments = "/run /tn `"$TaskName`""
    $Shortcut.WorkingDirectory = $WorkingDirectory
    $Shortcut.Description = "Run $ProgramName as Administrator without UAC prompt"

    # Set the icon to match the original program; fallback to shell
    if (Test-Path -LiteralPath $ProgramPath) {
        $Shortcut.IconLocation = "$ProgramPath,0"
    } else {
        $Shortcut.IconLocation = (Join-Path $env:WINDIR 'System32\\imageres.dll') + ",2"
    }

    # Save the shortcut
    $Shortcut.Save()

    Write-ColoredText "✅ Successfully created shortcut: $ShortcutName.lnk" "Green"
}
catch {
    Write-ColoredText "❌ Failed to create shortcut: $_" "Red"
    Write-ColoredText "The scheduled task was created successfully, but the shortcut creation failed." "Yellow"
}

# 9.5 --- RECORD REGISTRY ENTRY ---
try {
    $entry = [ordered]@{
        TaskName          = $TaskName
        ProgramPath       = $ProgramPath
        Arguments         = $ProgramArgs
        WorkingDirectory  = $WorkingDirectory
        ExecPath          = $execPath
        ExecArguments     = $argLine
        ShortcutLocation  = $ShortcutLocation
        ShortcutName      = $ShortcutName
        ShortcutPath      = $ShortcutPath
        CreatedBy         = $env:USERNAME
        CreatedAtUtc      = [DateTime]::UtcNow.ToString("o")
    }
    Update-TaskRegistryEntry -Entry $entry
}
catch {
    Write-ColoredText "⚠️  Failed to update registry file: $(Get-RegistryPath)" "Yellow"
}

# 10. --- COMPLETION SUMMARY ---
Write-ColoredText ""
Write-ColoredText "═══════════════════════════════════════════════════════════" "Cyan"
Write-ColoredText "    SETUP COMPLETE!" "Green"
Write-ColoredText "═══════════════════════════════════════════════════════════" "Cyan"
Write-ColoredText ""
Write-ColoredText "What was created:" "Yellow"
Write-ColoredText "  ✅ Scheduled Task: $TaskName" "Green"
Write-ColoredText "  ✅ Shortcut: $ShortcutName.lnk" "Green"
Write-ColoredText ""
Write-ColoredText "How to use:" "Yellow"
Write-ColoredText "  • Double-click the desktop shortcut to run $ProgramName" "White"
Write-ColoredText "  • The program will start with admin privileges" "White"
Write-ColoredText "  • No UAC prompt will appear!" "White"
Write-ColoredText ""
Write-ColoredText "To remove:" "Yellow"
Write-ColoredText "  • Delete the shortcut" "White"
Write-ColoredText "  • Run: schtasks /delete /tn `"$TaskName`" /f" "White"
Write-ColoredText ""

# Test the shortcut
$shouldTest = $false
if ($Test) { $shouldTest = $true }
else {
    $TestChoice = Read-Host "Would you like to test the shortcut now? (y/N)"
    if ($TestChoice -match '^[Yy]') { $shouldTest = $true }
}
if ($shouldTest) {
    Write-ColoredText ""
    Write-ColoredText "🚀 Testing shortcut..." "Yellow"
    try {
        Start-ScheduledTask -TaskName $TaskName
        Write-ColoredText "✅ Test completed! Check if $ProgramName started." "Green"
    }
    catch {
        Write-ColoredText "❌ Test failed: $_" "Red"
    }
}

Write-ColoredText ""
Invoke-PauseIfInteractive "Press Enter to exit"

# --- END OF SCRIPT ---
