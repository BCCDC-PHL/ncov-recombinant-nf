# ncov-recombinant-nf

Nextflow wrapper for [ktmeaton/ncov-recombinant](https://github.com/ktmeaton/ncov-recombinant)



## Usage

This pipeline is designed to take in the run name, the ncov2019-artic-nf output directory of consensus sequence files for that run and the corresponding metadata.tsv file as input.

```
nextflow run BCCDC-PHL/ncov-recombinant-nf \
  -profile conda \
  --cache ~/.conda/envs \
  --artic_analysis_dir  </path/to/artic-outputs> \
  --run_name <run_name> \
  --metadata </path/to/metadata.tsv> \
  --outdir </path/to/outdir>

```


