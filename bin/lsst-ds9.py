#!/usr/bin/env python
import sys
import time
from collections import OrderedDict

import lsst.afw.display.ds9 as ds9
import lsst.afw.image as afwImage


import argparse
description = "python script for calling LSST DS9 interface."
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--mask',default=None)
parser.add_argument('args',nargs=argparse.REMAINDER)
opts = parser.parse_args(); args = opts.args
nargs = len(args)

# Try to stick with LSST defaults when possible
# http://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/namespacelsst_1_1afw_1_1display_1_1ds9.html
MASK_BITS = OrderedDict([
        ["BAD", 'RED',],  # From mkbpm
        ["SAT", 'GREEN'], # ???
        ["INTRP", 'GREEN'], # ???
        ["LOW",'CYAN'], # ???
        ["CR", 'MAGENTA'], #immask
        ["DETECTED", 'BLUE'], #mkbleedmask
        ["TRAIL", "BLUE"], #mkbleedmask
        ["EDGEBLEED", "BLUE" ], #mkbleedmask
        ["SSXTALK", "BLUE"], #mkbleedmask
        ["EDGE", "YELLOW"], # ???
        ["STREAK", "CYAN"], # from immask
        ["FIX","RED"], # ???
        ])

def defineMaskPlanes(name):
    afwImage.MaskU.clearMaskPlaneDict()    
    for bit,color in name.items():
        afwImage.MaskU.addMaskPlane(bit)
    ds9.setMaskPlaneColor(name)

defineMaskPlanes(MASK_BITS)

for i in range(3):
    try:
        ds9.initDS9(i == 0)
    except ds9.Ds9Error:
        time.sleep(0.5)
    else:
        if i > 0: break

settings = dict(width=1024,height=512,
                zoom=0.25, rotate=270,
                wcs="skyformat degrees",
                tile='yes' if nargs > 1 else 'no')

for key, value in settings.items():
    ds9.ds9Cmd("%s %s"%(key,value))

for i,arg in enumerate(args):
    image = afwImage.MaskedImageF(arg)

    if opts.mask:
        input_mask = afwImage.ImageU(opts.mask).getArray()
        original_mask = image.getMask().getArray()
        original_mask |= input_mask

    ds9.mtv(image, frame=i)
    ds9.setMaskTransparency(50)
    ds9.ds9Cmd("scale mode zscale")

    if nargs == 1: 
        # Hack to display mask as image
        mask = afwImage.ImageU(image.getMask().getArray())
        ds9.mtv(mask, frame=i+1)
        ds9.mtv(image.getMask(), frame=i+1, isMask=True)
        ds9.ds9Cmd("scale log")
        ds9.setMaskTransparency(50)

ds9.ds9Cmd("lock frame image")
ds9.setDefaultFrame(0)
ds9.show()
