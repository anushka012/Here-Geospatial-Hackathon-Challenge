import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Load the access segments and validation data
access_gdf = gpd.read_file(r"D:\Hackathon\data sets\ExternalFileShares\ExternalFileShares\Chicago_Hackathon_expanded_datasets\23608577\23608577_access_chars.geojson")
validations_gdf = gpd.read_file(r"D:\Hackathon\data sets\ExternalFileShares\ExternalFileShares\Chicago_Hackathon_expanded_datasets\23608577\23608577_validations.geojson")

# Load probe data
probe_df = pd.read_csv(r"D:\Hackathon\data sets\ExternalFileShares\ExternalFileShares\Chicago_Hackathon_expanded_datasets\23608577\23608577_probe_data.csv")

# Step 1: Create geometry column from lat/lon
probe_df['geometry'] = probe_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
probe_gdf = gpd.GeoDataFrame(probe_df, geometry='geometry', crs='EPSG:4326')

# Step 2: Convert everything to a common projection for distance calculations
access_gdf = access_gdf.to_crs(epsg=3857)
probe_gdf = probe_gdf.to_crs(epsg=3857)

# Step 3: Spatial join - match probe points to nearest road segment (within 20m)
print("Performing spatial join...")
joined_probe = gpd.sjoin_nearest(probe_gdf, access_gdf, max_distance=20, how='inner', distance_col='distance_to_segment')
print(f"Number of rows after join: {len(joined_probe)}")
# Step 4: Aggregate behavior per segment
print("Aggregating behavior per segment...")
segment_stats = joined_probe.groupby('id').agg({
    'speed': ['mean', 'count']
}).reset_index()
segment_stats.columns = ['id', 'avg_speed', 'num_traces']

# Print the output of the aggregation
print("Segment Statistics:")
print(segment_stats)
segment_stats.columns = ['id', 'avg_speed', 'num_traces']

# Merge with access characteristics
access_with_stats = access_gdf.merge(segment_stats, on='id', how='left')

# Fill missing values with zero (fixed without inplace=True)
access_with_stats['avg_speed'] = access_with_stats['avg_speed'].fillna(0)
access_with_stats['num_traces'] = access_with_stats['num_traces'].fillna(0)

# Step 5: Logic to detect suspicious pedestrian flags
def is_suspect(row):
    # Check if 'pedestrian' exists before applying logic
    if 'pedestrian' in row and str(row['pedestrian']).upper() == 'TRUE':
        if row['avg_speed'] > 10 and row['num_traces'] > 5:
            return True
    return False

# Apply the function to detect suspicious segments
if 'pedestrian' in access_with_stats.columns:
    access_with_stats['suspect_pedestrian_flag'] = access_with_stats.apply(is_suspect, axis=1)
else:
    print("Warning: Column 'pedestrian' not found in DataFrame.")
    access_with_stats['suspect_pedestrian_flag'] = False

# Output suspect segments
suspect_segments = access_with_stats[access_with_stats['suspect_pedestrian_flag']]
print(f"Found {len(suspect_segments)} segments with suspicious pedestrian=TRUE flag.")

# Save output
suspect_segments.to_file("suspect_pedestrian_segments.geojson", driver="GeoJSON")
