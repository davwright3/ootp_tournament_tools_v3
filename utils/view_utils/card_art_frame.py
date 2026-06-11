import tkinter as tk
import os
from pathlib import Path
from utils.config_utils.load_save_settings import get_setting
from PIL import Image, ImageTk



class CardArtFrame(tk.Frame):
    def __init__(self, parent, selected_card_id=None, max_width=None):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)

        self.image_label = tk.Label(self)
        self.image_label.grid(row=0, column=0, sticky='nsew')

        if selected_card_id is not None:
            self.update_frame(selected_card_id, max_width)

    def update_frame(self, selected_card_id, max_width=None):
        try:
            card_list_path = (
                get_setting('TargetFiles', 'target_card_list'))
            data_dir = Path(
                os.path.join(os.path.dirname(card_list_path), r'cache\cards'))
            target_string = str(selected_card_id)
            matching_file = next(file.name for file in data_dir.iterdir() if
                                 file.name.startswith(target_string))
            if matching_file:
                pil_image = Image.open(os.path.join(data_dir, matching_file))
                if max_width:
                    if pil_image.width > max_width:
                        ratio = max_width / pil_image.width
                        new_height = int(pil_image.height * ratio)
                        pil_image = (
                            pil_image.resize((max_width, new_height),
                                                     Image.LANCZOS))
                tk_image = ImageTk.PhotoImage(pil_image)
                self.image_label.configure(image=tk_image)
                self.image_label.image = tk_image

        except FileNotFoundError:
            self.image_label.configure(text='Card not found')

        except Exception as e:
            self.image_label.configure(text=str(e))

