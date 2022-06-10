from wasteof import api
from keep_alive import keep_alive
import os, threading,time, json

import socketio
try:
  sio = socketio.Client(logger=True)
except AttributeError:
  os.system("pip install python-socketio[client]")
  os.system("clear")
  import socketio
  sio = socketio.Client()

api = api()


"""
def p():
  while True:
    time.sleep(1)
    print(threading.active_count())
api = api()
t = threading.Thread(target = p)
t.start()
"""
@sio.event
def dsconnect(data):
  print('I received a message!')
  print(data)

"""
@sio.on('handshake')
def on_message(data):
  print('HandShake', data)
"""
@sio.on('updateMessageCount')
def on_message(data):
  print('I received a message!')
  print(data)

@sio.event
def connect():
  print("I'm connected!")
  sio.emit('login', {'Authorization': api.token})
  print(vars(sio))


sio.connect("https://api.wasteof.money/", {"auth": {"token":api.token}})
keep_alive()
