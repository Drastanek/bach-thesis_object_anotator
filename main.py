import tkinter as tk
from src.UserInterfaceView import UserInterfaceView
from src.UserInterfaceController import MicroObjectController
from src import MicroObject
import src.fileControl as fileControl
import src.globalVariables as globalVariables
from src.fileControl import check_path, check_file

def setup_ui():
    root = tk.Tk()
    controller = MicroObjectController()
    view = UserInterfaceView(root, controller)
    controller.set_view(view)
    controller.next_image()
    root.mainloop()


def main():
    check_path(globalVariables.DATA_DIR)
    check_path(globalVariables.OUTPUT_DIR)
    check_path(globalVariables.INPUT_PROCESS_DIR)
    check_file(globalVariables.MICRO_OBJECTS_JSON)
    check_file(globalVariables.WRITE_ONLY_MICRO_OBJECTS_JSON)
    fileControl.load_object_classes_from_json(globalVariables.MICRO_OBJECTS_JSON)

    setup_ui()

    all_instances = MicroObject.MicroObject.get_all_instances()

    for obj in all_instances:
        print(obj)

    fileControl.save_object_classes_to_json(all_instances, globalVariables.MICRO_OBJECTS_JSON)


if __name__ == '__main__':
    main()
