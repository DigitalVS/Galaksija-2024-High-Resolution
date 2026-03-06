# Galaksija 2024 High Resolution

This is the high resolution expansion project for [Galaksija](https://en.wikipedia.org/wiki/Galaksija_(computer)) 2024 retro computer, which is in its original form limited to text (character) screen display. It is a hardware and software expansion of the Galaksija 2024 computer to achieve graphics resolution of 256 x 208 pixels. Software part of the project is mostly port of Galaksija Plus ROM C to newer Galaksija 2024 and it has high level of compatibility with Galaksija Plus.

This documentation is still __work in progress__!

## Hardware Description

Hardware of the High Resolution expansion is extremely simple. It consists of only one flip-flop which switches from character based mode to graphics mode and vice versa. This flip-flop extends Galaksija's, so called, *latch* circuit from six to seven bits and is handled exclusively by Galaksija's graphics raster generation service routine.

Output of the flip-flop is connected to the character's generator A12 line. This means that high resolution image goes through character generator EPROM, which is bit unusual, but is possible because this EPROM chip has greater then needed capacity and has all eight data bus lines connected to EPROM address lines. Each of the 256 possible data bus values addresses one EPROM cell where that same value has been stored. Thus, character generator is used to transfer any data bus value to the shift register connected to its output data lines.

Fact that high resolution image data goes through character generator means that character generator chip has to be replaced or reprogrammed before using new high resolution capabilities. Note that if reprogrammed, chip does not have to be erased before reprogramming - new contents can be reprogrammed with old contents left in the chip, because new contents is added while old is unchanged and will not be altered.

Folder *hardware* contains Gerber files, schematics, BOM list and character generator binary file needed for making high resolution expansion.

### Installation Procedure

The flip-flop is soldered to small PCB which plugs into the character generator socket (U4 on the Galaksija 2024 schematics) and character generator chip is then plugged to this PCB. Additionally, one of necessary signals, not available at character generator socket, has to be brought to the marked solder pad by short wire. This signal is CLK signal from neighboring 74HCT174 chip (U18, pin number 9).

ROM chip, usually labeled as *BASIC*, has to be changed or reprogrammed with new software as well.

## New ROM Software

Software consists of screen editor and eighteen BASIC commands. Syntax of the commands is the same as on Galaksija Plus. Screen editor itself and number of new commands are not related to high resolution functionality, and work in text mode as well. This makes this project more general then just adding high resolution features and it can be also called the __Galaksija 2024 Plus__ project though.

Source code is published in __plus.asm__ file. This file is supposed to be assembled together with the rest of the sources for Galaksija 2024, but these other files are not published here. Only resulting binary ROM file is published in release section of this repository.

After the Galaksija's startup, computer is booted in its main text mode and, therefore, high resolution and other new capabilities are not yet available. New features are available only after the initialization with command `A=USR(&E000)`.

### Screen Editor

Screen editor is the same Galaksija Plus editor with few small fixes. It works only in overwrite mode, which is unusual by modern standards, but expected considering how few keys the keyboard has (e.g. no backspace nor control keys).

Characters in front of the cursor are deleting with DEL key, and space for new characters are creating with SHIFT + "-" key combination.

### BASIC Commands

New BASIC commands, including unofficial command R2, are: GRAPH, TEXT, DRAW, UNDRAW, PLOT, UNPLOT, FILL, SOUND, LINE, FAST, SLOW, CLEAR, KILL, DESTROY, AUTO, UP, DOWN, R2.

Graphics commands work with graphics coordinates, where (0,0) point is in lower-left corner, and (255,207) is in upper-right corner. The coordinate value is kept within visible area by calculating value further by modulo 256. Vertical coordinate values from 208 to 255 are equal to value 0. Vertical resolution is adjustable from 49 to 208 lines with LINE command.

Graphics mode allocates 6.5 kilobytes for video memory, together with additional 32 bytes for its internal variables. This memory is initially allocated at the top of the RAM, but can be relocated elsewhere.

Graphics mode uses its own character set which may be redefined.

#### GRAPH and TEXT

`GRAPH` command switches Galaksija to graphics mode and `TEXT` switches back to text mode.

#### PLOT and UNPLOT

`PLOT x,y` turns-on point at coordinates x,y, and `UNPLOT x,y` turns-off point at coordinates x,y. Both commands set new current point location at coordinates x,y.

#### DRAW and UNDRAW

`DRAW x,y` draws a strait line from current point location to the new point location at coordinates x,y. `UNDRAW x,y` turns-off points on a strait line from current point location to the new point location at coordinates x,y.

#### FILL

Command `FILL x,y` fills with white color shape enclosed around point x,y. This is equivalent to use of *paint bucket* option in modern drawing tools.

#### SOUND

This command generates sound by manipulating register values of sound generator chip, like Yamaha YM2149 and other compatible models. Command syntax is `SOUND register,value` where *register* is YM2149 register number from 0 to 15 and *value* is value from 0 to 255 to be written to the target register. In case that [sound generator](https://github.com/DigitalVS/Galaksija-Resources/blob/main/README.md#g2024-ym2149-sound-generator) is not available, this command has no effect.

#### LINE

`LINE n` command sets new vertical resolution value. Acceptable value is from 49 to 208. Sometimes setting lower then maximum value is useful, at least for short period of time, because it leaves more CPU cycles to application software and thus improves speed.

#### FAST and SLOW

`FAST` command will switch Galaksija to fast mode of operation when picture is not generated and `SLOW` command will revert this to normal mode of operation with visible picture on the screen.

#### CLEAR

Initial value of all numeric variables is 0.5. The `CLEAR` command will set all numeric variables value to true zero.

#### KILL and DESTROY

Command `KILL` will reinitialize the computer, the same way as command `PRINT USR(0)`. Before reinitialization it will ask for confirmation.

Command `DESTROY n,m` will clear the memory from address *n* to address *m*, setting all byte values to zero.

#### AUTO

`AUTO n,m` will automatically generate BASIC program numbers starting from number *n* with step *m*. If autogenerated program line already exists, warning will be displayed. With pressing the ENTER key, existing line will stay in memory, otherwise it will be rewritten with new typed contents.

#### UP and DOWN

`UP n` command will move BASIC program up for *n* bytes. `DOWN n` command will move BASIC program *n* bytes down.

#### R2

This is unofficial command which de-initializes high resolution mode and all other Plus features and puts Galaksija in its main text mode of operation. Basically its effect is the same as a computer reset, except that RAM contents is preserved.

## Troubleshooting

There is a well known issue with Galaksija 2024 picture which is even more visible in graphics mode in which this expansion works.

This issue is manifested in text mode as ghost pixels for characters wider then 6 pixels. For example, two asterisk characters placed by each other are displayed as joined in the middle, even there should be one pixel wide gap between them. In graphics mode this is much more obvious, and seen as, at every eight pixels, first column displayed twice and eighth column not displayed at all.

Fortunately, solution is simple by soldering small ceramic capacitor with capacitance of 470 pF between pin 9 and ground (pin 7) of chip 74HCT74 (U18) on Galaksija 2024 main PCB. It is easiest to solder it underneath of the 74HCT74 on the other side of the board. If you wish, you can first try smaller capacitor values if they fix the problem, for example, 330 or 390 pF, because required value can slightly vary with manufacturer of ICs used on each single Galaksija.

The MIT License (MIT)

Copyright (c) 2026 Vitomir Spasojević (<https://github.com/DigitalVS/Galaksija-2024-High-Resolution>). All rights reserved.