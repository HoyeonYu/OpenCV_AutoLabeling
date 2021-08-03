import sys

import cv2

src = cv2.imread('beltImage/starbucksBox.png')

if src is None:
    print('Image load failed!')
    sys.exit()

src = cv2.resize(src, dsize=(500, 700))
src_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # BGR -> HSV 로 변경(색상 검출에 효율적)


# 트랙바 콜백 함수 생성
def on_trackbar(pos):
    hmin = cv2.getTrackbarPos('H_min', 'dst')
    hmax = cv2.getTrackbarPos('H_max', 'dst')

    smin = cv2.getTrackbarPos('S_min', 'dst')
    smax = cv2.getTrackbarPos('S_max', 'dst')

    vmin = cv2.getTrackbarPos('V_min', 'dst')
    vmax = cv2.getTrackbarPos('V_max', 'dst')

    dst = cv2.inRange(src_hsv, (hmin, smin, vmin), (hmax, smax, vmax))
    cv2.imshow('dst', dst)


cv2.namedWindow('dst')

# 트랙바 콜백 함수 등록
cv2.createTrackbar('H_min', 'dst', 0, 255, on_trackbar)
cv2.createTrackbar('H_max', 'dst', 0, 255, on_trackbar)

cv2.createTrackbar('S_min', 'dst', 0, 255, on_trackbar)
cv2.createTrackbar('S_max', 'dst', 0, 255, on_trackbar)

cv2.createTrackbar('V_min', 'dst', 0, 255, on_trackbar)
cv2.createTrackbar('V_max', 'dst', 0, 255, on_trackbar)
on_trackbar(0)

cv2.waitKey()

cv2.destroyAllWindows()
