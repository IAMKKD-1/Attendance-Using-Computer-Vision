import mysql.connector
try:
  def connector(returnval):
    '''
    1 -> cursor
    2 -> cursor, db_connector
    3 -> db_connector
    '''
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="root",
    )
    cursor = db.cursor()
    if returnval == 1:
      return cursor
    elif returnval == 2:
      return (cursor, db)
    elif returnval == 3:
      return db
    else:
      return 'Error! Please enter proper return value!'

  cursor, db = connector(2)

  dbname = 'DataScience'
  cursor.execute(f'Create Database IF NOT EXISTS {dbname}')
  cursor.execute(f'Use {dbname}')

  cursor.execute('select curdate()')
  for date in cursor.fetchall():
    current_date = str(date[0])
    current_date = current_date.replace('-','')

  cursor.execute(f'Create Table IF NOT EXISTS student (stdid int primary key, name varchar(50) not null, age int)')

  cursor.execute(f'Create Table IF NOT EXISTS d{current_date} (aid int primary key auto_increment, stdid int, name varchar(50) not null, attendance Boolean default True, time timestamp default CURRENT_TIMESTAMP(), FOREIGN KEY (stdid) REFERENCES student(stdid))')

  print('Database & Tables Created!')
except:
  print('Some Error Occured!')