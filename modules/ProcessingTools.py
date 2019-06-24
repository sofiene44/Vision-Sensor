import cv2
import numpy as np
import math


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
    def cropFrame(self, frame, x, y,  height,width):

        heightCap = max(0, min(y + height, frame.shape[0]))
        widthCap = max(0, min(x + width, frame.shape[1]))
        print(y,x)
        print("height, width")
        print(heightCap,widthCap)

        return frame[min(y, heightCap):max(y, heightCap), min(x, widthCap):max(x, widthCap)].copy()

    def replacePartFrame(self,masterFrame,slaveFrame,x=0,y=0):
        height,width,_=slaveFrame.shape
        x=max(x,0)
        y=max(y,0)
        frame = masterFrame.copy()
        frame[y:y + height, x:x + width] = slaveFrame
        return frame

    def ignoreEdge(self,edged,x,y,height=1,width=1):
        temp=edged.copy()
        if len(temp.shape) == 2:

            heightCap=max(0, min(y+height,temp.shape[0]))
            widthCap=max(0, min(x+width,temp.shape[1]))
            temp[min(y, heightCap):max(y, heightCap), min(x, widthCap):max(x, widthCap)] = 0

        return temp

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
        temp = frame.copy()
        for pt in zip(*loc[::-1]):
            if len(pos) == 0 or self.notInList(pt, pos, min(height, width)):
                pos.append(pt)

                # optional show frames with detected patterns in red boxes
                if showOutput:
                    cv2.rectangle(temp, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), 2)

        return pos, temp

    # count pixels of a specific color
    def countColorPixel(self, frame, color=(0, 0, 0), threshold=0, showOutput=False):
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
        return pixels, outputFrame

    @staticmethod
    def gray2BGR(frame):

        return cv2.merge((frame, frame, frame))

    def getNearestPos(self, edged, pos):
        nonzero = cv2.findNonZero(edged)
        if nonzero is None:
            return None, None

        distances = np.sqrt((nonzero[:, :, 0] - pos[0]) ** 2 + (nonzero[:, :, 1] - pos[1]) ** 2)
        nearest_index = np.argmin(distances)
        return nonzero[nearest_index][0][0], nonzero[nearest_index][0][1]

    def measure(self, edged, minDistance=5, xAxis=False, yAxis=False):
        pt1=(0,0)
        pt2=(0,0)
        height, width = edged.shape
        xdistance, ydistance = 0, 0
        edged3CH=self.gray2BGR(edged)
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
            # for simple line
            # cv2.line(edged3CH, pt1, pt2, (255, 0, 0))
            # for double arrow line
            cv2.arrowedLine(edged3CH, pt1, pt2,(255, 0, 0))
            cv2.arrowedLine(edged3CH, pt2, pt1, (255, 0, 0))

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

            # for simple line draw
            # cv2.line(edged3CH, pt1, pt2, (255, 0, 0))
            # for double arrow line draw
            cv2.arrowedLine(edged3CH, pt1, pt2, (255, 0, 0))
            cv2.arrowedLine(edged3CH, pt2, pt1, (255, 0, 0))

        return xdistance, ydistance, edged3CH

    def detectCircle (self, frame, sensibility=1.0, shouldBlure=False):

        frame=frame.copy()

        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        distanceBetweenCircles = (min(gray.shape)) / 10
        if shouldBlure :
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
        print("detecting circles ...")
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, sensibility, distanceBetweenCircles)
        print("total circles detected: ", len(circles[0]))
        print(circles[0])
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                if len(frame.shape)==2:
                    frame=self.gray2BGR(frame)

                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        return frame


    def compareFeatures(self, master, slave, obr=False):
        if obr:

            orb = cv2.ORB_create()
            norm=cv2.NORM_HAMMING
        else:
            orb = cv2.xfeatures2d.SURF_create()
            norm=cv2.NORM_L1
        master=master.copy()
        slave=slave.copy()
        if len(master.shape)==3:
            master=cv2.cvtColor(master, cv2.COLOR_BGR2GRAY)
        if len(slave.shape)==3:
            slave=cv2.cvtColor(slave, cv2.COLOR_BGR2GRAY)

        masterKeypoints, masterDescriptors = orb.detectAndCompute(master, None)
        slaveKeypoints, slaveDescriptors = orb.detectAndCompute(slave, None)

        if not slaveKeypoints or not masterKeypoints:
            return
        matcher = cv2.BFMatcher(norm, crossCheck=True)

        matches=matcher.match(masterDescriptors,slaveDescriptors)

        masterMatches = [(int(masterKeypoints[mat.queryIdx].pt[0]),int(masterKeypoints[mat.queryIdx].pt[1])) for mat in matches[:50]]
        slaveMatches = [(int(slaveKeypoints[mat.trainIdx].pt[0]),int(slaveKeypoints[mat.trainIdx].pt[1])) for mat in matches[:50]]
        #matches = sorted(matches, key=lambda x: x.distance)

        print(masterMatches)
        print(slaveMatches)

        matching_result = cv2.drawMatches(master, masterKeypoints, slave, slaveKeypoints, matches[:4], None, flags=2)
        cv2.imshow("Matching result", matching_result)

        return masterMatches, slaveMatches


#
#
# frame = cv2.imread("pictures/color-pixel-count.jpg")
# # frame = cv2.imread("pictures/piece-mecanique.jpg")
# h,w,_=frame.shape
#
# frame = ProcessingTools().detectEdges(frame)
# slave = ProcessingTools().cropFrame(frame,int(w/2)-50, 0, 50, int(h/2))
#
# ProcessingTools().compareFeatures(frame,slave)
# # cv2.imshow("circles",ProcessingTools().detectCircle(frame))
# #cv2.imshow("frame",frame)
# cv2.waitKey()
