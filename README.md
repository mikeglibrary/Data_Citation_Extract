# Data Citation Extraction Scripts

Three simple Python scripts that extract the DOIs from academic article PDFs and then verifies whether the DOIs reference data whose metadata is available through the DataCite API. If metadata is available through the DataCite API, corresponding metadata is downloaded to a CSV file. 

The file, all_dois_datacite.py, checks all DOIs in an academic article against the DataCite API.

The file, datacite_dois_datacite.py, checks only DOIs commonly used by DataCite against the DataCite API (10.5060 or 10.34960).  

The file, specific_repositories_datacite.py, checks DOIs specific to data repositories such as Zenodo. Repositories can be added or removed using the data_url_keywords variable on line 48 of the script.

# How to Use

After running one of the DOI extraction scripts, you will be prompted to enter the directory where your PDF files are stored. Once you enter the directory, the script will begin searching for data set citations within the PDF files stored in this directory.

# Requirements

This script relies on the PyPDF2 (https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html) package to extract text from PDFs.

# Acknowledgements

The development of this script was funded by a Concordia University Library (https://library.concordia.ca/) research grant. The code in this repository was primarily written by Concordia student Raeika Maroufi, with some additional coding done by Michael Groenendyk. 
