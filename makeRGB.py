'''
ABOUT:
This Python program will create an RGB png file from
3 spectral bands from an Earth Observing-1 ALI scene.

DEPENDS:
PIL
gdal
numpy

AUTHORS:
Jake Bruggemann
Maria Patterson

HISTORY:
April 2014: Original script (beta).

USE:
For use on the Open Science Data Cloud public data commons.
> python makeRGB.py YEAR DAY IMAGE OUTFILE.png [SCALE]
For example, make an image of the Italian coast from Jan 29, 2014 with a brightening scale factor=2:
> python makeRGB.py 2014 029 EO1A1930292014029110PZ italy.png 2
'''

__author__ = 'Jake Bruggemann'
__version__ = 0.1

def saveRGB(r,g,b,outfile,scale):
	rtif = gdal.Open(r)
	gtif = gdal.Open(g)
	btif = gdal.Open(b)
	rimg = rtif.ReadAsArray()
	gimg = gtif.ReadAsArray()
	bimg = btif.ReadAsArray()
	rmin = float(np.min(rimg[np.nonzero(rimg)]))
	gmin = float(np.min(gimg[np.nonzero(gimg)]))
	bmin = float(np.min(bimg[np.nonzero(bimg)]))
	rscale = (rimg - np.percentile(rimg[np.nonzero(rimg)],1))/(np.percentile(rimg[np.nonzero(rimg)],97)-rmin)
	gscale = (gimg - np.percentile(gimg[np.nonzero(gimg)],1))/(np.percentile(gimg[np.nonzero(gimg)],97)-gmin)
	bscale = (bimg - np.percentile(bimg[np.nonzero(bimg)],1))/(np.percentile(bimg[np.nonzero(bimg)],97)-bmin)
	rscale[rscale>1]=1
	gscale[gscale>1]=1
	bscale[bscale>1]=1
	rgbArray = np.zeros(( rimg.shape[0],rimg.shape[1],3),'uint8')
	rgbArray[...,0] = rscale*255.*scale
	rgbArray[...,1] = gscale*255.*scale
	rgbArray[...,2] = bscale*255.*scale
	img = Image.fromarray(rgbArray)	
	img.save(outfile)

#################################################
#################################################

if __name__ == '__main__':
	from PIL import Image
	import gdal
	import numpy as np
	import argparse

	parser = argparse.ArgumentParser(description='Make a png image from ALI data.')
    	parser.add_argument('YYYY',type=str,help='Year of ALI scene.')
    	parser.add_argument('DDD',type=str,help='Day number of ALI scene.')
    	parser.add_argument('imname',type=str,help='Scene ID of ALI scene')
    	parser.add_argument('outfile',type=str,help='Output png file name.')
    	parser.add_argument('scale',nargs='?',const=1,type=float,default=1,help='Scale factor to brighten image. (Default = 1).')
	  	
 	options = parser.parse_args()
	YYYY = options.YYYY
	DDD = options.DDD
	imname= options.imname
	outfile = options.outfile
        scale = options.scale
	basedir = '/glusterfs/osdc_public_data/eo1/ali_l1g/'
	basefile = basedir+str(YYYY)+'/'+str(DDD)+'/'+str(imname)+'_ALI_L1G/'+str(imname)
	bands = [5,4,3]	# The ALI bands to use: [R, G, B]
	tiffnameR = basefile+'_B'+"%02d"%bands[0]+'_L1T.TIF'
	tiffnameG = basefile+'_B'+"%02d"%bands[1]+'_L1T.TIF'
	tiffnameB = basefile+'_B'+"%02d"%bands[2]+'_L1T.TIF'
	
	saveRGB(tiffnameR,tiffnameG,tiffnameB,outfile,scale)
