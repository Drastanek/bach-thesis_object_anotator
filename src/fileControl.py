import json
import os
import shutil
import cv2 as cv
import piexif
from src.Image import Image
from datetime import datetime
from typing import List, Optional, Dict

import src.MicroObject as MicroObject
from src import globalVariables


def save_object_classes_to_json(object_classes: List[MicroObject.MicroObject], filename: str) -> None:
    """
    Save a list of object classes to a JSON file.
    """
    with open(filename, 'w') as file:
        json.dump([obj.to_dict() for obj in object_classes], file, indent=4)


def load_object_classes_from_json(filename: str) -> Optional[List[MicroObject.MicroObject]]:
    """
    Load object classes from a JSON file.
    """
    with open(filename, 'r') as file:
        if os.stat(filename).st_size == 0:
            return None
        data = json.load(file)
        object_instances = [MicroObject.MicroObject(**obj, from_json=True) for obj in data]
        return object_instances


def get_next_image() -> Optional[Image]:
    """
    Get the next image to be processed.
    """
    next_image_path = get_next_image_path()
    if next_image_path is None:
        return None
    img = cv.imread(next_image_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    image_name = parse_image_name(next_image_path)
    original_path = next_image_path
    return Image(image_name, original_path, None, img)


def get_next_image_path() -> Optional[str]:
    """
    Get the path of the next image to be processed.
    """
    if len(globalVariables.image_paths) == 0:
        read_images_in_input_dir()
    if len(globalVariables.image_paths) == 0:
        return None
    return globalVariables.image_paths.pop(0)


def parse_image_name(image_path: str) -> str:
    """
    Parse the image name from the image path.
    """
    return os.path.basename(image_path)


def copy_images_to_process(directory: str) -> None:
    """
    Copy images from the specified directory to the processing directory.
    """
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


def save_image_micro_object(image: Image) -> None:
    """
    Save the image with its classification to the output directory.
    """
    path = os.path.join(globalVariables.OUTPUT_DIR, image.get_classification().get_latin_name())
    check_path(path)
    path = os.path.join(f"{path}", f"{image.get_name()}")

    cv.imwrite(path, cv.cvtColor(image.image, cv.COLOR_RGB2BGR))
    print(f"Saved image for {image.get_classification().get_latin_name()}")
    add_metadata_to_file(path, image.get_classification(), read_old_meta_data(image))


def add_metadata_to_file(path: str, classification: MicroObject.MicroObject, old_meta_data: Dict[str, str]) -> None:
    """
    Add metadata to the image file.
    """
    exif_dict = piexif.load(path)
    user_comment = old_meta_data.get('Exif.Photo.UserComment', '{}')
    user_comment_data = json.loads(user_comment)
    user_comment_data['human_classification_classified'] = True
    user_comment_data['human_classification_class'] = classification.get_latin_name()
    user_comment_data['human_classification_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    exif_dict['Exif'][piexif.ExifIFD.UserComment] = json.dumps(user_comment_data).encode('utf-8')
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, path)


def read_old_meta_data(image: Image) -> Dict[str, str]:
    """
    Read the old metadata from the image file.
    """
    exif_dict = piexif.load(image.get_original_path())
    metadata = {}
    if piexif.ExifIFD.UserComment in exif_dict['Exif']:
        metadata['Exif.Photo.UserComment'] = exif_dict['Exif'][piexif.ExifIFD.UserComment].decode('utf-8')
    return metadata


def check_path(path: str) -> None:
    """
    Check if a directory exists, and create it if it does not.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")


def check_file(path: str) -> None:
    """
    Check if a file exists, and create it if it does not.
    """
    if not os.path.isfile(path):
        with open(path, 'w') as file:
            pass
        print(f"Created file: {path}")


def remove_image(image_path: str) -> None:
    """
    Remove an image file.
    """
    os.remove(image_path)


def read_images_in_input_dir() -> None:
    """
    Read images from the input directory and add their paths to the global list.
    """
    i = 0
    for root, dirs, files in os.walk(globalVariables.INPUT_PROCESS_DIR):
        for file in files:
            if file.endswith('.jpg'):
                path = os.path.join(root, file)
                globalVariables.image_paths.append(path)
                i += 1
    print(f"Images found: {i}")


def save_to_write_only_json(obj: MicroObject.MicroObject) -> None:
    """
    Save a micro object to a write-only JSON file.
    """
    with open(globalVariables.WRITE_ONLY_MICRO_OBJECTS_JSON, 'a') as file:
        json.dump(obj.to_dict(), file, indent=4)
        file.write('\n')
        print(f"Saved: {obj}")
