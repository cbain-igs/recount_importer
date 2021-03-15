import csv
import tarfile
import gzip
import urllib.request
import openpyxl
import json
import os
import sys

dataset_name = sys.argv[1]

exp_file = open("test_expr.tsv")
read_tsv1 = csv.reader(exp_file, delimiter="\t")
colmetadata_file = open("test_colmetadata.tsv")
read_tsv2 = csv.reader(colmetadata_file, delimiter="\t")
metadata_file_path = 'metadata.xlsx'
sheet_name = 'metadata'

new_exp_file = "expression.tab"
gene_file = "genes.tab"
new_colmetadata_file = "observations.tab"
out_tar = "recount_processed.tar.gz"

human_conv_file = "human_ensembl.txt"

unconverted_count = 0
duplicate_count = 0

# creating conversion dicts
with open(human_conv_file, 'rt') as htable:
    human_conv_dict = {}
    for line in htable:
        if line.startswith("e"):  # removes first line
            continue
        split_line = line.rstrip().split()
        if len(split_line) == 2:  # removes lines with no gene symbol
            continue
        (key, val1, val2) = (split_line[0], split_line[1], split_line[2])  # creates dictionary entry
        human_conv_dict[key] = val1, val2  # creates dictionary

# opening files to write to
with open(new_exp_file, 'w') as exp, open(gene_file, 'w') as gene, open(new_colmetadata_file, 'w') as col:
    gene.write("gene\tgene_symbol\n")
    conversion_dict = human_conv_dict
    converted_genes = {}  # list of converted genes to prevent duplicates
    col_data = {}
    mean = 0

    for row in read_tsv1:
        if row[0].startswith("S"):  # adding "Gene" in front of experiment names (not included previously)
            row.insert(0, "Gene")
            exp.write('\t'.join(row))
            exp.write('\n')

        elif row[0].startswith("E"):
            period_idx = 0  # index of the period in the ensembl string
            for i in row[0]:
                if i == '.':
                    phrase = row[0][period_idx:]
                    replace = row[0].replace(phrase, '')
                    row[0] = replace  # deletes all characters after period in name
                period_idx += 1
            #exp.write('\t'.join(row))
            #exp.write('\n')

            name = row[0]
            if row[0] in conversion_dict:  # searches for name in conversion dict
                for i in row[1:]:
                    i = float(i)
                    mean += i
                mean /= (len(row) - 1)
                mean = abs(mean)

                if conversion_dict[name][0] not in converted_genes:  # if gene name is not in file
                    converted_genes[conversion_dict[name][0]] = mean, row
                else:
                    duplicate_count += 1
                    if mean >= converted_genes[conversion_dict[name][0]][0]:
                        converted_genes[conversion_dict[name][0]] = mean, row
            else:
                unconverted_count += 1
    with open("hmm.txt", "w") as hmm:
        for i in converted_genes:
            hmm.write("{}\t{}\n".format(i,converted_genes[i]))

    for i in converted_genes:
        out_line = '\t'.join(converted_genes[i][1])
        exp.write(out_line)
        exp.write('\n')

        gene_contents = (converted_genes[i][1][0], i)
        out_line2 = '\t'.join(gene_contents)
        gene.write(out_line2)
        gene.write('\n')

    for row in read_tsv2:
        if row[0] != 'project':
            idx = 0
            replace = row[-1].strip('c()')
            replace = replace.split('\",')
            for i in replace:
                replace[idx] = i.replace('\"', '').strip(' ')
                idx += 1
            row[-1] = replace
            col_data[row[0]] = row[-1]

    metadata_length = len(list(col_data.values())[0]) + 1
    col.write('observations')
    for i in range(1, metadata_length):
        col.write('\tV{}'.format(str(i)))
    col.write('\n')
    for i in col_data:
        out_list = [i, '\t'.join(col_data[i])]
        out_line = '\t'.join(out_list)
        col.write(out_line)
        col.write('\n')

# with tarfile.open(out_tar, "w:gz") as tar:
#     for name in [exp_file, gene_file]:
#         tar.add(name)

with open("test.txt", "r") as abstract_file:
    abstract_text = abstract_file.readline().strip().replace('"', '').lstrip("[1] ")

# editing metadata
wb = openpyxl.load_workbook(metadata_file_path)
ws = wb[sheet_name]

title = ws.cell(2, 2)
summary = ws.cell(3, 2)
dataset_type = ws.cell(4, 2)
geo_accession = ws.cell(7, 2)
contact_email = ws.cell(8, 2)
contact_institute = ws.cell(9, 2)
contact_name = ws.cell(10, 2)

dataset_type.value = "bulk-rnaseq"
title.value = dataset_name
summary.value = abstract_text
geo_accession.value = dataset_name
contact_email.value = "sament@som.umaryland.edu"
contact_institute.value = "University of Maryland Institute for Genome Sciences"
contact_name.value = "Seth Ament"

wb.save(metadata_file_path)

htable.close()
exp.close()
gene.close()

with tarfile.open(out_tar, "w:gz") as tar:
    for name in [new_exp_file, gene_file, new_colmetadata_file]:
        tar.add(name)

print(unconverted_count, "genes unconverted")
print(duplicate_count, "duplicates found")