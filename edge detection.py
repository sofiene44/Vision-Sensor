import cv2

# cap = cv2.VideoCapture(0)
cap = cv2.imread('piece-mecanique.jpg', 0)

# width=int(cap.get(3))
# height=int(cap.get(4))


scale = 2
while 1:

    # ret, img = cap.read()
    img = cap

    frame = cv2.Canny(img, 50, 100)
    cv2.imshow("edge detection", frame)
    cv2.imshow('original', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # ecp key pressed
        break

cap.release()
cv2.destroyAllWindows()
