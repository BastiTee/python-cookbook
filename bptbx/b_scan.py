r"""This module contains methods to work with scan devices""" 
from os import path

from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from bptbx import b_cmdline





def convert_images_to_a4_pdf (images, target_pdf='output.pdf'):  
    """Takes a list of JPG/PNG/BMP images and stores the images to 
       an A4-format PDF with each image as one page."""
       
    c = canvas.Canvas(target_pdf)
    c.setPageCompression(1)
    for image in images:
        c.drawImage(image, 0, 0, 21 * cm, 29.7 * cm)
        c.showPage()
    c.save()
    

def scan_image (target_file, resolution=100, contrast=0):
    """Uses a twain-compatible scanner to scan an image to BMP"""
    
    pf = b_cmdline.get_platform()
    if not 'windows' in pf:
        raise OSError
    
    here = path.dirname(path.realpath(__file__))

    command = path.join(here, 'ext', 'cmdtwain-win', 'ScanBmp.exe')
    command = '{} /PAPER=a4 /RGB /DPI={} {}'.format(command, resolution,
                                                    target_file)
    b_cmdline.runcommand(command, True, True)
