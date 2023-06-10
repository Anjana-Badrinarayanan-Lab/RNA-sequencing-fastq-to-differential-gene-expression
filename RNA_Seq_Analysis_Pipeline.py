#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#os.run_line_magic('pip', 'install --user pandas')
#os.run_line_magic('pip', 'install --user seaborn')
#!sudo apt-get install fastqc 
#!sudo apt-get install bwa 
#!sudo apt-get install samtools 
#!sudo apt-get install bedtools


#Run once
#!bwa index -a is c_crescentus.fna
#!python gff2bed.py c_crescentus.gff c_crescentus.bed

import pandas as pd
import seaborn as sns

import os

def run_fastqc_analysis(filename,filelocation):
  input_file = filelocation+filename
  output_directory = filelocation
  os.system('fastqc {input_file} -o {filelocation}')
  print("FastQC finished.")

#run_fastqc_analysis("WT_20mins_MMS_Replicate1.fastq.gz","/content/drive/MyDrive/RNA_Seq_Analysis/MMS_WT/")



def run_alignment(filename,filelocation):
    os.system('gunzip '+filelocation+filename)
    print("File unzipped.")
    #all files will be saved in the following locations with the following names
    file_name_loc = str(filelocation+filename).split(".fastq.gz")[0]
    print(file_name_loc)
    #start the process
    os.system('bwa index -a is GCF_000022005.1_ASM2200v1_genomic.fna')
    print("hi")
    os.system('python gff2bed.py GCF_000022005.1_ASM2200v1_genomic.gff GCF_000022005.1_ASM2200v1_genomic.bed')
    os.system('bwa aln -q 20 GCF_000022005.1_ASM2200v1_genomic.fna '+file_name_loc+'.fastq > '+file_name_loc+'.sai')
    os.system('head '+file_name_loc+'.sai')
    os.system('bwa samse GCF_000022005.1_ASM2200v1_genomic.fna '+file_name_loc+'.sai '+file_name_loc+'.fastq > '+file_name_loc+'.sam')
    os.system('head '+file_name_loc+'.sam')
    os.system('samtools view -q0 -Sb '+file_name_loc+'.sam > '+file_name_loc+'.bam')
    os.system('head '+file_name_loc+'.bam')
    os.system('samtools sort '+file_name_loc+'.bam -o '+file_name_loc+'.sorted.bam')
    os.system('head '+file_name_loc+'.sorted.bam')
    os.system('gzip '+file_name_loc+'.fastq')
    os.system('samtools index '+file_name_loc+'.sorted.bam')
    os.system('head '+file_name_loc+'.sorted.bam')
    os.system('samtools flagstat '+file_name_loc+'.sorted.bam > '+file_name_loc+'.flagstat')
    os.system('head '+file_name_loc+'.flagstat')
    os.system('bedtools bamtobed -i '+file_name_loc+'.sorted.bam > '+file_name_loc+'.bed')
    os.system('head '+file_name_loc+'.bed')
    os.system('bedtools coverage -a GCF_000022005.1_ASM2200v1_genomic.bed -b '+file_name_loc+'.bed > '+file_name_loc+'.cov')
    os.system('head '+file_name_loc+'.cov')

import glob

files_for_loop_running = []
for i in os.listdir("/media/neha/My Passport/RNA_seq_Asha_070423/"):
#for i in glob.glob("/media/neha/My\ Passport/RNA_seq_Asha_070423/*.fastq.gz"):
    filename = i.split("/")[-1]
    files_for_loop_running.append(i)
    
for i in files_for_loop_running:
    	run_alignment(filename,'/media/neha/My\ Passport/RNA_seq_Asha_070423/')





