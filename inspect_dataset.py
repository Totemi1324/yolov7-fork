import os
import random
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

annotations_directory = 'C:\\Projects\\Machine Learning\\yolov7\\dataset\\labels\\train'
annotations = [os.path.join(annotations_directory, x) for x in os.listdir(annotations_directory) if x[-3:] == "txt"]

class_id_to_name_mapping = {0: 'P', 1 : 'H', 2 : 'TOC', 3 : 'L', 4: 'Table', 5: 'Figure', 6: 'Caption', 7: 'Note', 8: 'BlockQuote'}

def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size
    
    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
    transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h 
    
    transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
    transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
    transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
    transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]
    
    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0,y0), (x1,y1)), outline="red")
        
        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))], fill="black");
    
    plt.imshow(np.array(image))
    plt.show()

annotation_file = 'C:\\Projects\\Machine Learning\\yolov7\\dataset\\labels\\train\\62928_0.txt' #random.choice(annotations)
with open(annotation_file, "r") as file:
    annotation_list = file.read().split("\n")[:-1]
    annotation_list = [x.split(" ") for x in annotation_list]
    annotation_list = [[float(y) for y in x ] for x in annotation_list]

image_file = annotation_file.replace("labels", "images").replace("txt", "png")
assert os.path.exists(image_file)

#Load the image
image = Image.open(image_file)

#Plot the Bounding Box
plot_bounding_box(image, annotation_list)