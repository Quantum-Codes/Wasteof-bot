import requests, os, json, time, random
from db import database
from replit import db


db_temp = database()

class api:
  def __init__(self):
    self.prefix = "wob"
    self.login()
    self.header = {"User-Agent":"@wasteof_bot by @Ankit_Anmol | Contact on wasteof-@ankit_anmol on github-@Quantum-Codes on discord(you have)", "Authorization": self.token}

  def login(self):
    user = os.environ["User"]
    passw = os.environ["passw"]
    data = {"username":user, "password":passw}
    token = requests.post("https://api.wasteof.money/session",  json=data).json()["token"]
    print("logged in!")
    self.token = token

  def logpost(self, id):
    with open("recents.txt", "a") as file:
      file.write(f"{id}\n")

  def checkpost(self, id):
    with open("recents.txt", "r") as file:
      return (id in file.read())
  
  def repost(self, id, post):
    post = requests.post("https://api.wasteof.money/posts",headers = self.header, json={"post": post, "repost":id})
    self.logpost(id)
    print(post.json())

    return post

  def noping(self, ping):
    if "@" in ping:
      return ping[:1] + "​" + ping[1:] #zero widthspace
    return ping

  
  def post(self, post):
    post = requests.post("https://api.wasteof.money/posts",headers = self.header, json={"post": post})
    print(post.json())
    return post

  def read_message(self):
    messages = requests.get("https://api.wasteof.money/messages/unread",headers = self.header)
    return messages

  def random_post(self):
    post = requests.get("https://api.wasteof.money/random-post",headers = self.header).json()
    return post

  def get_preferences(self, user, t = None):
    if user["id"] not in db_temp:
      db_temp.new_user(user["id"])
      preferences = {"site": "prod", "theme":"dark"}
    else:
      data = db_temp.execute("SELECT beta, dark FROM wasteof WHERE userid = %s;", (user["id"],))[0]
      preferences = {
        "site": "beta" if data[0] else "prod",
        "theme":"dark" if data[1] else "light"
      }
    db["users"].setdefault(user["id"], {"site": "prod", "theme":"dark"}) #set value if not exists 
    preference = db["users"][user["id"]]
    if t:
      return preference[t]
    return preference

  def wall_reply(self, user, id, post):
    if self.checkpost(id):
      return
    post = requests.post(f"https://api.wasteof.money/users/{user}/wall",headers = self.header, json={"content": post, "parent":id})
    #print(post,"\n", vars(post))
    self.logpost(id)
    print(post.json())
    return post

  def post_reply(self, id, post, parent_id=None):
    if parent_id:
      if self.checkpost(parent_id):
        return
      self.logpost(parent_id)
    elif self.checkpost(id):
      return
    else:
      self.logpost(id)
    post = requests.post(f"https://api.wasteof.money/posts/{id}/comments",headers = self.header, json={"content": post, "parent": parent_id})
    #print(post,"\n", vars(post))
    print(post.json())
    return post

  def wall_post(self, user, post):
    post = requests.post(f"https://api.wasteof.money/users/{user}/wall",headers = self.header, json={"content": post})
    #print(post,"\n", vars(post))
    print(post.json())
    return post
  def raw_user(self, user):
    post = requests.get(f"https://api.wasteof.money/users/{user}",  headers= self.header)
    post = post.json()
    return post
    
  def user_online(self, user):
    return self.raw_user(user).get("online", None) #error key may also come up

  def user_exists(self, user):
    post = requests.get(f"https://api.wasteof.money/username-available?username={user}",  headers=self.header).json()
    r = 1 - post.get("available", True)
    return bool(r)

  def _stats(self, id):
    user = requests.get(f"https://api.wasteof.money/username-from-id/{id}",  headers=self.header).json()["username"]
    post = requests.get(f"https://api.wasteof.money/users/{user}",  headers=self.header).json()["stats"]
    post["user"] = user
    return post
  
  def stats(self, user):
    emoji = ("🔴", "🟢", "","✅","","🛡","","🚫","","🧪")
    #1print(user)
    post = requests.get(f"https://api.wasteof.money/users/{user}",  headers=self.header)
    #print(post)
    post = post.json()
    if post.get("error"):
      return "User doesnt exist"
    #print(post)
    res = f"""<p><b>{user}</b> {emoji[post["online"]]} {emoji[post["verified"]+2]} {emoji[post["permissions"]["admin"]+4]} {emoji[post["beta"]+8]} {emoji[post["permissions"]["banned"]+6]}</p>
<p><b>ID:</b>        {post["id"]}</p>
<p><b>Bio:</b>       {post["bio"]}</p>
<p><b>Followers:</b> {post["stats"]["followers"]}</p>
<p><b>Following:</b> {post["stats"]["following"]}</p>
<p><b>Posts:</b>     {post["stats"]["posts"]}</p>
"""

    if post.get("history"):
      joining = (int(time.time()) - int(post["history"]["joined"]/1000))//(24*3600)
      jointype = "days"
      if joining >= 30:
        joining //= 30
        jointype = "months"
        if joining >= 12:
          joining = int(joining*100 / 12)/100
          jointype = "years"
      res += f"""<p><b>Joined:</b>    {time.strftime('%d-%m-%Y', time.gmtime(int(post["history"]["joined"]/1000)))} ({joining} {jointype} ago)</p>"""

    return res

  def joke(self):
    x = requests.get("https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun,Christmas?blacklistFlags=nsfw,racist,sexist,explicit")
    s = x.status_code
    if s != 200:
      return f"An error has occurred. please try again later{s}"

    x = x.json()
    if x["error"] == True:
      return f"An error has occurred. please try again later. Error code {json.dumps(x)}"
    if x["type"] == "single":
      return x["joke"]
    else:
      return f"{x['setup']}</p>\n<p>{x['delivery']}"

  def image(self, user, prefix, actual=None): #actual is set when the client searches for graph other than his own
    if user == "all":
      user = {"name": "Overall wasteof", "id":"Wasteof"}
      theme = self.get_preferences(actual, "theme")
    elif actual:
      theme = self.get_preferences(actual, "theme")     
    else:
      theme = self.get_preferences(user, "theme")

    userid = user["id"]
    if userid in db["track"] or (userid == "Wasteof"):
      x = requests.get("https://raw.githubusercontent.com/Quantum-Codes/Wob-Graphs/main/url.json").json()
      match = [(key[key.index("-")+1:-4], value) for key, value in x.items() if key.startswith(f"{theme}_{userid}-")]
      if len(match) == 0:
        y = ""
        if actual:
          y = f" for {user['name']}"
        return f"No graphs to show currently{y}. Return back at the start of next week."
      match = dict(match)
    else:
      y = "You"
      if actual:
        return f"{user['name']} didnt use <code>{self.noping(prefix)} track</code>."
      return f"{y} didnt use <code>{self.noping(prefix)} track</code>. Use it to allow me track you. Return back for a graph next week since data is collected every week."

    tip = f"<blockquote>Tip: Use \"{self.noping(prefix)} graph all\" for graph of all opted-in users</blockquote>"
    if random.randint(0,1) or userid=="Wasteof":
      opp_theme = "dark" if theme=="light" else "light"
      tip = f"<blockquote>Tip: Use \"{self.noping(prefix)} prefer {opp_theme}\" to see graphs in {opp_theme}mode</blockquote>"
    return f"""{tip}<p><b><h2>{user['name']}'s graphs</h2></b></p>
<p><b>Posts:</b><img src=\"{match["posts"]}\"></p>
<p><b>Followers:</b><img src=\"{match["followers"]}\"></p>
<p><b>Following:</b><img src=\"{match["following"]}\"></p>
<p>Note: To stop tracking, you have to use <code>{self.noping(prefix)} track</code>. However, for data deletion, contact Ankit_Anmol on wasteof.</p>
"""
  def recent_posts(self, prefix, beta=False):
    z= time.time()
    users = ["ratio", "zu"]
    url = "https://api.wasteof.money/users/{user}/following/posts"
    all_posts = set()
    for item in users:
      x = requests.get(url.format(user=item), headers=self.header).json()["posts"]
      #print(f"{item}: {len(x)}")
      x = [json.dumps(i) for i in x]
      all_posts = all_posts.union(set(x))
    
    def timestamp_key(thedict):
      return thedict["time"]
    z = time.time() - z
    y = time.time()
    all_posts = [json.loads(item) for item in all_posts]
    all_posts = sorted(all_posts, key = timestamp_key,  reverse=True)[:15]
    if beta:  beta = "beta."
    else:  beta = ""
    url = 'https://{beta}wasteof.money/posts/{id}'
    all_posts = [url.format(id=item["_id"], beta=beta) for item in all_posts]
    y = time.time() - y
    if prefix == "wob":
      return "<b>Recent posts:</b><ul><li>" + "</li><li>".join(all_posts[:7]) + "</li></ul>"
    else:
      return "<b>Recent posts:</b><ol><li>" + "</li><li>".join(all_posts) + "</li></ol>"
