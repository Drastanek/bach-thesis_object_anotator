from src.MicroObject import MicroObject
from typing import Optional

class Image:
    name: str = ""
    original_path: str = ""
    classification: Optional[MicroObject] = None
    image = None
    is_classified: bool = False

    def __init__(self, name: str, original_path: str, classification: Optional[MicroObject], image) -> None:
        self.name = name
        self.original_path = original_path
        self.classification = classification
        self.image = image

    def get_name(self) -> str:
        return self.name

    def get_original_path(self) -> str:
        return self.original_path

    def set_classification(self, classification: MicroObject) -> None:
        self.classification = classification

    def get_classification(self) -> Optional[MicroObject]:
        return self.classification

    def get_image(self):
        return self.image

    def set_is_classified(self, is_classified: bool) -> None:
        self.is_classified = is_classified

    def get_is_classified(self) -> bool:
        return self.is_classified
