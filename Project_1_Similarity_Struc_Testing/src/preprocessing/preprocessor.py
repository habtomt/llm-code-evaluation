
import ast, io, keyword, os, re, tokenize
import builtins as _builtins
import pandas as pd
from pathlib import Path
from typing import Optional
         #helpers 
 
BUILTIN_NAMES = set(dir(_builtins))
KEYWORD_NAMES = set(keyword.kwlist)
 
 
def remove_comments_and_docstrings(source: str) -> str:
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        out = []
        prev_ttype = tokenize.INDENT
        
        for ttype, tstr, *rest in tokens:
            
            if ttype == tokenize.COMMENT: 
                continue
                
            
            if ttype == tokenize.STRING:
                
                if prev_ttype in (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL):
                    
                    if tstr.startswith(('"""', "'''")):
                        continue
            
            out.append((ttype, tstr))
            prev_ttype = ttype
            
        return tokenize.untokenize(out)
    except (tokenize.TokenError, IndentationError):
        src = re.sub(r'#[^\n]*', '', source)
        return src
 
 
def normalize_whitespace(source: str) -> str:
    
    lines, result, prev_blank = source.splitlines(), [], False
    for line in lines:
        stripped = line.rstrip()
        if stripped == '':
            if not prev_blank:
                result.append('')
            prev_blank = True
        else:
            result.append(stripped)
            prev_blank = False
    return '\n'.join(result).strip()
 
 
def normalize_identifiers(source: str) -> str:
    
    try:
        raw_tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError, Exception):
        return source
 
    name_map: dict = {}
    counter = 0
    out = []
    for ttype, tstr, tstart, tend, tline in raw_tokens:
        if ttype == tokenize.NAME:
            if tstr in KEYWORD_NAMES or tstr in BUILTIN_NAMES:
                out.append((ttype, tstr, tstart, tend, tline))
            else:
                if tstr not in name_map:
                    name_map[tstr] = f'VAR_{counter}'
                    counter += 1
                out.append((ttype, name_map[tstr], tstart, tend, tline))
        elif ttype == tokenize.STRING:
            out.append((ttype, 'STR_LIT', tstart, tend, tline))
        elif ttype == tokenize.NUMBER:
            out.append((ttype, 'NUM_LIT', tstart, tend, tline))
        else:
            out.append((ttype, tstr, tstart, tend, tline))
    try:
        return tokenize.untokenize(out)
    except Exception:
        return source
 
 
def preprocess_source(source: str, normalize_ids: bool = False) -> str:
   
    source = remove_comments_and_docstrings(source)
    source = normalize_whitespace(source)
    if normalize_ids:
        source = normalize_identifiers(source)
    return source
 
 
#ffile I / O 
 
def preprocess_file(src_path: str, dst_path: str,
                    normalize_ids: bool = False) -> Optional[str]:
    try:
        raw = Path(src_path).read_text(encoding='utf-8', errors='replace')
    except OSError as exc:
        print(f'  [WARN] Cannot read {src_path}: {exc}')
        return None
    cleaned = preprocess_source(raw, normalize_ids=normalize_ids)
    Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
    Path(dst_path).write_text(cleaned, encoding='utf-8')
    return cleaned
 
 
                # batch runer 
 
def run_preprocessing(
    metadata_csv: str,
    raw_base: str = 'data/raw',
    processed_base: str = 'data/processed',
    normalize_ids: bool = False,
    max_scenarios: int = 15,
) -> pd.DataFrame:
    
    meta = pd.read_csv(metadata_csv)
    scenarios = meta['scenario'].unique()[:max_scenarios]
    meta = meta[meta['scenario'].isin(scenarios)].copy()
 
    records = []
    for _, row in meta.iterrows():
        scenario, task_id = row['scenario'], row['task_id']
        
        ref_in  = os.path.join('data', row['reference_file'])
        llm_in  = os.path.join('data', row['llm_file'])
        
        ref_out = os.path.join('data', row['reference_file'].replace('raw/', 'processed/'))
        llm_out = os.path.join('data', row['llm_file'].replace('raw/', 'processed/'))
 
        r_ok = preprocess_file(ref_in, ref_out, normalize_ids) is not None
        l_ok = preprocess_file(llm_in, llm_out, normalize_ids) is not None
        status = 'ok' if (r_ok and l_ok) else 'error'
        records.append(dict(scenario=scenario, task_id=task_id,
                            ref_processed=ref_out, llm_processed=llm_out,
                            status=status))
        print(f'  [{status.upper()}] {scenario}/{task_id}')
 
    df = pd.DataFrame(records)
    manifest = os.path.join(processed_base, 'preprocessing_manifest.csv')
    os.makedirs(processed_base, exist_ok=True)
    df.to_csv(manifest, index=False)
    print(f'\nphase 2 manifest saved in {manifest}')
    return df
 
 
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--metadata',       default='data/metadata.csv')
    p.add_argument('--raw',            default='data/raw')
    p.add_argument('--processed',      default='data/processed')
    p.add_argument('--normalize-ids',  action='store_true')
    p.add_argument('--max-scenarios',  type=int, default=15)
    a = p.parse_args()
    run_preprocessing(a.metadata, a.raw, a.processed, a.normalize_ids, a.max_scenarios)
 
