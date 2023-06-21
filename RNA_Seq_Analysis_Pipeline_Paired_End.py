#READ the comments!!!

###Paired End RNA seq pipeline : Will take approx. 20 minutes to run
#Please do not change the names of fastq files from the names given by the sequencing facility
#Please store input fastq files in Input_Output_Storage_Folder
#Find the output in the same folder

#Written by Neha Sontakke (April 2023)
#Import required libraries and dependencies
#If not installed then install using the following commans in Ubuntu

import os
from sys import exit


#Function to run the paired end RNA seq pipeline
def run_get_coverage_files(file1,file2,filelocation):
	#file1 = first fastq file from paired end run (given by sequencing facility)
	file1_name = filelocation+file1.split(".fastq.gz")[0]
	#file2 = second fastq file from paired end run (given by sequencing facility)
	file2_name = filelocation+file2.split(".fastq.gz")[0]
	#variable to store the name of the final file 
	final_filename = file1_name.split("_R")[0]+"_R1_R2_"+file1_name.split("_")[-1]
	#verify file names and final file name is correct
	print("File1: ",file1_name,"File2:",file2_name,"Final_filename:",final_filename)

	#Unzipping both sequencing fastq files
	os.system('gunzip '+file1_name+".fastq.gz")
	os.system('gunzip '+file2_name+".fastq.gz")

	#Prepare reference index for Caulobacter crescentus from NCBI latest as of (January 2023)
	#This file for caulobacter is to be stored in the same folder as this script
	#BWA has to be installed in Ubuntu (use the command line, google if you don't know.
	#If not installed use sudo apt-get install bwa
	os.system('bwa index -a is GCF_000022005.1_ASM2200v1_genomic.fna')

	#Conversion of gff file containing features of Caulobacter crescentus genome to bed file (useful for the computer)
	#gff files from NCBI to be stored in the same folder as this script
	#GFF2BED is a custom python script designed by Nitish Malhotra from ASN lab
	#GFF2BED to be stored in the same folder as this file.
	os.system('python gff2bed.py GCF_000022005.1_ASM2200v1_genomic.gff GCF_000022005.1_ASM2200v1_genomic.bed')

	#Align both paired end reads to reference
	#Please check sai file after it is made
	os.system('bwa aln -q 20 GCF_000022005.1_ASM2200v1_genomic.fna '+file1_name+'.fastq > '+file1_name+'.sai')
	os.system('bwa aln -q 20 GCF_000022005.1_ASM2200v1_genomic.fna '+file2_name+'.fastq > '+file2_name+'.sai')

	#Create SAM file combining alignments of both fastq files (from paired end sequencing run)
	#Using BWA sampe command (sampe is for paired end)
	os.system('bwa sampe GCF_000022005.1_ASM2200v1_genomic.fna '+file1_name+'.sai '+file2_name+'.sai '+file1_name+'.fastq '+file2_name+'.fastq > '+final_filename+'.sam')
      	print("SAM file made.")	

	#Re zip the fastq files to save space on the disk, this step might take some time.
	os.system('gzip '+file1_name+'.fastq')
	os.system('gzip '+file2_name+'.fastq')

	#Conversion of sam to bam
	#Install using: sudo apt-get install samtools
	os.system('samtools view -q 0 -Sb '+final_filename+'.sam > '+final_filename+'.bam')
	print("BAM file made.")

	#Sorting the .bam file
	os.system('samtools sort '+final_filename+'.bam -o '+final_filename+'.sorted.bam')
	print("BAM file sorted.")

	#Indexing sorted bam files
	os.system('samtools index '+final_filename+'.sorted.bam')
	print("BAM file indexed.")

	#Displaying statistics of the mapped reads
	#Please check statistics later
	os.system('samtools flagstat '+final_filename+'.sorted.bam > '+final_filename+'.flagstat')
        os.system('head '+final_filename+'.flagstat')

	#delete SAM file
	os.system('rm '+final_filename+'.sam')

	#Converting Bam to Bed file for cov
	os.system('bedtools bamtobed -i '+final_filename+'.sorted.bam > '+final_filename+'.bed')

	#Generating gene coverage files
	os.system('bedtools coverage -a GCF_000022005.1_ASM2200v1_genomic.bed -b '+final_filename+'.bed > '+final_filename+'.cov')

	#sample_coverage_table = pd.read_table(str(final_filename+".cov"),sep="\t",header=None, names=['NC_ID','Gene Start','Gene End','Gene ID','Gene Name','Strand','Reads Mapped','Gene length covered by reads','Gene Length','Coverage'])
   	#sns.kdeplot(data=sample_coverage_table['Coverage'])
	#sample_coverage_table.to_csv(final_filename+"_coverage.csv")

# Create an empty dictionary to store file groups
file_groups = {}

# Loop through each file in the directory
for filename in os.listdir("/Input_Output_Storage_Folder/"):
    # Split the filename into components based on underscores
    parts = filename.split("_")

    # Extract the stem (all parts except the last two)
    stem = "_".join(parts[:-2])

    # Add the file to the corresponding group in the dictionary
    if stem in file_groups:
        file_groups[stem].append(filename)
    else:
        file_groups[stem] = [filename]

# Loop through each group in the dictionary and print any pairs of files that shares a name
for stem in file_groups:
    if len(file_groups[stem]) == 2:
	  #get names for file one and file 2
        print(file_groups[stem][0], file_groups[stem][1])
	  #run function on all files in the storage folder
        run_get_coverage_files(file_groups[stem][0],file_groups[stem][1],"/Input_Output_Storage_Folder/")
