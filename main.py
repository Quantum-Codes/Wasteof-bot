# CREATE REPLYING FEATURES FOR ALL THINGS IN API FOR allowed_types TUPLE 
#COPY JOKE FUNCTION OF DISCORD BOT TO wasteof.py joke()

from wasteof import api
from keep_alive import keep_alive
import os

os.system("pip install python-socketio[client]")
os.system("clear")
import socketio
sio = socketio.Client(logger=True)

api = api() #login
count = 100000
allowed_types = ("wall_comment_mention", "post_mention", "comment_mention") #maybe wall_comment.. didn't put as pinging is necessary in the bot command syntax

def respond(messages):
  for item in messages:
    if not item["type"] in allowed_types:
      continue
    comment = item["data"][item["type"].split("_")[-2]]["content"][3:-4].split()
    comment = [i.lower() for i in comment]
    print(comment)
    if comment[0] == "@wasteof_bot":
      if item["type"] == allowed_types[0]:
        api.wall_reply(item["data"]["comment"]["wall"]["name"], item["data"]["comment"]["_id"], "hi")

      elif item["type"] == allowed_types[1]:
        api.post_reply(item["data"]["post"]["_id"], "hi")







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
  print(data)

@sio.event
def connect():
  sio.emit("message","[auto message] Bot started")
  print("I'm connected!")

sio.connect("https://api.wasteof.money/", auth= {"token":api.token})
keep_alive()
