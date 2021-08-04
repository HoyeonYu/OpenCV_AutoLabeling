import os
import cv2


def main():
    read_label_dir = 'D:/study/python/OpenCV_Labeling/labels'
    read_image_dir = 'D:/study/python/OpenCV_Labeling/images'
    write_label_dir = 'D:/study/python/OpenCV_Labeling/labels_formal'

    for label_folder_idx, label_folder in enumerate(os.listdir(read_label_dir)):
        for file_name in os.listdir(read_label_dir + '/' + label_folder):
            file_name = file_name.split('.txt')[0]
            read_label_file = open(read_label_dir + '/' + label_folder + '/' + file_name + '.txt', 'r')
            read_image_file = cv2.imread(read_image_dir + '/' + label_folder + '/' + file_name + '.jpg')

            if not os.path.exists(write_label_dir + '/' + label_folder):
                os.makedirs(write_label_dir + '/' + label_folder)

            write_label_file = open(write_label_dir + '/' + label_folder + '/' + file_name + '.txt', 'w')

            img_width = read_image_file.shape[1]
            img_height = read_image_file.shape[0]

            for line_idx, line in enumerate(read_label_file.readlines()):
                if line_idx == 0:
                    continue

                x = int(line.split(' ')[1]) / img_width
                y = int(line.split(' ')[2]) / img_height
                w = (int(line.split(' ')[3]) - int(line.split(' ')[1])) / img_width
                h = (int(line.split(' ')[4]) - int(line.split(' ')[2])) / img_height

                write_label_file.write('%s %f %f %f %f' % (label_folder, x, y, w, h))

            read_label_file.close()
            write_label_file.close()
            print('Done:', write_label_dir + '/' + label_folder + '/' + file_name)


if __name__ == "__main__":
    main()
