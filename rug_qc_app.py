
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
    from xlsxwriter.utility import xl_rowcol_to_cell

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

        workbook = writer.book
        worksheet = writer.sheets['Grid']

        # Define formats for each severity level
        severity_formats = {
            1: workbook.add_format({'bg_color': '#90EE90', 'align': 'center'}),
            2: workbook.add_format({'bg_color': '#9ACD32', 'align': 'center'}),
            3: workbook.add_format({'bg_color': '#FFD700', 'align': 'center'}),
            4: workbook.add_format({'bg_color': '#FFA500', 'align': 'center'}),
            5: workbook.add_format({'bg_color': '#FF6347', 'align': 'center'}),
        }

        for defect in defects:
            location = defect.get("Grid Location", "")
            severity = defect.get("Severity (1–5)", "")
            if "cm x" in location and severity in severity_formats:
                try:
                    col_cm, row_cm = map(lambda x: int(x.strip().replace("cm", "")), location.split("cm x"))
                    col_idx = int(col_cm / interval_cm)
                    row_idx = int(row_cm / interval_cm)
                    excel_row = row_idx + 1  # account for header
                    excel_col = col_idx + 1  # account for index label
                    worksheet.write(excel_row, excel_col, severity, severity_formats[severity])
                except:
                    continue

    output.seek(0)
    return output

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
        "Photo Filename": photo.name if photo else "", "Photo Data": photo.read() if photo else None,
        "Video Filename": video.name if video else "", "Video Data": video.read() if video else None
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


if st.button("🖨️ Generate PDF Summary"):
    if st.session_state.defect_log:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=t["title"], ln=True, align="C")
        pdf.ln(10)

        from base64 import b64encode
        for i, defect in enumerate(st.session_state.defect_log, 1):
            photo_link = ""
            video_link = ""
            if defect.get("Photo Data"):
                encoded = b64encode(defect["Photo Data"]).decode()
                photo_link = f"[View Image](data:image/jpeg;base64,{encoded})"
            if defect.get("Video Data"):
                encoded = b64encode(defect["Video Data"]).decode()
                video_link = f"[View Video](data:video/mp4;base64,{encoded})"

            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 8, txt=f"Issue #{i}\nLocation: {defect['Grid Location']}\nSeverity: {defect['Severity (1–5)']}\nType: {defect['Type of Defect']}\nDescription: {defect['Description of Issue']}\nPhoto: {photo_link}\nVideo: {video_link}\n", border=1)
            pdf.ln(2)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        st.download_button(
            label="📄 Download PDF Summary",
            data=pdf_output,
            file_name="Rug_QC_Report.pdf",
            mime="application/pdf"
        )

    excel_file = create_rug_qc_excel(width, length, interval, st.session_state.defect_log)
    st.download_button(
        label=t["download"],
        data=excel_file,
        file_name="Rug_QC_Sheet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
