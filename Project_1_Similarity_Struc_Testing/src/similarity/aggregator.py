
import os
from pathlib import Path
from typing import Dict, Tuple
 
import pandas as pd
from tqdm import tqdm
 
from src.similarity.lexical        import lexical_similarity
from src.similarity.structural_sim import structural_similarity
from src.similarity.semantic       import semantic_similarity
                #   weights s
W_LEXICAL    = 0.2
W_STRUCTURAL = 0.4
W_SEMANTIC   = 0.4
 
 
def final_score(s_lex: float, s_struct: float, s_sem: float) -> float:
    """Weighted aggregation; all inputs and output in [0, 1]."""
    return round(W_LEXICAL * s_lex + W_STRUCTURAL * s_struct + W_SEMANTIC * s_sem, 6)
 
 
#             pipfeline 
 
def run_similarity_analysis(
    manifest_csv: str,
    out_csv: str = 'data/results/similarity_scores.csv',
) -> pd.DataFrame:
    
    manifest = pd.read_csv(manifest_csv)
    manifest = manifest[manifest['status'] == 'ok'].reset_index(drop=True)
 
    records = []
    for _, row in tqdm(manifest.iterrows(), total=len(manifest),
                       desc='phase 4 similarity'):
        scenario = row['scenario']
        task_id  = row['task_id']
 
        ref_src = Path(row['ref_processed']).read_text(encoding='utf-8', errors='replace')
        llm_src = Path(row['llm_processed']).read_text(encoding='utf-8', errors='replace')
 
        s_lex    = lexical_similarity(ref_src, llm_src)
        s_struct = structural_similarity(ref_src, llm_src)
        s_sem    = semantic_similarity(ref_src, llm_src)
        s_final  = final_score(s_lex, s_struct, s_sem)
 
        records.append({
            'scenario':          scenario,
            'task_id':           task_id,
            's_lexical':         s_lex,
            's_structural':      s_struct,
            's_semantic':        s_sem,
            's_final':           s_final,
            'w_lexical':         W_LEXICAL,
            'w_structural':      W_STRUCTURAL,
            'w_semantic':        W_SEMANTIC,
        })
        print(f'    {scenario}/{task_id}: lex={s_lex:.3f}  '
              f'struct={s_struct:.3f}  sem={s_sem:.3f}  '
              f'final={s_final:.3f}')
 
    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(out_csv) or '.', exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f'\nphase 4 similarity scores {out_csv}')
    return df
 
 
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', default='data/processed/preprocessing_manifest.csv')
    p.add_argument('--out',      default='data/results/similarity_scores.csv')
    a = p.parse_args()
    run_similarity_analysis(a.manifest, a.out)
 
