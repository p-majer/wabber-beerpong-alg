import streamlit as st
from wabballgorithm import matchmaker 

st.set_page_config(page_title="Matchmaker", layout="wide")

# Custom CSS to make it look modern
st.markdown("""
    <style>
    body {background-color: #f5f6fa;}
    .main {background-color: #ffffff; padding: 2rem; border-radius: 10px;}
    h1, h2, h3 {color: #222;}
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1rem;
    }
    .stButton>button:hover {
        background-color: #357ABD;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Tournament Matchmaker")

with st.sidebar:
    st.header("Settings")
    n_teams = st.number_input("Number of Teams", min_value=2, value=8)
    n_tables = st.number_input("Number of Tables", min_value=1, value=4)
    iterations = st.number_input("Iterations (Try 50–200)", min_value=1, value=50)

    st.markdown("---")
    st.subheader("Add Existing Matches (Optional)")

    existing_struct = {}
    add_existing = st.checkbox("Add existing matches manually")

    if add_existing:
        num_slots = st.number_input("How many timeslots so far?", min_value=1, value=1)
        for slot in range(1, num_slots + 1):
            st.markdown(f"**Timeslot {slot}**")
            num_matches = st.number_input(f"Matches in Timeslot {slot}", min_value=1, value=1, key=f"slot_{slot}")
            matches = []
            for m in range(num_matches):
                col1, col2 = st.columns(2)
                with col1:
                    a = st.number_input(f"Team A (Match {m+1})", min_value=1, max_value=n_teams, key=f"a_{slot}_{m}")
                with col2:
                    b = st.number_input(f"Team B (Match {m+1})", min_value=1, max_value=n_teams, key=f"b_{slot}_{m}")
                if a != b:
                    matches.append((int(a), int(b)))
            existing_struct[slot] = matches

    st.markdown("---")
    if st.button("Generate Schedule"):
        result = matchmaker(int(iterations), int(n_tables), int(n_teams), existing_struct)
        st.session_state["result"] = result

# ---------- DISPLAY RESULTS ----------

if "result" in st.session_state:
    result = st.session_state["result"]

    st.subheader("Match Schedule")

    cols = st.columns(3)
    for i, (slot, matches) in enumerate(result.items()):
        col = cols[i % 3]
        with col:
            st.markdown(f"### Timeslot {slot}")
            for match in matches:
                a, b = match
                st.markdown(f"- Team **{a}** vs Team **{b}**")
            st.markdown("---")

else:
    st.info("Use the sidebar to set your tournament details, then click Generate Schedule.")