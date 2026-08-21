
import warnings
from typing import List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine
 
warnings.filterwarnings('ignore')

        #lazy-load to avoid mandatory GPUor transformers dependency
_tokenizer = None
_model     = None
 
 
def _load_model():
    global _tokenizer, _model
    if _tokenizer is None:
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
            _tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')
            _model     = AutoModel.from_pretrained('microsoft/codebert-base')
            _model.eval()
            print('[Semantic] CodeBERT loaded.')
        except Exception as exc:
            print(f'[Semantic] CodeBERT unavailable ({exc}); using TF-IDF fallback.')
            _tokenizer = 'fallback'
            _model     = 'fallback'
 
 
def _embed_codebert(source: str) -> np.ndarray:
    
    import torch
    inputs = _tokenizer(
        source, return_tensors='pt', truncation=True,
        max_length=512, padding=True,
    )
    with torch.no_grad():
        outputs = _model(**inputs)
    
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding
 
 
def _embed_tfidf(source: str) -> np.ndarray:
    
    from sklearn.feature_extraction.text import HashingVectorizer
    vec = HashingVectorizer(n_features=2**14, norm='l2')
    return vec.transform([source]).toarray()[0]
 
 
def embed(source: str) -> np.ndarray:
    _load_model()
    if _tokenizer == 'fallback':
        return _embed_tfidf(source)
    return _embed_codebert(source)
 
 
def semantic_similarity(src_a: str, src_b: str) -> float:
    
    if not src_a.strip() and not src_b.strip():
        return 1.0
    if not src_a.strip() or not src_b.strip():
        return 0.0
 
    emb_a = embed(src_a).reshape(1, -1)
    emb_b = embed(src_b).reshape(1, -1)
    raw   = float(sk_cosine(emb_a, emb_b)[0, 0])
    # Cosine can return values slightly below 0 due to floating point
    return round(min(max(raw, 0.0), 1.0), 6)
 
 
def batch_semantic_similarity(pairs: List[Tuple[str, str]]) -> List[float]:
    return [semantic_similarity(a, b) for a, b in pairs]
 
