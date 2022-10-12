#!/usr/bin/env python3

#load modules
import argparse
import pandas as pd
from datetime import date

def read_sequences(args):

    #get the number of lines in the multi fasta file   	
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

    # add columns to required location (must be "strain date country")
    df.insert(1, "date", dates)
    df.insert(2, "country", country)

    return df



def main(args):

    # get the list of sample IDs from multi fasta file
    sample_ID = read_sequences(args)

    # import metadata
    df = pd.read_csv(args.input, sep='\t')

    # rename sample to strain to match pipeline requirements
    # save date as sample data
    df.rename(columns = {"sample": "strain", "date": "sample_date"}, inplace =True)

    # if there are differences from the metadata file and the sequence files, use the sample_ID 
    # in place of the metadata file    
    if len(sample_ID) != len(df):
        df = pd.DataFrame(sample_ID, columns = ["strain"])

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
