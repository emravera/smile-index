# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html#face-detection

import argparse
import cv2
import os
from shutil import copyfile

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')


def detect_faces(raw, filtered, draw, verbose):
    raw_files = os.listdir(raw)
    count = 0

    try:
        for file in raw_files:
            if file.endswith('.jpg'):
                filename = raw + file
                img = cv2.imread(filename)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

                # If the file has only 1 face we filtered to the destination
                if len(faces) == 1:
                    destination = filtered + file
                    if verbose:
                        print 'Face found!!! File %s copied to %s' % (filename, destination)
                    count += 1
                    copyfile(filename, destination)

                # We draw a rectangle on the face
                if draw:
                    for (x,y,w,h) in faces:
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = img[y:y+h, x:x+w]
                        eyes = eye_cascade.detectMultiScale(roi_gray)
                        for (ex,ey,ew,eh) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        print 'STATS -> Total Faces found %d' % count

    except KeyboardInterrupt:
        cv2.destroyAllWindows()


if __name__== "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--raw", help="Path to raw images ")
    a.add_argument("--filtered", help="Path to filtered images")
    a.add_argument("--draw", help="Draw rectangle on face")
    a.add_argument("--verbose", default=False, action='store_true', help="Print more logs and info")
    args = a.parse_args()
    detect_faces(args.raw, args.filtered, args.draw, args.verbose)
