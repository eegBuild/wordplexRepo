from xml.dom.minidom import parse
import xml.dom.minidom
from io import StringIO
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element
import os



def xmlTojson():

    buf = StringIO()
      
    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse("static/Files/highScores.xml")
    collection = DOMTree.documentElement

    # Get all the players in the collection
    players = collection.getElementsByTagName("player")

    buf.write("{\n\"players\" : [\n")
    for player in players:
        a = player.getElementsByTagName('fname')[0]
        fname = "\"fname\": \"%s\",\n" % a.childNodes[0].data
        b = player.getElementsByTagName('sname')[0]
        sname = "\"sname\": \"%s\",\n" % b.childNodes[0].data
        c = player.getElementsByTagName('rank')[0]
        rank = "\"rank\": \"%s\",\n" % c.childNodes[0].data
        d = player.getElementsByTagName('time')[0]
        time = "\"time\": \"%s\",\n" % d.childNodes[0].data
        e = player.getElementsByTagName('date_set')[0]
        date = "\"date\": \"%s\"\n" % e.childNodes[0].data
        buf.write("{"+fname+sname+rank+time+date+"},")

    temp = buf.getvalue()
    temp = temp[:-1]
    temp += "]}"
      
    buf.close()
    return temp

# Function specific to Class Player and highscore.xml
def appendXml(classIn):

    tree = etree.parse("static/Files/highScores.xml")
    root = tree.getroot()
    

    for x in tree.iterfind('players'):

        #add new player tag to root<highscore>
        pl = Element("player")
        
        #add new fname tag to parent<player>
        # and give value from classIn
        fname = Element("fname")
        fname.text = classIn.fname
        pl.append(fname)
        
        sname = Element("sname")
        sname.text = classIn.sname
        pl.append(sname)
        
        rank = Element("rank")
        rank.text = classIn.rank
        pl.append(rank)
        
        time = Element("time")
        time.text = classIn.time
        pl.append(time)
        
        time_secs = Element("time_secs")
        time_secs.text = classIn.time_secs
        pl.append(time_secs)
        
        date = Element("date_set")
        date.text = classIn.date
        pl.append(date)
        
        x.append(pl)

    # Write new xml file to highscore.xml
    tree.write("static/Files/highScoresxx.xml")

def sortXml():

    tree = etree.parse("static/Files/highScoresTest.xml")
    root = tree.getroot()
    # this element holds the player entries
    container = Element("players")


    data = []

    for elem in tree.iterfind('players/player'):
        time_secs = float(elem.findtext("time_secs"))
        print(time_secs)
        data.append((time_secs , elem))
        
    sorted_x = sorted(data, key=getKey)
    for all in sorted_x:
        print(all)

    # insert the last item from each tuple
    container[:] = [item[-1] for item in sorted_x]
    
##    for x in tree.iterfind('players'):
##         root.remove(x)
##    root.append(container)



    tree.write("static/Files/highScoresTestxx.xml")


def getKey(item):
    return item[0]




