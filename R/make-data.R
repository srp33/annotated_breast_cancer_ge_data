#' Function that creates downloads data and creates SummarizedExperiment object
#' 
#' Takes a name of data set and passes to identifiers named list
#' Uses the vector of identifiers in the list to get URL and download
#' 
#' @param identifier name of data set
#' @param identifier_list list of identifiers, defaults to current list
#' @return a SummarizedExperiment object for the data set
#' @examples makeObject('GSE41197')
#' @export
makeObject <- function(identifier, identifier_list=identifiers) {
    identifier_vec <- identifier_list[[identifier]]
    expression_data <- downloadZenodoFile(identifier_vec) %>%
        filterRepeatRows()
    start_col <- colnames(expression_data)[7]
    end_col <- colnames(expression_data)[ncol(expression_data)]
    
    expression_matrix <- makeDataMatrix(expression_data, start_col, end_col)
    
    sample_metadata <- getMetadata(identifier_vec)
    
    feature_data <- makeFeatureData(expression_data)
    
    se <- makeSummarizedExperiment(
        expression_matrix,
        feature_data,
        sample_metadata)
    
    return(se)
}