import os
import time

import cv2 as cv


def main():
    video_dir = 'D:/study/python/OpenCV_Labeling/video'

    for video_folder_idx, video_folder in enumerate(os.listdir(video_dir)):
        class_name = ['pet', 'pen', 'mouse', 'paper_box', 'key', 'clip', 'vinyl', 'stick_vinyl', 'can']
        class_idx = int(video_folder[1])
        print(video_folder)
        print(os.listdir(video_dir))

        '''
        Done 12
        01bluePen
        01bluePen_light
        03post
        03seviz
        03starbucks
        04key
        05clip
        07coffeeStick_light
        07iceteaStick
        08colacan
        08spritecan
        08spritecanLight
        '''

        '''
        Impossible 5
        00pet
        01blackMarker
        01blackPen
        01blackSharp
        02mouse
        '''

        '''
        Ambiguous 3
        01greenPen
        06vinyl
        07coffeeStick
        '''

        hsv_h_min = {'00pet': 0, '01blackMarker': 0, '01blackPen': 0, '01blackSharp': 0, '01bluePen': 43,
                     '01bluePen_light': 49, '01greenPen': 23, '02mouse': 28, '03post': 0, '03seviz': 5, '03starbucks': 0, '04key': 0, '05clip': 0,
                     '06vinyl': 0, '07coffeeStick': 0, '07coffeeStick_light': 0, '07iceteaStick': 29, '08colacan': 24, '08spritecan': 17, '08spritecan_light': 17}
        hsv_h_max = {'00pet': 0, '01blackMarker': 0, '01blackPen': 0, '01blackSharp': 0, '01bluePen': 210,
                     '01bluePen_light': 123, '01greenPen': 255, '02mouse': 196, '03post': 29, '03seviz': 87, '03starbucks': 83, '04key': 255, '05clip': 255,
                     '06vinyl': 255, '07coffeeStick': 255, '07coffeeStick_light': 255, '07iceteaStick': 255, '08colacan': 210, '08spritecan': 170, '08spritecan_light': 186}

        hsv_s_min = {'00pet': 0, '01blackMarker': 0, '01blackPen': 0, '01blackSharp': 0, '01bluePen': 0,
                     '01bluePen_light': 0, '01greenPen': 35, '02mouse': 3, '03post': 28, '03seviz': 0, '03starbucks': 52, '04key': 106, '05clip': 128,
                     '06vinyl': 0, '07coffeeStick': 62, '07coffeeStick_light': 49, '07iceteaStick': 0, '08colacan': 102, '08spritecan': 0, '08spritecan_light': 101}
        hsv_s_max = {'00pet': 0, '01blackMarker': 0, '01blackPen': 0, '01blackSharp': 0, '01bluePen': 118,
                     '01bluePen_light': 255, '01greenPen': 255, '02mouse': 255, '03post': 217, '03seviz': 255,'03starbucks': 255,  '04key': 255, '05clip': 210,
                     '06vinyl': 40, '07coffeeStick': 255, '07coffeeStick_light': 255, '07iceteaStick': 255, '08colacan': 255, '08spritecan': 255, '08spritecan_light': 255}

        hsv_v_min = {'00pet': 0, '01blackMarker': 255, '01blackPen': 255, '01blackSharp': 0, '01bluePen': 94,
                     '01bluePen_light': 187, '01greenPen': 149, '02mouse': 0, '03post': 198, '03seviz': 0, '03starbucks': 163, '04key': 163, '05clip': 224,
                     '06vinyl': 156, '07coffeeStick': 62, '07coffeeStick_light': 99, '07iceteaStick': 184, '08colacan': 62, '08spritecan': 73, '08spritecan_light': 40}
        hsv_v_max = {'00pet': 0, '01blackMarker': 255, '01blackPen': 255, '01blackSharp': 0, '01bluePen': 255,
                     '01bluePen_light': 255, '01greenPen': 255, '02mouse': 255, '03post': 255, '03seviz': 255, '03starbucks': 255, '04key': 255, '05clip': 255,
                     '06vinyl': 190, '07coffeeStick': 255, '07coffeeStick_light': 255, '07iceteaStick': 255, '08colacan': 255, '08spritecan': 255, '08spritecan_light': 255}

        min_area = {'00pet': 999999, '01blackMarker': 999999, '01blackPen': 999999, '01blackSharp': 999999, '01bluePen': 0,
                     '01bluePen_light': 0, '01greenPen': 1000, '02mouse': 999999, '03post': 10000, '03seviz': 20000, '03starbucks': 30000, '04key': 2000, '05clip': 800,
                    '06vinyl': 50000, '07coffeeStick': 5000, '07coffeeStick_light': 5000, '07iceteaStick': 5000, '08colacan': 20000, '08spritecan': 20000, '08spritecan_light': 20000}
        max_area = {'00pet': 10000, '01blackMarker': 40000, '01blackPen': 10000, '01blackSharp': 10000, '01bluePen': 40000,
                     '01bluePen_light': 40000, '01greenPen': 30000, '02mouse': 10000, '03post': 200000, '03seviz': 100000, '03starbucks': 100000, '04key': 5000,
                    '05clip': 10000, '06vinyl': 500000, '07coffeeStick': 100000, '07coffeeStick_light': 100000, '07iceteaStick': 100000, '08colacan': 100000,
                    '08spritecan': 40000, '08spritecan_light': 40000}

        for video_idx, video in enumerate(os.listdir(video_dir + '/' + video_folder)):
            print(video)
            print(video_idx)
            cap = cv.VideoCapture(video_dir + '/' + video_folder + '/' + video)
            bgs = cv.createBackgroundSubtractorKNN(dist2Threshold=500, detectShadows=False)
            prev_time = 0
            FPS = 1000
            write_image_dir = 'D:/study/python/OpenCV_Labeling/images/' + str(class_idx)
            write_boundedImage_dir = 'D:/study/python/OpenCV_Labeling/bounded_images/' + str(class_idx)
            write_label_dir = 'D:/study/python/OpenCV_Labeling/labels/' + str(class_idx)

            if not os.path.exists(write_image_dir):
                os.makedirs(write_image_dir)

            if not os.path.exists(write_boundedImage_dir):
                os.makedirs(write_boundedImage_dir)

            if not os.path.exists(write_label_dir):
                os.makedirs(write_label_dir)

            data_num = len(os.listdir(write_image_dir))

            while cap.isOpened():
                ret, frame = cap.read()
                current_time = time.time() - prev_time

                if (ret is True) and (current_time > 1. / FPS):
                    prev_time = time.time()

                    frame = cv.resize(frame, None, fx=0.3, fy=0.3, interpolation=cv.INTER_CUBIC)
                    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                    hsv_binary = cv.inRange(hsv, (hsv_h_min[video_folder], hsv_s_min[video_folder], hsv_v_min[video_folder]),
                                            (hsv_h_max[video_folder], hsv_s_max[video_folder], hsv_v_max[video_folder]))
                    hsv_out = cv.bitwise_and(hsv, hsv, mask=hsv_binary)
                    result = cv.cvtColor(hsv_out, cv.COLOR_HSV2BGR)
                    # fgmask = bgs.apply(result)

                    contours, hierarchy = cv.findContours(hsv_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
                    mask_color = cv.cvtColor(hsv_binary, cv.COLOR_GRAY2BGR)
                    mask_max_color = frame

                    max_x, max_y, max_w, max_h, area = 0, 0, 0, 0, 0

                    for contour in contours:
                        x, y, w, h = cv.boundingRect(contour)
                        cv.rectangle(mask_color, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        if area < (w * h) and x > 5 and y > 5:
                            max_x, max_y, max_w, max_h = cv.boundingRect(contour)
                            area = w * h
                    #
                    # if max_x >= 0 and max_y >= 0 and max_x + max_w < mask_color.shape[1] \
                    #         and max_y + max_h < mask_color.shape[0] \
                    #         and min_area[video_folder] < area < max_area[video_folder]:
                    if min_area[video_folder] < area < max_area[video_folder] and 5 < max_y:
                        cv.rectangle(mask_max_color, (max_x, max_y), (max_x + max_w, max_y + max_h), (0, 255, 0), 2)

                        write_image_file = '%s/%s_%d.jpg' % (write_image_dir, class_idx, data_num)
                        cv.imwrite(write_image_file, frame)

                        write_boundedImage_file = '%s/%s_%d.jpg' % (write_boundedImage_dir, class_idx, data_num)
                        cv.imwrite(write_boundedImage_file, mask_max_color)

                        write_label_file = open('%s/%s_%d.txt' % (write_label_dir, class_idx, data_num), 'w')
                        write_label_file.write(
                            '1\n%s %d %d %d %d' % (class_name[class_idx], max_x, max_y, max_x + max_w, max_y + max_h))
                        data_num += 1

                        print(data_num)
                        write_label_file.close()

                    window_init = 100
                    window_dist = 500
                    cv.namedWindow('original_frame')
                    cv.moveWindow('original_frame', window_init, 30)
                    cv.imshow('original_frame', frame)

                    cv.namedWindow('bounding_object')
                    cv.moveWindow('bounding_object', window_init + window_dist * 1, 30)
                    cv.imshow('bounding_object', mask_color)

                    cv.namedWindow('mask_max_color')
                    cv.moveWindow('mask_max_color', window_init + window_dist * 2, 30)
                    cv.imshow('mask_max_color', mask_max_color)

                else:
                    break

                if cv.waitKey(1) > 0:
                    cap.release()
                    cv.destroyAllWindows()
                    print("done")


if __name__ == "__main__":
    main()
