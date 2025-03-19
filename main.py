import tkinter as tk
from src.UserInterfaceView import UserInterfaceView
from src.UserInterfaceController import MicroObjectController
from src import MicroObject
import src.fileControl as fileControl
import src.globalVariables as globalVariables
from src.fileControl import check_path, check_file

def setup_ui() -> None:
    """
    Set up the user interface and start the main loop.
    """
    root = tk.Tk()
    controller = MicroObjectController()
    view = UserInterfaceView(root, controller)
    controller.set_view(view)
    controller.next_image()
    root.mainloop()

def main() -> None:
    """
    Main function to initialize directories, load data, set up the UI, and save data.
    """
    # Check and create necessary directories
    check_path(globalVariables.DATA_DIR)
    check_path(globalVariables.OUTPUT_DIR)
    check_path(globalVariables.INPUT_PROCESS_DIR)
    
    # Check and create necessary files
    check_file(globalVariables.MICRO_OBJECTS_JSON)
    check_file(globalVariables.WRITE_ONLY_MICRO_OBJECTS_JSON)
    
    # Load object classes from JSON file
    fileControl.load_object_classes_from_json(globalVariables.MICRO_OBJECTS_JSON)

    # Set up the user interface
    setup_ui()

    # Get all instances of MicroObject
    all_instances = MicroObject.MicroObject.get_all_instances()

    # Print all instances
    for obj in all_instances:
        print(obj)

    # Save object classes to JSON file
    fileControl.save_object_classes_to_json(all_instances, globalVariables.MICRO_OBJECTS_JSON)

if __name__ == '__main__':
    main()
