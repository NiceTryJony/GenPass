import customtkinter as CTk
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import tkinter as tk
import tkinter
from tkinter import filedialog, messagebox
from PIL import Image
import random
import os

class AppP(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("660x330")
        self.title("Password Generator")
        self.resizable(False, False)

        self.password_frame = CTk.CTkFrame(master=self, fg_color="transparent")
        self.password_frame.grid(row=1, column=0, padx=(20,20), sticky="nsew")

        self.password_name_label = CTk.CTkLabel(master=self.password_frame, text=" PASSWORD NAME")
        self.password_name_label.grid(row=0, column=0, padx=(0,10), pady=(10,0))

        self.entry_password_name = CTk.CTkEntry(master=self.password_frame, width=200)
        self.entry_password_name.grid(row=1, column=0, padx=(0,10))

        self.password_label = CTk.CTkLabel(master=self.password_frame, text=" GENERATE PASSWORD")
        self.password_label.grid(row=0, column=2, padx=(0,10), pady=(10,0))

        self.entry_password = CTk.CTkEntry(master=self.password_frame, width=200)
        self.entry_password.grid(row=1, column=2, padx=(10,20))

        self.btn_generate = CTk.CTkButton(master=self.password_frame, 
                                        text="Generate Password", width=75, 
                                        command=self.set_password)
        self.btn_generate.grid(row=2, column=2, columnspan=1, padx=(10, 10), pady=(10,10))


        self.settings_frame = CTk.CTkFrame(master=self)
        self.settings_frame.grid(row=3, column=0, padx=(20, 0), sticky="nsew", pady=(5))

        self.password_lenght_slider = CTk.CTkSlider(master=self.settings_frame, from_=0, to=50, number_of_steps=100, command=self.slider_event)

        self.password_lenght_slider.grid(row=3, column=0, columnspan=3, padx=(20, 20), sticky="ew")

        self.password_lenght_entry = CTk.CTkEntry(master=self.settings_frame, width = 50)
        self.password_lenght_entry.grid(row=3, column=3, padx=(20,10), sticky="we", pady=(10))

        self.cb_digits_var = tkinter.StringVar()
        self.cb_digits = CTk.CTkCheckBox(master=self.settings_frame, text="0-9", 
                                         variable=self.cb_digits_var, 
                                         onvalue=digits, offvalue="")

        self.cb_digits.grid(row=4, column=0, padx=10, pady=(5))

        self.cb_lower_var = tkinter.StringVar()
        self.cb_lower = CTk.CTkCheckBox(master=self.settings_frame, text="a-z", 
                                        variable=self.cb_lower_var,  
                                        onvalue=ascii_lowercase, offvalue="")

        self.cb_lower.grid(row=4, column=1, pady=(5))

        self.cb_upper_var = tkinter.StringVar()
        self.cb_upper = CTk.CTkCheckBox(master=self.settings_frame, text="A-Z", 
                                        variable=self.cb_upper_var, 
                                        onvalue=ascii_uppercase, offvalue="")

        self.cb_upper.grid(row=4, column=2, pady=(5))

        self.cb_symbol_var = tkinter.StringVar()
        self.cb_symbol = CTk.CTkCheckBox(master=self.settings_frame, text="@#$%", 
                                         variable=self.cb_symbol_var, 
                                         onvalue="!@#$%&", offvalue="")

        self.cb_symbol.grid(row=4, column=3, pady=(5))

        self.save_frame = CTk.CTkFrame(master=self)
        self.save_frame.grid(row=5, column=0, padx=(20, 0), sticky="nsew")

        self.save_label = CTk.CTkLabel(master=self.save_frame, text="Save passwords to:")
        self.save_label.grid(row=0, column=0, padx=(10, 10))

        self.save_entry = CTk.CTkEntry(master=self.save_frame, width=300)
        self.save_entry.grid(row=0, column=1, padx=(10, 10))

        self.save_button = CTk.CTkButton(master=self.save_frame, text="Browse", command=self.browse_directory)
        self.save_button.grid(row=0, column=2, padx=(10, 10))

        self.open_button = CTk.CTkButton(master=self.save_frame, text="Open PASSWORDS", command=self.open_passwords)
        self.open_button.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(10))

        self.save_password_button = CTk.CTkButton(master=self.password_frame, text="Save Password", command=self.save_password)
        self.save_password_button.grid(row=2, column=0, columnspan=1, padx=(10, 10))

        self.password_lenght_slider.set(12)
        self.password_lenght_entry.insert(0, 12)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.save_entry.delete(0, "end")
        self.save_entry.insert(0, directory)
        self.save_directory(directory)

    def open_passwords(self):
        directory = self.save_entry.get()
        if directory:
            file_path = os.path.join(directory, "passwords.txt")
            if os.path.exists(file_path):
                messagebox.showinfo("Open File", "Do you want to open the file with Notepad or default text editor?")
                if messagebox.askyesno("Open File", "Open with Notepad?"):
                    os.startfile(file_path, "open -a Notepad")
                else:
                    os.startfile(file_path)
            else:
                messagebox.showerror("Error", "File not found")
        else:
            messagebox.showerror("Error", "Select a directory to save passwords")

    def save_directory(self, directory):
        with open("directory.txt", "w") as file:
            file.write(directory)

    def load_directory(self):
        try:
            with open("directory.txt", "r") as file:
                return file.read()
        except FileNotFoundError:
            return ""
        
    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)

    def slider_event(self, value):
        self.password_lenght_entry.delete(0, "end")
        self.password_lenght_entry.insert (0, int(value))

    def set_password(self):
        password_length = int(self.password_lenght_entry.get())
        password_characters = self.cb_digits_var.get() + self.cb_lower_var.get() + self.cb_upper_var.get() + self.cb_symbol_var.get()
        if password_characters:
            password = ''.join(random.choice(password_characters) for _ in range(password_length))
            self.entry_password.delete(0, "end")
            self.entry_password.insert(0, password)
        else:
            messagebox.showerror("Error", "Select at least one character type")

    def save_password(self):
        password_name = self.entry_password_name.get()
        password = self.entry_password.get()
        if password_name and password:
            directory = self.save_entry.get()
            if directory:
                try:
                    with open(directory + "/passwords.txt", "a") as file:
                        file.write(f"{password_name}. {password}\n\n")
                    messagebox.showinfo("Success", "Password saved successfully")
                except FileNotFoundError:
                    messagebox.showerror("Error", "File not found")
            else:
                messagebox.showerror("Error", "Select a directory to save passwords")
        else:
            messagebox.showerror("Error", "Enter password name and password")

if __name__ == "__main__":
    app = AppP()
    app.mainloop()