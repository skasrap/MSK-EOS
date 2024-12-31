import pydicom
from pydicom import dcmread
import csv

listofFiles = open('ky/filenames.csv')
csvreader = csv.reader(listofFiles)  # Prepared the list of file names beforehand.

# Function for anonymizing personal information
def anonymize_dicom(dataset, excluded_elements):
    anonym_elements = ["PN", "DA", "TM", "LO", "SH", "LT", "UI"]  # Personal info elements.
    for elem in dataset:
        if elem.VR in anonym_elements and elem.tag not in excluded_elements:
            elem.value = None

# Tags to exclude from anonymization
excluded_tags = [
    (0x0008, 0x103e),  # Series Description
    (0x0020, 0x0020),  # Patient Orientation
    (0x0020, 0x0060),  # Laterality
]

# Process each file in the list
for file_path in csvreader:
    file_path = file_path[0].strip() 
    ds = dcmread(file_path)
    
    # for debugging
    if (0x0008, 0x103e) in ds:
        print(f"Original Series Description: {ds[0x0008, 0x103e].value}")
    
    # Anonymize the dataset
    anonymize_dicom(ds, excluded_tags)
    
    # Save anonymized file with new name
    base_name = file_path.rsplit(".", 1)[0]
    output_file_name = base_name + "_anonymized.dcm"
    ds.save_as(output_file_name)
    print(f"Saved anonymized file: {output_file_name}")
