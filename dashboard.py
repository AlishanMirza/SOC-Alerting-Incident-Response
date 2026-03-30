import streamlit as st
import os

INCIDENT_DIR = "incident_reports"

st.title("SOC Incident Dashboard")

if os.path.exists(INCIDENT_DIR):

    files = os.listdir(INCIDENT_DIR)

    if files:

        for file in files:

            st.subheader(file)

            with open(os.path.join(INCIDENT_DIR, file)) as f:

                st.text(f.read())

    else:

        st.write("No incidents detected")

else:

    st.write("Incident directory not found")