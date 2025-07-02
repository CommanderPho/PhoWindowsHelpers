; ________________________________________
;
; WINDOWS + V
; Swap clipboard and selection
#IfWinActive ahk_class Chrome_WidgetWin_1 && ahk_exe Code.exe
; ^b::
; #v::


; save clipboard content to paste later
pastebackup = %clipboard%
ClipWait, 0.05, 1
 
; get selected text
clipboard =
ClipWait, 0.05, 1
Send ^c
ClipWait, 0.05, 1
 
; save selected text to put in clipboard later
clipboardbackup = %clipboard%
ClipWait, 0.05, 1
 
; add paster content to clipboard
clipboard = %pastebackup%
ClipWait, 0.05, 1
 
; paste
Send ^v
 
; add original selection to clipboard
clipboard = %clipboardbackup%
ClipWait, 0.05, 1
 
return
