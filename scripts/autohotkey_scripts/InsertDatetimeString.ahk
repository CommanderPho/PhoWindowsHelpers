; By PhoHale 2023-07-31
; Replaces my macOS BetterTouchTool expansion macros for Obsidian

#Requires AutoHotkey v2.0
Hotstring("EndChars", "`s`t") ; only expand after plain spaces or tabs

#HotIf WinActive("ahk_exe Obsidian.exe")
; only defined in Obsidian

:://timenow::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput "//" . FormatTime(, "yyyy-MM-dd h:mmt")  . ": "  ; It will look like 9/1/2005 53P
}

:://datenow::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput "//" . FormatTime(, "yyyy-MM-dd h:mmt")  . ": "  ; It will look like 9/1/2005 53P
}

:://now::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput "//" . FormatTime(, "h:mmt")  . ": " ; It will look like 9/1/2005 53P
}

::.now::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput FormatTime(, "h:mmt") . ": " ; It will look like 9/1/2005 3:53P
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




