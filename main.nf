#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include { download_ncov_recombinant }  from './modules/ncov-recombinant.nf'
include { ncov_recombinant }           from './modules/ncov-recombinant.nf'
include { concatenate_consensus_seqs } from './modules/ncov-recombinant.nf'
include { create_metadata } from './modules/ncov-recombinant.nf'

workflow {

  ch_ncov_recombinant_version = Channel.of(params.ncov_recombinant_version)
  ch_run_name = Channel.of(params.run_name)
  ch_artic_analysis_dir = Channel.fromPath(params.artic_analysis_dir, type: 'dir')
  ch_metadata = Channel.fromPath(params.metadata, type: 'file')

  download_ncov_recombinant(ch_ncov_recombinant_version)

  concatenate_consensus_seqs(ch_run_name.combine(ch_artic_analysis_dir))

  create_metadata(ch_run_name.combine(ch_metadata).join(concatenate_consensus_seqs.out.seqs)).view()

  ncov_recombinant(concatenate_consensus_seqs.out.seqs.join(create_metadata.out).combine(download_ncov_recombinant.out))
 
}
