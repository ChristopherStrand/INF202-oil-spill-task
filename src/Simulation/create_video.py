import cv2 as cv

# list for all image names
images = [f"images/{i}.png" for i in range(0, 20)]

# reads in first image and gets dimensions
frame = cv.imread(images[0])
height, width, layers = frame.shape

# defines codec (mp4) and creates video object
fourcc = cv.VideoWriter_fourcc(*"mp4v")
video = cv.VideoWriter("video.avi", fourcc, 1, (width, height))

# writes each image to video object
for image in images:
    video.write(cv.imread(image))

# closes all windows and releases video object
cv.destroyAllWindows()
video.release()
