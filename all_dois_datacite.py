import os
import re
import requests
import json
import csv
from PyPDF2 import PdfReader

parent_dir = 'C:/python_code/library_grant/pdf2'
datacite_api = 'https://api.datacite.org/dois'

csv_titles = ["Title", "DOI", "Created on", "Last Updated On", "Download count", "Cited By Count", "Number of Other Version", "Title of Citing Local PDF"]

# Create CSV file with headers
with open('out.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile, delimiter=',')
    my_writer.writerow(csv_titles)

directory = os.fsencode(parent_dir)

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

            # Find all URLs in the extracted text
            urls = re.findall(r'(https?://[^\s]+)', str_text)

            # Filter URLs that contain 'doi'
            doi_urls = [url for url in urls if 'doi' in url]
            print(f"Found DOI URLs: {doi_urls}")

            for doi_url in doi_urls:
                # Extract DOI from the URL
                doi_to_check = re.sub(r'.*doi.org/', '', doi_url)  # Extract the DOI part
                datacite_api_url = f"{datacite_api}/{doi_to_check}"
                print("DOI URL is: ", datacite_api_url)

                response = requests.get(datacite_api_url)
                if response.status_code == 200:
                    
                    print("Datacite URL Found")
                    
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

                    csv_input = [title, doi_to_check, created, last_updated, download_count, citation_count, version_count, cited_by]

                    # Write the results to the CSV
                    with open('out.csv', 'a', newline='') as csvfile:
                        my_writer = csv.writer(csvfile, delimiter=',')
                        my_writer.writerow(csv_input)
                        
                    #pause to give the datacite api a break    
                    time.sleep(2)
                
                else:    

                    print("URL has no record on DataCite")                

        except Exception as e:
            print(f"Error processing {filename}: {e}")
    else:
        print("End of files")