import requests, os, json, time

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

  def repost(self, id, post):
    post = requests.post("https://api.wasteof.money/posts",headers = self.header, json={"post": post, "repost":id})
    print(post.json())
    return post

  def post(self, post):
    post = requests.post("https://api.wasteof.money/posts",headers = self.header, json={"post": post})
    print(post.json())
    return post

  def read_message(self):
    messages = requests.get("https://api.wasteof.money/messages/unread",headers = self.header)
    return messages

  def wall_reply(self, user, id, post):
    post = requests.post(f"https://api.wasteof.money/users/{user}/wall",headers = self.header, json={"content": post, "parent":id})
    #print(post,"\n", vars(post))
    print(post.json())
    return post

  def post_reply(self, id, post, parent_id=None):
    post = requests.post(f"https://api.wasteof.money/posts/{id}/comments",headers = self.header, json={"content": post, "parent": parent_id})
    #print(post,"\n", vars(post))
    print(post.json())
    return post

  def wall_post(self, user, post):
    post = requests.post(f"https://api.wasteof.money/users/{user}/wall",headers = self.header, json={"content": post})
    #print(post,"\n", vars(post))
    print(post.json())
    return post

  def user_online(self, user):
    post = requests.get(f"https://api.wasteof.money/users/{user}",  headers= self.header)
    #print(post)
    post = post.json().get("online", None) #error key may also come up
    return post

  def user_exists(self, user):
    post = requests.get(f"https://api.wasteof.money/username-available?username={user}",  headers=self.header).json()
    post = 1 - post.get("available", True)
    return bool(post)

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
    print(post)
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

