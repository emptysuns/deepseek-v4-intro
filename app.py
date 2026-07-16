import streamlit as st

st.set_page_config(
    page_title="DeepSeek V4 — Model Overview",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --ink: #0d1b1e;
    --muted: #5f6f72;
    --line: #dbe5e3;
    --paper: #f7faf9;
    --mint: #18a77b;
    --mint-soft: #ddf5ed;
    --navy: #102f35;
}
html { scroll-behavior: smooth; }
.stApp { background: var(--paper); color: var(--ink); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"], footer { display: none; }
.block-container { max-width: 1180px; padding: 2rem 2.25rem 5rem; }
* { font-family: "DM Sans", sans-serif; }
h1, h2, h3, .display, .metric-value { font-family: "Space Grotesk", sans-serif !important; }

.topbar { display:flex; align-items:center; justify-content:space-between; padding: .4rem 0 3rem; }
.brand { display:flex; align-items:center; gap:.7rem; font-family:"Space Grotesk",sans-serif; font-weight:700; letter-spacing:-.02em; }
.brand-mark { width:1.8rem; height:1.8rem; display:grid; place-items:center; border-radius:50%; background:var(--ink); color:white; font-size:.8rem; }
.top-note { color:var(--muted); font-size:.86rem; }
.hero { padding: 4.3rem 0 4rem; border-top:1px solid var(--line); }
.eyebrow { display:inline-flex; align-items:center; gap:.55rem; color:#087c5d; font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.14em; }
.eyebrow:before { content:""; width:1.7rem; height:1px; background:var(--mint); }
.display { max-width:960px; font-size:clamp(3.2rem,8vw,7.2rem); line-height:.9; letter-spacing:-.075em; margin:1.6rem 0 1.8rem; font-weight:600; }
.display .accent { color:var(--mint); }
.hero-grid { display:grid; grid-template-columns:1.35fr .65fr; gap:4rem; align-items:end; }
.lede { max-width:670px; color:var(--muted); font-size:1.18rem; line-height:1.75; margin:0; }
.hero-aside { border-left:1px solid var(--line); padding-left:1.5rem; color:var(--muted); font-size:.9rem; line-height:1.7; }
.hero-aside strong { display:block; color:var(--ink); font-size:1rem; margin-bottom:.35rem; }

.metric-grid { display:grid; grid-template-columns:repeat(4,1fr); border:1px solid var(--line); border-radius:1rem; overflow:hidden; background:white; box-shadow:0 18px 50px rgba(16,47,53,.05); }
.metric { padding:1.7rem; min-height:140px; border-right:1px solid var(--line); display:flex; flex-direction:column; justify-content:space-between; }
.metric:last-child { border-right:0; }
.metric-label { color:var(--muted); font-size:.75rem; font-weight:700; letter-spacing:.09em; text-transform:uppercase; }
.metric-value { font-size:2rem; font-weight:600; letter-spacing:-.05em; }
.metric-value small { color:var(--mint); font-size:.82rem; letter-spacing:0; }

.section { padding:6.5rem 0 1rem; }
.section-head { display:grid; grid-template-columns:.65fr 1.35fr; gap:4rem; margin-bottom:3rem; }
.section-index { color:var(--mint); font-weight:700; font-size:.8rem; letter-spacing:.1em; }
.section h2 { margin:0 0 1rem; font-size:clamp(2rem,4vw,3.5rem); letter-spacing:-.055em; line-height:1.05; }
.section-copy { color:var(--muted); font-size:1.03rem; line-height:1.75; max-width:700px; }
.card-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
.card { background:white; border:1px solid var(--line); border-radius:1rem; padding:1.6rem; min-height:230px; transition:transform .2s ease,border-color .2s ease; }
.card:hover { transform:translateY(-3px); border-color:#9dd8c5; }
.card-num { color:var(--mint); font-size:.74rem; font-weight:700; letter-spacing:.1em; }
.card h3 { margin:2.6rem 0 .7rem; font-size:1.25rem; letter-spacing:-.025em; }
.card p { color:var(--muted); line-height:1.65; font-size:.92rem; margin:0; }

.context-panel { display:grid; grid-template-columns:1fr 1fr; background:var(--navy); color:white; border-radius:1.25rem; overflow:hidden; margin-top:5rem; }
.context-copy { padding:3.5rem; }
.context-copy .section-index { color:#7de0c0; }
.context-copy h2 { margin:1.1rem 0; font-size:clamp(2rem,4vw,3.8rem); letter-spacing:-.055em; }
.context-copy p { color:#b8cccf; line-height:1.7; }
.context-visual { padding:3rem; background:linear-gradient(145deg,#16434a,#0d282d); display:flex; flex-direction:column; justify-content:center; gap:1rem; }
.bar-row { display:grid; grid-template-columns:6rem 1fr 3.5rem; gap:1rem; align-items:center; font-size:.8rem; color:#c9d9db; }
.bar { height:.55rem; background:#284f55; border-radius:2rem; overflow:hidden; }
.bar span { display:block; height:100%; background:#66dab5; border-radius:2rem; }

.benchmark { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; }
.score { padding:1.4rem 0; border-top:1px solid var(--line); }
.score strong { display:block; font-family:"Space Grotesk",sans-serif; font-size:2.25rem; letter-spacing:-.06em; }
.score span { color:var(--muted); font-size:.83rem; }
.mode-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
.mode { padding:1.6rem; border:1px solid var(--line); border-radius:1rem; }
.mode-tag { display:inline-block; padding:.25rem .55rem; border-radius:2rem; background:var(--mint-soft); color:#087c5d; font-size:.7rem; font-weight:700; text-transform:uppercase; }
.mode h3 { margin:1.4rem 0 .55rem; }
.mode p { margin:0; color:var(--muted); line-height:1.6; font-size:.9rem; }
.footer-note { margin-top:7rem; padding-top:2rem; border-top:1px solid var(--line); display:flex; justify-content:space-between; color:var(--muted); font-size:.78rem; }

@media (max-width: 800px) {
 .block-container { padding:1.2rem 1.1rem 3rem; }
 .topbar { padding-bottom:1.8rem; }
 .top-note { display:none; }
 .hero { padding:2.8rem 0; }
 .hero-grid,.section-head,.context-panel { grid-template-columns:1fr; gap:1.5rem; }
 .hero-aside { border-left:0; border-top:1px solid var(--line); padding:1rem 0 0; }
 .metric-grid { grid-template-columns:1fr 1fr; }
 .metric:nth-child(2) { border-right:0; }
 .metric:nth-child(-n+2) { border-bottom:1px solid var(--line); }
 .card-grid,.mode-grid { grid-template-columns:1fr; }
 .benchmark { grid-template-columns:1fr 1fr; }
 .section { padding-top:4.5rem; }
 .context-panel { margin-top:4rem; }
 .context-copy,.context-visual { padding:2rem; }
 .footer-note { flex-direction:column; gap:.5rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="topbar">
  <div class="brand"><span class="brand-mark">V4</span> DeepSeek Intelligence</div>
  <div class="top-note">Model overview · 2026</div>
</div>

<section class="hero">
  <div class="eyebrow">Frontier intelligence, efficiently activated</div>
  <h1 class="display">DeepSeek <span class="accent">V4</span><br>at a glance.</h1>
  <div class="hero-grid">
    <p class="lede">A next-generation Mixture-of-Experts model designed for demanding reasoning, software engineering, mathematics and million-token context workloads.</p>
    <div class="hero-aside"><strong>One model. Three reasoning modes.</strong>Scale inference effort from immediate answers to deliberate, maximum-depth analysis.</div>
  </div>
</section>

<div class="metric-grid">
  <div class="metric"><span class="metric-label">Total parameters</span><span class="metric-value">1.6T</span></div>
  <div class="metric"><span class="metric-label">Activated per token</span><span class="metric-value">49B <small>3.1%</small></span></div>
  <div class="metric"><span class="metric-label">Context window</span><span class="metric-value">1M</span></div>
  <div class="metric"><span class="metric-label">Pre-training data</span><span class="metric-value">32T+</span></div>
</div>

<section class="section">
  <div class="section-head">
    <div class="section-index">01 / Architecture</div>
    <div><h2>More capacity.<br>Less wasted compute.</h2><p class="section-copy">DeepSeek V4 concentrates model capacity where each token needs it. Sparse expert routing, compressed attention and stable residual pathways work together to make frontier-scale intelligence more efficient.</p></div>
  </div>
  <div class="card-grid">
    <article class="card"><span class="card-num">A / 01</span><h3>Hybrid Attention</h3><p>Compressed Sparse Attention and Heavily Compressed Attention reduce inference work and KV-cache pressure across very long sequences.</p></article>
    <article class="card"><span class="card-num">A / 02</span><h3>MoE Routing</h3><p>A large expert pool activates only the relevant fraction of parameters for each token, balancing specialist capacity with practical serving cost.</p></article>
    <article class="card"><span class="card-num">A / 03</span><h3>mHC Connections</h3><p>Manifold-Constrained Hyper-Connections strengthen information flow through deep networks while preserving training stability and expressivity.</p></article>
  </div>
</section>

<section class="context-panel">
  <div class="context-copy"><div class="section-index">02 / Long Context</div><h2>A million tokens, kept in view.</h2><p>DeepSeek V4 is designed to reason across repositories, research corpora and extended multi-document workflows without fragmenting the task into disconnected windows.</p></div>
  <div class="context-visual">
    <div class="bar-row"><span>V4 context</span><div class="bar"><span style="width:100%"></span></div><b>1M</b></div>
    <div class="bar-row"><span>384K tier</span><div class="bar"><span style="width:38.4%"></span></div><b>384K</b></div>
    <div class="bar-row"><span>128K tier</span><div class="bar"><span style="width:12.8%"></span></div><b>128K</b></div>
  </div>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-index">03 / Benchmarks</div>
    <div><h2>Built for difficult work.</h2><p class="section-copy">Reported evaluations highlight strength in competitive programming, software engineering, mathematical reasoning and long-context retrieval.</p></div>
  </div>
  <div class="benchmark">
    <div class="score"><strong>93.5</strong><span>LiveCodeBench</span></div>
    <div class="score"><strong>3206</strong><span>Codeforces rating</span></div>
    <div class="score"><strong>90.1</strong><span>GPQA Diamond</span></div>
    <div class="score"><strong>83.5</strong><span>MRCR 1M</span></div>
  </div>
</section>

<section class="section">
  <div class="section-head">
    <div class="section-index">04 / Reasoning</div>
    <div><h2>Match depth to the task.</h2><p class="section-copy">Reasoning effort can be aligned with latency, cost and complexity instead of applying the same inference pattern to every request.</p></div>
  </div>
  <div class="mode-grid">
    <article class="mode"><span class="mode-tag">Fast</span><h3>Non-think</h3><p>Direct responses for everyday knowledge, drafting and straightforward transformations.</p></article>
    <article class="mode"><span class="mode-tag">Balanced</span><h3>Think High</h3><p>Deliberate analysis for coding, planning and multi-step reasoning with a practical latency profile.</p></article>
    <article class="mode"><span class="mode-tag">Maximum</span><h3>Think Max</h3><p>Extended inference for complex proofs, hard engineering tasks and deep research synthesis.</p></article>
  </div>
</section>

<div class="footer-note"><span>DeepSeek V4 — independent model introduction</span><span>Figures shown are reported model specifications.</span></div>
""",
    unsafe_allow_html=True,
)
