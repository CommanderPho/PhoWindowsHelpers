; Allows zooming with [Ctrl] modifier
#IfWinActive, ahk_class illustrator
{
    ^WheelUp::!WheelUp ; Ctrl becomes Alt
    ^WheelDown::!WheelDown ; Ctrl becomes Alt
    !WheelUp::^WheelUp ; Alt becomes Ctrl
    !WheelDown::^WheelDown ; Alt becomes Ctrl
}
