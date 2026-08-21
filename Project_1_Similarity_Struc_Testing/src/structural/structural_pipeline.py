import json
import os
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from src.structural.cfg_builder  import build_cfg, build_function_cfgs, save_cfg
from src.structural.metrics      import compute_cfg_metrics, compute_ast_metrics, compare_structural_metrics
from src.structural.ast_analyzer import build_ast_graph, ast_graph_features
from src.structural.cfg_visualizer import visualize_graphml_files 
 
def analyze_file(source: str, graph_out_prefix: str) -> Dict[str, Any]:
    
            ##cfg
    cfg = build_cfg(source)
    cfg_metrics = compute_cfg_metrics(cfg)
    save_cfg(cfg, graph_out_prefix + '_cfg.graphml')
 
# Per  function cfgs
    func_cfgs = build_function_cfgs(source)
    func_complexity = {fn: compute_cfg_metrics(g)['cyclomatic_complexity']
                       for fn, g in func_cfgs.items()}
 
            
            #ast graph
    ast_graph = build_ast_graph(source)
    ast_g_feats = ast_graph_features(ast_graph)
 
#aAST metrices
    ast_metrics = compute_ast_metrics(source)
 
    return {
        **{f'cfg_{k}': v for k, v in cfg_metrics.items()
           if not isinstance(v, dict)},
        'cfg_density': cfg_metrics.get('density', 0),
        'cfg_is_dag':  int(cfg_metrics.get('is_dag', True)),
        'max_func_complexity': max(func_complexity.values(), default=0),
        'num_functions': len(func_cfgs),
        **{f'ast_{k}': v for k, v in ast_metrics.items()
           if not isinstance(v, dict)},
        'ast_graph_nodes': ast_g_feats.get('ast_graph_nodes', 0),
        'ast_graph_edges': ast_g_feats.get('ast_graph_edges', 0),
        'ast_max_depth':   ast_g_feats.get('ast_max_depth', 0),
    }
 
 
def run_structural_analysis(
    manifest_csv: str,
    cfg_out_dir: str = 'data/results/cfg',
    metrics_out: str = 'data/results/structural_metrics.csv',
) -> pd.DataFrame:
    manifest = pd.read_csv(manifest_csv)
    manifest = manifest[manifest['status'] == 'ok']
 
    records = []
    for _, row in manifest.iterrows():
        scenario = row['scenario']
        task_id  = row['task_id']
 
        ref_src = Path(row['ref_processed']).read_text(encoding='utf-8', errors='replace')
        llm_src = Path(row['llm_processed']).read_text(encoding='utf-8', errors='replace')
 
        prefix_ref = os.path.join(cfg_out_dir, scenario, f'{task_id}_ref')
        prefix_llm = os.path.join(cfg_out_dir, scenario, f'{task_id}_llm')
        os.makedirs(os.path.dirname(prefix_ref), exist_ok=True)
 
        print(f'  Analyzing {scenario}/{task_id} …')
        ref_m = analyze_file(ref_src, prefix_ref)
        llm_m = analyze_file(llm_src, prefix_llm)
        diff  = compare_structural_metrics(ref_m, llm_m)
 
        record = {'scenario': scenario, 'task_id': task_id}
        record.update({f'ref_{k}': v for k, v in ref_m.items()})
        record.update({f'llm_{k}': v for k, v in llm_m.items()})
        record.update(diff)
        records.append(record)
 
    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(metrics_out) or '.', exist_ok=True)
    df.to_csv(metrics_out, index=False)
    print(f'\nphase 3 structural metrics savedin {metrics_out}')
    print(f'phase 3b generating cfg visualizations')
     
    visualize_graphml_files(cfg_out_dir, 'reports/cfg', manifest_csv)
    return df
 
 
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', default='data/processed/preprocessing_manifest.csv')
    p.add_argument('--cfg-dir',  default='data/results/cfg')
    p.add_argument('--out',      default='data/results/structural_metrics.csv')
    a = p.parse_args()
    run_structural_analysis(a.manifest, a.cfg_dir, a.out)