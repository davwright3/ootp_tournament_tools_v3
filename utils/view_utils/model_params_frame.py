"""Custom frame for setting modeling parameters"""
import tkinter as tk

class ModelParametersFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_model = tk.StringVar(value="RidgeCV")

        # Alpha variables for RidgeCV model
        self.alpha_one = tk.StringVar(value="0.1")
        self.alpha_two = tk.StringVar(value="1.0")
        self.alpha_three = tk.StringVar(value="10.0")
        self.alpha_four = tk.StringVar(value="100.0")
        self.cv_set = tk.StringVar(value="3")
        self.test_size = tk.StringVar(value="0.2")

        self.columnconfigure(0, weight=1)

        def set_model_params_frame():
            if self.selected_model.get() == 'RidgeCV':
                widgets = self.params_input_frame.winfo_children()
                for widget in widgets:
                    widget.destroy()

                self.alphas_label = tk.Label(self.params_input_frame, text="Alphas")
                self.alphas_label.grid(row=0, column=0, padx=1, pady=1, columnspan=4)

                self.alpha_one_entry = tk.Entry(self.params_input_frame, width=10, textvariable=self.alpha_one)
                self.alpha_one_entry.grid(row=1, column=0, padx=1, pady=1)

                self.alpha_two_entry = tk.Entry(self.params_input_frame, width=10, textvariable=self.alpha_two)
                self.alpha_two_entry.grid(row=1, column=1, padx=1, pady=1)

                self.alpha_three_entry = tk.Entry(self.params_input_frame, width=10, textvariable=self.alpha_three)
                self.alpha_three_entry.grid(row=1, column=2, padx=1, pady=1)

                self.alpha_four_entry = tk.Entry(self.params_input_frame, width=10, textvariable=self.alpha_four)
                self.alpha_four_entry.grid(row=1, column=3, padx=1, pady=1)

                self.cv_label = tk.Label(self.params_input_frame, text="CV")
                self.cv_label.grid(row=0, column=4, padx=1, pady=1)

                self.cv_entry = tk.Entry(self.params_input_frame, width=10, textvariable=self.cv_set)
                self.cv_entry.grid(row=1, column=4, padx=1, pady=1)

                self.test_size_label = tk.Label(self.params_input_frame, text="Test Size")
                self.test_size_label.grid(row=0, column=5, padx=1, pady=1)

                self.test_size_entry = tk.Entry(self.params_input_frame, width=10, textvariable=self.test_size)
                self.test_size_entry.grid(row=1, column=5, padx=1, pady=1)

        # Frame for selecting model to use (add new models later)
        self.select_model_frame = tk.Frame(self)
        self.select_model_frame.grid(row=0, column=0, padx=10, pady=10)

        self.select_ridge_cv_button = tk.Radiobutton(
            self.select_model_frame,
            text="RidgeCV",
            variable=self.selected_model,
            value='RidgeCV',
            command=set_model_params_frame

        )
        self.select_ridge_cv_button.grid(row=0, column=0)

        self.params_input_frame = tk.Frame(self)
        self.params_input_frame.grid(row=1, column=0, padx=10, pady=10)

        set_model_params_frame()

    def get_params(self):
        if self.selected_model.get() == 'RidgeCV':
            try:
                alpha_one = float(self.alpha_one.get())
                alpha_two = float(self.alpha_two.get())
                alpha_three = float(self.alpha_three.get())
                alpha_four = float(self.alpha_four.get())
                alphas = [
                    alpha_one, alpha_two, alpha_three, alpha_four
                ]
            except ValueError:
                alphas = [0.1, 1.0, 10.0, 100.0]

            try:
                cv = int(self.cv_set.get())
            except ValueError:
                cv = 3

            try:
                test_size = float(self.test_size.get())
                if not 0.1 <= test_size <= 0.4:
                    test_size = 0.2
            except ValueError:
                test_size = 0.2


            return alphas, cv, test_size
