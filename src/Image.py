from src.MicroObject import MicroObject


class Image:
    name = ""
    original_path = ""
    classification: MicroObject = None
    image = None
    is_classified = False

    def __init__(self, name, original_path, classification, image):
        self.name = name
        self.original_path = original_path
        self.classification: MicroObject = classification
        self.image = image

    def get_name(self):
        return self.name

    def get_original_path(self):
        return self.original_path

    def set_classification(self, classification):
        self.classification = classification

    def get_classification(self):
        return self.classification

    def get_image(self):
        return self.image

    def set_is_classified(self, is_classified):
        self.is_classified = is_classified

    def get_is_classified(self):
        return self.is_classified
