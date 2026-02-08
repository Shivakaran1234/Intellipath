# app.py
import streamlit as st
from utils import save_uploaded_file
from resume_parser import extract_text
from iextract import extract_entities, normalize_entities
from generator import generate_career_path


# Page configuration
st.set_page_config(
    page_title="IntelliPath - AI Career Path Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .download-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px dashed #6c757d;
        text-align: center;
        margin: 2rem 0;
    }
    .user-input-section {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🎯 IntelliPath — AI Career Path Recommender</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    1. **Upload** your resume (PDF, DOCX, or TXT)
    2. **Provide** your area of interest and future goals
    3. **Click Analyze** to process your resume
    4. **Review** the extracted information
    5. **Get** your personalized career path
    6. **Download** your career plan
    """)
    
    st.header("🔧 Features")
    st.markdown("""
    - 📄 **Resume Parsing**: Extract text from multiple formats
    - 🧠 **AI Analysis**: Identify skills, experience, and education
    - 🎯 **Personalized Matching**: Consider your interests and goals
    - 📈 **3-Stage Planning**: Entry, Mid, and Senior level guidance
    - 💾 **Download Results**: Save your career plan
    """)

# Main content
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    uploaded = st.file_uploader(
        "📁 Upload your resume",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT"
    )

if uploaded:
    st.markdown('<div class="info-box">📄 <strong>File uploaded successfully!</strong> Now provide your preferences below.</div>', unsafe_allow_html=True)

# User preferences section
st.markdown('<h2 class="sub-header">🎯 Your Career Preferences</h2>', unsafe_allow_html=True)
st.markdown('<div class="user-input-section">Please provide your preferences to get a more personalized career path recommendation.</div>', unsafe_allow_html=True)

# Area of interest
st.subheader("🌟 Area of Interest")
area_of_interest = st.selectbox(
    "What area of technology interests you most?",
    [
        "Software Development",
        "Data Science & Analytics", 
        "DevOps & Cloud",
        "Cybersecurity",
        "Product Management",
        "UI/UX Design",
        "Artificial Intelligence & Machine Learning",
        "Mobile Development",
        "Web Development",
        "Game Development",
        "Blockchain & Web3",
        "Other (please specify)"
    ],
    help="Select the area that most interests you for your career"
)

# Custom area of interest
if area_of_interest == "Other (please specify)":
    area_of_interest = st.text_input("Please specify your area of interest:")

# Future goals
st.subheader("🎯 Future Goals")
future_goals = st.multiselect(
    "What are your future career goals? (Select all that apply)",
    [
        "Become a technical leader/architect",
        "Move into management/leadership",
        "Start my own company/entrepreneurship",
        "Work for top tech companies (FAANG)",
        "Become a subject matter expert",
        "Work remotely/freelance",
        "Contribute to open source",
        "Pursue advanced education (Master's/PhD)",
        "Specialize in emerging technologies",
        "Work internationally",
        "Focus on social impact/tech for good",
        "Achieve work-life balance",
        "High salary/compensation",
        "Job security and stability"
    ],
    help="Select your primary career goals"
)

# Additional goals
additional_goals = st.text_area(
    "Any other specific goals or preferences?",
    placeholder="E.g., I want to work in healthcare technology, I prefer startups over large companies, I want to focus on sustainability...",
    help="Share any additional context about your career aspirations"
)

# Timeline preference
st.subheader("⏰ Career Timeline")
timeline = st.selectbox(
    "What's your preferred timeline for career advancement?",
    [
        "Fast-track (aim for rapid advancement)",
        "Steady growth (balanced pace)",
        "Long-term focus (patient, thorough development)",
        "Flexible (adapt to opportunities)"
    ],
    help="How quickly do you want to advance in your career?"
)

# Analysis button
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    analyze_button = st.button("🚀 Generate Personalized Career Path", type="primary", use_container_width=True)

if analyze_button:
    if not uploaded:
        st.error("❌ Please upload a resume first.")
        st.stop()
    
    if not area_of_interest:
        st.error("❌ Please select or specify your area of interest.")
        st.stop()

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Step 1: Save file
    status_text.text("📁 Saving uploaded file...")
    progress_bar.progress(10)
    with st.spinner("Saving file..."):
        tmp_path = save_uploaded_file(uploaded, uploaded.name)

    # Step 2: Extract text
    status_text.text("📖 Extracting text from resume...")
    progress_bar.progress(20)
    with st.spinner("Extracting text..."):
        try:
            raw = extract_text(tmp_path)
        except Exception as e:
            st.error(f"❌ Failed to parse file: {e}")
            st.stop()

    # Step 3: NER Processing
    status_text.text("🧠 Analyzing resume content...")
    progress_bar.progress(40)
    with st.spinner("Running AI analysis..."):
        ents = extract_entities(raw)
        summary = normalize_entities(ents)

    # Step 4: Generate career path
    status_text.text("🎯 Generating personalized career path...")
    progress_bar.progress(60)
    with st.spinner("Creating your personalized career plan..."):
        try:
            # Add user preferences to summary
            user_preferences = {
                "area_of_interest": area_of_interest,
                "future_goals": future_goals,
                "additional_goals": additional_goals,
                "timeline": timeline
            }
            summary["user_preferences"] = user_preferences
            
            plan_md = generate_career_path(summary)
        except Exception as e:
            st.error(f"❌ Generation failed: {e}")
            st.stop()

    # Complete
    progress_bar.progress(100)
    status_text.text("✅ Analysis complete!")
    st.success("🎉 Your personalized career path has been generated successfully!")

    # Display results in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Resume Analysis", "🎯 Career Path", "📄 Raw Text", "💾 Download", "⚙️ Your Preferences"])

    with tab1:
        st.markdown('<h2 class="sub-header">📊 Resume Analysis Results</h2>', unsafe_allow_html=True)
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Skills Identified")
            if summary.get("skills"):
                for skill in summary["skills"][:10]:  # Show first 10 skills
                    st.markdown(f"- {skill}")
                if len(summary["skills"]) > 10:
                    st.markdown(f"- *... and {len(summary['skills']) - 10} more*")
            else:
                st.info("No skills detected in the resume")

            st.subheader("🏢 Companies")
            if summary.get("companies"):
                for company in summary["companies"][:5]:
                    st.markdown(f"- {company}")
            else:
                st.info("No companies detected")

        with col2:
            st.subheader("💼 Job Titles")
            if summary.get("job_titles"):
                for title in summary["job_titles"][:5]:
                    st.markdown(f"- {title}")
            else:
                st.info("No job titles detected")

            st.subheader("🎓 Education")
            if summary.get("education"):
                for edu in summary["education"][:3]:
                    st.markdown(f"- {edu}")
            else:
                st.info("No education detected")

        # Projects section
        if summary.get("projects"):
            st.subheader("🚀 Projects")
            for project in summary["projects"][:5]:
                st.markdown(f"- {project}")
        
        # Certifications section
        if summary.get("certifications"):
            st.subheader("🏆 Certifications")
            for cert in summary["certifications"][:5]:
                st.markdown(f"- {cert}")
        
        # Achievements section
        if summary.get("achievements"):
            st.subheader("🏅 Achievements")
            for achievement in summary["achievements"][:5]:
                st.markdown(f"- {achievement}")

    with tab2:
        st.markdown('<h2 class="sub-header">🎯 Your Personalized Career Path</h2>', unsafe_allow_html=True)
        st.markdown(plan_md)

    with tab3:
        st.markdown('<h2 class="sub-header">📄 Raw Resume Text</h2>', unsafe_allow_html=True)
        st.text_area("Raw text from your resume", raw[:5000], height=300, disabled=True)
        if len(raw) > 5000:
            st.info(f"Showing first 5000 characters. Total length: {len(raw)} characters")

    with tab4:
        st.markdown('<h2 class="sub-header">💾 Download Your Career Plan</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        st.markdown("### 📥 Download Options")
        
        # Download as Markdown
        st.download_button(
            label="📄 Download as Markdown (.md)",
            data=plan_md,
            file_name="intellipath_career_plan.md",
            mime="text/markdown",
            use_container_width=True
        )
        
        # Download as Text
        st.download_button(
            label="📝 Download as Text (.txt)",
            data=plan_md,
            file_name="intellipath_career_plan.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.markdown("""
        **📋 What you'll get:**
        - Your personalized 3-stage career development plan
        - Skill analysis and recommendations based on your preferences
        - Immediate next steps and long-term strategy
        - Professional formatting ready for sharing
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<h2 class="sub-header">⚙️ Your Career Preferences</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌟 Area of Interest")
            st.info(area_of_interest)
            
            st.subheader("⏰ Timeline Preference")
            st.info(timeline)
        
        with col2:
            st.subheader("🎯 Future Goals")
            if future_goals:
                for goal in future_goals:
                    st.markdown(f"- {goal}")
            else:
                st.info("No specific goals selected")
        
        if additional_goals:
            st.subheader("📝 Additional Goals")
            st.info(additional_goals)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <p>🎯 IntelliPath - AI-Powered Career Path Recommender</p>
    <p>Upload your resume and share your preferences to get personalized career guidance!</p>
</div>
""", unsafe_allow_html=True)