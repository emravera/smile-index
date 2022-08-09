import argparse

import cv2


def extract_images(path_in, path_out):
    count = 0
    vidcap = cv2.VideoCapture(path_in)
    success, image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))  # get a frame every one second
        success, image = vidcap.read()
        if success:
            count += 1
            cv2.imwrite(path_out + "%d_frame.jpg" % count, image)  # save frame as JPG file

    print 'STATS -> Obtained %d frames from video  %s' % (count, path_in)

if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--input", help="Path to video")
    a.add_argument("--out", help="Path to images folder")
    args = a.parse_args()
    extract_images(args.input, args.out)
