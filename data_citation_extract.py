import os
import re
import requests
import json
import csv
from PyPDF2 import PdfReader


print("Please enter the directory where your saved articles are stored")
raw_input = input()
parent_dir = raw_input
datacite_api = 'https://api.datacite.org/dois'

csv_titles = ["Title", "DOI", "Created on", "Last Updated On", "Download count", "Cited By Count", "Number of Other Version", "Title of Citing Local PDF"]
with open('data_citation_metadata.csv', 'w', newline = '') as csvfile:
    my_writer = csv.writer(csvfile, delimiter = ',')
    my_writer.writerow(csv_titles)

directory = os.fsencode(parent_dir)
for file in os.listdir(directory):
 
    filename = os.fsdecode(file)
    if filename.endswith('.pdf'): 
        
        filepath = parent_dir + "/" + filename
        print("Found PDF file: ", filepath)
 
        
        reader = PdfReader(filepath)


        pdf_title = reader.getDocumentInfo().title
     
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        str_text = str(text)

        urls = re.findall(r'(https?://[^\s]+)', str_text)
        data_urls_holder = []
        
        data_url_keywords = ['zenodo', 'icpsr', 'csv', 'statista']

        for url in urls:
            for keyword in data_url_keywords:
                if keyword in url:
                    print("Found data citation URL: ", url)
                    data_urls_holder.append(url)
                    

       # print("URls: ", urls)    
       # print("Data URLS: ", data_urls_holder)

        for data_urls in data_urls_holder:
            data_urls_work = re.sub('^(.*)(?=doi.org)',"", data_urls)
            data_urls_work = data_urls_work.replace("doi.org", "")
           # print("DOI extension is: ", data_urls_work)
            datacite_api_url = datacite_api + data_urls_work
            print("Extracting data citation metadata")
           # datacite_url_get = datacite_api + data_urls
            response = requests.get(datacite_api_url)
            if response.status_code == 200:
                json_result = response.json()
                parsed_json = json.loads(json.dumps(json_result))
                
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

                csv_input = [title, doi_to_csv, created, last_updated, download_count, citation_count, version_count, cited_by]

                with open('data_citation_metadata.csv', 'a', newline = '') as csvfile:
                    my_writer = csv.writer(csvfile, delimiter = ',')
                    my_writer.writerow(csv_input)
                
        continue
    else:
        print("Finished scanning all PDFs in the given directory")
        continue
