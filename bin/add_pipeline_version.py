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





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help="ncov-recombinant version")
    args = parser.parse_args()
    main(args)

