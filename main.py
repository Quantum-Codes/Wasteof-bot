from wasteof import api
from keep_alive import keep_alive
from threading import Thread
from replit import db
import os, time, json

db["ping"] = []

os.system("pip install python-socketio[client]")
os.system("clear")
import socketio
sio = socketio.Client(logger=True)

api = api() #login
count = 100000
allowed_types = ("wall_comment_mention", "post_mention", "comment_mention", "chat") #maybe wall_comment.. didn't put as pinging is necessary in the bot command syntax

def cooldown(user):
  time.sleep(60)
  db["ping"].remove(user)
  print(user)

def respond(messages):
  for item in messages:
    if not item["type"] in allowed_types:
      continue
    response = "<p>hi. I am a bot.</p><p>Use `@wasteof_bot joke` to hear a joke.</p><p>Use `@wasteof_bot ping [user] to call somebody for chatting in wasteof.money/chat</p><p>That's the only command I have for now. Suggest commands on my wall.</p>"
    
  
    if item["type"] == allowed_types[3]:
      comment = item["content"].split()
    else:
      comment = item["data"][item["type"].split("_")[-2]]["content"][3:-4].split()
    comment = [i.lower() for i in comment]
    if comment[0] == api.prefix:
      comment[0] = "@wasteof_bot"
    print(comment)
    try:
      if comment[1] == "joke":
        response = api.joke()
      elif comment[1] == "ping":
        if item["type"] == "chat":
          from_user = item["from"]["name"]
        else:
          from_user = item['data']['actor']['name']
        response = f"@{from_user} is inviting you to chat on wasteof.money/chat <p></p>Don't make them wait!"
        if comment[2][0] == "@":
          comment[2] = comment[2][1:]
        to_ping_user = comment[2]
        #print(api.user_exists(to_ping_user))
        if api.user_exists(to_ping_user) and (from_user not in db["ping"]):
          api.wall_post(to_ping_user, response)
          response = "Done. Link to chat https://wasteof.money/chat"
          db["ping"].append(from_user)
          t = Thread(target = cooldown, args=(from_user,))
          t.start()
        else:
          if from_user in db["ping"]:
            response = "You are on a cooldown for 1 minute. Calm down, have patience.. Else go and have a glass of water"
          else:
            response = f"@{to_ping_user} doesn't exist."
    except IndexError:
      print("indexerror???")
      if len(comment) == 2 and comment[1] == "ping":
        if item["type"] == "chat":
          temp = api.prefix + " "
        else:
          temp = "@wasteof_bot "
        response = f"<p>who to ping? Syntax:</p><p>`{temp}ping @user`</p>"
        del temp

    if comment[0] == "@wasteof_bot" or (item["type"]==allowed_types[3] and comment[0]==api.prefix):
      if item["type"] == allowed_types[0]:
        api.wall_reply(item["data"]["comment"]["wall"]["name"], item["data"]["comment"]["_id"], response)

      elif item["type"] == allowed_types[1]:
        api.post_reply(item["data"]["post"]["_id"], response)

      elif item["type"] == allowed_types[2]:
        api.post_reply(item["data"]["post"]["_id"], response, item["data"]["comment"]["_id"])

      elif item["type"] == allowed_types[3]:
        #if comment[0][0] == api.prefix:
          #if comment[0][1:] =="joke":
            #response = api.joke()
        sio.emit("message", "<p>"+response+"</p>")






@sio.on('updateMessageCount')
def on_message(data):
  global count
  if count == 100000:
    count = data
    return None
  print('ping!')
  messages = data - count
  count = data
  print(f"{count = } {messages = }")
  if messages > 0:
    message = api.read_message().json()["unread"][0:messages]
    #with open("post.json","w") as file:
      #file.write(json.dumps(message,indent=2))
    respond(message)

@sio.on('message')
def on_message(data):
  data["type"] = "chat"
  data = (data,)
  respond(data)#data in tuple/list only

@sio.event
def connect():
  sio.emit("message","[auto message] Bot started")
  print("I'm connected!")

sio.connect("https://api.wasteof.money/", auth= {"token":api.token})
keep_alive()
