import mysql.connector, os


class database:
  def __init__(self):
    mydb = mysql.connector.connect(
      host = os.environ["host"],
      user = os.environ["dbuser"],
      password = os.environ["dbpass"],
      database = os.environ["database"]
    )
    self.db = mydb
    self.cursor = mydb.cursor()


  def commit(self):
    self.db.commit()
    return self.db

  def execute(self, *args):
    self.cursor.execute(*args)
    result = []
    for item in self.cursor:
      result.append(item)
    return result

  def __contains__(self, item):
    exists = self.execute("SELECT exists(SELECT * FROM wasteof WHERE userid=%s);", (item,))
    return exists[0][0]

  def new_user(self, id, track=0, beta=0, dark=1):
    if not self.__contains__(id):
      self.execute("INSERT INTO wasteof (userid, track, beta, dark) VALUES (%s, %s, %s, %s);", (id, track, beta, dark))
      self.commit()


"""
CREATE TABLE wasteof (
  userid varchar(30) UNIQUE NOT NULL,
  track BOOL,
  dark BOOL,
  beta BOOL
);
"""