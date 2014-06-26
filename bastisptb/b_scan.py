r"""This module contains methods to work with scan devices
    
    Necessary external modules include:
    
    https://pypi.python.org/pypi/twain Scanner library for twain 
    (tested with twain-1.0.5.win32-py2.7)

""" 

import twain

def get_scanner ( pickfirst = False ):
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

def scan_image ( target_file, scanner_name=None, resolution=100, contrast=0):
    """Uses a twain-compatible scanner to scan an image to BMP"""
    
    # Initialize scanner
    sm = twain.SourceManager(0)
    
    if scanner_name == None:
        scanner_name = get_scanner ( False )
        
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
