All network adapters didn't work after adjusting the VMWare Virtual network adapters.


```ps1
PowerShell 7.5.4
PS C:\Users\pho> Get-NetAdapter -Physical

Name                      InterfaceDescription                    ifIndex Status       MacAddress             LinkSpeed
----                      --------------------                    ------- ------       ----------             ---------
Ethernet                  Intel(R) Ethernet Controller (3) I225-V      17 Disconnected 50-EB-F6-57-1B-27       2.5 Gbps
Wi-Fi                     Intel(R) Wi-Fi 6 AX201 160MHz                 7 Up           70-A6-CC-B7-B9-16          0 bps

PS C:\Users\pho> netsh wlan show drivers
The Wireless AutoConfig Service (wlansvc) is not running.
PS C:\Users\pho> netsh wlan show interfaces
The Wireless AutoConfig Service (wlansvc) is not running.
PS C:\Users\pho> sc config wlansvc start= auto
[SC] ChangeServiceConfig SUCCESS
PS C:\Users\pho> net stop wlansvc
The WLAN AutoConfig service is not started.

More help is available by typing NET HELPMSG 3521.

PS C:\Users\pho> net start wlansvc
The WLAN AutoConfig service is starting.
The WLAN AutoConfig service was started successfully.

PS C:\Users\pho> netsh wlan show drivers
```