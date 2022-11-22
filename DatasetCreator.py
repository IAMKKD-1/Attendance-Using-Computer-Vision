import cv2 as cv
import os
from Database import connector, dbname

cursor, db = connector(2)
cursor.execute(f'Use {dbname}')

identity =  int(input('Enter rollno: '))
name = input('Enter your name: ')
age = int(input('Enter your age: '))
path = os.getcwd()

sample = 1
data = None

cursor.execute(f'Select * from student where stdid = {identity}')
for row in cursor.fetchall():
    data = row

if data is None:
    cmd = f'Insert into student(stdid, name, age) values({identity},\'{name}\',{age})'
else:
    cmd = f'Update student set name = \'{name}\', age = {age} where stdid = {identity}'

cursor.execute(cmd)
db.commit()

face = cv.CascadeClassifier('haar_face.xml')
cam = cv.VideoCapture(0)

while True:
    ret, img = cam.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, scaleFactor =1.2, minNeighbors = 3)
    for x,y,w,h in faces:
        cv.imwrite(f'{path}\Dataset\{identity}.{sample}.jpg', gray[y:y+h,x:x+h])
        sample += 1
        cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        cv.waitKey(100)
    cv.imshow('Face', img)
    cv.waitKey(1)
    if(sample > 50):
        break

cam.release()
cv.destroyAllWindows()