""" run with: streamlit run simple_dashboard.py """
# iimports
import os
import ast
import textwrap
import tempfile
from pathlib import Path
from collections import Counter
from functools import lru_cache
 
import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

# Check if running inside the Docker container env
if os.getenv("PYTHONUNBUFFERED") == "1":
    print("\n" + "═"*60)
    print("To open dashboard UI go to http://localhost:8501")
    print("═"*60 + "\n")
 
#page confige
st.set_page_config(
    page_title="LLM Generated Code Analysis via Graph Matching & CFG",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
#    paths
ROOT         = Path(__file__).parent
DATA         = ROOT / "data"
PROCESSED    = DATA / "processed"
RESULTS      = DATA / "results"
CFG_DIR      = RESULTS / "cfg"
MANIFEST_CSV = PROCESSED / "preprocessing_manifest.csv"
STRUCT_CSV   = RESULTS   / "structural_metrics.csv"
SIM_CSV      = RESULTS   / "similarity_scores.csv"
TEST_CSV     = RESULTS   / "test_results.csv"
 
# ccolour Palette
C = dict(
    green="#2ECC71", red="#E74C3C", blue="#3498DB",
    orange="#E67E22", purple="#9B59B6", teal="#1ABC9C",
    yellow="#F39C12", accent="#4F6BED",
    bg="#0F1117", card="#1E2139", border="#2D3047",
    text="#E2E8F0", muted="#64748B",
)
 
CFG_COLORS = {
    "ENTRY":"#2ECC71","EXIT":"#E74C3C","IF_TRUE":"#3498DB",
    "IF_FALSE":"#E67E22","IF_MERGE":"#9B59B6","LOOP_HEAD":"#1ABC9C",
    "LOOP_BODY":"#2980B9","LOOP_AFTER":"#8E44AD","TRY":"#F39C12",
    "EXCEPT":"#C0392B","TRY_ELSE":"#27AE60","FINALLY":"#D35400",
    "DEAD":"#636E72","DEFAULT":"#5DADE2",
}
 
EDGE_COLORS = {
    "true":"#2ECC71","false":"#E74C3C","back_edge":"#E67E22",
    "exception":"#C0392B","return":"#9B59B6","break":"#F39C12",
    "continue":"#1ABC9C","merge":"#85929E","fall":"#BDC3C7",
    "try":"#F39C12","try_ok":"#2ECC71","handled":"#2980B9",
    "else":"#8E44AD","enter_loop":"#1ABC9C",
    "loop_true":"#2ECC71","loop_false":"#E74C3C",
}
 
TPL   = "plotly_dark"
PAPER = "#0F1117"
PLOT  = "#1E2139"
GRID  = "#2D3047"
FONT  = "#E2E8F0"
 
#gllobal CSS
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.main .block-container {{ padding-top:1.2rem; max-width:1380px; }}
section[data-testid="stSidebar"] {{ background:{C['bg']}; }}
h2.section-hdr {{
    font-size:.75rem; font-weight:600; color:{C['accent']};
    text-transform:uppercase; letter-spacing:.1em;
    border-bottom:1px solid {C['border']}; padding-bottom:.35rem;
    margin:2rem 0 .9rem;
}}
.mcard {{
    background:{C['card']}; border:1px solid {C['border']};
    border-radius:10px; padding:1rem 1.2rem; text-align:center;
}}
.mcard .lbl {{ font-size:.68rem; color:{C['muted']};
    text-transform:uppercase; letter-spacing:.08em; margin-bottom:.2rem; }}
.mcard .val {{ font-size:1.75rem; font-weight:700; line-height:1.1; }}
.sep {{ border:none; border-top:1px solid {C['border']}; margin:2rem 0; }}
.legend-row {{ display:flex; gap:1rem; flex-wrap:wrap;
    background:{C['card']}; border:1px solid {C['border']};
    border-radius:8px; padding:.55rem .9rem; font-size:.72rem;
    color:{C['muted']}; margin-bottom:.7rem; align-items:center; }}
.dot {{ width:11px; height:11px; border-radius:50%; display:inline-block;
    margin-right:.3rem; vertical-align:middle; }}
</style>
""", unsafe_allow_html=True)
 
# dataa loaders that are catched
 
@lru_cache(maxsize=1)
def manifest() -> pd.DataFrame:
    if not MANIFEST_CSV.exists():
        return pd.DataFrame()
    df = pd.read_csv(MANIFEST_CSV)
    df = df[df["status"] == "ok"].drop_duplicates(subset=["scenario","task_id"])
    df["task_id"] = df["task_id"].astype(str)
    return df.reset_index(drop=True)
 
@lru_cache(maxsize=1)
def sim_df() -> pd.DataFrame:
    if not SIM_CSV.exists():
        return pd.DataFrame()
    df = pd.read_csv(SIM_CSV)
    df["task_id"] = df["task_id"].astype(str)
    return df
 
@lru_cache(maxsize=1)
def struct_df() -> pd.DataFrame:
    if not STRUCT_CSV.exists():
        return pd.DataFrame()
    df = pd.read_csv(STRUCT_CSV)
    df["task_id"] = df["task_id"].astype(str)
    return df
 
@lru_cache(maxsize=1)
def test_df() -> pd.DataFrame:
    if not TEST_CSV.exists():
        return pd.DataFrame()
    df = pd.read_csv(TEST_CSV)
    df["task_id"] = df["task_id"].astype(str)
    return df
 
def merged() -> pd.DataFrame:
    s = sim_df()
    if s.empty:
        return pd.DataFrame()
    d = s.copy()
    if not struct_df().empty:
        d = d.merge(struct_df(), on=["scenario","task_id"], how="left")
    if not test_df().empty:
        d = d.merge(test_df(),   on=["scenario","task_id"], how="left")
    return d
 
def find_graphml(scenario: str, task_id: str, kind: str) -> Path | None:
    safe = scenario.replace(" ","_").replace("&","and")
    for folder in [CFG_DIR / scenario, CFG_DIR / safe]:
        for tid in [task_id, str(int(task_id)) if task_id.isdigit() else task_id]:
            p = folder / f"{tid}_{kind}_cfg.graphml"
            if p.exists():
                return p
    return None
 
def load_graph(scenario: str, task_id: str, kind: str) -> nx.DiGraph | None:
    p = find_graphml(scenario, task_id, kind)
    if p is None:
        return None
    try:
        return nx.read_graphml(str(p))
    except Exception:
        return None
 
# Helperes
def section(title: str) -> None:
    st.markdown(f'<h2 class="section-hdr">{title}</h2>', unsafe_allow_html=True)
 
def divider() -> None:
    st.markdown('<hr class="sep">', unsafe_allow_html=True)
 
def metric_card(label: str, value: str, color: str) -> str:
    return (f'<div class="mcard">'
            f'<div class="lbl">{label}</div>'
            f'<div class="val" style="color:{color}">{value}</div>'
            f'</div>')
 
def _base(title: str = "", height: int = 380) -> dict:
    return dict(
        template=TPL, paper_bgcolor=PAPER, plot_bgcolor=PLOT,
        font=dict(family="Inter", color=FONT, size=12),
        margin=dict(l=42, r=18, t=46 if title else 18, b=40),
        height=height,
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        title=dict(text=title, font=dict(size=14)) if title else {},
    )
 
def infer_btype(label: str) -> str:
    up = label.upper()
    for k in ["ENTRY","EXIT","IF_MERGE","IF_TRUE","IF_FALSE",
              "LOOP_HEAD","LOOP_BODY","LOOP_AFTER",
              "TRY_ELSE","FINALLY","EXCEPT","TRY","DEAD"]:
        if k in up:
            return k
    return "DEFAULT"
 
def pyvis_html(G: nx.DiGraph, height: int = 500,
               node_colors: dict | None = None) -> str:
    net = Network(height=f"{height}px", width="100%", directed=True,
                  bgcolor="#1A1D2E", font_color=FONT)
    net.set_options("""{
      "nodes":{"font":{"size":10,"face":"JetBrains Mono","color":"#E2E8F0"},
               "shape":"box","borderWidth":2,"shadow":{"enabled":true}},
      "edges":{"arrows":{"to":{"enabled":true,"scaleFactor":0.65}},
               "font":{"size":8,"color":"#94A3B8"},
               "smooth":{"type":"cubicBezier","forceDirection":"vertical","roundness":0.4}},
      "layout":{"hierarchical":{"enabled":true,"levelSeparation":110,
                "nodeSpacing":140,"direction":"UD","sortMethod":"directed"}},
      "physics":{"enabled":false},
      "interaction":{"hover":true,"zoomView":true,"dragView":true,
                     "navigationButtons":true}
    }""")
    for nid, data in G.nodes(data=True):
        lbl  = str(data.get("label", str(nid)))
        bt   = infer_btype(lbl)
        col  = (node_colors or {}).get(str(nid),
               CFG_COLORS.get(bt, CFG_COLORS["DEFAULT"]))
        tip  = f"<b>Block {nid}</b><br>Type: {bt}<br><code>{lbl[:180]}</code>"
        net.add_node(str(nid), label="\n".join(lbl.split("\n")[:3]),
                     title=tip,
                     color={"background":col,"border":"#1A1D2E",
                            "highlight":{"background":"#F39C12","border":"#E67E22"}},
                     size=20)
    for u, v, d in G.edges(data=True):
        el  = str(d.get("label",""))
        ec  = EDGE_COLORS.get(el.lower(), "#7F8C8D")
        net.add_edge(str(u), str(v), label=el, color=ec,
                     dashes=el in ("back_edge","fall","merge"),
                     title=f"<b>{el}</b>", arrows="to")
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False,
                                     mode="w", encoding="utf-8") as f:
        tmp = f.name
    net.save_graph(tmp)
    html = open(tmp, encoding="utf-8").read()
    os.unlink(tmp)
    return html
 
def cfg_metrics(G: nx.DiGraph) -> dict:
    if G is None or G.number_of_nodes() == 0:
        return dict(N=0, E=0, M=0, depth=0, density=0.0, is_dag="—")
    E = G.number_of_edges()
    N = G.number_of_nodes()
    P = max(1, nx.number_weakly_connected_components(G))
    srcs  = [n for n,d in G.in_degree() if d == 0]
    depth = 0
    for s in srcs:
        try:
            depth = max(depth, max(nx.single_source_shortest_path_length(G,s).values(),default=0))
        except Exception:
            pass
    return dict(N=N, E=E, M=E-N+2*P, depth=depth,
                density=round(nx.density(G),4),
                is_dag="✓" if nx.is_directed_acyclic_graph(G) else "✗")
 
def diff_colors(ref_g: nx.DiGraph, llm_g: nx.DiGraph):
    """Return (ref_node_colors, llm_node_colors) for structural diff."""
    def ctr(G):
        return Counter(infer_btype(str(d.get("label","")))
                       for _,d in G.nodes(data=True))
    rc, lc = ctr(ref_g), ctr(llm_g)
    matched = Counter({bt: min(rc.get(bt,0), lc.get(bt,0))
                       for bt in set(rc)|set(lc)})
    def assign(G, miss_col):
        used = Counter()
        out = {}
        for nid, d in G.nodes(data=True):
            bt = infer_btype(str(d.get("label","")))
            if used[bt] < matched[bt]:
                out[str(nid)] = C["green"];  used[bt] += 1
            else:
                out[str(nid)] = miss_col
        return out
    return assign(ref_g, C["red"]), assign(llm_g, C["blue"])
 
#hEADer
 
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1E2139,#252840);
            border:1px solid {C['border']};border-radius:12px;
            padding:1.3rem 1.8rem;margin-bottom:1.4rem">
  <div style="font-size:1.55rem;font-weight:700;color:{C['text']}">
    Structural &amp; Similarity Analysis and Testing of LLM-Generated &amp; Reference Programs
  </div>
  <div style="font-size:.82rem;color:{C['muted']};margin-top:.3rem">
    Structural complexity, similarity analysis and testing of AI-generated vs reference Python code using Control Flow Graphs, Abstract Syntax Tree, CodeBERT, structural metrices, and graph matching
  </div>
</div>""", unsafe_allow_html=True)
 
#   GlobaL  overview kards
sd = sim_df(); strd = struct_df(); td = test_df(); man = manifest()
 
# Updated to 6 columns to accommodate LLM Pass Rate and Ref Pass Rate side-by-side
c1, c2, c3, c4, c5, c6 = st.columns(6)

llm_pass_mean = td[td['variant'] == 'llm']['pass_rate'].mean() if not td.empty and 'pass_rate' in td else float('nan')
ref_pass_mean = td[td['variant'].str.startswith('ref')]['pass_rate'].mean() if not td.empty and 'pass_rate' in td else float('nan')

cards = [
    ("Scenarios",      str(man["scenario"].nunique()) if not man.empty else "—", C["accent"]),
    ("Tasks",          str(len(man))                  if not man.empty else "—", C["blue"]),
    ("Avg S_final",    f"{sd['s_final'].mean():.3f}"  if not sd.empty and "s_final" in sd else "—", C["teal"]),
    ("Avg Complexity", f"{strd['llm_cfg_cyclomatic_complexity'].mean():.1f}"
                       if not strd.empty and "llm_cfg_cyclomatic_complexity" in strd else "—", C["purple"]),
    ("LLM Pass Rate",  f"{llm_pass_mean:.1%}" if not np.isnan(llm_pass_mean) else "—", C["blue"]),
    ("Ref Pass Rate",  f"{ref_pass_mean:.1%}" if not np.isnan(ref_pass_mean) else "—", C["green"]),
]
for col, (lbl, val, color) in zip([c1, c2, c3, c4, c5, c6], cards):
    col.markdown(metric_card(lbl, val, color), unsafe_allow_html=True)
 
        # cfg Viewer
divider()
section("① Control Flow Graph Viewer")
 
scenarios = sorted(man["scenario"].unique().tolist()) if not man.empty else []
if not scenarios:
    st.warning("No processed scenarios found. Run `python run_pipeline.py` first.")
else:
    col_sc, col_tid, col_mode = st.columns([2, 1, 1])
    with col_sc:
        sel_sc   = st.selectbox("Scenario", scenarios, key="cfg_sc",
                                label_visibility="collapsed")
    with col_tid:
        tasks    = sorted(man[man["scenario"]==sel_sc]["task_id"].tolist())
        sel_task = st.selectbox("Task ID", tasks, key="cfg_tid",
                                label_visibility="collapsed")
    with col_mode:
        cfg_mode = st.radio("View", ["Side by Side", "Diff"], key="cfg_mode",
                            horizontal=True, label_visibility="collapsed")
 
    ref_g = load_graph(sel_sc, sel_task, "ref")
    llm_g = load_graph(sel_sc, sel_task, "llm")
 
                        #     Metrics    strip
    rm = cfg_metrics(ref_g)
    lm = cfg_metrics(llm_g)
    mc = st.columns(8)
    metric_pairs = [
        ("M (REF)", str(rm["M"]),    C["green"]),
        ("M (LLM)", str(lm["M"]),    C["blue"]),
        ("N (REF)", str(rm["N"]),    C["green"]),
        ("N (LLM)", str(lm["N"]),    C["blue"]),
        ("E (REF)", str(rm["E"]),    C["green"]),
        ("E (LLM)", str(lm["E"]),    C["blue"]),
        ("Depth REF", str(rm["depth"]), C["green"]),
        ("Depth LLM", str(lm["depth"]), C["blue"]),
    ]
    for col, (lbl, val, color) in zip(mc, metric_pairs):
        col.markdown(metric_card(lbl, val, color), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
                                    #collapsible coode panell
    if "show_code" not in st.session_state:
        st.session_state.show_code = False
 
    _btn_label = "Hide Code ▲" if st.session_state.show_code else "Show Code ▼"
    if st.button(_btn_label, key="code_toggle"):
        st.session_state.show_code = not st.session_state.show_code
        st.rerun()
 
    if st.session_state.show_code:
        def _load_src(scenario, task_id, col):
            """Read processed source file for the selected scenario/task."""
            row = manifest()[
                (manifest()["scenario"] == scenario) &
                (manifest()["task_id"] == str(task_id))
            ]
            if row.empty:
                return "# File not found in manifest."
            
            #normalize path string to handle windows vs linux path separators
            raw_path_str = str(row.iloc[0][col]).replace("\\", "/")
            path = Path(raw_path_str)
            if not path.exists():
                return f"# File not found:\n# {path}"
            try:
                return path.read_text(encoding="utf-8", errors="replace")
            except Exception as exc:
                return f"# Read error: {exc}"
 
        _ref_src = _load_src(sel_sc, sel_task, "ref_processed")
        _llm_src = _load_src(sel_sc, sel_task, "llm_processed")
 
        _cc_ref, _cc_llm = st.columns(2)
        with _cc_ref:
            st.markdown(
                f'<div style="font-size:.75rem;font-weight:600;color:{C["green"]};'  
                f'margin-bottom:.4rem;letter-spacing:.05em">◀ REFERENCE CODE</div>',
                unsafe_allow_html=True,
            )
            with st.container(height=350):
                st.code(_ref_src, language="python", line_numbers=True)
            
        with _cc_llm:
            st.markdown(
                f'<div style="font-size:.75rem;font-weight:600;color:{C["blue"]};'  
                f'margin-bottom:.4rem;letter-spacing:.05em">▶ LLM GENERATED CODE</div>',
                unsafe_allow_html=True,
            )
            with st.container(height=350):
                st.code(_llm_src, language="python", line_numbers=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
    #end collapsible   code panel
 
    #Grapgh panels
    if ref_g is None and llm_g is None:
        st.markdown(
            f'<div style="background:{C["card"]};border:1px solid {C["border"]};'
            f'border-radius:8px;padding:1rem;color:{C["muted"]};font-size:.82rem">'
            f'⚠ No GraphML files found for this task. '
            f'Run <code>python run_pipeline.py --phase 3</code> to build CFGs.</div>',
            unsafe_allow_html=True)
    else:
        if cfg_mode == "Side by Side":
            c_ref, c_llm = st.columns(2)
            with c_ref:
                st.markdown(f'<div style="font-size:.75rem;font-weight:600;'
                            f'color:{C["green"]};margin-bottom:.3rem">▶ REFERENCE</div>',
                            unsafe_allow_html=True)
                if ref_g:
                    components.html(pyvis_html(ref_g, 480), height=490, scrolling=False)
                else:
                    st.info("Reference CFG not found.")
            with c_llm:
                st.markdown(f'<div style="font-size:.75rem;font-weight:600;'
                            f'color:{C["blue"]};margin-bottom:.3rem">▶ LLM GENERATED</div>',
                            unsafe_allow_html=True)
                if llm_g:
                    components.html(pyvis_html(llm_g, 480), height=490, scrolling=False)
                else:
                    st.info("LLM CFG not found.")
 
        else:  # difference modee
            st.markdown(f"""
            <div class="legend-row">
                <b style="color:{C['text']}">Diff Key:</b>
                <span><span class="dot" style="background:{C['green']}"></span>Matched block type</span>
                <span><span class="dot" style="background:{C['red']}"></span>REF only — missing from LLM</span>
                <span><span class="dot" style="background:{C['blue']}"></span>LLM only — extra block</span>
            </div>""", unsafe_allow_html=True)
 
            if ref_g and llm_g:
                rc, lc = diff_colors(ref_g, llm_g)
                c_ref, c_llm = st.columns(2)
                with c_ref:
                    st.markdown(f'<div style="font-size:.75rem;font-weight:600;'
                                f'color:{C["green"]};margin-bottom:.3rem">▶ REFERENCE (coloured by match)</div>',
                                unsafe_allow_html=True)
                    components.html(pyvis_html(ref_g, 480, rc), height=490, scrolling=False)
                with c_llm:
                    st.markdown(f'<div style="font-size:.75rem;font-weight:600;'
                                f'color:{C["blue"]};margin-bottom:.3rem">▶ LLM (coloured by match)</div>',
                                unsafe_allow_html=True)
                    components.html(pyvis_html(llm_g, 480, lc), height=490, scrolling=False)
            else:
                st.warning("Both CFGs required for diff view.")
 
#FINAL similarity by the scenarioss

divider()
section("② Final Similarity Score by Scenario")
 
if sd.empty:
    st.warning("No similarity data. Run `python run_pipeline.py --phase 4`")
else:
    order = (sd.groupby("scenario")["s_final"]
               .median().sort_values(ascending=False).index.tolist())
    fig_box = px.box(
        sd, x="scenario", y="s_final",
        color="scenario", points="all",
        category_orders={"scenario": order},
        template=TPL,
        labels={"scenario":"Scenario","s_final":"S_final"},
    )
    fig_box.update_traces(marker=dict(size=5, opacity=0.75))
    fig_box.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PLOT,
        font=dict(color=FONT, family="Inter"),
        xaxis=dict(gridcolor=GRID, tickangle=-25, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID, title="S_final [0–1]"),
        showlegend=False, height=390,
        margin=dict(l=42, r=18, t=18, b=60),
    )
    st.plotly_chart(fig_box, use_container_width=True)
    #Scenario summarytable under the a chartt
    tbl = sd.groupby("scenario").agg(
        tasks        =("task_id","count"),
        mean_final   =("s_final","mean"),
        mean_lex     =("s_lexical","mean"),
        mean_sem     =("s_semantic","mean"),
        mean_struct  =("s_structural","mean"),
    ).round(3).reset_index()
    tbl.columns = ["Scenario","Tasks","Mean S_final","Mean Lexical","Mean Semantic","Mean Structural"]
    st.dataframe(tbl.style.format({c:"{:.3f}" for c in tbl.columns[2:]}),
                 use_container_width=True, hide_index=True)
 
 

        #       similarity SCOrE Distribution histogranms
divider()
section("③ Similarity Score Distribution")
 
if sd.empty:
    st.warning("No similarity data.")
else:
    c_h1, c_h2 = st.columns(2)
    with c_h1:
            #Finalscore histogram
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=sd["s_final"].dropna(), nbinsx=25,
            marker=dict(color=C["accent"], opacity=0.85,
                        line=dict(color=GRID, width=0.4)),
            name="S_final",
            hovertemplate="Score: %{x:.3f}<br>Count: %{y}<extra></extra>",
        ))
        mn = sd["s_final"].mean()
        fig_hist.add_vline(x=mn, line_dash="dash", line_color=C["red"],
                           annotation_text=f"μ={mn:.3f}",
                           annotation_font=dict(color=C["red"], size=11))
        
#   separation of template layout from axis properties
        fig_hist.update_layout(**_base("Final Similarity Distribution (S_final)"))
        fig_hist.update_xaxes(title="S_final", gridcolor=GRID)
        fig_hist.update_yaxes(title="Count",   gridcolor=GRID)
        
        st.plotly_chart(fig_hist, use_container_width=True)
 
    with c_h2:
    # Ccomponent overrlay
        fig_comp = go.Figure()
        comps = [("Lexical","s_lexical",C["blue"]),
                 ("Structural","s_structural",C["purple"]),
                 ("Semantic","s_semantic",C["teal"])]
        for name, col_, color in comps:
            if col_ in sd.columns:
                fig_comp.add_trace(go.Histogram(
                    x=sd[col_].dropna(), nbinsx=25, name=name,
                    marker=dict(color=color, opacity=0.6,
                                line=dict(color=GRID, width=0.3)),
                    hovertemplate=name+": %{x:.3f}<extra></extra>",
                ))
                
        # sseparation of template Layout from axis oR legend propeerties
        fig_comp.update_layout(
            **_base("Component Scores Overlay"),
            barmode="overlay",
            legend=dict(orientation="h", y=-0.2, font=dict(size=11)),
        )
        fig_comp.update_xaxes(title="Score", gridcolor=GRID)
        fig_comp.update_yaxes(title="Count", gridcolor=GRID)
        
        st.plotly_chart(fig_comp, use_container_width=True)
                #           graphg thehoretic metrics
divider()
section("④ Graph-Theoretic Metrics")
 
if strd.empty:
    st.warning("No structural metrics. Run `python run_pipeline.py --phase 3`")
else:
#Row of metric oveRrview kards
    def _sm(col): return round(strd[col].dropna().mean(),2) if col in strd.columns else None
    def _fmt(v):  return f"{v:.2f}" if v is not None else "—"
 
    mc2 = st.columns(6)
    gm_cards = [
        ("Avg M (LLM)",   _fmt(_sm("llm_cfg_cyclomatic_complexity")), C["accent"]),
        ("Avg M (REF)",   _fmt(_sm("ref_cfg_cyclomatic_complexity")),  C["green"]),
        ("Avg Nodes LLM", _fmt(_sm("llm_cfg_num_nodes")),              C["blue"]),
        ("Avg Edges LLM", _fmt(_sm("llm_cfg_num_edges")),              C["purple"]),
        ("Avg Depth LLM", _fmt(_sm("llm_cfg_graph_depth")),            C["teal"]),
        ("Avg AST Nodes", _fmt(_sm("llm_ast_total_ast_nodes")),        C["orange"]),
    ]
    for col, (lbl, val, color) in zip(mc2, gm_cards):
        col.markdown(metric_card(lbl, val, color), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
 
    #two charts for complexity histogram and REF versuss LLM scatter
    c_gm1, c_gm2 = st.columns(2)
    with c_gm1:
        col_ = "llm_cfg_cyclomatic_complexity"
        vals = strd[col_].dropna()
        fig_mc = go.Figure(go.Histogram(
            x=vals, nbinsx=20,
            marker=dict(color=C["accent"], opacity=0.85,
                        line=dict(color=GRID, width=0.4)),
            hovertemplate="M=%{x}: %{y} tasks<extra></extra>",
        ))
        fig_mc.add_vline(x=vals.mean(), line_dash="dash",
                         line_color=C["red"],
                         annotation_text=f"μ={vals.mean():.1f}",
                         annotation_font=dict(color=C["red"],size=11))
        
        #separation of template layout frrom axis properties
        fig_mc.update_layout(**_base("LLM Cyclomatic Complexity Distribution"))
        fig_mc.update_xaxes(title="M", gridcolor=GRID)
        fig_mc.update_yaxes(title="Count", gridcolor=GRID)
        
        st.plotly_chart(fig_mc, use_container_width=True)
 
    with c_gm2:
        rc = "ref_cfg_cyclomatic_complexity"
        lc = "llm_cfg_cyclomatic_complexity"
        if rc in strd.columns and lc in strd.columns:
            d_ = strd[[rc, lc, "scenario","task_id"]].dropna()
            hover = d_.apply(lambda r: f"{r['scenario']}/{r['task_id']}", axis=1)
            fig_rv = go.Figure()
            # y=x referrence lineE
            mx_ = max(d_[rc].max(), d_[lc].max())
            fig_rv.add_trace(go.Scatter(
                x=[0,mx_], y=[0,mx_], mode="lines",
                line=dict(color=GRID, dash="dot", width=1.5),
                showlegend=False, hoverinfo="skip"))
            fig_rv.add_trace(go.Scatter(
                x=d_[rc], y=d_[lc], mode="markers",
                text=hover,
                marker=dict(color=C["accent"], size=8, opacity=0.8,
                            line=dict(width=1, color=GRID)),
                hovertemplate="%{text}<br>REF M=%{x}<br>LLM M=%{y}<extra></extra>",
                showlegend=False,
            ))
            
            # SSeparation inthe of template layout fram axis properties
            fig_rv.update_layout(**_base("REF vs LLM Cyclomatic Complexity"))
            fig_rv.update_xaxes(title="M — Reference",   gridcolor=GRID)
            fig_rv.update_yaxes(title="M — LLM Generated", gridcolor=GRID)
            
            st.plotly_chart(fig_rv, use_container_width=True)
 
# all metrics grouped bar ref vs llM pere scenario
    grp_cols = {
        "M":     ("ref_cfg_cyclomatic_complexity","llm_cfg_cyclomatic_complexity"),
        "Nodes": ("ref_cfg_num_nodes",             "llm_cfg_num_nodes"),
        "Edges": ("ref_cfg_num_edges",             "llm_cfg_num_edges"),
        "Depth": ("ref_cfg_graph_depth",           "llm_cfg_graph_depth"),
    }
    avail_gc = {k:v for k,v in grp_cols.items()
                if v[0] in strd.columns and v[1] in strd.columns}
    if avail_gc:
        metric_sel = st.selectbox("Metric for scenario comparison",
                                  list(avail_gc.keys()), key="gm_sel")
        rc_, lc_ = avail_gc[metric_sel]
        grp2 = strd.groupby("scenario")[[rc_, lc_]].mean().reset_index()
        fig_grp = go.Figure()
        fig_grp.add_trace(go.Bar(name="Reference",
                                  x=grp2["scenario"], y=grp2[rc_],
                                  marker_color=C["green"], opacity=0.85,
                                  text=grp2[rc_].round(1), textposition="outside"))
        fig_grp.add_trace(go.Bar(name="LLM",
                                  x=grp2["scenario"], y=grp2[lc_],
                                  marker_color=C["blue"], opacity=0.85,
                                  text=grp2[lc_].round(1), textposition="outside"))
#sseparation of tamplate layout fram axis or llegend properties
        fig_grp.update_layout(
            **_base(f"Mean {metric_sel}: Reference vs LLM by Scenario", height=360),
            barmode="group",
            legend=dict(orientation="h", y=-0.22),
        )
        fig_grp.update_xaxes(tickangle=-20, gridcolor=GRID)
        fig_grp.update_yaxes(title=metric_sel, gridcolor=GRID)
        
        st.plotly_chart(fig_grp, use_container_width=True)
 
 

                #           CORREllaTION hEATmAP
divider()
section("⑤ Correlation Heatmap")
 
all_df = merged()
wanted = [
    "s_lexical","s_structural","s_semantic","s_final",
    "pass_rate","coverage_pct",
    "llm_cfg_cyclomatic_complexity","llm_cfg_num_nodes",
    "llm_cfg_num_edges","llm_cfg_graph_depth",
    "llm_ast_total_ast_nodes","llm_ast_branching_nodes",
    "absdiff_cyclomatic_complexity","absdiff_num_nodes",
]
avail = [c for c in wanted if c in all_df.columns]
 
if len(avail) >= 3:
    corr = all_df[avail].corr().round(2)
    short = [c.replace("llm_cfg_","").replace("llm_ast_","")
              .replace("absdiff_","Δ").replace("_"," ")
             for c in avail]
 
    import numpy as np
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    z = corr.values.astype(float).copy()
    z[mask] = np.nan
 
    fig_hm = go.Figure(go.Heatmap(
        z=z, x=short, y=short,
        colorscale="RdBu", zmid=0, zmin=-1, zmax=1,
        colorbar=dict(title="r", tickfont=dict(size=10)),
        text=np.where(mask, "", corr.round(2).astype(str).values),
        texttemplate="%{text}", textfont=dict(size=9),
        hovertemplate="%{y} × %{x}: %{z:.2f}<extra></extra>",
    ))
    n = len(avail)
    fig_hm.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PLOT,
        font=dict(color=FONT, family="Inter"),
        title=dict(text="Pearson Correlation — All Key Metrics", font=dict(size=14)),
        xaxis=dict(tickfont=dict(size=9), gridcolor=GRID, tickangle=-30),
        yaxis=dict(tickfont=dict(size=9), gridcolor=GRID, autorange="reversed"),
        height=max(440, n*38+100),
        margin=dict(l=160, r=20, t=54, b=120),
    )
    st.plotly_chart(fig_hm, use_container_width=True)
    st.markdown(
        f'<div style="font-size:.75rem;color:{C["muted"]};margin-top:-.5rem">'
        f'Blank cells = upper triangle (mirror). '
        f'Computed over {len(all_df)} tasks.</div>',
        unsafe_allow_html=True,
    )
else:
    st.warning("Not enough columns for correlation. Run Phases 3, 4, and 5.")

            #similarity VersuS Cyclomatik COMPLEXITY
divider()
section("⑥ Similarity vs Cyclomatic Complexity")
 
req6 = ["s_final","llm_cfg_cyclomatic_complexity","scenario","task_id"]
if all_df.empty or any(c not in all_df.columns for c in req6):
    st.warning("Run Phases 3 + 4 to see this chart.")
else:
    d6 = all_df[req6].dropna()
    hover6 = d6.apply(lambda r: f"{r['scenario']}/{r['task_id']}", axis=1)
 
    fig_sc = px.scatter(
        d6, x="llm_cfg_cyclomatic_complexity", y="s_final",
        color="scenario", symbol="scenario",
        hover_data={"task_id":True},
        labels={"llm_cfg_cyclomatic_complexity":"Cyclomatic Complexity M (LLM)",
                "s_final":"Final Similarity S_final"},
        template=TPL,
        opacity=0.82,
    )
    #trendd liine
    if len(d6) > 3:
        z6 = np.polyfit(d6["llm_cfg_cyclomatic_complexity"], d6["s_final"], 1)
        xr = np.linspace(d6["llm_cfg_cyclomatic_complexity"].min(),
                         d6["llm_cfg_cyclomatic_complexity"].max(), 100)
        fig_sc.add_trace(go.Scatter(
            x=xr, y=np.poly1d(z6)(xr), mode="lines", name="Trend",
            line=dict(color=C["orange"], dash="dash", width=2),
            hoverinfo="skip",
        ))
    fig_sc.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PLOT,
        font=dict(color=FONT, family="Inter"),
        xaxis=dict(title="Cyclomatic Complexity M (LLM)", gridcolor=GRID),
        yaxis=dict(title="S_final [0–1]", gridcolor=GRID, range=[0,1.05]),
        legend=dict(font=dict(size=10)),
        height=420, margin=dict(l=42,r=18,t=18,b=42),
    )
    fig_sc.update_traces(marker=dict(size=9))
    st.plotly_chart(fig_sc, use_container_width=True)
 #              Ppearson r anotasion
    if len(d6) > 2:
        r6 = np.corrcoef(d6["llm_cfg_cyclomatic_complexity"], d6["s_final"])[0,1]
        st.markdown(
            f'<div style="font-size:.78rem;color:{C["muted"]};margin-top:-.4rem">'
            f'Pearson r = <b style="color:{C["text"]}">{r6:.3f}</b> &nbsp;|&nbsp; '
            f'n = {len(d6)} tasks</div>',
            unsafe_allow_html=True,
        ) 
"""similarity VrS test pass ratee"""

divider()
section("⑦ Similarity vs Test Pass Rate")
 
req7 = ["s_final","pass_rate","scenario","task_id"]
if all_df.empty or any(c not in all_df.columns for c in req7):
    st.warning("Run Phases 4 + 5 to see this chart.")
else:
    d7 = all_df[req7].dropna()
    if d7.empty or d7["pass_rate"].sum() == 0:
        st.info("Test pass rate data is all zero or missing. Run Phase 5 to populate real results.")
    else:
        fig_pr = px.scatter(
            d7, x="pass_rate", y="s_final",
            color="scenario", symbol="scenario",
            hover_data={"task_id":True},
            labels={"pass_rate":"Test Pass Rate","s_final":"S_final"},
            template=TPL, opacity=0.82,
        )
        fig_pr.update_traces(marker=dict(size=9))
        fig_pr.add_hline(y=0.5, line_dash="dot", line_color=GRID, opacity=0.7)
        fig_pr.add_vline(x=0.5, line_dash="dot", line_color=GRID, opacity=0.7)
    #quadrant  annotations
        for xp,yp,txt in [(0.13,0.92,"High sim\nLow pass"),(0.88,0.92,"High sim\nHigh pass"),
                           (0.13,0.06,"Low sim\nLow pass"), (0.88,0.06,"Low sim\nHigh pass")]:
            fig_pr.add_annotation(x=xp, y=yp, text=txt, showarrow=False,
                                   font=dict(size=8, color=C["muted"]),
                                   xref="paper", yref="paper")
        fig_pr.update_layout(
            paper_bgcolor=PAPER, plot_bgcolor=PLOT,
            font=dict(color=FONT, family="Inter"),
            xaxis=dict(title="Test Pass Rate", gridcolor=GRID,
                       range=[0,1.05], tickformat=".0%"),
            yaxis=dict(title="S_final [0–1]", gridcolor=GRID, range=[0,1.05]),
            legend=dict(font=dict(size=10)),
            height=420, margin=dict(l=42,r=18,t=18,b=42),
        )
        st.plotly_chart(fig_pr, use_container_width=True)
        st.markdown(f"""
        <div style="font-size:.78rem;color:{C['muted']};
             background:{C['card']};border:1px solid {C['border']};
             border-radius:6px;padding:.6rem .9rem;margin-top:-.3rem">
            <b style="color:{C['text']}">Quadrant interpretation:</b>&nbsp;&nbsp;
            ↗ High sim + High pass = LLM closely reproduced a correct reference.&nbsp;&nbsp;
            ↖ High sim + Low pass = Superficially similar but functionally wrong.&nbsp;&nbsp;
            ↘ Low sim + High pass = Different approach, still correct.&nbsp;&nbsp;
            ↙ Low sim + Low pass = Different and incorrect.
        </div>""", unsafe_allow_html=True)
 
            #       footeer
divider()
st.markdown(
    f'<div style="text-align:center;font-size:.72rem;color:{C["muted"]};'
    f'padding-bottom:1.5rem">'
    f'</div>',
    unsafe_allow_html=True,
)