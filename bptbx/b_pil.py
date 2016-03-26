r"""Wrapper for operations using Python image library (PIL)""" 

from os import path
from re import compile

from PIL import Image


GIF_PATTERN = compile('^.*\\.gif$')
"""Pattern for GIF files"""

def get_length_of_long_side (source_image):
    """Returns the number of pixels of the long side of the image"""
    image = Image.open(source_image)
    width, height = image.size
    if (width > height):
        return width
    else:
        return height
    
def resize_image_with_factor (source_image, target_image, factor):
    """Reads the image width and height from the given image and
    resizes the file to the given target file using the provided 
    resize factor"""
     
    if not source_image:
        raise TypeError ('source_image not set')
    if not target_image:
        raise TypeError ('target_image not set')
    if not path.exists(source_image):
        raise TypeError ('source_image does not exist')
    if not path.exists(path.dirname(target_image)):
        raise TypeError ('Folder for target_image does not exist')
     
    image = Image.open(source_image)
    width, height = image.size
    width_new = int(float(width) * factor)
    height_new = int(float(height) * factor)

    image = image.resize((width_new, height_new), Image.ANTIALIAS) 
    if GIF_PATTERN.match(target_image.lower()):
        image.save(target_image, 'GIF')
    else:
        image.save (target_image, 'JPEG')
     
    return width_new, height_new
