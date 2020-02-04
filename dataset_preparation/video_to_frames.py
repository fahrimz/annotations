"""
    Extract frames from video
"""

import os
import sys
import argparse

from shutil import rmtree

OUTPUT_DIR = "./result"

def buildArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file-path', type=str,
                    required=True,
                    help='Path to video')
    return parser

def prepareFolder(extension):
    location = "{}/{}".format(OUTPUT_DIR, extension)
    rmtree(location, ignore_errors=True)
    os.makedirs(location)
    

def getFilename(filepath):
    _, filename = os.path.split(filepath)
    return filename

def getName(filename):
    name, _ = os.path.splitext(filename)
    return name

def main():
    args = buildArgParser().parse_args()

    filename = getName(getFilename(args.file_path))

    prepareFolder(extension=filename)

    # Extract frames from video, save to result
    command = 'ffmpeg -i {} -r 1/1 {}/{}/{}%03d.jpg'.format(args.file_path, OUTPUT_DIR, filename, filename)
    os.system(command)

if __name__ == "__main__":
    exit(main() or 0)