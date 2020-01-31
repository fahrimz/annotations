""" Export the annotation from VIA (VGG Image Annotator)
    to KITTI annotation format.
    VIA: http://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html
"""

import os
import sys
import csv
import json
import math
import argparse

from shutil import rmtree, copyfile
import cv2

CONVERTED_DIR = './result'
CONVERTED_IMG_DIR = '{}/images'.format(CONVERTED_DIR)
CONVERTED_LBL_DIR = '{}/labels'.format(CONVERTED_DIR)


def createArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--file-type', type=str,
                    help='The file format. [CSV, JSON]', default="CSV")
    parser.add_argument('-a', '--file-path', type=str,
                    help='The annotation file path.', default="via.csv")
    parser.add_argument('-f', '--folder-path', type=str, required=True,
                    help='The path to the folder containing the images.')
    return parser


def box_to_line(box):
    """Convert 1 bounding box into 1 line in the KITTI txt file.

    # Arguments
      box: [x_min, y_min, x_max, y_max].

    KITTI format:
    Values  Name        Description
    --------------------------------------------------------------------
       1    type        Describes the type of object: 'Car', 'Van',
                        'Truck', 'Pedestrian', 'Person_sitting',
                        'Cyclist', 'Tram', 'Misc' or 'DontCare'
       1    truncated   Float from 0 (non-truncated) to 1 (truncated),
                        where truncated refers to the object leaving
                        image boundaries
       1    occluded    Integer (0,1,2,3) indicating occlusion state:
                        0 = fully visible, 1 = partly occluded
                        2 = largely occluded, 3 = unknown
       1    alpha       Observation angle of object, ranging [-pi..pi]
       4    bbox        2D bounding box of object in the image
                        (0-based index): contains left, top, right,
                        bottom pixel coordinates
       3    dimensions  3D object dimensions: height, width, length
       3    location    3D object location x,y,z in camera coordinates
       1    rotation_y  Rotation ry around Y-axis in camera coordinates
                        [-pi..pi]
       1    score       Only for results: Float, indicating confidence
                        in detection, needed for p/r curves, higher is
                        better.
    """
    return ' '.join(['hand',
                     '0',
                     '0',
                     '0',
                     '{} {} {} {}'.format(*box),
                     '0 0 0',
                     '0 0 0',
                     '0',
                     '0'])


def prepareFolder():
    rmtree(CONVERTED_DIR, ignore_errors=True)
    os.makedirs(CONVERTED_IMG_DIR)
    os.makedirs(CONVERTED_LBL_DIR)


def main():
    args = createArgParser().parse_args()

    prepareFolder()

    if args.file_type == "CSV":
        with open(args.file_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            
            for count, row in enumerate(readCSV):
                if count is 0:
                    continue

                filename = row[0]

                # Copy image to 'images' folder
                src_jpg = os.path.join(args.folder_path, filename)
                dst_jpg = os.path.join(CONVERTED_IMG_DIR, filename)
                copyfile(src_jpg, dst_jpg)

                # Save box coordinates as txt file in 'labels' folder
                box = json.loads(row[5])
                x_min = int(math.floor(box['x']))
                y_min = int(math.floor(box['y']))
                x_max = int(math.ceil(box['width'])) + x_min
                y_max = int(math.ceil(box['height'])) + y_min
                box = [x_min, y_min, x_max, y_max]

                savedFile = os.path.join(CONVERTED_LBL_DIR, os.path.splitext(filename)[0] + ".txt")
                if os.path.isfile(savedFile):
                    with open(savedFile, 'a') as f:
                        f.write(box_to_line(box) + '\n')
                else:
                    with open(savedFile, 'w') as f:
                        f.write(box_to_line(box) + '\n')
            

if __name__ == "__main__":
    sys.exit(main() or 0)