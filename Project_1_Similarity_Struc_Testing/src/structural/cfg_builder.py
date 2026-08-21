#importts 
import ast
import os
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple
import networkx as nx
 
        #datDa structures
@dataclass
class BasicBlock:
    block_id: int
    stmts: List[ast.stmt] = field(default_factory=list)
    label: str = ''
 
    def add_stmt(self, s: ast.stmt) -> None:
        self.stmts.append(s)
 
    def summary(self) -> str:
        if self.stmts:
            return f'B{self.block_id}: ' + '; '.join(
                ast.dump(s)[:40] for s in self.stmts[:2])
        return f'B{self.block_id}: (empty)'
 
 
        #CFG  Vvisitor
 
class CFGBuilder(ast.NodeVisitor):
 
    def __init__(self) -> None:
        self._counter = 0
        self.graph: nx.DiGraph = nx.DiGraph()
        self._entry: Optional[BasicBlock] = None
        self._exit_block: Optional[BasicBlock] = None
        self._current: Optional[BasicBlock] = None
        self._loop_exit_stack: List[BasicBlock] = []   # for break
        self._loop_cont_stack: List[BasicBlock] = []   # for continue
 
#internal helpers
    def _new_block(self, label: str = '') -> BasicBlock:
        b = BasicBlock(block_id=self._counter, label=label)
        self._counter += 1
        self.graph.add_node(b.block_id, label=b.summary(), block=b)
        return b
 
    def _add_edge(self, src: BasicBlock, dst: BasicBlock, label: str = '') -> None:
        if src is not None and dst is not None:
            self.graph.add_edge(src.block_id, dst.block_id, label=label)
    def _seal(self, block: BasicBlock) -> None:
        """Finalize block label after all stmts added."""
        self.graph.nodes[block.block_id]['label'] = block.summary()
            # intry 
    def build(self, source: str) -> nx.DiGraph:
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
#return a single node graph for unparsable code
            g = nx.DiGraph()
            g.add_node(0, label=f'SYNTAX_ERROR: {exc}')
            return g
 
        self._entry = self._new_block('ENTRY')
        self._exit_block = self._new_block('EXIT')
        self._current = self._entry
        self.visit(tree)
                #  Fall  through to exit
        if self._current is not None:
            self._add_edge(self._current, self._exit_block, 'fall')
        self._seal(self._exit_block)
        return self.graph 
# visitors 
    def visit_Module(self, node: ast.Module) -> None:
        for stmt in node.body:
            self.visit(stmt)
 
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                    #treat function def ass the single statement nn a outer block
        if self._current:
            self._current.add_stmt(node)
            self._seal(self._current)
#Reecurse in to the function body via a new sub  graph is not donehere;
         # also see analyze_functions() for per-function CFGs
 
    visit_AsyncFunctionDef = visit_FunctionDef
 
    def visit_If(self, node: ast.If) -> None:
# current_block  to     condition edge
        test_block = self._current
        if test_block:
            test_block.add_stmt(node)
            self._seal(test_block)
 
        true_block  = self._new_block('IF_TRUE')
        false_block = self._new_block('IF_FALSE')
        merge_block = self._new_block('IF_MERGE')
 
        self._add_edge(test_block, true_block,  'true')
        self._add_edge(test_block, false_block, 'false')
 
                #ttrue branch
        self._current = true_block
        for s in node.body:
            self.visit(s)
        self._add_edge(self._current, merge_block, 'merge')
 # ffalse or elif Bbranch
        self._current = false_block
        for s in node.orelse:
            self.visit(s)
        self._add_edge(self._current, merge_block, 'merge')
        self._current = merge_block
    def _visit_loop(self, node: ast.AST,
                    body: list, orelse: list) -> None:
        header = self._new_block('LOOP_HEAD')
        body_b = self._new_block('LOOP_BODY')
        after  = self._new_block('LOOP_AFTER')
 
        self._add_edge(self._current, header, 'enter_loop')
        self._add_edge(header, body_b,  'loop_true')
        self._add_edge(header, after,   'loop_false')
 
        self._loop_exit_stack.append(after)
        self._loop_cont_stack.append(header)
        self._current = body_b
        for s in body:
            self.visit(s)
        self._add_edge(self._current, header, 'back_edge')
        self._loop_exit_stack.pop()
        self._loop_cont_stack.pop()
        self._current = after
        for s in orelse:
            self.visit(s)
 
    def visit_For(self, node: ast.For) -> None:
        self._visit_loop(node, node.body, node.orelse)
 
    def visit_While(self, node: ast.While) -> None:
        self._visit_loop(node, node.body, node.orelse)
 
    def visit_Try(self, node: ast.Try) -> None:
        try_block    = self._new_block('TRY')
        except_block = self._new_block('EXCEPT')
        else_block   = self._new_block('TRY_ELSE')
        finally_blk  = self._new_block('FINALLY')
 
        self._add_edge(self._current, try_block, 'try')
        self._current = try_block
        for s in node.body:
            self.visit(s)
        self._add_edge(self._current, else_block,   'try_ok')
        self._add_edge(self._current, except_block, 'exception')
 
        #except handlers
        for handler in node.handlers:
            self._current = except_block
            for s in handler.body:
                self.visit(s)
        self._add_edge(self._current, finally_blk, 'handled')
 
        #alse clause
        self._current = else_block
        for s in node.orelse:
            self.visit(s)
        self._add_edge(self._current, finally_blk, 'else')
 
        # F inally
        self._current = finally_blk
        for s in node.finalbody if hasattr(node, 'finalbody') else []:
            self.visit(s)
 
    def visit_Return(self, node: ast.Return) -> None:
        if self._current:
            self._current.add_stmt(node)
            self._add_edge(self._current, self._exit_block, 'return')
        self._current = self._new_block('DEAD')   # unreachable continuation
 
    def visit_Break(self, node: ast.Break) -> None:
        if self._loop_exit_stack and self._current:
            self._add_edge(self._current, self._loop_exit_stack[-1], 'break')
        self._current = self._new_block('DEAD')
 
    def visit_Continue(self, node: ast.Continue) -> None:
        if self._loop_cont_stack and self._current:
            self._add_edge(self._current, self._loop_cont_stack[-1], 'continue')
        self._current = self._new_block('DEAD')
 
    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(node, ast.stmt) and self._current:
            self._current.add_stmt(node)
            self._seal(self._current)
        else:
            super().generic_visit(node)
 
 
                #.per function CFGs 
 
def build_cfg(source: str) -> nx.DiGraph:
    """Build module-level CFG from source string."""
    return CFGBuilder().build(source)
def build_function_cfgs(source: str) -> dict:
    """
    Return a dict {func_name: DiGraph} for every top-level function definition.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    cfgs = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_src = ast.get_source_segment(source, node) or \
                       textwrap.dedent(ast.unparse(node))
            cfgs[node.name] = CFGBuilder().build(func_src)
    return cfgs
 
 
#.                 persistence 
 
def save_cfg(graph: nx.DiGraph, out_path: str) -> None:
    """Save CFG as GraphML, stripping non-serializable node attributes."""
  
    safe_g = nx.DiGraph()
    for n, data in graph.nodes(data=True):
        safe_g.add_node(n, label=str(data.get('label', n)))
    for u, v, data in graph.edges(data=True):
        safe_g.add_edge(u, v, label=str(data.get('label', '')))
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    nx.write_graphml(safe_g, out_path)
 
 
def load_cfg(path: str) -> nx.DiGraph:
    return nx.read_graphml(path)
 
