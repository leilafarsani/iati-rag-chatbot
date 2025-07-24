# app.py

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

from utils.iati_api import fetch_iati_activities, get_country_options, get_sector_options, extract_code
from utils.embeddings import retrieve_context
from utils.llm import ask_llm

load_dotenv()

st.set_page_config(page_title="IATI Aid Chatbot", page_icon="🌍")
st.title("🌍 IATI Aid Chatbot")
st.markdown(
    "Explore live international aid activities from the [IATI Datastore](https://iatistandard.org). "
    "Start by filtering aid projects by country and sector, and optionally ask a question!"
)

st.divider()
st.subheader("🔎 Filter Aid Projects")

# Dropdown filters
dynamic_countries = get_country_options()
dynamic_sectors = get_sector_options()

col1, col2, col3 = st.columns(3)
with col1:
    country = st.selectbox("🌍 Country", [""] + [f"{name} ({code})" for code, name in dynamic_countries], key="country")
with col2:
    sector = st.selectbox("🏥 Sector", [""] + [f"{name} ({code})" for code, name in dynamic_sectors], key="sector")
with col3:
    year = st.text_input("📅 Year (optional)", placeholder="e.g. 2023")

# Reset
if st.button("🔁 Reset Filters"):
    st.session_state.clear()
    st.rerun()

# Proceed if filters are valid
if country and sector:
    with st.spinner("Fetching aid projects..."):
        try:
            activities = fetch_iati_activities(
                extract_code(country),
                extract_code(sector),
                year,
                limit=500
            )
            total = len(activities)

            if total == 0:
                st.warning("⚠️ No matching activities found.")
            else:
                st.success(f"✅ Found {total} matching activities.")
                st.subheader("📄 Matching Activities")

                df = pd.DataFrame(activities)
                csv = df.to_csv(index=False)

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.download_button("⬇️ Download Results as CSV", csv, "iati_activities.csv", "text/csv")
                with col2:
                    show_all = st.checkbox("Show all results")

                items_per_page = 10
                total_pages = (total - 1) // items_per_page + 1

                if not show_all:
                    page = st.number_input("📄 Page", min_value=1, max_value=total_pages, value=1)
                    start = (page - 1) * items_per_page
                    end = start + items_per_page
                    st.write(f"Showing results {start + 1} to {min(end, total)} of {total}")
                    display_activities = activities[start:end]
                else:
                    st.write(f"Showing all {total} results")
                    display_activities = activities

                for a in display_activities:
                    title = a.get("title_narrative", "Untitled")
                    desc = a.get("description_narrative")
                    date = a.get("activity_date_iso_date", "")

                    if isinstance(desc, list):
                        desc = desc[0] if desc else ""
                    elif not isinstance(desc, str):
                        desc = ""

                    with st.container():
                        st.markdown(f"**{title}**")
                        if desc:
                            st.caption(desc[:300] + "...")
                        if date:
                            st.caption(f"📅 {date}")
                        st.markdown("---")

                st.markdown("👉 *Want AI insights on these projects? Scroll down and ask a question!*")

                st.subheader("💬 Ask a Question About These Projects")
                st.markdown("💡 *Examples:*")
                st.code("What are these projects focused on?")
                st.code("Who is funding or implementing them?")
                st.code("Are they targeting children or schools?")

                query = st.text_input("Type your question (optional)")

                if query:
                    context = retrieve_context(activities, query)
                    if not context:
                        st.warning("No relevant information found.")
                    else:
                        answer = ask_llm(context, query)
                        st.subheader("🧠 Answer")
                        st.write(answer)

        except Exception as e:
            st.error(f"❌ Failed to fetch data: {e}")
else:
    st.info("⬆️ Please select both a **country** and a **sector** to begin.")
