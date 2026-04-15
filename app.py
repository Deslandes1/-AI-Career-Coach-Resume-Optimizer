import streamlit as st
import openai
import PyPDF2
import docx
import io
import os

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Career Coach | GlobalInternet.py",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS for Readability & Color
# -----------------------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9edf2 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e3c72 !important;
        font-weight: 700 !important;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton button {
        background: #1e3c72;
        color: white;
        border-radius: 40px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        transition: 0.2s;
    }
    .stButton button:hover {
        background: #2a5298;
        transform: scale(1.02);
    }
    
    /* Success/Warning/Info boxes */
    .stAlert {
        border-radius: 15px;
        font-weight: 500;
    }
    
    /* File uploader */
    .stFileUploader {
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
        border: 1px dashed #1e3c72;
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 15px;
        border: 1px solid #ccd7e8;
        font-size: 1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffffdd;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.8rem;
    }
    
    /* Globe symbol */
    .big-globe {
        font-size: 3rem;
        display: inline-block;
        margin-right: 10px;
    }
    
    /* Readability */
    p, li, .stMarkdown {
        color: #212529;
        line-height: 1.5;
    }
    
    .highlight {
        background: #e8f0fe;
        padding: 2px 6px;
        border-radius: 12px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar - Language & Company Info
# -----------------------------
with st.sidebar:
    st.markdown('<span class="big-globe">🌐</span> **GlobalInternet.py**', unsafe_allow_html=True)
    st.markdown("---")
    
    # Language selection
    lang = st.radio("🌐 Language / Langue", ["English", "Français"], index=0)
    
    st.markdown("---")
    st.markdown("**Founder & CEO:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🌐 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$20 USD** per analysis (one‑time) or **$49/month** for unlimited analyses.")
    st.markdown("---")
    st.markdown("© 2025 GlobalInternet.py")
    st.markdown("All Rights Reserved")

# -----------------------------
# Main Title
# -----------------------------
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown('<span class="big-globe">🌐</span>', unsafe_allow_html=True)
with col_title:
    st.markdown("# AI Career Coach – Resume Optimizer")
    st.markdown("**Get tailored resume improvements and interview questions** – powered by AI.")

st.markdown("---")

# -----------------------------
# Language Texts
# -----------------------------
if lang == "English":
    upload_label = "📄 Upload your CV (PDF, DOCX, or TXT)"
    paste_label = "Or paste your CV text below"
    jd_label = "📋 Job Description (paste or upload .txt)"
    analyze_btn = "🔍 Analyze & Get Suggestions"
    processing = "Processing your CV and job description..."
    error_no_cv = "Please provide your CV (upload or paste)."
    error_no_jd = "Please provide a job description."
    error_api_key = "OpenAI API key not found. Please add it to your Streamlit secrets."
    result_title = "🎯 AI Analysis Results"
    keywords_section = "📌 Keywords to Add"
    skills_section = "🛠️ Missing Skills / Improvements"
    format_section = "📄 Formatting Suggestions"
    questions_section = "❓ Predicted Interview Questions"
    disclaimer = "⚠️ AI suggestions are for guidance only. Always review before using."
else:
    upload_label = "📄 Téléchargez votre CV (PDF, DOCX ou TXT)"
    paste_label = "Ou collez le texte de votre CV ci-dessous"
    jd_label = "📋 Description de poste (collez ou téléchargez .txt)"
    analyze_btn = "🔍 Analyser et obtenir des suggestions"
    processing = "Traitement de votre CV et de la description de poste..."
    error_no_cv = "Veuillez fournir votre CV (téléchargement ou texte)."
    error_no_jd = "Veuillez fournir une description de poste."
    error_api_key = "Clé API OpenAI introuvable. Ajoutez‑la dans les secrets Streamlit."
    result_title = "🎯 Résultats de l'analyse IA"
    keywords_section = "📌 Mots‑clés à ajouter"
    skills_section = "🛠️ Compétences manquantes / Améliorations"
    format_section = "📄 Suggestions de mise en forme"
    questions_section = "❓ Questions d'entretien prédites"
    disclaimer = "⚠️ Les suggestions IA sont indicatives. Relisez toujours avant utilisation."

# -----------------------------
# CV Input
# -----------------------------
st.subheader("📄 Your CV")
cv_file = st.file_uploader(upload_label, type=["pdf", "docx", "txt"])
cv_text = ""
if cv_file:
    file_type = cv_file.type
    try:
        if cv_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(cv_file)
            cv_text = " ".join([page.extract_text() or "" for page in pdf_reader.pages])
        elif cv_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(cv_file)
            cv_text = " ".join([para.text for para in doc.paragraphs])
        else:  # txt
            cv_text = cv_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        cv_text = ""

cv_paste = st.text_area(paste_label, height=150)
if cv_paste:
    cv_text = cv_paste

# -----------------------------
# Job Description Input
# -----------------------------
st.subheader("💼 Job Description")
jd_text = ""
jd_file = st.file_uploader(jd_label, type=["txt"])
if jd_file:
    jd_text = jd_file.read().decode("utf-8")
jd_paste = st.text_area("", height=150, placeholder="Paste the job description here...")
if jd_paste:
    jd_text = jd_paste

# -----------------------------
# Analyze Button
# -----------------------------
if st.button(analyze_btn, use_container_width=True):
    if not cv_text.strip():
        st.error(error_no_cv)
    elif not jd_text.strip():
        st.error(error_no_jd)
    else:
        # Check for OpenAI API key
        openai_api_key = st.secrets.get("OPENAI_API_KEY")
        if not openai_api_key:
            st.error(error_api_key)
        else:
            openai.api_key = openai_api_key
            with st.spinner(processing):
                try:
                    # Construct prompt
                    system_prompt = """You are an expert career coach and resume writer. Analyze the CV against the job description. 
Provide output in the following format:

📌 KEYWORDS TO ADD:
- (list keywords missing from CV that appear in job description)

🛠️ MISSING SKILLS / IMPROVEMENTS:
- (list skills or experiences to highlight)

📄 FORMATTING SUGGESTIONS:
- (tips to improve CV layout, readability, or impact)

❓ PREDICTED INTERVIEW QUESTIONS:
- (list 5 likely interview questions based on the job description and CV)

Keep each section concise but actionable. Use bullet points."""
                    
                    user_prompt = f"JOB DESCRIPTION:\n{jd_text}\n\nCV:\n{cv_text}"
                    
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    
                    result = response.choices[0].message.content
                    
                    # Display results in nice cards
                    st.markdown(f"## {result_title}")
                    
                    # Split sections by markdown headers
                    sections = result.split("\n\n")
                    for section in sections:
                        if section.strip():
                            if "📌 KEYWORDS" in section or "📌 Mots‑clés" in section:
                                st.markdown(f'<div class="card"><h3>{keywords_section}</h3>{section.replace("📌 KEYWORDS TO ADD:", "").replace("📌 Mots‑clés à ajouter:", "")}</div>', unsafe_allow_html=True)
                            elif "🛠️ MISSING SKILLS" in section or "🛠️ Compétences manquantes" in section:
                                st.markdown(f'<div class="card"><h3>{skills_section}</h3>{section.replace("🛠️ MISSING SKILLS / IMPROVEMENTS:", "").replace("🛠️ Compétences manquantes / Améliorations:", "")}</div>', unsafe_allow_html=True)
                            elif "📄 FORMATTING" in section or "📄 Suggestions de mise en forme" in section:
                                st.markdown(f'<div class="card"><h3>{format_section}</h3>{section.replace("📄 FORMATTING SUGGESTIONS:", "").replace("📄 Suggestions de mise en forme:", "")}</div>', unsafe_allow_html=True)
                            elif "❓ PREDICTED INTERVIEW" in section or "❓ Questions d'entretien prédites" in section:
                                st.markdown(f'<div class="card"><h3>{questions_section}</h3>{section.replace("❓ PREDICTED INTERVIEW QUESTIONS:", "").replace("❓ Questions d'entretien prédites:", "")}</div>', unsafe_allow_html=True)
                            else:
                                # Fallback: show as normal text
                                st.markdown(f'<div class="card">{section}</div>', unsafe_allow_html=True)
                    
                    st.info(disclaimer)
                    
                except Exception as e:
                    st.error(f"AI analysis failed: {e}")

# -----------------------------
# Footer
# -----------------------------
st.markdown('<div class="footer">🌐 GlobalInternet.py – AI Career Coach. From Haiti to the world.</div>', unsafe_allow_html=True)
