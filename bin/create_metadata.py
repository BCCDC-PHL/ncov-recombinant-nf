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



def add_country(df, args):

   
    # create country header required by pipeline
 
    country = ["Canada"] * len(df)

    # add columns to required location (must be "strain date country")
    #df.insert(1, "date", dates)
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
    df2.insert(2, "date", sample_date)

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
            df2["date"][row] = dictionary[df["strain"][row]][1]
    

    
    return df2



def create_metadata(sample_ID):

    # create new dataframe using sample IDs from multi fasta as strain
    df = pd.DataFrame(sample_ID, columns = ["strain"])

    # create column for sample_date with NA place holder
    sample_date = ["NA"] * len(df)
   
    # add column to dataframe
    df.insert(1, "date", sample_date)

    return df


def main(args):

    # get the list of sample IDs from multi fasta file
    sample_ID = read_sequences(args)

    # check if metadata.tsv file exists
    if args.input == "NO_FILE":
        
        # create a metadata file if no file given
        df = create_metadata(sample_ID)

    else:
    # otherswise import metadata
        df = pd.read_csv(args.input, sep='\t')

        # rename sample to strain to match pipeline requirements
        # save date as sample data
        df.rename(columns = {"sample": "strain"}, inplace =True)

   
       
        # use the sample_ID from the sequences.fasta as the strain to ensure the names match 
        # and fill in sample_date and ct from metadata if available    
        df = fix_metadata(sample_ID, df)

        # reorder date frame

        df = df[['strain', 'date', 'ct']]


    # add country headers required by pipeline
    df = add_country(df, args)

    # save metadata to use in pipeline
    df.to_csv(args.output, sep="\t", index = False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input data")
    parser.add_argument('-o', '--output', help="Output file")
    parser.add_argument('-s', '--seqs', help="Sequences fasta file")
    parser.add_argument('-r', '--run', help="run id")
    args = parser.parse_args()
    main(args)
