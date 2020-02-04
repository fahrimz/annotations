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
            drawBox(img, box)

def createRectFromVIACSV(img, labelPath):
    with open(labelPath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        for count, row in enumerate(readCSV):
            if count is 0:
                continue
            
            box = json.loads(row[5])
            box = [int(box['x']), int(box['y']), int(box['width'] + box['x']), int(box['height'] + box['y'])]
            drawBox(img, box)

def drawBox(img, box):
    cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 255), 2, 1)


def createArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--multi-image', action='store_true',
                    help='Process multiple images.')
    parser.add_argument('-t', '--annotation-type', type=str,
                    help='The annotation type of the file. [VIA (CSV), KITTI]', default="VIA")
    parser.add_argument('-i', '--image-path', type=str,
                    help='The annotated image path. Change to image folder path if in multi mode', default="annotated.jpg")
    parser.add_argument('-a', '--annotation-path', type=str,
                    help='The annotation file path.', default="via.csv")
    return parser

def scaleImage(image, percent):
    scale_percent = percent # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    return image

def main():
    arguments = createArgParser().parse_args()
    
    if not arguments.multi_image:
        img = cv2.imread(arguments.image_path)
        createRectFromKittiText(img, arguments.annotation_path) if arguments.annotation_type == 'KITTI' else createRectFromVIACSV(img, arguments.annotation_path)

        cv2.imshow("{} Annotation".format(arguments.annotation_type), img)
        cv2.waitKey()
    else:
        folderPath = os.listdir(arguments.image_path)
        
        with open(arguments.annotation_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            for count, row in enumerate(readCSV):
                if count is 0:
                    continue

                imagePath = arguments.image_path + "/" + row[0]
                image = cv2.imread(imagePath)

                box = json.loads(row[5])
                box = [int(box['x']), int(box['y']), int(box['width'] + box['x']), int(box['height'] + box['y'])]
                drawBox(image, box)
                
                if image.shape[1] > 1200:
                    image = scaleImage(image, 20)
                
                cv2.imshow('VIA', image)
                cv2.waitKey()

if __name__ == "__main__":
    sys.exit(main() or 0)