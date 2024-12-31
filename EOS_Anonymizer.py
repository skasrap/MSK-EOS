import os
import pydicom
from pydicom import dcmread
import csv



listofFiles = open("FILE_PATHS.csv")
output_dir = "PATH_TO_OUTPUT"
csvreader = csv.reader(listofFiles)  # Prepare the list of file names beforehand.

def anonymize_dicom(dataset, excluded_elements):
    anonym_elements = ["PN", "DA", "TM", "LO", "SH", "LT", "UI"]  # Personal info elements to anonymize.
    for elem in dataset:
        if elem.VR in anonym_elements and elem.tag not in excluded_elements:
            elem.value = None

# Tags to exclude from anonymization (retain these fields)
excluded_tags = [
    (0x0008, 0x103e),  # Series Description
    (0x0020, 0x0020),  # Patient Orientation
    (0x0020, 0x0060),  # Laterality
    (0x0020, 0x4000),  # Image Comments

]

# Process each file in the list
for file_path in csvreader:
    file_path = file_path[0].strip()  # Remove extra whitespace/newline
    ds = dcmread(file_path)
    
    # Print original series info (for debugging)
    if (0x0020, 0x4000) in ds:
        img_comment = ds[0x0020, 0x4000].value
        print(f"Image Comments: {img_comment}")
    
    # Anonymize the dataset
    anonymize_dicom(ds, excluded_tags)
    
    # Save anonymized file with new name
    base_name = os.path.join(output_dir, os.path.basename(file_path))
    if "Frontal" in img_comment:
        output_file_name = base_name + "_AP" + "_anonymized.dcm"
    elif "Lateral" in img_comment:
        output_file_name = base_name + "_Lat" + "_anonymized.dcm"
    else:
        output_file_name = base_name + "_unk" + "_anonymized.dcm"
        
    ds.save_as(output_file_name)
    print(f"Saved anonymized file: {output_file_name}")
