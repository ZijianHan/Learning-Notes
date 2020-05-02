from PIL import Image
import numpy as np



OUTPUT_WIDTH = 388#400
OUTPUT_HEIGHT = 518#300
IMAGE_PATH = ""
IMAGE_NAME = "test2.jpg"
OUTPUT_NAME = "test2_small.jpg"


image_original = Image.open(IMAGE_PATH+IMAGE_NAME)
image_original.show()
print('original size is: '+str(image_original.size))
print('Resized size is: '+str((OUTPUT_WIDTH, OUTPUT_HEIGHT)))
image_out = image_original.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT))
image_out.save(IMAGE_PATH+OUTPUT_NAME)
