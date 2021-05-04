import string
import argparse
from math import gcd

charFrequency = [0.08, 0.02, 0.03, 0.04, 0.13, 0.02, 0.02, 0.06, 0.07, 0.0, 0.01, 0.04, 0.02, 0.07, 0.08, 0.02, 0.0, 0.06, 0.06, 0.09, 0.03, 0.01, 0.02, 0.0, 0.02, 0.0]
tripleCharSet=set()
tripleCharDic={}
topKeyLengthsDic={i:0 for i in range(1,20)}
gcdList=[]
indexes = [i for i in range(0, 26)]

# Parse command line arguments

parser = argparse.ArgumentParser(description="Crack a Vigenere encryption key and decrypt the ciphertext")
parser.add_argument("cipherText", metavar="CipherText", type=str, help="The Vigenere encrypted ciphertext")
args=parser.parse_args()
cipherText=args.cipherText


# Make triple char groups, find said groups in the ciphertext and count occurrencies
# Skip last indexes, considered as garbage since they are not triple char groups
# Store triple chars in a set, I dont want repeated sets since that would change the occurrences
# Create set with unique triple chars

def createTripleCharSet():
    skipOffset=len(cipherText)-2
    for i in range(len(cipherText)):
        if i<skipOffset:
            offset=i+3
            tripleChar=cipherText[i:offset]
            tripleCharSet.add(tripleChar)


# Calculate spacing between each triple char occurrence
# For each triple char, first calculate index of found occurrence, store in variable, find next index starting from lastindex +1, iterate number of occurrencies times
# I initialize foundIndex as -1 to start at the right place, else id obtain a -1

def createOccurrenciesTripleCharDic():
    indexesList=[]
    minOccurrencies=2
    for i in tripleCharSet:
        occurrencies=cipherText.count(i)
        tripleCharDic[i] = occurrencies
        foundIndex=-1
        if occurrencies > minOccurrencies:
            indexesList=[]
            spacingList=[]
            for j in range(occurrencies):
                startSearchIndex=foundIndex+1
                foundIndex = cipherText.find(i,startSearchIndex)
                indexesList.append(foundIndex)
            for counter,k in enumerate(indexesList):
                for l in range(len(indexesList)-counter-1):
                    spacing=indexesList[-1-l]-k
                    spacingList.append(spacing)
            gcdList.append(gcd(*spacingList))
    return gcdList


# Calculate top keylenghts with a dic, being the key the number and the value the number of repetitions

def topKeyLengths():
    sortedTopKeyLenghtsDic={}
    for i in gcdList:
        topKeyLengthsDic[i]+=1
    sortedTopKeyLenghtsDic=dict(sorted(topKeyLengthsDic.items(), key=lambda item: item[1], reverse=True))
    return sortedTopKeyLenghtsDic


# Get user guess of the keylenght based on the top

def getInputKeylength():
    inputKeylength=int(input("Enter Keylength: "))
    return inputKeylength


# Create n Cipher Blocks appending ciphertext chars with n spacing, where n = keylenght

def cipherBlocks():
    cipherBlockList = []
    for cipherTextIndex in range(0, KeyLength):
        cipherBlock = ""
        while (cipherTextIndex < len(cipherText)):
            cipherBlock += cipherText[cipherTextIndex]
            cipherTextIndex += KeyLength
        cipherBlockList.append(cipherBlock)
    return cipherBlockList


# Create a 26 indexes list, take a cipher block and create a unicode list showing the frequency
# Index is based on the unicode decimal value of the char, taking 13 and calculating its modulo 26

def frequencyResolve():
    cipherFrequency = []
    for i in range(0, KeyLength):
        unicodeList = [0] * 26
        cipherBlock = cipherBlockList[i]
        for j in range(0, len(cipherBlock)):
            index = (ord(cipherBlock[j]) - 13) % 26
            unicodeList[index] += 1
        cipherFrequency.append(unicodeList)
    return cipherFrequency


# Shift a frequency block n times to the left and store the result in shift1

def shiftLeft(n, shift1):
    for i in range(0, n):
        shift2 = shift1
        shift1 = shift2[1:len(shift2)] + [shift2[0]]
    return shift1


# Each frequency block has a fixed lenght of 26 ints (Number of letter in the english alphabet)
# Shift to the left each value in each frequency block until completing a full round (26 times)
# For each single shift, multiply each value in the resulting shifted frequency block times the frequency value of each letter in the English alphabet (etaoin shrdlu. The tool that the teacher used is based on the english alphabet frequencies, even tho the result is in spanish)
# Add each value to a new list
# When all the sums are done, find the max frequency by creating an iter made out of the frequency and the letter in the alphabet
# Finally Get the key chars by using the most frequent letter in the alphabet and adding it 65 to get the decimal value in unicode (A = 65 decimal unicode)

def getKey():
    guessedKey = ""
    for i in range(0, KeyLength):
        frequencySums = []
        for j in range(0, 26):
            shiftedFrequencyBlock = shiftLeft(j, cipherFrequency[i])
            sum = 0
            for k in range(0, 26):
                sum += shiftedFrequencyBlock[k] * charFrequency[k]
            frequencySums.append(sum)
        frequencyMax = sorted(list(zip(frequencySums, indexes)), reverse=True)        
        guessedKey += chr(65 + frequencyMax[0][1])
    return guessedKey


# Create a list of the unicode values of the ciphertext and the key
# Turns each unicode value of the ciphertext into the unicode value of the plaintext
# Turns the list of unicode values into characters

def decrypt():
    plainUnicode = []
    cipherUnicode = [ord(letter) for letter in cipherText]
    keyUnicode = [ord(letter) for letter in guessedKey]
    for i in range(len(cipherUnicode)):
        plainUnicode.append(((cipherUnicode[i]-keyUnicode[i % KeyLength]) % 26) +97)
    plaintext = ''.join(chr(i) for i in plainUnicode)
    return plaintext


# Function calls, program execution flow

createTripleCharSet()
gcdList=createOccurrenciesTripleCharDic()

# print(tripleCharDic, end = "\n\n")
# print(gcdList, end = "\n\n")

sortedTopKeyLenghtsDic=topKeyLengths()
# print(sortedTopKeyLenghtsDic, end = "\n\n")

KeyLength=getInputKeylength()

cipherBlockList=cipherBlocks()
# print(cipherBlockList, end = "\n\n")

cipherFrequency=frequencyResolve()
# print(cipherFrequency, end = "\n\n")

guessedKey=getKey()
print("Guessed Key: " + guessedKey, end = "\n\n")

decryptedText=decrypt()
print (decryptedText, end = "\n\n")


# Program made by Efren Garcia, 2020/2021
