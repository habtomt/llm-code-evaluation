
import re
import tokenize
import io
from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
 
# ttokenization
 
def tokenize_code(source: str) -> str:
    


    tokens = []
    try:
        for tok_type, tok_str, *_ in tokenize.generate_tokens(
                io.StringIO(source).readline):
            if tok_type in (tokenize.COMMENT, tokenize.NEWLINE,
                            tokenize.NL, tokenize.INDENT,
                            tokenize.DEDENT, tokenize.ENCODING,
                            tokenize.ENDMARKER):
                continue
            tokens.append(tok_str)
    except tokenize.TokenError:
        tokens = source.split()
    return ' '.join(tokens)
 
 
          #pairwise      similarity 
 
def lexical_similarity(src_a: str, src_b: str) -> float:
    
    tok_a = tokenize_code(src_a)
    tok_b = tokenize_code(src_b)
 
    if not tok_a.strip() and not tok_b.strip():
        return 1.0
    if not tok_a.strip() or not tok_b.strip():
        return 0.0
 
    vectorizer = TfidfVectorizer(
        analyzer='word',
        token_pattern=r'(?u)\b\w+\b',
        sublinear_tf=True,
    )
    try:
        tfidf = vectorizer.fit_transform([tok_a, tok_b])
        score = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0, 0])
    except ValueError:
        score = 0.0
 
    return round(min(max(score, 0.0), 1.0), 6)
 
 
def batch_lexical_similarity(pairs: List[Tuple[str, str]]) -> List[float]:
    #"  cCompute lexical similarity(ref, llm)pairs"""
    return [lexical_similarity(a, b) for a, b in pairs]
 
