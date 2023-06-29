###Paired End RNA seq pipeline
import os
from sys import exit
import pandas as pd
#Running the paired end RNA seq pipeline
def run_get_coverage_files(file1,file2,filelocation):
	file1_name = filelocation+file1.split(".fastq.gz")[0]
	file2_name = filelocation+file2.split(".fastq.gz")[0]
	final_filename = file1_name.split("_R")[0]+"_R1_R2_"+file1_name.split("_")[-1]
	print("File1: ",file1_name,"File2:",file2_name,"Final_filename:",final_filename)

	#Unzipping both read files
	os.system('gunzip '+file1_name+".fastq.gz")
	os.system('gunzip '+file2_name+".fastq.gz")
	#Prepare reference index
	os.system('bwa index -a is GCF_000022005.1_ASM2200v1_genomic.fna')
	#
	os.system('python gff2bed.py GCF_000022005.1_ASM2200v1_genomic.gff GCF_000022005.1_ASM2200v1_genomic.bed')
	#Align both paired end reads to reference
	os.system('bwa aln -q 20 GCF_000022005.1_ASM2200v1_genomic.fna '+file1_name+'.fastq > '+file1_name+'.sai')
	os.system('bwa aln -q 20 GCF_000022005.1_ASM2200v1_genomic.fna '+file2_name+'.fastq > '+file2_name+'.sai')
	os.system('bwa sampe GCF_000022005.1_ASM2200v1_genomic.fna '+file1_name+'.sai '+file2_name+'.sai '+file1_name+'.fastq '+file2_name+'.fastq > '+final_filename+'.sam')
        print("SAM file made.")	
	#Re zip the fastq files
	os.system('gzip '+file1_name+'.fastq')
	os.system('gzip '+file2_name+'.fastq')
	#Conversion of sam to bam
	os.system('samtools view -q0 -Sb '+final_filename+'.sam > '+final_filename+'.bam')
	print("BAM file made.")
	#Sorting the .bam file
	os.system('samtools sort '+final_filename+'.bam -o '+final_filename+'.sorted.bam')
	print("BAM file sorted.")
	#Indexing sorted bam files
	os.system('samtools index '+final_filename+'.sorted.bam')
	print("BAM file indexed.")
	#Displaying statistics of the mapped reads
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
for filename in os.listdir("/media/neha/My Passport/Input_Output_Storage_Folder/"):
	if filename.endswith(".fastq.gz"):
	    # Split the filename into components based on underscores
	    parts = filename.split("_")

	    # Extract the stem (all parts except the last two)
	    stem = "_".join(parts[:-2])

	    # Add the file to the corresponding group in the dictionary
	    if stem in file_groups:
		file_groups[stem].append(filename)
	    else:
		file_groups[stem] = [filename]

# Loop through each group in the dictionary and print any pairs of files that share a stem
for stem in file_groups:
    if len(file_groups[stem]) == 2:
        print(file_groups[stem][0], file_groups[stem][1])
        run_get_coverage_files(file_groups[stem][0],file_groups[stem][1],"/media/neha/My\ Passport/Input_Output_Storage_Folder/")
