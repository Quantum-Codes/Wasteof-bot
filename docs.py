"""efficient binary search WIP
def search(target, list1, start): #my style binary search B)
  approx = target//(list1[-1] / len(list)) #assuming the list increases uniformly
  if list1[approx] > target:
    x = search(target, list1)
"""
import json


def search(target, list1):
  for item in list1:
    if item > target:
      return list1.index(item)

def splitter(message, lim):
  doc = message.split("\n")
  lengths = [len(item) for item in doc]
  added_lengths = [0]
  for item in lengths:
    added_lengths.append(added_lengths[-1] + item)
  added_lengths.pop(0)
  print(lengths, "\n", "x",  "\n", added_lengths)
  x = []
  for i in range(1,added_lengths[-1]//lim +2):
    if added_lengths[-1] > lim*i:
      x.append(search(lim*i, added_lengths))
  x.append(None)
  print(x)
  messages = ["\n".join(doc[x[index-1]:item]) for index,item in enumerate(x)]
  with open("test2.json","w") as file:
    file.write(json.dumps(messages, indent=2))



  

def docs(temp):
  if temp == "wob":
    message = """<p>hi. I am a bot.
<u><b>Commands:</b></u>
●`wob joke` to hear a <b>joke</b>
●`wob coinflip` to <b>flip a coin</b>
●`wob rolldice [faces]` to <b>roll a dice</b>. If `faces` isn't given, it defaults to 6
●`wob avatar [user]` to get the user's <b>profile picture</b>. If `user` isn't given, it gives your avatar/profile pic
●`wob banner [user]` to get the user's <b>banner</b>. If `user` isn't given, it gives your banner
●`wob stats [user]` to get the user's <b>statistics</b>. If `user` isn't given, it gives your stats
<i>These are the only commands I have for now. Suggest commands on my wall.</i>
</p>"""
    message += ("\n" + "0"*100)*5
    return splitter(message,493)

  else:
    doc = f"""<p><p>hi. I am a bot.</p>
<p><u>Commands:</u></p><ul>
<li><code>{temp} joke</code> to hear a <b>joke</b></li>
<li><code>{temp} coinflip</code> to <b>flip a coin</b></li>
<li><code>{temp} rolldice [faces]</code> to <b>roll a dice</b>. If <code>faces</code> isn't given, it defaults to 6</li>
<li><code>{temp} avatar [user]</code> to get the user's <b>profile picture</b>. If <code>user</code> isn't given, it gives your avatar/profile pic</li>
<li><code>{temp} banner [user]</code> to get the user's <b>banner</b>. If <code>user</code> isn't given, it gives your banner</li>
<li><code>{temp} stats [user]</code> to get the user's <b>statistics</b>. If <code>user</code> isn't given, it gives your stats</li>
</ul>
<p><i>These are the only commands I have for now. Suggest commands on my wall.</i></p></p>"""
    return doc

docs("wob")