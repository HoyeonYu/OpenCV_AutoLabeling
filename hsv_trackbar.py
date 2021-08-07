import sys
import cv2

src = cv2.imread('trackbar_image/clip.png')

if src is None:
    print('Image load failed!')
    sys.exit()

src = cv2.resize(src, dsize=(500, 700))
src_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)


def on_trackbar(pos):
    hmin = cv2.getTrackbarPos('H_min', 'Trackbar')
    hmax = cv2.getTrackbarPos('H_max', 'Trackbar')

    smin = cv2.getTrackbarPos('S_min', 'Trackbar')
    smax = cv2.getTrackbarPos('S_max', 'Trackbar')

    vmin = cv2.getTrackbarPos('V_min', 'Trackbar')
    vmax = cv2.getTrackbarPos('V_max', 'Trackbar')

    dst = cv2.inRange(src_hsv, (hmin, smin, vmin), (hmax, smax, vmax))
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    color_dst = cv2.bitwise_and(src, dst)
    cv2.imshow('Trackbar', color_dst)


cv2.namedWindow('Trackbar')

cv2.createTrackbar('H_min', 'Trackbar', 0, 255, on_trackbar)
cv2.createTrackbar('H_max', 'Trackbar', 0, 255, on_trackbar)

cv2.createTrackbar('S_min', 'Trackbar', 0, 255, on_trackbar)
cv2.createTrackbar('S_max', 'Trackbar', 0, 255, on_trackbar)

cv2.createTrackbar('V_min', 'Trackbar', 0, 255, on_trackbar)
cv2.createTrackbar('V_max', 'Trackbar', 0, 255, on_trackbar)

on_trackbar(0)

cv2.waitKey()
cv2.destroyAllWindows()
