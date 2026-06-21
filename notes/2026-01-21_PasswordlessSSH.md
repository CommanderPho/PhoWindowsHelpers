```ps1
ssh-keygen -t ed25519


## Windows -> Windows
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | ssh pho@VM-Win10Updated.local "powershell -Command `"New-Item -Force -ItemType Directory -Path .ssh; `$input | Out-File -Append -Encoding ASCII .ssh\authorized_keys`""

## Windows -> Unix
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | ssh username@192.168.1.x "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

```

scp "$env:USERPROFILE\.ssh\id_ed25519.pub" pho@VM-Win10Updated.local:temp_key.pub

if (!(Test-Path .ssh)) { New-Item -ItemType Directory -Path .ssh }
Add-Content -Path .ssh\authorized_keys -Value (Get-Content temp_key.pub)
Remove-Item temp_key.pub

```