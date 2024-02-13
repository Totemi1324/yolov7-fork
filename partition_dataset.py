import os, shutil
from sklearn.model_selection import train_test_split

annotations_directory = 'C:\\Projects\\Machine Learning\\yolov7\\dataset\\labels'
images_directory = 'C:\\Projects\\Machine Learning\\yolov7\\dataset\\images'

# Ensure consistent dataset size
'''for filename in os.listdir(annotations_directory):
    if filename.endswith('.txt'):
        png_filename = os.path.splitext(filename)[0] + '.png'
        
        png_filepath = os.path.join(images_directory, png_filename)
        if not os.path.exists(png_filepath):
            txt_filepath = os.path.join(annotations_directory, filename)
            os.remove(txt_filepath)
            print(f"Deleted '{txt_filepath}' as no corresponding image file exists.")'''

# Read images and annotations
images = [os.path.join(images_directory, x) for x in os.listdir(images_directory) if x[-3:] == "png"]
annotations = [os.path.join(annotations_directory, x) for x in os.listdir(annotations_directory) if x[-3:] == "txt"]

images.sort()
annotations.sort()

# Split the dataset into train-valid-test splits 
train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

move_files_to_folder(train_images, os.path.join(images_directory, "train"))
move_files_to_folder(val_images, os.path.join(images_directory, "val"))
move_files_to_folder(test_images, os.path.join(images_directory, "test"))
move_files_to_folder(train_annotations, os.path.join(annotations_directory, "train"))
move_files_to_folder(val_annotations, os.path.join(annotations_directory, "val"))
move_files_to_folder(test_annotations, os.path.join(annotations_directory, "test"))