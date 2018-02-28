# Import argparse to handle the command line arguments
import argparse

# Declare global variables (defines)
COMMENT_CHAR = ";"                      # Character to specify comments
NOP_OPCODE = "00000000"                 # Opcode for NOP
LOAD_OPCODE = "10000000"                # Opcode for LOAD
OEN_OPCODE = "01000000"                 # Opcode for OEN
STORE_OPCODE = "00100000"               # Opcode for STORE
SUB_INST_LEN = 3                        # Length of Instruction with sub-op
INST_LEN = 2                            # Length of instruction sans sub-op
SUBOP_OFFSET = 3                        # Bit offset of sub-op field
NOT_SUBOP = "01"                        # Sub opcde for NOT
NAND_SUBOP = "10"                       # Sub opcode for NAND
NOR_SUBOP = "11"                        # Sub opcode for NOR
ADDR_BOUND = 7                          # Upper address bound
OPCODE_ERR = "No Opcode Present"        # Error if no opcode
SUBOP_ERR = "Invalid Sub Operation"     # Error if invalid sub-op
ARG_ERR = "Invalid Number of Arguments" # Error if invalid # of args
ADDR_ERR = "Invalid Address"            # Error if invalid address

# The assembler function. Takes a file object as input and returns list of opcodes if
# successful or an error string and line number in unsuccessful.
def assembler(inputFile):
    # Create empty opcode list
    opcodeList = []
    # Assembler loop
    for lineNum, line in enumerate(inputFile):
        line = line.strip()
        # If the line isn't a comment or whitespace then assemble it
        if not line == "" and not line.startswith(COMMENT_CHAR):
            # If a comment on non comment line then remove it and strip any whitespace
            if COMMENT_CHAR in line:
                line = line[0:line.index(COMMENT_CHAR)]
                line = line.strip()
            # Split each line of the input file into a list and assemble it then append
            # the result to opcodeList
            opcode = asminner(line.split(" "))
            # If asminner returned succesfully then append opcode, else set error
            if type(opcode) is int:
                opcodeList.append(opcode)
            else:
                opcodeList = [opcode, (lineNum + 1)]
                break
    # Return completed opcodeList
    return opcodeList

# Inner algorithm for assembler function. Takes list or arguments and either outputs
# the appropriate opcode or an error string
def asminner(lineList):
    # Determine the type of instruction then create appropriate opcode
    if lineList[0].upper() == "NOP":
        opcode = int(NOP_OPCODE, 2)
    elif lineList[0].upper() == "LOAD":
        opcode = int(LOAD_OPCODE, 2)
    elif lineList[0].upper() == "OEN":
        opcode = int(OEN_OPCODE, 2)
    elif lineList[0].upper() == "STORE":
        opcode = int(STORE_OPCODE, 2)
    # If no instruction present then set error
    else:
        opcode = OPCODE_ERR
    # If sub operation specified then OR it and the address onto opcode
    if len(lineList) == SUB_INST_LEN and type(opcode) is int:
        # Determine sub-op and OR it to opcode
        if lineList[1].upper() == "NOT":
            opcode = opcode | (int(NOT_SUBOP, 2) << SUBOP_OFFSET)
        elif lineList[1].upper() == "NAND":
            opcode = opcode | (int(NAND_SUBOP, 2) << SUBOP_OFFSET)
        elif lineList[1].upper() == "NOR":
            opcode = opcode | (int(NOR_SUBOP, 2) << SUBOP_OFFSET)
        # If invalid sub-op then set error
        else:
            opcode = SUBOP_ERR
        # OR address onto op code
        # Throw error if address not a number or out of bounds
        if type(opcode) is int and lineList[2].isdigit():
            if int(lineList[2]) <= ADDR_BOUND:
                opcode = opcode | int(lineList[2])
            else:
                opcode = ADDR_ERR
        elif type(opcode) is int and not lineList[2].isdigit():
            opcode = ADDR_ERR
    # If no sub operation specified then just OR address
    elif len(lineList) == INST_LEN and type(opcode) is int:
        # OR address onto opcode
        # Throw error if address not a number or out of bounds
        if type(opcode) is int and lineList[1].isdigit():
            if int(lineList[1]) <= ADDR_BOUND:
                opcode = opcode | int(lineList[1])
            else:
                opcode = ADDR_ERR
        elif type(opcode) is int and not lineList[1].isdigit():
            opcode = ADDR_ERR
    # If the next instruction is not a NOP instruction and has an invalid # of args
    # then set error.
    elif not lineList[0].upper() == "NOP" and type(opcode) is int:
        opcode = ARG_ERR
    # Return opcode for this loop
    return opcode

# Main Program
# Declares argparse instance and parses input and output file names
parser = argparse.ArgumentParser(description='Assembler for the Uno Computer')
parser.add_argument("input", help="Input file name")
parser.add_argument("-o","--output", help="Output file name, if unspecified output goes to stdout.")
arguments = parser.parse_args()

inputName = arguments.input
outputName = arguments.output

# Open the input file to read from
try:
    inputFile = open(inputName)
except Exception as message:
    print "Error,", message
    exit()

# Assemble input file to intermediate list and close it
opcodeList = assembler(inputFile)
inputFile.close()

# If error in assembler then print error, close file and return
if not type(opcodeList[0]) is int:
    print "Syntax Error on line " + str(opcodeList[1]) + ": " + opcodeList[0]
    exit()

# If oputput specified then open file for writing and write to it
if arguments.output:
    try:
        outputFile = open(outputName, 'w')
    except Exception as message:
        print "Error,", message
        exit()
    # Write header and then write human readable addreses and opcodes
    outputFile.write("Address:  Data:\n")
    for index, opcode in enumerate(opcodeList):
        outputFile.write(format(index, "08b") + "  " + format(opcode, "08b") + "\n")
    outputFile.close()
# If no output specified then print to stdout
else:
    # Print header and then print human readable addresses and opcodes
    print "Address:  Data:"
    for index, opcode in enumerate(opcodeList):
        print format(index, "08b") + "  " + format(opcode, "08b")

