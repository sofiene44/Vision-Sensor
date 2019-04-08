import cv2
import numpy as np
import math


class ProcessingTools(object):

    def detectEdges(self, frame, sigma=0.33):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # compute the median of the single channel pixel intensities
        v = np.median(frame)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)
        #print(lower, upper)

        # return the edged image
        return edged

    def cropFrame(self, frame, x, y, width, height):
        return frame[y:y + height, x:x + width].copy()

    def notInList(self, newObject, detectedObjects, spaceBetweenObjects):
        for detectedObject in detectedObjects:
            if math.hypot(newObject[0] - detectedObject[0], newObject[1] - detectedObject[1]) < spaceBetweenObjects:
                return False
        return True

    def detectPattern(self, frame, masterPattern, threshold=0.8):
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pattern_gray = cv2.cvtColor(masterPattern, cv2.COLOR_BGR2GRAY)

        h, w = pattern_gray.shape
        res = cv2.matchTemplate(img_gray, pattern_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        pos = []
        for pt in zip(*loc[::-1]):
            if len(pos) == 0 or self.notInList(pt, pos, min(h, w)):
                pos.append(pt)
        #         cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        # cv2.imshow("frame", frame)
        # cv2.waitKey()
        return pos

    def countColorPixel (self, frame, color=[0, 0, 0], threshold=0):
        upper = np.array([min(color[0]+threshold,255),min(color[1]+threshold,255),min(color[2]+threshold,255)])
        lower = np.array([max(color[0]-threshold,0),max(color[1]-threshold,0),max(color[2]-threshold,0)])
        mask=cv2.inRange(frame,lower,upper)
        output = cv2.bitwise_and(frame, frame, mask=mask)
        pixels=np.count_nonzero(output)
        print(pixels)
        cv2.imshow("out", output)
        cv2.waitKey()
        return pixels










