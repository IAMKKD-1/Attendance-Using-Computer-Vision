import cv2 as cv
from Database import connector, dbname, current_date

face = cv.CascadeClassifier('haar_face.xml')
cam = cv.VideoCapture(0)
recog = cv.face.LBPHFaceRecognizer_create()
recog.read(r'C:\Users\krish\Desktop\Codes\OpenCV\Recognizer\TrainingData.yml')

def get_profile(std_id):
    cursor, db = connector(2)
    cursor.execute(f'Use {dbname}')
    cmd = f'Select * from student where stdid = {std_id}'
    cursor.execute(cmd)
    profile = None
    for row in cursor.fetchall():   
        profile = row

    checker = f'select * from d{current_date} where stdid = {std_id}'
    cursor.execute(checker)
    pf = None
    for row in cursor.fetchall():
        pf = row

    if pf is None:
        cmd = f"insert into d{current_date} (stdid, name) values({profile[0]},'{profile[1]}')"
        cursor.execute(cmd)
    db.commit()
    db.close()
    return profile  

while True:
    ret, img = cam.read()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, scaleFactor =1.1, minNeighbors = 5)
    for x,y,w,h in faces:
        cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        id, conf = recog.predict(gray[y:y+h,x:x+w])
        profile = get_profile(id)
        cv.putText(img, str(f'Roll no: {profile[0]}'),(x,y+h+30), cv.FONT_HERSHEY_DUPLEX, 1.0, (0,255,0), 1)
        cv.putText(img, str(f'Name: {profile[1]}'),(x,y+h+55), cv.FONT_HERSHEY_DUPLEX, 1.0, (0,255,0), 1)
        cv.putText(img, str(f'Age: {profile[2]}'),(x,y+h+80), cv.FONT_HERSHEY_DUPLEX, 1.0, (0,255,0), 1)
    cv.imshow('Face', img)
    if(cv.waitKey(1) == ord('q')):
        break

cam.release()
cv.destroyAllWindows()

