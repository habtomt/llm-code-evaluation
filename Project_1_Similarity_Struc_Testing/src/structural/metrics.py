
import ast
import math
from collections import Counter
from typing import Any, Dict, List
 
import networkx as nx
import numpy as np
 
 
# /'cfg metrics
 
def cyclomatic_complexity(graph: nx.DiGraph) -> int:
    """
    M = E - N + 2P
    where E = edges, N = nodes, P = connected components (in undirected sense).
    """
    E = graph.number_of_edges()
    N = graph.number_of_nodes()
    P = nx.number_weakly_connected_components(graph)
    return E - N + 2 * P
 
 
def graph_depth(graph: nx.DiGraph) -> int:
   


    if graph.number_of_nodes() == 0:
        return 0
    sources = [n for n, d in graph.in_degree() if d == 0]
    if not sources:
        return 0
    max_depth = 0
    for src in sources:
        try:
            lengths = nx.single_source_shortest_path_length(graph, src)
            max_depth = max(max_depth, max(lengths.values(), default=0))
        except Exception:
            pass
    return max_depth
 
 
def degree_distribution(graph: nx.DiGraph) -> Dict[str, Any]:
    
    in_degs  = [d for _, d in graph.in_degree()]
    out_degs = [d for _, d in graph.out_degree()]
 
    def _stats(seq: List[int]) -> Dict[str, float]:
        if not seq:
            return dict(mean=0.0, std=0.0, max=0, entropy=0.0)
        arr = np.array(seq, dtype=float)
        counts = Counter(seq)
        total  = len(seq)
        probs  = np.array([c / total for c in counts.values()])
        entropy = -float(np.sum(probs * np.log(probs + 1e-12)))
        return dict(mean=float(arr.mean()), std=float(arr.std()),
                    max=int(arr.max()), entropy=round(entropy, 4))
 
    return dict(in_degree=_stats(in_degs), out_degree=_stats(out_degs))
 
 
def compute_cfg_metrics(graph: nx.DiGraph) -> Dict[str, Any]:
    """Aggregate all CFG metrics into one dict."""
    return {
        'num_nodes':            graph.number_of_nodes(),
        'num_edges':            graph.number_of_edges(),
        'cyclomatic_complexity': cyclomatic_complexity(graph),
        'graph_depth':          graph_depth(graph),
        'degree_dist':          degree_distribution(graph),
        'density':              round(nx.density(graph), 6),
        'is_dag':               nx.is_directed_acyclic_graph(graph),
    }
 
 
# \\ast metrics 
 
class ASTMetricsVisitor(ast.NodeVisitor):
    """Collect AST-level structural features in a single walk."""
 
    def __init__(self) -> None:
        self.node_counts: Counter = Counter()
        self.max_depth: int = 0
        self._depth: int = 0
 
    def generic_visit(self, node: ast.AST) -> None:
        self.node_counts[type(node).__name__] += 1
        self._depth += 1
        self.max_depth = max(self.max_depth, self._depth)
        super().generic_visit(node)
        self._depth -= 1
 
 
def compute_ast_metrics(source: str) -> Dict[str, Any]:
    """Parse *source* and return AST structural features."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {'error': str(exc)}
 
    visitor = ASTMetricsVisitor()
    visitor.visit(tree)
 
    total_nodes = sum(visitor.node_counts.values())
    branching_nodes = (
        visitor.node_counts.get('If', 0)
        + visitor.node_counts.get('For', 0)
        + visitor.node_counts.get('While', 0)
        + visitor.node_counts.get('Try', 0)
        + visitor.node_counts.get('ExceptHandler', 0)
    )
 
    return {
        'total_ast_nodes':  total_nodes,
        'max_ast_depth':    visitor.max_depth,
        'branching_nodes':  branching_nodes,
        'function_defs':    visitor.node_counts.get('FunctionDef', 0)
                          + visitor.node_counts.get('AsyncFunctionDef', 0),
        'class_defs':       visitor.node_counts.get('ClassDef', 0),
        'imports':          visitor.node_counts.get('Import', 0)
                          + visitor.node_counts.get('ImportFrom', 0),
        'return_stmts':     visitor.node_counts.get('Return', 0),
        'node_type_counts': dict(visitor.node_counts),
    }
 
 
# ';structural comparison 
 
def compare_structural_metrics(ref_metrics: Dict, llm_metrics: Dict) -> Dict[str, Any]:
    

    scalar_keys = [
        'num_nodes', 'num_edges', 'cyclomatic_complexity',
        'graph_depth', 'density',
    ]
    result: Dict[str, Any] = {}
    for key in scalar_keys:
        r_val = ref_metrics.get(key, 0)
        l_val = llm_metrics.get(key, 0)
        result[f'diff_{key}'] = round(float(l_val) - float(r_val), 6)
        result[f'absdiff_{key}'] = round(abs(float(l_val) - float(r_val)), 6)
    return result
 
