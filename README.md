# recount_importer

This script imports recount data and transforms it into a manageable format to be uploaded to NeMO Analytics.

This script also runs an R script with pre-written commands. Simply download all the files from this repository to run the script properly.

In this repository, you will find a requirements file (```requirements.txt```) provided above. All of the necessary files needed to run the script are also provided above.

# To Run Script in cmd Line

```python3 recount_editor.py [Recount_dataset_name]```

# Files Created
```
expression.tab
genes.tab
observations.tab
metadata.xlsx
[accession_name]_abstract.txt
[accession_name]_expression.tsv
[accession_name]_col_metadata.tsv
[accession_name]_processed.tar.gz
```

# Requirements

##### Language Requirements
```
python > 3
R >= 3.6
```

##### Installations
```
R-Hmisc
```

##### Requirements without Version Specifiers
```
tarfile
csv
sys
```

##### Requirements with Version Specifiers
```
openpyxl >= 3.0.5
```

##### Required Files
```
human_ensembl.txt           # human conversion table
metadata.xlsx               # metadata template
```
