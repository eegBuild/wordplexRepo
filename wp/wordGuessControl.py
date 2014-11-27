import time
import datetime
import random
import linecache
import xml.etree.ElementTree as ET
from xmlParse import *
from wordplexModel import Player
from io import StringIO
from flask import Flask, render_template

# Returns a string of todays date in Irish format
def getStrDate():

    date = datetime.date.today()
    return "{}-{}-{}".format(date.day,date.month,date.year)

player = Player()
player.date = getStrDate()



# Updates player
def savePlayerName(fname,sname):
    player.fname = fname
    player.sname = sname

#
def begin_game():
    player.s_time = getTimeNow()
    out = getRandomWord()
    out = out.rstrip('\r\n')
    player.word = out
    out = '{\"data\": \"%s\"}' % out
    return out

def saveGame():
    player.e_time = getTimeNow()
    player.time_secs = str(player.e_time - player.s_time)
    player.time = getStrTimeDiff(player.s_time,player.e_time)
    appendXml(player)
    out = states = {
    'fname': player.fname,
    'rank': player.rank,
    'time': player.time}
    return out
    
    
    
# Returns a float of time now in seconds
def getTimeNow():
    return time.time()

# Returns a string of time elapsed between two times in seconds
def getStrTimeDiff(start, end):
    mins = " Minute"
    diff = end - start
    
    mint = int(diff/60) % 60
    sec = float("{0:.2f}".format(diff % 60))
    if mint != 1:
        mins = "Minutes"
    if mint < 1:
        return "{} Seconds".format(sec)
    if mint >= 1:
        return "{} {} and {} seconds".format(mint,mins,sec)

#Returns a string of randomly picked word from a file of words
def getRandomWord():
    fobj = open("static\Files\sevenWords.txt","r")
    lineCount = sum(1 for _ in fobj)
    randnum = random.randint(0,lineCount-1)
    #json format
    word = open("static\Files\sevenWords.txt","r").readlines()[randnum]
    #word = '{\"data\": \"%s\"}' % open("static\Files\sevenWords.txt","r").readlines()[randnum]
    #word = word.replace("\n","")
    return word

def checkWords(word_list):
    check = isListMatch(word_list,"static\\Files\\testWords.txt")
    if check != "xtruex":
        return check
    return check

#Returns a boolean if word matches word in file
# isWordMatch(word[string], filepath[string])
def isWordMatch(wordin, filein):
    out = False
    fobj = open(filein,"r")
    
    for word in fobj:
        if word == wordin:
            out = True
    return out


#Returns a error message of any word that
# is not i aggreement with the rules
# checkInputWord((wordIn[string], filepath[string])
def checkInputWord(wordIn, filein):
    wordIn.lower()
    fobj = open(filein,"r")
    message = "x"
    player.word_list.append(wordIn)
        
    if player.word == wordIn:

        message = "The source word cannot be used as an answer word."
        del player.word_list[-1]
        return message

    matchFile = wordInFile(wordIn, fobj)
    if len(matchFile) > 0:
        if len(matchFile[0]) < 3:
            message = "The Word "+matchFile[0]+" is Less than 3 letters long"
            del player.word_list[-1]
            return message
        else:
            message = "The Word "+matchFile[0]+" is not in the Test Dictionary"
            del player.word_list[-1]
            return message
        
    duplicates = isDuplicateInList(player.word_list)
    if len(duplicates) > 0:
        message = "The Word "+duplicates[0]+" has been used more than once"
        del player.word_list[-1]
        return message
        
    for word in fobj:
     
        char_overload = isCharInWord(player.word, wordIn)
        if len(char_overload) > 0:
            message = "The Word "+wordIn.replace("\n","")+" uses the letter "+char_overload[0]+" which is not in the source word"
            del player.word_list[-1]
            return message
        cheat = isCheatWord(player.word, wordIn)
        if len(cheat) > 0:
            message = "The Word "+wordIn.replace("\n","")+" uses "+cheat[0]+" to many times"
            del player.word_list[-1]
            return message

                                      
    return message
    
# Returns a list if testword uses to many same letters
def isCheatWord(goodword, testword):
    out = []
    for c in testword:
        if testword.count(c) > goodword.count(c):
            out.append(c)
    return out

# Returns a list if testword uses letters not in source word
def isCharInWord(goodword, testword):
    out = []
    check = True
    for c in testword:
        if check == False:
            out.append(temp_c)
        temp_c = c
        check = False
        for ch in goodword:
            if c == ch:
                check = True

    return out

# Returns a list of duplicates in a list
def isDuplicateInList(listin):
    print("InDUP")
    out =[]
    for word in listin:
        i = listin.index(word)+1
        for j in range(i,len(listin)):
            print("************"+word)
            print("************"+listin[j])
            print()
            if word == listin[j]:
                out.append(word)
    
    return out

# Returns a list of word if not in file
def wordInFile(wordin,filein):
    print("InDict")
    out = []
    check = False
    for w in filein:
        if w.replace("\n", "").replace("\t", "") == wordin.replace("\n", "").replace("\t", ""):
            check = True
            break
    if check == False:
        out.append(wordin)
    return out

# Returns list[] of highScores
def getHighScores(filein):
    tree = ET.parse(filein)
    root = tree.getroot()
    outlist = []
    for player in root.findall('player'):
            rank = player.find('rank').text
            name = player.find('name').text
            time = player.find('time').text
            timesecs = player.find('time_secs').text
            date = player.find('date_set').text
            templist = [rank,name,time,timesecs,date]
            outlist.append(templist)
    return outlist
    

##player =Player()
##player.word = "superman"
##player.word_list.append("super")
##player.word_list.append("man")
##player.word_list.append("ram")
##out = checkInputWord("supper", "static\\Files\\testWords.txt")
##print(out)
##if len(player.word_list) > 0:
##    for w in player.word_list:
##        print(w)

   
