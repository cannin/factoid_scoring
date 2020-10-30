# Installation 

## Download PubMed Data (in R)

* Necessary libraries are listed at the top of download_pubmed_abstracts.R

## Extract Interactions with REACH (in Python)

Use pipenv: https://github.com/pypa/pipenv with dependencies listed in Pipfile 

### Java installation 

The code runs REACH (https://github.com/clulab) locally. 

1. Install using the instructions here: https://indra.readthedocs.io/en/latest/modules/sources/reach/index.html (labeled: INDRA using a REACH JAR through a Python-Java bridge )
2. Change path: reach_jar_path = "CHANGE_ME/reach/target/scala-2.11/reach-1.6.0-FAT.jar" in score_request_indra_sm.py

## Compare Article Suitability to Curated Data (in R)

* Necessary libraries are listed at the top of make_performance_roc_curves.R

# Run

## Download PubMed Data (in R)

Downloads content for PMIDs in 'jwong_data/all_pmids.txt' (see code for source of file)

```
source('download_pubmed_abstracts.R')
```

### Output

Output is found in 'jwong_data/all_pmids_abstracts.csv'

## Extract Interactions with REACH (in Python)

Extracts interaction information for abstract data from previous step

```
python score_request_indra_sm.py
```

### Output

Output is found in 'jwong_data/all_pmids_abstracts_scores_mod_types.csv'

## Compare Article Suitability to Curated Data (in R)

Plots various performance charts in R using data from 'jwong_data/all_pmids_abstracts_scores_mod_types.csv'

```
source('make_performance_roc_curves.R')
```

### Output

No output is saved. Plots are shown in R. 








