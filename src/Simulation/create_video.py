"""
A script to create a video from a sequence of images using OpenCV.

This script reads a series of images, combines them into a video file, and saves the output. 
The video is created in `.avi` format with a specified frame rate and resolution based on the dimensions of the first image.

Typical usage example:

    python create_video.py

Key functionalities:
- Reads images from a predefined directory and sequence.
- Configures the codec for the output video file.
- Combines the images into a single video file with a frame rate of 1 frame per second.

Dependencies:
- OpenCV (`cv2`)

Output:
- A video file named `video.avi`.

"""

import cv2 as cv


def make_video(image_folder="images", intervals=100, steps=10):
    # list for all image names
    images = [f"images/{i}.png" for i in range(0, intervals, steps)]

    # reads in first image and gets dimensions
    frame = cv.imread(images[0])
    height, width, layers = frame.shape

    # defines codec (mp4) and creates video object
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    video = cv.VideoWriter("video.mp4", fourcc, 1, (width, height))

    # writes each image to video object
    for image in images:
        video.write(cv.imread(image))

    # closes all windows and releases video object
    cv.destroyAllWindows()
    video.release()
