import streamlit as st
import operator
import pandas as pd
import altair as alt

# ==========================================
# 1. APP CONFIGURATION & HEADER
# ==========================================
st.set_page_config(page_title="Pathfinder BC", page_icon="🧭", layout="centered")

# --- CUSTOM CSS FOR CLEAN LOOK ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(to bottom right, #e0f7fa, #e1bee7); }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stMarkdown, .stTitle, .stHeader, .stSubheader { color: #000000; }
</style>
""", unsafe_allow_html=True)

st.title("🧭 BC High School Course Compass")

# ==========================================
# 2. THE PITCH (ADDED BACK)
# ==========================================
with st.expander("ℹ️ About This Tool (The Problem & The Solution)", expanded=True):
    st.markdown("""
    ### 🛑 The Problem (Pain Points)
    * **Course Guides are Overwhelming:** The PDF guide is 60+ pages long. It's hard to find what you actually like.
    * **"Friend-Following":** Many students just pick the courses their friends pick, which leads to boredom and bad grades.
    * **The "Job" Trap:** Asking a 13-year-old *"What job do you want?"* is stressful. You shouldn't have to decide your career yet.
    
    ### 💡 The Idea
    This tool is a **"Cognitive Compass."** We don't ask about jobs. We ask about **how your brain works**.
    * Do you think in **Systems**? (Engineering)
    * Do you think in **Stories**? (Drama/Marketing)
    * Do you think in **People**? (Leadership/Socials)
    
    **The Goal:** To match your natural "Thinking Style" to the **BC High School Curriculum** so you actually enjoy your classes next year.
    """)

st.markdown("---")
st.markdown("""
#### ⚠️ Critical Instructions
1.  **Be Honest:** Pick what you *actually* do, not what you wish you did.
2.  **No Data Saved:** We do not store your answers. **Screenshot your result** at the end.
""")
st.markdown("---")

# ==========================================
# 3. THE QUESTION DATABASE
# ==========================================
question_database = [
    # --- A: Analytical ---
    {"id": 1,  "cat": "A", "w": 1.0, "text": "When making a big decision (like picking a new phone):", "opt1": "I go with my gut feeling or what looks cool.", "opt2": "I watch review videos and compare specs first."},
    {"id": 2,  "cat": "A", "w": 1.5, "text": "An app keeps crashing on your phone. You:", "opt1": "Get annoyed and stop using it.", "opt2": "Google the problem to see if there's a fix."},
    {"id": 3,  "cat": "A", "w": 1.5, "text": "When packing a bag for a trip:", "opt1": "I throw things in until it's full.", "opt2": "I organize it perfectly like Tetris to save space."},
    {"id": 4,  "cat": "A", "w": 1.5, "text": "When doing chores, I:", "opt1": "Just start the first one I see.", "opt2": "Plan the exact order to finish fastest."},
    {"id": 5,  "cat": "A", "w": 1.0, "text": "I prefer stories where:", "opt1": "Everything is explained at the end.", "opt2": "I have to solve the mystery myself."},
    {"id": 6,  "cat": "A", "w": 2.0, "text": "If I had free time, I would rather:", "opt1": "Write a short story.", "opt2": "Write code to make a robot move."},
    
    # --- N: Natural World ---
    {"id": 7,  "cat": "N", "w": 1.5, "text": "A friend is sick or hurt. Your immediate reaction is to:", "opt1": "Google their symptoms to see what's wrong logically.", "opt2": "Bring them water/blankets and try to comfort them."},
    {"id": 8,  "cat": "N", "w": 1.5, "text": "When it rains heavily, I:", "opt1": "Just use my umbrella.", "opt2": "Wonder where all the gutter water flows to."},
    {"id": 9,  "cat": "N", "w": 1.5, "text": "You are stuck on a hard riddle or puzzle. You:", "opt1": "Check the answer key after 5 minutes.", "opt2": "Refuse to look at the answer until you solve it."},
    {"id": 10, "cat": "N", "w": 1.0, "text": "I like animals because:", "opt1": "They are cute.", "opt2": "I want to know how they communicate."},
    {"id": 11, "cat": "N", "w": 1.5, "text": "When I look at food, I'd rather:", "opt1": "Learn how to cook it.", "opt2": "Learn what the vitamins do to my body."},
    {"id": 12, "cat": "N", "w": 2.0, "text": "If I saw a science experiment video:", "opt1": "I'd watch it and laugh.", "opt2": "I'd buy the ingredients to try it myself."},

    # --- C: Creative ---
    {"id": 13, "cat": "C", "w": 1.5, "text": "When using a new app, I often think:", "opt1": "'This works fine.'", "opt2": "'The buttons are in the wrong spot, I'd move them.'"},
    {"id": 14, "cat": "C", "w": 1.5, "text": "In group projects, I usually suggest:", "opt1": "The safe, standard ideas.", "opt2": "The crazy, weird ideas."},
    {"id": 15, "cat": "C", "w": 1.0, "text": "You have to do a slide presentation. You spend the most time on:", "opt1": "Writing the script so I say the right words.", "opt2": "Finding the perfect images and slide transitions."},
    {"id": 16, "cat": "C", "w": 2.0, "text": "In a customizable game (Minecraft/Sims/Roblox), I prefer to:", "opt1": "Play the game exactly how it's supposed to be played.", "opt2": "Spend hours building custom houses, skins, or maps."},
    {"id": 17, "cat": "C", "w": 1.0, "text": "When I finish a really good movie or show:", "opt1": "I just move on to the next one.", "opt2": "I go online to read theories and hidden details."},
    {"id": 18, "cat": "C", "w": 2.0, "text": "With YouTube/TikTok, I prefer to:", "opt1": "Watch and scroll.", "opt2": "Film, edit, and upload my own."},

    # --- S: Social ---
    {"id": 19, "cat": "S", "w": 2.0, "text": "You see a rare item at a thrift store for $5 that sells for $50 online. You:", "opt1": "Leave it there.", "opt2": "Buy it immediately to resell it for profit."},
    {"id": 20, "cat": "S", "w": 2.0, "text": "Your friend group is trying to plan a meetup but no one can decide. You:", "opt1": "Wait for someone else to pick a spot.", "opt2": "Create a poll or specific plan to force a decision."},
    {"id": 21, "cat": "S", "w": 1.5, "text": "If I love a movie, I:", "opt1": "Just enjoy it myself.", "opt2": "Try hard to convince my friends to watch it."},
    {"id": 22, "cat": "S", "w": 1.5, "text": "When friends are fighting, I:", "opt1": "Walk away.", "opt2": "Try to mediate and fix the problem."},
    {"id": 23, "cat": "S", "w": 1.5, "text": "Explaining things to others makes me:", "opt1": "Annoyed if they don't get it.", "opt2": "Happy when they have an 'Aha!' moment."},
    {"id": 24, "cat": "S", "w": 1.0, "text": "Speaking in front of the class makes me:", "opt1": "Want to hide.", "opt2": "Secretly enjoy the attention."},

    # --- P: Practical ---
    {"id": 25, "cat": "P", "w": 1.5, "text": "You see a weird machine you don't recognize. Your first instinct is to:", "opt1": "Ignore it.", "opt2": "Look at the back or press buttons to see how it works."},
    {"id": 26, "cat": "P", "w": 1.0, "text": "With phones, I care more about:", "opt1": "The apps and games.", "opt2": "The camera specs and processor speed."},
    {"id": 27, "cat": "P", "w": 2.0, "text": "I would rather:", "opt1": "Draw a picture of a house.", "opt2": "Build a model house with glue/cardboard."},
    {"id": 28, "cat": "P", "w": 1.5, "text": "If the WiFi stops, I:", "opt1": "Call my parents.", "opt2": "Check the cables and router myself."},
    {"id": 29, "cat": "P", "w": 2.0, "text": "I prefer working with:", "opt1": "My keyboard/screen.", "opt2": "My hands (tools, cooking, building)."},
    {"id": 30, "cat": "P", "w": 1.5, "text": "Have you ever taken a pen apart?", "opt1": "No, never.", "opt2": "Yes, to see the spring inside."}
]

# ==========================================
# 4. THE UI FORM
# ==========================================
user_answers = {}
with st.form("quiz_form"):
    for q in question_database:
        st.write(f"**{q['id']}. {q['text']}**")
        choice = st.radio("Select one:", (q['opt1'], q['opt2']), key=q['id'], label_visibility="collapsed", index=None)
        st.markdown("") 
        
        if choice == q['opt1']: user_answers[q['id']] = 1
        elif choice == q['opt2']: user_answers[q['id']] = 2
        else: user_answers[q['id']] = 0 
    
    st.markdown("---")
    submitted = st.form_submit_button("Find My Path 🚀", type="primary")

# ==========================================
# 5. LOGIC ENGINE (UNIVERSAL BC)
# ==========================================
if submitted:
    # A. Calculate Weighted Scores
    scores = {"A": 0, "N": 0, "C": 0, "S": 0, "P": 0}
    max_possible_scores = {"A": 0, "N": 0, "C": 0, "S": 0, "P": 0}
    
    for q in question_database:
        val = user_answers.get(q["id"], 0)
        scores[q["cat"]] += (val * q["w"])
        if val == 2: max_possible_scores[q["cat"]] += q["w"]

    total_score = sum(scores.values())

    # >>>>> 1. ENGAGEMENT FILTER <<<<<
    if total_score < 48:
        st.error(f"⚠️ **Engagement Score Too Low: {total_score} / 100**")
        st.info("Result Inconclusive. You selected 'Option 1' for almost everything. Please try again!")
        st.stop()

    # B. SORT & TIE-BREAKER
    sorted_cats = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    top_cat = sorted_cats[0][0]
    second_cat = sorted_cats[1][0]
    
    # Tie-Breaker
    if sorted_cats[0][1] == sorted_cats[1][1]:
        if max_possible_scores[second_cat] > max_possible_scores[top_cat]:
            top_cat, second_cat = second_cat, top_cat
    
    profile_code = top_cat + second_cat

    # C. CLUSTER MAPPINGS (UNIVERSAL BC CURRICULUM)
    force_non_medical = True if user_answers.get(7) == 1 else False
    
    final_cluster = "General Studies"
    cluster_desc = ""
    rec_courses = []
    launchpad_links = []

    # 1. THE BIO-ANALYSTS (Nature + Logic)
    if profile_code in ["AN", "NA"]:
        if force_non_medical:
            final_cluster = "BIO (Environmental & Research)"
            cluster_desc = "You are curious about the natural world but prefer understanding systems over medical issues."
            rec_courses = ["Food Studies 9/10", "Outdoor Education / Environmental Science", "Science 10"]
            launchpad_links = ["- [Khan Academy: Ecology](https://www.khanacademy.org/science/biology/ecology)"]
        else:
            final_cluster = "BIO (Health Sciences)"
            cluster_desc = "You have a strong analytical mind applied to living systems. You likely enjoy understanding the human body."
            rec_courses = ["Food Studies 9/10", "Science 10", "Intro to Health Sciences (if available)"]
            launchpad_links = ["- [Crash Course: Anatomy](https://www.youtube.com/playlist?list=PL8dPuuaLjXtOAKed_MxxWBNaPno5h3Zs8)"]
    
    # 2. THE ENGINEERS (Physics + Logic)
    elif profile_code in ["NP", "PN"]: 
        final_cluster = "PHY (Physics & Engineering)"
        cluster_desc = "You are driven by understanding 'how things work' in the physical world. You enjoy math and mechanics."
        rec_courses = ["ADST: Power Technology / Mechanics", "ADST: Drafting & Design", "Science 10"]
        launchpad_links = ["- [Mark Rober: Engineering](https://www.youtube.com/channel/UCY1kMZp36IQSyNx_9h4mpCg)"]
    
    # 3. THE BUILDERS (Practical + Analytical)
    elif profile_code in ["AP", "PA"]:
        final_cluster = "TECH (Robotics & Hardware)"
        cluster_desc = "You blend analytical thinking with hands-on building. You want to make machines move."
        rec_courses = ["ADST: Electronics & Robotics", "ADST: Metalwork", "ADST: Power Technology"]
        launchpad_links = ["- [Arduino Project Hub](https://create.arduino.cc/projecthub)"]
    
    # 4. THE CODERS (Analytical + Creative)
    elif profile_code in ["AC", "CA"]:
        final_cluster = "TECH (Coding & Digital)"
        cluster_desc = "You enjoy solving logical puzzles and creating digital systems using code."
        rec_courses = ["Computer Programming / Coding", "Digital Media Development", "ADST: Drafting (CAD)"]
        launchpad_links = ["- [freeCodeCamp](https://www.freecodecamp.org/)"]
    
    # 5. THE STRATEGISTS (Social + Analytical)
    elif profile_code in ["AS", "SA", "SB", "BS"]:
        final_cluster = "BUS (Business & Leadership)"
        cluster_desc = "You are goal-oriented and enjoy systems involving people, strategy, and value."
        rec_courses = ["Entrepreneurship & Marketing", "Leadership / Business Ed", "Economics"]
        launchpad_links = ["- [JA British Columbia](https://jabc.ca/)"]
    
    # 6. THE CREATORS (Creative + Social)
    elif profile_code in ["CS", "SC"]:
        final_cluster = "ART (Media & Communication)"
        cluster_desc = "You combine creativity with social awareness. You are great for storytelling and content creation."
        rec_courses = ["Visual Arts (2D/3D)", "Drama / Theatre", "Media Arts / Graphic Design"]
        launchpad_links = ["- [Canva Design School](https://www.canva.com/designschool/)"]
    
    # 7. THE MAKERS (Practical + Creative)
    elif profile_code in ["CP", "PC"]:
        final_cluster = "ART (Architecture & Design)"
        cluster_desc = "You are a 'Practical Creative.' You want to design functional things using structure and craft."
        rec_courses = ["ADST: Woodwork / Carpentry", "Visual Arts", "ADST: Drafting"]
        launchpad_links = ["- [SketchUp Free](https://www.sketchup.com/plans-and-pricing/sketchup-free)"]
    
    else:
        final_cluster = "General Exploration"
        cluster_desc = "Your interests are balanced. Try a 'Rotation' of courses to find your spark."
        rec_courses = ["ADST Rotation (Wood/Metal/Drafting)", "Visual Arts", "Food Studies"]
        launchpad_links = ["- [Ted-Ed](https://ed.ted.com/)"]

    # --- DISPLAY RESULTS ---
    st.balloons()
    
    # Header & Desc
    st.header(f"Recommended Cluster: {final_cluster}")
    st.subheader(f"Code: {profile_code}")
    st.info(f"**Why this cluster?**\n\n{cluster_desc}")
    st.success(f"**Typical Electives:** {', '.join(rec_courses)}")
    
    # Activities & Links
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🚀 Free Learning")
        for link in launchpad_links: st.markdown(link)
    with col2:
        st.info("💡 **Reminder:** Your results disappear when you close this tab.")

    # ==========================================
    # ACTION PLAN
    # ==========================================
    st.markdown("---")
    st.subheader("📝 Your 3-Step Action Plan")
    
    ac1, ac2, ac3 = st.columns(3)
    
    with ac1:
        st.markdown("#### 1. Save It 📸")
        st.write("Take a screenshot or photo of your **Profile Code** and **Chart** right now.")
    
    with ac2:
        st.markdown("#### 2. Research It 📖")
        st.write(f"Open your school's Course Guide. Look for courses in **{final_cluster}**. Read the descriptions.")
    
    with ac3:
        st.markdown("#### 3. Verify It 🗣️")
        st.write("Show this result to your School Counsellor or a Parent. Ask them: *'Does this look like a good fit for me?'*")
    
    st.warning("💡 **Tip:** If your 'Analytical' and 'Creative' bars are almost equal, you are a **Hybrid**. You should look at courses from *both* lists!")

    st.markdown("---")
    
    # Chart
    st.write("### 📊 Your Personality Breakdown")
    chart_data = pd.DataFrame({
        'Trait': ["Analytical", "Natural", "Creative", "Social", "Practical"],
        'Score': [scores["A"], scores["N"], scores["C"], scores["S"], scores["P"]],
    })
    c = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Trait', sort=None),
        y='Score',
        color=alt.Color('Trait', scale=alt.Scale(scheme='tableau10'), legend=None),
        tooltip=['Trait', 'Score']
    ).properties(height=300)
    st.altair_chart(c, use_container_width=True)
    
    # FOOTER
    st.markdown("---")
    with st.expander("⚙️ How this Algorithm Works"):
        st.write("This tool uses a weighted behavioral analysis to map your natural instincts to general High School Electives (ADST, Arts, and Sciences).")
