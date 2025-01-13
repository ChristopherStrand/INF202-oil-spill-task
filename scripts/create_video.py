import cv2 as cv

images = [f"images/{i}.png" for i in range(0, 20)]

frame = cv.imread(images[0])
height, width, layers = frame.shape

fourcc = cv.VideoWriter_fourcc(*"mp4v")
video = cv.VideoWriter("video.avi", fourcc, 1, (width, height))
for image in images:
    video.write(cv.imread(image))

cv.destroyAllWindows()
video.release()
