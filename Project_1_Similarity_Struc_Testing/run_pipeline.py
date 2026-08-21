#python run_pipeline.py
#python run_pipeline.py --max-scenarios 30 --phase 2 3 4 5 6
#python run_pipeline.py --phase 6
import argparse
import sys
import time
from pathlib import Path

#cli
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description='CFG complexity and similarity pipeline'
    )
    p.add_argument(
        '--phase', nargs='+', type=int, default=[2, 3, 4, 5, 6],
        metavar='N',
        help='Phases to run (default: 2 3 4 5 6)',
    )
    p.add_argument('--metadata',       default='data/metadata.csv')
    p.add_argument('--raw',            default='data/raw')
    p.add_argument('--processed',      default='data/processed')
    p.add_argument('--max-scenarios',  type=int, default=30)
    p.add_argument('--normalize-ids',  action='store_true',
                   help='Normalize identifiers during preprocessing')
    p.add_argument('--cfg-dir',        default='data/results/cfg')
    p.add_argument('--results',        default='data/results')
    p.add_argument('--reports',        default='reports')
    p.add_argument('--project-root',   default='.')
    p.add_argument('--test-timeout',   type=int, default=60)
    return p.parse_args()

#Hhelpers 
def banner(phase: int, title: str) -> None:
    
    print(f'  phase {phase} {title}')
    
def check_csv(path: str, label: str) -> bool:
    if not Path(path).exists():
        print(f'  required file not found: {path} ({label})')
        return False
    return True

#        fo r phase  Rrunners 
def phase2(args: argparse.Namespace) -> str:
    banner(2, 'preprocesing')
    from src.preprocessing.preprocessor import run_preprocessing
    df = run_preprocessing(
        metadata_csv=args.metadata,
        raw_base=args.raw,
        processed_base=args.processed,
        normalize_ids=args.normalize_ids,
        max_scenarios=args.max_scenarios,
    )
    manifest = f'{args.processed}/preprocessing_manifest.csv'
    print(f'  Processed {len(df)} pairs  ({(df.status=="ok").sum()} ok)')
    return manifest

def phase3(args: argparse.Namespace, manifest: str) -> str:
    banner(3, 'structural Analysis')
    if not check_csv(manifest, 'preprocessing manifest'):
        sys.exit(1)
        
    from src.structural.structural_pipeline import run_structural_analysis
    from src.structural.cfg_visualizer import visualize_graphml_files
    
    struct_csv = f'{args.results}/structural_metrics.csv'
    
    #to ggenerate the aa  .graphml filees
    run_structural_analysis(
        manifest_csv=manifest,
        cfg_out_dir=args.cfg_dir,
        metrics_out=struct_csv,
    )
    #gHand off to viisualizer
    print('\n phase 3b: visualizing graphs')
    visualize_graphml_files(
        input_base_dir=args.cfg_dir,
        output_base_dir=f'{args.results}/cfg_visualize',
        manifest_csv_path=manifest 
    )
    return struct_csv

def phase4(args: argparse.Namespace, manifest: str) -> str:
    banner(4, 'similarity analysis')
    if not check_csv(manifest, 'preprocessing manifest'):
        sys.exit(1)
    from src.similarity.aggregator import run_similarity_analysis
    sim_csv = f'{args.results}/similarity_scores.csv'
    run_similarity_analysis(manifest_csv=manifest, out_csv=sim_csv)
    return sim_csv

def phase5(args: argparse.Namespace, manifest: str) -> str:
    banner(5, 'testing')
    if not check_csv(manifest, 'preprocessing manifest'):
        sys.exit(1)
    
    from src.testing.test_runner import run_all_tests

    # Target directory to save manual test files
    tests_dir = 'tests'
    test_results_csv = f'{args.results}/test_results.csv'
    
    #print('\n phase 5 running tests')
    run_all_tests(
        manifest_csv=manifest,
        tests_dir=tests_dir,
        out_csv=test_results_csv,
        timeout=args.test_timeout,
    )
    return test_results_csv

def phase6(args: argparse.Namespace) -> None:
    banner(6, 'evaluation')
    from src.evaluation.reporter import run_evaluation
    run_evaluation(
        structural_csv=f'{args.results}/structural_metrics.csv',
        similarity_csv=f'{args.results}/similarity_scores.csv',
        test_csv=f'{args.results}/test_results.csv',
        out_dir=args.reports,
        results_dir=args.results,
    )

#Mmain
def main() -> None:
    args = parse_args()
    phases = sorted(set(args.phase))
    t0 = time.time()

    manifest = f'{args.processed}/preprocessing_manifest.csv'

    for ph in phases:
        if ph == 2:
            manifest = phase2(args)
        elif ph == 3:
            phase3(args, manifest)
        elif ph == 4:
            phase4(args, manifest)
        elif ph == 5:
            phase5(args, manifest)
        elif ph == 6:
            phase6(args)
        else:
            print(f'unknown phase {ph}')

    elapsed = time.time() - t0
    
    print(f'  complete in {elapsed:.1f}s')
    print(f'  results in {args.results}/')
    print(f'  reports in {args.reports}/')
    print(f'  for dashboard run: streamlit run simple_dashboard.py')
    
if __name__ == '__main__':
    main()