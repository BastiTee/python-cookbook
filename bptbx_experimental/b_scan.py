r"""This module contains methods to work with scan devices
    
    Necessary external modules include:
    
     http://www.reportlab.com/software/opensource/ PDF creator library 
    (tested with reportlab-3.0.win32-py2.7)
    https://pypi.python.org/pypi/twain Scanner library for twain 
    (tested with twain-1.0.5.win32-py2.7)
    
""" 

import twain
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm

def convert_images_to_a4_pdf (images, target_pdf='output.pdf'):  
    """Takes a list of JPG/PNG/BMP images and stores the images to 
       an A4-format PDF with each image as one page."""
       
    c = canvas.Canvas(target_pdf)
    c.setPageCompression(1)
    for image in images:
        c.drawImage(image, 0, 0, 21 * cm, 29.7 * cm)
        c.showPage()
    c.save()
    
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
        (handle, count) = rv
        twain.DIBToBMFile(handle, target_file)
    sm.destroy() 