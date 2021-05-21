import discord
import os
import requests
import json
import random
import calendar
from replit import db
from keep_alive import keep_alive
import datetime
from datetime import date
import numpy
from ast import literal_eval


#Variables
client = discord.Client()
today = date.today()
todayArray = str(today).split("-")
myCal = []
defaultCal = []
calData = []
calName = "No name"
habitName = "No name"
numDaysInMonth = 0
weekDay = 0
startIndex = 0
memName = ""
ran = 0

'''
global myCal
global numDaysInMonth
global weekDay
numDaysInMonth = 0
weekDay = 0
myCal = []
'''
month = str(todayArray[1])
if month[0] == "0":
  month = int(month[1])
numDaysInMonth = calendar.monthrange(int(todayArray[0]),month)[1]
weekDay = date(int(todayArray[0]), month, 1).weekday()
#global startIndex
startIndex = weekDay + 1


if "responding" not in db.keys():
  db["responding"] = True

#
def initialize_cal():
  

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

def retrieve_data(senderName):
  global ran
  global myCal
  global habitName
  global calName
  ran = 0
  dataBase = list(db.keys())
  h = len(dataBase)
  if " " in senderName:
        senderName = senderName.replace(" ", "@")
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
      db[senderName] = calData
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
  
  

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  #nickname = message.author
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

  if msg.startswith('$delData'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    db[userName] = [memName, defaultCal, 0, "No name"]
    retrieve_data(userName)
    await message.channel.send("Erased your data!")

  if msg.startswith('$dbTesting'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    
    value = db[userName]
    await message.channel.send(value)

    

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
      initialize_cal()
      userName = ""
      if " " in memName:
        userName = memName.replace(" ", "@")
        userName = userName.replace("#", "@")
      db[userName] = [memName, myCal, startIndex, habitName]
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
    value = db[userName]
    await message.channel.send(value)
    val = db[userName]
    val = str(val).replace("[[", "[")
    val = str(val).replace("]]", "]")
    await message.channel.send(val)

  if msg.startswith('$date'):
    await message.channel.send(today)

  if msg.startswith('$sentBy'):
    await message.channel.send(message.author)

  if msg.startswith('$calName'):
    global calName
    await message.channel.send(calName)


  if msg.startswith('$addHabit'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    end = len(memName) - 5
    calName = (memName[slice(end)]) + "'s Accountability Calendar"
    habitDict = {}
    if habitName == "No name":
      habitList = msg.split(" ", 10)
      if len(habitList) > 2:
        for a in range(1, len(habitList)):
          initialize_cal()
          newHabit = ""
          newHabit = habit[a]
          newHabit = habit[0].upper() + habit[1:]
          habitDict[]


      else:
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
          db[userName] = [memName, myCal, startIndex, newHabit]
          await message.channel.send("Intialized Your Calender! Now type $myCal" + " ")
        else:
          await message.channel.send("Add a habit! Type $addHabit HabitGoesHere" + " ")
    

  if msg.startswith('$success'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    day = int(todayArray[2]) + startIndex - 1
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
    db[userName] = [memName, newCal, startIndex, habitName]
    retrieve_data(userName)
    await message.channel.send("Recorded success for the day!")

  if msg.startswith('$sModify'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    dayArray = msg.split(" ", 35)
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
      db[userName] = [memName, newCal, startIndex, habitName]
      retrieve_data(userName)
    await message.channel.send("Recorded success for that day!")

  if msg.startswith('$fModify'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    dayArray = msg.split(" ", 35)
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
      db[userName] = [memName, newCal, startIndex, habitName]
      retrieve_data(userName)
    await message.channel.send("Recorded fail for that day :(")

  if msg.startswith('$uModify'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    dayArray = msg.split(" ", 35)
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
      db[userName] = [memName, newCal, startIndex, habitName]
      retrieve_data(userName)
    await message.channel.send("Removed markings for that day.")

  if msg.startswith('$fail'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    day = int(todayArray[2]) + startIndex - 1
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
    db[userName] = [memName, newCal, startIndex, habitName]
    retrieve_data(userName)
    await message.channel.send("Recorded failure for the day :(")

  if msg.startswith('$unmark'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    day = int(todayArray[2]) + startIndex - 1
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
    db[userName] = [memName, newCal, startIndex, habitName]
    retrieve_data(userName)
    await message.channel.send("Removed markings from the day.")

  if msg.startswith('$myCal'):
    userName = ""
    if " " in memName:
      userName = memName.replace(" ", "@")
      userName = userName.replace("#", "@")
    retrieve_data(userName)
    success = 0
    fail = 0
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
    

    await message.channel.send(calString + "\nReport Card\n" + habitName + ": " + grade + "```")

    #await message.channel.send(calString + "\nReport Card\n" + "Gym" + ": " + str(percentage)+ "%" + "```")


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
keep_alive()
my_secret = os.environ['theKey']
client.run(my_secret)

