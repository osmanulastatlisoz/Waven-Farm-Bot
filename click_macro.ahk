#SingleInstance force

F8::
    Click
    return

F7::
    Click Down  ; Sol tıkı basılı tutar
    KeyWait, F7  ; F7 tuşu bırakılana kadar bekler
    Click Up  ; Sol tıkı bırakır
    return

F1::
    Send, {Esc down}  ; ESC tuşuna basılı tutar
    KeyWait, F1  ; F1 tuşu bırakılana kadar bekler
    Send, {Esc up}  ; ESC tuşunu bırakır
    return
