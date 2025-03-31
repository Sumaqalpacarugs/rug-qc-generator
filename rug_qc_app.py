
import streamlit as st
import pandas as pd
import string
from io import BytesIO

# Translations
translations = {
    "en": {
        "title": "🧵 Rug QC Sheet Generator",
        "width": "Enter rug width (in cm or ft):",
        "length": "Enter rug length (in cm or ft):",
        "interval": "Grid interval (in cm):",
        "button": "Generate QC Excel Sheet",
        "download": "📥 Download Excel QC Sheet",
        "severity": "Severity Level (1–5)",
        "location": "Defect Location (e.g., 10 cm x 60 cm)",
        "description": "Description of the Issue",
        "type": "Type of Defect",
        "upload": "Upload Photo (Optional)",
        "video_upload": "Upload Video (Optional)",
        "log_title": "📝 Add a Defect Entry",
        "unit": "Select unit of measurement"
    },
    "es": {
        "title": "🧵 Generador de Hoja de Control de Calidad de Alfombras",
        "width": "Ingrese el ancho de la alfombra (en cm o pies):",
        "length": "Ingrese el largo de la alfombra (en cm o pies):",
        "interval": "Intervalo de cuadrícula (en cm):",
        "button": "Generar Hoja de Excel de CC",
        "download": "📥 Descargar Hoja de Excel de CC",
        "severity": "Nivel de Severidad (1–5)",
        "location": "Ubicación del Defecto (ej. 10 cm x 60 cm)",
        "description": "Descripción del Problema",
        "type": "Tipo de Defecto",
        "upload": "Subir Foto (Opcional)",
        "video_upload": "Subir Video (Opcional)",
        "log_title": "📝 Añadir una Entrada de Defecto",
        "unit": "Seleccione unidad de medida"
    }
}

# Defect log entries
defect_entries = []

def create_rug_qc_excel(rug_width_cm, rug_length_cm, interval_cm=5, defects=[]):
    num_columns = int(rug_width_cm / interval_cm)
    num_rows = int(rug_length_cm / interval_cm)

    column_labels_cm = [f"{i * interval_cm} cm" for i in range(num_columns)]
    row_labels_cm = [f"{i * interval_cm} cm" for i in range(num_rows)]

    grid = pd.DataFrame('', index=row_labels_cm, columns=column_labels_cm)

    defect_log = pd.DataFrame(defects)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        grid.to_excel(writer, sheet_name='Grid', index_label='Distance from Top (cm)')
        defect_log.to_excel(writer, sheet_name='Defect Log', index=False)

    output.seek(0)
    return output

# Language selector
lang = st.selectbox("Language / Idioma", ["en", "es"])
t = translations[lang]

# Unit selector
unit = st.selectbox(t["unit"], ["cm", "ft"])
conversion_factor = 30.48 if unit == "ft" else 1

# UI
st.title(t["title"])

width_input = st.number_input(t["width"], min_value=1.0, value=7.0 if unit == "ft" else 213.0)
length_input = st.number_input(t["length"], min_value=1.0, value=10.0 if unit == "ft" else 305.0)
interval = st.number_input(t["interval"], min_value=1, value=5)

width = width_input * conversion_factor
length = length_input * conversion_factor

st.subheader(t["log_title"])
location = st.text_input(t["location"])
description = st.text_area(t["description"])
defect_type = st.text_input(t["type"])
severity = st.slider(t["severity"], 1, 5, 3)
photo = st.file_uploader(t["upload"], type=["png", "jpg", "jpeg"])
video = st.file_uploader(t["video_upload"], type=["mp4", "mov", "avi"])

if "defect_log" not in st.session_state:
    st.session_state.defect_log = []

if st.button("➕ Add Defect"):
    entry = {
        "Grid Location": location,
        "Description of Issue": description,
        "Type of Defect": defect_type,
        "Severity (1–5)": severity,
        "Photo Filename": photo.name if photo else "",
        "Video Filename": video.name if video else ""
    }
    st.session_state.defect_log.append(entry)
    st.success("Defect added!")

if st.session_state.defect_log:
    df = pd.DataFrame(st.session_state.defect_log)
    def color_severity(val):
        color = ''
        if val == 5: color = 'red'
        elif val == 4: color = 'orange'
        elif val == 3: color = 'gold'
        elif val == 2: color = 'yellowgreen'
        elif val == 1: color = 'lightgreen'
        return f'background-color: {color}'

    st.dataframe(df.style.applymap(color_severity, subset=["Severity (1–5)"]))

if st.button(t["button"]):
    excel_file = create_rug_qc_excel(width, length, interval, st.session_state.defect_log)
    st.download_button(
        label=t["download"],
        data=excel_file,
        file_name="Rug_QC_Sheet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
