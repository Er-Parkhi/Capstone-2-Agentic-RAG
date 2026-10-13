import streamlit as st

from src.agent import MedicalAgent

st.set_page_config(page_title="Doctor Chatty", page_icon="🩺", layout="wide")


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #fff8fa;
            --panel: rgba(255,255,255,0.85);
            --panel-strong: #ffffff;
            --primary: #bd5d7b;
            --primary-soft: #fff0f4;
            --accent: #93609b;
            --success: #10b981;
            --text: #493843;
            --muted: #786874;
            --border: rgba(116,75,98,0.14);
            --shadow: 0 18px 45px rgba(151,83,115,0.12);
        }

        .stApp {
            background: linear-gradient(135deg, #fff4f6 0%, #fffafd 48%, #f8f1fa 100%);
            color: var(--text);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1300px;
        }

        .hero {
            background: linear-gradient(135deg, #c76582, #93609b);
            padding: 2rem 2.2rem;
            border-radius: 24px;
            box-shadow: var(--shadow);
            color: white;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.15);
        }

        .hero h1 {
            font-size: 2.4rem !important;
            margin-bottom: 0.3rem;
            font-weight: 700;
        }

        .hero p {
            color: rgba(255,255,255,0.88);
            font-size: 1rem;
            margin-bottom: 0;
        }

        .status-chip {
            display: inline-block;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.26);
            font-size: 0.82rem;
            font-weight: 600;
            margin-top: 0.8rem;
        }

        .glass-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1.2rem 1.3rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(8px);
        }

        .metric-box {
            background: linear-gradient(180deg, #ffffff 0%, #fff3f6 100%);
            border: 1px solid rgba(189,93,123,0.14);
            border-radius: 16px;
            padding: 1rem;
            height: 100%;
        }

        .metric-box h4 {
            margin: 0 0 0.4rem 0;
            color: var(--muted);
            font-size: 0.78rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .metric-box .value {
            font-size: 1.7rem;
            font-weight: 700;
            color: var(--primary);
            margin: 0;
        }

        .prompt-button {
            width: 100%;
            text-align: left;
            padding: 0.8rem 0.9rem;
            border-radius: 14px;
            background: linear-gradient(180deg, #ffffff 0%, #fff5f7 100%);
            border: 1px solid rgba(189,93,123,0.14);
            color: var(--text);
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .prompt-button:hover {
            transform: translateY(-1px);
            border-color: rgba(189,93,123,0.32);
            box-shadow: 0 8px 20px rgba(189,93,123,0.10);
        }

        .answer-box {
            background: linear-gradient(180deg, rgba(189,93,123,0.06) 0%, rgba(147,96,155,0.04) 100%);
            border: 1px solid rgba(189,93,123,0.2);
            border-radius: 20px;
            padding: 1.4rem 1.2rem;
            color: var(--text);
            line-height: 1.7;
        }

        .answer-box h3 {
            margin-top: 0;
            color: var(--primary);
        }

        [data-testid="stSidebar"] {
            background: rgba(255,244,247,0.9);
            border-right: 1px solid rgba(116,75,98,0.10);
        }

        .sidebar-section {
            background: rgba(255,255,255,0.7);
            border: 1px solid rgba(116,75,98,0.10);
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .sidebar-section h3 {
            margin-top: 0;
            margin-bottom: 0.6rem;
            font-size: 0.95rem;
            color: var(--text);
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.7rem 1.05rem;
            transition: 0.2s ease;
        }

        .stButton > button:hover {
            filter: brightness(1.06);
            box-shadow: 0 8px 18px rgba(189,93,123,0.22);
        }

        .stTextArea textarea {
            border-radius: 16px;
            border: 1px solid rgba(189,93,123,0.18);
            background: rgba(255,255,255,0.9);
            min-height: 150px;
        }

        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 1px solid rgba(189,93,123,0.18);
            background: rgba(255,255,255,0.9);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def get_agent() -> MedicalAgent:
    return MedicalAgent()


inject_styles()
agent = get_agent()

sample_prompts = [
    "What are the symptoms of diabetes?",
    "How can I identify signs of hypertension?",
    "What diseases are associated with chronic fatigue?",
    "What are common symptoms of asthma?",
]

st.markdown(
    """
    <div class="hero">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom: 10px;">
            <div style="font-size: 2rem;">🩺</div>
            <div style="font-size: 0.9rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.9;">Your AI Health Companion</div>
        </div>
        <h1>Doctor Chatty</h1>
        <p>Ask about symptoms, disease patterns, and medical guidance using the project’s curated dataset and retrieval system.</p>
        <div class="status-chip">Live local knowledge base</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("### Quick start")
    for prompt in sample_prompts:
        if st.button(prompt, key=f"prompt_{prompt}", use_container_width=True):
            st.session_state.question = prompt
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("### Project status")
    st.success("System ready")
    st.info("Retrieval model is loaded from the local dataset.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
    st.markdown("### Safety note")
    st.write("This assistant provides general information, not a diagnosis. For serious symptoms, seek medical care immediately.")
    st.markdown("</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="metric-box">
            <h4>Knowledge base</h4>
            <p class="value">Local</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="metric-box">
            <h4>Mode</h4>
            <p class="value">RAG</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="metric-box">
            <h4>Focus</h4>
            <p class="value">Symptoms</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='glass-card' style='margin-top: 1.5rem; margin-bottom: 1.2rem;'>", unsafe_allow_html=True)
question = st.text_area(
    "Ask a medical question",
    value=st.session_state.get("question", ""),
    placeholder="Example: What are the symptoms of diabetes?",
    height=140,
)

submit_col, _, _ = st.columns([1, 3, 2])
with submit_col:
    ask_clicked = st.button("Ask Doctor Chatty", use_container_width=True)

if ask_clicked and not question.strip():
    st.warning("Please enter a medical question before submitting.")

if ask_clicked and question.strip():
    with st.spinner("Searching the medical knowledge base..."):
        answer = agent.ask(question)

    st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
    st.markdown("### Answer")
    st.markdown(answer)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.caption("Doctor Chatty retrieves the most relevant records from the local medical dataset to support contextual answers.")
