import discord
import os
import calendar
from replit import db
from keep_alive import keep_alive
import datetime
from datetime import date
from ast import literal_eval
from pytz import timezone
import io

import requests
import json
import random
import numpy


#Variables
tz = timezone('US/Eastern')
client = discord.Client()
today = str(datetime.datetime.now(tz))[0:10]
theTime = str(datetime.datetime.now(tz))[11:16]
todayArray = str(today).split("-")
myCal = []
defaultCal = []
calData = []
calName = "No name"
habitName = "No name"
numDaysInMonth = 0
weekDay = 0
memName = ""
ran = 0



if "responding" not in db.keys():
  db["responding"] = True


def month_detection(userName):
  month = str(todayArray[1])
  if month[0] == "0":
    month = int(month[1])
  numDaysInMonth = calendar.monthrange(int(todayArray[0]),month)[1]
  weekDay = date(int(todayArray[0]), month, 1).weekday()

  initCalYear = []
  #initialize_cal for each month
  for monthNum in range (1,13):
    tempCal = []
    numDaysInMonth = calendar.monthrange(int(todayArray[0]),monthNum)[1]
    weekDay = date(int(todayArray[0]), monthNum, 1).weekday()
    global startIndex
    startIndex = weekDay + 1
    if weekDay == 6:
      for y in range (0, numDaysInMonth):
        #myCal.append["."]
        if (numDaysInMonth - ((numDaysInMonth // 7) * 7)) != 0:
          leftover = numDaysInMonth - ((numDaysInMonth // 7) * 7)
          for a in range (0, leftover):
            tempCal.append(".")
    else : #Monday
      for b in range (0, weekDay + 1):
        tempCal.append(" ")
      for a in range (0, numDaysInMonth):
        tempCal.append(".")
    initCalYear.append(tempCal)
  userTempCal = []
  takenCal = []
  if db[userName][3] == "Multiple":
    takenCal = (list(db[userName][1].values())[0])
  else:
    takenCal = (db[userName][1])

  for symbol in takenCal:
    if symbol == " ":
      userTempCal.append(" ")
    if symbol == "✓" or symbol == "x" or symbol == ".":
      userTempCal.append(".")
  
  #compare initialized cals months with past cal
  for monthNum in range (0,12):
    if userTempCal == initCalYear[monthNum]:
      pastMonVal = monthNum
      return pastMonVal + 1
  print (startIndex)

def month_change(userName):
  month = str(todayArray[1])
  if month[0] == "0":
    month = int(month[1])
  numDaysInMonth = calendar.monthrange(int(todayArray[0]),month)[1]
  weekDay = date(int(todayArray[0]), month, 1).weekday()

  initCalYear = []
  #initialize_cal for each month
  for monthNum in range (1,13):
    tempCal = []
    numDaysInMonth = calendar.monthrange(int(todayArray[0]),monthNum)[1]
    weekDay = date(int(todayArray[0]), monthNum, 1).weekday()
    global startIndex
    startIndex = weekDay + 1
    if weekDay == 6:
      for y in range (0, numDaysInMonth):
        #myCal.append["."]
        if (numDaysInMonth - ((numDaysInMonth // 7) * 7)) != 0:
          leftover = numDaysInMonth - ((numDaysInMonth // 7) * 7)
          for a in range (0, leftover):
            tempCal.append(".")
    else : #Monday
      for b in range (0, weekDay + 1):
        tempCal.append(" ")
      for a in range (0, numDaysInMonth):
        tempCal.append(".")
    initCalYear.append(tempCal)
  userTempCal = []
  takenCal = []
  if db[userName][3] == "Multiple":
    takenCal = (list(db[userName][1].values())[0])
  else:
    takenCal = (db[userName][1])

  for symbol in takenCal:
    if symbol == " ":
      userTempCal.append(" ")
    if symbol == "✓" or symbol == "x" or symbol == ".":
      userTempCal.append(".")
  
  #compare initialized cals months with past cal
  for monthNum in range (0,12):
    if userTempCal == initCalYear[monthNum]:
      pastMonVal = monthNum

  #when match is found match current initialized_cal
  currentTempCal = clean_initialize_cal()
  for monthNum in range (0,12):
    if currentTempCal == initCalYear[monthNum]:
      curMonVal = monthNum

  #if current match matches past cal match do nothing/proceed, if they do not match print new month detected, restart calendar?
  if pastMonVal != curMonVal:
    return True
  else:
    return False

def initialize_cal():
  month = str(todayArray[1])
  if month[0] == "0":
    month = int(month[1])
  numDaysInMonth = calendar.monthrange(int(todayArray[0]),month)[1]
  weekDay = date(int(todayArray[0]), month, 1).weekday()

  #for x in range(1, int(weekDay)+1):
  if weekDay == 6:
    for y in range (0, numDaysInMonth):
      #myCal.append["."]
      if (numDaysInMonth - ((numDaysInMonth // 7) * 7)) != 0:
        leftover = numDaysInMonth - ((numDaysInMonth // 7) * 7)
        for a in range (0, leftover):
          myCal.append(".")
  else : #Monday
    for b in range (0, weekDay + 1):
      myCal.append(" ")
    for a in range (0, numDaysInMonth):
      myCal.append(".")

def clean_initialize_cal():
  month = str(todayArray[1])
  if month[0] == "0":
    month = int(month[1])
  numDaysInMonth = calendar.monthrange(int(todayArray[0]),month)[1]
  weekDay = date(int(todayArray[0]), month, 1).weekday()
  
  myCalClean = []
  #for x in range(1, int(weekDay)+1):
  if weekDay == 6:
    for y in range (0, numDaysInMonth):
      #myCal.append["."]
      if (numDaysInMonth - ((numDaysInMonth // 7) * 7)) != 0:
        leftover = numDaysInMonth - ((numDaysInMonth // 7) * 7)
        for a in range (0, leftover):
          myCalClean.append(".")
  else : #Monday
    for b in range (0, weekDay + 1):
      myCalClean.append(" ")
    for a in range (0, numDaysInMonth):
      myCalClean.append(".")
  return myCalClean

def retrieve_data(senderName):
  global ran
  global myCal
  global habitName
  global calName
  global startIndex
  ran = 0
  dataBase = list(db.keys())
  h = len(dataBase)
  if " " in senderName:
        senderName = senderName.replace(" ", "@")
        senderName = senderName.replace("#", "@")
  else:
    senderName = senderName.replace("#", "@")
  while ran != 1:
    if h == -1:
      break
    if dataBase[h-1] == senderName:
      val = db[senderName]
      val = str(val).replace("[[", "[")
      val = str(val).replace("]]", "]")
      val = literal_eval(val)
      myCal = val[1]
      habitName = val[3]
      startIndex = val[2]
      calName = "No name"
      ran = 1
      #db[senderName] = calData
    else:
      h -= 1
  if ran != 1:
      calData.append([senderName, defaultCal, 0, "No name"])
      myCal = defaultCal
      habitName = "No name"
      calName = "No name"
      if " " in senderName:
        senderName = senderName.replace(" ", "@")
        senderName = senderName.replace("#", "@")
      else:
        senderName = senderName.replace("#", "@")
      db[senderName] = calData
  

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name="type $help"))

@client.event
async def on_message(message):

  month = str(todayArray[1])
  if month[0] == "0":
    month = int(month[1])
  numDaysInMonth = calendar.monthrange(int(todayArray[0]),month)[1]
  weekDay = date(int(todayArray[0]), month, 1).weekday()
  startIndex = weekDay + 1
  #nickname = message.author
#-------------------------------------------------
  if message.author == client.user:
    return
  msg = message.content
  memName = str(message.author) 
  if "force" in msg:
    if memName == "CinnamonToast <3#9606":
      grabMember = msg.split("_")
      memName = grabMember[2]
      msg = msg.replace("force","")
      msg = msg.replace(str(grabMember[2]),"")
      msg = msg.replace("_","")
      await message.channel.send("You are now " + str(memName))
    else:
      await message.channel.send("You don't have permission to do that! We will do the requested command under your username instead.")
#-------------------------------------------------
  if msg.startswith('$help'):
    await message.channel.send("**$addHabit** habitName: adds a new habit named habitName (pick your own habit name) limit of 3 habits\n**$success**: marks success for the day for all habits \n**$fail**: marks fail for the day for all habits \n**$unmark**: unmarks the day for all habits \n**$sModify** 3 9 6: marks success for the 3rd 9th and 6th (pick your own numbers)\n**$fModify** 3 9 6: marks fail for the 3rd 9th and 6th (pick your own numbers)\n**$uModify** 3 9 6: unmarks the 3rd 9th and 6th (pick your own numbers\n**$advanceMonth**: restarts calendar to the new month\n**$myCal**: prints out your calendar")
    
  if msg.startswith('$delData'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    db[userName] = [memName, defaultCal, 0, "No name"]
    retrieve_data(userName)
    await message.channel.send("Erased your data!")

  if msg.startswith('$Testing'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    if month_change(userName):
      await message.channel.send("New month detected, restart calendar?Send Y for yes and N for no.")
      sameAuthor = False
      while sameAuthor == False:
        msg2 = await client.wait_for("message")
        if str(memName) == str(msg2.author):
          string = '{0.content}'.format(msg2)
          sameAuthor = True
      if string.upper() == "Y":
        await message.channel.send("Restarted!")
      else:
        await message.channel.send("Okay! Your calendar wasn't restarted. If you ever would like to go to the next month, just type $advanceMonth")

  if msg.startswith('$exampleWait'):
    await message.channel.send("Which habit would you like to change?")
    sameAuthor = False
    while sameAuthor == False:
      msg2 = await client.wait_for("message")
      if str(memName) == str(msg2.author):
        string = '{0.content}'.format(msg2)
        sameAuthor = True
    await message.channel.send(memName + " said " + string)
    
  if msg.startswith('$keys'):
    
    keys = db.keys()
    await message.channel.send(list(keys))

  if msg.startswith('$daTesting2'):
    db["test@"] = "value"
    db["test<"] = "value"
    db["test3"] = "value"
    #db["test#"] = "value"

    value1 = db["test@"]
    value2 = db["test<"]
    value3 = db["test3"]
    #value4 = db["test#"]

    value = db[value1]
    print (value)

    value = db[value2]
    print (value)

    value = db[value3]
    print (value)

    #value = db[value4]
    #print (value)
    await message.channel.send("Done!")

  if msg.startswith('$addData'):
    if memName == "CinnamonToast <3#9606":
      dataToAdd = msg.split("|", 2) # $addData, memName, habit
      memName = dataToAdd[1]
      global habitName
      habitName = dataToAdd[2]
      calVal = clean_initialize_cal()
      userName = ""
      if " " in memName:
        userName = memName.replace(" ", "@")
        userName = userName.replace("#", "@")
      else:
        userName = memName.replace("#", "@")
      db[userName] = [memName, calVal, 0, habitName]
      retrieve_data(userName)
      await message.channel.send("Done!")
    else:
      await message.channel.send("You don't have permission to do that!")

  if msg.startswith('$printData'):
    if len (str(calData))>1999:
      await message.channel.send(str(calData)[0:1999])
      await message.channel.send(str(calData)[1999:])
    else:
      await message.channel.send(calData)

  if msg.startswith('$calendarSurgery'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    command = msg.split(" ")
    if len(command) != 2 and db[userName][3] != "Multiple":
      await message.channel.send("Enter one command after $calendarSurgery please! Example: $calendarSurgery r3")

    elif len(command) != 3 and db[userName][3] == "Multiple":
      await message.channel.send("Enter one command and/or a habit name after $calendarSurgery please! Example: $calendarSurgery r3 Reading")

    else:
      if db[userName][3] != "Multiple":
        command = msg.split(" ")[1]
        fixedCal = []
        n = 0
        for t in myCal:
          if n != int(command[1]):
            fixedCal.append(t)
          else:
            if command[0] == "r":
              fixedCal.append(" ")
            elif command[0] == "s":
              fixedCal.append("✓")
            elif command[0] == "f":
              fixedCal.append("x")
            elif command[0] == "u":
              fixedCal.append(".")
            else:
              fixedCal.append(t)
          n += 1
        startIndex = db[userName][2]
        db[userName] = [memName, fixedCal, startIndex, habitName]
        retrieve_data(userName)
        
      else:
        command = msg.split(" ")[1]
        habitUndergoer = msg.split(" ")[2]
        fixedCal = []
        n = 0
        for t in myCal[habitUndergoer]:
          if n != int(command[1]):
            fixedCal.append(t)
          else:
            if command[0] == "r":
              fixedCal.append(" ")
            elif command[0] == "s":
              fixedCal.append("✓")
            elif command[0] == "f":
              fixedCal.append("x")
            elif command[0] == "u":
              fixedCal.append(".")
            else:
              fixedCal.append(t)
          n += 1
        myCal[habitUndergoer] = fixedCal
        db[userName] = [memName, myCal, startIndex, habitName]
        retrieve_data(userName)

      await message.channel.send("Performed the surgery!")

  if msg.startswith('$retrieveData'):
    if memName == "CinnamonToast <3#9606":
      retrieve_data(memName)
    else:
      await message.channel.send("You don't have permission to do that!")

  if msg.startswith('$pd2'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    value = db[userName]
    #await message.channel.send(value)
    val = db[userName]
    val = str(val).replace("[[", "[")
    val = str(val).replace("]]", "]")
    await message.channel.send(val)

  if msg.startswith('$date'):
    await message.channel.send(today)

  if msg.startswith('$time'):
    theTime = str(datetime.datetime.now(tz))[11:16]
    if int(theTime[0:2]) > 12:
      newTime = str(int(theTime[0:2]) - 12) + theTime [2:5] + " PM"
    else:
      newTime = theTime + " AM"
    print (theTime)
    await message.channel.send(newTime)

  if msg.startswith('$sentBy'):
    await message.channel.send(message.author)

  if msg.startswith('$checkIndex'):
    await message.channel.send(startIndex)

  if msg.startswith('$calName'):
    global calName
    await message.channel.send(calName)

  if msg.startswith('$advanceMonth'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    startIndex = weekDay + 1
    newCal = clean_initialize_cal()
    if db[userName][3] != "Multiple":
      db[userName] = [userName, newCal, startIndex, habitName]
    else:
      newCal = clean_initialize_cal()
      for key in db[userName][1]:
        myCal[key] = newCal
      db[userName] = [userName, myCal, startIndex, habitName]
    await message.channel.send("Intialized New Calender! Now type $myCal" + " ")

  if msg.startswith('$addHabit'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    end = len(memName) - 5
    calName = (memName[slice(end)]) + "'s Accountability Calendar"
    habitDict = {}
    if habitName == "No name":
      habitList = msg.split(" ", 10)
      if len(habitList) > 2:
        initialize_cal()
        for a in range(1, len(habitList)):
          newHabit = ""
          habit = habitList[a]
          newHabit = habit[0].upper() + habit[1:]
          habitDict[newHabit] = myCal

          
          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")

          db[userName] = [memName, habitDict, startIndex, "Multiple"]
        await message.channel.send("Intialized Your Calender! Now type $myCal" + " ")


      if len(habitList) == 2:
        habit = msg.split(" ", 1)[1]

        if len(habit) > 1:
          initialize_cal()
          newHabit = ""
          newHabit = habit[1]
          newHabit = habit[0].upper() + habit[1:]
          calData.append([memName, myCal, startIndex, newHabit])

          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")

          db[userName] = [memName, myCal, startIndex, newHabit]
          await message.channel.send("Intialized Your Calender! Now type $myCal" + " ")
        else:
          await message.channel.send("Add a habit! Type $addHabit HabitGoesHere" + " ")
    else:
      await message.channel.send("There is already a habit in place! Would you like to add another habit? Send Y for yes or N for no.")
      choice = await client.wait_for("message")
      choice = '{0.content}'.format(choice)
      if choice.upper() == "Y":
        habitList = msg.split(" ", 10)
        if len(habitList) > 2:
          if habitName == "Multiple":
            await message.channel.send("Performing habit add with numerous habits")
            initialize_cal()
            for a in range(1, len(habitList)):
              newHabit = ""
              habit = habitList[a]
              newHabit = habit[0].upper() + habit[1:]
              habitDict[newHabit] = myCal

              if " " in memName:
                userName = memName.replace(" ", "@")
                userName = userName.replace("#", "@")
              else:
                userName = memName.replace("#", "@")

              db[userName] = [memName, habitDict, startIndex, "Multiple"]
              await message.channel.send("Intialized Your Calender! Now type $myCal" + " ")
          else:
            await message.channel.send("Performing habit add with 1 habit")
            habitDict[habitName] =  myCal
            calVal = clean_initialize_cal()
            for a in range(1, len(habitList)):
              newHabit = ""
              habit = habitList[a]
              newHabit = habit[0].upper() + habit[1:]
              habitDict[newHabit] = calVal

            if " " in memName:
              userName = memName.replace(" ", "@")
              userName = userName.replace("#", "@")
            else: 
              userName = memName.replace("#", "@")
            db[userName] = [memName, habitDict, startIndex, "Multiple"]

            await message.channel.send("Intialized Your Calender! Now type $myCal" + " ")
        
        elif len(habitList) == 2:
          '''
          if habitName == "Multiple":
            await message.channel.send("Performing habit add 1 habit with numerous habits")
            habit = msg.split(" ", 1)[1]
            clean_initialize_cal

          else:
            '''
          await message.channel.send("Performing habit add 1 habit with 1 habit")
          if habitName != "Multiple":
            habitDict[habitName] =  myCal
          else:
            for key, value in myCal.items():
              habitDict[key] = value
          habit = msg.split(" ", 1)[1]
          if len(habit) > 1:
            newHabit = ""
            newHabit = habit[1]
            newHabit = habit[0].upper() + habit[1:]
            calVal = clean_initialize_cal()
            
            habitDict[newHabit] = calVal

            if " " in memName:
              userName = memName.replace(" ", "@")
              userName = userName.replace("#", "@")
            else:
              userName = memName.replace("#", "@")
            db[userName] = [memName, habitDict, startIndex, "Multiple"]
            await message.channel.send("Intialized Your Calender! Now type $myCal" + " ")
        else:
          await message.channel.send("Add a habit! Type $addHabit HabitGoesHere" + " ")

      if choice.upper() == "N":
        await message.channel.send("No habit was added. Remember, if you'd like to erase all data (including habits) you can use $delData")

  if msg.startswith("$set"):
    #db["BigBlue@5676"]=['BigBlue#5676', [' ', ' ', '✓', '✓', '✓', '✓', '✓', '✓', '✓', '✓', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 2, 'Exercise']
    await message.channel.send("Set!")

  if msg.startswith('$success'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    startIndex = db[userName][2]
    if month_change(userName):
      await message.channel.send("New month detected, restart calendar? Send Y for yes and N for no.")
      sameAuthor = False
      while sameAuthor == False:
        msg3 = await client.wait_for("message")
        if str(memName) == str(msg3.author):
          string = '{0.content}'.format(msg3)
          sameAuthor = True
      if string.upper() == "Y":
        newCal = clean_initialize_cal()
        if db[userName][3] != "Multiple":
          db[userName] = [userName, newCal, startIndex, habitName]
        else:
          newCal = clean_initialize_cal()
          for key in db[userName][1]:
            myCal[key] = newCal
          db[userName] = [userName, myCal, startIndex, habitName]
        await message.channel.send("Restarted! Now retry $success")
      else:
        await message.channel.send("Okay! Your calendar wasn't restarted. Use $sModify, $fModify, or $uModify to modify your calendar. If you ever would like to go to the next month, just type $advanceMonth")
    else:
      day = int(todayArray[2]) + startIndex - 1
      newCal = []
      habitArray = []
      n = 0
      habitArray = msg.split(" ", 15)
      if len(habitArray) > 1 and habitName == "Multiple":
        for key in myCal:
          for proposedHabit in habitArray:
            if key == proposedHabit:
              newCal = []
              n = 0
              for t in myCal[key]:
                if n != day:
                  newCal.append(t)
                else:
                  newCal.append("✓")
                n += 1
              myCal[key] = newCal
          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")
        db[userName] = [memName, myCal, startIndex, habitName]
        retrieve_data(userName)
      elif len(habitArray) == 1 and habitName == "Multiple":
        for key in myCal:
          for proposedHabit in habitArray:
            newCal = []
            n = 0
            for t in myCal[key]:
              if n != day:
                newCal.append(t)
              else:
                newCal.append("✓")
              n += 1
            myCal[key] = newCal
          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")
        db[userName] = [memName, myCal, startIndex, habitName]
        retrieve_data(userName)
      else:
        for i in myCal:
          if n != day:
            newCal.append(i)
          else:
            newCal.append("✓")
          n += 1
        if " " in memName:
          userName = memName.replace(" ", "@")
          userName = userName.replace("#", "@")
        else:
          userName = memName.replace("#", "@")
        db[userName] = [memName, newCal, startIndex, habitName]
        retrieve_data(userName)
      await message.channel.send("Recorded success for the day!")

  if msg.startswith('$sModify'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    dayArray = msg.split(" ", 35)
    startIndex = db[userName][2]
    if len(dayArray) > 1 and habitName == "Multiple":
      await message.channel.send("Which habit(s) would you like to modify the calendar for?")
      msg2 = await client.wait_for("message")
      string2 = '{0.content}'.format(msg2)
      habitRequests = string2.split(" ")
      for string in habitRequests:
        if string in myCal:
          for a in range(1, len(dayArray)):
            day = dayArray[a]
            day = int(day) + startIndex -1
            newCal = []
            n = 0
            for i in myCal[string]:
              if n != int(day):
                newCal.append(i)
              else:
                newCal.append("✓")
              n += 1
              
            myCal[string] = newCal
            if " " in memName:
              userName = memName.replace(" ", "@")
              userName = userName.replace("#", "@")
            else:
              userName = memName.replace("#", "@")
          db[userName] = [memName, myCal, startIndex, habitName]
          retrieve_data(userName)
          await message.channel.send("Recorded " + string + "!")
        else:
          await message.channel.send("No such habit: " +string)
    else:
      for a in range(1, len(dayArray)):
        day = dayArray[a]
        day = int(day) + startIndex -1
        newCal = []
        n = 0
        for i in myCal:
          if n != day:
            newCal.append(i)
          else:
            newCal.append("✓")
          n += 1
        if " " in memName:
          userName = memName.replace(" ", "@")
          userName = userName.replace("#", "@")
        else:
          userName = memName.replace("#", "@")
        db[userName] = [memName, newCal, startIndex, habitName]
        retrieve_data(userName)
      await message.channel.send("Recorded!")
  
  if msg.startswith('$fModify'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    dayArray = msg.split(" ", 35)
    startIndex = db[userName][2]
    if len(dayArray) > 1 and habitName == "Multiple":
      await message.channel.send("Which habit(s) would you like to modify the calendar for?")
      msg2 = await client.wait_for("message")
      string2 = '{0.content}'.format(msg2)
      habitRequests = string2.split(" ")
      for string in habitRequests:
        if string in myCal:
          for a in range(1, len(dayArray)):
            day = dayArray[a]
            day = int(day) + startIndex -1
            newCal = []
            n = 0
            for i in myCal[string]:
              if n != int(day):
                newCal.append(i)
              else:
                newCal.append("x")
              n += 1
              
            myCal[string] = newCal
            if " " in memName:
              userName = memName.replace(" ", "@")
              userName = userName.replace("#", "@")
            else:
              userName = memName.replace("#", "@")
          db[userName] = [memName, myCal, startIndex, habitName]
          retrieve_data(userName)
          await message.channel.send("Recorded " + string + "!")
        else:
          await message.channel.send("No such habit: " +string)
    else:
      for a in range(1, len(dayArray)):
        day = dayArray[a]
        day = int(day) + startIndex -1
        newCal = []
        n = 0
        for i in myCal:
          if n != day:
            newCal.append(i)
          else:
            newCal.append("x")
          n += 1
        if " " in memName:
          userName = memName.replace(" ", "@")
          userName = userName.replace("#", "@")
        else:
          userName = memName.replace("#", "@")
        db[userName] = [memName, newCal, startIndex, habitName]
        retrieve_data(userName)
      await message.channel.send("Recorded!")

  if msg.startswith('$uModify'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    dayArray = msg.split(" ", 35)
    startIndex = db[userName][2]
    if len(dayArray) > 1 and habitName == "Multiple":
      await message.channel.send("Which habit(s) would you like to modify the calendar for?")
      msg2 = await client.wait_for("message")
      string2 = '{0.content}'.format(msg2)
      habitRequests = string2.split(" ")
      for string in habitRequests:
        if string in myCal:
          for a in range(1, len(dayArray)):
            day = dayArray[a]
            day = int(day) + startIndex -1
            newCal = []
            n = 0
            for i in myCal[string]:
              if n != int(day):
                newCal.append(i)
              else:
                newCal.append(".")
              n += 1
              
            myCal[string] = newCal
            if " " in memName:
              userName = memName.replace(" ", "@")
              userName = userName.replace("#", "@")
            else:
              userName = memName.replace("#", "@")
          db[userName] = [memName, myCal, startIndex, habitName]
          retrieve_data(userName)
          await message.channel.send("Recorded " + string + "!")
        else:
          await message.channel.send("No such habit: " +string)
    else:
      for a in range(1, len(dayArray)):
        day = dayArray[a]
        day = int(day) + startIndex -1
        newCal = []
        n = 0
        for i in myCal:
          if n != day:
            newCal.append(i)
          else:
            newCal.append(".")
          n += 1
        if " " in memName:
          userName = memName.replace(" ", "@")
          userName = userName.replace("#", "@")
        else:
          userName = memName.replace("#", "@")
        db[userName] = [memName, newCal, startIndex, habitName]
        retrieve_data(userName)
      await message.channel.send("Recorded!")

  if msg.startswith('$fail'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    startIndex = db[userName][2]
    if month_change(userName):
      await message.channel.send("New month detected, restart calendar? Send Y for yes and N for no.")
      sameAuthor = False
      while sameAuthor == False:
        msg3 = await client.wait_for("message")
        if str(memName) == str(msg3.author):
          string = '{0.content}'.format(msg3)
          sameAuthor = True
      if string.upper() == "Y":
        newCal = clean_initialize_cal()
        if db[userName][3] != "Multiple":
          db[userName] = [userName, newCal, startIndex, habitName]
        else:
          newCal = clean_initialize_cal()
          for key in db[userName][1]:
            myCal[key] = newCal
          db[userName] = [userName, myCal, startIndex, habitName]
        await message.channel.send("Restarted! Now retry $success")
      else:
        await message.channel.send("Okay! Your calendar wasn't restarted. Use $sModify, $fModify, or $uModify to modify your calendar. If you ever would like to go to the next month, just type $advanceMonth")
    else:
      day = int(todayArray[2]) + startIndex - 1
      newCal = []
      habitArray = []
      n = 0
      habitArray = msg.split(" ", 15)
      if len(habitArray) > 1 and habitName == "Multiple":
        for key in myCal:
          for proposedHabit in habitArray:
            if key == proposedHabit:
              newCal = []
              n = 0
              for t in myCal[key]:
                if n != day:
                  newCal.append(t)
                else:
                  newCal.append("x")
                n += 1
              myCal[key] = newCal
          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")
        db[userName] = [memName, myCal, startIndex, habitName]
        retrieve_data(userName)
      elif len(habitArray) == 1 and habitName == "Multiple":
        for key in myCal:
          for proposedHabit in habitArray:
            newCal = []
            n = 0
            for t in myCal[key]:
              if n != day:
                newCal.append(t)
              else:
                newCal.append("x")
              n += 1
            myCal[key] = newCal
          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")
        db[userName] = [memName, myCal, startIndex, habitName]
        retrieve_data(userName)
      else:
        for i in myCal:
          if n != day:
            newCal.append(i)
          else:
            newCal.append("x")
          n += 1
        if " " in memName:
          userName = memName.replace(" ", "@")
          userName = userName.replace("#", "@")
        else:
          userName = memName.replace("#", "@")
        db[userName] = [memName, newCal, startIndex, habitName]
        retrieve_data(userName)
      await message.channel.send("Recorded failure for the day :(")

  if msg.startswith('$unmark'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    startIndex = db[userName][2]
    if month_change(userName):
      await message.channel.send("New month detected, restart calendar? Send Y for yes and N for no.")
      sameAuthor = False
      while sameAuthor == False:
        msg3 = await client.wait_for("message")
        if str(memName) == str(msg3.author):
          string = '{0.content}'.format(msg3)
          sameAuthor = True
      if string.upper() == "Y":
        newCal = clean_initialize_cal()
        if db[userName][3] != "Multiple":
          db[userName] = [userName, newCal, startIndex, habitName]
        else:
          newCal = clean_initialize_cal()
          for key in db[userName][1]:
            myCal[key] = newCal
          db[userName] = [userName, myCal, startIndex, habitName]
        await message.channel.send("Restarted! Now retry $success")
      else:
        await message.channel.send("Okay! Your calendar wasn't restarted. Use $sModify, $fModify, or $uModify to modify your calendar. If you ever would like to go to the next month, just type $advanceMonth")
    else:
      day = int(todayArray[2]) + startIndex - 1
      newCal = []
      habitArray = []
      n = 0
      habitArray = msg.split(" ", 15)
      if len(habitArray) > 1 and habitName == "Multiple":
        for key in myCal:
          for proposedHabit in habitArray:
            if key == proposedHabit:
              newCal = []
              n = 0
              for t in myCal[key]:
                if n != day:
                  newCal.append(t)
                else:
                  newCal.append(".")
                n += 1
              myCal[key] = newCal
          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")
        db[userName] = [memName, myCal, startIndex, habitName]
        retrieve_data(userName)
      elif len(habitArray) == 1 and habitName == "Multiple":
        for key in myCal:
          for proposedHabit in habitArray:
            newCal = []
            n = 0
            for t in myCal[key]:
              if n != day:
                newCal.append(t)
              else:
                newCal.append(".")
              n += 1
            myCal[key] = newCal
          if " " in memName:
            userName = memName.replace(" ", "@")
            userName = userName.replace("#", "@")
          else:
            userName = memName.replace("#", "@")
        db[userName] = [memName, myCal, startIndex, habitName]
        retrieve_data(userName)
      else:
        for i in myCal:
          if n != day:
            newCal.append(i)
          else:
            newCal.append(".")
          n += 1
        if " " in memName:
          userName = memName.replace(" ", "@")
          userName = userName.replace("#", "@")
        else:
          userName = memName.replace("#", "@")
        db[userName] = [memName, newCal, startIndex, habitName]
        retrieve_data(userName)
      await message.channel.send("Removed marking!")

  if msg.startswith('$myCal'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    success = 0
    fail = 0

    if habitName == "Multiple":
      gradeDict = {}
      if calName == "No name":
        end = len(memName) - 5
        calName = (memName[slice(end)]) + "'s Accountability Calendar"
      calString = "```" + calName + "\n\n"
      i = 0
      for key in myCal:
        calString += key + "\nS M T W T F S\n"
        k = 0
        list2 = myCal.values()
        strList2 = str(list2)
        strList21 = strList2.replace("dict_values([", "")
        strList22 = strList21.replace("])", "")

        val = literal_eval(strList22)
        value = val[i]
        j = 0
        success = 0
        fail = 0
        for t in value:
          j = j + 1
          calString += t + " "
          if t == "✓":
            success += 1
          if t == "x":
            fail += 1
          if j == 7:
            calString += "\n"
            j = 0
          k = k + 1
        calString += "\n\n"
        i = i+1
        if (success+fail != 0):
          percentage = (str((success / (success+fail))*100))
          percentage = int((percentage.split(".", 1))[0])
          grade = "Z"
          if (percentage >= 97):
            grade = "A+"
          elif (percentage >= 93):
            grade = "A"
          elif (percentage >= 90):
            grade = "A-"
          elif (percentage >= 87):
            grade = "B+"
          elif (percentage >= 83):
            grade = "B"
          elif (percentage >= 80):
            grade = "B-"
          elif (percentage >= 77):
            grade = "C+"
          elif (percentage >= 73):
            grade = "C"
          elif (percentage >= 70):
            grade = "C-"
          elif (percentage >= 67):
            grade = "D+"
          elif (percentage >= 63):
            grade = "D"
          elif (percentage >= 60):
            grade = "D-"
          else:
            grade = "F"
        else:
            grade = "-"
        gradeDict[key] = grade
      
    else:
      if calName == "No name":
        end = len(memName) - 5
        calName = (memName[slice(end)]) + "'s Accountability Calendar"
      calString = "```" + calName + "\n\n" + habitName + "\nS M T W T F S\n"
      i = 0
      j = 0
      while i < len(myCal):
          for t in myCal:
            calString += t + " "
            i = i+1
            j = j+1
            if t == "✓":
              success += 1
            if t == "x":
              fail += 1
            if j == 7:
              calString += "\n"
              j = 0
          j = j + 1
      calString += "\n"

      if (success+fail != 0):
        percentage = (str((success / (success+fail))*100))
        percentage = int((percentage.split(".", 1))[0])
        grade = "Z"
        if (percentage >= 97):
          grade = "A+"
        elif (percentage >= 93):
          grade = "A"
        elif (percentage >= 90):
          grade = "A-"
        elif (percentage >= 87):
          grade = "B+"
        elif (percentage >= 83):
          grade = "B"
        elif (percentage >= 80):
          grade = "B-"
        elif (percentage >= 77):
          grade = "C+"
        elif (percentage >= 73):
          grade = "C"
        elif (percentage >= 70):
          grade = "C-"
        elif (percentage >= 67):
          grade = "D+"
        elif (percentage >= 63):
          grade = "D"
        elif (percentage >= 60):
          grade = "D-"
        else:
          grade = "F"
      else:
        grade = "-"
    
    if habitName == "Multiple":
      calString += "\nReport Card\n"
      for key, value in gradeDict.items():
        calString += key + ": " + value + "\n"
      await message.channel.send(calString + "```")
      
    else:
      await message.channel.send(calString + "\nReport Card\n" + habitName + ": " + grade + "```")

  if msg.startswith('$downloadData'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    else:
      userName = memName.replace("#", "@")
    retrieve_data(userName)
    success = 0
    fail = 0

    if habitName == "Multiple":
      gradeDict = {}
      if calName == "No name":
        end = len(memName) - 5
        calName = (memName[slice(end)]) + "'s Accountability Calendar"
      calString = calName + "\n\n"
      i = 0
      for key in myCal:
        calString += key + "\nS M T W T F S\n"
        k = 0
        list2 = myCal.values()
        strList2 = str(list2)
        strList21 = strList2.replace("dict_values([", "")
        strList22 = strList21.replace("])", "")

        val = literal_eval(strList22)
        value = val[i]
        j = 0
        success = 0
        fail = 0
        for t in value:
          j = j + 1
          calString += t + " "
          if t == "✓":
            success += 1
          if t == "x":
            fail += 1
          if j == 7:
            calString += "\n"
            j = 0
          k = k + 1
        calString += "\n\n"
        i = i+1
        if (success+fail != 0):
          percentage = (str((success / (success+fail))*100))
          percentage = int((percentage.split(".", 1))[0])
          grade = "Z"
          if (percentage >= 97):
            grade = "A+"
          elif (percentage >= 93):
            grade = "A"
          elif (percentage >= 90):
            grade = "A-"
          elif (percentage >= 87):
            grade = "B+"
          elif (percentage >= 83):
            grade = "B"
          elif (percentage >= 80):
            grade = "B-"
          elif (percentage >= 77):
            grade = "C+"
          elif (percentage >= 73):
            grade = "C"
          elif (percentage >= 70):
            grade = "C-"
          elif (percentage >= 67):
            grade = "D+"
          elif (percentage >= 63):
            grade = "D"
          elif (percentage >= 60):
            grade = "D-"
          else:
            grade = "F"
        else:
            grade = "-"
        gradeDict[key] = grade
      
    else:
      if calName == "No name":
        end = len(memName) - 5
        calName = (memName[slice(end)]) + "'s Accountability Calendar"
      calString = calName + "\n\n" + habitName + "\nS M T W T F S\n"
      i = 0
      j = 0
      while i < len(myCal):
          for t in myCal:
            calString += t + " "
            i = i+1
            j = j+1
            if t == "✓":
              success += 1
            if t == "x":
              fail += 1
            if j == 7:
              calString += "\n"
              j = 0
          j = j + 1
      calString += "\n"
      if (success+fail != 0):
        percentage = (str((success / (success+fail))*100))
        percentage = int((percentage.split(".", 1))[0])
        grade = "Z"
        if (percentage >= 97):
          grade = "A+"
        elif (percentage >= 93):
          grade = "A"
        elif (percentage >= 90):
          grade = "A-"
        elif (percentage >= 87):
          grade = "B+"
        elif (percentage >= 83):
          grade = "B"
        elif (percentage >= 80):
          grade = "B-"
        elif (percentage >= 77):
          grade = "C+"
        elif (percentage >= 73):
          grade = "C"
        elif (percentage >= 70):
          grade = "C-"
        elif (percentage >= 67):
          grade = "D+"
        elif (percentage >= 63):
          grade = "D"
        elif (percentage >= 60):
          grade = "D-"
        else:
          grade = "F"
      else:
        grade = "-"

    detectedMonth = month_detection(userName)
    if (detectedMonth == 1):
      detectedMonth = "January"
    elif (detectedMonth == 2):
      detectedMonth = "February"
    elif (detectedMonth == 3):
      detectedMonth = "March"
    elif (detectedMonth == 4):
      detectedMonth = "April"
    elif (detectedMonth == 5):
      detectedMonth = "May"
    elif (detectedMonth == 6):
      detectedMonth = "June"
    elif (detectedMonth == 7):
      detectedMonth = "July"
    elif (detectedMonth == 8):
      detectedMonth = "August"
    elif (detectedMonth == 9):
      detectedMonth = "September"
    elif (detectedMonth == 10):
      detectedMonth = "October"
    elif (detectedMonth == 11):
      detectedMonth = "November"
    elif (detectedMonth == 12):
      detectedMonth = "December"

    if habitName == "Multiple":
      calString += "\nReport Card\n"
      for key, value in gradeDict.items():
        calString += key + ": " + value + "\n"
      
      #calString += calString 
      
    else:
      calString += "\nReport Card\n" + habitName + ": " + grade 

    fileName = detectedMonth +str(todayArray[0]) + "_HU" + ".txt"

    buf = io.BytesIO(calString.encode())
    f = discord.File(buf,     filename=fileName)
    await message.channel.send("Your file is:", file=f)



keep_alive()
my_secret = os.environ['theKey']
client.run(my_secret)

'''
--------------------------------------------------
global myCal
global numDaysInMonth
global weekDay
numDaysInMonth = 0
weekDay = 0
myCal = []
'''

'''
  while ran != 1:
    if h == -1:
      break
    if calData[h-1][0] == senderName:
      myCal = calData[h-1][1]
      habitName = calData[h-1][3]
      calName = "No name"
      ran = 1
      if " " in senderName:
        senderName = senderName.replace(" ", "@")
        senderName = senderName.replace("#", "@")
      db[senderName] = calData

    else:
      h -= 1
  if ran != 1:
      calData.append([senderName, defaultCal, 0, "No name"])
      myCal = defaultCal
      habitName = "No name"
      calName = "No name"
      if " " in senderName:
        senderName = senderName.replace(" ", "@")
        senderName = senderName.replace("#", "@")
      db[senderName] = calData
'''


'''
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
'''

'''
    with open(fileName, "w") as file:
        file.write(calString)
    
    # send file to Discord in message
    with open(fileName, "rb") as file:
        await message.channel.send("Your file is:", file=discord.File(file, fileName))
'''