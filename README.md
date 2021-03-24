# recount_importer

This script imports recount data and transforms it into a manageable format to be uploaded to NeMO Analytics.

This script is currently in a 2-script development phase in which libraries and files must be installed and downloaded from R, to which the user can then run the Python script with the locally installed files to obtain the items to upload.

In this repository, you will find directions on how to install these libraries, obtain the files and run the Python script. A requirements file (```requirements.txt```) is also provided above. All of the necessary files needed to run the script are also provided above.

# To Run Script in cmd Line

```python3 recount_editor.py [Recount_dataset_name]```

# Files Created
```
expression.tab
genes.tab
observations.tab
metadata.xlsx
[dataset tag]_processed.tar.gz
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

# Recount R commands

##### Creating Conda Env and Installing Recount
```
>>> conda create --name <env> -c bioconda -c r --file requirements.txt
```

```
>>> R
>>> if (!requireNamespace("BiocManager", quietly = TRUE))
...   install.packages("BiocManager")
>>> BiocManager::install("recount")
```

##### Get Project and Download Data to Files
```
>>> project_info <- abstract_search("[GEO name]")
>>> download_study(project_info$project)
>>> load(file.path(project_info$project, "rse_gene.Rdata"))
>>> rse <- scale_counts(rse_gene)
>>> write.table(assays(rse)$counts, file="[expression_file_name].tsv", quote=F, sep="\t")
>>> write.table(colData(rse_gene), file="[col_metadata_file_name].tsv", quote=F, sep="\t")
```

##### Getting Project Title and Abstract
```
>>> project_info$project
>>> project_info$abstract
>>> sink("[file_name].txt")
```

# After Downloading Files
After the files have been downloaded, you can directly run the script with the Python command shown above. Make sure the files are saved in the same location as the script.
