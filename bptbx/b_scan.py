r"""This module contains methods to work with scan devices""" 

import twain
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
    
def convert_images_to_a4_pdf (images, target_pdf='output.pdf'):  
    """Takes a list of JPG/PNG/BMP images and stores the images to 
       an A4-format PDF with each image as one page."""
       
    c = canvas.Canvas(target_pdf)
    c.setPageCompression(1)
    for image in images:
        c.drawImage(image, 0, 0, 21 * cm, 29.7 * cm)
        c.showPage()
    c.save()

images = ['d:/2014-06-28_104815.bmp' ]
convert_images_to_a4_pdf(images, 'd:/target.pdf')
    
def get_scanner (pickfirst=False):
    """Obtain the name of an available scanner"""
    
    sm = twain.SourceManager(0)
    scanner_name = ''

    if pickfirst:
        scanners = sm.GetSourceList()
        if len(scanners) > 0:
            scanner_name = scanners[0]
    else:
        source = sm.OpenSource()
        scanner_name = source.GetSourceName()

    sm.destroy()
    return scanner_name

def scan_image (target_file, scanner_name=None, resolution=100, contrast=0):
    """Uses a twain-compatible scanner to scan an image to BMP"""
    
    # Initialize scanner
    sm = twain.SourceManager(0)
    
    if scanner_name == None:
        scanner_name = get_scanner (False)
        
    ss = sm.OpenSource(scanner_name)
    
    ss.SetCapability(twain.ICAP_XRESOLUTION, 7 , float(resolution))
    ss.SetCapability(twain.ICAP_CONTRAST, 7 , float(contrast))
    ss.HideUI()
    ss.RequestAcquire(0, 0)
    
    # the next command actually performs the scanning 
    rv = ss.XferImageNatively()
    if rv:
        (handle, _) = rv
        twain.DIBToBMFile(handle, target_file)
    sm.destroy() 
