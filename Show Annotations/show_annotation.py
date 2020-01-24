import cv2
import os
import sys
import csv
import json
import argparse

def createRectFromKittiText(img, labelPath):
    with open(labelPath) as f:
        for line in f:
            listOfStr = [x for x in line.split(" ")]
            box = [int(listOfStr[4]), int(listOfStr[5]), int(listOfStr[6]), int(listOfStr[7])]
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 255), 1, 1)

def createRectFromVIACSV(img, labelPath):
    with open(labelPath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        for count, row in enumerate(readCSV):
            if count is 0:
                continue
            
            box = json.loads(row[5])
            box = [int(box['x']), int(box['y']), int(box['width'] + box['x']), int(box['height'] + box['y'])]
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 255), 1, 1)

def createArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--annotation-type', type=str,
                    help='The annotation type of the file. [VIA (CSV), KITTI]', default="VIA")
    parser.add_argument('-i', '--image-path', type=str,
                    help='The annotated image path', default="annotated.jpg")
    parser.add_argument('-a', '--annotation-path', type=str,
                    help='The annotation file path', default="via.csv")
    return parser

def main():
    arguments = createArgParser().parse_args()
    img = cv2.imread(arguments.image_path)
    
    createRectFromKittiText(img, arguments.annotation_path) if arguments.annotation_type == 'KITTI' else createRectFromVIACSV(img, arguments.annotation_path)

    cv2.imshow("{} Annotation".format(arguments.annotation_type), img)
    cv2.waitKey()

if __name__ == "__main__":
    sys.exit(main() or 0)