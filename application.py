"""
    cryptograms
    ~~~~~~~~
    a console application that entertains user with cryptogram games

    :copyright: (c) 2017 Shanshan Wang
    :license: MIT
"""

import csv
import random
import os

difficulty = 3 # control the number of letters being replaced in the cryptogram.

def loadData(idx):
    # load a quote from \data\quotes.csv
    with open('data/quotes.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if reader.line_num==idx:
                quote = row[1]
                author = row[2]
                return [quote, author]
            else:
                continue

def genKeys(original):
    # generate character mapping for encryption
    characterSet = [x for x in set(original.lower()) if x.isalpha()]
    nKeys = min(difficulty, len(characterSet))

    keys = random.sample(characterSet, nKeys)
    valueSet = set([chr(i) for i in range(ord('a'), ord('z'))]).difference(characterSet).union(set(keys))
    values= random.sample(valueSet, nKeys)
    keyMap={}
    for k in keys:
        v = random.sample(set(values).difference(k),1)
        values.remove(v[0])
        keyMap[k]=v[0]

    return keyMap

def getUserKeys(keyMap):
    # reverse key and value pairs in keyMap, to generate the answer for users
    userKeys= {}
    for key in keyMap:
        userKeys[keyMap[key]]= key
    return userKeys

def encrypt(original, keyMap):
    encryptedList = list(original)
    for i in range(0,len(original)):
        if (original[i].lower() in keyMap):
            key = original[i].lower()
            value = keyMap[key]
            if (original[i].islower()):
                encryptedList[i] = value
            else:
                encryptedList[i] = value.upper()
    encrypted = ''.join(encryptedList)
    return encrypted

def score(userInputs,userKeys):
    total = len(userInputs)
    correctCnt =0
    wrongCnt = 0

    for key in userKeys:
        if userKeys[key]==userInputs[key]:
            correctCnt +=1
        else:
            wrongCnt +=1

    if wrongCnt == 0:
        return "You are awesome!"
    elif wrongCnt == 1:
        return "So close!"
    else:
        return "Try again!"

if __name__ == "__main__":
    while True:
        idx =random.randint(1, 1000)
        print('game id = ' + str(idx))
        [original, author] = loadData(idx)

        print(author)
        keyMap = genKeys(original)

        encrypted = encrypt(original,keyMap)
        print(encrypted)

        print()
        input("Press enter when you are ready to crack the encrytogram...")
        userInputs={}
        for key in keyMap:
            ans = input(keyMap[key] + "=")
            userInputs[keyMap[key]]=str(ans)

        print()
        print("your answer=")
        print(encrypt(encrypted,userInputs))

        print()
        print('correct answer=')
        print(original)
        userKeys = getUserKeys(keyMap)
        print(userKeys)

        print("****************" + score(userInputs,userKeys) + "****************")

        print()
        yorn =input("Play another one(y/n)?")
        if yorn.lower()=='y':
            os.system('cls' if os.name == 'nt' else 'clear') # clear the window
            continue
        else:
            break
