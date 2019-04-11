import cv2
import numpy as np
import math
from scipy.spatial import distance as dist


class ProcessingTools(object):

    # detect the edges in a frame with a variable sensibility and return the edged frame
    def detectEdges(self, frame, sigma=0.33):
        # get the single channel gray image from frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # blur the image to eliminate edge noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # compute the median of the single channel pixel intensities
        v = np.median(gray)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)

        # return the edged frame
        return edged

    # crop a frame with specific coordinates
    def cropFrame(self, frame, x, y, width, height):
        return frame[y:y + height, x:x + width].copy()

    # check for pattern overlap
    def notInList(self, newObject, detectedObjects, spaceBetweenObjects):
        for detectedObject in detectedObjects:
            if math.hypot(newObject[0] - detectedObject[0], newObject[1] - detectedObject[1]) < spaceBetweenObjects:
                return False
        return True

    # detect patterns in a specific frame
    def detectPattern(self, frame, masterPattern, threshold=0.8, showOutput=False):
        # get the single channel gray image from the frame and master pattern
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pattern_gray = cv2.cvtColor(masterPattern, cv2.COLOR_BGR2GRAY)
        # get height and width of the master pattern
        height, width = pattern_gray.shape
        # look for the pattern in the frame
        res = cv2.matchTemplate(img_gray, pattern_gray, cv2.TM_CCOEFF_NORMED)
        # eliminate matches based on the specified threshold
        loc = np.where(res >= threshold)
        # save and return detected pattern positions
        pos = []
        for pt in zip(*loc[::-1]):
            if len(pos) == 0 or self.notInList(pt, pos, min(height, width)):
                pos.append(pt)

                # optional show frames with detected patterns in red boxes
                if showOutput:
                    temp = frame.copy()
                    cv2.rectangle(temp, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), 2)
            if showOutput:
                print(len(pos), " matching patterns detected")
                cv2.imshow("frame", temp)
                cv2.waitKey()
        return pos

    # count pixels of a specific color
    def countColorPixel(self, frame, color=[0, 0, 0], threshold=0, showOutput=False):
        # calculate the upper and lower threshold for the color detection based on the specified threshold
        upper = np.array(
            [min(color[0] + threshold, 255), min(color[1] + threshold, 255), min(color[2] + threshold, 255)])
        lower = np.array([max(color[0] - threshold, 0), max(color[1] - threshold, 0), max(color[2] - threshold, 0)])
        # mask the colors that are not in the previously calculated range
        mask = cv2.inRange(frame, lower, upper)
        # apply the mask to the frame
        outputFrame = cv2.bitwise_and(frame, frame, mask=mask)
        # count the pixels that have non zero values in the masked image
        pixels = np.count_nonzero(outputFrame)

        # optional print the counted pixel number and show the output frame

        if showOutput:
            print("pixels counted= ", pixels)
            cv2.imshow("out", outputFrame)
            cv2.waitKey()
        # returns the counted pixels and output frame
        return [pixels, outputFrame]

    def measure(self, edged, minDistance=5, xAxis=False, yAxis=False):

        height, width = edged.shape
        xdistance, ydistance = 0, 0

        if yAxis:
            midV = edged[:, int(width / 2)]
            y = np.nonzero(midV)
            y = y[0]
            for i in range(len(y) - 1):

                if y[i + 1] - y[i] >= minDistance:
                    pt2 = int(width / 2), y[i + 1]
                    pt1 = int(width / 2), y[i]
                    ydistance = y[i + 1] - y[i]
                    print("y distance= ", ydistance)
                    break

            cv2.line(edged, pt1, pt2, 255)

        if xAxis:
            midH = edged[int(height / 2), :]
            x = np.nonzero(midH)
            x = x[0]
            for i in range(len(x) - 1):

                if x[i + 1] - x[i] >= minDistance:
                    pt2 = x[i + 1], int(height / 2)
                    pt1 = x[i], int(height / 2)
                    xdistance = x[i + 1] - x[i]
                    print("x distance= ", xdistance)
                    break

            cv2.line(edged, pt1, pt2, 255)
        cv2.imshow("", edged)
        cv2.waitKey()

        return xdistance, ydistance

    def detectCircle(self, frame, sensibility=1.0):
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        distanceBetweenCircles = (min(gray.shape)) / 10
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        print("detecting circles ...")
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, sensibility, distanceBetweenCircles)
        print(len(circles[0]))
        print(circles[0])
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        cv2.imshow("", frame)
        cv2.waitKey()


# frame = cv2.imread("color-pixel-count.jpg")
# frame = cv2.imread("piece-mecanique.jpg")
#
# frame = ProcessingTools().detectEdges(frame)
# print(ProcessingTools().measure(frame, 30, True, True))
