# Uno 1-bit Computer
This is an old project with incomplete documentation and is presented for reference and educational purposes only.

The Uno is a simple one bit computer loosely based on the instruction set of the Motorola MC14500B and has the following specifications:
  - Harvard Architecture
  - 256 bytes of program memory
  - 8 1-bit I/O ports
  - 500 Hz clock frequency
  - 1 clock cycle per instruction

The computer does not use a jump instruction. Instead of jumping, the machine continuously loops through the instruction memory, disabling and re-enabling output in different parts of the program.

You'll also notice that the spec list does not contain any data memory. However, it is possible to map a bit of memory to an I/O port by jumpering the input and output pins together.

A full explanation of the machine and its use can be found under Uno Description.txt, a simple assembler in python under Assembler, and the schematics for both the Uno and a simple I/O expander under Kicad Files.
