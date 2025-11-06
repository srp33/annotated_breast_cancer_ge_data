import pandas as pd
import requests 
import os

"""
This first part of the code downloads the original NCIT definitions file.
This is a large file! It may take a minute to download. Please let us 
know if it raises an error while trying to download. The link may need to
be updated. 

The next file it downloads is the Excel file that relates the definitions
and ontology terms to the actual datasets. 

The downloads should only happen the first time you run the code as it is
designed to check if the file path exists before downloading. 

IF RECENT CHANGES HAVE BEEN MADE TO THE DEFINITIONS FILE OR THE XL FILE:
    Make sure you delete the original download before running the code!
    If the file path still exists, it will not rewrite it with the new
    file and you will be using out of date files.  

"""

def_url = "https://data.bioontology.org/ontologies/NCIT/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&download_format=csv"
def_filename = "NCIT_definitions.csv"

map_url = "https://zenodo.org/records/17545645/files/mapping_file.xlsx?download=1"
map_filename = "mapping_file.xlsx"

if not os.path.exists(def_filename):

    response = requests.get(def_url)
    response.raise_for_status()

    with open(def_filename, "wb") as file:
        file.write(response.content)

if not os.path.exists(map_filename):

    m_response = requests.get(map_url)
    m_response.raise_for_status()

    with open(map_filename, "wb") as f:
        f.write(m_response.content)


"""
This part of the code reads the files downloaded into variables. The
first file is the NCIT definitions file. The second is the Excel file
With the information relating ontology terms to the actual data sets. 

The code then slightly modefies the mapping file dataframes to only 
include columns that will be used in this part of the project. 

"""

ncit_df = pd.read_csv("NCIT_definitions.csv", low_memory=False)

ont_cate = pd.read_excel("mapping_file.xlsx", sheet_name="Categorical")
ont_nume = pd.read_excel("mapping_file.xlsx", sheet_name="Numerical")
ont_rang = pd.read_excel("mapping_file.xlsx", sheet_name="Ranged")
ont_surec = pd.read_excel("mapping_file.xlsx", sheet_name="Survival-Recurrence Problems")

ont_cate_cols = ont_cate.iloc[:,0:3].copy()
ont_nume_cols = ont_nume.iloc[:,0:3].copy()
ont_rang_cols = ont_rang.iloc[:,0:3].copy()
ont_surec_cols = ont_surec.iloc[:,0:3].copy()


"""
This part of the code defines an apply function for the dataframe 
that creates a new column in the mapping dataframes containing only
the NCIT code. This is important for comparing the definitions file
and the mapping files. 

The code then applies this function to the mapping dataframes,
creating the new columns. It then pulls just the codes as a list to 
compare the codes included in the definitions dataframe. 

"""

def get_codes(row):
    ncit_term = row["NCIT_field"]

    if "||" not in ncit_term:
        ncit_list = ncit_term.split(" ")
        ncit_with_paren = ncit_list[-1]
        code_len = len(ncit_with_paren)
        code = ncit_with_paren[0:code_len-1]
        return [code]

    else:
        ncit_list = ncit_term.split('||')
        code_list = []
        for term in ncit_list:
            ncit_list = term.split(" ")
            ncit_with_paren = ncit_list[-1]
            code_len = len(ncit_with_paren)
            code = ncit_with_paren[0:code_len-1]
            code_list.append(code)
        return code_list

ont_cate_cols["NCIT_code"] = ont_cate_cols.apply(get_codes, axis=1)
ont_nume_cols["NCIT_code"] = ont_nume_cols.apply(get_codes, axis=1)
ont_rang_cols["NCIT_code"] = ont_rang_cols.apply(get_codes, axis=1)
ont_surec_cols["NCIT_code"] = ont_surec_cols.apply(get_codes, axis=1)

cate_codes = ont_cate_cols["NCIT_code"].tolist()
nume_codes = ont_nume_cols["NCIT_code"].tolist()
rang_codes = ont_rang_cols["NCIT_code"].tolist()
surec_codes = ont_surec_cols["NCIT_code"].tolist()

all_codes_list = cate_codes + nume_codes + rang_codes + surec_codes 
all_codes_no_list = [code for lst in all_codes_list for code in lst]
all_codes = set(all_codes_no_list)

"""
This part of the code first filters the definitions dataframe to only
include rows with codes that are in the all_codes list. This filters it
to only have the terms and definitions that are used in the ontology
mapping file (and thus the data).

Line 147 adds the term "Metastasis-Free Survival", which wasn't included
in the original definitions file. The following lines correct values that 
were listed as "NA" in the definitions file. 

When adding new terms to the definitions file, check these 3 things before
uploading the updated file to Zenodo:
    
    1. Was the code in the original definitions file, and therefore did the
        new term actually get added?
    
    2. Are there any NA values in the term you added?
    
    3. Is the term you added (or any of the terms currently in the file)
        considered obsolete? If so, please update them. 

When adding a term to the definitions file, running the code once should be
sufficient to create the updated version of the file on your machine. If the
above cases are correct, you shouldn't have to actually write any code. 

"""

ncit_filter_codes = ncit_df[ncit_df["code"].isin(all_codes)]
ncit_select_cols = ncit_filter_codes[["Class ID", "Preferred Label", "Synonyms", "Definitions", "code"]]
ncit_select_cols = ncit_select_cols.reset_index(drop=True)
ncit_select_cols.loc[len(ncit_select_cols)] = ["http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C210589", "Metastasis-Free Survival", "Metastasis Free Survival, Metastasis-Free Survival", "The length of time a patient has no evidence of the spread of their cancer.", "C210589"]
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Intratumoral", "Definitions"] = "Within a tumor."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Endocrine Drug Therapy", "Definitions"] = "Drug therapy that uses an endocrine hormone."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Taxane Compound", "Definitions"] = "A type of drug that blocks cell growth by stopping mitosis (cell division). Taxanes interfere with microtubules (cellular structures that help move chromosomes during mitosis). They are used to treat cancer. A taxane is a type of mitotic inhibitor and a type of antimicrotubule agent."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Polysomy 17", "Definitions"] = "A chromosomal abnormality characterized by the presence of more than two copies of chromosome 17 in a cell."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Pleomorphic", "Definitions"] = "Occurring in various distinct forms. In terms of cells, having variation in the size and shape of cells or their nuclei."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Treatment Status", "Definitions"] = "Type of treatment if applicable"
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Nuclear Grade", "Definitions"] = "An evaluation of the size and shape of the nucleus in tumor cells and the percentage of tumor cells that are in the process of dividing or growing. Cancers with low nuclear grade grow and spread less quickly than cancers with high nuclear grade."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Generic Regional Lymph Nodes TNM Finding", "Definitions"] = "A finding about one or more characteristics of cancer, following the rules of the TNM AJCC classification system as they pertain to staging of the regional lymph nodes."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Generic Primary Tumor TNM Finding", "Definitions"] = "A finding about one or more characteristics of cancer, following the rules of the TNM AJCC classification system as they pertain to staging of the primary tumor."
ncit_select_cols.loc[ncit_select_cols["Preferred Label"]=="Prediction of Response to Therapy", "Definitions"] = "General prediction about patient response to given therapy"


"""
The original NCIT definitions file called the URI column Class ID, so we
rename it here. The final line of code creates the updated .csv file. 

After making a change or update to the .csv file, please upload it to
Zenodo to reflect the change (upload as a new version of the old file).
If any changes were made to this file in order to add the term, please
update this file in GitHub. Lastly, make sure the correct version of the
definitions file is accessed by AnnotatedBCGEData.

"""

ncit_select_cols = ncit_select_cols.rename(columns={"Class ID": "URI"})

ncit_select_cols.to_csv("NCIT_definitions_filtered.csv", index=False)