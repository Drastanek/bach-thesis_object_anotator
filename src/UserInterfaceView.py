import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk
from PIL import Image as PILImage
import platform
from typing import Tuple

import src.globalVariables as globalVariables
from src.MicroObject import MicroObject


class UserInterfaceView:
    """
    Class to handle the user interface of the MicroObject Viewer.
    """
    button_grid_column: int = 0 # column for the button grid
    button_grid_row: int = 0 # row for the button grid

    user_name: str = "Not_specified"

    def __init__(self, root: tk.Tk, controller) -> None:
        """
        Initialize the UserInterfaceView with the main Tkinter root and controller.
        """
        self.edit_window: tk.Toplevel = None
        self.edit_frame: tk.Frame = None
        self.edit_micro_object_window: tk.Toplevel = None
        self.image_label: tk.Label = None
        self.photo: ImageTk.PhotoImage = None
        self.selection_box: ttk.Combobox = None
        self.hotkey_combobox: ttk.Combobox = None
        self.hotkey_var: tk.StringVar = None
        self.has_button_var: tk.BooleanVar = None
        self.common_name_entry: tk.Entry = None
        self.latin_name_entry: tk.Entry = None
        self.new_window: tk.Toplevel = None
        self.history_listbox: tk.Listbox = None
        self.history_frame: tk.Frame = None
        self.controller = controller
        self.root = root
        self.root.title("MicroObject Viewer")
        self.root.configure(bg='gray')

        self.root.wm_state('normal')

        if platform.system() == 'Linux':
            self.root.wm_attributes('-zoomed', True)
        elif platform.system() == 'Windows':
            self.root.state('zoomed')

        # frame for the image
        self.image_frame = tk.Frame(self.root, bg='black')
        self.image_frame.pack(pady=20)

        # label for the image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # frame for the buttons and selection box
        self.control_frame = tk.Frame(self.root, bg='black')
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, anchor='center')

        # frame for object buttons (left side)
        self.object_button_frame = tk.Frame(self.control_frame, bg='black')
        self.object_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # frame for control buttons (right side)
        self.control_button_frame = tk.Frame(self.control_frame, bg='black')
        self.control_button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # create buttons and selection box
        self.recreate_buttons([])
        self.recreate_selection_box([])

        # skip button
        self.button_skip = tk.Button(self.control_button_frame, text="Skip\n(→)",
                                     command=self.controller.next_image, width=20, height=2)
        self.button_skip.pack(pady=5)
        self.root.bind('<KeyRelease-Right>', lambda event: self.controller.next_image())

        # edit microObjects button
        self.button_edit_class = tk.Button(self.control_button_frame, 
                                           text="Edit Class",
                                           command=self.controller.edit_micro_objects,
                                           width=20, height=2)
        self.button_edit_class.pack(pady=5)

        # new MicroObjects
        self.button_add_class = tk.Button(self.control_button_frame,
                                          text="Add Class",
                                          command=self.controller.add_micro_object, 
                                          width=20, height=2)
        self.button_add_class.pack(pady=5)

        # frame for the history pane
        self.history_frame = tk.Frame(self.root, bg='black')
        self.history_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # listbox for the history log
        self.history_listbox = tk.Listbox(self.history_frame, bg='white',
                                           fg='black', width=50, height=30)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbar for the history listbox
        scrollbar = tk.Scrollbar(self.history_frame, orient="vertical")
        scrollbar.config(command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)

# Create MicroObjects --------------------------------------------------------------------------------

    def show_new_micro_object_window(self) -> None:
        """
        Display a window to create a new MicroObject.
        """
        def toggle_hotkey_combobox() -> None:
            if self.has_button_var.get():
                self.hotkey_combobox.config(state='readonly')
            else:
                self.hotkey_combobox.config(state='disabled')

        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add New MicroObject")

        # latin name input
        tk.Label(self.new_window, text="Latin Name:").grid(row=0, column=0, padx=10, pady=5)
        self.latin_name_entry = tk.Entry(self.new_window)
        self.latin_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # common name input
        tk.Label(self.new_window, text="Common Name:").grid(row=1, column=0, padx=10, pady=5)
        self.common_name_entry = tk.Entry(self.new_window)
        self.common_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # has_button checkbox
        self.has_button_var = tk.BooleanVar()
        tk.Checkbutton(self.new_window, text="Has Button", variable=self.has_button_var,
                       command=toggle_hotkey_combobox).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # hotkey selection input
        tk.Label(self.new_window, text="Hotkey:").grid(row=3, column=0, padx=10, pady=5)
        self.hotkey_var = tk.StringVar()
        self.hotkey_combobox = ttk.Combobox(self.new_window, textvariable=self.hotkey_var, state='disabled')
        self.hotkey_combobox['values'] = ['None'] + globalVariables.available_hotkeys
        self.hotkey_combobox.grid(row=3, column=1, padx=10, pady=5)
        self.hotkey_combobox.current(0)  # Set default value to 'None'

        # Submit button
        tk.Button(self.new_window, text="Add", 
                  command=self.controller.create_micro_object).grid(row=4, 
                                                                    column=0,
                                                                    columnspan=2, 
                                                                    pady=10)

    def has_button_checkbox(self) -> None:
        """
        Create a checkbox for 'Has Button' and a combobox for hotkey selection.
        """
        def toggle_hotkey_combobox() -> None:
            if self.has_button_var.get():
                self.hotkey_combobox.config(state='readonly')
            else:
                self.hotkey_combobox.config(state='disabled')

        tk.Checkbutton(self.edit_micro_object_window, text="Has Button", variable=self.has_button_var,
                       command=toggle_hotkey_combobox).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # hotkey selection input
        tk.Label(self.edit_micro_object_window, text="Hotkey:").grid(row=3, column=0, padx=10, pady=5)
        self.hotkey_var = tk.StringVar()
        self.hotkey_combobox = ttk.Combobox(self.edit_micro_object_window, textvariable=self.hotkey_var,
                                            state='disabled')
        self.hotkey_combobox['values'] = ['None'] + globalVariables.available_hotkeys
        self.hotkey_combobox.grid(row=3, column=1, padx=10, pady=5)

    def get_new_class_data(self) -> Tuple[str, str, bool, str]:
        """
        Retrieve data for a newly created MicroObject class.
        """
        latin_name = self.latin_name_entry.get()
        common_name = self.common_name_entry.get()
        has_button = self.has_button_var.get()
        hotkey = self.hotkey_var.get()
        self.new_window.destroy()
        return latin_name, common_name, has_button, hotkey

# Edit MicroObjects --------------------------------------------------------------------------------

    def show_edit_micro_objects_window(self) -> None:
        """
        Display a window to edit existing MicroObjects.
        """
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit MicroObjects")
        self.edit_window.geometry("600x600")

        # Create a canvas for the scrollable window
        self.canvas = tk.Canvas(self.edit_window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self.edit_window, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to be scrollable
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        # Create a frame inside the canvas
        self.edit_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.edit_frame, anchor="nw")

        # Create table headers
        tk.Label(self.edit_frame, text="Common Name", font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.edit_frame, text="Latin Name", font=('Arial', 12, 'bold')).grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.edit_frame, text="Actions", font=('Arial', 12, 'bold')).grid(row=0, column=2, padx=10, pady=5)

        # Create a control items and button for each MicroObject
        micro_objects = MicroObject.get_all_instances()
        for i, micro_object in enumerate(micro_objects, start=1):
            tk.Label(self.edit_frame, text=micro_object.get_common_name()).grid(row=i, column=0, padx=10, pady=5)
            tk.Label(self.edit_frame, text=micro_object.get_latin_name()).grid(row=i, column=1, padx=10, pady=5)
            tk.Button(self.edit_frame, text="Edit",
                      command=lambda mo=micro_object: self.controller.edit_micro_object(mo)).grid(row=i, column=2, padx=5, pady=5)
            tk.Button(self.edit_frame, text="Delete", fg='red',
                      command=lambda mo=micro_object: self.controller.delete_micro_object(mo)).grid(row=i, column=3, padx=5, pady=5)

    def close_edit_micro_objects_window(self) -> None:
        """
        Close the edit MicroObjects window.
        """
        self.edit_window.destroy()

    def show_edit_micro_object_window(self, micro_object: MicroObject) -> None:
        """
        Display a window to edit a specific MicroObject.
        """
        self.edit_micro_object_window = tk.Toplevel(self.root)
        self.edit_micro_object_window.title("Edit MicroObject")

        # latin name input
        tk.Label(self.edit_micro_object_window, text="Latin Name:").grid(row=0, column=0, padx=10, pady=5)
        self.latin_name_entry = tk.Entry(self.edit_micro_object_window)
        self.latin_name_entry.insert(0, micro_object.get_latin_name())
        self.latin_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # common name input
        tk.Label(self.edit_micro_object_window, text="Common Name:").grid(row=1, column=0, padx=10, pady=5)
        self.common_name_entry = tk.Entry(self.edit_micro_object_window)
        self.common_name_entry.insert(0, micro_object.get_common_name())
        self.common_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # has_button checkbox
        self.has_button_var = tk.BooleanVar()
        self.has_button_var.set(micro_object.get_has_button())
        self.has_button_checkbox()
        if micro_object.get_hotkey():
            self.hotkey_combobox.set(micro_object.get_hotkey())
        else:
            self.hotkey_combobox.set('None')

        # Save button
        tk.Button(self.edit_micro_object_window, text="Save",
                  command=lambda: self.controller.save_edited_micro_object(micro_object)).grid(row=4, column=0,
                                                                                               columnspan=2,
                                                                                               pady=10)

    def get_edit_class_data(self) -> Tuple[str, str, bool, str]:
        """
        Retrieve data for editing a MicroObject class.
        """
        latin_name = self.latin_name_entry.get()
        common_name = self.common_name_entry.get()
        has_button = self.has_button_var.get()
        hotkey = self.hotkey_var.get()
        self.edit_micro_object_window.destroy()
        return latin_name, common_name, has_button, hotkey

    def recreate_edit_selection_box(self) -> None:
        """
        Recreate the selection box in the edit window.
        Used for updating after modifying MicroObjects. (eg. deleting)
        """
        # Clear existing selection box
        self.edit_window.destroy()

        self.show_edit_micro_objects_window()

# Image Handling main view --------------------------------------------------------------------------------

# Image Handling main view - No images left ---------------------------------------------------------------
    def update_image(self, image: PILImage) -> None:
        """
        Update the displayed image.
        
        param image: PILImage object to display
        """

        # Maximum dimensions for the displayed image
        # - image will not overflow into the other elemetns
        MAX_WIDTH = 500
        MAX_HEIGHT = 500

        if not hasattr(self, 'image_label') or not self.image_label.winfo_exists():
            self.photo = ImageTk.PhotoImage(PILImage.new('RGB', (MAX_WIDTH, MAX_HEIGHT), color='white'))
            self.image_label = tk.Label(self.image_frame, image=self.photo)
            self.image_label.pack()

        pil_image = PILImage.fromarray(image.image)

        # Scale down the image if it exceeds the maximum dimensions
        pil_image.thumbnail((MAX_WIDTH, MAX_HEIGHT), PILImage.LANCZOS)

        self.photo = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=self.photo)
        self.image_label.image = self.photo

    def show_no_images_left(self) -> None:
        """
        Display a message when no images are left.
        Giving option to user, to select a new image location.
        """
        # Clear the image frame
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Display a message
        message_label = tk.Label(self.image_frame, text="No images left.", bg='black', fg='white')
        message_label.pack(pady=10)

        # Add a button to select a new image location
        select_button = tk.Button(self.image_frame, text="Select New Image Location",
                                  command=self.controller.find_new_images_form_dir, bg='black', fg='white')
        select_button.pack(pady=10)

    def ask_for_new_image_location(self) -> str:
        """
        Ask the user to select a new directory for images.
        Executed when no images are left in the globalVariables.INPUT_PROCESS_DIR.

        return: path to the new image location
        """
        new_image_path = filedialog.askdirectory(
            title="Select Directory for New Images",
            parent=self.root,
            mustexist=True
        )
        return new_image_path

    def destroy_show_no_images_left(self) -> None:
        """
        Destroy the 'No images left' message and button.
        """
        for widget in self.image_frame.winfo_children():
            widget.destroy()

# Image Handling main view - Helping classes for managing the view --------------------------------------
    def recreate_buttons(self, micro_objects_with_hotkeys: list[MicroObject]) -> None:
        """
        Recreate the buttons for MicroObjects.
        Used to update the buttons after modifying MicroObjects. (eg. adding, deleting)
        """
        # Clear existing buttons
        for widget in self.object_button_frame.winfo_children():
            widget.destroy()

        self.button_grid_column = 0
        self.button_grid_row = 0
        for micro_object in micro_objects_with_hotkeys:
            self.add_micro_object_button(micro_object)

    def unbind_hotkeys(self, micro_objects_with_hotkeys: list[MicroObject]) -> None:
        """
        Unbind all old key bindings.
        Used to update the key bindings after modifying MicroObjects (eg. adding, deleting),
        so the old bindings do not interfere with the new ones.
        """
        for micro_object in micro_objects_with_hotkeys:
            self.root.unbind(micro_object.get_hotkey().lower())

    def add_micro_object_button(self, micro_object: MicroObject) -> None:
        """
        Add a button for a MicroObject with has_button atribute.
        """
        # button text
        button_text = f"{micro_object.get_latin_name()}\n{micro_object.get_common_name()}"
        if micro_object.get_hotkey():
            button_text += f" ({micro_object.get_hotkey()})"
        
        # create the button with controller function assignment
        button = tk.Button(self.object_button_frame,
                           text=button_text,
                           command=lambda: self.controller.assign_classification(micro_object),
                           width=20, height=2)
        
        # bind hotkey to the button if required
        if micro_object.get_hotkey() and micro_object.get_hotkey().lower() != 'none':
            self.root.bind(f'<KeyRelease-{micro_object.get_hotkey().lower()}>',
                           lambda event, mo=micro_object: self.controller.assign_classification(mo))
        
        # place button into the view grid
        button.grid(row=self.button_grid_row, column=self.button_grid_column, pady=5)
        self.button_grid_row += 1
        if self.button_grid_row >= 5:
            self.button_grid_row = 0
            self.button_grid_column += 2

    def recreate_selection_box(self, micro_objects_without_hotkeys: list[MicroObject]) -> None:
        """
        Recreate the selection box for MicroObjects without has_button atribute.
        Used to update the selection box after modifying MicroObjects. (eg. adding, deleting)
        """
        # Clear existing selection box
        for widget in self.control_frame.winfo_children():
            if isinstance(widget, ttk.Combobox):
                widget.destroy()
            if isinstance(widget, tk.Button) and widget.cget('text') == "Confirm\n(Enter)":
                widget.destroy()

        names = [micro_object.get_common_name() for micro_object in micro_objects_without_hotkeys]

        self.selection_box = ttk.Combobox(self.control_frame, values=names, width=20, height=2)
        self.selection_box.pack(pady=5)
        if names:
            self.selection_box.current(0)

        # confirm button
        self.button_confirm = tk.Button(self.control_frame, text="Confirm\n(Enter)",
                                        command=self.confirm_selection, width=20, height=2)
        self.button_confirm.pack(pady=5)
        self.root.bind('<KeyRelease-Return>', lambda event: self.confirm_selection())

    def confirm_selection(self) -> None:
        """
        Confirm the selected MicroObject from the selection box.
        """
        selected_common_name = self.selection_box.get()
        selected_micro_object = self.controller.micro_object_dict.get(selected_common_name)
        if selected_micro_object:
            self.controller.assign_classification(selected_micro_object)

    def update_history_log(self, image_name: str, classification: str, storage_path: str) -> None:
        """
        Update the history log with a new entry.
        """
        log_entry = f"{image_name} - {classification} - {storage_path}"
        self.history_listbox.insert(0, log_entry)

