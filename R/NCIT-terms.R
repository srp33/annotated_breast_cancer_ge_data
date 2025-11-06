library(tidyverse)

## Download .csv NCIT definitions file from Zenodo
## This code is different from downloadZenodoFile because it is a csv

downloadCSVFile <- function(url) {
    temp_file_path <- str_c(tempdir(), "/", "NCIT_definitions_filtered.csv")
    
    if (!file.exists(temp_file_path)) {
        download.file(url, temp_file_path, mode="wb")
    }
    
    return (read_csv(temp_file_path))
}

NCIT_defs_url <- "https://zenodo.org/records/17545810/files/NCIT_definitions_filtered.csv?download=1"



## base function that is called by user. different parameters call different
## helper functions, eventually returns dataframe matching parameters

searchDefs <- function(term, term_type="Name") {
    acceptable_terms <- c("Name", "URI", "Code")
    
    if (!(term_type %in% acceptable_terms)) {
        stop(paste0(term_type, 
                    " is not an acceptable search term.",
                    " Try: Name, URI, or Code."))
    }
    
    NCIT_defs = downloadCSVFile(NCIT_defs_url)
    
    if (term_type == "Name") {
        df <- searchNames(term, NCIT_defs)
        return(df)
    } else if (term_type == "URI") {
        df <- searchURIs(term, NCIT_defs) 
        return(df)
    } else {
        df <- searchCodes(term, NCIT_defs)
        return(df)
    }
}


## helper function 1: searchNames, searches through Names in definitions df

searchNames <- function(term, df) {
    ncit_names <- rename(df, label = `Preferred Label`) %>%
        select(label, code)
    
    ncit_synonyms <- rename(df, label = Synonyms) %>%
        select(label, code) %>%
        separate_rows(label, sep = "\\|")
    
    names_syns <- bind_rows(ncit_names, ncit_synonyms) %>%
        filter(str_detect(label, regex(term, ignore_case=TRUE))) %>%
        pull(code)
    
    codes <- unique(names_syns)
    
    df_searched <- filter(df, code %in% codes)
    
    return(df_searched)
}


## helper function 2: searchURI, searches through URIs in definitions df

searchURIs <- function(term, df) {
    df_searched <- filter(df, URI==term) 
    return(df_searched)
}


## helper function 3: searchCodes, searches through codes in definitions df

searchCodes <- function(term, df) {
    df_searched <- filter(df, code==term)
    return(df_searched)
}