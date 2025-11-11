#' @importFrom readr read_csv
#' @importFrom stringr regex str_detect
#' @importFrom dplyr rename filter select pull %>% bind_rows
#' @importFrom utils download.file
#' @importFrom tidyr separate_rows

utils::globalVariables(c(
    "code",
    "Preferred Label",
    "Synonyms",
    "URI",
    "Definitions",
    "label"
))

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


#' Function that searches NCIT definitions file
#' 
#' Takes a search term and the column of the defs file to search by
#' Returns a dataframe with all matches to the parameters
#' 
#' @param term string to search df by
#' @param term_type column to search in df, default Name
#' @return a dataframe with matching rows to search term
#' @examples searchDefs("Tumor Size")
#' @export 
searchDefs <- function(term, term_type="Name") {
    acceptable_terms <- c("Name", "URI", "Code", "Definition")
    
    if (!(term_type %in% acceptable_terms)) {
        stop(paste0(term_type, 
                    " is not an acceptable search term.",
                    " Try: Name, URI, Code, or Definition"))
    }
    
    NCIT_defs = downloadCSVFile(NCIT_defs_url)
    
    if (term_type == "Name") {
        df <- searchNames(term, NCIT_defs)
        return(df)
    } else if (term_type == "URI") {
        df <- searchURIs(term, NCIT_defs) 
        return(df)
    } else if (term_type == "Code") {
        df <- searchCodes(term, NCIT_defs)
        return(df)
    } else {
        df <- searchDefinition(term, NCIT_defs)
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


## helper function 4: searchDefinitions, searches through defs in definitions df

searchDefinition <- function(term, df) {
    df_searched <- filter(df, str_detect(Definitions, regex(term, ignore_case = TRUE)))
    return(df_searched)
}