# ncov-recombinant-nf

Nextflow wrapper for [ktmeaton/ncov-recombinant](https://github.com/ktmeaton/ncov-recombinant)

The ncov2019-artic-nf output directory and the corresponding metadata.tsv file are required as input.

## Usage

```
nextflow run BCCDC-PHL/ncov-recombinant-nf  --cache ~/.conda/envs --artic_analysis_dir  --run_name --metadata --outdir
```


Example script to run the pipeline with run as input:

```
#!/bin/bash

echo Please enter the run name:
read RUN

nextflow run main.nf -profile conda --cache ~/.conda/envs --artic_analysis_dir test_input/analysis_by_run/$RUN/ncov2019-artic-nf-v1.3-output  --run_name $RUN --metadata test_input/analysis_by_run/$RUN/metadata.tsv --outdir test_output
```
Enter the run name when prompted and ensure the directories are set up according to your data before running the script.)
