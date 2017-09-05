"""Wrapper for operations using Python image library PIL"""

from os import path
from re import compile

from PIL import Image


GIF_PATTERN = compile('^.*\\.gif$')


def get_length_of_long_side(source_image):
    """Returns the number of pixels of the long side of the image"""
    image = Image.open(source_image)
    width, height = image.size
    image.close()
    if (width > height):
        return width
    else:
        return height


def resize_image_with_factor(source_image, target_image, factor):
    """Reads the image width and height from the given image and
    resizes the file to the given target file using the provided
    resize factor"""

    if not source_image:
        raise TypeError('source_image not set')
    if not target_image:
        raise TypeError('target_image not set')
    source_image = path.abspath(source_image)
    target_image = path.abspath(target_image)
    if not path.exists(source_image):
        raise TypeError('source_image does not exist')
    if not path.exists(path.dirname(target_image)):
        raise TypeError('Folder for target_image does not exist')

    image = Image.open(source_image)
    width, height = image.size
    width_new = int(float(width) * factor)
    height_new = int(float(height) * factor)

    image = image.resize((width_new, height_new), Image.ANTIALIAS)
    if GIF_PATTERN.match(target_image.lower()):
        image.save(target_image, 'GIF')
    else:
        image.save(target_image, 'JPEG')

    image.close()
    return width_new, height_new

# -----------------------------------------------------------------------------
# MAIN PROPAGATION
# -----------------------------------------------------------------------------


def _main_resize_image():
    from argparse import ArgumentParser
    from sys import exit, argv
    prs = ArgumentParser(description='Resize an image.')
    prs.add_argument('-i', metavar='INFILE', help='Input file')
    prs.add_argument('-o', metavar='OUTFILE', help='Output file')
    prs.add_argument('-f', metavar='FACTOR', type=float, help='Resize factor')
    args = prs.parse_args()
    if not args.i or not args.o or not args.f:
        prs.print_help()
        exit(1)
    resize_image_with_factor(args.i, args.o, args.f)