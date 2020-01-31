import os
import cv2
import argparse
import logging

from shutil import rmtree

from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d%m%Y-%H%M%S")
RESIZED_DIR = './result/resized-{}'.format(dt_string)


def createArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--single-mode', action="store_true",
                    help='Single file mode / Multi file mode')
    parser.add_argument('-i', '--file-path', type=str, required=True,
                    help='The path to image/folder.')
    parser.add_argument('--height', type=int, help='The output height of the image')
    parser.add_argument('--width', type=int, help='The output width of the image')
    parser.add_argument('--save-result', action="store_true", help='Save the resized images instead of showing it')
    parser.add_argument('-q', '--image-quality', help='Change the quality of the saved image', type=int)
    return parser


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def prepareFolder():
    rmtree(RESIZED_DIR, ignore_errors=True)
    os.makedirs(RESIZED_DIR)

def resize(filepath, height, width):
    img = cv2.imread(filepath)
    img = image_resize(img, height=height, width=width)

    return img

def getFilename(filepath):
    _, filename = os.path.split(filepath)
    return filename

def saveImage(img, name, image_quality=None):
    saveFile = "{}/{}".format(RESIZED_DIR, name)

    save_success = cv2.imwrite(saveFile, img, [int(cv2.IMWRITE_JPEG_QUALITY), (image_quality if image_quality is not None else 100)])

    if save_success is True:
        print('Saved image: {} with quality {}%'.format(name, (image_quality if image_quality is not None else 100)))
    else:
        print('Failed to save: {}'.format(name))

def processImage(filepath, height, width, save_image, image_quality):
    img = resize(filepath, height=height, width=width)
        
    if save_image:
        saveImage(img, name=getFilename(filepath), image_quality=image_quality)
    else:
        cv2.imshow('img', img)
        cv2.waitKey()

def main():
    args = createArgParser().parse_args()

    if args.save_result:
        prepareFolder()
    
    if args.single_mode: processImage(args.file_path, height=args.height, width=args.width, save_image=args.save_result, image_quality=args.image_quality)

    else:
        for filename in os.listdir(args.file_path):
            if ".jpg" not in filename.lower(): continue

            filepath = "{}/{}".format(args.file_path, filename)
            processImage(filepath, height=args.height, width=args.width, save_image=args.save_result, image_quality=args.image_quality)

if __name__ == "__main__":
    exit(main() or 0)
