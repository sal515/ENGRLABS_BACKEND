class softwareObject:
    pass


def parsingStep1(sourceCode, debug):
    global listOfSoftwareAndRooms, beginning, end, sliceObject
    lastInstanceOfTr = 0
    loopCounter = 0
    listOfSoftwareAndRooms = []
    while (sourceCode.find('<tr>') > -1) and loopCounter < 200:
        beginning = (sourceCode.find("<tr>", lastInstanceOfTr));
        end = (sourceCode.find("</tr>", lastInstanceOfTr)) + 5;
        if (end < beginning):
            if (debug == True):
                print('error')
            break
        sliceObject = slice(beginning, end, 1)
        temp = sourceCode[sliceObject]
        if (debug == True):
            print(temp)
        listOfSoftwareAndRooms.append(temp)
        lastInstanceOfTr = end
        loopCounter += 1
    if (debug == True):
        print('step 1 done')


# each index of listOfSoftwareAndRooms looks like this ---->  <tr><td>Android Studio 3</td><td> H0903-00, H0915-00, H0929-00</td></tr>


def parsingStep2(debug):
    global softwareObjectList, beginning, end, sliceObject
    softwareObjectList = []
    for stringAtIndex in listOfSoftwareAndRooms:
        lastInstanceOfTd = 0
        tempSoftwareObject = softwareObject()

        beginning = (stringAtIndex.find("<td>", 0))
        end = (stringAtIndex.find("</td>", 0))
        sliceObject = slice(beginning + 4, end, 1)
        softwareName = stringAtIndex[sliceObject]
        # print(softwareName)

        beginning2 = (stringAtIndex.find("<td>", end + 5))
        end2 = (stringAtIndex.find("</td>", end + 5))
        sliceObject2 = slice(beginning2 + 4, end2, 1)
        classList = stringAtIndex[sliceObject2].replace(' ', '')
        # print(classList)

        # print(tempSoftwareObject.softwareName)
        # print(tempSoftwareObject.classList)

        if (len(classList) > 0):
            tempSoftwareObject.softwareName = softwareName
            tempSoftwareObject.classList = classList + ','
            softwareObjectList.append(tempSoftwareObject)

            if (debug == True):
                if (len(softwareObjectList) > 0):
                    print(softwareObjectList[len(softwareObjectList) - 1].softwareName)
                    print(softwareObjectList[len(softwareObjectList) - 1].classList)
    if (debug == True):
        print('step 2 done')


def parsingStep3(SoftwareAndClassList, debug, outputView):
    global sliceObject, tempSoftwareAndClassObject

    # softwareObject.softwareName   looks like this -----> CPLEX_Studio_127
    # softwareObject.classList   looks like this -----> H0811-00,H0819-00,H0823-00,H0831-00,H0854-00,H0961-01,H0961-02,H0961-03,
    # H0961-04,H0961-06,H0961-07,H0961-10,H0961-11,H0961-13,H0961-14,
    # H0961-15,H0961-17,H0961-19,H0961-21,H0961-23,H0961-25,H0961-26,
    # H0961-27,H0961-28,H0961-29,H0961-31,H0961-33
    class SoftwareAndClass:
        pass

    for softwareObjectAtIndex in softwareObjectList:
        comma = 0
        while (softwareObjectAtIndex.classList.find(",", comma) > -1):
            nextComma = (softwareObjectAtIndex.classList.find(",", comma))
            sliceObject = slice(comma, nextComma)
            extractedRoom = softwareObjectAtIndex.classList[sliceObject]
            if (debug == True):
                print(extractedRoom)
            extractedBuilding = extractedRoom[0]
            if (extractedBuilding == 'H'):
                extractedFloor = extractedRoom[1] + extractedRoom[2]
                extractedClassNumber = extractedRoom[3] + extractedRoom[4]
                if (debug == True):
                    print(
                            'building: ' + extractedBuilding + ' floor: ' + extractedFloor + ' classNumber: ' + extractedClassNumber)
                tempSoftwareAndClassObject = SoftwareAndClass()
                tempSoftwareAndClassObject.softwareName = softwareObjectAtIndex.softwareName
                tempSoftwareAndClassObject.classBuilding = extractedBuilding
                tempSoftwareAndClassObject.classFloor = extractedFloor
                tempSoftwareAndClassObject.classRoom = extractedClassNumber

                alreadyPresent = False
                for SoftwareAndClassListObjectAtIndex in SoftwareAndClassList:
                    if ((SoftwareAndClassListObjectAtIndex.softwareName == tempSoftwareAndClassObject.softwareName)
                            and (
                                    SoftwareAndClassListObjectAtIndex.classBuilding == tempSoftwareAndClassObject.classBuilding)
                            and (SoftwareAndClassListObjectAtIndex.classFloor == tempSoftwareAndClassObject.classFloor)
                            and (SoftwareAndClassListObjectAtIndex.classRoom == tempSoftwareAndClassObject.classRoom)):
                        alreadyPresent = True
                        if (debug == True):
                            print('alreadyThere')
                        break
                if (alreadyPresent == False):
                    SoftwareAndClassList.append(tempSoftwareAndClassObject)
            comma = nextComma + 1
    if (debug == True):
        print('step 3 done')
    if (outputView == True):
        for tempIndex in SoftwareAndClassList:
            print(
                    'Software Name: ' + tempIndex.softwareName + ' Building: ' + tempIndex.classBuilding + ' Floor: ' + tempIndex.classFloor + ' ClassNumber: ' + tempIndex.classRoom)

    # return SoftwareAndClassList

    # Software Name: SuperDecision Building: H Floor: 08 ClassNumber: 35
    # Software Name: THERM761 Building: H Floor: 08 ClassNumber: 19
    # Software Name: Trane_Pipe_Designer_v4.1.0 Building: H Floor: 08 ClassNumber: 07
    # Software Name: Unity 2018.3.1f1 Building: H Floor: 08 ClassNumber: 23
    # Software Name: Unity 2018.3.1f1 Building: H Floor: 09 ClassNumber: 17
    # Software Name: Visual_MODFLOW_v2009_1 Building: H Floor: 08 ClassNumber: 19
    # Software Name: Visual_MODFLOW_v2009_1 Building: H Floor: 08 ClassNumber: 21
    # Software Name: Weka3_8_0 Building: H Floor: 08 ClassNumber: 15
    # Software Name: Weka3_8_0 Building: H Floor: 08 ClassNumber: 17
    # Software Name: Weka3_8_0 Building: H Floor: 08 ClassNumber: 25
    # Software Name: Weka3_8_0 Building: H Floor: 08 ClassNumber: 27
    # Software Name: Weka3_8_0 Building: H Floor: 08 ClassNumber: 31
    # Software Name: Weka3_8_0 Building: H Floor: 08 ClassNumber: 43


def convertingDataFromList2Dict(SoftwareAndClassList, softLabDict):
    for tempIndex in SoftwareAndClassList:
        arr = []
        tempIndex.softwareName = str(tempIndex.softwareName).replace(".", "_")
        if str(tempIndex.softwareName) not in softLabDict:
            arr = [tempIndex]
            tempIndex.classFloor = (str(tempIndex.classFloor).lstrip("0"))
            # tempIndex.classRoom = (str(tempIndex.classRoom).lstrip("0"))
            softLabDict.update({str(tempIndex.softwareName): arr})
        else:
            arr = softLabDict.get(str(tempIndex.softwareName))
            tempIndex.classFloor = (str(tempIndex.classFloor).lstrip("0"))
            # tempIndex.classRoom = (str(tempIndex.classRoom).lstrip("0"))
            arr.append(tempIndex)


        # Testing String strippng
        # print "software names " + tempIndex.softwareName
        # replacedString = str(tempIndex.softwareName).replace(".", "_")
        # print "software names stripped/replaced   " + replacedString


        # print "class room: " + tempIndex.classRoom
        # print "class room stripped: " + (str(tempIndex.classRoom).lstrip("0"))

        # print "class number: " + tempIndex.classFloor
        # print "class number stripped: " + (str(tempIndex.classFloor).lstrip("0"))

    # pause = 0
    return softLabDict

def softwareParsingMain():
    fileName = 'input.txt'
    file = open(fileName, 'r')
    sourceCode = file.read()

    debug = False
    outputView = False
    # printTester = True
    printTester = False

    parsingStep1(sourceCode, debug)

    parsingStep2(debug)

    SoftwareAndClassList = []

    parsingStep3(SoftwareAndClassList, debug, outputView)

    if printTester:
        for tempIndex in SoftwareAndClassList:
            print(
                    'Software Name: ' + tempIndex.softwareName + ' Building: ' + tempIndex.classBuilding + ' Floor: ' + tempIndex.classFloor + ' ClassNumber: ' + tempIndex.classRoom)

    # tester = 10

    softLabDict = {}
    return convertingDataFromList2Dict(SoftwareAndClassList, softLabDict)


# Calling the main function
# main()
