#!/usr/bin/env python3

#load modules
import pandas as pd
import glob

# drop date from linelist
linelist_files = glob.glob('linelists/*.tsv', recursive = True)



for file in linelist_files:
	try:
		df_temp = pd.read_csv(file, sep = "\t")
		df_temp.drop("date", axis = 1, inplace = True)
		df_temp.to_csv(file, sep = "\t", index = False)
	
	except:
		print("ignore")


nextclade_files = glob.glob('nextclade*/metadata.tsv', recursive = True)

for file in nextclade_files:
	try:
		df_temp = pd.read_csv(file, sep = "\t")
		df_temp.drop("date", axis = 1, inplace = True)
		df_temp.drop("sample_date", axis = 1, inplace = True)
		df_temp.to_csv(file, sep = "\t", index = False)
	except:
		print("ignore")
