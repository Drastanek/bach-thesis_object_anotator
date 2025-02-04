from src.MicroObject import MicroObject
import src.fileControl as fileControl
from src.UserInterfaceView import UserInterfaceView
import src.globalVariables as globalVariables
import os


def recalculate_hotkey_list():
    globalVariables.available_hotkeys = [hotkey
                                         for hotkey in globalVariables.POSSIBLE_HOTKEYS
                                         if hotkey not in [micro_object.get_hotkey()
                                                           for micro_object in MicroObject.get_all_instances()
                                                           if micro_object.get_hotkey() is not None]]


class MicroObjectController:
    view: UserInterfaceView | None
    current_image = None
    micro_object_dict = {}

    def __init__(self):
        self.view = None

    def set_view(self, view):
        self.view = view
        self.recalculation()

    def add_micro_object(self):
        self.view.show_new_micro_object_window()

    def create_micro_object(self):
        latin_name, common_name, has_button, hotkey = self.view.get_new_class_data()
        if not has_button:
            hotkey = None
        new_micro_object = MicroObject(latin_name, common_name, 0, has_button, hotkey)
        print(f"Created: {new_micro_object}")
        self.recalculation()

    def show_image(self):
        self.view.update_image(self.current_image)

    def next_image(self):
        img = fileControl.get_next_image()
        if img is None:
            self.view.show_no_images_left()
            self.current_image = None
            return
        self.view.destroy_show_no_images_left()
        self.current_image = img
        self.show_image()

    def find_new_images_form_dir(self):
        dir_path = self.view.ask_for_new_image_location()
        fileControl.copy_images_to_process(dir_path)
        fileControl.read_images_in_input_dir()
        self.next_image()

    def assign_classification(self, classification):
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

    def recalculate_dict(self):
        self.micro_object_dict = {micro_object.get_common_name():
                                  micro_object for micro_object in MicroObject.get_all_instances() if
                                  not micro_object.get_has_button()}

    def edit_micro_objects(self):
        self.view.show_edit_micro_objects_window()

    def edit_micro_object(self, micro_object):
        self.view.show_edit_micro_object_window(micro_object)

    def save_edited_micro_object(self, micro_object):
        appearance = micro_object.get_appearance()
        latin_name, common_name, has_button, hotkey = self.view.get_edit_class_data()
        if not has_button:
            hotkey = None

        self.view.unbind_hotkeys()
        self.delete_micro_object(micro_object)
        MicroObject(latin_name, common_name, appearance, has_button, hotkey)

        self.view.edit_micro_object_window.destroy()
        self.recalculation()

    def delete_micro_object(self, micro_object):
        self.view.unbind_hotkeys()
        MicroObject.instances.remove(micro_object)
        self.recalculation()
        self.view.close_edit_micro_object_window()

    def recalculation(self):
        self.recalculate_dict()
        recalculate_hotkey_list()
        self.view.recreate_buttons()
        self.view.recreate_selection_box()
        if self.view.edit_window is not None:
            self.view.recreate_edit_selection_box()
