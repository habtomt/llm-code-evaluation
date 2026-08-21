
import ast
from typing import Dict, Any, Tuple
import networkx as nx
 
 
class ASTGraphBuilder(ast.NodeVisitor):
#converts a Python AST in to a the directed graph
 
    def __init__(self) -> None:
        self._graph: nx.DiGraph = nx.DiGraph()
        self._counter: int = 0
        self._parent_id: int = -1
 
    def _new_id(self) -> int:
        nid = self._counter
        self._counter += 1
        return nid
 
    def build(self, source: str) -> nx.DiGraph:
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            g = nx.DiGraph()
            g.add_node(0, label='SYNTAX_ERROR')
            return g
        root_id = self._new_id()
        self._graph.add_node(root_id, label='Module')
        self._parent_id = root_id
        for child in ast.iter_child_nodes(tree):
            self._visit_node(child, parent_id=root_id)
        return self._graph
 
    def _visit_node(self, node: ast.AST, parent_id: int) -> int:
        nid = self._new_id()
        label = type(node).__name__
        self._graph.add_node(nid, label=label)
        self._graph.add_edge(parent_id, nid)
        for child in ast.iter_child_nodes(node):
            self._visit_node(child, parent_id=nid)
        return nid
 
 
def build_ast_graph(source: str) -> nx.DiGraph:
    return ASTGraphBuilder().build(source)
 
 
def ast_graph_features(graph: nx.DiGraph) -> Dict[str, Any]:
    """Summary statistics of the AST graph."""
    if graph.number_of_nodes() == 0:
        return {}
    labels = [data.get('label', '') for _, data in graph.nodes(data=True)]
    from collections import Counter
    label_counts = Counter(labels)
    depths = {}
    roots = [n for n, d in graph.in_degree() if d == 0]
    for r in roots:
        for n, depth in nx.single_source_shortest_path_length(graph, r).items():
            depths[n] = max(depths.get(n, 0), depth)
    max_depth = max(depths.values(), default=0)
    return {
        'ast_graph_nodes':  graph.number_of_nodes(),
        'ast_graph_edges':  graph.number_of_edges(),
        'ast_max_depth':    max_depth,
        'ast_label_counts': dict(label_counts),
    }
 
