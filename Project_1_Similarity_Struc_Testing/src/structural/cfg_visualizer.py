




import ast
import io
import os
import textwrap
import tokenize
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
            #   directory
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
INPUT_DIR = str(PROJECT_ROOT / "data/results/cfg")
OUTPUT_DIR = str(PROJECT_ROOT / "reports/cfg")
MANIFEST_CSV = str(PROJECT_ROOT / "data/processed/preprocessing_manifest.csv")
THEME = {
    'ENTRY':        '#2ECC71',  
    'EXIT':         '#E74C3C',  
    'IF_TRUE':      '#3498DB', 
    'IF_FALSE':     '#E67E22',  
    'IF_MERGE':     '#9B59B6',  
    'LOOP_HEAD':    '#1ABC9C',  
    'LOOP_BODY':    '#2980B9',  
    'LOOP_AFTER':   '#8E44AD', 
    'TRY':          '#F39C12',   
    'EXCEPT':       '#C0392B', 
    'TRY_ELSE':     '#27AE60',  
    'FINALLY':      '#D35400',   
    'DEAD':         '#BDC3C7',   
    'DEFAULT':      '#5DADE2',   
}

EDGE_COLORS = {
    'true':       '#2ECC71',
    'false':      '#E74C3C',
    'back_edge':  '#E67E22',
    'exception':  '#C0392B',
    'return':     '#9B59B6',
    'break':      '#F39C12',
    'continue':   '#1ABC9C',
    'merge':      '#85929E',
    'fall':       '#AEB6BF',
    'try':        '#F39C12',
    'try_ok':     '#2ECC71',
    'handled':    '#2980B9',
    'else':       '#8E44AD',
    'enter_loop': '#1ABC9C',
    'loop_true':  '#2ECC71',
    'loop_false': '#E74C3C',
    'DEFAULT':    '#7F8C8D',
}

#cfg builderr
@dataclass
class BasicBlock:
    block_id: int
    stmts: List[ast.stmt] = field(default_factory=list)
    label: str = ''

    def add_stmt(self, s: ast.stmt) -> None:
        self.stmts.append(s)

    def short_label(self) -> str:
        if not self.stmts:
            return f'B{self.block_id}\n(empty)'
        lines = []
        for stmt in self.stmts[:2]:
            try:
                src = ast.unparse(stmt)
            except Exception:
                src = type(stmt).__name__
            lines.append(textwrap.shorten(src, width=28, placeholder='…'))
        suffix = f' +{len(self.stmts)-2}' if len(self.stmts) > 2 else ''
        return f'B{self.block_id}\n' + '\n'.join(lines) + suffix
class CFGBuilder(ast.NodeVisitor):
    def __init__(self) -> None:
        self._counter = 0
        self.graph: nx.DiGraph = nx.DiGraph()
        self._entry: Optional[BasicBlock] = None
        self._exit_block: Optional[BasicBlock] = None
        self._current: Optional[BasicBlock] = None
        self._loop_exit_stack: List[BasicBlock] = []
        self._loop_cont_stack: List[BasicBlock] = []

    def _new_block(self, label: str = '') -> BasicBlock:
        b = BasicBlock(block_id=self._counter, label=label)
        self._counter += 1
        self.graph.add_node(b.block_id,
                            label=b.short_label(),
                            block_type=label or 'DEFAULT',
                            block=b)
        return b

    def _add_edge(self, src: Optional[BasicBlock],
                 dst: Optional[BasicBlock], label: str = '') -> None:
        if src is not None and dst is not None:
            self.graph.add_edge(src.block_id, dst.block_id, label=label)
    def _seal(self, block: BasicBlock) -> None:
        if block.block_id in self.graph.nodes:
            self.graph.nodes[block.block_id]['label'] = block.short_label()
    def build(self, source: str) -> nx.DiGraph:
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            g = nx.DiGraph()
            g.add_node(0, label=f'SYNTAX_ERROR\n{exc}',
                       block_type='DEFAULT', block=None)
            return g
        self._entry = self._new_block('ENTRY')
        self._exit_block = self._new_block('EXIT')
        self._current = self._entry
        self.visit(tree)
        if self._current is not None:
            self._add_edge(self._current, self._exit_block, 'fall')
        self._seal(self._exit_block)
        return self.graph

    def visit_Module(self, node: ast.Module) -> None:
        for stmt in node.body:
            self.visit(stmt)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self._current:
            self._current.add_stmt(node)
            self._seal(self._current)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_If(self, node: ast.If) -> None:
        test_block = self._current
        if test_block:
            test_block.add_stmt(node)
            self._seal(test_block)
        true_block  = self._new_block('IF_TRUE')
        false_block = self._new_block('IF_FALSE')
        merge_block = self._new_block('IF_MERGE')
        self._add_edge(test_block, true_block,  'true')
        self._add_edge(test_block, false_block, 'false')
        self._current = true_block
        for s in node.body:
            self.visit(s)
        self._add_edge(self._current, merge_block, 'merge')
        self._current = false_block
        for s in node.orelse:
            self.visit(s)
        self._add_edge(self._current, merge_block, 'merge')
        self._current = merge_block

    def _visit_loop(self, body: list, orelse: list) -> None:
        header = self._new_block('LOOP_HEAD')
        body_b = self._new_block('LOOP_BODY')
        after  = self._new_block('LOOP_AFTER')
        self._add_edge(self._current, header, 'enter_loop')
        self._add_edge(header, body_b, 'loop_true')
        self._add_edge(header, after,  'loop_false')
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
        self._visit_loop(node.body, node.orelse)

    def visit_While(self, node: ast.While) -> None:
        self._visit_loop(node.body, node.orelse)

    def visit_Try(self, node: ast.Try) -> None:
        try_b    = self._new_block('TRY')
        except_b = self._new_block('EXCEPT')
        else_b   = self._new_block('TRY_ELSE')
        finally_b = self._new_block('FINALLY')
        self._add_edge(self._current, try_b, 'try')
        self._current = try_b
        for s in node.body:
            self.visit(s)
        self._add_edge(self._current, else_b,   'try_ok')
        self._add_edge(self._current, except_b, 'exception')
        for handler in node.handlers:
            self._current = except_b
            for s in handler.body:
                self.visit(s)
        self._add_edge(self._current, finally_b, 'handled')
        self._current = else_b
        for s in node.orelse:
            self.visit(s)
        self._add_edge(self._current, finally_b, 'else')
        self._current = finally_b
        for s in getattr(node, 'finalbody', []):
            self.visit(s)

    def visit_Return(self, node: ast.Return) -> None:
        if self._current:
            self._current.add_stmt(node)
            self._add_edge(self._current, self._exit_block, 'return')
        self._current = self._new_block('DEAD')

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
def build_cfg_from_source(source: str) -> nx.DiGraph:
    return CFGBuilder().build(source)
def build_cfg_from_graphml(path: str) -> nx.DiGraph:
    return nx.read_graphml(path)

                            # layout helperss

def _hierarchical_layout(G: nx.DiGraph, root: Optional[int] = None) -> Dict[int, Tuple[float, float]]:
    if G.number_of_nodes() == 0:
        return {}

    if root is None:
        entry_candidates = [n for n, d in G.nodes(data=True)
                            if 'ENTRY' in str(d.get('block_type', ''))
                            or 'ENTRY' in str(d.get('label', ''))]
        if entry_candidates:
            root = entry_candidates[0]
        else:
            root = min(G.nodes(), key=lambda n: (G.in_degree(n), n))

    levels: Dict[int, int] = {root: 0}
    queue = [root]
    visited = {root}
    while queue:
        node = queue.pop(0)
        for succ in G.successors(node):
            if succ not in visited:
                levels[succ] = levels[node] + 1
                visited.add(succ)
                queue.append(succ)

    max_level = max(levels.values(), default=0)
    for n in G.nodes():
        if n not in levels:
            levels[n] = max_level + 1

    from collections import defaultdict
    level_nodes: Dict[int, List[int]] = defaultdict(list)
    for n, lv in levels.items():
        level_nodes[lv].append(n)

    pos: Dict[int, Tuple[float, float]] = {}
    for lv, nodes in level_nodes.items():
        n_nodes = len(nodes)
        x_start = -(n_nodes - 1) / 2.0
        for i, node in enumerate(sorted(nodes)):
            pos[node] = (x_start + i, -lv * 1.8)

    return pos


def _node_colors(G: nx.DiGraph) -> List[str]:
    colors = []
    for n, data in G.nodes(data=True):
        block_type = str(data.get('block_type', data.get('label', '')))
        matched = 'DEFAULT'
        for key in THEME:
            if key != 'DEFAULT' and key in block_type.upper():
                matched = key
                break
        colors.append(THEME[matched])
    return colors


def _edge_colors_list(G: nx.DiGraph) -> List[str]:
    colors = []
    for u, v, data in G.edges(data=True):
        lbl = str(data.get('label', '')).lower()
        matched = EDGE_COLORS.get(lbl, EDGE_COLORS['DEFAULT'])
        colors.append(matched)
    return colors


def _wrap_label(text: str, width: int = 22) -> str:
    lines = text.split('\n')
    result = []
    for line in lines:
        if len(line) > width:
            result.append(textwrap.shorten(line, width=width, placeholder='…'))
        else:
            result.append(line)
    return '\n'.join(result)



                                            #single  cfg plot
def plot_cfg(
    G: nx.DiGraph,
    title: str = '',
    ax: Optional[plt.Axes] = None,
    figsize: Tuple[float, float] = (10, 9),
    show_edge_labels: bool = True,
    metrics: Optional[Dict] = None,
) -> plt.Figure:
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor('#FAFAFA')
    else:
        fig = ax.get_figure()

    ax.set_facecolor('#F8F9FA')

    if G.number_of_nodes() == 0:
        ax.text(0.5, 0.5, 'Empty graph', ha='center', va='center',
                transform=ax.transAxes, fontsize=12, color='grey')
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
        return fig

    pos = _hierarchical_layout(G)
    if not pos:
        pos = nx.spring_layout(G, seed=42, k=2.0)

    node_colors   = _node_colors(G)
    labels = {n: _wrap_label(str(data.get('label', f'B{n}'))) for n, data in G.nodes(data=True)}
    node_sizes = [max(800, min(3500, len(labels[n]) * 55)) for n in G.nodes()]

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes, node_shape='s', alpha=0.92, linewidths=1.5, edgecolors='#2C3E50')
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=6.5, font_color='#1A1A2E', font_family='monospace', font_weight='bold')

    back_edges   = [(u, v) for u, v, d in G.edges(data=True) if 'back' in str(d.get('label', '')).lower()]
    normal_edges = [(u, v) for u, v in G.edges() if (u, v) not in back_edges]

    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, ax=ax,
                           edge_color=[EDGE_COLORS.get(str(G[u][v].get('label', '')).lower(), EDGE_COLORS['DEFAULT']) for u, v in normal_edges],
                           arrows=True, arrowsize=18, arrowstyle='-|>', width=1.6, alpha=0.85, min_source_margin=22, min_target_margin=22)

    if back_edges:
        nx.draw_networkx_edges(G, pos, edgelist=back_edges, ax=ax, edge_color=[EDGE_COLORS['back_edge']] * len(back_edges),
                               arrows=True, arrowsize=18, arrowstyle='-|>', width=2.0, alpha=0.85, connectionstyle='arc3,rad=0.35', style='dashed', min_source_margin=22, min_target_margin=22)

    if show_edge_labels and G.number_of_edges() <= 30:
        edge_labels = {(u, v): str(d.get('label', '')) for u, v, d in G.edges(data=True) if d.get('label', '')}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=6, font_color='#2C3E50',
                                     bbox=dict(boxstyle='round,pad=0.15', fc='white', alpha=0.65, ec='none'), label_pos=0.38)

    if metrics:
        E = G.number_of_edges()
        N = G.number_of_nodes()
        P = nx.number_weakly_connected_components(G)
        M = E - N + 2 * P
        metrics_text = f'N={N}  E={E}  P={P}\nM = E−N+2P = {M}\nDepth = {_graph_depth(G)}'
        ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes, fontsize=7.5, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#EBF5FB', edgecolor='#2E86C1', alpha=0.9))

    legend_items = [
        mpatches.Patch(color=THEME['ENTRY'],     label='Entry'),
        mpatches.Patch(color=THEME['EXIT'],      label='Exit'),
        mpatches.Patch(color=THEME['IF_TRUE'],   label='If-True / Body'),
        mpatches.Patch(color=THEME['IF_FALSE'],  label='If-False'),
        mpatches.Patch(color=THEME['IF_MERGE'],  label='Merge'),
        mpatches.Patch(color=THEME['LOOP_HEAD'], label='Loop Head'),
        mpatches.Patch(color=THEME['TRY'],       label='Try'),
        mpatches.Patch(color=THEME['EXCEPT'],    label='Except'),
        mpatches.Patch(color=THEME['DEAD'],      label='Dead (unreachable)'),
    ]
    ax.legend(handles=legend_items, loc='lower right', fontsize=6.5, framealpha=0.88, title='Block Types', title_fontsize=7, ncol=1, borderpad=0.6)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=12, color='#1A1A2E')
    ax.axis('off')

    if standalone:
        fig.tight_layout()
    return fig


def _graph_depth(G: nx.DiGraph) -> int:
    if G.number_of_nodes() == 0:
        return 0
    sources = [n for n, d in G.in_degree() if d == 0]
    if not sources:
        return 0
    max_d = 0
    for s in sources:
        try:
            lengths = nx.single_source_shortest_path_length(G, s)
            max_d = max(max_d, max(lengths.values(), default=0))
        except Exception:
            pass
    return max_d



# Sside by side comparison plort


def plot_cfg_comparison(ref_graph: nx.DiGraph, llm_graph: nx.DiGraph, scenario: str, task_id: str, out_path: str) -> None:
    def _metrics(G: nx.DiGraph) -> Dict:
        E = G.number_of_edges()
        N = G.number_of_nodes()
        P = max(1, nx.number_weakly_connected_components(G))
        return dict(N=N, E=E, P=P, M=E - N + 2 * P, depth=_graph_depth(G))

    rm = _metrics(ref_graph)
    lm = _metrics(llm_graph)

    fig = plt.figure(figsize=(20, 10), facecolor='#F4F6F7')
    fig.suptitle(f'CFG Comparison — Scenario: {scenario}   Task: {task_id}', fontsize=14, fontweight='bold', color='#1A1A2E', y=0.98)

    delta_M = lm['M'] - rm['M']
    delta_N = lm['N'] - rm['N']
    delta_E = lm['E'] - rm['E']
    banner = f'ΔM(Cyclomatic) = {delta_M:+d}   ΔN(Nodes) = {delta_N:+d}   ΔE(Edges) = {delta_E:+d}   ΔDepth = {lm["depth"] - rm["depth"]:+d}'
    fig.text(0.5, 0.94, banner, ha='center', fontsize=9, color='#2C3E50', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#D6EAF8', edgecolor='#2E86C1', alpha=0.9))

    ax_ref = fig.add_subplot(1, 2, 1)
    ax_llm = fig.add_subplot(1, 2, 2)

    plot_cfg(ref_graph, title=f'Reference   (M={rm["M"]}  N={rm["N"]}  E={rm["E"]}  depth={rm["depth"]})', ax=ax_ref, metrics=rm)
    plot_cfg(llm_graph, title=f'LLM-Generated   (M={lm["M"]}  N={lm["N"]}  E={lm["E"]}  depth={lm["depth"]})', ax=ax_llm, metrics=lm)

    fig.subplots_adjust(top=0.89, wspace=0.06)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'   save {out_path}')
#gallerry
def plot_cfg_gallery(pairs: List[Tuple[str, str, nx.DiGraph, nx.DiGraph]], out_path: str, cols: int = 4) -> None:
    if not pairs:
        return

    n_pairs = len(pairs)
    n_cols   = min(cols, n_pairs) * 2
    n_rows   = (n_pairs + cols - 1) // cols

    fig_w = n_cols * 5.5
    fig_h = n_rows * 6.0

    fig = plt.figure(figsize=(fig_w, fig_h), facecolor='#F0F3F4')
    fig.suptitle('CFG Gallery — All Scenarios', fontsize=16, fontweight='bold', color='#1A1A2E', y=1.01)

    for idx, (scenario, task_id, ref_g, llm_g) in enumerate(pairs):
        row = idx // cols
        col = idx  % cols

        ax_r = fig.add_subplot(n_rows, n_cols, row * n_cols + col * 2 + 1)
        ax_l = fig.add_subplot(n_rows, n_cols, row * n_cols + col * 2 + 2)

        short_s = textwrap.shorten(scenario, 22, placeholder='…')
        plot_cfg(ref_g, title=f'{short_s}/{task_id}\nREF', ax=ax_r, show_edge_labels=False)
        plot_cfg(llm_g, title=f'{short_s}/{task_id}\nLLM', ax=ax_l, show_edge_labels=False)

        if col < cols - 1:
            x_sep = (col * 2 + 2) / n_cols
            fig.add_artist(plt.Line2D([x_sep, x_sep], [row / n_rows, (row + 1) / n_rows], transform=fig.transFigure, color='#BFC9CA', lw=0.8))

    fig.tight_layout(pad=1.5, h_pad=2.5, w_pad=0.5)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f'   [GALLERY] {out_path}')


def _resolve_graphml_path(cfg_dir: str, scenario: str, task_id: str, suffix: str) -> Optional[str]:
    safe_s = scenario.replace(' ', '_').replace('&', 'and')
    candidates = [
        os.path.join(cfg_dir, scenario,  f'{task_id}_{suffix}_cfg.graphml'),
        os.path.join(cfg_dir, safe_s,    f'{task_id}_{suffix}_cfg.graphml'),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None
                #maIN EXECUTION Rout

def visualize_graphml_files(input_base_dir: str, output_base_dir: str, manifest_csv_path: str):
    

    
    if not os.path.exists(manifest_csv_path):
        print(f"[ERROR] Manifest file not found at: {manifest_csv_path}")
        return

    manifest = pd.read_csv(manifest_csv_path)
    manifest = manifest[manifest['status'] == 'ok'].drop_duplicates(subset=['scenario', 'task_id']).reset_index(drop=True)

    if manifest.empty:
        print("no valid tasks found in the preprocessing manifest")
        return

    print(f"{len(manifest)} structural tasks to process from manifest")
    gallery_pairs = []

    for _, row in manifest.iterrows():
        scenario = row['scenario']
        task_id  = str(row['task_id'])

        ref_gml = _resolve_graphml_path(input_base_dir, scenario, task_id, 'ref')
        llm_gml = _resolve_graphml_path(input_base_dir, scenario, task_id, 'llm')

        if ref_gml is None or llm_gml is None:
            continue

        print(f"   Visualizing {scenario} / {task_id}")
        ref_g = build_cfg_from_graphml(ref_gml)
        llm_g = build_cfg_from_graphml(llm_gml)

        safe_s  = scenario.replace(' ', '_').replace('&', 'and')
        ref_out = os.path.join(output_base_dir, safe_s, f'{task_id}_ref_cfg.png')
        llm_out = os.path.join(output_base_dir, safe_s, f'{task_id}_llm_cfg.png')
        cmp_out = os.path.join(output_base_dir, safe_s, f'{task_id}_llm&ref_cfg.png')

        Path(ref_out).parent.mkdir(parents=True, exist_ok=True)

        fig = plot_cfg(ref_g, title=f'REF — {scenario} / {task_id}')
        fig.savefig(ref_out, dpi=150, bbox_inches='tight')
        plt.close(fig)

        fig = plot_cfg(llm_g, title=f'LLM — {scenario} / {task_id}')
        fig.savefig(llm_out, dpi=150, bbox_inches='tight')
        plt.close(fig)

        plot_cfg_comparison(ref_g, llm_g, scenario, task_id, cmp_out)
        gallery_pairs.append((scenario, task_id, ref_g, llm_g))

    if gallery_pairs:
        plot_cfg_gallery(gallery_pairs, out_path=os.path.join(output_base_dir, 'cfg_gallery.png'))


if __name__ == "__main__":
    print(f"[INFO] Running visualization from base path config loops...")
    visualize_graphml_files(INPUT_DIR, OUTPUT_DIR, MANIFEST_CSV)
    print("\n[PHASE 3b] Advanced CFG Visualization complete.")