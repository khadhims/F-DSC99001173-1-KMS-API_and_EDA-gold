import datetime
import sqlite3

DATABASE = 'cleaned_data.db'

def init_db():
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute('''
    CREATE TABLE IF NOT EXISTS cleaned_data(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cleaned_text TEXT,
      file_path TEXT,
      upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  	)
  ''')
  conn.commit()
  conn.close()

def insert_data(cleaned_text=None, file_path=None, datetime=datetime.datetime.now()):

  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  c.execute('''
    INSERT INTO cleaned_data (cleaned_text, file_path, upload_time)
    VALUES (?, ?, ?)
  ''', (cleaned_text, file_path, datetime))
  conn.commit()
  conn.close()
