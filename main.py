"""MADE TRACKING. LATER TRANSFER track command functionality and graph making + uploading to github for cron jobs (track list in https://Wasteof-api-test.quantumcodes.repl.co/track)


TO MAKE GRAPH IN STATS COMMAND (follow + following data I same linechart)
MAYBE MAKE COMPARISON CHART VS ALL USERS

<p>
<p>Note: wherever I say “wasteof chat or “/chat“, I am referring to wasteof.money/chat</p>
<p>I’m one of the first bots to exist on this website!</p>
<p>I work on the whole site! (Including wasteof chat!)</p>
<p>Here is how to use me:</p>

<li>Use <code>{temp} joke</code> to hear a <b>joke</b>.</li>
<li>Use <code>{temp} avatar [user]</code> to get the user's <b>profile picture</b>. If <code>user</code> isn't given, it gives your avatar/profile pic.</li>
<li>Use <code>{temp} banner [user]</code> to get the user's <b>banner</b>. If <code>user</code> isn't given, it gives your banner.</li>
<li>Use <code>{temp} stats [user]</code> to get the user's <b>statistics</b>. If <code>user</code> isn't given, it gives your stats.</li>
</p>
"""
from docs import docs
from net import net
from wasteof import api
from keep_alive import keep_alive
from replit import db
import os, json, random
#"""
#db["track"] = []
#"""
prev_net = 0
os.system("pip install python-socketio[client]")
os.system("clear")
import socketio
sio = socketio.Client(logger=True)

api = api()
count = 100000
coin = ("heads, ", "tails, ")
allowed_types = ("wall_comment_mention", "post_mention", "comment_mention", "chat") #maybe wall_comment.. didn't put as pinging is necessary in the bot command syntax

def insert_user(comment, item):
  if len(comment) == 2:
    if item["type"] == allowed_types[3]:
      comment.append(item["from"]["name"])
    else:
      comment.append(item["data"]["actor"]["name"])
  elif len(comment) > 2:
    if comment[2][0] == "@":
      comment[2] = comment[2][1:]

def randomroll(comment, default, max, mode):
  response = f"You got a "
  endcoin = "!"
  coins = default
  if len(comment) == 2:
    comment.append(str(default))
  if comment[2].isdigit():
    coins = int(comment[2])
    if coins > max:
      coins = max
      if mode == "coin":
        endcoin = "! Sorry, I only have 10 coins..."
      else:
        endcoin = "! Sorry, I cannot make more than a <b>QUADRILLION</b> faces on a dice."
    if coins < 1:
      coins = 1
      if mode == "coin":
        endcoin = "! I will flip because I have 🪙s"
      else:
        endcoin = "! I have a dice and I will roll it! You can't stop me."
  if mode == "coin":
    for I in range(coins):
      response += coin[random.randint(0,1)]
    response = response[:-2] + endcoin
    return response
  else:
    return f"{response} {random.randint(1, coins)}{endcoin}" 


def respond(messages):
  global prev_net
  for item in messages:
    if not item["type"] in allowed_types:
      continue
    if item["type"] == "chat":
      temp = api.prefix
    else:
      temp = "@wasteof_bot"
    response = docs(temp)
    
    if item["type"] == allowed_types[3]:
      client = item["from"]
      comment = item["content"].strip().split()
    else:
      client = item["data"]["actor"]
      comment = item["data"][item["type"].split("_")[-2]]["content"][3:-4].strip().split()
    comment = [i.lower() for i in comment]

    if "|" in comment:
      comment = comment[:comment.index("|")]
    try:
      if comment[0] == api.prefix:
        comment[0] = "@wasteof_bot"
      print(comment)
      if comment[1] == "joke":
        response = api.joke()
      elif comment[1].isdigit():
        response = "muck"#"0"*int(comment[1])
      elif comment[1] == "coinflip":
        response = randomroll(comment, 1, 10, "coin")
      elif comment[1] == "rolldice":
        response = randomroll(comment, 6, 1000000000000000, "dice")
      elif comment[1] == "avatar" or comment[1] == "banner":
        temp = comment[1].replace("avatar","picture")
        insert_user(comment, item)
        if api.user_exists(comment[2]):
          response = f"<img src='https://api.wasteof.money/users/{comment[2]}/{temp}'>"
        else:
          response = f"{comment[2]} doesn't exist"
      elif comment[1] == "stats":
        insert_user(comment, item)
        response = api.stats(comment[2])
      elif comment[1] == "track":
        if client["id"] in db["track"]:
          index = db["track"].index(client["id"])
          db["track"].pop(index)
          response=  "You have <b>opted-out</b> for me to <s>stalk</s> track statistics. Don't complain later that I don't show your stats in graph."
        else:
          db["track"].append(client["id"])
          response = "You have <b>opted-in</b> for me to <s>stalk you</s> track your statistics. Through this, you will be able to use an upcoming feature which will show your graph of statistics in stats command."
        

    except IndexError:
      print("No command given")
      
    if comment[0] == "@wasteof_bot" or (item["type"]==allowed_types[3] and comment[0]==api.prefix):
      if item["type"] == allowed_types[0]:
        api.wall_reply(item["data"]["comment"]["wall"]["name"], item["data"]["comment"]["_id"], response)

      elif item["type"] == allowed_types[1]:
        api.post_reply(item["data"]["post"]["_id"], response)

      elif item["type"] == allowed_types[2]:
        api.post_reply(item["data"]["post"]["_id"], response, item["data"]["comment"]["_id"])

      elif item["type"] == allowed_types[3]:
        if type(response) is list:
          for item1 in response:
            sio.emit("message", "<p>"+item1+"</p>")
        else:
          #print("no list", type(response) is list)
          sio.emit("message", "<p>"+response+"</p>")

  print(net() - prev_net, "MB")
  prev_net = net()


@sio.on('updateMessageCount')
def on_message(data):
  global count
  if count == 100000:
    count = data
    return None
  messages = data - count
  count = data
  print(f"{count = } {messages = }")
  if messages > 0:
    message = api.read_message().json()["unread"][0:messages]
    #with open("post.json","w") as file:
      #file.write(json.dumps(message,indent=2))
    msg_save = message[:]
    if "jeff" in json.dumps(msg_save):
      with open("logs.txt", "a") as file:
        file.write(f"JEFF:\n{msg_save}\n\n\n-----\n\n")
    try:
      respond(message)
    except Exception as e:
      with open("logs.txt", "a") as file:
        file.write(f"Message:\n{msg_save}\n\n{e}\n-----\n\n")

@sio.on('message')
def on_mesage(data):
  data["type"] = "chat"
  print(data["from"]["name"])
  data = (data,)
  data_save = data[:]
  try:
    respond(data)#data in tuple/list only
  except Exception as e:
    with open("logs.txt", "a") as file:
      file.write(f"Chat:\n{data_save}\n\n{e}\n-----\n\n")

@sio.event
def connect():
  #sio.emit("message","@everyone , From now I will not irritate humanity by spamming when I reatarted!! I will instead finish your whole existence. For now, you may wait for extinction in peace.")
  print("I'm connected!")

sio.connect("https://api.wasteof.money/", auth= {"token":api.token})

keep_alive()
