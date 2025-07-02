#Requires AutoHotkey v2.0

; This script will not exit automatically, even though it has nothing to do.
; However, you can use its tray icon to open the script in an editor, or to
; launch Window Spy or the Help file.
Persistent

; Frequencies for each modifier key
CtrlFreq := 500
AltFreq := 600
ShiftFreq := 700
WinFreq := 800

; Duration of the beep in milliseconds
BeepDuration := 200

; Function to play sound
PlaySound(frequency) {
    ; SoundBeep frequency, BeepDuration
	SoundPlay("C:\Windows\Media\chimes.wav")  ; This should play the 'Chimes' sound when the script is run
}

; Debug function to display messages
Debug(message) {
    ; MsgBox %message%
	; MsgBox "Result: " message

}

; testing
; PlaySound(CtrlFreq)
; PlaySound(AltFreq)
; PlaySound(ShiftFreq)
; PlaySound(WinFreq)

SoundPlay("C:\Windows\Media\chimes.wav")  ; This should play the 'Chimes' sound when the script is run
; SoundBeep
SoundPlay "*-1"
SoundPlay("C:\Windows\Media\chimes.wav")  ; This should play the 'Chimes' sound when the script is run

; ; Play sound when Ctrl is held down
; ~Ctrl::
; {
;     Debug("Ctrl key pressed")
;     PlaySound(CtrlFreq)
;     while GetKeyState("Ctrl", "P")
;         Sleep 10
;     Debug("Ctrl key released")
;     return
; }

; ; Play sound when Alt is held down
; ~Alt::
; {
;     Debug("Alt key pressed")
;     PlaySound(AltFreq)
;     while GetKeyState("Alt", "P")
;         Sleep 10
;     Debug("Alt key released")
;     return
; }

; ; Play sound when Shift is held down
; ~Shift::
; {
;     Debug("Shift key pressed")
;     PlaySound(ShiftFreq)
;     while GetKeyState("Shift", "P")
;         Sleep 10
;     Debug("Shift key released")
;     return
; }

; ; Play sound when Win key is held down
; ~LWin::
; ~RWin::
; {
;     Debug("Win key pressed")
;     PlaySound(WinFreq)
;     while GetKeyState("LWin", "P") || GetKeyState("RWin", "P")
;         Sleep 10
;     Debug("Win key released")
;     return
; }
