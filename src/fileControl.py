import json
import os
import shutil
import pyexiv2
import cv2 as cv
from src.Image import Image
from datetime import datetime

import src.MicroObject as MicroObject
from src import globalVariables


def save_object_classes_to_json(object_classes, filename):
    with open(filename, 'w') as file:
        json.dump([obj.to_dict() for obj in object_classes], file, indent=4)


def load_object_classes_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        object_instances = [MicroObject.MicroObject(**obj) for obj in data]
        return object_instances


def get_next_image():
    next_image_path = get_next_image_path()
    if next_image_path is None:
        return None
    img = cv.imread(next_image_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    image_name = parse_image_name(next_image_path)
    original_path = next_image_path
    return Image(image_name, original_path, None, img)


def get_next_image_path():
    if len(globalVariables.image_paths) == 0:
        read_images_in_input_dir()
    if len(globalVariables.image_paths) == 0:
        return None
    return globalVariables.image_paths.pop(0)


def parse_image_name(image_path):
    return os.path.basename(image_path)


def copy_images_to_process(directory):
    i = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg'):
                path = os.path.join(root, file)
                dest = os.path.join(globalVariables.INPUT_PROCESS_DIR, file)
                shutil.copy(path, dest)
                i += 1
                print(f"Copied image: {path} to {dest}")
    print(f"Images copied: {i}")


def save_image_micro_object(image):
    path = os.path.join(globalVariables.OUTPUT_DIR, image.get_classification().get_latin_name())
    check_path(path)
    path = os.path.join(f"{path}", f"{image.get_name()}")

    cv.imwrite(path, cv.cvtColor(image.image, cv.COLOR_RGB2BGR))
    print(f"Saved image for {image.get_classification().get_latin_name()}")
    add_metadata_to_file(path, image.get_classification(), read_old_meta_data(image))


def add_metadata_to_file(path, classification, old_meta_data):
    with pyexiv2.Image(path) as img:
        metadata = img.read_exif()

        # Update the UserComment tag with additional classification data
        user_comment = old_meta_data.get('Exif.Photo.UserComment', '{}')
        user_comment_data = json.loads(user_comment)
        user_comment_data['human_classification_classified'] = True
        user_comment_data['human_classification_class'] = classification.get_latin_name()
        user_comment_data['human_classification_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # add meta for user that classified the image
        metadata['Exif.Photo.UserComment'] = json.dumps(user_comment_data)

        # Write the updated metadata back to the image
        img.modify_exif(metadata)


def read_old_meta_data(image):
    with pyexiv2.Image(image.get_original_path()) as img:
        metadata = img.read_exif()
        return metadata


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def remove_image(image_path):
    os.remove(image_path)


def read_images_in_input_dir():
    i = 0
    for root, dirs, files in os.walk(globalVariables.INPUT_PROCESS_DIR):
        for file in files:
            if file.endswith('.jpg'):
                path = os.path.join(root, file)
                globalVariables.image_paths.append(path)
                i += 1
    print(f"Images found: {i}")
