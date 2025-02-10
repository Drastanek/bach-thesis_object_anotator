import os

DATA_DIR = 'data'
MICRO_OBJECTS_JSON = os.path.join(DATA_DIR, 'microObjects.json')
WRITE_ONLY_MICRO_OBJECTS_JSON = os.path.join(DATA_DIR, 'microObjects_write_only.json')
OUTPUT_DIR = 'output'
INPUT_PROCESS_DIR = os.path.join(DATA_DIR, 'images_to_process')

TEST_IMAGE = os.path.join(DATA_DIR, 'test.jpg')

USER_NAME = "not_specified"

image_paths = []

POSSIBLE_HOTKEYS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]
available_hotkeys = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
]