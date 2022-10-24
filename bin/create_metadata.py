#!/usr/bin/env python3

#load modules
import argparse
import pandas as pd
from datetime import date
import numpy as np

def read_sequences(args):

    # get the number of lines in the multi fasta file   	
    with open(args.seqs, 'r') as f:
        number_of_lines = len(open(args.seqs).readlines())
    


    # make empty list to add sequence sample ID's
    sample_ID = []
    with open(args.seqs, 'r') as f:

    # read each line and append the sample ID's to the sample_ID list
        for i in range(0,number_of_lines):
        
            a = f.readline()
        
            if '>' in a:
                sample_ID.append( a.strip('\n').strip('>'))

    return sample_ID



def add_date_and_country(df):

    # create date and country headers required by pipeline
    date_str = date.today().isoformat()

    dates= [date_str] * len(df)
    
    country = ["Canada"] * len(df)

    # if sample date is available, use as the date
    # otherwise analysis date is used as the date

    for i in range(0, len(dates)):
        if pd.isna(df["sample_date"][i])  != True:
            dates[i] = df["sample_date"][i]
	
    # add columns to required location (must be "strain date country")
    df.insert(1, "date", dates)
    df.insert(2, "country", country)

    return df



def fix_metadata(sample_ID, df):
    
    # create new dataframe using sample IDs from multi fasta as strain
    df2 = pd.DataFrame(sample_ID, columns = ["strain"])

    # create columns for sample_date and ct values with NA place holders
    sample_date = ["NA"] * len(df2)
    ct_value = ["NA"] * len(df2)
    
    # add columns to dataframe
    df2.insert(1, "ct", ct_value)
    df2.insert(2, "sample_date", sample_date)

    # fill in "nan" values with "NA" string 
    # (without this the metadata_out.tsv doesn't print NA, just a blank number)
    df = df.replace(np.nan, "NA", regex=True)
    
    # create dictionary from the original metadata.tsv file
    # using the sample as the key and the date and ct as the values
    dictionary = df.set_index('strain').T.to_dict('list')

   
    # for every row in the new dataframe
    for row in range(0,len(df2)):
        
        # if the row in df2 matches a key in the dictionary
        if df2["strain"][row] in  dictionary:
            
            # replace the NA value with the dictionary value
            df2["ct"][row] = dictionary[df["strain"][row]][0]
            df2["sample_date"][row] = dictionary[df["strain"][row]][1]
    

    
    return df2

def main(args):

    # get the list of sample IDs from multi fasta file
    sample_ID = read_sequences(args)

    # import metadata
    df = pd.read_csv(args.input, sep='\t')

    # rename sample to strain to match pipeline requirements
    # save date as sample data
    df.rename(columns = {"sample": "strain", "date": "sample_date"}, inplace =True)

    # if there are differences in the number of samples from the metadata file and the sequence files, 
    # use the sample_ID as the strain and fill in sample_date and ct from metadata if available    
    if len(sample_ID) != len(df):
        df = fix_metadata(sample_ID, df)

    # add date and country headers required by pipeline
    df = add_date_and_country(df)

    # save metadata to use in pipeline
    df.to_csv(args.output, sep="\t", index = False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input data")
    parser.add_argument('-o', '--output', help="Output file")
    parser.add_argument('-s', '--seqs', help="Sequences fasta file")
    args = parser.parse_args()
    main(args)
