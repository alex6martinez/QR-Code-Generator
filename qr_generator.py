import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import qrcode


# App(ctk.CTk) -> In here App is inheriting ctk.CTk class
class App(ctk.CTk):
    # Class initialization function
    def __init__(self):
        # Window Setup
        ctk.set_appearance_mode("light")
        super().__init__(fg_color="white")

        # Customization
        self.title("")
        self.iconbitmap(r"C:\Users\amartinez\Desktop\python\tkinter\QR_Code\empty.ico")
        self.geometry("400x400")

        # Entry field
        self.entry_string = ctk.StringVar()
        self.entry_string.trace("w", self.create_qr)
        EntryField(self, self.entry_string, self.save)

        # Save
        self.bind("<Return>", self.save)

        # QR Code
        self.raw_image = None
        self.tk_image = None
        self.qr_image = QrImage(self)

        # Running the App
        self.mainloop()

    def create_qr(self, *args):
        current_text = self.entry_string.get()
        if current_text:
            self.raw_image = qrcode.make(current_text).resize((200, 200))
            self.tk_image = ImageTk.PhotoImage(self.raw_image)
            self.qr_image.update_image(self.tk_image)
        else:
            self.qr_image.clear()
            self.raw_image = None
            self.tk_image = None

    def save(self, event=""):
        if self.raw_image:
            file_path = filedialog.asksaveasfilename()
            if file_path:
                self.raw_image.save(file_path + ".jpg")


class EntryField(ctk.CTkFrame):
    def __init__(self, parent, entry_string, save_func):
        super().__init__(master=parent, corner_radius=20, fg_color="#021fb3")
        self.place(relx=0.5, rely=1, relwidth=1, relheight=0.4, anchor="center")

        # Grid Layout
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

        # Widgets
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.columnconfigure(0, weight=1, uniform="b")
        self.frame.columnconfigure(1, weight=4, uniform="b")
        self.frame.columnconfigure(2, weight=2, uniform="b")
        self.frame.columnconfigure(3, weight=1, uniform="b")
        self.frame.grid(row=0, column=0)

        # Entry and Button Widgets
        entry = ctk.CTkEntry(
            self.frame,
            textvariable=entry_string,
            fg_color="#2e54e8",
            border_width=0,
            text_color="white",
        )
        entry.grid(row=0, column=1, sticky="nsew")
        button = ctk.CTkButton(
            self.frame,
            text="Save",
            command=save_func,
            fg_color="#2e54e8",
            hover_color="#4266f1",
        )
        button.grid(row=0, column=2, sticky="nsew", padx=10)


class QrImage(tk.Canvas):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            background="white",
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.place(relx=0.5, rely=0.4, width=200, height=200, anchor="center")

    def update_image(self, image_tk):
        self.clear()  # we add this here because what is happenning is that a new image is being generated
        # and superimposed in the previous image, so we clear the previous image before adding a new one
        self.create_image(0, 0, image=image_tk, anchor="nw")

    def clear(self):
        self.delete("all")


App()
