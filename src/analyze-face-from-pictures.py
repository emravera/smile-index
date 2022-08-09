import argparse
import cognitive_face as CF
import cv2
import os
import time

# Configurations for AI
BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0'  # 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'
API_KEY = 'COMPLETE'


def recognize(path, video, title):
    # set API key and BASE_URL
    CF.Key.set(API_KEY)
    CF.BaseUrl.set(BASE_URL)

    files = os.listdir(path)
    counter = 0

    # Print header of what represent each column in the csv
    if title:
        print 'video,imagen,sonrisa,genero,edad,maq_ojos,maq_labios,accesorios,e_ENOJO,e_CONTEMPLACION,e_DISGUSTO,e_MIEDO,e_ALEGRIA,e_NEUTRAL,e_TRISTEZA,e_SORPRESA'

    for name in files:
        counter += 1
        fullpath = path + name
        if counter == 19:
            time.sleep(70) # this is done because free api needs to stop 1 minute after 19
            counter = 0  # restart the counter
        result = CF.face.detect(fullpath, attributes='smile,age,gender,makeup,emotion,accessories')
        try:
            # Is done for multiple faces
            for face in result:
                smile = face['faceAttributes']['smile']
                gender = face['faceAttributes']['gender']
                age = face['faceAttributes']['age']
                makeup_eye = face['faceAttributes']['makeup']['eyeMakeup']
                makeup_lips = face['faceAttributes']['makeup']['lipMakeup']
                accessories = face['faceAttributes']['accessories'][0]['type'] if face['faceAttributes']['accessories'] else face['faceAttributes']['accessories']
                emotion_anger = face['faceAttributes']['emotion']['anger']
                emotion_contempt = face['faceAttributes']['emotion']['contempt']
                emotion_disgust = face['faceAttributes']['emotion']['disgust']
                emotion_fear = face['faceAttributes']['emotion']['fear']
                emotion_happiness = face['faceAttributes']['emotion']['happiness']
                emotion_neutral = face['faceAttributes']['emotion']['neutral']
                emotion_sadness = face['faceAttributes']['emotion']['sadness']
                emotion_surprise = face['faceAttributes']['emotion']['surprise']

                print '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (video, fullpath, smile, gender, age, makeup_eye, makeup_lips, accessories, emotion_anger, emotion_contempt, emotion_disgust, emotion_fear, emotion_happiness, emotion_neutral, emotion_sadness, emotion_surprise)

        except not result:
            continue

        except KeyboardInterrupt:
            cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True, type=str, help='path to the images with faces')
    parser.add_argument('-v', '--video', required=True, type=str, help='Video name')
    parser.add_argument('-t', '--title', default=False, action='store_true', help='Header is included')
    args = parser.parse_args()
    recognize(args.path, args.video, args.title)
