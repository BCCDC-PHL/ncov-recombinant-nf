#!/usr/bin/env python3

#load modules
import pandas as pd
from datetime import date


# import metadata
df = pd.read_csv("metadata_original.tsv", sep='\t')


# rename sample to strain to match pipeline requirements
# save date as sample data
df.rename(columns = {"sample": "strain", "date": "sample_date"}, inplace =True)



# create date and country headers required by pipeline
date_str = date.today().isoformat()

date = [date_str] * len(df)

country = ["Canada"] * len(df)

# add columns to required location (must be "strain date country")
df.insert(1, "date", date)
df.insert(2, "country", country)

# save metadata 
df.to_csv("metadata.tsv", sep="\t")
