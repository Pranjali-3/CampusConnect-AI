import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os
from github_analyser import GitHubAnalyzer
from ai_engine import analyze_profile
from llm_engine import get_ai_feedback, generate_7_day_plan, generate_readme_template
from ambassador import get_ambassador_insights

# --- Page Configuration ---
st.set_page_config(
    page_title="CampusConnect AI", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Preserved Exactly) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
    }
    /* Style for the code block export */
    code {
        color: #00f2fe !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Global Session State ---
if 'db' not in st.session_state: 
    st.session_state.db = []
if 'tasks' not in st.session_state:
    st.session_state.tasks = [{"id": 1, "title": "Optimize Profile README", "deadline": "2026-04-30", "points": 100}]

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rocket.png", width=80)
    st.markdown("### Navigation")
    # Fixed Label Visibility to avoid terminal warnings
    mode = st.selectbox("Select Mode", ["👨‍💻 Student Mode", "🏫 Ambassador Mode"], label_visibility="collapsed")
    st.divider()
    st.markdown("📅 **Deadline:** 26th April, 6:00 PM")

# --- Student Mode ---
if mode == "👨‍💻 Student Mode":
    st.markdown('<h1 class="main-title">CampusConnect AI</h1>', unsafe_allow_html=True)
    
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        username = st.text_input("🔍 Enter GitHub Username to Begin Assessment", placeholder="e.g. yyx990803")

    if username:
        with st.spinner("Analyzing profile..."):
            data = GitHubAnalyzer().fetch_user_data(username)
            if data:
                res = analyze_profile(data)
                if res['score'] > 80: st.balloons()
                
                # Metrics Row
                st.markdown("### 📊 Profile Strength")
                c1, c2, c3 = st.columns(3)
                c1.metric("GitHub Score", f"{res['score']}/100")
                c2.metric("ATS Ready Score", f"{int(res['ats'])}%")
                c3.metric("Recruiter Benchmark", res['benchmark'])

                st.markdown("---")
                st.markdown(f"### 🤖 AI Recruiter Perspective")
                st.info(get_ai_feedback(res['score']))

                # Visual Analytics
                col_left, col_right = st.columns(2)
                with col_left:
                    st.markdown("#### 🧠 Score Breakdown")
                    st.plotly_chart(px.bar(
                        x=list(res['breakdown'].values()), 
                        y=list(res['breakdown'].keys()), 
                        orientation='h',
                        color=list(res['breakdown'].keys()),
                        template="plotly_dark"
                    ), use_container_width=True)

                with col_right:
                    st.markdown("#### 🛠 Skill Diversity")
                    st.plotly_chart(px.pie(
                        values=list(res['languages'].values()), 
                        names=list(res['languages'].keys()), 
                        hole=0.5,
                        template="plotly_dark"
                    ), use_container_width=True)

                # --- FEATURE 1: Professional Portfolio Export ---
                st.markdown("### 📄 Recruiter-Ready Portfolio")
                with st.expander("✨ Generate Verified Profile Markdown"):
                    portfolio_md = f"""
# 🚀 Verified Developer Profile: {username}
**CampusConnect AI Score:** {res['score']}/100 | **ATS Readiness:** {int(res['ats'])}%

### 🛠 Technical Skillset
- **Primary Expertise:** {", ".join(list(res['languages'].keys())[:3])}
- **Recruiter Benchmark:** {res['benchmark']}

### 🤖 AI Recruiter Insights
> "{get_ai_feedback(res['score'])}"

---
*Verified via CampusConnect AI Platform*
                    """
                    st.code(portfolio_md, language="markdown")
                    st.caption("Copy-paste this into your GitHub Profile README!")

                # --- FEATURE 2: Peer Mentorship Matcher ---
                st.markdown("### 🤝 Peer Mentorship")
                if st.button("🔍 Find a Mentor for my Tech Stack"):
                    if res['languages']:
                        top_lang = max(res['languages'], key=res['languages'].get)
                        # Find someone in DB with score > 80 who isn't the current user
                        mentors = [u for u in st.session_state.db if u['user'] != username and u['score'] > 80]
                        if mentors:
                            st.success(f"🎉 Match Found! **{mentors[0]['user']}** is an expert in your field. Connect with them to grow!")
                        else:
                            st.info(f"You are a trailblazer in {top_lang}! As more students join, matches will appear here.")

                st.markdown("### 📂 Repository Optimization")
                st.dataframe(pd.DataFrame([{"Repo Name": r['name'], "Stars": r['stargazers_count'], "Language": r['language']} for r in data['repos']]), width="stretch")

                # Task Assignment & Submission Section
                st.divider()
                st.markdown("### 📋 Pending Campus Assignments")
                if st.session_state.tasks:
                    for t in st.session_state.tasks:
                        with st.container():
                            tc1, tc2, tc3 = st.columns([3, 2, 1])
                            tc1.write(f"**{t['title']}** ({t['points']} pts)")
                            tc2.write(f"📅 Deadline: {t['deadline']}")
                            if tc3.button("Verify & Submit", key=f"task_{t['id']}"):
                                user_idx = next((i for i, d in enumerate(st.session_state.db) if d['user'] == username), None)
                                if user_idx is not None:
                                    st.session_state.db[user_idx]['tasks'] = st.session_state.db[user_idx].get('tasks', 0) + 1
                                    st.session_state.db[user_idx]['task_points'] = st.session_state.db[user_idx].get('task_points', 0) + t['points']
                                    st.success(f"Task Verified! {t['points']} points added.")
                                else:
                                    st.session_state.db.append({
                                        "user": username, "score": res['score'], 
                                        "tasks": 1, "task_points": t['points']
                                    })
                                    st.success(f"Verified! {username} added with {t['points']} points.")
                else:
                    st.info("No active tasks found.")

                st.markdown("---")
                if st.button("📅 Generate My Recruiter-Ready Roadmap"):
                    for i, step in enumerate(generate_7_day_plan(res['score'])):
                        st.markdown(f"**{i+1}.** {step}")

# --- Ambassador Mode ---
else:
    st.markdown('<h1 class="main-title">Ambassador Dashboard</h1>', unsafe_allow_html=True)
    
    with st.expander("➕ Assign New Task to Campus Students"):
        with st.form("task_creator"):
            t_title = st.text_input("Task Title/Description")
            t_deadline = st.date_input("Submission Deadline", datetime.date.today())
            t_points = st.number_input("Reward Points", 10, 500, 50)
            if st.form_submit_button("Broadcast Task"):
                st.session_state.tasks.append({
                    "id": len(st.session_state.tasks) + 1,
                    "title": t_title,
                    "deadline": str(t_deadline),
                    "points": t_points
                })
                st.success("Task successfully broadcasted!")

    stats = get_ambassador_insights(st.session_state.db)
    
    if stats:
        c1, c2, c3 = st.columns(3)
        c1.metric("Ecosystem Health", stats['health'])
        c2.metric("Avg Campus Strength", f"{stats['avg']:.1f}")
        c3.metric("Total Students Enrolled", f"{len(st.session_state.db)}")
        
        st.markdown("### 🏆 Real-time Points Leaderboard")
        st.dataframe(stats['leaderboard'][['user', 'points', 'score']], width="stretch")
        
        st.markdown("### 📈 Management ROI")
        st.success(f"**Strategic Recommendation:** {stats['rec']}")
    else:
        st.warning("No data yet. Students must verify in Student Mode first.")