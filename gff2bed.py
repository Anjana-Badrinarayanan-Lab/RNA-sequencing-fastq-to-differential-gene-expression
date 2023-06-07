import sys

if not len(sys.argv) == 3:
    print("Usage instruction: python gff2bed.py <gff_file> <output_file_name>")
    exit()    

gff_file = sys.argv[1]
out_file = sys.argv[2]

with open(gff_file) as f:
    lines = f.readlines()
    lines = [l.split("\t") for l in lines if not l.startswith('#')]
    lines = [l for l in lines if len(l) >= 8]
    lines = [l for l in lines if l[2].lower() == "gene"]
    nc_id = [l[0] for l in lines]
    feature_start = [l[3] for l in lines]
    feature_stop = [l[4] for l in lines]
    feature_strand = [l[6] for l in lines]
    feature_name = [[a.split("=")[1] for a in l[-1].split(";") if a.startswith("Name=")][0].rstrip() for l in lines]
    #feature_name = [l.split("=")[1] for l in lines if l.startswith("gene")]
    locus_tag = [[a.split("=")[1] for a in l[-1].split(";") if a.startswith("locus_tag=")][0].rstrip() for l in lines]    

with open(out_file,"w") as out:
    for i in range(len(feature_start)):
        feature_info = "\t".join([nc_id[i],feature_start[i],feature_stop[i],feature_name[i],locus_tag[i],feature_strand[i]])
        out.write("%s\n"%feature_info)
        

