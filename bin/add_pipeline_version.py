#!/usr/bin/env python3

#load modules
import pandas as pd
import glob
import argparse

def main(args):

	# drop date from linelist
	linelist_files = glob.glob('linelists/*.tsv', recursive = True)



	for file in linelist_files:
	
		df_temp = pd.read_csv(file, sep = "\t")
			

		# replace ncov-recombinant version with proper version output

		try:
			df_temp['ncov-recombinant_version'] = args.version

		except:
			print("file doesn't have ncov-recombinant_version column")

		# overwrite csv file with date columns removed and version replaced if applicable
		df_temp.to_csv(file, sep = "\t", index = False)


	# create a subset of only the columns required for QC Summary file
	linelist_tsv_file = 'linelists/linelist.tsv'


	# read in linelist.tsv file
	linelist = pd.read_csv(linelist_tsv_file, sep = "\t")
	
	# rename column names 
	linelist.rename(columns = {'status':'recombinant_status', 'lineage':'recombinant_lineage', 'parents_clade':'recombinant_parents_clade', 'ncov-recombinant_version':'ncov_recombinant_version'}, inplace = True)

	
	# subset only required columns
	linelist_subset = linelist[['strain', 'recombinant_status','recombinant_lineage','recombinant_parents_clade','ncov_recombinant_version']]

	
	linelist_subset.to_csv("linelist/linelist_qc_summary_subset.csv")





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help="ncov-recombinant version")
    args = parser.parse_args()
    main(args)

