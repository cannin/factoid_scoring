import jnius_config

reach_jar_path = "CHANGE_ME/reach/target/scala-2.11/reach-1.6.0-FAT.jar"

jnius_config.add_classpath(reach_jar_path)

import json
import requests
import pandas as pd
from tqdm import tqdm
from indra.sources import reach
from indra.statements.statements import stmts_to_json_file, stmts_to_json

from get_jsonpath import get_jsonpath

dat_filename = 'jwong_data/all_pmids_abstracts.csv'
results_filename = 'jwong_data/all_pmids_abstracts_scores_mod_types.csv'

dat = pd.read_csv(dat_filename)

scores = []
mod_scores = []
types = []

#maxIter = 10
maxIter = len(dat)

for i in tqdm(range(maxIter)): 
    text = dat['abstract'][i]

    try: 
        reach_processor = reach.api.process_text(text, offline=True)
        stmts = reach_processor.statements

        tmp = stmts_to_json(stmts)
        json_str = json.dumps(tmp) 
        jsonpath_expr_str = "$..type"
        results = get_jsonpath(None, json_str, jsonpath_expr_str)
        counts = dict((x, results.count(x)) for x in set(results))
        types_str = json.dumps(counts)

        score = len(stmts)

        # Modified score
        interactions_cnt = len(stmts)

        jsonpath_expr_str = "$..UP"
        l1 = get_jsonpath(None, json_str, jsonpath_expr_str)
        grounded_nodes_cnt = len(l1)

        jsonpath_expr_str = "$..db_refs"
        l1 = get_jsonpath(None, json_str, jsonpath_expr_str)
        ungrounded_nodes_cnt = len(l1) - grounded_nodes_cnt

        mod_score = grounded_nodes_cnt - 0.5*ungrounded_nodes_cnt + interactions_cnt
    except Exception as e:
        score = 0
        mod_score = 0
        types_str = '{}'

    scores.append(score)
    mod_scores.append(mod_score)
    types.append(types_str)

dat['score'] = scores 
dat['mod_score'] = mod_scores 
dat['types'] = types 
dat.to_csv(results_filename, index=False)

# DEBUG 
# text = 'Cleavage of influenza virus hemagglutinin (HA) by host proteases is essential for virus infectivity. HA of most influenza A and B (IAV/IBV) viruses is cleaved at a monobasic motif by trypsin-like proteases. Previous studies have reported that transmembrane serine protease 2 (TMPRSS2) is essential for activation of H7N9 and H1N1pdm IAV in mice but that H3N2 IAV and IBV activation is independent of TMPRSS2 and carried out by as-yet-undetermined protease(s). Here, to identify additional H3 IAV- and IBV-activating proteases, we used RNA-Seq to investigate the protease repertoire of murine lower airway tissues, primary type II alveolar epithelial cells (AECIIs), and the mouse lung cell line MLE-15. Among 13 candidates identified, TMPRSS4, TMPRSS13, hepsin, and prostasin activated H3 and IBV HA in vitro IBV activation and replication was reduced in AECIIs from Tmprss2/Tmprss4-deficient mice compared with WT or Tmprss2-deficient mice, indicating that murine TMPRSS4 is involved in IBV activation. Multicycle replication of H3N2 IAV and IBV in AECIIs of Tmprss2/Tmprss4-deficient mice varied in sensitivity to protease inhibitors, indicating that different, but overlapping, sets of murine proteases facilitate H3 and IBV HA cleavages. Interestingly, human hepsin and prostasin orthologs did not activate H3, but they did activate IBV HA in vitro Our results indicate that TMPRSS4 is an IBV-activating protease in murine AECIIs and suggest that TMPRSS13, hepsin, and prostasin cleave H3 and IBV HA in mice. They further show that hepsin and prostasin orthologs might contribute to the differences observed in TMPRSS2-independent activation of H3 in murine and human airways.'
# text = "Small RNAs derived from mature tRNAs, referred to as tRNA fragments or tRFs, are an emerging class of regulatory RNAs with poorly understood functions. We recently identified a role for one specific tRF-5' tRF-Gly-GCC, or tRF-GG-as a repressor of genes associated with the endogenous retroelement MERVL, but the mechanistic basis for this regulation was unknown. Here, we show that tRF-GG plays a role in production of a wide variety of noncoding RNAs-snoRNAs, scaRNAs, and snRNAs-that are dependent on Cajal bodies for stability and activity. Among these noncoding RNAs, regulation of the U7 snRNA by tRF-GG modulates heterochromatin-mediated transcriptional repression of MERVL elements by supporting an adequate supply of histone proteins. Importantly, the effects of inhibiting tRF-GG on histone mRNA levels, on activity of a histone 3' UTR reporter, and ultimately on MERVL regulation could all be suppressed by manipulating U7 RNA levels. We additionally show that the related RNA-binding proteins hnRNPF and hnRNPH bind directly to tRF-GG, and are required for Cajal body biogenesis, positioning these proteins as strong candidates for effectors of tRF-GG function in vivo. Together, our data reveal a conserved mechanism for 5 tRNA fragment control of noncoding RNA biogenesis and, consequently, global chromatin organization."
# reach_processor = reach.api.process_text(text, offline=True)
# stmts = reach_processor.statements
# stmts_to_json_file(stmts=stmts, fname='del.json')
# tmp = stmts_to_json(stmts)
# json_str = json.dumps(tmp) 

# score = len(stmts)
# score

# jsonpath_expr_str = "$..type"
# l1 = get_jsonpath(None, json_str, jsonpath_expr_str)
# counts = dict((x,l1.count(x)) for x in set(l1))
# counts_str = json.dumps(counts)

# jsonpath_expr_str = "$..db_refs"
# l1 = get_jsonpath(None, json_str, jsonpath_expr_str)
# counts = dict((x,l1.count(x)) for x in set(l1))
# counts_str = json.dumps(counts)

# jsonpath_expr_str = "$..UP"
# l1 = get_jsonpath(None, json_str, jsonpath_expr_str)
# counts = dict((x,l1.count(x)) for x in set(l1))
# counts_str = json.dumps(counts)

