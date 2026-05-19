from PIL import Image
import os

folder = "your_folder"
output_folder = "/opt/icons/"

for filename in os.listdir(folder):
    if filename.endswith(".tiff"):
        full_path = os.path.join(folder, filename)

        im = Image.open(full_path)

        new_im = im.rotate(90).resize((128, 128))

        name, extension = os.path.splitext(filename)
        new_name = name + ".jpeg"
        new_im.save(os.path.join(output_folder, new_name))