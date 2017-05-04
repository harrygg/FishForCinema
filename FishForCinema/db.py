import sqlite3
from film import *
from utils import log

db_file = "movies.db"

def get_last_id():
  try:
    conn = sqlite3.connect(db_file)
    with conn:
      cursor = conn.cursor()
      sql_command = "SELECT MAX(id) FROM movies;"
      cursor.execute(sql_command)
      last = cursor.fetchone()[0]
      return last if last else 0
  except:
    return 0

def add(movie):
  try:
    conn = sqlite3.connect(db_file)
    with conn:
      ### Are we inserting or updating?
      cursor = conn.cursor()
      #sql_command = "SELECT id from movies WHERE id=%s" % movie.id
      #cursor.execute(sql_command)
      #id = cursor.fetchone()[0]
      #if not id: 
      sql_command = """
      INSERT INTO movies
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
      data = movie.to_list()
      cursor.execute(sql_command, data)
      conn.commit()
      return True
  except Exception as er:
    log(er, 1)
    return False
  pass