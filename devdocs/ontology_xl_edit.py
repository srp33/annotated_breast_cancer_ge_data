import pandas as pd 
import requests 
import os

"""
This first part of the code downloads the mapping file from Zenodo.
If the file is already on your computer, it does nothing. If changes
have been made to the mapping file recently, make sure you delete
your local copy of the mapping file before running this code, or it
will not overwrite it. 

"""

map_url = "https://zenodo.org/records/17545645/files/mapping_file.xlsx?download=1"
map_filename = "mapping_file.xlsx"

if not os.path.exists(map_filename):
    response = requests.get(map_url)
    response.raise_for_status()

    with open(map_filename, "wb") as file:
        file.write(response.content)


"""
This part of the code reads the mapping file into pandas dataframes.
The dataframes then split the NCIT field column by ||, then makes a 
new row for each item in the new list. This ensures there is only one 
term name per line. The code then drops the extra "comments" column
that was created for data curation. 

The get_code function gets just the NCIT code from the NCIT field name.
The function is then used with the .apply function for each dataframe,
making a new column with just the NCIT code.

"""

ont_cate = pd.read_excel("mapping_file.xlsx", sheet_name="Categorical")
ont_nume = pd.read_excel("mapping_file.xlsx", sheet_name="Numerical")
ont_rang = pd.read_excel("mapping_file.xlsx", sheet_name="Ranged")

ont_cate["NCIT_field"] = ont_cate["NCIT_field"].str.split('||', regex=False)
ont_cate = ont_cate.explode('NCIT_field').reset_index(drop=True)
ont_cate = ont_cate.iloc[:,0:4]

ont_nume["NCIT_field"] = ont_nume["NCIT_field"].str.split('||', regex=False)
ont_nume = ont_nume.explode('NCIT_field').reset_index(drop=True)
ont_nume = ont_nume.iloc[:,0:4]

ont_rang["NCIT_field"] = ont_rang["NCIT_field"].str.split('||', regex=False)
ont_rang = ont_rang.explode('NCIT_field').reset_index(drop=True)
ont_rang = ont_rang.iloc[:,0:4]

def get_codes(row):
    ncit_term = row["NCIT_field"]

    ncit_list = ncit_term.split(" ")
    ncit_with_paren = ncit_list[-1]
    code_len = len(ncit_with_paren)
    code = ncit_with_paren[0:code_len-1]
    return code

ont_cate["NCIT_field_code"] = ont_cate.apply(get_codes, axis=1)
ont_nume["NCIT_field_code"] = ont_nume.apply(get_codes, axis=1)
ont_rang["NCIT_field_code"] = ont_rang.apply(get_codes, axis=1)


"""
This code writes the adjusted dataframes to csv files. Make
sure you upload the updated csv files to Zenodo after they
have been updated, and that the code pulls the correct version. 

"""

ont_cate.to_csv("mapped_categorical.csv", index=False)
ont_nume.to_csv("mapped_numerical.csv", index=False)
ont_rang.to_csv("mapped_ranged.csv", index=False)