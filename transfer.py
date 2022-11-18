from osgeo import gdal
import sys
import os
from os import listdir
from os.path import join
from os.path import isfile
from tkinter import *
from tkinter import Tcl

#inputArg = sys.argv
image_path = "output/clip/"
mask_path = "output/prediction/"


#path is the path of the folder where the images(tiled) are found 
#path1 is the path of the folder where the mask(predicted mask ) are found
class Transfer_info:
    def Giveninfor(image_path, mask_path):
        output= [f for f in listdir(mask_path) if isfile(join(mask_path, f)) and  f.endswith(".tif")]
        input= [f for f in listdir(image_path) if isfile(join(image_path, f)) and  f.endswith(".jpg")]
        inp=Tcl().call('lsort', '-dict',input)  
        out=Tcl().call('lsort', '-dict',output)
        print(len(inp))
        print(len(out))
        a=[]        #list the slide images
        b=[]       # list for the mask
        for file in inp:
            a.append(gdal.Open(image_path + file, gdal.GA_ReadOnly))            
        for file in out:
            b.append(gdal.Open(mask_path + file, gdal.GA_Update))
        for i in range(len(a)):
            print('1')
            a[i].GetProjection()
            a[i].GetGeoTransform()
            b[i].SetProjection(a[i].GetProjection())          #setting the mask  projection
            b[i].SetGeoTransform(a[i].GetGeoTransform())      #setting the mask trnsformatio
            b[i]= None                          #saving the image link

            
            
filter_path='filter/guene/'
tile_path='tiles/guene/'        
