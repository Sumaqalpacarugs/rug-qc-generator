
import streamlit as st
import matplotlib.pyplot as plt

st.title("🧵 Rug QC Sheet Generator with Defect Visualization")

defects = [{"Grid Location": "10 cm x 60 cm", "Severity (1–5)": 3},
           {"Grid Location": "30 cm x 120 cm", "Severity (1–5)": 5}]

def display_defect_layout(width_cm, length_cm, interval_cm, defects):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, width_cm)
    ax.set_ylim(0, length_cm)
    ax.invert_yaxis()
    color_map = {1: 'green', 2: 'yellowgreen', 3: 'gold', 4: 'orange', 5: 'red'}

    for defect in defects:
        try:
            loc = defect["Grid Location"]
            severity = defect["Severity (1–5)"]
            x_cm, y_cm = map(lambda x: int(x.strip().replace("cm", "")), loc.split("cm x"))
            ax.plot(x_cm, y_cm, 'o', color=color_map[severity])
            ax.text(x_cm + 2, y_cm, str(severity), fontsize=8)
        except:
            continue

    ax.set_xlabel("Width (cm)")
    ax.set_ylabel("Length (cm)")
    ax.set_title("Defect Map")
    st.pyplot(fig)

display_defect_layout(213, 305, 5, defects)
