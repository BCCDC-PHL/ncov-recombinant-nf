
process download_ncov_recombinant {

  tag { version }

  executor 'local'
  
  input:
  val(version)
  
  output:
  path("ncov-recombinant", type: 'dir')

  script:
  """
  wget https://github.com/ktmeaton/ncov-recombinant/archive/refs/tags/v${version}.tar.gz
  tar -xzf v${version}.tar.gz
  mv ncov-recombinant-${version} ncov-recombinant
  """
}


process concatenate_consensus_seqs {

  tag { run_id }

  input:
  tuple val(run_id), path(artic_analysis_dir)
  
  output:
  tuple val(run_id), path("sequences.fasta"), emit: seqs

  script:
  """
  cat ${artic_analysis_dir}/${params.consensus_subdir}/*${params.consensus_file_suffix} > sequences.fasta 
  
  #TN - I had to change ${run_id}_sequences.fasta to sequences.fasta because of input requirements
  """
}

process create_metadata {

  tag { run_id }

  input:
  tuple val(run_id), file(metadata)

  output:
  tuple val(run_id), path("metadata.tsv")

  script:
  """
  cp ${metadata} metadata_original.tsv
  create_metadata.py
   
  """


}

process ncov_recombinant {

  tag { run_id }

  publishDir "${params.outdir}", mode: 'copy', pattern: ""

  input:
  tuple val(run_id), path(consensus_seqs), path(ncov_recombinant)
  
  output:
  path("ncov-recombinant/results/${run_id}")
  

  script:
  """
  # setup
  cp -r --dereference ncov-recombinant ncov-recombinant-local
  rm ncov-recombinant
  mv ncov-recombinant-local ncov-recombinant
  mkdir -p ncov-recombinant/data/${run_id}
  cp --dereference ${consensus_seqs} ncov-recombinant/data/${run_id}
  cp /home/tara.newman/recombinant_pipeline_development/ncov-recombinant-nf/test_input/analysis_by_run/220303_VH00502_53_AAAVYGTM5/data/metadata.tsv ncov-recombinant/data/${run_id}
  # run the pipeline...
  cd ncov-recombinant
  # create the profile
  scripts/create_profile.sh --data data/${run_id}
  
  # run snakemake
  pip install click
  snakemake --profile my_profiles/${run_id}
  """
}
