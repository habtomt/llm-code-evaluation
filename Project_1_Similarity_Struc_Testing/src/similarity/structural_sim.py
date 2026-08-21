
import ast
from typing import Any, List, Tuple
import networkx as nx
try:
    import zss
    ZSS_AVAILABLE = True
except ImportError:
    ZSS_AVAILABLE = False
from src.structural.cfg_builder  import build_cfg
from src.structural.ast_analyzer import build_ast_graph
# tedd helpers
class _ZSSNode:
    
    def __init__(self, label: str):
        self.label = label
        self.children: List['_ZSSNode'] = []
 
    def addkid(self, child: '_ZSSNode') -> '_ZSSNode':
        self.children.append(child)
        return self
 
    @staticmethod
    def get_children(node: '_ZSSNode') -> List['_ZSSNode']:
        return node.children
 
    @staticmethod
    def get_label(node: '_ZSSNode') -> str:
        return node.label
 
 
def _ast_to_zss(node: ast.AST) -> '_ZSSNode':
    
    z = _ZSSNode(type(node).__name__)
    for child in ast.iter_child_nodes(node):
        z.addkid(_ast_to_zss(child))
    return z
 
 
def _ast_node_count(node: ast.AST) -> int:
    return sum(1 for _ in ast.walk(node))
 
 
def tree_edit_distance_similarity(src_a: str, src_b: str) -> float:
   
    try:
        tree_a = ast.parse(src_a)
        tree_b = ast.parse(src_b)
    except SyntaxError:
        return 0.0
 
    size_a = _ast_node_count(tree_a)
    size_b = _ast_node_count(tree_b)
    max_cost = size_a + size_b
    if max_cost == 0:
        return 1.0
 
    if ZSS_AVAILABLE:
        try:
            za = _ast_to_zss(tree_a)
            zb = _ast_to_zss(tree_b)
            dist = zss.simple_distance(
                za, zb,
                get_children=_ZSSNode.get_children,
                get_label=_ZSSNode.get_label,
                label_dist=lambda a, b: 0 if a == b else 1,
            )
            sim = 1.0 - (dist / max_cost)
        except Exception:
            sim = 1.0 - abs(size_a - size_b) / max_cost
    else:
                            #heuristic show ratio of smaller to laryger tree
        sim = min(size_a, size_b) / max(size_a, size_b)
 
    return round(min(max(sim, 0.0), 1.0), 6)

        #   graph Similarity 
def _cfg_label_set(graph: nx.DiGraph) -> set:
    return {data.get('label', '') for _, data in graph.nodes(data=True)}
 
 
def graph_similarity(src_a: str, src_b: str) -> float:
    
    cfg_a = build_cfg(src_a)
    cfg_b = build_cfg(src_b)
    labels_a = _cfg_label_set(cfg_a)
    labels_b = _cfg_label_set(cfg_b)
    union = labels_a | labels_b
    if not union:
        return 1.0
    intersection = labels_a & labels_b
    return round(len(intersection) / len(union), 6)
 
 
# Combined structural score 
 
def structural_similarity(src_a: str, src_b: str,
                          w_ted: float = 0.6,
                          w_graph: float = 0.4) -> float:
    
    ted   = tree_edit_distance_similarity(src_a, src_b)
    graph = graph_similarity(src_a, src_b)
    return round(w_ted * ted + w_graph * graph, 6)
 
 
def batch_structural_similarity(pairs: List[Tuple[str, str]]) -> List[float]:
    return [structural_similarity(a, b) for a, b in pairs]
 
