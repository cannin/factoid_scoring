library(magrittr)
library(xml2)

#download.file('https://raw.githubusercontent.com/jvwong/filterGene2Pubmed/master/article_hit_enrichment/all_pmids.txt', destfile = 'jwong_data/all_pmids.txt')
#download.file('https://raw.githubusercontent.com/jvwong/filterGene2Pubmed/master/article_hit_enrichment/hits_pmids.txt', destfile = 'jwong_data/hit_pmids.txt')

pmids <- readLines("jwong_data/all_pmids.txt")

stop_flag <- TRUE
file_dir <- 'cache'

if(!dir.exists(file_dir)) {
  dir.create(file_dir)
}

while(stop_flag) {
  for(i in 1:length(pmids)) {
    #i <- 1
    cat("I: ", i, "\n")
    
    id <- pmids[i]
    url <- paste0('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=', id)
    
    filename <- paste0(file_dir, '/pmid', id, '.xml')
    
    if(file.exists(filename)) {
      next
    } else {
      try(download.file(url, filename))
    }
    
    Sys.sleep(0.5)
    
    if(i == length(pmids)) {
      stop_flag <- FALSE
    }
  }
}

# MAKE DF ----
results_filename <- 'jwong_data/all_pmids_abstracts.csv'

files <- dir(file_dir, pattern = '.xml', full.names = TRUE)

if(file.exists(results_filename)) {
  results <- read.csv(results_filename)  
} else {
  results <- data.frame(
    pmid=character(0),
    abstract=numeric(0),
    stringsAsFactors = FALSE)
}

for(i in 1:length(files)) {
#for(i in 1:10) {
  #doc <- read_xml('efetch.xml')
  #i <- 2
  cat("I: ", i, "\n")
  
  file <- files[i]
  doc <- read_xml(file)
  
  # Initialize 
  pmid <- NA
  abstract <- NA
  
  # Set variables
  pmid <- xml_find_first(doc, './/PMID') %>% xml_text
  abstract <- xml_find_first(doc, './/AbstractText') %>% xml_text
  
  if(pmid %in% results$pmid) {
    stop("ERROR: Duplicate")
  }
    
  tmp_df <- data.frame(
    pmid=pmid,
    abstract=abstract,
    stringsAsFactors = FALSE)
  
  results <- rbind(results, tmp_df)
  
  # Save results
  write.csv(results, results_filename, row.names = FALSE)
}

# tmp <- results[results$abstract != "", ]

