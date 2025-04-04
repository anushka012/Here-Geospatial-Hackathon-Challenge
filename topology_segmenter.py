import json
import geopandas as gpd
import pandas as pd
import shapely
from shapely.ops import substring

##########################################################
### LOAD FULL TOPOLOGY TILE
##########################################################
topology_gdf = gpd.read_file(r"data\23599610_full_topology_data.geojson")

##########################################################
### FILTER TO THE SELECTED PARAMETERIZED ATTRIBUTE
##########################################################
access_characteristics_gdf = topology_gdf[['id','accessCharacteristics', 'geometry']]

##########################################################
### NORMALIZE THE COLUMN WITH JSON LOADS
##########################################################
def convert_data(x):
            try:
                return json.loads(x)
            except:
                return {}
access_characteristics_gdf['accessCharacteristics'] = access_characteristics_gdf['accessCharacteristics'].apply(convert_data)

##########################################################
### EXPLODE DATASET BASED ON THE PARAMETERIZED ATTRIBUTION COLUMN (essentially duplicate some geoms before cutting)
##########################################################
access_characteristics_gdf = access_characteristics_gdf.explode('accessCharacteristics')
access_characteristics_gdf['id'] = access_characteristics_gdf['id'] + "_" + access_characteristics_gdf.index.astype(str)

##########################################################
### GET START AND END OFFSET
##########################################################
access_characteristics_gdf['startOffset'] = access_characteristics_gdf['accessCharacteristics'].str['range'].str['startOffset']
access_characteristics_gdf['endOffset'] = access_characteristics_gdf['accessCharacteristics'].str['range'].str['endOffset']

##########################################################
### SPLIT SHAPELY GEOMETRY
##########################################################
def split_shapely_string(geom_column, start_offset, end_offset):
    try:
        result = substring(geom_column, start_dist=start_offset, end_dist=end_offset, normalized=True)
        result = shapely.transform(result, lambda x: x, include_z=False)
    except Exception as e:
        result = None
        print("SKIPPED GEOMETRY SUBSTRING SPLIT", e)
    return result
access_characteristics_gdf['geometry'] = access_characteristics_gdf.apply(lambda x: split_shapely_string(x.geometry, x['startOffset'], x['endOffset']), axis=1)

##########################################################
### JSON NORMALIZE NEW GDF TO SPLIT OUT COLUMNS
##########################################################
access_characteristics_gdf = pd.json_normalize(data=pd.DataFrame.to_dict(access_characteristics_gdf, orient='records'))
access_characteristics_gdf = gpd.GeoDataFrame(data=access_characteristics_gdf, geometry=access_characteristics_gdf['geometry'])

access_characteristics_gdf.to_file("output.geojson")