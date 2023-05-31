"""
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

"UPDATE URLLIB WHEN THE 'STRICT' ERROR WITH POETRY GETS FIXED https://stackoverflow.com/questions/76175361/firebase-authentication-httpresponse-object-has-no-attribute-strict-status"
from docs import docs
from wasteof import api
from keep_alive import keep_alive
from replit import db
import os, random
#with open("abc", "w") as file:
#  file.write(os.environ["REPLIT_DB_URL"])
#db["users"]  = {}
db["track"] = list(set(db["track"])) #to be safe
os.system("clear")
try:
  import socketio
  from pyEventLogger import pyLogger
except ModuleNotFoundError:
  os.system("pip install python-socketio[client] pyEventLogger")
  import socketio
  from pyEventLogger import pyLogger

if not "REPL_SLUG" in os.environ:
  import dotenv
  dotenv.load_dotenv()

  


sio = socketio.Client(logger=True)
log = pyLogger(colored_output=True, make_file=True)

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

def preferences(comment, user, prefix):
  pointer = api.get_preferences(user)
  if "beta" in comment:
    pointer["site"] = "beta"
  elif "prod" in comment:
    pointer["site"] = "prod"

  if "light" in comment:
    pointer["theme"] = "light"
  elif "dark" in comment:
    pointer["theme"] = "dark"

  response = f"Set {user['name']}'s preferences as:\n<b>Site:</b> {pointer['site']}\n<b>Theme:</b> {pointer['theme']}"
  #if prefix == "wob":
  response = response.replace("\n", "</p>\n<p>")
  return response



def respond(messages):
  for item in messages:
    if not item["type"] in allowed_types:
      continue 
    if item["type"] == "chat":
      prefix = api.prefix
    else:
      prefix = "@wasteof_bot"
    response = docs(api.noping(prefix))
    
    if item["type"] == allowed_types[3]:
      client = item["from"]
      comment = item["content"].strip().split()
    else:
      client = item["data"]["actor"]
      comment = item["data"][item["type"].split("_")[-2]]["content"][3:-4].strip().split()
    comment = [i.lower() for i in comment]
    if comment[0] == "@wasteof_bot" or (item["type"]==allowed_types[3] and comment[0]==api.prefix):
      tempo = "COMMAND"
      if item["type"] == allowed_types[3]:
        tempo = "CHAT"
      log.info(message= f"{tempo} - {client['name']} {client['id']} - {comment}")
      del tempo
    if "|" in comment:
      comment = comment[:comment.index("|")]
    if len(comment) > 1:
      if comment[0] == api.prefix:
        comment[0] = "@wasteof_bot"
      print(comment)
      if comment[1] == "joke":
        response = api.joke()
      elif comment[1].isdigit():
        response = "muck" #"0"*int(comment[1])
      elif comment[1] == "online":
        response = "yep"
      elif comment[1] == "coinflip":
        response = randomroll(comment, 1, 10, "coin")
      elif comment[1] == "rolldice":
        response = randomroll(comment, 6, 1000000000000000, "dice")
      elif comment[1] == "prefer":
        response = preferences(comment, client, prefix)

      elif comment[1] == "randompost":
        beta = ""
        if len(comment) > 2 or api.get_preferences(client, "site") == "beta":
          beta = "beta."
        response = f"https://{beta}wasteof.money/posts/{api.random_post()['_id']}"
      elif comment[1] == "graph":
        if len(comment) == 2: #wob graph
          response = api.image(client, prefix)
        else:
          if comment[2] == "all":
            response = api.image("all", prefix, actual=client)
          else:
            existence = api.raw_user(comment[2])
            if existence.get("id"):
              response = api.image(existence, prefix, actual=client)
            else:
              response = "That user doesn't even exist."
      elif comment[1] == "avatar" or comment[1] == "banner":
        prefix = comment[1].replace("avatar","picture")
        insert_user(comment, item)
        if api.user_exists(comment[2]):
          response = f"<img src='https://api.wasteof.money/users/{comment[2]}/{prefix}'>"
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
      elif comment[1] == "recents":
        if len(comment) > 2 or api.get_preferences(client, "site") == "beta":
          response = api.recent_posts(prefix, True)
        else:
          response = api.recent_posts(prefix, False)

      elif "drama" in comment[1]:
        response = "A wise man once said:\n<img src='https://i.ibb.co/QpQdCdP/1019993439028383784-1.webp'>"

    else:
      print("No command given. Docs sent")

    if comment[0] == "@wasteof_bot" or (item["type"]==allowed_types[3] and comment[0]==api.prefix):
      if item["type"] == allowed_types[0]:
        req = api.wall_reply(item["data"]["comment"]["wall"]["name"], item["data"]["comment"]["_id"], response)
        if req:
          if req.status_code == 200:
            log.success(message=f"COMMAND WALL - Response sent to {client['name']} {client['id']}")
          else:
            log.critical(message=f"COMMAND WALL - ResponseError {req.status_code} {client['name']} {client['id']}")
        else:
          log.success(message=f"COMMAND WALL <ignored> {client['name']} {client['id']}")

      elif item["type"] == allowed_types[1]:
        req = api.post_reply(item["data"]["post"]["_id"], response)
        if req:
          if req.status_code == 200:
            log.success(message=f"COMMAND POST - Response sent to {client['name']} {client['id']}")
          else:
            log.critical(message=f"COMMAND POST - ResponseError {req.status_code} {client['name']} {client['id']}")
        else:
          log.success(message=f"COMMAND POST <ignored> {client['name']} {client['id']}")

      elif item["type"] == allowed_types[2]:
        req = api.post_reply(item["data"]["post"]["_id"], response, item["data"]["comment"]["_id"])
        if req:
          if req.status_code == 200:
            log.success(message=f"COMMAND POST_REPLY - Response sent to {client['name']} {client['id']}")
          else:
            log.critical(message=f"COMMAND POST_REPLY - ResponseError {req.status_code} {client['name']} {client['id']}")
        else:
          log.success(message=f"COMMAND POST_REPLY <ignored> {client['name']} {client['id']}")

      elif item["type"] == allowed_types[3]:
        if type(response) is list:
          for item1 in response:
            sio.emit("message", "<p>"+item1+"</p>")
            log.success(message=f"doc msg {len(item1)}")
        else:
          sio.emit("message", "<p>"+response+"</p>")
        log.success(message=f"CHAT - Response sent to {client['name']} {client['id']} with len {len(response) + 7}")


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
    message = api.read_message().json()["unread"][:messages]
    try:
      respond(message)
    except Exception as e:
      print(e)
      log.error(True)


@sio.on('message')
def on_mesage(data):
  #sio.emit("redirect", "https://wasteof.money/")
  data["type"] = "chat"
  data = (data,)
  try:
    respond(data)
  except Exception as e:
    print(e)
    log.error(True, message=f"CHAT ERROR - {data[0]['content']}\n DATA: {data[0]}")

"""
@sio.on('redirect')
def on_redirect(url):
  sio.emit("message", f"Users redirected to {url}")
  log.success(message=f"CHAT - REDIRECT DETECTED {url}")
"""

@sio.event
def connect():
  print("I'm connected!")

sio.connect("https://api.wasteof.money/", auth= {"token":api.token})

keep_alive()
