# Firebase admin sdk import
import firebase_admin
# firebase realtime database import
from firebase_admin import credentials, db

import softwareParser

import datetime

from operator import itemgetter, attrgetter, methodcaller



def connectAndCreateBlankCollectionAndDB(privateKeyPath):
    try:
        # realtime database connection setup variables
        cred = credentials.Certificate(privateKeyPath)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://engrlabs-10f0c.firebaseio.com/'})
        ref = db.reference('/')

    except ValueError:
        # realtime database connection setup variables
        ref = db.reference('/')
        # print ref.get()

    return ref


def currentTimeInMinutes(hour, minute):
    hour2min = hour * 60
    return (hour2min + minute)



def updateUpcommingClass():
    # FIXME: TEST STUff
    # ================  Local Test paths - comment out before moving to the server  ===============
    # privateKeyPath = "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
    # ================  Test paths - comment out before moving to the server  ===============

    privateKeyPath = "/opt/testFlaskApp/engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"

    currentDT = datetime.datetime.now()

    ref = connectAndCreateBlankCollectionAndDB(privateKeyPath)

    ref_CurrentSemesterLabs = ref.child('PUBLIC_DATA/CurrentSemesterLabs')
    ref_DynamicData = ref.child('PUBLIC_DATA/DynamicData')

    # print ref_CurrentSemesterLabs.get()
    # print ref_DynamicData.get()

    currentSemesterLabsDic = ref_CurrentSemesterLabs.get()
    dynamicData = ref_DynamicData.get()

    dynamicLabList = dynamicData.keys()

    # currentSemesterLabsDic.keys()

    currentDayLetter = currentDT.strftime("%A")
    currentTimeMin = currentTimeInMinutes(currentDT.hour, currentDT.minute)

    # FIXME : Comment out the current time
    # FIXME: Comment the current day below
    currentTimeMin = 820
    currentDayLetter = "Tuesday"


    coursesTodayDict = {}
    coursesTodayList = []
    labCoursesTodayMap = {}
    availability = "true"

    for lab in dynamicLabList:
        # labCoursesTodayMap.clear()
        labCoursesTodayMap = {}

        if dict(currentSemesterLabsDic).has_key(lab):
            coursesList = currentSemesterLabsDic.get(lab).keys()
            for course in coursesList:

                startTimeStr = "StartTime: " + str(
                    currentTimeInMinutes(int(currentSemesterLabsDic.get(lab).get(course).get("StartHour")),
                                         int(currentSemesterLabsDic.get(lab).get(course).get("StartMin"))))
                endTimeStr = "EndTime: " + str(
                    currentTimeInMinutes(int(currentSemesterLabsDic.get(lab).get(course).get("EndHour")),
                                         int(currentSemesterLabsDic.get(lab).get(course).get("EndMin"))))

                startTime = (currentTimeInMinutes(int(currentSemesterLabsDic.get(lab).get(course).get("StartHour")),
                                                  int(currentSemesterLabsDic.get(lab).get(course).get("StartMin"))))
                endTime = (currentTimeInMinutes(int(currentSemesterLabsDic.get(lab).get(course).get("EndHour")),
                                                int(currentSemesterLabsDic.get(lab).get(course).get("EndMin"))))
                # upcommingClassTimeInMin =

                # startTime = 780
                # endTime = 840

                # if int(startTime) <= int(currentTimeMin) <= int(endTime):
                #     availability = "false"
                # else:
                #     availability = "true"

                if currentSemesterLabsDic.get(lab).get(course).get("Mon") == "Y" and currentDayLetter == "Monday":
                    print lab + " - " + course + " - " + "Monday"
                    # print currentSemesterLabsDic.get(lab).get(course).get("StartHour")
                    # print currentSemesterLabsDic.get(lab).get(course).get("StartMin")
                    #
                    # print startTimeStr
                    # print endTimeStr
                    # print "availability: " + availability
                    # print  currentTimeMin

                    labCoursesTodayMap = {}

                    labCoursesTodayMap.update({"RoomCode": lab})
                    labCoursesTodayMap.update({"Course": course})
                    labCoursesTodayMap.update({"startTimeMin": startTime})
                    labCoursesTodayMap.update({"endTimeMin": endTime})
                    labCoursesTodayMap.update({"Available": availability})
                    labCoursesTodayMap.update({"UpcommingClassCheck": availability})

                    # print labCoursesTodayMap

                    coursesTodayList.append(labCoursesTodayMap)
                    coursesTodayDict.update({lab: labCoursesTodayMap})
                    # coursesTodayDict.update({lab: labCoursesTodayMap})

                elif currentSemesterLabsDic.get(lab).get(course).get("Tues") == "Y" and currentDayLetter == "Tuesday":
                    print lab + " - " + course + " - " + "Tuesday"

                    labCoursesTodayMap = {}

                    labCoursesTodayMap.update({"RoomCode": lab})
                    labCoursesTodayMap.update({"Course": course})
                    labCoursesTodayMap.update({"startTimeMin": startTime})
                    labCoursesTodayMap.update({"endTimeMin": endTime})
                    labCoursesTodayMap.update({"Available": availability})
                    labCoursesTodayMap.update({"UpcommingClassCheck": availability})

                    # print labCoursesTodayMap

                    # coursesTodayDict.append(course)
                    coursesTodayList.append(labCoursesTodayMap)
                    coursesTodayDict.update({lab: labCoursesTodayMap})


                elif currentSemesterLabsDic.get(lab).get(course).get("Wed") == "Y" and currentDayLetter == "Wednesday":
                    print lab + " - " + course + " - " + "Wednesday"

                    labCoursesTodayMap = {}

                    labCoursesTodayMap.update({"RoomCode": lab})
                    labCoursesTodayMap.update({"Course": course})
                    labCoursesTodayMap.update({"startTimeMin": startTime})
                    labCoursesTodayMap.update({"endTimeMin": endTime})
                    labCoursesTodayMap.update({"Available": availability})
                    labCoursesTodayMap.update({"UpcommingClassCheck": availability})

                    # print labCoursesTodayMap

                    # coursesTodayDict.append(course)
                    coursesTodayList.append(labCoursesTodayMap)
                    coursesTodayDict.update({lab: labCoursesTodayMap})

                elif currentSemesterLabsDic.get(lab).get(course).get("Thurs") == "Y" and currentDayLetter == "Thursday":
                    print lab + " - " + course + " - " + "Thurs"

                    labCoursesTodayMap = {}

                    labCoursesTodayMap.update({"RoomCode": lab})
                    labCoursesTodayMap.update({"Course": course})
                    labCoursesTodayMap.update({"startTimeMin": startTime})
                    labCoursesTodayMap.update({"endTimeMin": endTime})
                    labCoursesTodayMap.update({"Available": availability})
                    labCoursesTodayMap.update({"UpcommingClassCheck": availability})

                    # print labCoursesTodayMap

                    # coursesTodayDict.append(course)
                    coursesTodayList.append(labCoursesTodayMap)
                    coursesTodayDict.update({lab: labCoursesTodayMap})

                elif currentSemesterLabsDic.get(lab).get(course).get("Friday") == "Y" and currentDayLetter == "Friday":
                    print lab + " - " + course + " - " + "Friday"

                    labCoursesTodayMap = {}

                    labCoursesTodayMap.update({"RoomCode": lab})
                    labCoursesTodayMap.update({"Course": course})
                    labCoursesTodayMap.update({"startTimeMin": startTime})
                    labCoursesTodayMap.update({"endTimeMin": endTime})
                    labCoursesTodayMap.update({"Available": availability})
                    labCoursesTodayMap.update({"UpcommingClassCheck": availability})

                    # print labCoursesTodayMap

                    # coursesTodayDict.append(course)
                    coursesTodayList.append(labCoursesTodayMap)
                    coursesTodayDict.update({lab: labCoursesTodayMap})

                elif currentSemesterLabsDic.get(lab).get(course).get(
                        "Saturday") == "Y" and currentDayLetter == "Saturday":
                    print lab + " - " + course + " - " + "Saturday"

                    labCoursesTodayMap = {}

                    labCoursesTodayMap.update({"RoomCode": lab})
                    labCoursesTodayMap.update({"Course": course})
                    labCoursesTodayMap.update({"startTimeMin": startTime})
                    labCoursesTodayMap.update({"endTimeMin": endTime})
                    labCoursesTodayMap.update({"Available": availability})
                    labCoursesTodayMap.update({"UpcommingClassCheck": availability})

                    # print labCoursesTodayMap

                    # coursesTodayDict.append(course)
                    coursesTodayList.append(labCoursesTodayMap)
                    coursesTodayDict.update({lab: labCoursesTodayMap})

                elif currentSemesterLabsDic.get(lab).get(course).get("Sun") == "Y" and currentDayLetter == "Sunday":
                    print lab + " - " + course + " - " + "Sunday"

                    labCoursesTodayMap = {}

                    labCoursesTodayMap.update({"RoomCode": lab})
                    labCoursesTodayMap.update({"Course": course})
                    labCoursesTodayMap.update({"startTimeMin": startTime})
                    labCoursesTodayMap.update({"endTimeMin": endTime})
                    labCoursesTodayMap.update({"Available": availability})
                    labCoursesTodayMap.update({"UpcommingClassCheck": availability})

                    # print labCoursesTodayMap

                    # coursesTodayDict.append(course)
                    coursesTodayList.append(labCoursesTodayMap)
                    coursesTodayDict.update({lab: labCoursesTodayMap})

        else:
            print lab + " - Available"

    # print coursesTodayList
    # print coursesTodayDict

    # the keys of the labs that has class today
    coursesTodayInLabsList = coursesTodayDict.keys()

    dict2Save = {}
    tempSaveArr = []

    for scheduleObj in coursesTodayList:
        tempSaveArr = []
        # print scheduleObj
        if not dict2Save.has_key(scheduleObj.get("RoomCode")):
            tempSaveArr.append(scheduleObj)
            dict2Save.update({scheduleObj.get("RoomCode"): tempSaveArr})

        else:
            tempSaveArr = dict2Save.get(scheduleObj.get("RoomCode"))
            tempSaveArr.append(scheduleObj)
            dict2Save.update({scheduleObj.get("RoomCode"): tempSaveArr})

    # print dict2Save

    # currentTimeMin = 800

    calculateTimeForUpcomingClass = -1;

    for lab in dynamicLabList:
        if dict2Save.has_key(lab):
            # print 'PUBLIC_DATA/DynamicData/' + lab
            ref_DynamicDataRoomCode = ref.child('PUBLIC_DATA/DynamicData/' + lab)

            ref_DynamicDataRoomCode.update({
                unicode("UpcommingClass"): dict2Save.get(lab),
                # unicode("LabAvailable"): dict2Save.get(lab).get("Available")
            })

        else:
            ref_DynamicDataRoomCode = ref.child('PUBLIC_DATA/DynamicData/' + lab)

            ref_DynamicDataRoomCode.update({
                unicode("UpcommingClass"): [{"Available": "true", 'UpcommingClassCheck': -1}],
                # unicode("LabAvailable"): dict2Save.get(lab).get("Available")
            })

    # refreshing the data after saving the upcoming classes
    dynamicData = ref_DynamicData.get()
    dynamicLabList = dynamicData.keys()


    # RESETTING all the values of the availibility to true and the upcoming time is reset
    for lab in dynamicLabList:
        ref_DynamicDataRoomCode = ref.child('PUBLIC_DATA/DynamicData/' + lab)
        ref_DynamicDataRoomCode.update({
            unicode("LabAvailable"): "true",
            unicode("UpcomingClassTime"): -1
            # unicode("LabAvailable"): dict2Save.get(lab).get("Available")
        })

    for lab in dynamicLabList:
        upcomingArray = dynamicData.get(lab).get("UpcommingClass")
        # if (not len(list(upcomingArray)) > 1) and not (dict(upcomingArray[0]).get("UpcommingClassCheck")) == -1:

        # looking at labs that has labs
        if not (dict(upcomingArray[0]).get("UpcommingClassCheck")) == -1:
            # print len(list(upcomingArray))
            # print dynamicData.get(lab).get("UpcommingClass")

            # print upcomingArray
            # for schedule in upcomingArray:
            #     print schedule

            # print sorted(upcomingArray, key = lambda i: i["startTimeMin"], reverse=False)
            sortedArray = sorted(upcomingArray, key=lambda i: i["startTimeMin"], reverse=False)
            sortedArrayLength = len(sortedArray)
            # print sortedArrayLength

            sortedCounter = 0
            upcomingBusyIndex = -1
            #
            for sortedElement in sortedArray:
                sortedCounter = sortedCounter + 1
                # print sortedCounter
                # if sortedArrayLength == sortedCounter:
                #     print "lastElement"
                # else:
                #     print "Elements left"

                # calculating the ongoing class
                if int(sortedElement.get("startTimeMin")) <= int(currentTimeMin) <= int(
                        sortedElement.get("endTimeMin")):
                    # print sortedElement

                    upcomingBusyIndex = sortedCounter

                    ref_DynamicDataRoomCode = ref.child('PUBLIC_DATA/DynamicData/' + lab)
                    ref_DynamicDataRoomCode.update({
                        unicode("LabAvailable"): "false"
                        # unicode("LabAvailable"): dict2Save.get(lab).get("Available")
                    })

                    refreshUpcomingArrRef = ref.child('PUBLIC_DATA/DynamicData/' + lab + "/UpcommingClass")
                    refreshUpcomingArr = refreshUpcomingArrRef.get()

                    # print refreshUpcomingArr
                    # print len(refreshUpcomingArr)

                    for element in refreshUpcomingArr:
                        # print element
                        element.update({"Available": "false"})
                        # element.update()

                    # print refreshUpcomingArr

                    ref_DynamicDataRoomCode.update({
                        unicode("UpcommingClass"): refreshUpcomingArr
                        # unicode("LabAvailable"): dict2Save.get(lab).get("Available")
                    })

                else:
                    ref_DynamicDataRoomCode = ref.child('PUBLIC_DATA/DynamicData/' + lab)
                    ref_DynamicDataRoomCode.update({
                        unicode("LabAvailable"): "true"
                        # unicode("LabAvailable"): dict2Save.get(lab).get("Available")
                    })

                # calculating the upcoming class
                if sortedCounter == upcomingBusyIndex + 1:
                    calculateTimeForUpcomingClass = int(sortedElement.get("startTimeMin")) - currentTimeMin

                    ref_DynamicDataRoomCode.update({
                        unicode("LabAvailable"): "false",
                        unicode("UpcomingClassTime"): calculateTimeForUpcomingClass
                        # unicode("LabAvailable"): dict2Save.get(lab).get("Available")
                    })

