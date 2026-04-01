  include "galaksija.inc"

; High resolution subroutines
InitGraphics = $E055

IMAGE_LENGTH = 6656

    ORG $2C3A

; 1. Switch to graphics mode
; 2. Copy picture to the video memory
; 3. Wait for space key press and exit the program
Start:
    LD   A, 255           ; Set graphics mode indicator = 255
    LD   (TEXTHORPOS), A
    CALL InitGraphics     ; Initialize graphics mode if not already initialized

    ; Copy 6.656 bytes from Image to RAMTOP+32
    LD   HL, (RAMTOP)
    LD   BC, 32
    ADD  HL, BC
    LD   DE, HL           ; Destination address
    LD   HL, Image        ; Source address
    LD   BC, IMAGE_LENGTH ; Length
    LDIR                  ; Copy image to video memory

WaitKey:
    CALL ReadKey
    CP   ' '
    JR   NZ, WaitKey
    RET

Image:
    DS IMAGE_LENGTH, 0    ; Empty image space