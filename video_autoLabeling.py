import os
import time

import cv2 as cv


def main():
    cap = cv.VideoCapture('can_withoutLight.mp4')
    bgs = cv.createBackgroundSubtractorKNN(dist2Threshold=500, detectShadows=False)
    prev_time = 0
    FPS = 1000
    class_name = ['pet', 'pen', 'mouse', 'paper_box', 'key', 'clip', 'vinyl', 'stick_vinyl', 'can']
    class_idx = 8
    write_image_dir = 'D:/study/python/OpenCV_Labeling/images/' + str(class_idx)
    write_label_dir = 'D:/study/python/OpenCV_Labeling/labels/' + str(class_idx)
    data_num = len(os.listdir(write_label_dir))

    if not os.path.exists(write_image_dir):
        os.makedirs(write_image_dir)

    if not os.path.exists(write_label_dir):
        os.makedirs(write_label_dir)

    while cap.isOpened():
        ret, frame = cap.read()
        current_time = time.time() - prev_time

        if (ret is True) and (current_time > 1. / FPS):
            prev_time = time.time()

            frame = cv.resize(frame, None, fx=0.3, fy=0.3, interpolation=cv.INTER_CUBIC)
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

            hsv1_low = 39
            hsv1_high = 180
            hsv2_low = 21
            hsv2_high = 180
            hsv_s = 0
            hsv_v = 87

            lower_hsv = cv.inRange(hsv, (hsv1_low, hsv_s, hsv_v), (hsv1_high, 255, 255))
            upper_hsv = cv.inRange(hsv, (hsv2_low, hsv_s, hsv_v), (hsv2_high, 255, 255))
            added_hsv = cv.addWeighted(lower_hsv, 1.0, upper_hsv, 1.0, 0.0)
            hsv_out = cv.bitwise_and(hsv, hsv, mask=added_hsv)
            result = cv.cvtColor(hsv_out, cv.COLOR_HSV2BGR)
            fgmask = bgs.apply(result)

            contours, hierarchy = cv.findContours(fgmask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            mask_color = cv.cvtColor(fgmask, cv.COLOR_GRAY2BGR)

            max_x = 0
            max_y = 0
            max_w = 0
            max_h = 0
            max_area = 0

            for contour in contours:
                x, y, w, h = cv.boundingRect(contour)
                if max_area < (w * h):
                    max_x, max_y, max_w, max_h = cv.boundingRect(contour)

            if max_x >= 0 and max_y >= 0 and max_x + max_w < mask_color.shape[1] \
                    and max_y + max_h < mask_color.shape[0]:
                cv.rectangle(mask_color, (max_x, max_y), (max_x + max_w, max_y + max_h), (0, 255, 0), 2)

                write_image_file = '%s/%s_%d.jpg' % (write_image_dir, class_idx, data_num)
                cv.imwrite(write_image_file, frame)

                write_label_file = open('%s/%s_%d.txt' % (write_label_dir, class_idx, data_num), 'w')
                write_label_file.write(
                    '1\n%s %d %d %d %d' % (class_name[class_idx], max_x, max_y, max_x + max_w, max_y + max_h))
                data_num += 1

                print(data_num)
                write_label_file.close()

            window_init = 100
            window_dist = 400
            cv.namedWindow('original_frame')
            cv.moveWindow('original_frame', window_init, 30)
            cv.imshow('original_frame', frame)

            cv.namedWindow('converted_hsv')
            cv.moveWindow('converted_hsv', window_init + window_dist, 30)
            cv.imshow('converted_hsv', result)

            cv.namedWindow('binary_hsv')
            cv.moveWindow('binary_hsv', window_init + window_dist * 2, 30)
            cv.imshow('binary_hsv', fgmask)

            cv.namedWindow('bounding_object')
            cv.moveWindow('bounding_object', window_init + window_dist * 3, 30)
            cv.imshow('bounding_object', mask_color)

        if cv.waitKey(1) > 0:
            cap.release()
            cv.destroyAllWindows()
            print("done")
            break


if __name__ == "__main__":
    main()
