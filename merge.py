import os
from os import listdir
from os.path import join
from os.path import isfile
import rasterio
import rasterio as rio
from rasterio.merge import merge
from rasterio.plot import show
import sys

#inputArg = sys.argv
#image_path = "output/prediction/"+inputArg[2] +'/'

#out_path = "output/merge/"+inputArg[2] +'/'



class Merge:
    def merge(image_path,  out_path):
        """Merge a series of raster .

    Arguments
    ---------
    image_path : Str
        Path to the series of raster.
    save_path : Str
        Path of to the merged raster.

    Returns
    -------
    A merge raster with it's metadata.
    
    Notes
    -----
    This functions depends on "rasterio" and it's submodules.
    """
        nlyTIFF = [os.path.join(image_path, f) for f in listdir(image_path) if isfile(join(image_path, f)) and  f.endswith(".tif")]
    # List for the source files
        src_files_to_mosaic = []
        for fp in nlyTIFF:
            src = rio.open(fp)
            src_files_to_mosaic.append(src) 
        mosaic, out_trans = merge(src_files_to_mosaic)
        # Copy the metadata
        out_meta = src.meta.copy()
        # Update the metadata
        out_meta.update({"driver": "GTiff",
                "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 })
        with rasterio.open(out_path, "w", **out_meta) as dest:
            dest.write(mosaic)


            
#filter_path='filter/'+ 
#merge_path='merge/'          
            
#if __name__ == '__main__':
    #path ="/home/nteupe/all_results/"       
    #save_path="/home/nteupe/all_results/filter/"
    #Merge.merge(filter_path ,merge_path)

