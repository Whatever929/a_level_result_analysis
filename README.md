Overview
------
Exploratory data analysis of Cambridge International A Levels from year 2015 to year 2021. 

Scripts
-----
- `scrape.py` scrapes all statistics and grade threshold PDF files available in the official websites to your local machine.
- `pdf_to_csv_stat.py` converts the PDF files related to statistics stored in `PDF_PATH` (Stored as constant at the beginning of the script) to CSV files, using Tabula. It will print a preview of the resulting CSV file to the console for checking. If all available Tabula templates fail to extract data correctly, it will write the file name to `error.txt`. You will need to do the convertion manually using Tabula application.
- `clean_csv_stat.py` combines statistics CSV files of all exam series into a single CSV file. 

Various constants such as output path and website link are declared at the beginning of each script. You can change the values before running the script.

Data
---
`csv` folder contains the cleaned version of the data.

To-do
----
- Clean and analyze grade threshold data 
