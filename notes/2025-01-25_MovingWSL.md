# Moving WSL Storage Location:
https://blog.codetitans.pl/post/howto-docker-over-wsl2-location/

 wsl --export docker-desktop-data "E:\SlowSwap\Docker\wsl\data\docker-desktop-data.tar"

## List WSL Storages: `wsl --list -v`

wsl  --shutdown
wsl --export Ubuntu "E:\SlowSwap\Docker\wsl\data\Ubuntu.tar"
wsl --unregister Ubuntu
wsl --import Ubuntu "E:\SlowSwap\Docker\wsl\data" "E:\SlowSwap\Docker\wsl\data\Ubuntu.tar" --version 2


## Moving Docker:
sudo rsync -aqxP /var/lib/docker/ /volumes/red/docker



## 2025-01-28 - Apogee WSL Setup `"F:\FastSwap\ProgramData\Docker\wsl\data"`
```

wsl --export Ubuntu --vhd "F:\FastSwap\ProgramData\Docker\wsl\data\Ubuntu.vhdx"
wsl --export Ubuntu "F:\FastSwap\ProgramData\Docker\wsl\data\Ubuntu.tar"
wsl --unregister Ubuntu
wsl --import Ubuntu "F:\FastSwap\ProgramData\Docker\wsl\data" "F:\FastSwap\ProgramData\Docker\wsl\data\Ubuntu.tar" --version 2



# wsl --export Debian "F:\FastSwap\ProgramData\Docker\wsl\data\Debian.tar" 

wsl --export Debian --vhd "F:\FastSwap\ProgramData\Docker\wsl\data\Debian.vhdx" ## do VHDX which is easier and can import in-place
wsl --unregister Debian
wsl --import Debian "F:\FastSwap\ProgramData\Docker\wsl\data" "F:\FastSwap\ProgramData\Docker\wsl\data\Debian.tar" --version 2


wsl --manage Debian --move "F:\FastSwap\ProgramData\Docker\wsl\data"
 --manage <Distro> <Options...>
        Changes distro specific options.

        Options:
            --move <Location>




```