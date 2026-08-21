
import os
from pathlib import Path
from typing import Optional
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set_theme(style='whitegrid', palette='muted')
FIGURE_DPI = 150
                        #    data  loading 
 
def load_results(
    structural_csv: str,
    similarity_csv: str,
    test_csv: str,
) -> pd.DataFrame:
    #merge all three result tables on (scenario, task_id)
    struct = pd.read_csv(structural_csv)
    sim    = pd.read_csv(similarity_csv)
    tests  = pd.read_csv(test_csv)
 
    df = sim.merge(struct, on=['scenario', 'task_id'], how='left')
    df = df.merge(tests,  on=['scenario', 'task_id'], how='left')
    df['pass_rate']   = df['pass_rate'].fillna(0.0)
    df['coverage_pct'] = df['coverage_pct'].fillna(-1.0)
    return df
        # vvisualizations
 
def _save(fig: plt.Figure, path: str) -> None:
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close(fig)
    #print(f'  figure {path}')
def plot_similarity_histogram(df: pd.DataFrame, out: str) -> None:
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Similarity Score Distributions', fontsize=14, fontweight='bold')
 #final score histogram
    ax = axes[0]
    ax.hist(df['s_final'].dropna(), bins=20, color='steelblue',
            edgecolor='white', alpha=0.85)
    ax.axvline(df['s_final'].mean(), color='red', ls='--',
               label=f'Mean={df["s_final"].mean():.3f}')
    ax.set_xlabel('Final Similarity Score')
    ax.set_ylabel('Count')
    ax.set_title('Final Similarity (S_final)')
    ax.legend()
 
            # comp onent    comparison
    ax2 = axes[1]
    components = ['s_lexical', 's_structural', 's_semantic']
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    for col, c in zip(components, colors):
        ax2.hist(df[col].dropna(), bins=20, alpha=0.55, color=c,
                 label=col.replace('s_', '').title(), edgecolor='white')
    ax2.set_xlabel('Score')
    ax2.set_ylabel('Count')
    ax2.set_title('Component Scores Overlay')
    ax2.legend()
 
    _save(fig, out)
 
 
def plot_boxplot_per_scenario(df: pd.DataFrame, out: str) -> None:
    
    fig, ax = plt.subplots(figsize=(max(10, len(df['scenario'].unique()) * 0.8), 6))
    order = (df.groupby('scenario')['s_final']
               .median()
               .sort_values(ascending=False)
               .index.tolist())
    sns.boxplot(data=df, x='scenario', y='s_final', order=order, ax=ax,
                palette='Blues_d')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha='right', fontsize=9)
    ax.set_title('Final Similarity by Scenario', fontsize=13, fontweight='bold')
    ax.set_ylabel('S_final')
    ax.set_xlabel('Scenario')
    _save(fig, out)
 
 
def plot_scatter_sim_vs_complexity(df: pd.DataFrame, out: str) -> None:
    
    if 'llm_cfg_cyclomatic_complexity' not in df.columns:
        print('  [WARN] Skipping scatter (complexity column missing)')
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(
        df['llm_cfg_cyclomatic_complexity'], df['s_final'],
        c=df['s_semantic'], cmap='viridis', alpha=0.7, edgecolors='k', linewidths=0.3,
    )
    plt.colorbar(sc, ax=ax, label='Semantic Similarity')
    ax.set_xlabel('Cyclomatic Complexity (LLM)')
    ax.set_ylabel('Final Similarity (S_final)')
    ax.set_title('Similarity vs Cyclomatic Complexity', fontsize=13, fontweight='bold')
 
                                     #ttrend line
    x = df['llm_cfg_cyclomatic_complexity'].dropna()
    y = df.loc[x.index, 's_final'].dropna()
    idx = x.index.intersection(y.index)
    if len(idx) > 2:
        z = np.polyfit(x[idx], y[idx], 1)
        p = np.poly1d(z)
        xr = np.linspace(x.min(), x.max(), 100)
        ax.plot(xr, p(xr), 'r--', alpha=0.7, label='Trend')
        ax.legend()
    _save(fig, out)
 
 
def plot_scatter_sim_vs_passrate(df: pd.DataFrame, out: str) -> None:
    
    if 'pass_rate' not in df.columns:
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df['pass_rate'], df['s_final'],
               c=df['s_structural'], cmap='plasma',
               alpha=0.7, edgecolors='k', linewidths=0.3)
    ax.set_xlabel('Test Pass Rate')
    ax.set_ylabel('Final Similarity (S_final)')
    ax.set_title('Similarity vs Test Pass Rate', fontsize=13, fontweight='bold')
 
#aannotate intereesting quadrants
    for q, label in [
        ((0.5, 0.5, 1.0, 1.0), 'High sim, high pass'),
        ((0.0, 0.5, 0.5, 1.0), 'Low pass, high sim\n(Superficial)'),
        ((0.5, 0.0, 1.0, 0.5), 'High pass, low sim\n(Alt. correct)'),
    ]:
        ax.axhline(0.5, color='gray', ls=':', alpha=0.4)
        ax.axvline(0.5, color='gray', ls=':', alpha=0.4)
    _save(fig, out)
 
 
def plot_correlation_heatmap(df: pd.DataFrame, out: str) -> None:
    
    numeric_cols = [
        's_lexical', 's_structural', 's_semantic', 's_final', 'pass_rate',
        'coverage_pct',
        'llm_cfg_cyclomatic_complexity', 'llm_cfg_num_nodes', 'llm_cfg_num_edges',
        'llm_cfg_graph_depth', 'llm_ast_total_ast_nodes', 'llm_ast_branching_nodes',
        'absdiff_cyclomatic_complexity', 'absdiff_num_nodes',
    ]
    present = [c for c in numeric_cols if c in df.columns]
    if len(present) < 2:
        print('  Not enough columns for heatmap')
        return
    corr = df[present].corr()
    fig, ax = plt.subplots(figsize=(max(10, len(present)), max(8, len(present) - 2)))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, linewidths=0.5, ax=ax,
                xticklabels=[c.replace('llm_cfg_', '').replace('llm_ast_', '')
                              for c in present],
                yticklabels=[c.replace('llm_cfg_', '').replace('llm_ast_', '')
                              for c in present])
    ax.set_title('Correlation Heatmap', fontsize=13, fontweight='bold')
    plt.xticks(rotation=35, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    _save(fig, out)
#     \\suummary statistics
 
def compute_summary(df: pd.DataFrame, out_csv: str) -> pd.DataFrame:
    
    agg_cols = ['s_lexical', 's_structural', 's_semantic', 's_final', 'pass_rate']
    agg_cols = [c for c in agg_cols if c in df.columns]
    summary = (df.groupby('scenario')[agg_cols]
                  .agg(['mean', 'std', 'min', 'max'])
                  .round(4))
    summary.columns = ['_'.join(c) for c in summary.columns]
    summary.reset_index(inplace=True)
 
    os.makedirs(os.path.dirname(out_csv) or '.', exist_ok=True)
    summary.to_csv(out_csv, index=False)
    print(f'  summary in {out_csv}')
    return summary
 
 
            # main pipeline 
def run_evaluation(
    structural_csv: str = 'data/results/structural_metrics.csv',
    similarity_csv: str = 'data/results/similarity_scores.csv',
    test_csv:       str = 'data/results/test_results.csv',
    out_dir:        str = 'reports',
    results_dir:    str = 'results',
) -> None:
    print('results')
    df = load_results(structural_csv, similarity_csv, test_csv)
 
    print(f'  total llm & ref pairs: {len(df)}')
    print(f'  mean S_final: {df["s_final"].mean():.4f}')
    print(f'  mean pass_rate: {df["pass_rate"].mean():.4f}')
 
#, summary CSV
    compute_summary(df, os.path.join(results_dir, 'evaluation_summary.csv'))
 
#figures
    plot_similarity_histogram(df,
        os.path.join(out_dir, 'fig_similarity_histogram.png'))
    plot_boxplot_per_scenario(df,
        os.path.join(out_dir, 'fig_boxplot_per_scenario.png'))
    plot_scatter_sim_vs_complexity(df,
        os.path.join(out_dir, 'fig_scatter_sim_vs_complexity.png'))
    plot_scatter_sim_vs_passrate(df,
        os.path.join(out_dir, 'fig_scatter_sim_vs_passrate.png'))
    plot_correlation_heatmap(df,
        os.path.join(out_dir, 'fig_correlation_heatmap.png'))
 
    print(f'\nevaluation complete {out_dir}/')
 
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--structural', default='data/results/structural_metrics.csv')
    p.add_argument('--similarity', default='data/results/similarity_scores.csv')
    p.add_argument('--tests',      default='data/results/test_results.csv')
    p.add_argument('--out-dir',    default='reports')
    p.add_argument('--results',    default='results')
    a = p.parse_args()
    run_evaluation(a.structural, a.similarity, a.tests, a.out_dir, a.results)
 
