import streamlit as st
import requests
import time

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="TinyStories GPT | Portfolio Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. CLEAN PROFESSIONAL UI (REVISED CSS)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Import modern professional font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;600&family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean Dark Theme Background */
    .stApp {
        background-color: #0d1117; /* GitHub Dark tone */
        color: #c9d1d9;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Title - Clean White/Blue */
    .main-title {
        font-weight: 800;
        font-size: 2.5rem;
        color: #ffffff;
        margin-bottom: 0;
    }
    .subtitle {
        color: #8b949e;
        font-size: 1.1rem;
        margin-top: 10px;
    }

    /* Professional Card Styling (No excessive neon) */
    .pro-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* Badge Styling - Cleaner look */
    .tech-badge {
        display: inline-block;
        padding: 4px 10px;
        margin: 4px 2px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #30363d;
        background: #21262d;
        color: #c9d1d9;
    }
    
    /* Highlights */
    .highlight-blue { color: #58a6ff; border-color: #58a6ff33; }
    .highlight-green { color: #3fb950; border-color: #3fb95033; }

    /* Button Styling - Professional Blue */
    div.stButton > button:first-child {
        background-color: #238636; /* Professional Green */
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
    }

    div.stButton > button:first-child:hover {
        background-color: #2ea043;
        transform: translateY(-1px);
    }

    /* Input & Text Area */
    .stTextArea textarea {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
    }
    .stTextArea textarea:focus {
        border-color: #58a6ff !important;
    }

    /* Output Terminal - Cleaner monospace */
    .output-terminal {
        font-family: 'Roboto Mono', monospace;
        background-color: #0d1117;
        color: #e6edf3;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #30363d;
        line-height: 1.6;
        border-left: 4px solid #238636;
    }
    
    /* Image Placeholder Styling */
    .image-placeholder {
        background-color: #161b22;
        border: 2px dashed #30363d;
        border-radius: 12px;
        height: 250px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #8b949e;
        text-align: center;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. SIDEBAR CONTENT
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Model Parameters")
    
    length = st.slider("Max Sequence Length", 50, 500, 200)
    temp = st.slider("Temperature (Stochasticity)", 0.1, 2.0, 0.8, 0.1)
    
    st.markdown("---")
    
    st.markdown("### 👨‍💻 Technical Profile")
    
    # Clean Badges
    st.markdown("""
    <div style="margin-bottom: 15px;">
        <span class="tech-badge highlight-blue">Transformer Arch</span>
        <span class="tech-badge highlight-blue">PyTorch Native</span>
        <span class="tech-badge highlight-green">Custom BPE Tokenizer</span>
        <span class="tech-badge">FastAPI Inference</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(
        """
        **Project Identity:**
        
        This system is a generative Language Model built **entirely from scratch** for portfolio demonstration.
        
        It bypasses high-level abstractions to demonstrate core competency in Deep Learning architecture implementation (Attention, Feed-Forward, Normalization layers manually coded in PyTorch).
        """
    )
    
    st.markdown("---")
    st.caption("System Status: Localhost Deployment")


# ---------------------------------------------------------
# 4. MAIN CONTENT
# ---------------------------------------------------------

# Header Section
st.markdown('<div class="main-title">TinyStories GPT Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">An end-to-end implementation of a generative Transformer model trained on short narratives.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Workspace Layout
col1, col2 = st.columns([5, 4], gap="large")

with col1:
    st.markdown("### 📥 Text Input")
    st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
    prompt = st.text_area(
        "Prompt",
        value="Once upon a time, there was a brave little robot who wanted to",
        height=200,
        label_visibility="collapsed",
        placeholder="Start your story here..."
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Generate Story 🚀"):
        if not prompt.strip():
            st.toast("⚠️ Please enter a prompt first!", icon="⚠️")
        else:
            # Initialize Session State for results
            st.session_state['run_generation'] = True
            st.session_state['prompt'] = prompt
            
            with col2:
                status_placeholder = st.empty()
                status_placeholder.markdown("""
                <div class='pro-card' style='text-align: center; color: #8b949e; padding: 40px;'>
                    ⚡ <b>Processing Inference Pipeline...</b><br><br>
                    Tokenizing Input → Forward Pass → Decoding Output
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    start_ts = time.time()
                    # API Call
                    response = requests.post(
                        "http://127.0.0.1:8000/generate", 
                        json={"text": prompt, "length": length, "temp": temp},
                        timeout=45
                    )
                    end_ts = time.time()
                    
                    if response.status_code == 200:
                        data = response.json()
                        if "generated" in data:
                            st.session_state['gen_text'] = data['generated']
                            st.session_state['latency'] = end_ts - start_ts
                            status_placeholder.empty() # Remove loading state
                        else:
                            st.error(f"Backend Protocol Error: {data}")
                    else:
                        st.error(f"Connection Refused: HTTP {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Fatal Error: Inference Engine (Backend) is offline.")

# Default view for Output column
with col2:
    st.markdown("### 📤 Model Output")
    
    if 'gen_text' in st.session_state:
        # SHOW TEXT OUTPUT
        st.markdown(f"""
        <div class="output-terminal">
            <div style="margin-bottom: 15px; font-size: 0.9em; color: #3fb950;">
                ✅ Generation Successful ({st.session_state['latency']:.2f}s)
            </div>
            {st.session_state['gen_text']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # SHOW IMAGE PLACEHOLDER (Professional way to handle it)
        st.markdown("### 🎨 Visual Interpretation (Concept)")
        st.markdown("""
        <div class="image-placeholder">
            <p style="font-size: 2rem; margin-bottom: 10px;">🖼️</p>
            <p><b>Image Generation Pipeline Not Connected</b></p>
            <p style="font-size: 0.8em; max-width: 80%;">
            Note for review: This custom GPT model is text-only. 
            A separate generative image model (e.g., Stable Diffusion) would be required here to visualize the story dynamically. 
            This placeholder demonstrates multi-modal UI intent.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Initial Empty State
        st.markdown("""
        <div class="pro-card" style="min-height: 300px; display: flex; align-items: center; justify-content: center; color: #8b949e;">
            Waiting for input sequence to trigger generation...
        </div>
        """, unsafe_allow_html=True)