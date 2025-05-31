import cv2
from invasor import InvasionDetector


video_path = 'boneco3.mp4'



cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()


 
ret, frame = cap.read()
ret, frame = cap.read()

cv2.imshow('original', frame)
cv2.waitKey(0)

detector = InvasionDetector(frame)





while True:
    ret, frame = cap.read()
    if not ret:
        break
    result, cropped = detector.invasionCheck(frame)
    if(result):
        cv2.imshow('frame', cropped)
        print("ok")
    else:
        print("Invasion detected!")
    cv2.imshow('original', frame)
    cv2.waitKey(100)

cap.release()
cv2.destroyAllWindows()