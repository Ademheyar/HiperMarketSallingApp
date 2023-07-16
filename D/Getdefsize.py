import tkinter as tk

class ButtonEntryApp(tk.Toplevel):
    def __init__(self, root, main_app):
        self.a = super().__init__(root)
        self.result = []
        self.title("Size Manager")
        self.geometry("500x300")
        self.main_app = main_app

        self.first_frame = tk.Frame(self)
        self.first_frame.pack(pady=10)

        self.second_frame = tk.Frame(self)
        self.second_frame.pack(pady=10)

        self.sizeing_type = tk.StringVar()  # Variable to store the selected sizing type
        self.sizeing_type.set("Select Sizing Type")

        self.sizeing_type_label = tk.Label(self.first_frame, text="Select Sizing Type:")
        self.sizeing_type_label.pack(side=tk.LEFT)
        
        sizing_options = ["Trouser Sizes", "Clothing Sizes", "Shoe Sizes"]

        self.sizing_var = tk.StringVar()
        self.sizing_var.set("Select Size Type")
        sizing_menu = tk.OptionMenu(self.first_frame, self.sizing_var, *sizing_options)
        sizing_menu.pack()

        self.create_form_button = tk.Button(self.first_frame, text="Create Form", command=self.create_sizes_form)
        self.create_form_button.pack(side=tk.LEFT)

        self.form_frame = tk.Frame(self.second_frame)  # Frame to hold the form entries
        self.form_frame.pack(pady=10)

        self.form_entries = []  # List to store the form entries
        
        self.master.wait_window(self)
    
    def create_sizes_form(self):
        selected_type = self.sizing_var.get()
        if selected_type == "Select Sizing Type":
            return

        self.form_frame.destroy()  # Clear previous form entries

        self.form_frame = tk.Frame(self.second_frame)
        self.form_frame.pack(pady=10)

        self.form_entries = []  # Reset the list of form entries

        sizes_label = tk.Label(self.form_frame, text="Enter Quantities for the Sizes:")
        sizes_label.pack()

        sizes_text = tk.Text(self.form_frame, height=5, width=40)
        sizes_text.pack()

        sizes = []
        if selected_type == "Trouser Sizes":
            sizes = [str(size) + ":0" for size in range(21, 46)]
        elif selected_type == "Clothing Sizes":
            sizes = ["XS:0", "S:0", "M:0", "L:0", "XL:0", "2XL:0", "3XL:0", "4XL:0", "5XL:0"]
        elif selected_type == "Shoe Sizes":
            sizes = [str(size) + ":0" for size in range(1, 13)] + [str(a) + ":0" for a in range(30, 45)]

        for size in sizes:
            sizes_text.insert(tk.END, size + ", ")

        done_button = tk.Button(self.form_frame, text="Done", command=lambda: self.generate_list(selected_type, sizes_text.get("1.0", tk.END)))
        done_button.pack()

    def generate_list(self, sizing_type, sizes):
        sizes_list = sizes.strip().split(",")  # Split the entered sizes by comma
        sizes_list = [size.strip() for size in sizes_list]  # Remove leading/trailing whitespaces

        self.result = []
        for size in sizes_list:
            size_parts = size.split(":")
            if len(size_parts) == 2:
                size_value = size_parts[0].strip()
                quantity = size_parts[1].strip()
                if quantity != "0":
                    self.result.append([size_value, quantity])
        
        self.destroy()  # Close the ButtonEntryApp window