import argparse
import os
import errno
import sys
import glob
import fnmatch
import ntpath


def smile_index(path):
    try:
        videos_to_analize = glob.glob(path + '*.mp4')
        log('SMILE INDEX: Videos To Analize %d' % len(videos_to_analize), 'title')

        for video in videos_to_analize:
            folder_name = video.split('.mp4')[0]
            video_name = ntpath.basename(folder_name)
            log('START video: %s' % video_name, 'title')

            # 1. Create the main folder of the video
            main_video_folder = folder_name
            if not os.path.exists(main_video_folder):
                log('Creating folder %s' % folder_name)
                os.makedirs(main_video_folder)
            else:
                log('Main directory %s already exists' % folder_name, 'error')

            # 2. Generating the raw frames to analyze
            log('Obtaining frames from video %s' % video)
            frame_folder = main_video_folder + os.sep + 'frames' + os.sep

            if not os.path.exists(frame_folder):
                log('Generating raw frames in %s' % frame_folder)
                os.makedirs(frame_folder)
                cmd_frames = 'python ./src/video_frame.py --input %s --out %s' % (video, frame_folder + os.sep)
                os.system(cmd_frames)
            else:
                log('Raw frames Directory %s already exists' % folder_name, 'error')

            # 3. Obtaining the faces from videos
            log('Obtaining faces from video %s' % video)
            faces_folder = main_video_folder + os.sep + 'faces' + os.sep

            if not os.path.exists(faces_folder):
                log('Filtering faces in %s' % faces_folder)
                os.makedirs(faces_folder)
                cmd_faces = 'cd ./src && python face_detector.py --raw %s --filtered %s' % (frame_folder, faces_folder)
                os.system(cmd_faces)
            else:
                log('Faces Directory %s already exists' % faces_folder, 'error')

            # 4. Execute script for executing the AI
            log('Executing AI over the faces and generating report %s' % video)
            report_folder = main_video_folder + os.sep +'report' + os.sep
            csv_report = report_folder + 'report.csv'

            if not os.path.exists(report_folder):
                os.makedirs(report_folder)
                cmd_analyze = 'python ./src/analyze-face-from-pictures.py --path %s --video %s >> %s' % (faces_folder, video, csv_report)
                os.system(cmd_analyze)
            else:
                log('Could not generate the report %s already exists' % report_folder, 'error')


    except KeyboardInterrupt:
        print 'Operation cancelled by the user'

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    except:
        print 'Unexpected error:', sys.exc_info()[0]
        raise


def log(msg, log_type = 'info'):
    if log_type == 'title':
        print '####### %s ########' % msg
    elif log_type == 'error':
        print 'ERROR: %s' % msg
    elif log_type == 'info':
        print msg


def generate_report(path):
    report_name = 'final_report.csv'
    report_path = path + report_name
    try:
        csv_reports = []

        # Always regenerate the report
        if os.path.exists(report_path):
            os.remove(report_path)

        # Filter recursively the .csv files
        for root, dirnames, filenames in os.walk(path):
            for filtered_file in fnmatch.filter(filenames, '*.csv'):
                csv_reports.append(root + '/' + filtered_file)

        # Concatenate all the files in a single report
        with open(report_path, 'w') as outfile:
            for file in csv_reports:
                with open(file) as infile:
                    log('Writing %s to the report' % file)
                    outfile.write(infile.read())

    except KeyboardInterrupt:
        print 'Operation cancelled by the user'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--analyze', default=False, action='store_true', help='Flag to execute the analyze operation')
    parser.add_argument('-p', '--path', required=True, type=str, help='Path to the videos folder')
    parser.add_argument('-r', '--report', default=False, action='store_true', help='Generate one report')
    args = parser.parse_args()

    # Analyze operation or generate the report
    if args.analyze:
        smile_index(args.path)
    elif args.report:
        generate_report(args.path)
