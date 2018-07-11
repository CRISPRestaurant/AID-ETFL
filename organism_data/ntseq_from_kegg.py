import cobra
import pandas as pd
import numpy as np
import requests

kegg_url = "http://rest.kegg.jp/get/{org}:{gene_name}/ntseq"

ecoli = cobra.io.load_json_model('../models/iJO1366.json')

all_b_genes = pd.Series(['eco:{}'.format(x.id) for x in ecoli.genes])

rnap_genes = pd.Series(['eco:b3295','eco:b3649','eco:b3987','eco:b3988'])
rrna_genes = pd.Series(['eco:b3851','eco:b3854','eco:b3855'])
rpeptide_genes = pd.read_csv('ribosomal_proteins_ecoli.tsv',
                             delimiter='\t',
                             header=None)[0]

all_b_genes = pd.concat([all_b_genes, rnap_genes, rrna_genes, rpeptide_genes])

def get_from_kegg(gene_id):
    org,gene_name = gene_id.split(':')
    response = requests.post(kegg_url.format(org=org,
                                             gene_name=gene_name))
    if response.ok:
        eol_ix = response.text.find('\n')
        text = response.text[eol_ix+1:].replace('\n','')
        return text
    else:
        return np.nan

nt_sequences = all_b_genes.apply(get_from_kegg)
nt_sequences.index = all_b_genes.str.split(':').apply(lambda x:x[1])
nt_sequences.dropna(inplace = True)
nt_sequences.to_csv('iJO1366_nt_seq_kegg.csv', )