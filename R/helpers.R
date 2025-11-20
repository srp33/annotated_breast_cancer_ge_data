#' @importFrom dplyr filter %>% select distinct
#' @importFrom utils download.file
#' @importFrom stringr str_c str_starts
#' @importFrom readr read_tsv
#' @importFrom SummarizedExperiment SummarizedExperiment
#' @importFrom tibble column_to_rownames
#' @import tidyverse

utils::globalVariables(c(
    'Chromosome',
    'Dataset_ID',
    'Ensembl_Gene_ID',
    'Entrez_Gene_ID',
    'Gene_Biotype',
    'HGNC_Symbol'
))


##  download file from Zenodo
downloadZenodoFile <- function(identifier) {
    tmp_file_path <- str_c(tempdir(), "/", identifier[2], ".tsv.gz")
    
    if (!file.exists(tmp_file_path)) {
        download.file(paste0(
            "https://zenodo.org/records/", 
            identifier[1], 
            "/files/", 
            identifier[2], 
            "?download=1"), 
            tmp_file_path, 
            mode='wb')
    }
    
    return(read_tsv(tmp_file_path))
}


##  filter out repeat rows
filterRepeatRows <- function(expression_matrix) {
    expression_matrix <- expression_matrix %>%
        filter(!str_starts(Chromosome, 'H'))
    
    return(expression_matrix)
}

##  get metadata
getMetadata <- function(identifier) {
    metadata_identifier <- identifier[3:4]
    sample_metadata <- downloadZenodoFile(metadata_identifier) %>%
        column_to_rownames('Sample_ID')
    
    return(sample_metadata)
}

##  make feature data
makeFeatureData <- function(expression_matrix) {
    feature_data <- select(expression_matrix, 
                           Dataset_ID, Entrez_Gene_ID, 
                          HGNC_Symbol, Ensembl_Gene_ID, 
                          Chromosome, Gene_Biotype) %>%
        distinct(Ensembl_Gene_ID, .keep_all=TRUE) %>%
        column_to_rownames('Ensembl_Gene_ID')
    
    return(feature_data)
}


##  creating expression data matrix
makeDataMatrix <- function(dataset, start_col, end_col) {
    expressions <- select(dataset, Ensembl_Gene_ID, start_col:end_col)
    expression_matrix <- expressions %>%
        column_to_rownames('Ensembl_Gene_ID') %>%
        as.matrix()
    
    return(expression_matrix)
}

##  build SummarizedExperiment
makeSummarizedExperiment <- function(expressions, features, meta) {
    se <- SummarizedExperiment(
        assays = list(counts=expressions),
        rowData = features,
        colData = meta
    )
    
    return(se)
}

## make list of identifiers
identifiers <- list(
    GSE41197 = c('17428998','GSE41197.tsv.gz', 
                 '17429158', "GSE41197_metadata.tsv"),
    GSE10797 = c('17429390','GSE10797.tsv.gz', 
                 '17429390', 'GSE10797_metadata.tsv'),
    GSE59772 = c('17429395','GSE59772.tsv.gz', 
                 '17429395', 'GSE59772_metadata.tsv'),
    GSE10281 = c('17665426', 'GSE10281.tsv.gz',
                 '17665426', 'GSE10281_metadata.tsv'),
    GSE10780 = c("17665492", "GSE10780.tsv.gz",
                 "17665492", "GSE10780_metadata.tsv"),
    GSE96058_NextSeq = c("17665296", "GSE96058_NextSeq.tsv.gz",
                         "17665296", "GSE96058_NextSeq_metadata.tsv"),
    GSE96058_HiSeq = c("", "GSE96058_HiSeq.tsv.gz",
                       "", "GSE96058_HiSeq_metadata.tsv")
)
