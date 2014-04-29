# OSDC EO-1 Quick Start Tutorial

Hello! Welcome to the Open Science Data Cloud demo on NASA's Earth Observing-1 dataset. 
In this tutorial, we will show you how to use OSDC to visualize
and perform a simple example analysis of NASA satellite imagery data.

## About the Data
NASA's Earth Observing-1 satellite (EO-1) was launched in 2000 for the purpose of 
studying new technologies in remote earth imaging. On the OSDC, we host data from 
EO-1's two primary scientific instruments, the Hyperion imaging spectrometer and the 
Advanced Land Image (ALI). In this tutorial we will be working with ALI data.

The ALI instrument acquires data in 9 different wavelength bands from 0.48 - 2.35 micron
with 30-meter resolution plus a panchromatic band with higher 10-meter spatial resolution.  
The standard 'scene' (image) size projected on the Earth's surface equates to 37 km x 42 km 
(width x length).  Hyperion has similar spatial resolution but higher spectral resolution, 
observing in 242 band channels from 0.357 - 2.576 micron with 10-nm bandwidth. 
Hyperion scenes have a smaller standard footprint width of 7.7 km.

EO-1 Level 0 scenes (raw data) are received daily from NASA and processed by NASA on the 
OSDC to create various Level 1 data.  We will use here the Level 1Gst scenes, 
radiometrically corrected, resampled for geometric correction, and registered to a 
geographic map projection. 
These data are stored in GeoTiff format, one GeoTiff for each wavelength band, giving the 
corrected radiance value recorded at each pixel. Here we will show you how to use Python to 
* create png false-color images from GeoTiff data,
* use a machine algorithm to classify each pixel of a scene as desert, water, cloud, or vegetation,
* view GeoTiffs and save the results of your classification as an image.

## Viewing a GeoTiff
We will take a look at an example ALI GeoTiff from band 3, covering 0.45 - 0.515 micron. 
Our data resides in the /glusterfs/osdc_public_data/eo1 directory.  In the terminal, type:

```
python viewGeoTiff.py /glusterfs/osdc_public_data/eo1/ali_l1g/2014/029/EO1A1930292014029110PZ_ALI_L1G/EO1A1930292014029110PZ_B03_L1T.TIF
```

## Making an RGB Image
Here we will create an RGB image from three bands of an individual ALI scene. 
We will use the makeRGB.py script to look at a scene observed on the 29th 
day of 2014 and save it as a png image.  To make the image a little brighter,
we tell the script to scale each color up by a factor of 2.

In the terminal, type in:

```
python makeRGB.py 2014 029 EO1A1930292014029110PZ italy.png 2
```

To download this image to your local machine for viewing is a two-step process.
First, move the file to your gluster user directory on Sullivan
by typing the following into your VM terminal:

```
mv italy.png /glusterfs/users/USERNAME/
```

Then, in the terminal on your local machine, download the file into the preferred directory:

```
scp USERNAME@sullivan.opensciencedatacloud.org:~/italy.png .
```

Now take a look at your picture using your favorite image viewer.
Looks like a nice spot to run our classifier. This is a section of the Italian coast near Pisa.
 
## Classifying the Image
We will run our classifier see if it can identify which sections of the scene are clouds, 
water, desert, or vegetation.  The classifier uses a support vector machine (SVM) 
from Python's scikit-learn module to fit a model
to the training set from Hyperion data we have provided in 'FourClassTrainingSet.txt'. 
This classifier uses the ratios of ALI bands 3:7 and 4:8.
The file trainingSpectra.png shows a plot of the average reflectance spectra from Hyperion 
for each class in the training set.  Shaded grey areas show the wavelength coverage of
ALI bands, which are used by the classifier described.

You can run the classifier with the following command:

```
python classify.py 2014 029 EO1A1930292014029110PZ italyClassified.tif
```

It will take about 10 minutes to run, so go get a snack or some coffee. You 
can also look at the classified GeoTiff we have provided using the above procedure.

-----INTERMISSION-----

## Viewing the Results
Let's take a look at the GeoTiff created. Run viewClassifiedTiff.py on the file
made by the classification:

```
python viewClassifiedTiff.py italyClassified.tif italyClassified.png
```

You can download italyClassified.png to your local machine using the instructions 
above in 'Making an RGB image.'

The classified scene has a white pixel where the classifier identified clouds, 
blue for water, brown for desert, and green for vegetation. 

Using the USGS EarthExplorer webpage you can retrieve the scene IDs 
and dates for scenes all over the world and classify them. Have fun! 
