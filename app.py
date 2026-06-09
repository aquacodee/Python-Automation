import streamlit as st
import subprocess
import os
import time
import yaml
import inspect
import csv
from PIL import Image
from faker import Faker
import random
import pandas as pd
import qrcode
import requests
import pyttsx3
import pyshorteners
import numpy as np
import webbrowser
import smtplib
from email.message import EmailMessage
import psutil
import pyperclip
import yt_dlp
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoPilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── STYLES ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0a !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f0f !important;
    border-right: 1px solid #1e1e1e !important;
    padding-top: 2rem !important;
}
[data-testid="stSidebar"] * { color: #e8e8e8 !important; }
[data-testid="stSidebar"] .stMarkdown p {
    color: #666 !important;
    font-size: 0.75rem !important;
    line-height: 1.7 !important;
}
[data-testid="stSidebar"] hr {
    border-color: #1e1e1e !important;
    margin: 1.5rem 0 !important;
}

/* ── Sidebar title ── */
[data-testid="stSidebar"] h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #fff !important;
    margin-bottom: 1rem !important;
}

/* ── Main area ── */
[data-testid="stMainBlockContainer"] {
    padding: 3rem 4rem !important;
    max-width: 960px !important;
}

/* ── Page title ── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: #fff !important;
    margin-bottom: 0 !important;
}

/* ── Section headers ── */
h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    color: #fff !important;
    letter-spacing: -0.01em !important;
}
h3 { font-size: 1.1rem !important; margin-top: 2rem !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: #444 !important;
}
[data-testid="stSelectbox"] label {
    color: #555 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Text inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #fff !important;
    box-shadow: none !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label {
    color: #555 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Slider ── */
[data-testid="stSlider"] label {
    color: #555 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #fff !important;
    border-color: #fff !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #111 !important;
    border: 1px dashed #2a2a2a !important;
    border-radius: 6px !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #444 !important;
}
[data-testid="stFileUploader"] label {
    color: #555 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stFileUploader"] span { color: #888 !important; font-size: 0.8rem !important; }

/* ── Multiselect ── */
[data-testid="stMultiSelect"] > div > div {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
}
[data-testid="stMultiSelect"] label {
    color: #555 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    border-radius: 4px !important;
    color: #ccc !important;
    font-size: 0.75rem !important;
}

/* ── Run button ── */
[data-testid="stButton"] > button {
    background: #fff !important;
    color: #0a0a0a !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
    margin-top: 1rem !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #e8e8e8 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.4rem !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    transition: border-color 0.2s, color 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: #888 !important;
    color: #fff !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0f0f0f !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 6px !important;
    margin-top: 2rem !important;
}
[data-testid="stExpander"] summary {
    color: #555 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-family: 'DM Mono', monospace !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stExpander"] summary:hover { color: #aaa !important; }

/* ── Code block ── */
[data-testid="stCode"], .stCodeBlock {
    background: #0f0f0f !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 6px !important;
    font-size: 0.75rem !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 6px !important;
    border-left-width: 3px !important;
    background: #111 !important;
    font-size: 0.82rem !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Success / warning / error colors ── */
.stSuccess { border-left-color: #4ade80 !important; color: #4ade80 !important; }
.stWarning { border-left-color: #fbbf24 !important; color: #fbbf24 !important; }
.stError   { border-left-color: #f87171 !important; color: #f87171 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e1e1e !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}

/* ── Divider ── */
hr { border-color: #1e1e1e !important; margin: 2rem 0 !important; }

/* ── Script description ── */
.script-desc {
    color: #555;
    font-size: 0.8rem;
    line-height: 1.7;
    margin: 0.4rem 0 1.6rem 0;
    font-family: 'DM Mono', monospace;
}

/* ── Category badge ── */
.category-tag {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 3px;
    color: #666;
    font-size: 0.65rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 2px 8px;
    margin-bottom: 0.6rem;
}

/* ── Wordmark ── */
.wordmark {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 2rem;
}
.wordmark span { color: #444; font-weight: 400; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #444; }

/* ── Image display ── */
[data-testid="stImage"] img {
    border-radius: 6px !important;
    border: 1px solid #1e1e1e !important;
}

/* ── Columns gap ── */
[data-testid="stColumns"] { gap: 1.5rem !important; }

/* ── Input number buttons ── */
[data-testid="stNumberInput"] button {
    background: #1a1a1a !important;
    border-color: #2a2a2a !important;
    color: #888 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── HELPERS ────────────────────────────────────────────────────────────────────
def load_scripts_from_yaml(yaml_file):
    with open(yaml_file, "r") as stream:
        return yaml.safe_load(stream)


def save_uploaded_file(uploadedfile):
    if not os.path.exists("tempDir"):
        os.makedirs("tempDir")
    file_path = os.path.join("tempDir", uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return file_path


scripts_data = load_scripts_from_yaml("scripts.yaml")


# ── INPUT HANDLER ──────────────────────────────────────────────────────────────
def handle_inputs(selected_script):
    inputs = {}
    operation = None

    for input_item in selected_script["inputs"]:
        key = input_item["name"]
        if input_item["type"] == "file":
            inputs[key] = st.file_uploader(
                input_item["name"],
                type=input_item["format"].split(", "),
                key=key,
            )
        elif input_item["type"] == "files":
            inputs[key] = st.file_uploader(
                input_item["name"],
                type=input_item["format"].split(", "),
                accept_multiple_files=True,
                key=key,
            )
        elif input_item["type"] == "text" and "options" in input_item:
            inputs[key] = st.selectbox(
                input_item["name"], input_item["options"], key=key
            )
        elif input_item["type"] == "text":
            inputs[key] = st.text_input(input_item["name"], key=key)
        elif input_item["type"] == "number":
            inputs[key] = st.number_input(
                input_item["name"], min_value=1, step=1, key=key
            )
        elif input_item["type"] == "textarea":
            inputs[key] = st.text_area(input_item["name"], key=key)
        elif input_item["type"] == "select":
            inputs[key] = st.selectbox(
                input_item["name"], options=input_item["options"], key=key
            )
            if input_item["name"] == "Operation":
                operation = inputs[key]
        elif input_item["type"] == "slider":
            inputs[key] = st.slider(
                input_item["name"],
                min_value=float(input_item.get("min", 0)),
                max_value=float(input_item.get("max", 3)),
                value=float(input_item.get("value", 1)),
                step=float(input_item.get("step", 0.1)),
                key=key,
            )

    if operation:
        dependent_inputs = {
            "Convert Format": ["Format"],
            "Combine Images": ["Second Image"],
            "Resize": ["New Width", "New Height"],
            "Flip": ["Direction"],
            "Blur": ["Blur Radius"],
            "Add Shadow": [],
            "Crop": ["Left", "Upper", "Right", "Lower"],
            "Adjust Brightness": ["Brightness"],
            "Add Watermark": ["Watermark Text"],
            "Rotate": ["Angle"],
        }
        deps = dependent_inputs.get(operation, [])
        if deps:
            st.markdown(
                f"<div style='color:#555;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;margin:1rem 0 0.5rem'>— {operation} options</div>",
                unsafe_allow_html=True,
            )
        for dependent_input in deps:
            for input_item in selected_script["inputs"]:
                if input_item["name"] == dependent_input:
                    key = f"{operation}_{dependent_input}"
                    if input_item["type"] == "file":
                        inputs[dependent_input] = st.file_uploader(
                            dependent_input,
                            type=input_item["format"].split(", "),
                            key=key,
                        )
                    elif input_item["type"] == "text":
                        inputs[dependent_input] = st.text_input(
                            dependent_input, key=key
                        )
                    elif input_item["type"] == "number":
                        inputs[dependent_input] = st.number_input(
                            dependent_input, min_value=1, step=1, key=key
                        )
                    elif input_item["type"] == "select":
                        inputs[dependent_input] = st.selectbox(
                            dependent_input, options=input_item["options"], key=key
                        )
                    elif input_item["type"] == "slider":
                        inputs[dependent_input] = st.slider(
                            dependent_input,
                            min_value=float(input_item.get("min", 0.0)),
                            max_value=float(input_item.get("max", 3.0)),
                            value=float(input_item.get("value", 1.0)),
                            step=float(input_item.get("step", 0.1)),
                            key=key,
                        )
    return inputs


# ── MAIN ───────────────────────────────────────────────────────────────────────
def main():
    if "selected_script_title" not in st.session_state:
        st.session_state.selected_script_title = ""

    # ── Sidebar ──
    with st.sidebar:
        st.markdown(
            '<div class="wordmark">⚡ <span>Auto</span>Pilot</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#444;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1.5rem">Python Automation</p>',
            unsafe_allow_html=True,
        )

        categories = sorted(set(s["category"] for s in scripts_data["scripts"]))
        selected_categories = st.multiselect(
            "Filter categories",
            options=categories,
            default=categories,
        )

        st.markdown("---")
        st.markdown(
            "<p style=\"color:#2a2a2a;font-size:0.7rem;font-family:'DM Mono',monospace\">Built with Streamlit</p>",
            unsafe_allow_html=True,
        )

    # ── Filter scripts ──
    selected_scripts = (
        scripts_data["scripts"]
        if not selected_categories
        else [
            s for s in scripts_data["scripts"] if s["category"] in selected_categories
        ]
    )
    script_titles = [s["title"] for s in selected_scripts]

    # ── Header ──
    st.markdown("<h1>Automation Scripts</h1>", unsafe_allow_html=True)
    st.markdown(
        '<div style="width:40px;height:2px;background:#fff;margin:0.6rem 0 2rem"></div>',
        unsafe_allow_html=True,
    )

    # ── Script selector ──
    selected_script_title = st.selectbox(
        "Select script",
        script_titles,
        index=(
            script_titles.index(st.session_state.selected_script_title)
            if st.session_state.selected_script_title in script_titles
            else 0
        ),
    )
    st.session_state.selected_script_title = selected_script_title

    selected_script = next(
        s for s in selected_scripts if s["title"] == selected_script_title
    )

    # ── Script info ──
    st.markdown(
        f'<div class="category-tag">{selected_script.get("category", "")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<h3>{selected_script["title"]}</h3>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="script-desc">{selected_script["description"]}</p>',
        unsafe_allow_html=True,
    )

    # ── Inputs ──
    inputs = handle_inputs(selected_script)

    # ── Run ──
    if st.button("Run →"):
        with st.spinner(""):
            run_selected_script(selected_script, inputs)

    # ── Source code expander ──
    with st.expander("View source"):
        function_code = get_function_code_by_id(selected_script["id"])
        st.code(function_code, language="python")


# ── FUNCTION MAP ───────────────────────────────────────────────────────────────
def get_function_code_by_id(script_id):
    function_code = {
        1: run_background_remover,
        2: run_qr_code_generator,
        3: run_fake_data_generator,
        4: run_url_shortener,
        5: run_youtube_downloader,
        6: run_bulk_email_sender,
        7: run_image_downloader,
        8: run_audiobook_converter,
        9: run_code_analyzer,
        10: run_resource_monitor,
        11: run_clipboard_manager,
        12: run_spell_checker,
        13: run_link_checker,
        14: run_news_reader,
        15: run_article_summarizer,
        16: run_image_editor,
    }
    fn = function_code.get(script_id)
    return inspect.getsource(fn) if fn else "# Function not implemented."


def run_selected_script(script, inputs):
    sid = script["id"]
    if sid == 1:
        run_background_remover(inputs["Image file"])
    elif sid == 2:
        run_qr_code_generator(inputs["Link"], inputs["Filename"])
    elif sid == 3:
        run_fake_data_generator(inputs["Number of entries"])
    elif sid == 4:
        run_url_shortener(inputs["Long URL"])
    elif sid == 5:
        run_youtube_downloader(inputs)
    elif sid == 6:
        run_bulk_email_sender(
            inputs["Sender email"], inputs["Sender password"], inputs["Emails file"]
        )
    elif sid == 7:
        run_image_downloader(inputs)
    elif sid == 8:
        run_audiobook_converter(inputs["PDF file"])
    elif sid == 9:
        run_code_analyzer(inputs["Python files"])
    elif sid == 10:
        run_resource_monitor(
            inputs["CPU threshold"],
            inputs["Memory threshold"],
            inputs["GPU threshold"],
            inputs["Battery threshold"],
        )
    elif sid == 11:
        run_clipboard_manager()
    elif sid == 12:
        run_spell_checker(inputs["Input text"])
    elif sid == 13:
        run_link_checker(inputs)
    elif sid == 14:
        run_news_reader(inputs["News API key"])
    elif sid == 15:
        run_article_summarizer(inputs["Article URL"])
    elif sid == 16:
        run_image_editor(inputs)


# ── SCRIPT FUNCTIONS ───────────────────────────────────────────────────────────


def run_background_remover(input_img_file):
    input_img_path = save_uploaded_file(input_img_file)
    output_img_path = (
        input_img_path.replace(".", "_rmbg.")
        .replace("jpg", "png")
        .replace("jpeg", "png")
    )
    try:
        from rembg import remove

        inp = Image.open(input_img_path)
        output = remove(inp)
        output.save(output_img_path, "PNG")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Before**")
            st.image(input_img_path)
            with open(input_img_path, "rb") as f:
                st.download_button(
                    "Download original",
                    f,
                    os.path.basename(input_img_path),
                    "image/jpeg",
                )
        with col2:
            st.markdown("**After**")
            st.image(output_img_path)
            with open(output_img_path, "rb") as f:
                st.download_button(
                    "Download result", f, os.path.basename(output_img_path), "image/png"
                )
        st.success("Background removed.")
    except Exception as e:
        st.error(f"Error: {e}")


def run_qr_code_generator(link, filename):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="white", back_color="#0a0a0a")
        img_file_path = os.path.join("tempDir", filename)
        if not os.path.exists("tempDir"):
            os.makedirs("tempDir")
        img.save(img_file_path)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(img_file_path, caption=link)
            with open(img_file_path, "rb") as f:
                st.download_button("Download QR", f, filename, "image/png")
    except Exception as e:
        st.error(f"Error: {e}")

# fake data generation
def run_fake_data_generator(num_entries):
    try:
        fake = Faker()
        data = [
            {
                "Name": fake.name(),
                "Address": fake.address(),
                "Email": fake.email(),
                "Phone": fake.phone_number(),
                "DOB": fake.date_of_birth(minimum_age=18, maximum_age=65),
                "Job": fake.job(),
                "Company": fake.company(),
            }
            for _ in range(num_entries)
        ]
        st.dataframe(pd.DataFrame(data), use_container_width=True)
        st.success(f"{num_entries} records generated.")
    except Exception as e:
        st.error(f"Error: {e}")


def run_url_shortener(long_url):
    try:
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(long_url)
        st.markdown(f"**Shortened URL**")
        st.code(short_url, language=None)
    except Exception as e:
        st.error(f"Error: {e}")


#bulk email sender
def run_bulk_email_sender(sender_email, sender_password, emails_file):
    file_path = save_uploaded_file(emails_file)
    try:
        df = pd.read_excel(file_path)
        for _, item in df.iterrows():
            msg = EmailMessage()
            msg["from"] = sender_email
            msg["to"] = item[0]
            msg["subject"] = item[1]
            msg.set_content(item[2])
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)
            st.write(f"✓ Sent to {item[0]}")
        st.success("All emails sent.")
    except Exception as e:
        st.error(f"Error: {e}")


def run_image_downloader(inputs):
    from simple_image_download import simple_image_download as simp

    keyword = inputs["Keyword for images"]
    num_images = inputs["Number of images"]
    try:
        response = simp.simple_image_download()
        response.download(keyword, num_images)
        st.success("Images downloaded.")
    except Exception as e:
        st.error(f"Error: {e}")


def run_audiobook_converter(pdf_file):
    temp_dir = "tempDir"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = save_uploaded_file(pdf_file)
    try:
        import PyPDF2

        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join(p.extract_text() or "" for p in reader.pages)

        timestamp = int(time.time())
        base = os.path.splitext(os.path.basename(file_path))[0]
        audio_path = os.path.join(temp_dir, f"{base}_{timestamp}.wav")

        engine = pyttsx3.init()
        engine.setProperty("rate", 125)
        engine.setProperty("volume", 1.0)
        voices = engine.getProperty("voices")
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)
        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        engine.stop()

        st.success("Audiobook created.")
        with open(audio_path, "rb") as f:
            st.download_button(
                "Download audiobook", f, f"{base}_{timestamp}.wav", "audio/wav"
            )
    except Exception as e:
        st.error(f"Error: {e}")


def run_code_analyzer(code_files):
    if not code_files:
        return
    try:
        pylint_out, flake8_out = [], []
        for file in code_files:
            fp = save_uploaded_file(file)
            r1 = subprocess.run(
                f"pylint {fp}", shell=True, capture_output=True, text=True
            )
            r2 = subprocess.run(
                f"flake8 {fp}", shell=True, capture_output=True, text=True
            )
            pylint_out.append(f"### pylint — {file.name}\n```\n{r1.stdout}\n```")
            flake8_out.append(f"### flake8 — {file.name}\n```\n{r2.stdout}\n```")
        st.success("Analysis complete.")
        st.markdown("\n\n".join(pylint_out + flake8_out))
    except Exception as e:
        st.error(f"Error: {e}")


def run_resource_monitor(
    cpu_threshold, memory_threshold, gpu_threshold, battery_threshold
):
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        bat = psutil.sensors_battery()

        col1, col2, col3 = st.columns(3)
        col1.metric("CPU", f"{cpu}%", delta=f"{cpu - cpu_threshold:+.0f}% vs threshold")
        col2.metric(
            "Memory", f"{mem}%", delta=f"{mem - memory_threshold:+.0f}% vs threshold"
        )
        if bat:
            col3.metric("Battery", f"{bat.percent}%")

        if cpu >= cpu_threshold:
            st.warning(f"CPU high: {cpu}%")
        if mem >= memory_threshold:
            st.warning(f"Memory high: {mem}%")
        if bat and bat.percent <= battery_threshold:
            st.warning(f"Battery low: {bat.percent}%")
    except Exception as e:
        st.error(f"Error: {e}")


def run_clipboard_manager():
    if "clipboard_contents" not in st.session_state:
        st.session_state.clipboard_contents = []

    def update_clipboard():
        item = pyperclip.paste()
        if item and item not in st.session_state.clipboard_contents:
            st.session_state.clipboard_contents.append(item)
        st.rerun()

    st.markdown("**Clipboard history**")
    if st.session_state.clipboard_contents:
        for item in st.session_state.clipboard_contents:
            st.code(item, language=None)
    else:
        st.markdown(
            '<p style="color:#444;font-size:0.8rem">No items yet — copy something and refresh.</p>',
            unsafe_allow_html=True,
        )

    st.button("Refresh", on_click=update_clipboard)

        
        
def run_youtube_downloader(inputs):
    import yt_dlp
    youtube_url = inputs["YouTube URL"]
    format_choice = inputs["Format"]
    ydl_opts = {
        "format": (
            "bestvideo+bestaudio/best" if format_choice == "Video" else "bestaudio/best"
        ),
        "outtmpl": os.path.join("tempDir", "%(title)s.%(ext)s"),
        "js_runtimes": { 
            "node": {}
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(youtube_url, download=True)
        download_path = ydl.prepare_filename(result)
        label = "Download Video" if format_choice == "Video" else "Download Audio"
        mime_type = "video/mp4" if format_choice == "Video" else "audio/mp3"
        st.success("Download complete.")
        with open(download_path, "rb") as file:
            st.download_button(label, file, os.path.basename(download_path), mime_type)
    except Exception as e:
        st.error(f"Error: {e}")


def run_spell_checker(sample_text):
    try:
        import lmproof

        proof = lmproof.load("en")
        result = proof.proofread(sample_text)
        st.markdown("**Corrected text**")
        st.text_area("Output", value=result, height=200)
    except Exception as e:
        st.error(f"Error: {e}")


def run_article_summarizer(url):
    try:
        from bs4 import BeautifulSoup
        from transformers import BartTokenizer, BartForConditionalGeneration

        headers = {"User-Agent": "Mozilla/5.0"}
        soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        model_name = "facebook/bart-large-cnn"
        tokenizer = BartTokenizer.from_pretrained(model_name)
        model = BartForConditionalGeneration.from_pretrained(model_name)
        ids = tokenizer("summarize: " + text, return_tensors="pt").input_ids
        summary = tokenizer.decode(
            model.generate(ids, max_length=150, min_length=30)[0],
            skip_special_tokens=True,
        )

        st.markdown("**Summary**")
        st.markdown(
            f'<p style="line-height:1.8;color:#ccc;font-size:0.88rem">{summary}</p>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Error: {e}")


def run_link_checker(inputs):
    links_file = inputs.get("Links file")
    links_text = inputs.get("Links text", "")

    if links_file:
        fp = save_uploaded_file(links_file)
        with open(fp) as f:
            links = [l.strip() for l in f.readlines() if l.strip()]
    else:
        links = [l.strip() for l in links_text.split("\n") if l.strip()]

    if not links:
        st.warning("No links provided.")
        return

    try:

        def get_status(url):
            try:
                return (
                    "✓ Working"
                    if requests.get(url, timeout=5).status_code == 200
                    else "✗ Error"
                )
            except:
                return "✗ Failed"

        results = {link: get_status(link) for link in links}
        df = pd.DataFrame(list(results.items()), columns=["URL", "Status"])
        st.dataframe(df, use_container_width=True)

        csv_name = st.text_input("Save as CSV", "web_status.csv")
        if st.button("Export CSV"):
            df.to_csv(csv_name, index=False)
            st.success(f"Saved to {csv_name}")
    except Exception as e:
        st.error(f"Error: {e}")


def run_news_reader(api_key):
    try:
        url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        articles = requests.get(url).json().get("articles", [])
        if not articles:
            st.warning("No articles found. Check your API key.")
            return
        for i, ar in enumerate(articles, 1):
            st.markdown(
                f'<p style="font-size:0.85rem;color:#ccc;padding:0.5rem 0;border-bottom:1px solid #1e1e1e"><span style="color:#444;margin-right:0.8rem">{i:02d}</span>{ar["title"]}</p>',
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"Error: {e}")


def run_image_editor(inputs):
    input_img_file = inputs["Image file"]
    operation = inputs["Operation"]
    input_img_path = save_uploaded_file(input_img_file)

    try:
        img = Image.open(input_img_path)
        output_img_path = None
        fmt = "png"

        if operation == "Convert Format":
            fmt = inputs.get("Format", "png").lower()
            output_img_path = os.path.join("tempDir", f"converted_image.{fmt}")
            img.save(output_img_path, format=fmt.upper())

        elif operation == "Combine Images":
            second = inputs.get("Second Image")
            if second:
                img2 = Image.open(save_uploaded_file(second))
                out = Image.new(
                    "RGB", (img.width + img2.width, max(img.height, img2.height))
                )
                out.paste(img, (0, 0))
                out.paste(img2, (img.width, 0))
                output_img_path = os.path.join("tempDir", "combined_image.png")
                out.save(output_img_path)

        elif operation == "Resize":
            out = img.resize((int(inputs["New Width"]), int(inputs["New Height"])))
            output_img_path = os.path.join("tempDir", "resized_image.png")
            out.save(output_img_path)

        elif operation == "Flip":
            d = inputs.get("Direction", "Horizontal")
            out = img.transpose(
                Image.FLIP_LEFT_RIGHT if d == "Horizontal" else Image.FLIP_TOP_BOTTOM
            )
            output_img_path = os.path.join("tempDir", "flipped_image.png")
            out.save(output_img_path)

        elif operation == "Blur":
            out = img.filter(ImageFilter.GaussianBlur(inputs.get("Blur Radius", 2)))
            output_img_path = os.path.join("tempDir", "blurred_image.png")
            out.save(output_img_path)

        elif operation == "Add Shadow":
            out = ImageOps.expand(img, border=20, fill="black")
            output_img_path = os.path.join("tempDir", "shadow_image.png")
            out.save(output_img_path)

        elif operation == "Crop":
            out = img.crop(
                (inputs["Left"], inputs["Upper"], inputs["Right"], inputs["Lower"])
            )
            output_img_path = os.path.join("tempDir", "cropped_image.png")
            out.save(output_img_path)

        elif operation == "Adjust Brightness":
            out = ImageEnhance.Brightness(img).enhance(inputs.get("Brightness", 1.0))
            output_img_path = os.path.join("tempDir", "brightness_image.png")
            out.save(output_img_path)

        elif operation == "Add Watermark":
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            text = inputs.get("Watermark Text", "watermark")
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(
                (img.width - tw - 10, img.height - th - 10),
                text,
                font=font,
                fill=(255, 255, 255, 128),
            )
            output_img_path = os.path.join("tempDir", "watermarked_image.png")
            img.save(output_img_path)

        elif operation == "Rotate":
            out = img.rotate(inputs.get("Angle", 90), expand=True)
            output_img_path = os.path.join("tempDir", "rotated_image.png")
            out.save(output_img_path)

        if output_img_path:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Before**")
                st.image(img)
            with col2:
                st.markdown("**After**")
                st.image(output_img_path)
            with open(output_img_path, "rb") as f:
                st.download_button(
                    f"Download — {operation}",
                    f,
                    os.path.basename(output_img_path),
                    f"image/{fmt}",
                )

    except Exception as e:
        st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
