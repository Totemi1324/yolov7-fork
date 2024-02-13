import xml.etree.ElementTree as ET
import shutil
import os

valid_tags = ['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'TOC', 'L', 'Table', 'Figure', 'Caption', 'Note', 'BlockQuote']
tag_to_class = {'P': 0, 'H1': 1, 'H2': 1, 'H3': 1, 'H4': 1, 'H5': 1, 'H6': 1, 'TOC': 2, 'L': 3, 'Table': 4, 'Figure': 5, 'Caption': 6, 'Note': 7, 'BlockQuote': 8}

def find_xml_files(directory):
    xml_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.xml'):
                full_path = os.path.join(root, file)
                xml_files.append(full_path)

    return xml_files

def process_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    document_id = root.attrib['id']
    tag_info = []

    for elem in root.iter():
        if elem.tag in valid_tags:
            bbox_str = elem.attrib.get('bbox')
            bbox = [float(n) for n in bbox_str.split(';')] if bbox_str else []
            pageindex = elem.attrib.get('pageindex', 'N/A')
            tag_info.append({'tag': elem.tag, 'bbox': bbox, 'pageindex': pageindex})

    return document_id, tag_info

def convert_coords(bbox):
    left, bottom, right, top = bbox
    width = right - left
    height = top - bottom
    x_center = left + width / 2
    y_center = 1 - (top - height / 2)

    x_center = round(x_center, 5)
    y_center = round(y_center, 5)
    width = round(width, 5)
    height = round(height, 5)

    return [x_center, y_center, width, height]

def process_pages(search_dir, image_dir, annotations_directory, images_directory, xml_file, document_id, tag_info):
    relative_path = os.path.relpath(xml_file, search_dir)
    without_extension = os.path.splitext(relative_path)[0]
    without_extension2 = os.path.splitext(without_extension)[0]
    image_folder_path = os.path.join(image_dir, without_extension2)

    if not os.path.exists(image_folder_path):
        print("Path " + image_folder_path + " not found; skipping...");
        return
    
    for filename in os.listdir(image_folder_path):
        if filename.endswith('.png'):
            page_number = os.path.splitext(filename)[0]
            annotations = []
            txt_filename = f"{document_id}_{page_number}.txt"
            txt_path = os.path.join(annotations_directory, txt_filename)
            if os.path.exists(txt_path):
                continue

            for entry in tag_info:
                if entry['pageindex'] == page_number:
                    class_label = tag_to_class[entry['tag']]
                    converted_bbox = convert_coords(entry['bbox'])
                    annotations.append(f"{class_label} {' '.join(map(str, converted_bbox))}")
            
            with open(txt_path, 'w') as f:
                for annotation in annotations:
                    f.write(f"{annotation}\n")
            
            png_src_path = os.path.join(image_folder_path, filename)
            png_dest_path = os.path.join(images_directory, f"{document_id}_{page_number}.png")
            shutil.copy(png_src_path, png_dest_path)


directory_to_search = 'C:\\Projects\\a4.trainingdatamanager\\A4.Internal.AnnotationGenerator\\output'
image_directory = 'C:\\Projects\\a4.trainingdatamanager\\A4.Internal.RasterizationGenerator\\output'

annotations_directory = 'C:\\Projects\\Machine Learning\\yolov7\\dataset\\labels'
images_directory = 'C:\\Projects\\Machine Learning\\yolov7\\dataset\\images'

xml_files = find_xml_files(directory_to_search)

for xml_file in xml_files:
    #print(xml_file)
    document_id, tag_info = process_xml_file(xml_file)
    
    process_pages(directory_to_search, image_directory, annotations_directory, images_directory, xml_file, document_id, tag_info)
