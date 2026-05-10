import streamlit as st
import requests

st.set_page_config(
    page_title="BLECA SmartLabs AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    [data-testid="stSidebar"] .stButton > button { background: rgba(124,58,237,0.2) !important; border: 1px solid rgba(167,139,250,0.4) !important; color: #c4b5fd !important; font-size: 0.85rem !important; font-weight: 500 !important; }
    [data-testid="stSidebar"] .stButton > button:hover { background: rgba(124,58,237,0.4) !important; color: #ffffff !important; }
    .stat-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; text-align: center; }
    .stat-number { font-size: 1.6rem; font-weight: 800; color: #a78bfa; }
    .stat-label { font-size: 0.75rem; color: #9ca3af; }
    .status-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .status-ready { background: rgba(52,211,153,0.2); color: #34d399; border: 1px solid rgba(52,211,153,0.4); }
    hr { border-color: rgba(255,255,255,0.1) !important; }
    p, span, label { color: #e2e8f0; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

KNOWLEDGE_BASE = """
BLECA SMARTLABS KNOWLEDGE BASE
================================

1. ORGANIZATION OVERVIEW
BLECA SmartLabs is a technology and innovation initiative focused on Artificial Intelligence (AI), Software Engineering, Data Science, Smart Systems, Digital Transformation, and Research-based technology development. The organization aims to empower students, developers, innovators, researchers, startups, and communities through modern intelligent technologies and practical digital solutions.

2. VISION
To become a leading African smart technology and AI innovation laboratory that transforms education, research, communities, and businesses through intelligent digital solutions.

3. MISSION
BLECA SmartLabs aims to: Build intelligent systems for solving real-world problems. Promote innovation and digital transformation. Train future software engineers and AI developers. Advance AI and data science education. Develop scalable smart technologies. Support research and collaborative development. Create impactful digital platforms.

4. LOCATION AND CONTACT
BLECA SmartLabs is located at Mbeya University of Science and Technology (MUST), Mbeya, Tanzania, East Africa. The organization operates within MUST Campus, Mbeya City, Tanzania. Contact: bleca@smartlabs.co.tz. GitHub: github.com/bleca-smartlabs. Location: MUST Campus, Mbeya City, Tanzania.

5. CO-FOUNDERS AND TEAM
Co-founders of BLECA SmartLabs include Blandina Kakore and other founding members who established the innovation community at MUST campus. Team members include Johnson Hassan known for AI mentorship and engineering innovation. Jofrey Nasson known for machine learning and Python development. Fedelika Maxmus associated with IEEE representation. Jonathan Ndali known for leadership mentorship and youth empowerment.

6. CORE OBJECTIVES
Develop AI-powered systems. Build modern web and mobile applications. Promote research and innovation. Train students in technology and programming. Integrate AI into real-world systems. Support digital transformation. Encourage problem-solving through technology.

7. MAIN FOCUS AREAS
A. Artificial Intelligence: AI Chatbots, Natural Language Processing NLP, Machine Learning, Computer Vision, Recommendation Systems, Generative AI, Predictive Analytics.
B. Software Engineering: Web Development, Backend Development, Frontend Development, Mobile Development, API Development, Database Design, Cloud Deployment.
C. Data Science: Data Analysis, Data Visualization, Statistical Analysis, Machine Learning Models, Climate Data Analysis, Geospatial Analysis.
D. Smart Systems: Smart Education Platforms, Smart Automation Systems, AI Assistants, Intelligent Dashboards, Smart Monitoring Systems.

8. TECHNOLOGIES USED
Programming Languages: Python, JavaScript, Java, SQL, PHP, Kotlin, C++.
Frontend Technologies: HTML, CSS, React.js, Streamlit.
Backend Technologies: Flask, Django, FastAPI, Node.js.
Databases: MySQL, PostgreSQL, SQLite, MongoDB, Firebase.
AI and Machine Learning: Gemini AI, OpenAI APIs, TensorFlow, PyTorch, Scikit-learn, LangChain, Hugging Face Transformers.
Deployment Tools: GitHub, Docker, Render, Netlify, Vercel.

9. SERVICES OFFERED
Technology Services: Website Development, Mobile App Development, AI Chatbot Development, Data Analysis, Dashboard Development, Database Design, Automation Systems, API Integration.
Educational Services: Programming Tutorials, AI Training, Data Science Mentorship, Software Engineering Workshops, Research Support, Technical Guidance.
Innovation Services: Startup Technology Support, Prototype Development, Digital Transformation Consulting, Smart Systems Design.

10. TARGET USERS
Students, Developers, Researchers, Startups, Schools, Universities, Businesses, Innovators, Technology Enthusiasts.

11. AI CHATBOT SYSTEMS
BLECA SmartLabs develops AI chatbot systems capable of answering user questions, searching knowledge bases, processing documents, providing intelligent responses, and supporting conversational AI. Features include RAG Systems, PDF Processing, Conversation Memory, Semantic Search, AI Response Generation.

12. RETRIEVAL AUGMENTED GENERATION RAG
BLECA SmartLabs uses RAG systems where a user asks a question, the system searches a knowledge base, relevant information is retrieved, AI generates a contextual answer, and the response is returned to the user. RAG technologies include LangChain, ChromaDB, FAISS, Embedding Models, Vector Databases.

13. ACTIVITIES AND EVENTS
AI Hackathons: BLECA SmartLabs members participate in AI hackathons, innovation competitions, and technology challenges.
Engineering Day Events: BLECA SmartLabs is represented during engineering exhibitions, technology showcases, and innovation presentations.
Mentorship Programs: Tech mentorship, AI learning guidance, leadership discussions, and career growth sessions.
Community Outreach: Teaching coding, STEM practical training, supporting younger students, and innovation awareness.

14. ORGANIZATIONAL CULTURE
BLECA SmartLabs values Creativity, Innovation, Research, Teamwork, Excellence, Technology Leadership, Continuous Learning.

15. EDUCATIONAL PHILOSOPHY
BLECA SmartLabs promotes Learning by Doing, Real Projects, AI Literacy, Practical Skills, Collaborative Innovation, Self-learning Culture.

16. FUTURE GOALS
Build an AI Research Center. Expand Smart Education Platforms. Create African AI Innovation Networks. Develop National Smart Systems. Contribute to Open Source Technologies. Support Startup Ecosystems.

17. EXAMPLE PROJECTS
AI Chatbots, Smart Education Platforms, Data Analytics Dashboards, Smart Monitoring Systems, AI Assistants, Intelligent Recommendation Systems, Research Platforms, EasyHostel smart student accommodation platform.

18. FINAL SUMMARY
BLECA SmartLabs is a smart technology and AI innovation initiative focused on building intelligent systems, empowering developers and students, supporting research, and advancing digital transformation using modern technologies such as Artificial Intelligence, Machine Learning, Software Engineering, and Data Science. It is located at MUST, Mbeya, Tanzania and serves students, startups, researchers, and communities across East Africa.
"""

def search_knowledge(question):
    question_lower = question.lower()
    paragraphs = [p.strip() for p in KNOWLEDGE_BASE.split('\n') if len(p.strip()) > 40]
    scored = []
    question_words = set(question_lower.split())
    for para in paragraphs:
        para_lower = para.lower()
        score = sum(1 for word in question_words if word in para_lower)
        if score > 0:
            scored.append((score, para))
    scored.sort(reverse=True)
    top = [p for _, p in scored[:5]]
    return '\n\n'.join(top) if top else ""

def ask_gemini(question, api_key):
    context = search_knowledge(question)
    if not context:
        return "I could not find that information in the BLECA SmartLabs knowledge base."
    
    prompt = f"""You are BLECA SmartLabs AI Assistant.

RULES:
- Use ONLY the context below to answer
- Do NOT guess or use outside knowledge  
- If information is missing say: "I could not find that information in the BLECA SmartLabs knowledge base."
- Be clear and helpful

CONTEXT:
{context}

QUESTION: {question}

Answer clearly and accurately:"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 500}
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {str(e)}"

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = None

with st.sidebar:
    st.markdown("## 🤖 BLECA SmartLabs AI")
    st.markdown("Your intelligent AI assistant powered by Gemini + RAG")
    st.markdown("---")
    st.markdown("## 📊 Session Stats")
    col1, col2 = st.columns(2)
    msgs_count = len(st.session_state.get("messages", []))
    with col1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{msgs_count // 2}</div><div class='stat-label'>Questions Asked</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{'✅' if api_key else '❌'}</div><div class='stat-label'>{'Ready' if api_key else 'No Key'}</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 💡 Sample Questions")
    samples = ["What is BLECA SmartLabs?", "Where is BLECA located?", "Who are the co-founders?", "What AI technologies does BLECA use?", "What events does BLECA organize?"]
    for q in samples:
        if st.button(q, use_container_width=True, key=f"s_{q[:15]}"):
            st.session_state["pending"] = q
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    st.markdown("<div style='text-align:center; color:#6b7280; font-size:0.75rem; margin-top:1rem;'>Built with Gemini + Streamlit<br>BLECA SmartLabs © 2025</div>", unsafe_allow_html=True)

st.markdown("<div class='bleca-header'><h1>🤖 BLECA SmartLabs AI</h1><p>Your intelligent assistant for everything about BLECA SmartLabs</p></div>", unsafe_allow_html=True)

if api_key:
    st.markdown("<div style='text-align:center; margin-bottom:1rem;'><span class='status-badge status-ready'>✅ AI Ready — Gemini 1.5 Flash</span></div>", unsafe_allow_html=True)
else:
    st.error("⚠️ API Key haipo. Wasiliana na admin wa BLECA SmartLabs.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("---")

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'><div class='msg-label'>🙋 You</div>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><div class='msg-label'>🤖 BLECA AI</div>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("")
pending = st.session_state.pop("pending", None)
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_input = st.text_input("Ask", value=pending or "", placeholder="e.g. What is BLECA SmartLabs?", label_visibility="collapsed", key="chat_input")
with col_btn:
    send = st.button("Send 🚀", use_container_width=True)

if (send or pending) and user_input.strip():
    if not api_key:
        st.error("⚠️ API Key haipo.")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("🤔 Thinking..."):
            answer = ask_gemini(user_input.strip(), api_key)
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.rerun()
