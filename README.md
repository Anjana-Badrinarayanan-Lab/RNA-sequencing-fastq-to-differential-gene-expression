# RNA sequencing Analysis -  From fastq files to differential expression analysis

## Overview of RNA sequencing
![Overview](https://github.com/NehaSontakk/RNA-sequencing-fastq-to-differential-gene-expression/blob/main/README_Addons/RNA_Sequencing.png)

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

![Overview](https://github.com/NehaSontakk/RNA-sequencing-fastq-to-differential-gene-expression/blob/main/README_Addons/Code_Running_Flowchart.png)

## From fastq to coverage files
```
#In the terminal
python RNA_Seq_Analysis_Pipeline_Paired_End.py

#or

python RNA_Seq_Analysis_Pipeline_Single_End.py
```
## From coverage to log FC files

List below specifies all places requiring user input
1. Open EdgeR Normalization 190423.ipynb in google collab
2. Upload your coverage files to the data folder
3. Specifying the names of the samples and number of files for that replicate (This is Step 6). This cell needs to be filled in with the following information: paste(rep("SAMPLENAME",NUMBER_OF_COVERAGE_FILES),seq(1,NUMBER_OF_COVERAGE_FILES),sep = "_"). _For example: colnames(GenewiseCounts) <- c(paste(rep("lexASidA",2),seq(1,2),sep = "_"),paste(rep("WT_0",4),seq(1,4),sep = "_"))_
4. List of files with the replicates named as specified (This is Step 7). Just like above this needs a specification of individual samples: rep("SAMPLENAME",NUMBER_OF_COVERAGE_FILES). For example: _group<- c(rep("lexASidA",2),rep("WT_0",4))_
5. Comparative groups have to be specified below. The prefix “group” has to be present, the sample names have to be given as specified in step 6 and 7 above. "groupSampleName-groupSampletobeNormalisedto". For example: _comparisons<-c("grouplexASidA-groupWT_0")_


** Replace gff and fna files based on organism of interest from the NCBI databases (Also replace the names inside the code in that case).
