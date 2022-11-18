import math
#rom osgeo import gdal, ogr, osr
import rasterio
from rasterio.plot import show
import os
from itertools import product
import rasterio as rio
from rasterio import windows
import sys

tiles_width = 984    #wedth of the image
tiles_height = 984   #heigh of the image
output_filename = 'tile_{}-{}.jpg'
#input_filename='1.tif'
#inputArg = sys.argv

#out_path="/home/nteupe/extractBuildings/preprocessing/output/"
#in_path="/home/nteupe/extractBuildings/preprocessing/"








#inputArg = sys.argv
#ou_path="output/clip/"
#os.mkdir(ou_path+inputArg[1])
#out_path=ou_path+inputArg[1] + '/'
#in_path="input/"= inputArg[1]+'/'
#input_filename=inputArg[1]
#tiles_width = 256
#tiles_height = 256

def get_tiles(ds, width = tiles_width, height = tiles_height):
    nols, nrows = ds.meta['width'], ds.meta['height']
    offsets = product(range(0, nols, width), range(0, nrows, height))
    big_window = windows.Window(col_off=0, row_off=0, width=nols, height=nrows)
    for col_off, row_off in  offsets:
        window =windows.Window(col_off=col_off, row_off=row_off, width=width+40, height=height+40).intersection(big_window)
        transform = windows.transform(window, ds.transform)
        yield window, transform

class Tiles:
    def cut(in_path, input_filename, out_path,):
        """ Slice the images into several images of equal dimensions.
    
        Arguments
        ---------
        in_path : Str
            Path to the image.
        input_filename:str
            Name of the image
        save_path : Str
            Path to sav the masked slice images .

        Returns
        -------
        Several image of different dimension.

        Notes
        -----
        This functions depends on "rasterio" with it's subfunctions.
        """
        with rio.open(os.path.join(in_path, input_filename)) as inds:
            output_filename = 'tile_{}-{}.jpg'
            tiles_width =984    #wedth of the image
            tiles_height = 984
            tile_width, tile_height = tiles_width, tiles_height

            meta = inds.meta.copy()

            for window, transform in get_tiles(inds):
                print(window)
                meta['transform'] = transform
                meta['width'], meta['height'] = window.width, window.height
                outpath = os.path.join(out_path,output_filename.format(int(window.col_off), int(window.row_off)))
                with rio.open(outpath, 'w', **meta) as outds:
                    outds.write(inds.read(window=window))
        print('ok') 
        
        
import sys



#inputArg = sys.argv
#input_filename= inputArg[1]
#input_path = "input/" 
#tile_path='tiles/'
#tiles_width = 256    #wedth of the image
#tiles_height = 256   #heigh of the image
#output_filename = 'tile_{}-{}.png'        
        
#if __name__ == '__main__':
 #   Tiles.cut(input_path, input_filename, tile_path)
