import streamlit as st
import PyPDF2
import docx
from openai import OpenAI
import io

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
    
    /* Buttons - make text white */
    .stButton button {
        background: #1e3c72;
        color: white !important;
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
        font-size: 5rem;
        display: block;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .medium-globe {
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
    
    /* Login container */
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Pricing card */
    .pricing-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .pricing-card h3 {
        color: white !important;
        margin: 0;
    }
    .pricing-card .price {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
        color: white !important;
    }
    /* Make pricing card description text white */
    .pricing-card p {
        color: white !important;
        opacity: 0.9;
    }
    
    /* Sidebar text overrides for white on dark cards */
    [data-testid="stSidebar"] .pricing-card p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Authentication
# -----------------------------
def check_password():
    """Returns True if user is logged in."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<span class="big-globe">🌐</span>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>AI Career Coach</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>by GlobalInternet.py</p>", unsafe_allow_html=True)
    
    password = st.text_input("Enter password to access", type="password", key="login_pass")
    if st.button("Login", use_container_width=True):
        if password == "20082010":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Access denied.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Main App (only shown after login)
# -----------------------------
def main_app():
    # Sidebar - Language, API Key & Company Info + Logout
    with st.sidebar:
        st.markdown('<span class="medium-globe">🌐</span> **GlobalInternet.py**', unsafe_allow_html=True)
        st.markdown("---")
        
        # OpenAI API Key Input
        api_key = st.text_input("🔑 OpenAI API Key", type="password", help="Enter your OpenAI API key. Get one from https://platform.openai.com/api-keys")
        if api_key:
            st.success("✅ API key loaded")
        else:
            st.warning("⚠️ Please enter your OpenAI API key")
        
        st.markdown("---")
        
        # Language selection (English, Español, Français)
        lang = st.radio("🌐 Language", ["English", "Español", "Français"], index=0)
        
        st.markdown("---")
        st.markdown("**Founder & CEO:**")
        st.markdown("Gesner Deslandes")
        st.markdown("📞 WhatsApp: (509) 4738-5663")
        st.markdown("📧 deslandes78@gmail.com")
        st.markdown("🌐 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
        st.markdown("---")
        
        # Updated Pricing Section
        st.markdown("### 💰 Pricing Plans")
        st.markdown('<div class="pricing-card"><h3>🎯 Single Analysis</h3><div class="price">$10 USD</div><p>One-time fee · One full resume analysis</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="pricing-card" style="background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);"><h3>🚀 Monthly Subscription</h3><div class="price">$29 USD/month</div><p>Unlimited analyses · Cancel anytime</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="pricing-card" style="background: linear-gradient(135deg, #0f2b4d 0%, #1a3a6e 100%);"><h3>💎 Full Software Package</h3><div class="price">$149 USD one‑time</div><p>Complete source code + lifetime updates + free support · Delivered by email</p></div>', unsafe_allow_html=True)
        st.caption("💡 Compare: Rezi Lifetime $149 · Resumatic AI Lifetime $149 · ResuFit Pro $14.90/month")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown("© 2025 GlobalInternet.py")
        st.markdown("All Rights Reserved")

    # Main Title with globe
    col_logo, col_title = st.columns([1, 5])
    with col_logo:
        st.markdown('<span class="medium-globe">🌐</span>', unsafe_allow_html=True)
    with col_title:
        st.markdown("# AI Career Coach – Resume Optimizer")
        st.markdown("**Get tailored resume improvements and interview questions** – powered by AI.")

    st.markdown("---")

    # -----------------------------
    # Language Texts (English, Español, Français)
    # -----------------------------
    if lang == "English":
        upload_label = "📄 Upload your CV (PDF, DOCX, or TXT)"
        paste_label = "Or paste your CV text below"
        jd_label = "📋 Job Description (paste or upload .txt)"
        analyze_btn = "🔍 Analyze & Get Suggestions"
        processing = "Processing your CV and job description..."
        error_no_cv = "Please provide your CV (upload or paste)."
        error_no_jd = "Please provide a job description."
        error_api_key = "OpenAI API key is required. Please enter your API key in the sidebar."
        result_title = "🎯 AI Analysis Results"
        keywords_section = "📌 Keywords to Add"
        skills_section = "🛠️ Missing Skills / Improvements"
        format_section = "📄 Formatting Suggestions"
        questions_section = "❓ Predicted Interview Questions"
        disclaimer = "⚠️ AI suggestions are for guidance only. Always review before using."
        pricing_note = "💡 After analysis, contact us via WhatsApp or email to purchase credits, subscribe monthly, or buy the full software package."
    elif lang == "Español":
        upload_label = "📄 Sube tu CV (PDF, DOCX o TXT)"
        paste_label = "O pega el texto de tu CV abajo"
        jd_label = "📋 Descripción del puesto (pega o sube .txt)"
        analyze_btn = "🔍 Analizar y obtener sugerencias"
        processing = "Procesando tu CV y la descripción del puesto..."
        error_no_cv = "Por favor, proporciona tu CV (sube o pega)."
        error_no_jd = "Por favor, proporciona una descripción del puesto."
        error_api_key = "Se requiere la clave API de OpenAI. Ingresa tu clave API en la barra lateral."
        result_title = "🎯 Resultados del análisis IA"
        keywords_section = "📌 Palabras clave para añadir"
        skills_section = "🛠️ Habilidades faltantes / Mejoras"
        format_section = "📄 Sugerencias de formato"
        questions_section = "❓ Preguntas de entrevista previstas"
        disclaimer = "⚠️ Las sugerencias de IA son orientativas. Siempre revísalas antes de usar."
        pricing_note = "💡 Después del análisis, contáctanos vía WhatsApp o email para comprar créditos, suscribirte mensualmente o comprar el paquete completo."
    else:  # Français
        upload_label = "📄 Téléchargez votre CV (PDF, DOCX ou TXT)"
        paste_label = "Ou collez le texte de votre CV ci-dessous"
        jd_label = "📋 Description de poste (collez ou téléchargez .txt)"
        analyze_btn = "🔍 Analyser et obtenir des suggestions"
        processing = "Traitement de votre CV et de la description de poste..."
        error_no_cv = "Veuillez fournir votre CV (téléchargement ou texte)."
        error_no_jd = "Veuillez fournir une description de poste."
        error_api_key = "La clé API OpenAI est requise. Veuillez entrer votre clé API dans la barre latérale."
        result_title = "🎯 Résultats de l'analyse IA"
        keywords_section = "📌 Mots‑clés à ajouter"
        skills_section = "🛠️ Compétences manquantes / Améliorations"
        format_section = "📄 Suggestions de mise en forme"
        questions_section = "❓ Questions d'entretien prédites"
        disclaimer = "⚠️ Les suggestions IA sont indicatives. Relisez toujours avant utilisation."
        pricing_note = "💡 Après l'analyse, contactez-nous via WhatsApp ou email pour acheter des crédits, vous abonner mensuellement ou acheter le logiciel complet."

    # -----------------------------
    # CV Input
    # -----------------------------
    st.subheader("📄 Your CV")
    cv_file = st.file_uploader(upload_label, type=["pdf", "docx", "txt"])
    cv_text = ""
    if cv_file:
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
        elif not api_key:
            st.error(error_api_key)
        else:
            try:
                # Initialize the OpenAI client with the user's key
                client = OpenAI(api_key=api_key)
                with st.spinner(processing):
                    # Construct the system and user prompts
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
                    
                    # Make the API call using the new client-based approach
                    response = client.chat.completions.create(
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
                    
                    sections = result.split("\n\n")
                    for section in sections:
                        section = section.strip()
                        if not section:
                            continue
                        if section.startswith("📌 KEYWORDS TO ADD") or section.startswith("📌 Mots‑clés à ajouter") or section.startswith("📌 Palabras clave para añadir"):
                            content = section.split(":", 1)[-1].strip()
                            st.markdown(f'<div class="card"><h3>{keywords_section}</h3>{content}</div>', unsafe_allow_html=True)
                        elif section.startswith("🛠️ MISSING SKILLS") or section.startswith("🛠️ Compétences manquantes") or section.startswith("🛠️ Habilidades faltantes"):
                            content = section.split(":", 1)[-1].strip()
                            st.markdown(f'<div class="card"><h3>{skills_section}</h3>{content}</div>', unsafe_allow_html=True)
                        elif section.startswith("📄 FORMATTING") or section.startswith("📄 Suggestions de mise en forme") or section.startswith("📄 Sugerencias de formato"):
                            content = section.split(":", 1)[-1].strip()
                            st.markdown(f'<div class="card"><h3>{format_section}</h3>{content}</div>', unsafe_allow_html=True)
                        elif section.startswith("❓ PREDICTED INTERVIEW") or section.startswith("❓ Questions d'entretien prédites") or section.startswith("❓ Preguntas de entrevista previstas"):
                            content = section.split(":", 1)[-1].strip()
                            st.markdown(f'<div class="card"><h3>{questions_section}</h3>{content}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="card">{section}</div>', unsafe_allow_html=True)
                    
                    st.info(disclaimer)
                    st.caption(pricing_note)
                    
            except Exception as e:
                st.error(f"AI analysis failed: {e}. Please check your API key and try again.")

    # Footer
    st.markdown('<div class="footer">🌐 GlobalInternet.py – AI Career Coach. From Haiti to the world.</div>', unsafe_allow_html=True)

# -----------------------------
# Run login or main app
# -----------------------------
if not check_password():
    login()
else:
    main_app()
