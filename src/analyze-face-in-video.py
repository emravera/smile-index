import argparse
from scipy.misc import imsave
import cognitive_face as CF
import cv2
from sys import platform

def recognize(key):

  CF.Key.set(key) # set API key
  BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
  CF.BaseUrl.set(BASE_URL)
  cont = 0

  while True:
    cont += 1
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if platform.startswith('win'): # for windows we don't display video due to camera issues
      cap.release()
    name = 'tmp%d.png' % cont
    imsave(name, frame)

    result = CF.face.detect(name, attributes='age,gender')
    try:
      for face in result:
        gender = face['faceAttributes']['gender']
        age = face['faceAttributes']['age']
        print gender, age
        if platform == 'darwin': # for mac we display the video, face bounding box, age & gender
          rect = face['faceRectangle']
          width = rect['width']
          top = rect['top']
          height = rect['height']
          left = rect['left']
          cv2.rectangle(frame, (left, top), (left + width, top + height),
                        (0, 255, 0), 2)
          cv2.putText(frame, '{},{}'.format(gender, int(age)), (left, top),
                      cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
          cv2.imshow('Demo', frame)

    except not result:
      continue

    except KeyboardInterrupt:
      cap.release()
      cv2.destroyAllWindows()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-k','--key', required=True, type=str,
                      help='key for face api')
  args = parser.parse_args()
  recognize(args.key)
