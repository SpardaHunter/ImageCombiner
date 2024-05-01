from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_blank_image():
    global blank_image_path
    blank_image_path = filedialog.askopenfilename(title="Select Image")
    blank_image_path_entry.delete(0, tk.END)
    blank_image_path_entry.insert(0, blank_image_path)

def select_images_directory():
    global images_directory
    images_directory = filedialog.askdirectory(title="Image Folder")
    images_directory_entry.delete(0, tk.END)
    images_directory_entry.insert(0, images_directory)

def select_output_directory():
    global output_directory
    output_directory = filedialog.askdirectory(title="Output Folder")
    output_directory_entry.delete(0, tk.END)
    output_directory_entry.insert(0, output_directory)

def process_images():
    if not os.path.exists(blank_image_path) or not os.path.exists(images_directory):
        messagebox.showerror("Error", "Select the image and ROMS folder before processing.")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    blank_image = Image.open(blank_image_path)

    for filename in os.listdir(images_directory):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            current_image_path = os.path.join(images_directory, filename)
            current_image = Image.open(current_image_path)

            width, height = current_image.size
            new_height = int(height * 0.2)
            new_width = width

            blank_resized = blank_image.resize((new_width, new_height))

            combined_image = Image.new('RGB', (width, height + new_height))
            combined_image.paste(current_image, (0, 0))
            combined_image.paste(blank_resized, (0, height))

            output_path = os.path.join(output_directory, filename)
            combined_image.save(output_path)

    messagebox.showinfo("Process completed", "Edited images saved in the output directory.")

# Crear la ventana principal
root = tk.Tk()
root.title("Image Processor")

# Variables globales para las rutas de los directorios
blank_image_path = ""
images_directory = ""
output_directory = ""

# Crear y colocar widgets en la ventana
# Seleccionar Imagen
blank_image_frame = tk.Frame(root)
blank_image_frame.pack(pady=10)

blank_image_label = tk.Label(blank_image_frame, text="Select Image")
blank_image_label.pack(side=tk.LEFT, padx=(10, 5))

blank_image_path_entry = tk.Entry(blank_image_frame, width=50)
blank_image_path_entry.pack(side=tk.LEFT)

blank_image_button = tk.Button(blank_image_frame, text="Explore", command=select_blank_image)
blank_image_button.pack(side=tk.LEFT, padx=(5, 10))

# Seleccionar Carpeta ROMS
images_directory_frame = tk.Frame(root)
images_directory_frame.pack(pady=10)

images_directory_label = tk.Label(images_directory_frame, text="Image Folder")
images_directory_label.pack(side=tk.LEFT, padx=(10, 5))

images_directory_entry = tk.Entry(images_directory_frame, width=50)
images_directory_entry.pack(side=tk.LEFT)

images_directory_button = tk.Button(images_directory_frame, text="Explore", command=select_images_directory)
images_directory_button.pack(side=tk.LEFT, padx=(5, 10))

# Seleccionar Carpeta OUTPUT
output_directory_frame = tk.Frame(root)
output_directory_frame.pack(pady=10)

output_directory_label = tk.Label(output_directory_frame, text="Output Folder")
output_directory_label.pack(side=tk.LEFT, padx=(10, 5))

output_directory_entry = tk.Entry(output_directory_frame, width=50)
output_directory_entry.pack(side=tk.LEFT)

output_directory_button = tk.Button(output_directory_frame, text="Explore", command=select_output_directory)
output_directory_button.pack(side=tk.LEFT, padx=(5, 10))

# Procesar Imágenes
process_button = tk.Button(root, text="Process Images", command=process_images)
process_button.pack(pady=20)

root.mainloop()
