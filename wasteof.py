import requests, os, json

class api:
  def __init__(self):
    self.login()
    
  def login(self):
    user = os.environ["User"]
    passw = os.environ["passw"]
    data = {"username":user, "password":passw}
    token = requests.post("https://api.wasteof.money/session",  json=data).json()["token"]
    print("logged in!")
    self.token = token

  def repost(self, id, post):
    post = requests.post("https://api.wasteof.money/posts",headers = {"Authorization": self.token},json={"post": post, "repost":id})
    print(post.json())
    return post

  def post(self, post):
    post = requests.post("https://api.wasteof.money/posts",headers = {"Authorization": self.token},json={"post": post})
    print(post.json())
    return post

  def read_message(self):
    messages = requests.get("https://api.wasteof.money/messages/unread",headers = {"Authorization": self.token})
    return messages

  def wall_reply(self, user, id, post):
    post = requests.post(f"https://api.wasteof.money/users/{user}/wall",headers = {"Authorization": self.token},json={"content": post, "parent":id})
    #print(post,"\n", vars(post))
    print(post.json())
    return post

  def post_reply(self, id, post, parent_id=None):
    post = requests.post(f"https://api.wasteof.money/posts/{id}/comments",headers = {"Authorization": self.token},json={"content": post, "parent": parent_id})
    #print(post,"\n", vars(post))
    print(post.json())
    return post


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
      return f"{x['setup']}<p></p>{x['delivery']}"


#token = login()
#repostit("278fd7b182958jgugigyvhfgdhfycubibuctsrarsygjvgfu8")


#repostitpostit("61f91ca18bfdf1073c6df1c4")
#test()
