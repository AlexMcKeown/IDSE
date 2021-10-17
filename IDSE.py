
import sys # Read in from command line
import os # Exit if fail
from copy import copy, deepcopy

global size
global threshold
def readFileCLI(i):
    content = [] # Temp Array
    try:
        file_in = open(str(sys.argv[i]),"r")
        content = file_in.read().splitlines()
        file_in.close() # Close file

    except:
        print("Error in readFileCLI()! File " + str(sys.argv[1]) +" could not be loaded!")
        os._exit(-1) #Exit program

    return content


def evtProcess():
    global size
    content = readFileCLI(1)   # gives us an array with each index representing a line
    size = int(content[0])
    item = ""
    events = [] # List of events

    if(1 <= size and size <= 20): # Number of Monitored Events will be a positive integer no greater than 20.
        event = [["NULL"]*2] # Initalise event array with the number of monitored events
        evtIndex = 0

        i = 1

        while i < len(content): 
            colonCounter = 0 # colonCounter%2 == 0 -> new Event
            item = ""
            hitBreakPoint = False
            k = 0
            while k < len(content[i]):

                if(content[i][k] == ":"): # IF char == Colon
                    colonCounter+=1
                    hitBreakPoint = True
                else:
                    item += str(content[i][k]) # This char makes up a event
                

                if(hitBreakPoint == True):
                    if(colonCounter%2 == 1): # Event 
                        event[0][0] = item # Setting the Event 
                        item = "" #clear string 
              

                    elif(colonCounter%2 == 0): # Weight

                        event[0][1] = item # Setting the Event Weight
                        index = 0
                        item = "" #clear string
                        
                        events.append(deepcopy(event[0])) #Assign event to events list

                        if(evtIndex < size):
                            evtIndex+=1


                    hitBreakPoint = False
                k+=1
            i+=1
    else: # Error Message if exceeds the event constraint
        print("Error in evtProcess()! The Number of Monitored Events NEED to be 1) positive integer & 2) no greater than 20. You passed a total of "+str(size))
        os._exit(-1) #Exit program
    return events
    

def dataProcess():
    global size
    content = readFileCLI(2) # gives us an array with each index representing a line
    dataEvents =[]
    i = 0
    while i < len(content):
        k = 0
        index = 0
        item = ""
        event = [-1]*size #Initalise with temp data

        while k < len(content[i]):
            
            if(content[i][k] == ":"): # IF char == Colon
                
                event[index] = int(item)
                if(index < size):
                    index += 1
                    
                item = ""
            else:
                item += str(content[i][k]) # This char makes up a event

            k+=1
        i+=1
        dataEvents.append(deepcopy(event)) # Pass event to dataEvents list
    
    baseData = []
    i = 0 
    while i < size:
        baseData.append(stats(dataEvents,i))  #[i-size] [0] AVG | [1] STD
        i+=1
    return((baseData))


def stats(dataEvents, args):
    i = 0
    arr = []
    data = [] # [0] AVG | [1] STD
    while i < len(dataEvents):
        arr.append(dataEvents[i][args])
        i+=1

    data.append(round(sum(arr)/len(arr),2))
    variance = sum([((x - data[0]) ** 2) for x in arr]) / len(arr)
    data.append(round(variance ** 0.5, 2))

    return data


def printProfile(events, baseData):
    global size
    global threshold
    i = 0
    profileData = []
    profileData.append(["Event", "Average", "Stdev", "Weight"])
    while i < size:
        profileData.append([str(events[i][0]), str(baseData[i][0]), str(baseData[i][1]), str(events[i][1]) ])
        i+=1

    arr = []
    i = 0
    while i < len(events):
        arr.append(float(events[i][1]))
        i+=1

    for row in profileData:
        print("{: >20} {: >20} {:>20} {:>20}".format(*row))

    threshold = 2*(sum(arr))
    print("\nThreshold",threshold)


def testEvt(eventData):
    content = readFileCLI(3) # gives us an array with each index representing a line
    # Each [x][0] Row in Content Represents a different day
    # Each [0][x] Column Represents a different Event

    i = 0
    while i < len(content):
        if(content[i].replace(" ", "") != ""):
            distance = getDistance(eventData, content[i])
            print("Line "+str(i+1)+" -- "+str(content[i])+"\tDistance: "+str(distance) + "\t Alarm: "+isAlarming(distance))

 
        i+=1

def mergeData(events, baseData):
    eventData = [] # Merged base Data and Events -> [i][0] Event Names | [1] Event Weights | [2] Average | [3] Std Deviation
    i = 0
    while i < len(events):
        temp= [events[i][0],events[i][1], baseData[i][0], baseData[i][1]]
        eventData.append(deepcopy(temp))
        i+=1
    return(eventData)

def getDistance(eventData, content):
    arr = content.split(":")    
    arr.pop() # Remove white space at the end of the array
    totalDistance = 0.0
    i = 0
    while i < len(arr):
        #print(i,arr[i],eventData[i][2])
        totalDistance+= calcDistance(float(arr[i]), float(eventData[i][2]), float(eventData[i][3]), float(eventData[i][1]) )
        i+=1
    return round(totalDistance,2)

def calcDistance(event, mean, std, weight):
    return abs(((event-mean)/std)*weight)

def isAlarming(distance):
    if(distance > threshold):
        return "Yes"
    else:
        return "No"

def main():
    events = evtProcess() # 2D-Array [i][] -> [0] Event Names | [1] Event Weights
    baseData = dataProcess() #2D-Array [i][] -> [0] Average | [1] Std Deviation

    printProfile(events, baseData)
    
   
    eventData = mergeData(events,baseData) # Merged base Data and Events -> [i][0] Event Names | [1] Event Weights | [2] Average | [3] Std Deviation
    testEvt(eventData)
    

main()





