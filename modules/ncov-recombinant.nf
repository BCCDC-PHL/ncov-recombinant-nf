
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
 
  """
}

process create_metadata {

  tag { run_id }

  input:
  tuple val(run_id), file(metadata), path(consensus_seqs)

  output:
  tuple val(run_id), path("metadata_out.tsv")

  script:
  """
  create_metadata.py --input ${metadata} --output metadata_out.tsv --seqs ${consensus_seqs} --run ${run_id}
  """


}

process ncov_recombinant {

  tag { run_id }

  publishDir "${params.outdir}", mode: 'copy', pattern: "", saveAs: {filename -> filename.split("/").last()}

  input:
  tuple val(run_id), path(consensus_seqs), path(metadata), path(ncov_recombinant)
  
  output:
  path("ncov-recombinant/results/${run_id}")
  

  script:
  """
  # setup
  cp -r --dereference ncov-recombinant ncov-recombinant-local
  rm -r ncov-recombinant
  mv ncov-recombinant-local ncov-recombinant
  mkdir -p ncov-recombinant/data/${run_id}
  cp --dereference ${consensus_seqs} ncov-recombinant/data/${run_id}
  cp ${metadata} ncov-recombinant/data/${run_id}/metadata.tsv
  

  # run the pipeline...
  cd ncov-recombinant
  # create the profile
  scripts/create_profile.sh --data data/${run_id}
  
  # run snakemake
  snakemake --profile my_profiles/${run_id} --cores ${task.cpus}


  #add pipeline version to results

  cd results/${run_id}
  
  add_pipeline_version.py --version ${params.ncov_recombinant_version}

  """
}
