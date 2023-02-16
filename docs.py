# predicted lengths is off by 1 from actual and Idk why
def search(target, list1):
  for item in list1:
    if item > target:
      return list1.index(item) #item with  len just more than limit
  return len(list1) -1 #last index

def splitter(message, lim):
  doc = message.split("\n")
  lengths = [len(item) for item in doc] 
  added_lengths = [8] 
  for item in lengths:
    added_lengths.append(added_lengths[-1] + item + 8)#8 is length of </p>\n<p>. (\ isn't counted)
  added_lengths.pop(0)
  print("Lengths: ", lengths,  "\nAdded: ", added_lengths)
  x = []
  if added_lengths[-1]+len(added_lengths)*8  < lim: #if splitting not needed, simply return
    return "<p>\n</p>".join(doc)

  for i in range(1,added_lengths[-1]//lim +2): #start from 1 cuz first loop must have lim×1. Formula: total_len//lim +1 repetitions. add another 1 to it cuz python excludes max limit in range. 
    x.append(search(lim*i, added_lengths))
  x.append(None) # a[None:5] and a[5:None] works
  print("Split Index:", x)
  #messages = ["</p>\n<p>".join(doc[x[index-1]:item]) for index,item in enumerate(x)]
  
  messages=[]
  for index, item in enumerate(x):
    print("For:",x[index-1], item)
    print("  len:", len("</p>\n<p>".join(doc[x[index-1]: item])))
    messages.append("</p>\n<p>".join(doc[x[index-1]: item]))
    print("  lentotal:", sum([len(i) for i in messages]))
    print(messages[-1])
  
  return messages


def docs(temp):
  if temp == "wob":
    message = """hi. I am a bot.
<u><b>Commands:</b></u>
●`wob joke` to hear a <b>joke</b>
●`wob coinflip` to <b>flip a coin</b>
●`wob track` to let me <b>track your stats</b>
●`wob rolldice [faces]` to <b>roll a dice</b>. If `faces` isn't given, it defaults to 6
●`wob avatar [user]` to get the user's <b>profile picture</b>. If `user` isn't given, it gives your avatar/profile pic
●`wob banner [user]` to get the user's <b>banner</b>. If `user` isn't given, it gives your banner
●`wob stats [user]` to get the user's <b>statistics</b>. If `user` isn't given, it gives your stats
●`wob graph [user]` to get the user's <b>statistics graphs</b>. If `user` isn't given, it gives your own graphs
●`wob recents [mode]` to get the <b>recent posts on wasteof!</b>.(due to how this works, it doesn't exactly give posts of whole wasteof). If mode=beta, beta links are given. Else, it gives prod links. 
●`wob randompost [mode]` to get a <b>random post</b>. If mode=beta, beta links are given. Else, it gives prod links.
<i>These are the only commands I have for now. Suggest commands on my wall</i>
</p>"""
    #message = ("0"*100+"\n")*5
    message = splitter(message,493)
    if message[-1] == "</p>": #bruh. check for blank split
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
<li><code>{temp} graph [user]</code> to get the user's <b>statistics graphs</b>. If <code>user</code> isn't given, it gives your own graphs. If <code>user</code> is "<code>all</code>", then you get all of wasteofs graphs in one single image!</li>
<li><code>{temp} recents [mode]</code> to get the <b>recent posts on wasteof!</b>.(due to how this works, it doesn't exactly give posts of whole wasteof). If <code>mode</code> isn't given, it gives prod links. if <code>mode</code> is "<code>beta</code>", beta links are given.</li>
<li><code>{temp} randompost [mode]</code> to get a <b>random post</b>. If <code>mode</code> is "<code>beta</code>", beta links are given. Else, it gives prod links.</li>
</ul>
<p><i>These are the only commands I have for now. Suggest commands on my wall.</i></p></p>"""
    return doc

print(f"Result: {[len(item) for item in docs('wob')]}")