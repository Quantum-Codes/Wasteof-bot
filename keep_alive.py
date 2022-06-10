from flask import Flask

app = Flask('app')

@app.route("/")
def pingpage():
  return "ok"

def keep_alive():
  app.run("0.0.0.0", port=8080)