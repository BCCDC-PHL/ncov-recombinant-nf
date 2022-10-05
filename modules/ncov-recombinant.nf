
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
  tuple val(run_id), path("${run_id}_sequences.fasta"), emit: seqs

  script:
  """
  cat ${artic_analysis_dir}/${params.consensus_subdir}/*${params.consensus_file_suffix} > ${run_id}_sequences.fasta
  """
}


process ncov_recombinant {

  tag { run_id }

  publishDir "${params.outdir}", mode: 'copy', pattern: ""

  input:
  tuple val(run_id), path(consensus_seqs), path(ncov_recombinant)
  
  output:

  script:
  """
  # setup
  cp -r --dereference ncov-recombinant ncov-recombinant-local
  rm ncov-recombinant
  mv ncov-recombinant-local ncov-recombinant
  mkdir -p ncov-recombinant/data/${run_id}
  cp --dereference ${consensus_seqs} ncov-recombinant/data/${run_id}

  # run the pipeline...
  """
}
