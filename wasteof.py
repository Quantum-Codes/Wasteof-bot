import requests, os

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
    post = requests.post(f"https://api.wasteof.money/posts",headers = {"Authorization": self.token},json={"post": post, "repost":id})
    print(post.json())
    return post

  def post(self, post):
    post = requests.post(f"https://api.wasteof.money/posts",headers = {"Authorization": self.token},json={"post": post})
    print(post.json())
    return post

#token = login()
#repostit("278fd7b182958jgugigyvhfgdhfycubibuctsrarsygjvgfu8")


#repostitpostit("61f91ca18bfdf1073c6df1c4")
#test()
