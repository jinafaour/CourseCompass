import streamlit as st
import pandas as pd
import plotly.express as px

# --- APP CONFIGURATION ---
st.set_page_config(page_title="BC High School Course Compass", page_icon="🧭", layout="wide")

# --- CUSTOM CSS FOR HIGH-IMPACT VISUALS ---
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; color: #2E86C1; }
    .header-style { font-size:40px; font-weight: bold; color: #17202A; }
    .sub-header { font-size:20px; color: #566573; font-style: italic; }
    .highlight-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #2E86C1; }
    .alert-box { background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107; color: #856404; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: DISCLAIMER & INFO ---
with st.sidebar:
    st.header("⚠️ Critical Disclaimer")
    st.markdown("""
    <div class='alert-box'>
    <strong>Non-Institutional Status</strong><br>
    This application is a supplementary planning resource <strong>ONLY</strong>.
    <ul>
        <li>It <strong>does not replace</strong> official academic counseling, school board curriculum guides, or advice from your school.</li>
        <li><strong>Verification Required:</strong> All course selections must be verified with a certified school counselor.</li>
        <li><strong>Grade 8-12 Focus:</strong> Designed for students in Grade 8 (transitioning) through Grade 12.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("**Target Audience:** Students in BC (Grades 8-12)")
    st.write("**Goal:** Align interests with BC Curriculum Electives")

# --- MAIN HEADER ---
st.markdown("<p class='header-style'>🧭 BC High School Course Compass</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Discover the electives that match your brain, not just your grades.</p>", unsafe_allow_html=True)

st.markdown("---")

# --- INSTRUCTIONS (UPDATED) ---
with st.expander("📘 HOW TO USE THIS APP (Start Here)", expanded=True):
    st.markdown("""
    1.  **Rate Your Interests:** Be honest. 1 (Hate it) to 10 (Love it).
    2.  **Analyze:** The algorithm looks for patterns in your "Data DNA".
    3.  **Review Matches:** We suggest electives based on your dominant traits.
    
    **🎓 SPECIAL NOTE FOR GRADE 8 STUDENTS:**
    * **The "Transition" Strategy:** You are using this to plan your *entry* into high school. 
    * Use these results to start a conversation with your new high school counselor during course planning orientation. 
    * Focus on **Grade 9 introductory electives** (like Intro to Business, ICT 9, or General Visual Arts) that lead into the senior pathways shown below.
    """)

st.markdown("---")

# --- INPUT SECTION: BEHAVIORAL PROFILING ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🛠️ Builder & Engineer")
    mech = st.slider("Working with tools/machines?", 1, 10, 5)
    code = st.slider("Coding or solving logic puzzles?", 1, 10, 5)
    build = st.slider("Building physical things?", 1, 10, 5)

with col2:
    st.markdown("### 🎨 Creator & Communicator")
    art = st.slider("Drawing, designing, or visual art?", 1, 10, 5)
    write = st.slider("Writing stories or essays?", 1, 10, 5)
    speak = st.slider("Public speaking/debating?", 1, 10, 5)

with col3:
    st.markdown("### 🔬 Analyst & Strategist")
    math = st.slider("Solving complex math problems?", 1, 10, 5)
    sci = st.slider("Scientific experiments/Theory?", 1, 10, 5)
    biz = st.slider("Business ideas/Money management?", 1, 10, 5)

with st.expander("More Options (Social & Active)"):
    col4, col5 = st.columns(2)
    with col4:
        people = st.slider("Helping people/Social justice?", 1, 10, 5)
        med = st.slider("Medical/Human anatomy interest?", 1, 10, 5)
    with col5:
        active = st.slider("Physical activity/Sports?", 1, 10, 5)
        food = st.slider("Cooking/Nutrition?", 1, 10, 5)

# --- ALGORITHM CORE ---
# Calculate Category Scores
scores = {
    "STEM & Tech": (mech + code + math + sci) / 4,
    "Creative Arts": (art + write + build) / 3,
    "Business & Leadership": (biz + speak + people) / 3,
    "Health & Human Services": (med + people + food) / 3,
    "Trades & Applied Skills": (mech + build + food) / 3,
    "Active Living": (active * 1.2) # Weighted heavily if they love sports
}

# --- LOGIC GATES ---
# 1. Engagement Filter: If total enthusiasm is low, flag it.
total_engagement = mech + code + build + art + write + speak + math + sci + biz + people + med + active + food
engagement_threshold = 48 # Arbitrary "low effort" line

# 2. Safety Valve: High Science but Low Medical? Don't suggest Health Sciences.
if sci > 7 and med < 4:
    scores["Health & Human Services"] -= 3 # Downrank significantly

# 3. The Tie-Breaker: Intensity
# (Already handled by the 'Active Living' weight, but we sort carefully below)

# Convert to DataFrame for easier handling
df_scores = pd.DataFrame(list(scores.items()), columns=['Category', 'Score'])
df_scores = df_scores.sort_values(by='Score', ascending=False)

top_category = df_scores.iloc[0]['Category']
top_score = df_scores.iloc[0]['Score']

# --- OUTPUT SECTION ---
st.markdown("---")
if st.button("🚀 Analyze My Pathway"):
    
    # CASE: LOW ENGAGEMENT
    if total_engagement < engagement_threshold:
        st.error("⚠️ **Low Engagement Detected**")
        st.write("It looks like you rated most things pretty low. To get a good result, try to find *something* you are passionate about (rated 7+).")
        st.write("For now, we recommend **Exploratory Electives** to find your spark:")
        st.info("Try: **Information Tech 9**, **General Business**, or **Visual Arts 9**.")
        
    else:
        # VISUALIZATION
        st.markdown(f"## 🏆 Top Match: **{top_category}**")
        
        # Chart
        fig = px.bar(df_scores, x='Score', y='Category', orientation='h', 
                     title="Your Interest Profile", color='Score', 
                     color_continuous_scale='Bluered')
        st.plotly_chart(fig, use_container_width=True)
        
        # --- COURSE RECOMMENDATIONS (BC CURRICULUM ALIGNED) ---
        st.markdown("### 📚 Recommended Electives (Grades 9-12)")
        
        if top_category == "STEM & Tech":
            st.success("**Pathway: Engineering & Computer Science**")
            st.write("* **Grade 9/10:** ICT 9, Electronics & Robotics 10, Science 10 (Honours)")
            st.write("* **Grade 11/12:** Computer Science 11/12, Physics 11/12, Calculus 12")
            st.write("* **Career:** Software Engineer, Data Analyst, Civil Engineer")
            
        elif top_category == "Creative Arts":
            st.success("**Pathway: Design & Media**")
            st.write("* **Grade 9/10:** Visual Arts 9, Drama 9/10, Media Arts 10")
            st.write("* **Grade 11/12:** Graphic Design 11, Studio Arts 3D 11/12, Photography 12")
            st.write("* **Career:** UX Designer, Architect, Content Creator")
            
        elif top_category == "Business & Leadership":
            st.success("**Pathway: Commerce & Law**")
            st.write("* **Grade 9/10:** Entrepreneurship & Marketing 10, Social Studies 10")
            st.write("* **Grade 11/12:** Accounting 11, Marketing 12, Economics 12, Law 12")
            st.write("* **Career:** Project Manager, Accountant, Lawyer")
            
        elif top_category == "Health & Human Services":
            st.success("**Pathway: Health & Education**")
            st.write("* **Grade 9/10:** Food Studies 9/10, Science 10")
            st.write("* **Grade 11/12:** Anatomy & Physiology 12, Chemistry 11/12, Psychology 12")
            st.write("* **Career:** Nurse, Teacher, Social Worker, Nutritionist")
            
        elif top_category == "Trades & Applied Skills":
            st.success("**Pathway: Skilled Trades**")
            st.write("* **Grade 9/10:** Woodwork 9/10, Metalwork 10, Drafting 10")
            st.write("* **Grade 11/12:** Automotive Technology 11, Carpentry 11/12, Culinary Arts 11")
            st.write("* **Career:** Electrician, Red Seal Chef, Construction Manager")
            
        elif top_category == "Active Living":
            st.success("**Pathway: Athletics & Kinesiology**")
            st.write("* **Grade 9/10:** PHE 9/10, Leadership 10")
            st.write("* **Grade 11/12:** Active Living 11/12, Fitness & Conditioning 11/12")
            st.write("* **Career:** Physiotherapist, Coach, Firefighter")

        # --- NEXT STEPS ---
        st.markdown("---")
        st.markdown("### 📝 Your Next Steps")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("#### 1. The 'Why'")
            st.write("Review the courses above. Ask yourself: *Does this actually sound fun?*")
        with col_b:
            st.markdown("#### 2. The Verification")
            st.write("**REQUIRED:** Take this list to your school counselor (especially for Grade 12 grad requirements).")
        with col_c:
            st.markdown("#### 3. The Commit")
            st.write("Select 2 electives from your top category and 1 'Wildcard' from your second highest.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Built for BC Students | Unofficial Planning Tool</p>", unsafe_allow_html=True)
