#!/bin/bash


echo Please enter the run name:
read RUN



nextflow run main.nf -profile conda --cache ~/.conda/envs --artic_analysis_dir test_input/analysis_by_run/$RUN/ncov2019-artic-nf-v1.3-output  --run_name $RUN --metadata test_input/analysis_by_run/$RUN/metadata.tsv --outdir test_output -resume


# this undoes the changes to metadata.tsv made by the pipeline in create_metadata.py (caused by git issue #2 - temporary fix) 
cp test_input/analysis_by_run/220303_VH00502_53_AAAVYGTM5/metadata_original.tsv test_input/analysis_by_run/220303_VH00502_53_AAAVYGTM5/metadata.tsv

