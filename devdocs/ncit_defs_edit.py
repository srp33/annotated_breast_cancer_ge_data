import pandas as pd

ncit_df = pd.read_csv("NCIT_definitions.csv", low_memory=False)

ont_cate = pd.read_excel("mapping_file.xlsx", sheet_name="Categorical")
ont_nume = pd.read_excel("mapping_file.xlsx", sheet_name="Numerical")
ont_rang = pd.read_excel("mapping_file.xlsx", sheet_name="Ranged")
ont_surec = pd.read_excel("mapping_file.xlsx", sheet_name="Survival-Recurrence Problems")

ont_cate_cols = ont_cate.iloc[:,0:3].copy()
ont_nume_cols = ont_nume.iloc[:,0:3].copy()
ont_rang_cols = ont_rang.iloc[:,0:3].copy()
ont_surec_cols = ont_surec.iloc[:,0:3].copy()

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

ncit_filter_codes = ncit_df[ncit_df["code"].isin(all_codes)]
ncit_select_cols = ncit_filter_codes[["Preferred Label", "Synonyms", "Definitions", "code"]]
ncit_select_cols = ncit_select_cols.reset_index(drop=True)
ncit_select_cols.loc[len(ncit_select_cols)] = ["http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C210589", "Metastasis-Free Survival", "Metastasis Free Survival, Metastasis-Free Survival", "The length of time a patient has no evidence of the spread of their cancer."]
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

ncit_select_cols.to_csv("NCIT_definitions_filtered.csv", index=False)