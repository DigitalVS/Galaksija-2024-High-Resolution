  include "galaksija.inc"

; High resolution subroutines
InitGraphics = $E055
Plot         = $E161
DrawLine     = $E104

IMAGE_LENGTH = 6656

    ORG $2C3A

; 1. Switch to graphics mode
; 2. Copy picture to the video memory
; 3. Wait for space key press and exit the program
Start:
    LD   A, 255           ; Set graphics mode indicator = 255
    LD   (TEXTHORPOS), A
    CALL InitGraphics     ; Initialize graphics mode if not already initialized

    LD   HL, (RAMTOP)
    LD   BC, 32
    ADD  HL, BC
    LD   DE, HL           ; Destination address
    ; Copy 6.656 bytes from Data to RAMTOP+32
    LD   HL, Data         ; Source address
    LD   BC, IMAGE_LENGTH ; Length
    LDIR                  ; Copy image to video memory

KeyWait:
    CALL ReadKey
    CP   ' '
    JR   NZ, KeyWait
    RET

Data:
    ds IMAGE_LENGTH, 0    ; Empty image space