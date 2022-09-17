from flask import Flask
from replit import db
import random
app = Flask('app')

@app.route("/")
def pingpage():
  return {"message": f"ok{random.randint(0,1000)}"}

@app.route("/track")
def trackpage():
  return db.get_raw("track")

@app.route("/ping", methods = ["GET", "POST"])
def res():
  return "HELLO", 202

def keep_alive():
  app.run("0.0.0.0", port=8080)