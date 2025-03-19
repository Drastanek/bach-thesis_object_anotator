from src.MicroObject import MicroObject
import src.fileControl as fileControl
from src.UserInterfaceView import UserInterfaceView
import src.globalVariables as globalVariables
import os
from typing import Optional, Dict
from src.Image import Image


class MicroObjectController:
    view: Optional[UserInterfaceView]
    current_image: Optional[Image] = None 
    micro_object_dict: Dict[str, MicroObject] = {}

    def __init__(self) -> None:
        """
        Initialize the MicroObjectController with no view.
        """
        self.view = None

    def set_view(self, view: UserInterfaceView) -> None:
        """
        Set the view for the controller and trigger recalculation.
        """
        self.view = view
        self.recalculation()

    def add_micro_object(self) -> None:
        """
        Show the window to add a new micro object.
        """
        self.view.show_new_micro_object_window()

    def create_micro_object(self) -> None:
        """
        Create a new micro object based on user input and save it.
        """
        latin_name, common_name, has_button, hotkey = self.view.get_new_class_data()
        if not has_button:
            hotkey = None
        new_micro_object = MicroObject(latin_name, common_name, 0, has_button, hotkey)
        fileControl.save_to_write_only_json(new_micro_object)
        print(f"Created: {new_micro_object}")
        self.recalculation()

    def show_image(self) -> None:
        """
        Update the view with the current image.
        """
        self.view.update_image(self.current_image)

    def next_image(self) -> None:
        """
        Load the next image and update the view.
        """
        img = fileControl.get_next_image()
        if img is None:
            self.view.show_no_images_left()
            self.current_image = None
            return
        self.view.destroy_show_no_images_left()
        self.current_image = img
        self.show_image()

    def find_new_images_form_dir(self) -> None:
        """
        Ask the user for a new image directory, copy images to process, and read them.
        """
        dir_path = self.view.ask_for_new_image_location()
        fileControl.copy_images_to_process(dir_path)
        fileControl.read_images_in_input_dir()
        self.next_image()

    def assign_classification(self, classification: object) -> None:
        """
        Assign a classification to the current image and update the history log.
        """
        self.current_image.set_classification(classification)
        self.current_image.set_is_classified(True)
        fileControl.save_image_micro_object(self.current_image)
        self.current_image.get_classification().found()

        # Update the history log
        image_name = self.current_image.get_name()
        new_path = os.path.join(globalVariables.OUTPUT_DIR, classification.get_latin_name())
        new_path = os.path.join(new_path, image_name)
        self.view.update_history_log(image_name, classification.get_common_name(), new_path)
        fileControl.remove_image(self.current_image.get_original_path())

        self.next_image()

    def recalculate_dict(self) -> None:
        """
        Recalculate the dictionary of micro objects without buttons.
        """
        self.micro_object_dict = {
            micro_object.get_common_name(): micro_object
            for micro_object in MicroObject.get_all_instances()
            if not micro_object.get_has_button()
        }

    def edit_micro_objects(self) -> None:
        """
        Show the window to edit micro objects.
        """
        self.view.show_edit_micro_objects_window()

    def edit_micro_object(self, micro_object: MicroObject) -> None:
        """
        Show the window to edit a specific micro object.
        """
        self.view.show_edit_micro_object_window(micro_object)

    def save_edited_micro_object(self, micro_object: MicroObject) -> None:
        """
        Save the edited micro object and update the view.
        """
        appearance = micro_object.get_appearance()
        latin_name, common_name, has_button, hotkey = self.view.get_edit_class_data()
        if not has_button:
            hotkey = None

        self.delete_micro_object(micro_object)
        edited = MicroObject(latin_name, common_name, appearance, has_button, hotkey)
        fileControl.save_to_write_only_json(edited)

        self.view.edit_micro_object_window.destroy()
        self.recalculation()

    def delete_micro_object(self, micro_object: MicroObject) -> None:
        """
        Delete a micro object and update the view.
        """
        MicroObject.instances.remove(micro_object)
        self.recalculation()

    def recalculation(self) -> None:
        """
        Recalculate the micro object dictionary and update the view.
        """
        self.recalculate_dict()
        self.recalculate_hotkey_list()

        micro_objects = MicroObject.get_all_instances()
        micro_objects_with_hotkeys = [micro_object for micro_object in micro_objects if micro_object.get_has_button()]
        micro_objects_without_hotkeys = [micro_object for micro_object in micro_objects if not micro_object.get_has_button()]

        self.view.unbind_hotkeys(micro_objects_with_hotkeys)
        self.view.recreate_buttons(micro_objects_with_hotkeys)
        self.view.recreate_selection_box(micro_objects_without_hotkeys)
        if self.view.edit_window is not None:
            self.view.recreate_edit_selection_box()

    def recalculate_hotkey_list(self) -> None:
        """
        Recalculate the list of available hotkeys by excluding those already assigned to micro objects.
        """
        globalVariables.available_hotkeys = [
            hotkey for hotkey in globalVariables.POSSIBLE_HOTKEYS
            if hotkey not in [
                micro_object.get_hotkey() for micro_object in MicroObject.get_all_instances()
                if micro_object.get_hotkey() is not None
            ]
        ]
