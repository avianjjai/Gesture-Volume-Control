import math
import cv2
import time
import numpy as np
import HandTrackingModule as htm
from Speaker import Speaker

#################################################
wCam, hCam = 640, 480
#################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.HandDetector(detectionCon=0.7, maxHands=1)
spk = Speaker()
minVol, maxVol = 0, 100
curr_volume = 80

min_hand_range = float('inf')
max_hand_range = float('-inf')

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if lmList:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2-x1, y2-y1)

        if length > 150:
            length = 150
        min_hand_range = min(min_hand_range, length)
        max_hand_range = max(length, max_hand_range)

        curr_volume = int(((maxVol - minVol)*(length - min_hand_range)/max(1, (max_hand_range - min_hand_range))) + minVol)
        spk.setVolume(curr_volume)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(400 - 2.5*curr_volume)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{curr_volume}%', (45, 440), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Img', img)
    cv2.waitKey(1)