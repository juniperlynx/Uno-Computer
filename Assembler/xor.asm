; This is a simple program that performs the XOR function.
; It takes inputs 0 & 1 as inputs and outputs the result to
; output 0. I/Os 2 & 3 are used as scratch bits and should 
; be jumpered

; Based on the following circuit:
;                        ___
; INPUT 0 -+------------|   \
;          |   ___      |NAND)--+   ___
;          +--|   \   +-|___/   +--|   \
;             |NAND)--+  ___       |NAND)-- OUT
;          +--|___/   +-|   \   +--|___/
;          |            |NAND)--+
; INPUT 1 -+------------|___/

LOAD 0       ; First NAND
LOAD NAND 1
STORE 2
LOAD NAND 0 ; Lower NAND
STORE 3
LOAD 2      ; Upper NAND
LOAD NAND 1
LOAD NAND 3 ; Last NAND
STORE 0     ; Store result
