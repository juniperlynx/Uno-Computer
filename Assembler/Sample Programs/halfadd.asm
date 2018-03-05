; This is a simple program that implements a half-adder.
; It takes inputs 0 & 1 as inputs and outputs the result to
; output 0 & 1. I/Os 2 & 3 are used as scratch bits and should 
; be jumpered

LOAD 0       ; Start of XOR gate
LOAD NAND 1
STORE NOT 1  ; While we're here store AND result for high bit output
STORE 2      ; Then resume XOR operation
LOAD NAND 0
STORE 3
LOAD 2
LOAD NAND 1
LOAD NAND 3
STORE 0     ; Store result of XOR

