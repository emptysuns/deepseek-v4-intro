import streamlit as st
import json
import time
import os

# ── Page config ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="DeepSeek V4 Pro",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0 2rem 0;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
    }
    .main-header p {
        color: #888;
        font-size: 1.1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #333;
    }
    .stChatMessage {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=64)
    st.title("DeepSeek V4 Pro")
    st.caption("Introduction & Test Page")

    st.divider()
    st.subheader("⚙️ Parameters")

    api_base = st.text_input(
        "API Base URL",
        value=os.environ.get("API_BASE", "https://api.deepseek.com"),
        help="DeepSeek API endpoint"
    )
    api_key = st.text_input(
        "API Key",
        value=os.environ.get("API_KEY", ""),
        type="password",
        help="Your DeepSeek API key"
    )
    model = st.selectbox(
        "Model",
        ["deepseek-v4-pro", "deepseek-v4", "deepseek-r1", "deepseek-chat"],
        index=0,
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 256, 32768, 4096, 256)
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)

    st.divider()
    st.subheader("📊 Model Specs")
    col1, col2 = st.columns(2)
    col1.metric("Parameters", "685B")
    col2.metric("Context", "128K")
    col1.metric("MoE Experts", "256")
    col2.metric("Active Experts", "16")

    st.divider()
    st.caption("Built with Streamlit · Hysteria2 Relay")

# ── Main content ────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🔬 DeepSeek V4 Pro</h1>
    <p>Next-generation Mixture-of-Experts architecture · 685B parameters · 128K context window</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────────
tab_chat, tab_info, tab_api = st.tabs(["💬 Chat", "📖 Model Info", "🔌 API Reference"])

# ── Chat Tab ────────────────────────────────────────────────────────
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # System prompt
    system_prompt = st.text_area(
        "System Prompt (optional)",
        value="You are DeepSeek V4 Pro, a helpful and capable AI assistant.",
        height=68,
    )

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask DeepSeek V4 Pro anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Try real API call
            if api_key:
                import urllib.request
                import urllib.error

                payload = json.dumps({
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *[m for m in st.session_state.messages],
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": top_p,
                    "stream": True,
                })

                try:
                    req = urllib.request.Request(
                        f"{api_base}/v1/chat/completions",
                        data=payload.encode(),
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_key}",
                        },
                    )
                    with urllib.request.urlopen(req) as response:
                        for line in response:
                            line = line.decode().strip()
                            if line.startswith("data: ") and line != "data: [DONE]":
                                chunk = json.loads(line[6:])
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    full_response += delta["content"]
                                    message_placeholder.markdown(full_response + "▌")
                                    time.sleep(0.01)
                except Exception as e:
                    full_response = f"⚠️ API Error: {e}"
            else:
                # Demo response when no API key
                demo = (
                    f"**DeepSeek V4 Pro** received your message:\n\n"
                    f"> {prompt}\n\n"
                    f"This is a demo response. Configure your API key in the sidebar "
                    f"to connect to the real DeepSeek API.\n\n"
                    f"**Current settings:** model=`{model}`, temp=`{temperature}`, "
                    f"max_tokens=`{max_tokens}`, top_p=`{top_p}`"
                )
                for i in range(len(demo)):
                    full_response = demo[: i + 1]
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.008)

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ── Model Info Tab ──────────────────────────────────────────────────
with tab_info:
    st.header("DeepSeek V4 Pro Architecture")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🏗️ Architecture")
        st.markdown("""
        | Component | Value |
        |-----------|-------|
        | Total Parameters | 685B |
        | Active Parameters | 37B |
        | Number of Layers | 61 |
        | Hidden Size | 7168 |
        | MoE Experts | 256 shared + 1 routed |
        | Active Experts | 16 per token |
        | Context Window | 128K tokens |
        | Vocabulary Size | 129,280 |
        """)

    with col_b:
        st.subheader("⚡ Performance")
        st.markdown("""
        | Benchmark | Score |
        |-----------|-------|
        | MMLU | 90.9 |
        | HumanEval | 90.2 |
        | MATH-500 | 97.8 |
        | GPQA Diamond | 84.0 |
        | LiveCodeBench | 65.9 |
        | Codeforces | 90.2 |
        | SWE-bench Verified | 55.0 |
        | AIME 2025 | 88.6 |
        """)

    st.subheader("🔑 Key Innovations")
    st.markdown("""
    1. **Multi-head Latent Attention (MLA)** — Compresses KV cache into a low-dimensional latent space,
       reducing memory footprint by ~93% compared to standard MHA while maintaining performance.

    2. **DeepSeekMoE with Auxiliary-loss-free Load Balancing** — 256 shared experts + 1 routed expert per token,
       with a novel load-balancing strategy that avoids the performance degradation of traditional auxiliary losses.

    3. **FP8 Mixed Precision Training** — First model at this scale trained with FP8 from scratch,
       achieving 40% reduction in training compute with negligible quality loss.

    4. **Multi-Token Prediction (MTP)** — Trains on predicting multiple future tokens simultaneously,
       improving data efficiency and enabling speculative decoding at inference time.

    5. **128K Context with YaRN** — Extended from 4K to 128K using YaRN (Yet another RoPE extensioN)
       with a progressive 4-stage training schedule.
    """)

# ── API Reference Tab ───────────────────────────────────────────────
with tab_api:
    st.header("🔌 API Reference")

    st.subheader("Chat Completions")
    st.code("""
POST /v1/chat/completions
Content-Type: application/json
Authorization: Bearer <YOUR_API_KEY>

{
    "model": "deepseek-v4-pro",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 4096,
    "top_p": 0.9,
    "stream": true
}
""", language="json")

    st.subheader("Python Example")
    st.code("""
from openai import OpenAI

client = OpenAI(
    api_key="<YOUR_API_KEY>",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain MoE architecture."}
    ],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
""", language="python")

    st.subheader("cURL Example")
    st.code("""
curl https://api.deepseek.com/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer $API_KEY" \\
  -d '{
    "model": "deepseek-v4-pro",
    "messages": [{"role": "user", "content": "Hi"}],
    "stream": true
  }
""", language="bash")
