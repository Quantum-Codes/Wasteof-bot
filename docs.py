"""efficient binary search WIP
def search(target, list1, start): #my style binary search B)
  approx = target//(list1[-1] / len(list)) #assuming the list increases uniformly
  if list1[approx] > target:
    x = search(target, list1)
"""

def search(target, list1):
  for item in list1:
    if item > target:
      return list1.index(item) #item with  len just more than limit
  return len(list1) -1 #last index

def splitter(message, lim):
  doc = message.split("\n")
  lengths = [len(item) + 9 for item in doc] #9 is length of </p>\n<p>
  added_lengths = [0]
  for item in lengths:
    added_lengths.append(added_lengths[-1] + item)
  added_lengths.pop(0)
  #print("Lengths: ", lengths,  "\nAdded: ", added_lengths)
  x = []
  if added_lengths[-1] < lim: #if splitting not needed, simply return
    return "<p>\n</p>".join(doc)

  for i in range(1,added_lengths[-1]//lim +2): #start from 1 cuz first loop must have lim×1. Formula: total_len//lim +1 repetitions. add 1 to it cuz python excludes max limit in for
    x.append(search(lim*i, added_lengths))
  x.append(None)
  #print("Split Index:", x)
  messages = ["</p>\n<p>".join(doc[x[index-1]:item]) for index,item in enumerate(x)]
  return messages


def docs(temp):
  if temp == "wob":
    message = """<p>hi. I am a bot.
<u><b>Commands:</b></u>
●`wob joke` to hear a <b>joke</b>
●`wob coinflip` to <b>flip a coin</b>
●`wob track` to let me <b>track your stats</b>
●`wob rolldice [faces]` to <b>roll a dice</b>. If `faces` isn't given, it defaults to 6
●`wob avatar [user]` to get the user's <b>profile picture</b>. If `user` isn't given, it gives your avatar/profile pic
●`wob banner [user]` to get the user's <b>banner</b>. If `user` isn't given, it gives your banner
●`wob stats [user]` to get the user's <b>statistics</b>. If `user` isn't given, it gives your stats
●`wob graph [user]` to get the user's <b>statistics graphs</b>. If `user` isn't given, it gives your own graphs. If `user` is "all", then you get all of wasteofs graphs in one single image!
<i>These are the only commands I have for now. Suggest commands on my wall.</i>
</p>"""
    #message += ("\n" + "0"*100)*5
    message = splitter(message,493)
    if message[-1] == "</p>": #bruh. check for black split
      message.pop(-1)
    return message

  else:
    doc = f"""<p><p>hi. I am a bot.</p>
<p><u>Commands:</u></p><ul>
<li><code>{temp} joke</code> to hear a <b>joke</b></li>
<li><code>{temp} coinflip</code> to <b>flip a coin</b></li>
<li><code>{temp} track</code> to let me <b>track your stats</b></li>
<li><code>{temp} rolldice [faces]</code> to <b>roll a dice</b>. If <code>faces</code> isn't given, it defaults to 6</li>
<li><code>{temp} avatar [user]</code> to get the user's <b>profile picture</b>. If <code>user</code> isn't given, it gives your avatar/profile pic</li>
<li><code>{temp} banner [user]</code> to get the user's <b>banner</b>. If <code>user</code> isn't given, it gives your banner</li>
<li><code>{temp} stats [user]</code> to get the user's <b>statistics</b>. If <code>user</code> isn't given, it gives your stats</li>
<li><code>wob graph [user]</code> to get the user's <b>statistics graphs</b>. If <code>user</code> isn't given, it gives your own graphs. If <code>user</code> is "<code>all</code>", then you get all of wasteofs graphs in one single image!</li>
</ul>
<p><i>These are the only commands I have for now. Suggest commands on my wall.</i></p></p>"""
    return doc

#print(f"Result: {[len(item) for item in docs('wob')]}")