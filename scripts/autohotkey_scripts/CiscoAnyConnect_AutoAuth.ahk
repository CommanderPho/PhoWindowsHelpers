#Requires AutoHotkey v2.0

; Cisco AnyConnect Secure Mobility Client
; ahk_class #32770
; ahk_exe vpnui.exe
; ahk_pid 15296
; ahk_id 1050078

; ClassNN:	Button1
; Text:	Connect
; Screen:	x: 975	y: 581	w: 98	h: 23
; Client	x: 289	y: 69	w: 98	h: 23

; # Spawns the password window

; Cisco AnyConnect | UMHS SSL VPN
; ahk_class #32770
; ahk_exe vpnui.exe
; ahk_pid 15296
; ahk_id 1314608

; ClassNN:	Edit1
; Text:	halechr

; ClassNN:	Edit2
; Text:	USERPASSWORD

; ClassNN:	Button1
; Text:	OK


; ; Set a flag to control the loop
; RunConnectScript := true

; while (RunConnectScript)
; {
; Wait for the "Cisco AnyConnect Secure Mobility Client" window to appear
WinWait("Cisco AnyConnect Secure Mobility Client")

; Activate the window
WinActivate

; Press the "Connect" button using ClassNN
ControlClick("Button1") ; D is for using the ClassNN    

; Wait for the password input field to appear
; Wait for the "Spawned Window Title" window to appear
WinWait("Cisco AnyConnect | UMHS SSL VPN")

; Activate the spawned window
WinActivate

; Wait for the password input field "Edit2" to appear
ControlFocus("Edit2") ; Replace "Edit2" with the actual ClassNN of the edit field

; Type the password (replace 'YourPassword' with the actual password)
Send("Flex-Follow22")

; Click the submit button
; ControlClick, SubmitButton ; Replace "SubmitButton" with the actual control ID or text of the submit button

; ; ; Click the submit button using ClassNN
; ControlClick("Button1") ; D is for using the ClassNN

; ; Set the flag to false to stop the loop
; RunConnectScript := false

; ; Wait for the connection to establish (adjust the sleep time as needed)
; Sleep(9000)

; }
