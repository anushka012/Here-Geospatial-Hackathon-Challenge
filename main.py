import os
from src.utils import load_geojson, save_geojson
from src.process_validations import remove_signs_based_on_satellite

def main():
    data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    signs_path = os.path.join(data_dir, "23608577_signs.geojson")
    validations_path = os.path.join(data_dir, "23608577_validations.geojson")
    output_signs_path = os.path.join(data_dir, "23608577_signs_corrected.geojson")
    
    # Load GeoJSON files
    signs_data = load_geojson(signs_path)
    validations_data = load_geojson(validations_path)
    
    # HERE API key and parameters for satellite tile request
    api_key = "oTANAdIcCu8_TXX-32Ry6CCVhbKMXaUrnk9-aXrVS2s"  
    zoom_level = 16
    tile_format = "png"
    tile_size = 512
    
    # Process the signs based on satellite imagery check
    corrected_signs = remove_signs_based_on_satellite(signs_data, validations_data, api_key, zoom=zoom_level, tile_format=tile_format, tile_size=tile_size)
    
    # Save the new GeoJSON file
    save_geojson(corrected_signs, output_signs_path)
    print(f"Corrected signs GeoJSON saved to: {output_signs_path}")

if __name__ == "__main__":
    main()


# import os
# from src.utils import load_geojson, save_geojson
# from src.process_validations import remove_outdated_signs

# def main():
#     # Build the data directory path relative to the project root
#     data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
    
#     # Construct file paths
#     signs_path = os.path.join(data_dir, "23608577_signs.geojson")
#     validations_path = os.path.join(data_dir, "23608577_validations.geojson")
#     output_signs_path = os.path.join(data_dir, "23608577_signs_corrected.geojson")
    
#     # Load the input GeoJSON files
#     signs_data = load_geojson(signs_path)
#     validations_data = load_geojson(validations_path)
    
#     # Process scenario #1: remove outdated signs
#     corrected_signs = remove_outdated_signs(signs_data, validations_data)
    
#     # Save the corrected signs GeoJSON file
#     save_geojson(corrected_signs, output_signs_path)
#     print(f"Corrected signs GeoJSON saved to: {output_signs_path}")

# if __name__ == "__main__":
#     main()