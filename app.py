import streamlit as st
import requests
import random

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

# ─── Knowledge Base ────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = """
1. ORGANIZATION OVERVIEW
BLECA SmartLabs is a startup of technology and innovation initiative focused on Artificial Intelligence (AI), Software Engineering, Data Science, Smart Systems, Digital Transformation, and Research-based technology development located at CITT building in Mbeya University of Science and Technology (MUST). The organization aims to empower students, developers, innovators, researchers, startups, and communities through modern intelligent technologies and practical digital solutions. BLECA stands for Building, Learning, Exploring, Creating and Advancing practical digital solutions.

BLECA SmartLabs combines: Artificial Intelligence, Machine Learning, Data Science, Software Engineering, Research and Innovation, Smart Education Systems, Intelligent Applications, Digital Transformation.

2. VISION
To become a leading African smart technology and AI innovation laboratory that transforms education, research, communities, and businesses through intelligent digital solutions.

3. MISSION
BLECA SmartLabs aims to: Build intelligent systems for solving real-world problems. Promote innovation and digital transformation. Train future software engineers and AI developers. Advance AI and data science education. Develop scalable smart technologies. Support research and collaborative development. Create impactful digital platforms.

4. CORE OBJECTIVES
Develop AI-powered systems. Build modern web and mobile applications. Promote research and innovation. Train students in technology and programming. Integrate AI into real-world systems. Support digital transformation. Encourage problem-solving through technology.

5. MAIN FOCUS AREAS
A. Artificial Intelligence: AI Chatbots, Natural Language Processing NLP, Machine Learning, Computer Vision, Recommendation Systems, Generative AI, Predictive Analytics.
B. Software Engineering: Web Development, Backend Development, Frontend Development, Mobile Development, API Development, Database Design, Cloud Deployment.
C. Data Science: Data Analysis, Data Visualization, Statistical Analysis, Machine Learning Models, Climate Data Analysis, Geospatial Analysis.
D. Smart Systems: Smart Education Platforms, Smart Automation Systems, AI Assistants, Intelligent Dashboards, Smart Monitoring Systems.

6. TECHNOLOGIES USED
Programming Languages: Python, JavaScript, Java, SQL, PHP, Kotlin, C++.
Frontend Technologies: HTML, CSS, React.js, Streamlit.
Backend Technologies: Flask, Django, FastAPI, Node.js.
Databases: MySQL, PostgreSQL, SQLite, MongoDB, Firebase.
AI and Machine Learning: Gemini AI, OpenAI APIs, TensorFlow, PyTorch, Scikit-learn, LangChain, Hugging Face Transformers.
Deployment Tools: GitHub, Docker, Render, Netlify, Vercel.

7. SMARTLABS CONCEPT
The term SmartLabs refers to: A modern digital laboratory, A technology innovation environment, A research and experimentation center, A collaborative development ecosystem. The SmartLabs environment encourages: Hands-on learning, Experimentation, Team collaboration, Innovation, Project-based development.

8. SERVICES OFFERED
Technology Services: Website Development, Mobile App Development, AI Chatbot Development, Data Analysis, Dashboard Development, Database Design, Automation Systems, API Integration.
Educational Services: Programming Tutorials, AI Training, Data Science Mentorship, Software Engineering Workshops, Research Support, Technical Guidance.
Innovation Services: Startup Technology Support, Prototype Development, Digital Transformation Consulting, Smart Systems Design.

9. TARGET USERS
BLECA SmartLabs serves: Students, Developers, Researchers, Startups, Schools, Universities, Businesses, Innovators, Technology Enthusiasts.

10. AI CHATBOT SYSTEMS
BLECA SmartLabs develops AI chatbot systems capable of: Answering user questions, Searching knowledge bases, Processing documents, Providing intelligent responses, Supporting conversational AI. Features include: RAG Systems, PDF Processing, Conversation Memory, Semantic Search, AI Response Generation.

11. RETRIEVAL AUGMENTED GENERATION RAG
BLECA SmartLabs uses RAG systems where: A user asks a question, the system searches a knowledge base, relevant information is retrieved, AI generates a contextual answer, and the response is returned to the user. RAG technologies include: LangChain, ChromaDB, FAISS, Embedding Models, Vector Databases.

12. SOFTWARE DEVELOPMENT
BLECA SmartLabs develops: AI Platforms, Smart Dashboards, Education Systems, Research Platforms, Data Analysis Tools, Mobile Applications, Web Systems. Development Philosophy: Innovation First, Practical Learning, Real-World Impact, Open Collaboration, Continuous Improvement.

13. EDUCATIONAL PHILOSOPHY
BLECA SmartLabs promotes: Learning by Doing, Real Projects, AI Literacy, Practical Skills, Collaborative Innovation, Self-learning Culture.

14. FUTURE GOALS
Build an AI Research Center. Expand Smart Education Platforms. Create African AI Innovation Networks. Develop National Smart Systems. Contribute to Open Source Technologies. Support Startup Ecosystems.

15. ORGANIZATIONAL CULTURE
BLECA SmartLabs values: Creativity, Innovation, Research, Teamwork, Excellence, Technology Leadership, Continuous Learning.

16. TEAM STRUCTURE
Leadership: Founder, Director, Technical Lead.
Technical Team: Software Engineers, AI Engineers, Data Scientists, Backend Developers, Frontend Developers, UI/UX Designers.
Research Team: Researchers, Analysts, Innovation Specialists.

17. EXAMPLE PROJECTS
AI Chatbots, Smart Education Platforms, Data Analytics Dashboards, Smart Monitoring Systems, AI Assistants, Intelligent Recommendation Systems, Research Platforms.

18. COMMON QUESTIONS AND ANSWERS
Q: What is BLECA SmartLabs? A: BLECA SmartLabs is an AI and software innovation startup laboratory focused on intelligent systems, smart technologies, research, education, and digital transformation located at CITT building, MUST, Mbeya Tanzania.
Q: What does BLECA stand for? A: BLECA stands for Building, Learning, Exploring, Creating and Advancing practical digital solutions.
Q: What technologies does BLECA use? A: BLECA uses Python, JavaScript, React.js, Flask, FastAPI, Gemini AI, TensorFlow, LangChain, MySQL, PostgreSQL, Docker, and many more modern technologies.
Q: Does BLECA build AI systems? A: Yes. BLECA SmartLabs builds AI chatbots, RAG systems, machine learning models, computer vision systems, NLP tools, and AI-powered dashboards.
Q: What is RAG? A: RAG stands for Retrieval Augmented Generation. It is a technique where an AI system searches a knowledge base first, retrieves relevant information, then generates a contextual answer using an AI language model.
Q: Does BLECA teach programming? A: Yes. BLECA SmartLabs offers programming tutorials, AI training, data science mentorship, and software engineering workshops.
Q: What services does BLECA offer? A: BLECA offers website development, mobile app development, AI chatbot development, data analysis, dashboard development, automation systems, and educational services.
Q: What is the vision of BLECA SmartLabs? A: The vision is to become a leading African smart technology and AI innovation laboratory that transforms education, research, communities, and businesses through intelligent digital solutions.
Q: What is the mission of BLECA SmartLabs? A: The mission is to build intelligent systems, promote innovation, train future AI developers, advance AI education, and support digital transformation across Africa.
Q: Does BLECA support students? A: Yes. BLECA SmartLabs strongly supports students through mentorship, workshops, real project experience, and practical technology training.

19. LOCATION AND CONTACT
BLECA SmartLabs is located at: Mbeya University of Science and Technology MUST, CITT building, Mbeya, Tanzania, East Africa.
Contact and Social Media: GitHub: github.com/bleca-smartlabs, Email: bleca@smartlabs.co.tz, Location: CITT building MUST Campus, Mbeya, Tanzania.

20. CO-FOUNDERS AND MEMBERS
The co-founders of BLECA SmartLabs are Blandina Kakore and Fedelika Maxmus. Other people associated with BLECA SmartLabs include Johnson Hassan, Chris Bwesa, and Bro Ipyana. BLECA SmartLabs is closely connected with the innovation ecosystem around Mbeya University of Science and Technology MUST.

21. FINAL SUMMARY
BLECA SmartLabs is a smart technology and AI innovation startup initiative focused on building intelligent systems, empowering developers and students, supporting research, and advancing digital transformation using modern technologies such as Artificial Intelligence, Machine Learning, Software Engineering, and Data Science. It is located at CITT building, MUST, Mbeya, Tanzania and serves students, startups, researchers, and communities across East Africa with a vision to lead African AI innovation.
"""

# ─── Greeting Detection ────────────────────────────────────────────────────────
GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening",
             "howdy", "greetings", "what's up", "how are you", "how r u", "sup",
             "hii", "helo", "hellow", "how are you doing", "good day"]

GREETING_RESPONSES = [
    "Hello! 👋 Welcome to BLECA SmartLabs AI Assistant! I'm here to answer all your questions about BLECA SmartLabs. What would you like to know?",
    "Hi there! 😊 Great to have you here! I'm the BLECA SmartLabs AI Assistant. Feel free to ask me anything about BLECA SmartLabs!",
    "Hey! 🤖 Welcome! I'm your BLECA SmartLabs AI Assistant powered by Gemini AI. How can I help you today?",
    "Good day! 👋 I'm the BLECA SmartLabs AI Assistant. I can tell you everything about BLECA SmartLabs — our vision, mission, team, services, and more. What would you like to know?",
]

HOW_ARE_YOU_RESPONSES = [
    "I'm doing great, thank you for asking! 😊 I'm always ready to help you learn more about BLECA SmartLabs. What would you like to know?",
    "I'm wonderful! Thanks for asking! 🤖 I'm here and ready to answer all your questions about BLECA SmartLabs. How can I assist you?",
    "I'm fantastic! 😄 Always happy to chat and help! What would you like to know about BLECA SmartLabs today?",
]

def is_greeting(text):
    text_lower = text.lower().strip()
    for g in GREETINGS:
        if g in text_lower or text_lower == g:
            return True
    if len(text_lower.split()) <= 4 and any(g in text_lower for g in ["hi", "hello", "hey", "howdy"]):
        return True
    return False

def is_how_are_you(text):
    text_lower = text.lower()
    return any(p in text_lower for p in ["how are you", "how r u", "how are u", "how're you", "hows it going"])

# ─── API Key Rotation ──────────────────────────────────────────────────────────
def get_api_keys():
    keys = []
    try:
        k1 = st.secrets.get("GOOGLE_API_KEY")
        if k1: keys.append(k1)
    except: pass
    try:
        k2 = st.secrets.get("GOOGLE_API_KEY_2")
        if k2: keys.append(k2)
    except: pass
    try:
        k3 = st.secrets.get("GOOGLE_API_KEY_3")
        if k3: keys.append(k3)
    except: pass
    return keys

def call_gemini(prompt, api_keys):
    """Try each API key until one works."""
    # Shuffle to distribute load
    keys = api_keys.copy()
    random.shuffle(keys)
    
    last_error = ""
    for key in keys:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.1, "maxOutputTokens": 500}
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 429:
                last_error = "quota"
                continue  # Try next key
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            last_error = str(e)
            continue
    
    if "quota" in last_error:
        return "⚠️ All API keys have reached their daily limit. Please try again tomorrow or contact BLECA SmartLabs admin."
    return f"⚠️ Error: {last_error}"

# ─── Knowledge Search ──────────────────────────────────────────────────────────
def search_knowledge(question):
    question_lower = question.lower()
    paragraphs = [p.strip() for p in KNOWLEDGE_BASE.split('\n') if len(p.strip()) > 30]
    scored = []
    question_words = set(question_lower.split())
    # Remove common words
    stop_words = {"what", "is", "the", "a", "an", "of", "in", "at", "to", "and", "or", "for", "does", "do", "how", "who", "where", "when", "why", "are", "was", "were"}
    question_words = question_words - stop_words
    
    for para in paragraphs:
        para_lower = para.lower()
        score = sum(1 for word in question_words if word in para_lower)
        if score > 0:
            scored.append((score, para))
    scored.sort(reverse=True)
    top = [p for _, p in scored[:4]]
    return '\n\n'.join(top) if top else ""

def ask_bleca(question, api_keys):
    # Handle greetings first - no API needed
    if is_how_are_you(question):
        return random.choice(HOW_ARE_YOU_RESPONSES)
    
    if is_greeting(question):
        return random.choice(GREETING_RESPONSES)
    
    # Search knowledge base
    context = search_knowledge(question)
    
    if not context:
        return "I could not find that information in the BLECA SmartLabs knowledge base. Please try asking about our vision, mission, team, services, location, or technologies."
    
    prompt = f"""You are the official BLECA SmartLabs AI Assistant. You must answer ONLY in English.

STRICT RULES:
- Answer ONLY using the context provided below
- Do NOT use outside knowledge
- Respond in clear, friendly, professional English
- If the answer is not in the context, say: "I could not find that information in the BLECA SmartLabs knowledge base."
- Keep answers concise and helpful

CONTEXT:
{context}

QUESTION: {question}

Answer in English:"""

    return call_gemini(prompt, api_keys)

# ─── Load API Keys ─────────────────────────────────────────────────────────────
api_keys = get_api_keys()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 BLECA SmartLabs AI")
    st.markdown("Your intelligent AI assistant powered by Gemini AI")
    st.markdown("---")
    st.markdown("## 📊 Session Stats")
    col1, col2 = st.columns(2)
    msgs_count = len(st.session_state.get("messages", []))
    with col1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{msgs_count // 2}</div><div class='stat-label'>Questions Asked</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{'✅' if api_keys else '❌'}</div><div class='stat-label'>{'Ready' if api_keys else 'No Key'}</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; color:#34d399; font-size:0.8rem;'>🔑 {len(api_keys)} API Key(s) Active</div>", unsafe_allow_html=True)
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
    ]
    for q in samples:
        if st.button(q, use_container_width=True, key=f"s_{q[:15]}"):
            st.session_state["pending"] = q
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
    
    st.markdown("<div style='text-align:center; color:#6b7280; font-size:0.75rem; margin-top:1rem;'>Built with Gemini AI + Streamlit<br>BLECA SmartLabs © 2025<br>MUST, Mbeya, Tanzania</div>", unsafe_allow_html=True)

# ─── Main UI ──────────────────────────────────────────────────────────────────
st.markdown("<div class='bleca-header'><h1>🤖 BLECA SmartLabs AI</h1><p>Your intelligent assistant for everything about BLECA SmartLabs</p></div>", unsafe_allow_html=True)

if api_keys:
    st.markdown(f"<div style='text-align:center; margin-bottom:1rem;'><span class='status-badge status-ready'>✅ AI Ready — Gemini 2.0 Flash — {len(api_keys)} Keys Active</span></div>", unsafe_allow_html=True)
else:
    st.error("⚠️ No API Keys found. Please contact BLECA SmartLabs admin.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("---")

# Display chat
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
    if not api_keys:
        st.error("⚠️ No API Keys found.")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
        with st.spinner("🤔 Thinking..."):
            answer = ask_bleca(user_input.strip(), api_keys)
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        st.rerun()
