import streamlit as st
import requests
import random
import numpy as np

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BLECA SmartLabs AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #f0f0f0; }
    [data-testid="stSidebar"] { background: rgba(255,255,255,0.05); border-right: 1px solid rgba(255,255,255,0.1); }
    .bleca-header { text-align: center; padding: 2rem 0 1rem 0; }
    .bleca-header h1 { font-size: 2.5rem; font-weight: 800; background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
    .bleca-header p { color: #9ca3af; font-size: 1rem; margin-top: 0.5rem; }
    .user-msg { background: rgba(167,139,250,0.2); border: 1px solid rgba(167,139,250,0.4); border-radius: 12px 12px 4px 12px; padding: 12px 16px; margin: 8px 0 8px 40px; color: #e2e8f0; }
    .bot-msg { background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.3); border-radius: 12px 12px 12px 4px; padding: 12px 16px; margin: 8px 40px 8px 0; color: #e2e8f0; }
    .msg-label { font-size: 0.75rem; font-weight: 600; margin-bottom: 4px; opacity: 0.7; }
    .stTextInput > div > div > input { background: #1e1b4b !important; border: 2px solid #7c3aed !important; border-radius: 10px !important; color: #ffffff !important; font-size: 1rem !important; padding: 12px 16px !important; caret-color: #a78bfa !important; }
    .stTextInput > div > div > input::placeholder { color: #9ca3af !important; opacity: 1 !important; }
    .stButton > button { background: linear-gradient(135deg, #7c3aed, #2563eb) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 1rem !important; transition: all 0.2s ease !important; }
    .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(124,58,237,0.5) !important; }
    [data-testid="stSidebar"] .stButton > button { background: rgba(124,58,237,0.2) !important; border: 1px solid rgba(167,139,250,0.4) !important; color: #c4b5fd !important; font-size: 0.85rem !important; }
    [data-testid="stSidebar"] .stButton > button:hover { background: rgba(124,58,237,0.4) !important; color: #ffffff !important; }
    .stat-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; text-align: center; }
    .stat-number { font-size: 1.6rem; font-weight: 800; color: #a78bfa; }
    .stat-label { font-size: 0.75rem; color: #9ca3af; }
    .status-badge { display: inline-block; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .status-ready { background: rgba(52,211,153,0.2); color: #34d399; border: 1px solid rgba(52,211,153,0.4); }
    hr { border-color: rgba(255,255,255,0.1) !important; }
    p, span, label { color: #e2e8f0; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Knowledge Base ────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = """
ORGANIZATION OVERVIEW
BLECA SmartLabs is a startup of technology and innovation initiative focused on Artificial Intelligence AI, Software Engineering, Data Science, Smart Systems, Digital Transformation, and Research-based technology development located at CITT building in Mbeya University of Science and Technology MUST. The organization aims to empower students, developers, innovators, researchers, startups, and communities through modern intelligent technologies and practical digital solutions. BLECA stands for Building, Learning, Exploring, Creating and Advancing practical digital solutions.

VISION
The vision of BLECA SmartLabs is to become a leading African smart technology and AI innovation laboratory that transforms education, research, communities, and businesses through intelligent digital solutions.

MISSION
The mission of BLECA SmartLabs is to: Build intelligent systems for solving real-world problems. Promote innovation and digital transformation. Train future software engineers and AI developers. Advance AI and data science education. Develop scalable smart technologies. Support research and collaborative development. Create impactful digital platforms.

CORE OBJECTIVES
Develop AI-powered systems. Build modern web and mobile applications. Promote research and innovation. Train students in technology and programming. Integrate AI into real-world systems. Support digital transformation. Encourage problem-solving through technology.

MAIN FOCUS AREAS - ARTIFICIAL INTELLIGENCE
BLECA SmartLabs focuses on Artificial Intelligence including AI Chatbots, Natural Language Processing NLP, Machine Learning, Computer Vision, Recommendation Systems, Generative AI, and Predictive Analytics.

MAIN FOCUS AREAS - SOFTWARE ENGINEERING
BLECA SmartLabs focuses on Software Engineering including Web Development, Backend Development, Frontend Development, Mobile Development, API Development, Database Design, and Cloud Deployment.

MAIN FOCUS AREAS - DATA SCIENCE
BLECA SmartLabs focuses on Data Science including Data Analysis, Data Visualization, Statistical Analysis, Machine Learning Models, Climate Data Analysis, and Geospatial Analysis.

MAIN FOCUS AREAS - SMART SYSTEMS
BLECA SmartLabs focuses on Smart Systems including Smart Education Platforms, Smart Automation Systems, AI Assistants, Intelligent Dashboards, and Smart Monitoring Systems.

TECHNOLOGIES USED
Programming Languages used by BLECA: Python, JavaScript, Java, SQL, PHP, Kotlin, C++.
Frontend Technologies: HTML, CSS, React.js, Streamlit.
Backend Technologies: Flask, Django, FastAPI, Node.js.
Databases: MySQL, PostgreSQL, SQLite, MongoDB, Firebase.
AI and Machine Learning tools: Gemini AI, OpenAI APIs, TensorFlow, PyTorch, Scikit-learn, LangChain, Hugging Face Transformers.
Deployment Tools: GitHub, Docker, Render, Netlify, Vercel.

SMARTLABS CONCEPT
The term SmartLabs refers to a modern digital laboratory, a technology innovation environment, a research and experimentation center, and a collaborative development ecosystem. The SmartLabs environment encourages hands-on learning, experimentation, team collaboration, innovation, and project-based development.

SERVICES OFFERED - TECHNOLOGY
Technology Services offered by BLECA SmartLabs: Website Development, Mobile App Development, AI Chatbot Development, Data Analysis, Dashboard Development, Database Design, Automation Systems, API Integration.

SERVICES OFFERED - EDUCATION
Educational Services offered by BLECA SmartLabs: Programming Tutorials, AI Training, Data Science Mentorship, Software Engineering Workshops, Research Support, Technical Guidance.

SERVICES OFFERED - INNOVATION
Innovation Services offered by BLECA SmartLabs: Startup Technology Support, Prototype Development, Digital Transformation Consulting, Smart Systems Design.

TARGET USERS
BLECA SmartLabs serves: Students, Developers, Researchers, Startups, Schools, Universities, Businesses, Innovators, and Technology Enthusiasts.

AI CHATBOT AND RAG SYSTEMS
BLECA SmartLabs develops AI chatbot systems capable of answering user questions, searching knowledge bases, processing documents, providing intelligent responses, and supporting conversational AI. Features include RAG Systems, PDF Processing, Conversation Memory, Semantic Search, and AI Response Generation. RAG stands for Retrieval Augmented Generation. BLECA uses RAG systems where a user asks a question, the system searches a knowledge base, relevant information is retrieved, AI generates a contextual answer, and the response is returned to the user. RAG technologies include LangChain, ChromaDB, FAISS, Embedding Models, and Vector Databases.

SOFTWARE DEVELOPMENT PHILOSOPHY
BLECA SmartLabs develops AI Platforms, Smart Dashboards, Education Systems, Research Platforms, Data Analysis Tools, Mobile Applications, and Web Systems. Development Philosophy: Innovation First, Practical Learning, Real-World Impact, Open Collaboration, Continuous Improvement.

EDUCATIONAL PHILOSOPHY
BLECA SmartLabs promotes Learning by Doing, Real Projects, AI Literacy, Practical Skills, Collaborative Innovation, and Self-learning Culture.

FUTURE GOALS
Future goals of BLECA SmartLabs: Build an AI Research Center. Expand Smart Education Platforms. Create African AI Innovation Networks. Develop National Smart Systems. Contribute to Open Source Technologies. Support Startup Ecosystems.

ORGANIZATIONAL CULTURE
BLECA SmartLabs values: Creativity, Innovation, Research, Teamwork, Excellence, Technology Leadership, Continuous Learning.

GITHUB AND OPEN SOURCE
BLECA SmartLabs encourages GitHub Collaboration, Version Control, Open Source Contributions, Team-Based Development, and Documentation Practices.

TEAM STRUCTURE
Leadership of BLECA SmartLabs: Founder, Director, Technical Lead.
Technical Team: Software Engineers, AI Engineers, Data Scientists, Backend Developers, Frontend Developers, UI/UX Designers.
Research Team: Researchers, Analysts, Innovation Specialists.

EXAMPLE PROJECTS
Example projects by BLECA SmartLabs: AI Chatbots, Smart Education Platforms, Data Analytics Dashboards, Smart Monitoring Systems, AI Assistants, Intelligent Recommendation Systems, Research Platforms.

LOCATION AND CONTACT
BLECA SmartLabs is located at Mbeya University of Science and Technology MUST, CITT building, Mbeya, Tanzania, East Africa. Contact: Email bleca@smartlabs.co.tz. GitHub github.com/bleca-smartlabs. Location CITT building MUST Campus Mbeya Tanzania.

CO-FOUNDERS AND MEMBERS
The co-founders of BLECA SmartLabs are Blandina Kakore and Fedelika Maxmus. Other people associated with BLECA SmartLabs include Johnson Hassan, Chris Bwesa, and Bro Ipyana. BLECA SmartLabs is closely connected with the innovation ecosystem around Mbeya University of Science and Technology MUST in Tanzania.

SUMMARY
BLECA SmartLabs is a smart technology and AI innovation startup initiative focused on building intelligent systems, empowering developers and students, supporting research, and advancing digital transformation. It is located at CITT building MUST Mbeya Tanzania and serves students startups researchers and communities across East Africa with a vision to lead African AI innovation.
"""

# ─── Greeting Detection ────────────────────────────────────────────────────────
GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening",
             "howdy", "greetings", "hii", "helo", "hellow", "good day", "sup", "yo"]

GREETING_RESPONSES = [
    "Hello! 👋 Welcome to BLECA SmartLabs AI Assistant! I'm here to answer all your questions about BLECA SmartLabs. What would you like to know?",
    "Hi there! 😊 Great to have you here! I'm the BLECA SmartLabs AI Assistant. Feel free to ask me anything about BLECA SmartLabs — our vision, mission, team, services, and more!",
    "Hey! 🤖 Welcome! I'm your BLECA SmartLabs AI Assistant powered by Gemini AI. How can I help you today?",
    "Good day! 👋 I'm the BLECA SmartLabs AI Assistant. I can tell you everything about BLECA SmartLabs. What would you like to know?",
]

HOW_ARE_YOU_RESPONSES = [
    "I'm doing great, thank you for asking! 😊 I'm always ready to help you learn more about BLECA SmartLabs. What would you like to know?",
    "I'm wonderful and always ready to help! 🤖 What would you like to know about BLECA SmartLabs today?",
    "I'm fantastic! 😄 Always happy to assist! What would you like to know about BLECA SmartLabs?",
]

THANKS_RESPONSES = [
    "You're welcome! 😊 Feel free to ask more questions about BLECA SmartLabs anytime!",
    "Happy to help! 🤖 Is there anything else you'd like to know about BLECA SmartLabs?",
    "My pleasure! 😄 Don't hesitate to ask if you have more questions!",
]

def is_greeting(text):
    t = text.lower().strip().rstrip("!.,?")
    if t in GREETINGS:
        return True
    if len(t.split()) <= 3 and any(g in t for g in ["hi", "hello", "hey"]):
        return True
    return False

def is_how_are_you(text):
    t = text.lower()
    return any(p in t for p in ["how are you", "how r u", "how are u", "how're you", "hows it going", "how do you do"])

def is_thanks(text):
    t = text.lower().strip()
    return any(p in t for p in ["thank", "thanks", "thx", "ty ", "thank you", "great job", "well done", "awesome"])

# ─── FAISS RAG Setup ──────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def build_faiss_index():
    try:
        import faiss
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")

        # Split knowledge base into chunks
        chunks = []
        for paragraph in KNOWLEDGE_BASE.strip().split('\n\n'):
            paragraph = paragraph.strip()
            if len(paragraph) > 50:
                # Further split long paragraphs
                if len(paragraph) > 400:
                    sentences = paragraph.split('. ')
                    current = ""
                    for s in sentences:
                        if len(current) + len(s) < 400:
                            current += s + ". "
                        else:
                            if current.strip():
                                chunks.append(current.strip())
                            current = s + ". "
                    if current.strip():
                        chunks.append(current.strip())
                else:
                    chunks.append(paragraph)

        # Build embeddings
        embeddings = model.encode(chunks, show_progress_bar=False)
        embeddings = np.array(embeddings).astype('float32')

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        # Build FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)

        return model, index, chunks

    except Exception as e:
        return None, None, []

def search_faiss(question, model, index, chunks, top_k=3):
    try:
        import faiss
        query_vec = model.encode([question])
        query_vec = np.array(query_vec).astype('float32')
        faiss.normalize_L2(query_vec)
        scores, indices = index.search(query_vec, top_k)
        results = [chunks[i] for i in indices[0] if i < len(chunks)]
        return "\n\n".join(results)
    except:
        return ""

# ─── API Key Rotation ──────────────────────────────────────────────────────────
def get_api_keys():
    keys = []
    try:
        k = st.secrets.get("GOOGLE_API_KEY")
        if k: keys.append(k)
    except: pass
    try:
        k = st.secrets.get("GOOGLE_API_KEY_2")
        if k: keys.append(k)
    except: pass
    try:
        k = st.secrets.get("GOOGLE_API_KEY_3")
        if k: keys.append(k)
    except: pass
    return keys

def call_gemini(prompt, api_keys):
    keys = api_keys.copy()
    random.shuffle(keys)
    for key in keys:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 400}
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 429:
                continue
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return "⚠️ All API keys have reached their daily limit. Please try again tomorrow."

# ─── Main Answer Function ──────────────────────────────────────────────────────
def ask_bleca(question, api_keys, model, index, chunks):
    # Handle greetings — no API needed
    if is_greeting(question):
        return random.choice(GREETING_RESPONSES)

    if is_how_are_you(question):
        return random.choice(HOW_ARE_YOU_RESPONSES)

    if is_thanks(question):
        return random.choice(THANKS_RESPONSES)

    # RAG search
    if model is not None and index is not None:
        context = search_faiss(question, model, index, chunks, top_k=3)
    else:
        context = ""

    if not context:
        return "I could not find that information in the BLECA SmartLabs knowledge base. Please try asking about our vision, mission, team, services, location, or technologies."

    prompt = f"""You are the official BLECA SmartLabs AI Assistant. Always respond in clear, friendly, professional English.

STRICT RULES:
- Answer ONLY using the context provided below
- Do NOT use any outside knowledge
- If the answer is not in the context, say exactly: "I could not find that information in the BLECA SmartLabs knowledge base."
- Keep answers concise, helpful, and friendly
- Always respond in English only

CONTEXT:
{context}

QUESTION: {question}

Answer:"""

    return call_gemini(prompt, api_keys)

# ─── Initialize ───────────────────────────────────────────────────────────────
api_keys = get_api_keys()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 BLECA SmartLabs AI")
    st.markdown("Intelligent assistant powered by Gemini AI + FAISS RAG")
    st.markdown("---")

    st.markdown("## 📊 Session Stats")
    col1, col2 = st.columns(2)
    msgs_count = len(st.session_state.get("messages", []))
    with col1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{msgs_count // 2}</div><div class='stat-label'>Questions Asked</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{'✅' if api_keys else '❌'}</div><div class='stat-label'>{'Ready' if api_keys else 'No Key'}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div style='text-align:center; color:#34d399; font-size:0.85rem; padding:4px;'>🔑 {len(api_keys)} API Key(s) Active</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("## 💡 Sample Questions")
    samples = [
        "What is BLECA SmartLabs?",
        "What does BLECA stand for?",
        "Where is BLECA located?",
        "Who are the co-founders?",
        "What services does BLECA offer?",
        "What AI technologies does BLECA use?",
        "What is the vision of BLECA?",
        "What events does BLECA organize?",
    ]
    for q in samples:
        if st.button(q, use_container_width=True, key=f"s_{q[:15]}"):
            st.session_state["pending"] = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

    st.markdown("<div style='text-align:center; color:#6b7280; font-size:0.75rem; margin-top:1rem;'>Built with Gemini AI + FAISS + Streamlit<br>BLECA SmartLabs © 2025<br>MUST, Mbeya, Tanzania</div>", unsafe_allow_html=True)

# ─── Main UI ──────────────────────────────────────────────────────────────────
st.markdown("<div class='bleca-header'><h1>🤖 BLECA SmartLabs AI</h1><p>Your intelligent assistant for everything about BLECA SmartLabs</p></div>", unsafe_allow_html=True)

# Load FAISS index
with st.spinner("⚙️ Loading AI models... Please wait..."):
    embed_model, faiss_index, chunks = build_faiss_index()

if api_keys and embed_model is not None:
    st.markdown(f"<div style='text-align:center; margin-bottom:1rem;'><span class='status-badge status-ready'>✅ AI Ready — Gemini 2.0 Flash + FAISS RAG — {len(api_keys)} Keys Active</span></div>", unsafe_allow_html=True)
elif not api_keys:
    st.error("⚠️ No API Keys found. Please contact BLECA SmartLabs admin.")
else:
    st.warning("⚠️ FAISS index failed to load. Using basic search.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("---")

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'><div class='msg-label'>🙋 You</div>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><div class='msg-label'>🤖 BLECA AI</div>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("")
pending = st.session_state.pop("pending", None)
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_input = st.text_input(
        "Ask",
        value=pending or "",
        placeholder="e.g. What is BLECA SmartLabs?",
        label_visibility="collapsed",
        key="chat_input"
    )
with col_btn:
    send = st.button("Send 🚀", use_container_width=True)

if (send or pending) and user_input.strip():
    if not api_keys:
        st.error("⚠️ No API Keys found.")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("🤔 Thinking..."):
            answer = ask_bleca(user_input.strip(), api_keys, embed_model, faiss_index, chunks)
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.rerun()
