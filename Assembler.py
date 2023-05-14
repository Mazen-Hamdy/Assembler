def cal_bytes(mnemonic,operand):
    found=0
    NoOfBytes=-1
    if(mnemonic=="BYTE" or mnemonic=="WORD" or mnemonic=="RESB" or mnemonic=="RESW"):
        found=1
        if(mnemonic=="BYTE"):
            length = len(operand) - 3
            if(operand[0]=='X'):
                if(length%2==0):
                    NoOfBytes=length/2
                else:
                    NoOfBytes=(length/2)+1
            elif(operand[0]=='C'):
                NoOfBytes=length
        elif(mnemonic=="WORD"):
            NoOfBytes = 3
        elif(mnemonic=="RESB"):
            operand = int(operand)
            NoOfBytes = operand
        elif(mnemonic=="RESW"):
            operand=int(operand)
            NoOfBytes = operand*3
    if(found==0):
        opcode = open("OPCODE.txt","r")
        for opline in opcode:
            op = opline.split('\t')
            if(mnemonic==op[0]):
                found=1
                NoOfBytes=op[1]
                break
        opcode.close()
    if(found==0):
        NoOfBytes=-1
    NoOfBytes = int(NoOfBytes)
    return NoOfBytes
def NotExit(symbol):
    symfile=open("SYMTAB.txt","r")
    found=0
    for sline in symfile:
        line = sline
        line = line[:-1]
        spline = line.split('\t')
        if(spline[0]==symbol):
            found=1
            break
    symfile.close()
    if(found==1):
        return 0
    else:
        return 1
def retascii(char):
    Ascii=open("ASCII.txt","r")
    found=0
    for aline in Ascii:
        line=aline
        line=line[:-1] 
        linesp = line.split('\t')
        if(linesp[1]==str(char)):
            found=1
            asciicode=linesp[0]
            break
    Ascii.close()
    if(found==1):
        return asciicode
    else:
        return -1
def retOpcode(mnemonic):
	opcodeF = open("OPCODE.txt","r")
	found=0
	for opline in opcodeF:
			line = opline
			line = line[:-1]
			op = line.split('\t')
			if(mnemonic==op[0]):
				found=1
				opcode=op[2]
				break
	opcodeF.close()
	if(found==1):
		return opcode
	else:
		return -1
def retAddress(label):
    symFileR = open("SYMTAB.txt","r")
    found=0
    for aline in symFileR:
        line = aline
        line = line[:-1]
        spline=line.split('\t')
        if(spline[0]==label):
            found=1
            tAdd=spline[1]
            break
    symFileR.close()
    if(found==1):
        return tAdd
    else:
        return -1

filename=input("Enter the file's name: ")
ASMfile=open(filename,"r")
AddressCode=open("CodeplusAddress.txt","w+")
SYMfile=open("SYMTAB.txt","w+")

start = ASMfile.readline()
while(start[0]=='.'):
    start=ASMfile.readline()
start=start[:-1]
firstline=start.split('\t') 

Addf=firstline[2]
Add=int(Addf,16)
Add1=Addf


print("\n")
for iline in ASMfile:
    line = iline
    line = line[:-1]
    linesp = line.split('\t')

    if(line[0]!='.'):
        if(linesp[1]=="END"):
            break
        NoOfBytes = 0
        if(len(linesp)==3):
            NoOfBytes=cal_bytes(linesp[1],linesp[2])
        else:
            NoOfBytes=cal_bytes(linesp[1],0)
        if(NoOfBytes==-1):
            error= "Error: Invalid mnemonic " + linesp[1]
            print(error)
            input()
            exit(0)
        if(linesp[0]!=''):
            if(NotExit(linesp[0])):
                symbol = linesp[0] + "\t" + Add1
                SYMfile.write(symbol)
                SYMfile.write("\n")
                SYMfile.flush()
            else:
                error = "Error: " + linesp[0] +" - Multiple declaration"
                print(error)
                input()
                exit(0)
        writeline = Add1 + "\t" + line
        AddressCode.write(writeline)
        AddressCode.write("\n")
        AddressCode.flush()
        Add = Add + NoOfBytes
        Add1 = str(format(Add,'04X'))
SYMfile.close()
ASMfile.close()
AddressCode.close()


AddressCode1=open("CodeplusAddress.txt","r")
OBJcode=open("ObjectCodeFile.txt","w+")
obj=open("OBJCODE.o","w+")

AddressCode1.seek(0)

for aline in AddressCode1:
    line = aline
    line = line[:-1]
    linesp=line.split('\t')

    address = linesp[0]
    label = linesp[1]
    mnemonic = linesp[2]
    if(len(linesp)==4):
        operand = linesp[3]
    if(mnemonic!="RESB" and mnemonic!="RESW"):
        if(mnemonic=="BYTE"):
            arr = operand.split('\'')
            if(arr[0]=="X"):
                objline=arr[1]
            elif(arr[0]=="C"):
                chars=list(arr[1])
                objline = ""
                for char in chars:
                    asciicode = retascii(char)
                    if(asciicode==-1):
                        print("Error: Invalid character in BYTE")
                        input()
                        exit(0)
                    objline = objline + asciicode
        elif(mnemonic=="WORD"):
            operand = int(operand)
            objline = str(format(operand,'06X'))
        elif(mnemonic=="RSUB"):
            opcode = retOpcode(mnemonic)
            if(opcode==-1):
                print("Error: Opcode for RSUB could not be found")
                input()
                exit(0)
            objline = opcode + "0000"
        else:
            opcode = retOpcode(mnemonic)
            if(opcode==-1):
                error="Error: Opcode for " + mnemonic + " could not be found"
                print(error)
                input()
                exit(0)
            operandsp = operand.split(',')
            length=len(operandsp)
            targetadd = retAddress(operandsp[0])
            if(targetadd==-1):
                error="Error: Target address of " + operandsp[0] + " could not be found"
                print(error)
                input()
                exit(0)
            if(length==2 and operandsp[1]=="X"):
                string=targetadd
                part1 = string[:1]
                part2 = string[1:]
                part1 = int(part1)
                part1 = part1 + 8
                part1 = str(format(part1,'01X'))                
                targetadd = part1+part2
            objline = opcode + targetadd
        if(mnemonic=="RSUB"):
            writeline = line + "\t\t" + objline	
        else:
            writeline = line + "\t" + objline	
        OBJcode.write(writeline)				
        OBJcode.write("\n")
        obj.write(objline)						
        obj.write("\n")			
    else:
        OBJcode.write(line)
        OBJcode.write("\n")
		
		
AddressCode1.close()
OBJcode.close()
obj.close()

OBJcode = open("ObjectCodeFile.txt","r")

for aline in OBJcode:
	line = aline[:-1]
	print(line)