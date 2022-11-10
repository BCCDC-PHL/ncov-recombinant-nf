# ncov-recombinant-nf

Nextflow wrapper for [ktmeaton/ncov-recombinant](https://github.com/ktmeaton/ncov-recombinant)

The ncov2019-artic-nf output directory and the corresponding metadata.tsv file are required as input.

## Usage

```
nextflow run BCCDC-PHL/ncov-recombinant-nf \
  -profile conda \
  --cache ~/.conda/envs \
  --artic_analysis_dir  </path/to/artic-outputs> \
  --run_name <run_name> \
  --metadata </path/to/metadata.tsv> \
  --outdir </path/to/outdir>

```


