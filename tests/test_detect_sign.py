import sys
import os

# Add the project root (one level up) to the PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_root)

import os
from src.process_validations import detect_sign_in_image

def test_sign_detection():
    # Set paths relative to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    test_image_path = os.path.join(project_root, "synthetic_dataset_sign.jpg")
    template_path = os.path.join(project_root, "sign_template.png")
    
    threshold = 0.8  # adjust if needed

    result = detect_sign_in_image(test_image_path, template_path, threshold)
    print("Detection result:", result)
    
    # For a test, you might assert the expected outcome.
    # For example, if you expect the sign to be detected, assert result is True.
    # If you want to simulate both cases, you could change test image and threshold accordingly.
    assert result, "Test failed: The sign was not detected when it should be."

if __name__ == "__main__":
    test_sign_detection()