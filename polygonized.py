from osgeo import gdal
import skimage.io
import numpy as np
from shapely.geometry import shape
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd
import rasterio
from rasterio import features






def Binary_mask_to_poly_geojson(imagepath,output_path, channel_scaling=None, reference_im=None,cr=None,
                          output_type='geojson', min_area=27,
                         bg_threshold=0, simplify=True,
                         tolerance=15, **kwargs):
    """Get polygons from an image mask.

    Arguments
    ---------
    pred_arr : :class:`numpy.ndarray`
        A 2D array of integers. Multi-channel masks are not supported, and must
        be simplified before passing to this function. Can also pass an image
        file path here.
    channel_scaling : :class:`list`-like, optional
        If `pred_arr` is a 3D array, this argument defines how each channel
        will be combined to generate a binary output. channel_scaling should
        be a `list`-like of length equal to the number of channels in
        `pred_arr`. The following operation will be performed to convert the
        multi-channel prediction to a 2D output ::

            sum(pred_arr[channel]*channel_scaling[channel])

        If not provided, no scaling will be performend and channels will be
        summed.
    reference_im : str, optional
        The path to a reference geotiff to use for georeferencing the polygons
        in the mask. Required if saving to a GeoJSON (see the ``output_type``
        argument), otherwise only required if ``do_transform=True``.
    output_path : str, optional
        Path to save the output file to. If not provided, no file is saved.
    output_type : ``'csv'`` or ``'geojson'``, optional
        If ``output_path`` is provided, this argument defines what type of file
        will be generated - a CSV (``output_type='csv'``) or a geojson
        (``output_type='geojson'``).
    min_area : int, optional
        The minimum area of a polygon to retain. Filtering is done AFTER
        any coordinate transformation, and therefore will be in destination
        units.
    bg_threshold : int, optional
        The cutoff in ``mask_arr`` that denotes background (non-object).
        Defaults to ``0``.
    simplify : bool, optional
        If ``True``, will use the Douglas-Peucker algorithm to simplify edges,
        saving memory and processing time later. Defaults to ``False``.
    tolerance : float, optional
        The tolerance value to use for simplification with the Douglas-Peucker
        algorithm. Defaults to ``0.5``. Only has an effect if
        ``simplify=True``.

    Returns
    -------
    gdf : :class:`geopandas.GeoDataFrame`
        A GeoDataFrame of polygons.

    """
    mask_arr = skimage.io.imread(fname=imagepath)
    if reference_im is None:
        with rasterio.open(imagepath) as ref:
            transform = ref.transform
            crs = ref.crs
            ref.close()
    else:
        with rasterio.open(reference_im) as ref:
            transform = ref.transform
            crs = ref.crs
            ref.close()
    mask = mask_arr > bg_threshold
    mask = mask.astype('uint8')


    polygon_generator = features.shapes(mask_arr,transform=transform,mask=mask)
    polygons = []
    values = []  # pixel values for the polygon in mask_arr
    for polygon, value in polygon_generator:
        p = shape(polygon).buffer(0.0)
        if p.area >= min_area:
            polygons.append(shape(polygon).buffer(0.0))
            values.append(value)

    polygon_gdf = gpd.GeoDataFrame({'geometry': polygons, 'value': values},
                                   crs=crs.to_wkt())
    if simplify:
        polygon_gdf['geometry'] = polygon_gdf['geometry'].apply(
            lambda x: x.simplify(tolerance=tolerance)
        )
    #changing the crs in case
    if cr is not None:
        polygon_gdf=polygon_gdf.to_crs(epsg=cr)
    # save output files
    if output_path is not None:
        if output_type.lower() == 'geojson':
            #if len(polygon_gdf) > 0:
            polygon_gdf.to_file(output_path, driver='GeoJSON')
            #else:
                #save_empty_geojson(output_path, polygon_gdf.crs.to_epsg())
        elif output_type.lower() == 'csv':
            polygon_gdf.to_csv(output_path, index=False)
        else:
            polygon_gdf.to_file(output_path)
    return polygon_gdf






import geopandas
from shapely.geometry.polygon import LinearRing
from shapely.geometry import Polygon
import pandas as pd
#this function is to amelorate the field pllot to have well defined plots
def shape_plot(path,save_path):
    geojson=geopandas.read_file(path)
    d=[]
    for i in range(len(geojson["geometry"])):
        s=geojson["geometry"][i]
        v = s.convex_hull
        d.append(v)
    df3 = pd.DataFrame([ a for a in d],columns=['geometry'])
    gdf = gpd.GeoDataFrame(df3)
    gdf.to_file(filename=save_path, driver='GeoJSON')