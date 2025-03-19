from src.MicroObject import MicroObject
from typing import Optional

class Image:
    name: str = ""
    original_path: str = ""
    classification: Optional[MicroObject] = None
    image = None
    is_classified: bool = False

    def __init__(self, name: str, original_path: str, classification: Optional[MicroObject], image) -> None:
        """
        Initialize an Image instance.

        :param name: Name of the image.
        :param original_path: Original path of the image.
        :param classification: Classification of the image as a MicroObject.
        :param image: Image data.
        """
        self.name = name
        self.original_path = original_path
        self.classification = classification
        self.image = image

    def get_name(self) -> str:
        """
        Get the name of the image.

        :return: Name of the image.
        """
        return self.name

    def get_original_path(self) -> str:
        """
        Get the original path of the image.

        :return: Original path of the image.
        """
        return self.original_path

    def set_classification(self, classification: MicroObject) -> None:
        """
        Set the classification of the image.

        :param classification: Classification to set.
        """
        self.classification = classification

    def get_classification(self) -> Optional[MicroObject]:
        """
        Get the classification of the image.

        :return: Classification of the image.
        """
        return self.classification

    def get_image(self):
        """
        Get the image data.

        :return: Image data.
        """
        return self.image

    def set_is_classified(self, is_classified: bool) -> None:
        """
        Set the classification status of the image.

        :param is_classified: Classification status to set.
        """
        self.is_classified = is_classified

    def get_is_classified(self) -> bool:
        """
        Get the classification status of the image.

        :return: Classification status of the image.
        """
        return self.is_classified
