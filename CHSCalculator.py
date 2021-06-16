import sys

try:
    sys.argv[1]
except IndexError:
    print("Enter Head, Sector & Cylinder")
    sys.exit()

Cylinder=sys.argv[3]
Head=sys.argv[1]
Sector=sys.argv[2]

def toBin(value):
    result = bin(int(value, 16))[2:].zfill(8) 
    return result

def toHex(value):
    result=hex(int(value, 2))
    return result

Sector=str(toBin(Sector))
Cylinder=str(toBin(Cylinder))
Head=str(toBin(Head))

Cylinder=Sector[:2]+Cylinder
Sector=Sector[2:]

Sector=str(toHex(Sector))
Cylinder=str(toHex(Cylinder))
Head=str(toHex(Head))

print("Cylinder: ", Cylinder, "Head: ", Head, "Sector: ", Sector )


