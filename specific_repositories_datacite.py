import os
import re
import requests
import json
import csv
from PyPDF2 import PdfReader

#prompt user for the directory where the PDFs are stored
print("Please enter the directory where your saved articles are stored")
raw_input = input()
parent_dir = raw_input

#define the URL used by the datacite API
datacite_api = 'https://api.datacite.org/dois'

#print the metadata headings to the CSV
csv_titles = ["Title", "DOI", "Created on", "Last Updated On", "Download count", "Cited By Count", "Number of Other Version", "Title of Citing Local PDF"]
with open('data_citation_metadata.csv', 'w', newline = '') as csvfile:
    my_writer = csv.writer(csvfile, delimiter = ',')
    my_writer.writerow(csv_titles)


directory = os.fsencode(parent_dir)

#loop through each file in the directory, searching for PDF files
for file in os.listdir(directory):
 
    filename = os.fsdecode(file)
    if filename.endswith('.pdf'): 
        
        #identify found PDF files
        filepath = parent_dir + "/" + filename
        print("Found PDF file: ", filepath)
 
        #read PDF files using PyPDF2
        reader = PdfReader(filepath)


        pdf_title = reader.getDocumentInfo().title
     
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        str_text = str(text)

        #extract all urls in the PDF
        urls = re.findall(r'(https?://[^\s]+)', str_text)
        data_urls_holder = []
        
        #identify URLs that contain data-related keywords
        data_url_keywords = ['zenodo', 'icpsr', 'csv', 'statista']
        
        for url in urls:
            for keyword in data_url_keywords:
                if keyword in url:
                    print("Found data citation URL: ", url)
                    data_urls_holder.append(url)
                    


        #search the data URLs for doi references that can be used with DataCite
        for data_urls in data_urls_holder:
            data_urls_work = re.sub('^(.*)(?=doi.org)',"", data_urls)
            data_urls_work = data_urls_work.replace("doi.org", "")
           # print("DOI extension is: ", data_urls_work)
            datacite_api_url = datacite_api + data_urls_work
            print("Extracting data citation metadata")
         
            #attempt to download metadata from DataCite
            response = requests.get(datacite_api_url)
            if response.status_code == 200:

                #get the json
                json_result = response.json()
                parsed_json = json.loads(json.dumps(json_result))
                
                #get important JSON values 
                authors = parsed_json["data"]["attributes"]["creators"]

                titles = parsed_json["data"]["attributes"]["titles"]
                title_ex = titles[0]
                title = title_ex["title"]

                doi_to_csv = data_urls_work

                created = parsed_json["data"]["attributes"]["created"]

                last_updated = parsed_json["data"]["attributes"]["updated"]

                download_count= parsed_json["data"]["attributes"]["downloadCount"]
                
                citation_count= parsed_json["data"]["attributes"]["citationCount"]

                version_count = parsed_json["data"]["attributes"]["versionCount"]

                cited_by = pdf_title
               
                #print the JSON values to CSV
                csv_input = [title, doi_to_csv, created, last_updated, download_count, citation_count, version_count, cited_by]

                with open('data_citation_metadata.csv', 'a', newline = '') as csvfile:
                    my_writer = csv.writer(csvfile, delimiter = ',')
                    my_writer.writerow(csv_input)
                
        continue
    else:
        print("Finished scanning all PDFs in the given directory")
        continue
