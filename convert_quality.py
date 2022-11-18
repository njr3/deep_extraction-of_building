from PIL import Image
import os 


def change_qualitity_of_image(input_path , output_path):
    entries = os.listdir(input_path)
    for i in range(len(entries)):
        image_file = Image.open(input_path+entries[i])
        image_file.save(output_path+entries[i], quality=200)
    print('ok')