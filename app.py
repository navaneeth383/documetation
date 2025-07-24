import streamlit as st
from docx import Document
from docx.shared import Inches
import base64
import os
from io import BytesIO
import zipfile

st.set_page_config(page_title="Project Doc Generator", layout="wide")

# ----------------- Sidebar -----------------
st.sidebar.title("📄 Project Documentation Generator")
st.sidebar.markdown("Created by **Gattu Navaneeth Rao**")

# ----------------- Main UI -----------------
st.title("📝 AI-Powered Project Documentation Generator")

project_title = st.text_input("Enter Project Title", "AI Project Documentation")

user_notes = st.text_area("✍️ Add any specific text you'd like to include in the documentation")

uploaded_code_files = st.file_uploader(
    "📂 Upload Code Files (.py, .sql, .ipynb, .txt)", accept_multiple_files=True
)

uploaded_support_files = st.file_uploader(
    "🧾 Upload Supporting Files (images, excel, screenshots etc.)", accept_multiple_files=True
)

# ----------------- Utility Functions -----------------
def detect_language(content):
    if "import " in content or "def " in content:
        return "Python"
    elif "SELECT " in content.upper():
        return "SQL"
    elif "nbformat" in content:
        return "Jupyter Notebook"
    else:
        return "Text"

def clean_code(text):
    return text.replace('\r', '').replace('\t', '    ')

# ----------------- Document Generation -----------------
if st.button("📘 Create Documentation"):
    doc = Document()

    doc.add_heading(project_title, 0)
    doc.add_paragraph(f"Author: Gattu Navaneeth Rao")

    if user_notes:
        doc.add_heading("Project Notes", level=1)
        doc.add_paragraph(user_notes)

    if uploaded_code_files:
        doc.add_heading("Code Files", level=1)
        for file in uploaded_code_files:
            content = file.read().decode("utf-8", errors="ignore")
            lang = detect_language(content)
            doc.add_heading(f"{file.name} ({lang})", level=2)
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(clean_code(content))
            run.font.name = 'Courier New'

    if uploaded_support_files:
        doc.add_heading("Supporting Files", level=1)
        for file in uploaded_support_files:
            if file.type.startswith("image/"):
                image_stream = BytesIO(file.read())
                doc.add_picture(image_stream, width=Inches(5))
                doc.add_paragraph(f"Screenshot: {file.name}")
            else:
                doc.add_paragraph(f"Attached File: {file.name}")

    # ----------------- Save and Download -----------------
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.success("✅ Documentation created successfully!")

    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="project_documentation.docx">📥 Download .docx</a>'
    st.markdown(href, unsafe_allow_html=True)
