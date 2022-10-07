#!/usr/bin/env python3

#load modules
import argparse
import pandas as pd
from datetime import date


def main(args):

    # import metadata
    df = pd.read_csv(args.input, sep='\t')

    # rename sample to strain to match pipeline requirements
    # save date as sample data
    df.rename(columns = {"sample": "strain", "date": "sample_date"}, inplace =True)



    # create date and country headers required by pipeline
    date_str = date.today().isoformat()
    
    dates= [date_str] * len(df)

    country = ["Canada"] * len(df)

    # add columns to required location (must be "strain date country")
    df.insert(1, "date", dates)
    df.insert(2, "country", country)

    # save metadata 
    df.to_csv(args.output, sep="\t", index = False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input data")
    parser.add_argument('-o', '--output', help="Output file")
    args = parser.parse_args()
    main(args)
