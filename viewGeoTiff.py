'''
ABOUT:
This Python program will display a GeoTiff and optionally save the image as a .png file.

DEPENDS:
PIL
gdal
numpy
matplotlib.pyplot
pylab

AUTHORS:
Jake Bruggemann
Maria Patterson

HISTORY:
April 2014: Original script (beta) by Jake Bruggemann

USE:
For use on the Open Science Data Cloud public data commons.
> python viewGeoTiff.py TIFFNAME [OUTFILE.png]
For example, if you want to view a GeoTiff of Italy in ALI band 3 and save it as a .png file:
> python viewGeoTiff.py /glusterfs/osdc_public_data/eo1/ali_l1g/2014/029/EO1A1930292014029110PZ_ALI_L1G/EO1A1930292014029110PZ_B03_L1T.tif italyB3.png
'''

__author__ = 'Jake Bruggemann'
__version__ = 0.1

def displayTif(path,outfile):

	tif = gdal.Open(path)
	band = tif.GetRasterBand(1)
        img = band.ReadAsArray()

	imgplot = plt.imshow(img, interpolation="none")


	def format_coord(x, y):
    		col = int(x+0.5)
    		row = int(y+0.5)
        	z = img[row,col]
        	return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)


	plt.gca().format_coord = format_coord
        plt.axis('off')
	if outfile != None:
		plt.savefig(outfile,bbox_inches='tight')
	plt.show() 

#################################################
#################################################

if __name__ == '__main__':
    from PIL import Image
    from pylab import *
    import gdal, osr
    import matplotlib.pyplot as plt
    import numpy as np
    import argparse

    parser = argparse.ArgumentParser(description='View a GeoTiff file.')
    parser.add_argument('tifname',type=str,help='Name of GeoTiff file.')
    parser.add_argument('outfile',nargs='?',type=str,default=None,help='Output png file name.')
    
    options = parser.parse_args()

    tiffname = options.tifname
    outfile = options.outfile
    
    displayTif(tiffname,outfile)
