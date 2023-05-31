from replit import db
import mysql.connector, os, json


mydb = mysql.connector.connect(
  host = os.environ["host"],
  user = os.environ["dbuser"],
  password = os.environ["dbpass"],
  database = os.environ["database"]
)

sql = mydb.cursor()



tracked = set(db["track"])
other = json.loads(db.get_raw("users"))

users = []
for item in other:
  users.append(item)
  
print(len(set(tracked)), len(tracked))
print(len(set(users)), len(users))

overall = set(tracked).union(set(users))
print(len(overall))

data = []
for item in overall:
  if item in other:
    dark = 1 if other[item]["theme"] == "dark" else 0
    beta = 1 if other[item]["site"] == "beta" else 0
  else:
    dark, beta = 1, 0

  data.append(
    (
      item,
      (item in tracked)*1,
      beta,
      dark
    )
  )


query = "INSERT INTO wasteof (userid, track, beta, dark) VALUES (%s, %s, %s, %s)"

for item in data:
  sql.execute(query, item)

mydb.commit()

"""
CREATE TABLE wasteof (
  userid varchar(30) UNIQUE NOT NULL,
  track BOOL,
  dark BOOL,
  beta BOOL
);
"""