import os

read_bbox_dir = 'D:/study/python/OpenCV_Labeling/bounded_images'
read_images_dir = 'D:/study/python//OpenCV_Labeling/images'
read_labels_dir = 'D:/study/python//OpenCV_Labeling/labels'
read_labelsFormal_dir = 'D:/study/python//OpenCV_Labeling/labels_formal'

for images_folder_idx, images_folder in enumerate(os.listdir(read_images_dir)):
    for images_file_name in os.listdir(read_images_dir + '/' + images_folder):
        if not os.path.isfile(read_bbox_dir + '/' + images_folder + '/' + images_file_name):
            delete_file_name = images_file_name.split('.jpg')[0]
            print(delete_file_name)
            os.remove(read_images_dir + '/' + images_folder + '/' + delete_file_name + '.jpg')
            os.remove(read_labels_dir + '/' + images_folder + '/' + delete_file_name + '.txt')
            os.remove(read_labelsFormal_dir + '/' + images_folder + '/' + delete_file_name + '.txt')
