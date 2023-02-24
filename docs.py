
def splitter(message, lim):
  doc = message.split("\n")
  temp = []
  messages = []
  count = 0
  for item in doc:
    count += len(item)+8
    if count > lim:
      if count - 8 > lim:
        messages.append("</p>\n<p>".join(temp))
        temp.clear()
        temp.append(item)
        count= len(item)
      else:
        temp.append(item)
        messages.append("</p>\n<p>".join(temp))
        temp.clear()
        count= 0
      continue

    temp.append(item)

  messages.append("</p>\n<p>".join(temp))
  return messages


def docs(temp):
  if temp == "wob":
    message = """hi. I am a bot.
<u><b>Commands:</b></u>
●`wob joke` to hear a <b>joke</b>
●`wob coinflip` to <b>flip a coin</b>
●`wob track` to let me <b>track your stats</b>
●`wob prefer [list of choices]` to <b>set preferences</b> for the bot. if `list` isn't given, it shows the set preferences. `list` is a list of items separated by a space. Has 2 options: beta/prod, light/dark
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
<li><code>{temp} prefer [list of choices]</code> to <b>set preferences</b> for the bot. if <code>list</code> isn't given, it shows the set preferences. <code>list</code> is a list of items separated by a space. Has 2 options: beta/prod, light/dark</li>
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

#print(f"Result: {[len(item) for item in docs('wob')]}")