#Persistent
#SingleInstance Force

; Whenever the clipboard is changed, it displays the copied text as a tooltip for a short period.
; TODO: make tooltip transparent, make it only show the start/end of long multiline text


; ClipboardPrevious := ClipboardAll  ; Save the current clipboard content
ClipboardPrevious := Clipboard  ; Initialize the previous clipboard content as empty

; Monitor for clipboard changes
SetTimer, MonitorClipboard, 250
return

MonitorClipboard:
If (Clipboard != ClipboardPrevious) {
    ClipboardPrevious := Clipboard  ; Update the saved clipboard content
    if Clipboard {  ; Ensure clipboard contains text
        ToolTip, %Clipboard%  ; Show a tooltip with the current clipboard content
		; WinSet, Transparent, 200, ahk_class tooltips_class32  ; Set the transparency to 200 (range 0-255)
        SetTimer, HideToolTip, -1000  ; Hide the tooltip after 3 seconds
    }
}
return

HideToolTip:
ToolTip  ; Hide the tooltip
return