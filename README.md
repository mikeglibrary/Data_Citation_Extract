# Data Citation Extraction Script (First Draft - Work in Progress)

This is a simple Python script to extract the data citations from all academic article PDFs saved in a specific directory. The script uses the Data Cite API to download the metadata for each cited data set and then prints this metadata to a CSV file.  

# How to Use

After running the script, you will be prompted to enter the directory where your PDF files are stored. Once you enter the directory, the script will begin searching for data set citations within the PDF files stored in the directory.

# Requirements

This script relies on the PyPDF2 (https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html) package to extract text from PDFs.

# Acknowledgements

The development of this script was funded by a Concordia University Library (https://library.concordia.ca/) research grant.
