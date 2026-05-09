import streamlit as st
import google.generativeai as genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BLECA SmartLabs AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #f0f0f0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.05);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Header */
    .bleca-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .bleca-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .bleca-header p {
        color: #9ca3af;
        font-size: 1rem;
        margin-top: 0.5rem;
    }

    /* Chat messages */
    .user-msg {
        background: rgba(167,139,250,0.2);
        border: 1px solid rgba(167,139,250,0.4);
        border-radius: 12px 12px 4px 12px;
        padding: 12px 16px;
        margin: 8px 0 8px 40px;
        color: #e2e8f0;
    }
    .bot-msg {
        background: rgba(52,211,153,0.1);
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 12px 12px 12px 4px;
        padding: 12px 16px;
        margin: 8px 40px 8px 0;
        color: #e2e8f0;
    }
    .msg-label {
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 4px;
        opacity: 0.7;
    }

    /* Input box - comprehensive fix */
    .stTextInput > div > div > input {
        background: #1e1b4b !important;
        border: 2px solid #7c3aed !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
        caret-color: #a78bfa !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }
    .stTextInput label {
        color: #e2e8f0 !important;
    }
    p, span, label { color: #e2e8f0; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #1e1b4b !important;
        border: 2px solid #7c3aed !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 12px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(124,58,237,0.5) !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(124,58,237,0.2) !important;
        border: 1px solid rgba(167,139,250,0.4) !important;
        color: #c4b5fd !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(124,58,237,0.4) !important;
        color: #ffffff !important;
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-ready {
        background: rgba(52,211,153,0.2);
        color: #34d399;
        border: 1px solid rgba(52,211,153,0.4);
    }
    .status-error {
        background: rgba(239,68,68,0.2);
        color: #f87171;
        border: 1px solid rgba(239,68,68,0.4);
    }
    
    /* Stats cards */
    .stat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
    }
    .stat-number {
        font-size: 1.6rem;
        font-weight: 800;
        color: #a78bfa;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #9ca3af;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.1) !important; }

    /* Scrollable chat area */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Knowledge Base ────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = """
BLECA SMARTLABS KNOWLEDGE BASE
================================

1. ORGANIZATION OVERVIEW
------------------------
BLECA SmartLabs is a technology and innovation initiative focused on Artificial Intelligence (AI),
Software Engineering, Data Science, Smart Systems, Digital Transformation, and Research-based
technology development.

The organization aims to empower students, developers, innovators, researchers, startups, and
communities through modern intelligent technologies and practical digital solutions.

BLECA SmartLabs combines:
- Artificial Intelligence
- Machine Learning
- Data Science
- Software Engineering
- Research and Innovation
- Smart Education Systems
- Intelligent Applications
- Digital Transformation

2. VISION
----------
To become a leading African smart technology and AI innovation laboratory that transforms
education, research, communities, and businesses through intelligent digital solutions.

3. MISSION
-----------
BLECA SmartLabs aims to:
- Build intelligent systems for solving real-world problems
- Promote innovation and digital transformation
- Train future software engineers and AI developers
- Advance AI and data science education
- Develop scalable smart technologies
- Support research and collaborative development
- Create impactful digital platforms

4. CORE OBJECTIVES
-------------------
- Develop AI-powered systems
- Build modern web and mobile applications
- Promote research and innovation
- Train students in technology and programming
- Integrate AI into real-world systems
- Support digital transformation
- Encourage problem-solving through technology

5. MAIN FOCUS AREAS
--------------------

A. Artificial Intelligence
- AI Chatbots
- Natural Language Processing (NLP)
- Machine Learning
- Computer Vision
- Recommendation Systems
- Generative AI
- Predictive Analytics

B. Software Engineering
- Web Development
- Backend Development
- Frontend Development
- Mobile Development
- API Development
- Database Design
- Cloud Deployment

C. Data Science
- Data Analysis
- Data Visualization
- Statistical Analysis
- Machine Learning Models
- Climate Data Analysis
- Geospatial Analysis

D. Smart Systems
- Smart Education Platforms
- Smart Automation Systems
- AI Assistants
- Intelligent Dashboards
- Smart Monitoring Systems

6. TECHNOLOGIES USED
---------------------

Programming Languages:
- Python
- JavaScript
- Java
- SQL
- PHP
- Kotlin
- C++

Frontend Technologies:
- HTML
- CSS
- React.js
- Streamlit

Backend Technologies:
- Flask
- Django
- FastAPI
- Node.js

Databases:
- MySQL
- PostgreSQL
- SQLite
- MongoDB
- Firebase

AI and Machine Learning:
- Gemini AI
- OpenAI APIs
- TensorFlow
- PyTorch
- Scikit-learn
- LangChain
- Hugging Face Transformers

Deployment Tools:
- GitHub
- Docker
- Render
- Netlify
- Vercel

7. SMARTLABS CONCEPT
---------------------
The term "SmartLabs" refers to:
- A modern digital laboratory
- A technology innovation environment
- A research and experimentation center
- A collaborative development ecosystem

The SmartLabs environment encourages:
- Hands-on learning
- Experimentation
- Team collaboration
- Innovation
- Project-based development

8. SERVICES OFFERED
--------------------

Technology Services:
- Website Development
- Mobile App Development
- AI Chatbot Development
- Data Analysis
- Dashboard Development
- Database Design
- Automation Systems
- API Integration

Educational Services:
- Programming Tutorials
- AI Training
- Data Science Mentorship
- Software Engineering Workshops
- Research Support
- Technical Guidance

Innovation Services:
- Startup Technology Support
- Prototype Development
- Digital Transformation Consulting
- Smart Systems Design

9. TARGET USERS
----------------
BLECA SmartLabs serves:
- Students
- Developers
- Researchers
- Startups
- Schools
- Universities
- Businesses
- Innovators
- Technology Enthusiasts

10. AI CHATBOT SYSTEMS
-----------------------
BLECA SmartLabs develops AI chatbot systems capable of:
- Answering user questions
- Searching knowledge bases
- Processing documents
- Providing intelligent responses
- Supporting conversational AI

Features include:
- RAG Systems
- PDF Processing
- Conversation Memory
- Semantic Search
- AI Response Generation

11. RETRIEVAL AUGMENTED GENERATION (RAG)
-----------------------------------------
BLECA SmartLabs uses RAG systems where:
1. A user asks a question
2. The system searches a knowledge base
3. Relevant information is retrieved
4. AI generates a contextual answer
5. The response is returned to the user

RAG technologies include:
- LangChain
- ChromaDB
- FAISS
- Embedding Models
- Vector Databases

12. STREAMLIT APPLICATIONS
---------------------------
BLECA SmartLabs develops Streamlit-based applications for:
- AI Dashboards
- Interactive Data Analysis
- Machine Learning Interfaces
- Chatbot Systems
- Visualization Platforms

Features may include:
- File Uploads
- PDF Analysis
- AI Conversations
- Charts and Dashboards
- User Authentication

13. SOFTWARE DEVELOPMENT
-------------------------
BLECA SmartLabs develops:
- AI Platforms
- Smart Dashboards
- Education Systems
- Research Platforms
- Data Analysis Tools
- Mobile Applications
- Web Systems

Development Philosophy:
- Innovation First
- Practical Learning
- Real-World Impact
- Open Collaboration
- Continuous Improvement

14. EDUCATIONAL PHILOSOPHY
---------------------------
BLECA SmartLabs promotes:
- Learning by Doing
- Real Projects
- AI Literacy
- Practical Skills
- Collaborative Innovation
- Self-learning Culture

15. POTENTIAL FUTURE GOALS
---------------------------
- Build an AI Research Center
- Expand Smart Education Platforms
- Create African AI Innovation Networks
- Develop National Smart Systems
- Contribute to Open Source Technologies
- Support Startup Ecosystems

16. GITHUB AND OPEN SOURCE
---------------------------
BLECA SmartLabs encourages:
- GitHub Collaboration
- Version Control
- Open Source Contributions
- Team-Based Development
- Documentation Practices

17. ORGANIZATIONAL CULTURE
---------------------------
BLECA SmartLabs values:
- Creativity
- Innovation
- Research
- Teamwork
- Excellence
- Technology Leadership
- Continuous Learning

18. POSSIBLE TEAM STRUCTURE
----------------------------
Leadership:
- Founder
- Director
- Technical Lead

Technical Team:
- Software Engineers
- AI Engineers
- Data Scientists
- Backend Developers
- Frontend Developers
- UI/UX Designers

Research Team:
- Researchers
- Analysts
- Innovation Specialists

19. EXAMPLE PROJECTS
---------------------
- AI Chatbots
- Smart Education Platforms
- Data Analytics Dashboards
- Smart Monitoring Systems
- AI Assistants
- Intelligent Recommendation Systems
- Research Platforms

20. COMMON CHATBOT QUESTIONS AND ANSWERS
-----------------------------------------
Q: What is BLECA SmartLabs?
A: BLECA SmartLabs is an AI and software innovation laboratory focused on intelligent systems,
smart technologies, research, education, and digital transformation.

Q: What technologies does BLECA use?
A: BLECA uses Python, JavaScript, React.js, Flask, FastAPI, Gemini AI, TensorFlow, ChromaDB,
LangChain, MySQL, PostgreSQL, Docker, and many more modern technologies.

Q: Does BLECA build AI systems?
A: Yes. BLECA SmartLabs builds AI chatbots, RAG systems, machine learning models, computer
vision systems, NLP tools, and AI-powered dashboards.

Q: What is RAG?
A: RAG stands for Retrieval Augmented Generation. It is a technique where an AI system
searches a knowledge base first, retrieves relevant information, then generates a
contextual answer using an AI language model.

Q: Does BLECA teach programming?
A: Yes. BLECA SmartLabs offers programming tutorials, AI training, data science mentorship,
and software engineering workshops.

Q: What services does BLECA offer?
A: BLECA offers website development, mobile app development, AI chatbot development,
data analysis, dashboard development, automation systems, and educational services.

Q: What projects does BLECA develop?
A: BLECA develops AI chatbots, smart education platforms, data analytics dashboards,
smart monitoring systems, AI assistants, recommendation systems, and research platforms.

Q: Does BLECA support students?
A: Yes. BLECA SmartLabs strongly supports students through mentorship, workshops,
real project experience, and practical technology training.

Q: What is the vision of BLECA SmartLabs?
A: The vision is to become a leading African smart technology and AI innovation laboratory
that transforms education, research, communities, and businesses through intelligent digital solutions.

Q: What is the mission of BLECA SmartLabs?
A: The mission is to build intelligent systems, promote innovation, train future AI developers,
advance AI education, and support digital transformation across Africa.

21. IMPORTANT KEYWORDS
-----------------------
AI, Machine Learning, Data Science, Software Engineering, Innovation, Research,
Digital Transformation, Chatbot, RAG, Automation, Smart Systems, Education Technology,
Analytics, Cloud Computing, BLECA, SmartLabs, Tanzania, Africa, Gemini, Python, Streamlit

22. FINAL SUMMARY
------------------
BLECA SmartLabs is a smart technology and AI innovation initiative focused on building
intelligent systems, empowering developers and students, supporting research, and advancing
digital transformation using modern technologies such as Artificial Intelligence, Machine
Learning, Software Engineering, and Data Science. It serves students, startups, researchers,
and communities, with a vision to lead African AI innovation.

END OF KNOWLEDGE BASE
"""

# ─── Embedding Wrapper ────────────────────────────────────────────────────────
class EmbeddingWrapper:
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

# ─── Cached RAG Setup ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def setup_rag(api_key: str):
    genai.configure(api_key=api_key)
    gemini = genai.GenerativeModel("gemini-2.5-flash")

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=80)
    chunks = splitter.split_text(KNOWLEDGE_BASE)

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding_fn = EmbeddingWrapper(embedding_model)

    db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_fn,
        persist_directory="chroma_db_v2",
    )
    return gemini, db, len(chunks)


def ask_rag(question: str, gemini, db) -> str:
    docs = db.similarity_search(question, k=4)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""You are BLECA SmartLabs AI Assistant.

RULES:
- Use ONLY the context below
- Do NOT guess or use outside knowledge
- If information is missing, say: "I could not find that information in the BLECA SmartLabs knowledge base."

-------------------
CONTEXT:
{context}
-------------------

QUESTION:
{question}

Answer clearly and accurately."""

    response = gemini.generate_content(
        prompt,
        generation_config={"temperature": 0.1},
    )
    return response.text


# ─── API Key from Streamlit Secrets ──────────────────────────────────────────
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = None

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 BLECA SmartLabs AI")
    st.markdown("Your intelligent AI assistant powered by Gemini + RAG")
    st.markdown("---")
    st.markdown("## 📊 Session Stats")

    col1, col2 = st.columns(2)
    msgs_count = len(st.session_state.get("messages", []))
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{msgs_count // 2}</div>
            <div class='stat-label'>Questions Asked</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        status = "Ready" if api_key else "No Key"
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{'✅' if api_key else '❌'}</div>
            <div class='stat-label'>{status}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 💡 Sample Questions")
    sample_questions = [
        "What is BLECA SmartLabs?",
        "Who is Johnson Hassan?",
        "What AI technologies does BLECA use?",
        "What events does BLECA organize?",
        "What skills can members gain?",
    ]
    for q in sample_questions:
        if st.button(q, use_container_width=True, key=f"sample_{q[:20]}"):
            st.session_state["pending_question"] = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

    st.markdown("""
    <div style='text-align:center; color:#6b7280; font-size:0.75rem; margin-top:1rem;'>
        Built with Gemini + ChromaDB + Streamlit<br>
        BLECA SmartLabs © 2025
    </div>
    """, unsafe_allow_html=True)

# ─── Main UI ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class='bleca-header'>
    <h1>🤖 BLECA SmartLabs AI</h1>
    <p>Your intelligent assistant for everything about BLECA SmartLabs</p>
</div>
""", unsafe_allow_html=True)

# Init session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Load RAG
gemini_model = None
chroma_db = None
chunk_count = 0

if api_key:
    with st.spinner("⚙️ Loading AI models... (first time may take ~30s)"):
        try:
            gemini_model, chroma_db, chunk_count = setup_rag(api_key)
            st.markdown(f"""
            <div style='text-align:center; margin-bottom:1rem;'>
                <span class='status-badge status-ready'>
                    ✅ RAG Ready — {chunk_count} knowledge chunks indexed
                </span>
            </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div style='text-align:center; margin-bottom:1rem;'>
                <span class='status-badge status-error'>❌ Error: {str(e)[:60]}</span>
            </div>""", unsafe_allow_html=True)
else:
    st.error("⚠️ API Key haipo. Wasiliana na admin wa BLECA SmartLabs.")

st.markdown("---")

# Chat display
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='user-msg'>
            <div class='msg-label'>🙋 You</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='bot-msg'>
            <div class='msg-label'>🤖 BLECA AI</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)

# Input
st.markdown("")
col_input, col_btn = st.columns([5, 1])

pending = st.session_state.pop("pending_question", None)

with col_input:
    user_input = st.text_input(
        "Ask a question",
        value=pending or "",
        placeholder="e.g. What is BLECA SmartLabs?",
        label_visibility="collapsed",
        key="chat_input",
    )

with col_btn:
    send = st.button("Send 🚀", use_container_width=True)

# Handle send
if (send or pending) and user_input.strip():
    if not api_key:
        st.error("⚠️ API Key haipo. Wasiliana na admin.")
    elif gemini_model is None:
        st.error("AI model failed to load. Check your API key.")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("🤔 Thinking..."):
            try:
                answer = ask_rag(user_input.strip(), gemini_model, chroma_db)
            except Exception as e:
                answer = f"⚠️ Error generating response: {str(e)}"
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.rerun()
