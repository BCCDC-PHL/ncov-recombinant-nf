# ncov-recombinant-nf

Nextflow wrapper for [ktmeaton/ncov-recombinant](https://github.com/ktmeaton/ncov-recombinant)

The ncov2019-artic-nf output directory and the corresponding metadata.tsv file are required as input.

## Usage

```
nextflow run BCCDC-PHL/ncov-recombinant-nf  --cache ~/.conda/envs --artic_analysis_dir  --run_name --metadata --outdir
```

or  

```
./script_to_run_pipeline.sh
```
Enter the run name when prompted.

(Ensure the directories are set up according to your data before running the script.)
