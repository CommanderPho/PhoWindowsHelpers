::btw::
{
    MsgBox 'You typed "btw".'
}

:*:]d::  ; This hotstring replaces "]d" with the current date and time via the functions below.
{
    SendInput FormatTime(, "M/d/yyyy h:mm tt")  ; It will look like 9/1/2005 3:53 PM
}