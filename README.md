
<!-- README.md is generated from README.Rmd. Please edit that file -->

# AnnotatedBCGEData

<!-- badges: start -->

[![GitHub
issues](https://img.shields.io/github/issues/srp33/AnnotatedBCGEData)](https://github.com/srp33/AnnotatedBCGEData/issues)
[![GitHub
pulls](https://img.shields.io/github/issues-pr/srp33/AnnotatedBCGEData)](https://github.com/srp33/AnnotatedBCGEData/pulls)
<!-- badges: end -->

`AnnotatedBCGEData` is an R package that uses the ExperimentHub
infrastructure in [Bioconductor](https://bioconductor.org/). To create
this package, we gathered more than 100 gene-expression data sets
(microarray and RNA-Sequencing) from public repositories, including
[Gene Expression Omnibus](http://www.ncbi.nlm.nih.gov/geo/),
[ArrayExpress](https://www.ebi.ac.uk/biostudies/arrayexpress), and [The
Cancer Genome
Atlas](https://www.cancer.gov/ccg/research/genome-sequencing/tcga).
Where feasible, we obtained raw data and reprocessed the data using
modern computational pipelines. Additionally, we provide metadata in an
easy-to-use format. Our goal is to provide researchers with easier
access to these data with the goal of accelerating biomedical discovery.

## Installation instructions

Get the latest stable `R` release from
[CRAN](http://cran.r-project.org/). Then install `AnnotatedBCGEData`
from [Bioconductor](http://bioconductor.org/) using the following code:

``` r
if (!requireNamespace("BiocManager", quietly = TRUE)) {
    install.packages("BiocManager")
}

BiocManager::install("AnnotatedBCGEData")
```

This code installs BiocManager if it is not already installed. Running
the if statement is required to install the package as it is dependent
on BiocManager to load.

Download the development version from
[GitHub](https://github.com/srp33/AnnotatedBCGEData) with:

``` r
BiocManager::install("srp33/AnnotatedBCGEData")
```

## Data Info

The data used in this package was accessed through
[Zenodo](https://zenodo.org/communities/annnotatedbcgedata/records?q=&l=list&p=1&s=10&sort=newest).
This database allowed us to use data that was already neat and ready to
be analyzed. However, the original data came from Gene Expression
Omnibus (GEO), ArrayExpress, and The Cancer Genome Atlas. Learn more
about the data at the following links:

- GSE41197:
  <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE41197>
- GSE10797:
  <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE10797>
- GSE59772:
  <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE59772>

The package itself includes a metadata file as required by Bioconductor.
This file is a table that lists the name of each object and more
information about where it came from and how it was accessed. See
inst/extdata/metadata.csv.

# Filtering Data by Ontology

The following code is required to access the tools and data included in
AnnotatedBCGEData:

``` r
library(AnnotatedBCGEData)
```

This package contains several functions that are designed to help users
filter the included data sets based on their associated ontology terms.
The first function is `searchDefs`. This function takes two parameters:
the term to search by and the type of term it is. The options for terms
are Name, URI, Code, and Definition. If no term type is specified, the
function defaults to Name.

## Example: Searching for a data set by ontology term name

In this first example of using the `searchDefs` function, we search for
a particular ontology term, “Progesterone Receptor Status”.

``` r
searchDefs("Progesterone Receptor Status")
#> Rows: 198 Columns: 5
#> ── Column specification ────────────────────────────────────────────────────────
#> Delimiter: ","
#> chr (5): URI, Preferred Label, Synonyms, Definitions, code
#> 
#> ℹ Use `spec()` to retrieve the full column specification for this data.
#> ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.
#> # A tibble: 1 × 5
#>   URI                               `Preferred Label` Synonyms Definitions code 
#>   <chr>                             <chr>             <chr>    <chr>       <chr>
#> 1 http://ncicb.nci.nih.gov/xml/owl… Progesterone Rec… Progest… Indicates … C161…
```

The output of calling this function is a tibble containing the URI, the
name of the term, synonyms, the definition, and the NCIT code associated
with it. When the correct term is identified, the user can then pass the
URI to the `searchForDatasets` function, which identifies data sets that
contain the chosen ontology term.

## Example: Searching for a data set by ontology term definition

In this example, we search for the ontology term by an associated
definition. Because the definitions are more vague, this may identify
several similar terms. It is important that the user is able to identify
the exact term they are looking for.

``` r
searchDefs("Progesterone receptor", "Definition")
#> Rows: 198 Columns: 5
#> ── Column specification ────────────────────────────────────────────────────────
#> Delimiter: ","
#> chr (5): URI, Preferred Label, Synonyms, Definitions, code
#> 
#> ℹ Use `spec()` to retrieve the full column specification for this data.
#> ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.
#> # A tibble: 2 × 5
#>   URI                               `Preferred Label` Synonyms Definitions code 
#>   <chr>                             <chr>             <chr>    <chr>       <chr>
#> 1 http://ncicb.nci.nih.gov/xml/owl… Progesterone Rec… Progest… Indicates … C161…
#> 2 http://ncicb.nci.nih.gov/xml/owl… Triple-Negative … Triple … An invasiv… C717…
```

Again, when the chosen term is identified, it can be passed to the
`searchForDatasets` function.

# Examples

Downloading this package does not download the data sets onto the user’s
machine. To load the SummarizedExperiment object for a data set included
in AnnotatedBCGEData, the user chooses the name of the data set and
passes it as a string to the function makeObject. This function
downloads the data and creates the SummarizedExperiment object that is
accessible to the user. To see a comprehensive list of all data sets
included and where they came from, see the metadata.csv file in
inst/extdata/metadata.csv. This will be accessible in the code when the
package is available in ExperimentHub. <br> <br> The
SummarizedExperiment object for each data set includes 3 matrices. The
first, which we load as expression_data, is a matrix with the samples as
columns and genes as rows. The Ensembl gene ID is used as the row names.
The data in the actual matrix is the expression level of the gene for
the sample. <br> <br> The second matrix we load as sample_metadata. This
is information about the samples themselves, such as demographics for
the patient the sample came from. The samples are rows and the
information is in the columns. <br> <br> The third matrix we load as
feature_data. This is the information about the genes that were tested
for each sample. This includes information like the chromosome the gene
is located on, the Entrez gene ID, and the gene name. The genes are the
rows and the information about the samples is in the columns.

``` r
GSE41197_SE = makeObject("GSE41197")
#> Rows: 9593 Columns: 22
#> ── Column specification ────────────────────────────────────────────────────────
#> Delimiter: "\t"
#> chr  (5): Dataset_ID, HGNC_Symbol, Ensembl_Gene_ID, Chromosome, Gene_Biotype
#> dbl (17): Entrez_Gene_ID, GSM1010328, GSM1010329, GSM1010330, GSM1010331, GS...
#> 
#> ℹ Use `spec()` to retrieve the full column specification for this data.
#> ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.
#> Rows: 16 Columns: 5
#> ── Column specification ────────────────────────────────────────────────────────
#> Delimiter: "\t"
#> chr (5): Dataset_ID, Sample_ID, Platform_ID, Patient_ID, disease_state
#> 
#> ℹ Use `spec()` to retrieve the full column specification for this data.
#> ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.
expression_data = assay(GSE41197_SE)
sample_metadata = colData(GSE41197_SE)
feature_data = rowData(GSE41197_SE)
```

## Plot Example 1: Bar plot

In the following example, we first access the matrix of gene expression
values. To make it easier to analyze, we convert it into a tibble and
select the first 10 rows. We then used ggplot() to create a bar plot
showing the gene expression levels for one sample across 10 genes.

``` r
GSE41197 = makeObject("GSE41197")
gene_expression_values = assay(GSE41197)
```

``` r
exp_tib = as_tibble(gene_expression_values, rownames='Ensembl_Gene_ID')[1:10,] %>%
    ggplot(aes(x=Ensembl_Gene_ID, y=GSM1010328)) +
    geom_col() +
    labs(x='Ensembl Gene ID',y='Sample ID GSM1010328') +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))

exp_tib
```

<img src="man/figures/README-plot_example_p_2-1.png" width="100%" />

## Example 2: Boxplot with expression values

Here, we first accessed the matrices for 3 data sets included in
AnnotatedBCGEData.

``` r
GSE10797_SE = makeObject("GSE10797")
GSE41197_SE = makeObject("GSE41197")
GSE59772_SE = makeObject("GSE59772")

GSE10197 = assay(GSE10797_SE)
GSE41197 = assay(GSE41197_SE)
GSE59772 = assay(GSE59772_SE)
```

Next, we converted each to a tibble and selected one row, representing
one gene that we knew each data set had in common. We rotated the
tibbles to have one column (the gene) and many rows (the sample). Then,
we added the ‘group’ column, which was necessary for the function used
in the next step.

``` r
GSE10197_gene = GSE10197 %>%
    as_tibble(rownames='Ensembl_Gene_ID') %>%
    filter(Ensembl_Gene_ID == "ENSG00000171428") %>%
    pivot_longer(cols=-Ensembl_Gene_ID,names_to='Sample_ID',values_to='Expression_Level')%>%
    mutate(group = 'GSE10197')
GSE41197_gene = GSE41197 %>%
    as_tibble(rownames='Ensembl_Gene_ID') %>%
    filter(Ensembl_Gene_ID == "ENSG00000171428") %>%
    pivot_longer(cols=-Ensembl_Gene_ID,names_to='Sample_ID',values_to='Expression_Level')%>%
    mutate(group = 'GSE41197')
GSE59772_gene = GSE59772 %>%
    as_tibble(rownames='Ensembl_Gene_ID') %>%
    filter(Ensembl_Gene_ID == "ENSG00000171428") %>%
    pivot_longer(cols=-Ensembl_Gene_ID,names_to='Sample_ID',values_to='Expression_Level')%>%
    mutate(group = 'GSE59772')
```

We then joined the 3 tibbles into one tibble with the bind_rows()
function. We now have one tibble with one column (the gene) and many
rows (the samples). <br> <br> Finally, we used ggplot() to visualize the
expression levels for the gene across the three data sets.

``` r
combined_samples = bind_rows(GSE10197_gene, GSE41197_gene, GSE59772_gene)

ggplot(combined_samples, aes(x = group, y = Expression_Level, fill = group)) +
    geom_boxplot() +
    labs(x = "Dataset", y = "Expression Level") +
    theme_bw()
```

<img src="man/figures/README-plot_example_2_part_3-1.png" width="100%" />

## Example 3: Heat map

In this example, we combine using both the metadata and the expression
data to create a heat map of gene expression levels.<br> First, we load
the data sets, turn them into tibbles, and extract both the metadata and
expression data. We then filter the expression to only include the
samples that are identified as stroma cells. Finally, we create two
vectors with all the gene names in each tibble to set them up for
comparison.

``` r
GSE59772 = makeObject("GSE59772")
GSE59772_metadata = colData(GSE59772) %>%
    as_tibble(rownames = 'Sample_ID')

GSE59772_stroma_samples = filter(GSE59772_metadata, tissue == 'Stroma') %>%
    pull(Sample_ID)

GSE59772_gene_names = assay(GSE59772) %>%
    as_tibble(rownames="Ensembl_Gene_ID") %>%
    pull(Ensembl_Gene_ID)


GSE10797 = makeObject("GSE10797")
GSE10797_metadata = colData(GSE10797) %>%
    as_tibble(rownames = 'Sample_ID')

GSE10797_gene_names = assay(GSE10797) %>%
    as_tibble(rownames="Ensembl_Gene_ID") %>%
    pull(Ensembl_Gene_ID)

GSE10797_stroma_samples = filter(GSE10797_metadata, tissue_source == 'stromal cells from breast cancer patient')%>%
    pull(Sample_ID)
```

Next, we create a vector that has only the names of the genes the data
sets have in common. We use this vector to filter the expression tibbles
again to only include rows with genes in the vector.

``` r
common_genes = c()
for (gene in GSE59772_gene_names) {
    if (gene %in% GSE10797_gene_names) {
        common_genes = c(common_genes, gene)
    }
}

GSE59772_stroma_expressions = assay(GSE59772) %>%
    as_tibble(rownames= 'Ensembl_Gene_ID') %>%
    select(Ensembl_Gene_ID, all_of(GSE59772_stroma_samples)) %>%
    filter(Ensembl_Gene_ID %in% common_genes)
    
GSE10797_stroma_expressions = assay(GSE10797) %>%
    as_tibble(rownames = 'Ensembl_Gene_ID') %>%
    select(Ensembl_Gene_ID, all_of(GSE10797_stroma_samples)) %>% 
    filter(Ensembl_Gene_ID %in% common_genes)
```

Finally, we combine the data into one tibble called combined_data. We
make a new row called variance that calculates the variance across the 5
samples. We select the top 10 rows, those with greatest variance. We
then use ggplot to create a heat map of the genes with the top variance,
displayed below.

``` r
combined_data = full_join(GSE10797_stroma_expressions, GSE59772_stroma_expressions)
#> Joining with `by = join_by(Ensembl_Gene_ID)`
top_variance_genes = combined_data %>%
    rowwise() %>%
    mutate(variance = var(c_across(starts_with('GSM')))) %>%
    ungroup() %>%
    arrange(desc(variance)) %>%
    slice_head(n=10)

top_variance_map = top_variance_genes %>%
    select(-variance) %>%
    pivot_longer(cols = starts_with('GSM'), names_to = 'Sample_ID', values_to = 'Expression') %>%
    ggplot(aes(x = Sample_ID, y = Ensembl_Gene_ID, fill = Expression)) +
    geom_tile()+
    labs(x = 'Sample', y = 'Gene', fill = 'Expression', title = 'Top 10 Genes in Stroma Samples with Highest Variance') + 
    theme_bw() + 
    theme(axis.text.x = element_text(angle = 45, hjust = 1), plot.title = element_text(hjust = 0.5, face = "bold"))
top_variance_map
```

<img src="man/figures/README-heat_map_3-1.png" width="100%" />

## Example 4: Combining feature data and expression data

In this final example, we use aspects of the feature data along with the
expression data. <br> <br>

First, we get the feature data and convert it to a tibble. We then
filter this data for each data set to only include genes on chromosome
16. Similar to the last example, we also make a vector with the gene
names the data sets have in common.

``` r
GSE59772 = makeObject("GSE59772")
GSE59772_featuredata = rowData(GSE59772) %>%
    as_tibble(rownames = 'Ensembl_Gene_ID')

GSE59772_chr16 = GSE59772_featuredata %>%
    filter(Chromosome == '16') %>%
    pull(Ensembl_Gene_ID)

GSE59772_gene_names = assay(GSE59772) %>%
    as_tibble(rownames="Ensembl_Gene_ID") %>%
    pull(Ensembl_Gene_ID)


GSE10797 = makeObject("GSE10797")
GSE10797_featuredata = rowData(GSE10797) %>%
    as_tibble(rownames = 'Ensembl_Gene_ID')

GSE10797_chr16 = GSE10797_featuredata %>%
    filter(Chromosome == '16') %>%
    pull(Ensembl_Gene_ID)

GSE10797_gene_names = assay(GSE10797) %>%
    as_tibble(rownames="Ensembl_Gene_ID") %>%
    pull(Ensembl_Gene_ID)


common_genes = c()
for (gene in GSE59772_gene_names) {
    if (gene %in% GSE10797_gene_names) {
        common_genes = c(common_genes, gene)
    }
}
```

Next, we filter the expression data to include only genes on chromosome
16, then filter again to only include genes the data sets have in
common. We pivot and mutate to make the data ready for the boxplot.

``` r
GSE10797_chr16_common = assay(GSE10797) %>%
    as_tibble(rownames = 'Ensembl_Gene_ID') %>%
    filter(Ensembl_Gene_ID %in% GSE10797_chr16) %>%
    filter(Ensembl_Gene_ID %in% common_genes) %>%
    pivot_longer(cols=-Ensembl_Gene_ID,names_to='Sample_ID',values_to='Expression_Level')%>%
    mutate(Dataset = 'GSE10797')

GSE59772_chr16_common = assay(GSE59772) %>%
    as_tibble(rownames = 'Ensembl_Gene_ID') %>%
    filter(Ensembl_Gene_ID %in% GSE59772_chr16) %>%
    filter(Ensembl_Gene_ID %in% common_genes) %>%
    pivot_longer(cols=-Ensembl_Gene_ID,names_to='Sample_ID',values_to='Expression_Level')%>%
    mutate(Dataset = 'GSE59772')
```

Finally, we combine the data sets using bind_rows() and read it into a
ggplot.

``` r
combined_data = bind_rows(GSE10797_chr16_common, GSE59772_chr16_common) %>%
    ggplot(aes(x = Dataset, y = Expression_Level, fill = Dataset)) +
    geom_boxplot() +
    theme_bw() +
    labs(x = 'Dataset', y='Gene Expression Level', title = 'Gene Expression Levels in Chromosome 16') 
combined_data
```

<img src="man/figures/README-chr16_boxplot_3-1.png" width="100%" />

# Citation

Below is the citation output from using `citation('AnnotatedBCGEData')`
in R. Please run this yourself to check for any updates on how to cite
**AnnotatedBCGEData**.

``` r
print(citation('AnnotatedBCGEData'), bibtex = TRUE)
#> To cite package 'AnnotatedBCGEData' in publications use:
#> 
#>   Steadman H, Lo S (2025). _AnnotatedBCGEData: 100+ Breast Cancer Gene
#>   Expression Data sets_. R package version 0.99.0,
#>   <https://github.com/srp33/AnnotatedBCGEData>.
#> 
#> A BibTeX entry for LaTeX users is
#> 
#>   @Manual{,
#>     title = {AnnotatedBCGEData: 100+ Breast Cancer Gene Expression Data sets},
#>     author = {Heidi Steadman and Shu-Fei Lo},
#>     year = {2025},
#>     note = {R package version 0.99.0},
#>     url = {https://github.com/srp33/AnnotatedBCGEData},
#>   }
```

Please note that the `AnnotatedBCGEData` was only made possible thanks
to many other R and bioinformatics software authors, which are cited
either in the vignettes and/or the paper(s) describing this package.

# Development tools

- Continuous code testing is possible thanks to [GitHub
  actions](https://www.tidyverse.org/blog/2020/04/usethis-1-6-0/)
  through *[usethis](https://CRAN.R-project.org/package=usethis)*,
  *[remotes](https://CRAN.R-project.org/package=remotes)*, and
  *[rcmdcheck](https://CRAN.R-project.org/package=rcmdcheck)* customized
  to use [Bioconductor’s docker
  containers](https://www.bioconductor.org/help/docker/) and
  *[BiocCheck](https://bioconductor.org/packages/3.22/BiocCheck)*.
- Code coverage assessment is possible thanks to
  [codecov](https://codecov.io/gh) and
  *[covr](https://CRAN.R-project.org/package=covr)*.
- The code is styled automatically thanks to
  *[styler](https://CRAN.R-project.org/package=styler)*.
- The documentation is formatted thanks to
  *[devtools](https://CRAN.R-project.org/package=devtools)* and
  *[roxygen2](https://CRAN.R-project.org/package=roxygen2)*.

This package was developed using
*[biocthis](https://bioconductor.org/packages/3.22/biocthis)*.
