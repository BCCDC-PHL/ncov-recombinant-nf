
process download_ncov_recombinant {

  tag { version }

  executor 'local'
  
  input:
  val(version)
  
  output:
  path("ncov-recombinant", type: 'dir')

  script:
  """
  wget https://github.com/ktmeaton/ncov-recombinant/archive/v${version}.tar.gz
  tar -xzf v${version}.tar.gz
  mv ncov-tools-${version} ncov-tools
  """
}



process ncov_recombinant {

  tag { run_id }

  publishDir "${params.outdir}", mode: 'copy', pattern: ""

  input:
  tuple val(run_id), path(ncov_recombinant)
  
  output:

  script:
  """

  """
}
