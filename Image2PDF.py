import os
from tkinter import filedialog, Scrollbar, Toplevel, Canvas, ttk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

class ImageToPdfConverter:
    def __init__(self, root):
        self.root = root
        self.root.geometry('720x450')
        self.root.minsize(300, 300)
        self.root.maxsize(1280, 720)
        self.root.title('Image to PDF Converter - SZRXAI')
        self.image_list = []
        self.image_names = []

        
        self.root.configure(background='#283635')

        # Change fonts
        self.default_font = "Arial"
        self.default_font_size = 12

        self.open_button = Button(root, text='Open Folder', command=self.open_folder, font=(self.default_font, self.default_font_size))
        self.open_button.pack()

        self.submit_button = Button(root, text='Submit', command=self.convert_to_pdf, font=(self.default_font, self.default_font_size))
        self.submit_button.pack()

        self.settings_button = Button(root, text='Settings', command=self.open_settings, font=(self.default_font, self.default_font_size))
        self.settings_button.pack()

        self.clear_button = Button(root, text='Clear', command=self.clear_images, font=(self.default_font, self.default_font_size))
        self.clear_button.pack()

        self.text_box = Text(root, state='disabled', font=(self.default_font, self.default_font_size))
        self.text_box.pack(fill=BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.top_level = None
        self.resolution = IntVar(value=50)

        thisdir = os.path.dirname(__file__)

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        for file_name in os.listdir(folder_path):
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                image_path = os.path.join(folder_path, file_name)
                self.image_names.append(file_name)
                self.image_list.append(image_path)

                self.update_text_box(file_name)

    def update_text_box(self, msg):
        self.text_box.configure(state='normal')
        self.text_box.insert(END, msg + '\n')
        self.text_box.configure(state='disabled')
        self.text_box.configure(bg='#2A363B', fg='white')

    def convert_to_pdf(self):
        if self.image_list:
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
            if file_path:
                images_to_convert = [Image.open(image) for image in self.image_list]
                images_to_convert[0].save(file_path, "PDF", resolution=self.resolution.get(),
                                          save_all=True,
                                          append_images=images_to_convert[1:],
                                          quality=int(self.resolution.get()))

                # Show messagebox that the conversion is successful
                messagebox.showinfo("Success", "Images converted to PDF successfully!")
                
        else:
            # Show messagebox if there are no images
            messagebox.showerror("Error", "No images found!")

    def open_settings(self):
        if self.top_level:
            self.top_level.destroy()
            self.top_level = None
        else:
            self.top_level = Toplevel(self.root)
            self.top_level.title('Settings')
            self.top_level.geometry('200x200')
            self.top_level.minsize(200, 200)
            self.top_level.maxsize(300, 300)
            self.top_level.configure(background='#283635')

            def change_resolution(res):
                self.resolution.set(res)

            def save_settings():
                # Show messagebox that settings are saved
                messagebox.showinfo("Success", "Settings saved!")
                

            resolution_label = Label(self.top_level, text='PDF Size\n(50 is the best option)', font=(self.default_font, self.default_font_size), bg="#283635", fg="white")
            resolution_label.pack()

            resolution_slider = Scale(self.top_level, from_=50, to=300, orient=HORIZONTAL, command=change_resolution,
                                          font=(self.default_font, self.default_font_size), bg='#283635', fg='white')
            resolution_slider.set(self.resolution.get())
            resolution_slider.pack()

            save_button = Button(self.top_level, text='Save', command=save_settings, font=(self.default_font, self.default_font_size))
            save_button.pack()

    def clear_images(self):
        self.image_list = []
        self.image_names = []
        self.text_box.configure(state='normal')
        self.text_box.delete("1.0", END)
        self.text_box.configure(state='disabled')

root = Tk()
app = ImageToPdfConverter(root)
root.mainloop()