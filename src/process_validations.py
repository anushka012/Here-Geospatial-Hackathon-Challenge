import cv2
import numpy as np
from satellite_imagery_tile_request import get_satellite_tile

def detect_sign_in_image(image_path, template_path="sign_template.png", threshold=0.8):
    """
    Detects if a sign is present in the satellite image using template matching.
    
    :param image_path: Path to the satellite tile image.
    :param template_path: Path to the template image of the sign.
    :param threshold: Correlation threshold above which we assume the sign is present.
    :return: True if a sign is detected, False otherwise.
    """
    # Load the satellite image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Error: Could not load satellite image from", image_path)
        return False

    # Load the template image in grayscale
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("Error: Could not load template image from", template_path)
        return False

    # Get dimensions of the template
    w, h = template.shape[::-1]

    # Perform template matching using normalized cross-correlation
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print("Max correlation value:", max_val)
    
    # If the maximum correlation is above our threshold, we assume the sign is detected.
    if max_val >= threshold:
        return True
    else:
        return False

def remove_signs_based_on_satellite(signs_data, validations_data, api_key, zoom=16, tile_format='png', tile_size=512):
    """
    For each validation (WSIGN406), use the satellite imagery to verify if the sign is present.
    If the analysis indicates the sign is absent, remove it from the signs_data.
    """
    # Set to store IDs to remove after satellite check
    ids_to_remove = set()
    
    for validation in validations_data.get("features", []):
        props = validation.get("properties", {})
        # Check if the rule applies (WSIGN406)
        if props.get("Rule Code") == "WSIGN406":
            sign_id = props.get("Feature ID")
            # GeoJSON geometry is typically [lon, lat]
            coordinates = validation.get("geometry", {}).get("coordinates", [])
            if len(coordinates) >= 2:
                lon = coordinates[0]
                lat = coordinates[1]
                # Get the satellite tile and bounds (the tile image will be saved)
                wkt_bounds = get_satellite_tile(lat, lon, zoom, tile_format, api_key)
                # Use the downloaded tile image (e.g., satellite_tile.png) for detection
                if not detect_sign_in_image(f'satellite_tile.{tile_format}'):
                    # If detection indicates no sign, mark for removal
                    ids_to_remove.add(sign_id)
    
    # Now remove any sign whose "id" is in ids_to_remove
    filtered_features = [
        feat for feat in signs_data.get("features", [])
        if feat["properties"].get("id") not in ids_to_remove
    ]
    
    signs_data["features"] = filtered_features
    return signs_data



# def remove_outdated_signs(signs_data, validations_data):
#     """
#     Remove sign features from signs_data that are flagged in validations_data.
    
#     This version uses the "Feature ID" field from validations to compare against the
#     "id" field in the signs file.
#     """
#     # Gather all feature IDs to remove from validations (if the rule applies)
#     outdated_ids = set()
#     for feature in validations_data.get("features", []):
#         props = feature.get("properties", {})
#         # Optionally, you can check additional fields like "Rule Code" or "Status"
#         if props.get("Rule Code") == "WSIGN406":
#             fid = props.get("Feature ID")
#             if fid:
#                 outdated_ids.add(fid)
                
#     # Filter out any sign whose "id" is in the outdated_ids set
#     filtered_features = [
#         feat for feat in signs_data.get("features", [])
#         if feat["properties"].get("id") not in outdated_ids
#     ]
    
#     signs_data["features"] = filtered_features
#     return signs_data

