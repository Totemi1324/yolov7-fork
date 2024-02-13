import os

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def adjust_rectangle(x, y, width, height):
    width = clamp(width, 0, 1)
    height = clamp(height, 0, 1)

    if x - width / 2 < 0:
        width += x - width / 2
        x = width / 2
    elif x + width / 2 > 1:
        left_prev = x - width / 2
        width -= x + width / 2 - 1
        x = left_prev + width / 2

    if y - height / 2 < 0:
        height += y - height / 2
        y = height / 2
    elif y + height / 2 > 1:
        top_prev = y - height / 2
        height -= y + height / 2 - 1
        y = top_prev + height / 2

    return x, y, width, height

def process_file(filepath):
    unique_lines = set()
    with open(filepath, 'r') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.split()
        if len(parts) == 5:
            class_label, x, y, width, height = parts
            x, y, width, height = map(float, [x, y, width, height])

            x, y, width, height = adjust_rectangle(x, y, width, height)

            new_line = f"{class_label} {x:.5f} {y:.5f} {width:.5f} {height:.5f}\n"
            unique_lines.add(new_line)
    
    with open(filepath, 'w') as file:
        file.writelines(unique_lines)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                process_file(filepath)

process_directory('C:\\Projects\\Machine Learning\\yolov7\\dataset\\labels')