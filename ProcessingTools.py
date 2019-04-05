import cv2
import numpy as np

class ProcessingTools(object):




    def detectEdges(self, frame , sigma=0.33):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # compute the median of the single channel pixel intensities
        v = np.median(frame)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)

        # return the edged image
        return edged


