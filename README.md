# RNA sequencing Analysis -  From fastq files to differential expression analysis

## Overview of RNA sequencing

## Installations and dependencies
```
# For part A - fastq to coverage
sudo apt-get install fastqc
sudo apt-get install bwa
sudo apt-get install samtools 
sudo apt-get install bedtools

#Requirements for part B - coverage files to differential gene expression will be installed in google collab
```
## Folder contents

| File/Folder Name                        | Description                                                                                                                                                                    | Usage                                                                                                                 | Source                      |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| GCF_000022005.1_ASM2200v1_genomic.fna   | A file with the FNA file extension is a FASTA Format DNA and Protein Sequence Alignment file that stores DNA information that can be used by molecular biology software.       | A reference for alignment of the sequences from fastq files                                                           | NCBI Database               |
| GCF_000022005.1_ASM2200v1_genomic.gff   | The general feature format (gene-finding format, generic feature format, GFF) is a file format used for describing genes and other features of DNA, RNA and protein sequences. | A reference for features associated with every protein coding gene - start/stops and annotations used on the fna file | NCBI Database               |
| Input_Output_Storage_Folder             | Folder to store fastq files from sequencing runs                                                                                                                               | Storage folder for all files in analysis                                                                              |                             |
| gff2bed.py                              | Code to convert gff to bed file formats.                                                                                                                                       | First step converts the gff to a readable format to generate 5 additional files in the same folder                    | Written by Nitish Malhotra. |
| RNA_Seq_Analysis_Pipeline_Paired_End.py | Code to run all the RNA sequencing steps on the fastq files for paired end sequencing                                                                                                                   | Python containing code for fastq to coverage file generation                                                                    | Written by Neha Sontakke.   |
| RNA_Seq_Analysis_Pipeline_Single_End.py | Code to run all the RNA sequencing steps on the fastq files for single ended sequencing                                                                                                                   | Python containing code for fastq to coverage file generation                                                                    | Written by Neha Sontakke.   |
|EdgeR Normalization 190423.ipynb | Code for DGE analysis and Log Fold Change Outputs | R  code for coverage to logFC generation  | Written by Neha Sontakke.   |

## File usage flowchart

## From fastq to coverage files
```
#In the terminal
python RNA_Seq_Analysis_Pipeline_Paired_End.py

#or

python RNA_Seq_Analysis_Pipeline_Single_End.py
```
