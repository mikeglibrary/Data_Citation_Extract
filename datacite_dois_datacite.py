import os
import re
import requests
import json
import csv
from PyPDF2 import PdfReader
import time  # Import time for pauses

parent_dir = 'C:/python_code/library_grant/pdf2'
datacite_api = 'https://api.datacite.org/dois'

csv_titles = ["Title", "DOI", "Created on", "Last Updated On", "Download count", "Cited By Count", "Number of Other Version", "Title of Citing Local PDF"]

# Create CSV file with headers
with open('out.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile, delimiter=',')
    my_writer.writerow(csv_titles)

directory = os.fsencode(parent_dir)

# Regular expression pattern to match DOIs common to datecite (10.5060/ and 10.34960/)
doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith('.pdf'):
        filepath = os.path.join(parent_dir, filename)
        print("Found PDF file: ", filepath)

        try:
            reader = PdfReader(filepath)

            # Check if the PDF is encrypted to prevent errors
            if reader.is_encrypted:
                try:
                    reader.decrypt("")  # Attempt to decrypt with an empty password
                except Exception as e:
                    print(f"Could not decrypt {filename}: {e}")
                    continue  # Skip this file if it can't be decrypted

            pdf_title = reader.getDocumentInfo().title

            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            str_text = str(text)

            # Find all DOIs in the extracted text
            doi_matches = re.findall(doi_pattern, str_text)
            print(f"Found possible DOIs: {doi_matches}")

            # Check each DOI against the DataCite API
            for doi in doi_matches:
                datacite_api_url = f"{datacite_api}/{doi}"
                print("Possible DataCite DOI URL is: ", datacite_api_url)

                response = requests.get(datacite_api_url)
                if response.status_code == 200:
                    print("DataCite URL Found")
                    
                    json_result = response.json()
                    authors = json_result["data"]["attributes"]["creators"]

                    titles = json_result["data"]["attributes"]["titles"]
                    title_ex = titles[0]
                    title = title_ex["title"]

                    created = json_result["data"]["attributes"]["created"]
                    last_updated = json_result["data"]["attributes"]["updated"]
                    download_count = json_result["data"]["attributes"]["downloadCount"]
                    citation_count = json_result["data"]["attributes"]["citationCount"]
                    version_count = json_result["data"]["attributes"]["versionCount"]
                    cited_by = pdf_title

                    csv_input = [title, doi, created, last_updated, download_count, citation_count, version_count, cited_by]

                    # Write the results to the CSV
                    with open('out.csv', 'a', newline='') as csvfile:
                        my_writer = csv.writer(csvfile, delimiter=',')
                        my_writer.writerow(csv_input)
                        
                    # Pause to give the DataCite API a break    
                    time.sleep(2)
                
                else:    
                    print("URL has no record on DataCite")                 

        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        print("End of files")