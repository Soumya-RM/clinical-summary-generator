import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/generate_summary"

st.set_page_config(
    page_title="Clinical Summary Generator",
    layout="wide"
)

st.title("🩺 Clinical Summary Generator")
st.write("Generate a structured, evidence-based clinical summary from EHR data.")

# -----------------------------
# Input
# -----------------------------
patient_id = st.number_input(
    "Enter Patient ID",
    min_value=1,
    step=1
)

generate = st.button("Generate Summary")

# -----------------------------
# API Call
# -----------------------------
if generate:
    with st.spinner("Generating clinical summary..."):
        response = requests.post(
            API_URL,
            json={"patient_id": patient_id}
        )

    if response.status_code != 200:
        st.error(response.json().get("detail", "Unknown error"))
    else:
        data = response.json()

        # -----------------------------
        # Display Sections
        # -----------------------------
        def render_section(title, section):
            st.subheader(title)
            st.write(section["text"])

            if section.get("citations"):
                with st.expander("📌 Citations"):
                    st.json(section["citations"])

        render_section("Overview", data["overview"])
        render_section("Diagnoses", data["diagnoses"])
        render_section("Functional Status", data["functional_status"])
        render_section("Vitals", data["vitals"])
        render_section("Wounds", data["wounds"])
        render_section("Medications", data["medications"])
