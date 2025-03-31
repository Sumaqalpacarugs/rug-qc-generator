
import streamlit as st
import pandas as pd
import string
from io import BytesIO

def create_rug_qc_excel(rug_width_cm, rug_length_cm, interval_cm=5):
    num_columns = int(rug_width_cm / interval_cm)
    num_rows = int(rug_length_cm / interval_cm)

    column_labels = list(string.ascii_uppercase)
    if num_columns > 26:
        column_labels += [a + b for a in string.ascii_uppercase for b in string.ascii_uppercase]
    column_labels = column_labels[:num_columns]

    grid = pd.DataFrame('', index=range(1, num_rows + 1), columns=column_labels)

    defect_log = pd.DataFrame(columns=[
        "Issue #", "Grid Location (e.g., C12)", "Description of Issue",
        "Type of Defect", "Severity (1–5)", "Action Taken"
    ])

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        grid.to_excel(writer, sheet_name='Grid', index_label='Row')
        defect_log.to_excel(writer, sheet_name='Defect Log', index=False)

    output.seek(0)
    return output

st.title("🧵 Rug QC Sheet Generator")

width = st.number_input("Enter rug width (in cm):", min_value=50, value=213)
length = st.number_input("Enter rug length (in cm):", min_value=50, value=305)
interval = st.number_input("Grid interval (in cm):", min_value=1, value=5)

if st.button("Generate QC Excel Sheet"):
    excel_file = create_rug_qc_excel(width, length, interval)
    st.download_button(
        label="📥 Download Excel QC Sheet",
        data=excel_file,
        file_name="Rug_QC_Sheet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
