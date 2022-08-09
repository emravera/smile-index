import argparse
import os
import errno
import sys
from shutil import copyfile


def reorg_path(path, destination):
    try:
        folders_to_analyze = os.listdir(path)
        for folder in folders_to_analyze:
            files_to_analyze = os.listdir(path + '/' + folder)
            for image in files_to_analyze:
                image_name = folder.replace(" ", "_") + image.replace(" ", "_")
                print 'Copying %s' % image_name
                copyfile(path + '/' + folder + '/' + image, destination + image_name)

    except KeyboardInterrupt:
        print 'Operation cancelled by the user'

    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    except:
        print 'Unexpected error:', sys.exc_info()[0]
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reorg', default=False, action='store_true', help='Flag to execute the reorg')
    parser.add_argument('-p', '--path', required=True, type=str, help='Path to the images')
    parser.add_argument('-d', '--destination', required=True, type=str, help='Path to the result')
    args = parser.parse_args()

    # Analyze operation or generate the report
    if args.reorg:
        reorg_path(args.path, args.destination)
