import pydicom
from pydicom import dcmread
import csv


listofFiles = open('ky/filenames.csv')
csvreader = csv.reader(listofFiles) # Prepare the list of file names beforehand.



for x in listofFiles:
    fpath = x.strip()
    ds = dcmread(fpath)
    print(ds.PatientName)
    print(ds["PatientName"].VR)
    anonym_element = ["PN", "DA", "TM", "LO", "SH", "LT", "UI"] # Elements corresponding to Personal info.

    def person_names_callback(dataset, dataelements): # This function changes deletes the personal element info.
        for elem in dataset:    
            if elem.VR in dataelements:
                elem.value = None

    person_names_callback(ds, anonym_element)


    # for elem in ds: # This part is for testing the code!
    #     if elem.VR == "PN":
    #         print(elem)
    
    seperator = "."
    x_sep = fpath.split(seperator, 1)[0]
    print(x)
    output_file_name = x_sep + "anonymized.dcm"

    ds.save_as(output_file_name)