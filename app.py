from clip import Tiles
from convert_quality import change_qualitity_of_image
from merge import Merge
from transfer import Transfer_info
from polygonized import Binary_mask_to_poly_geojson
original_path=""
file_name=""
clip_path="./clip/"
convert_input_path="./convert/"
predict_path="./predict/"
merge_path="./merge/"
polygon_path="./polygon/"
save_model="./saved_model/mask_rcnn_object_0014.h5"
Tiles.cut(original_path, file_name, clip_path)
change_qualitity_of_image(clip_path, convert_input_path)
#^predict(convert_input_path, predict_path)
Transfer_info.Giveninfor(clip_path, predict_path)
Merge.merge( predict_path, merge_path)
Binary_mask_to_poly_geojson