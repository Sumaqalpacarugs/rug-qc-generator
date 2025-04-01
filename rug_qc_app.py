
import streamlit as st
import pandas as pd


# Display table with color-coded severity (excluding binary data)
if st.session_state.defect_log:
    # Exclude binary data for display
    df_display = pd.DataFrame([
        {k: v for k, v in d.items() if k not in ["Photo Data", "Video Data"]}
        for d in st.session_state.defect_log
    ])

    def color_severity(val):
        color = ''
        if val == 5: color = 'red'
        elif val == 4: color = 'orange'
        elif val == 3: color = 'gold'
        elif val == 2: color = 'yellowgreen'
        elif val == 1: color = 'lightgreen'
        return f'background-color: {color}'

    st.dataframe(df_display.style.applymap(color_severity, subset=["Severity (1–5)"]))

