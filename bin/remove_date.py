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
			



		# remove date column
		try:
			df_temp.drop("date", axis = 1, inplace = True)
	
		except:
			print("file doesnt have date column")


		# remove earliest_date column
		try:

			df_temp.drop("earliest_date", axis = 1, inplace = True)

		except:
			print("file doesn't have earliest date column")


		# remove latest_date column
		try: 

			df_temp.drop("latest_date", axis = 1, inplace = True)

		except:
			print("file doesn't have latest date column")


		# replace ncov-recombinant version with proper version output

		try:
			df_temp['ncov-recombinant_version'] = args.version

		except:
			print("file doesn't have ncov-recombinant_version column")

		# overwrite csv file with date columns removed and version replaced if applicable
		df_temp.to_csv(file, sep = "\t", index = False)



	nextclade_files = glob.glob('nextclade*/metadata.tsv', recursive = True)

	for file in nextclade_files:
		try:
			df_temp = pd.read_csv(file, sep = "\t")
			df_temp.drop("date", axis = 1, inplace = True)
			df_temp.drop("sample_date", axis = 1, inplace = True)
			df_temp.to_csv(file, sep = "\t", index = False)
		except:
			print("ignore")






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help="ncov-recombinant version")
    args = parser.parse_args()
    main(args)

