; By PhoHale 2023-07-31
; Replaces my macOS BetterTouchTool expansion macros for Obsidian

#Requires AutoHotkey v2.0
Hotstring("EndChars", "`s`t") ; only expand after plain spaces or tabs

#HotIf WinActive("ahk_exe Obsidian.exe")
; only defined in Obsidian

:://datenow::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput "//" . FormatTime(, "yyyy-M-d h:mm tt")  . ": "  ; It will look like 9/1/2005 3:53 PM
}

:://now::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput "//" . FormatTime(, "h:mm tt")  . ": " ; It will look like 9/1/2005 3:53 PM
}

::.now::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput FormatTime(, "h:mm tt") . ": " ; It will look like 9/1/2005 3:53 PM
}

#HotIf


; CurrentDateTime := FormatTime("yyyy-MM-dd_HH:mm:ss")
; if (A_Hour < 12)
;     CurrentDateTime .= "a"
; else
;     CurrentDateTime .= "p"

; ; MsgBox(CurrentDateTime)
; ; Send % CurrentDateTime
; ^1::SendText "//" . CurrentDateTime . ":"




