import cv2 as cv
import numpy as np
import os
from PIL import Image

recog = cv.face.LBPHFaceRecognizer_create()

stdImgData = []
path = r'C:\Users\krish\Desktop\Codes\OpenCV\Dataset\\'

def getImageId(path):
    imagePaths = [os.path.join(path, j) for j in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath)
        faceNp = np.array(faceImg,'uint8')
        Id = int(os.path.split(imagePath)[-1].split('.')[0])
        faces.append(faceNp)
        IDs.append(Id)
        cv.imshow('Training', faceNp)
        cv.waitKey(10)
    return np.array(IDs), faces

IDs, faces = getImageId(path)
recog.train(faces, IDs)
recog.save('Recognizer/TrainingData.yml')
cv.destroyAllWindows()