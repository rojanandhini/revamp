import streamlit as st
import pytesseract
import sqlite3
import pandas as pd
from pdf2image import convert_from_bytes
from PIL import Image
import re
import io

# --- PATH CONFIGURATION ---
POPPLER_PATH = r'C:\Program Files\poppler\poppler-24.08.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Bill Scanner Pro", layout="centered")
st.title("📄 Bill Scanner & Statement Generator")

# --- DB OPS (UNIFIED) ---
def db_op(v=None, d=None, a=None, mode="view"):
    conn = sqlite3.connect('bills_data.db')
    cursor = conn.cursor()
    # Initialize table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bills 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         Vendor TEXT, 
         BillDate TEXT, 
         Amount REAL)
    ''')
    if mode == "save":
        cursor.execute("INSERT INTO Bills (Vendor, BillDate, Amount) VALUES (?, ?, ?)", (v, d, a))
        conn.commit()
    elif mode == "reset":
        cursor.execute("DELETE FROM Bills")
        conn.commit()
    
    df = pd.read_sql("SELECT * FROM Bills", conn)
    conn.close()
    return df

# Initialize DB on load
db_op()

# --- OCR EXTRACTION LOGIC ---
def extract_bill_info(uploaded_file):
    file_bytes = uploaded_file.getvalue()
    
    if uploaded_file.type == "application/pdf":
        images = convert_from_bytes(file_bytes, poppler_path=POPPLER_PATH)
        text = "\n".join([pytesseract.image_to_string(img, lang='eng+ara') for img in images])
    else:
        img_obj = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(img_obj, lang='eng+ara')

    found_amounts = []
    fuzzy_patterns = [
        r"(?:BALANCE|PAID|TOTAL|AMOUNT|DUE).*?([\d,]+\.\d{2})",
        r"(?:AED|د\.إ|[B8DÐĐ|])\s?([\d,]+\.\d{2})",
    ]
    
    for pattern in fuzzy_patterns:
        matches = re.findall(pattern, text, re.I | re.DOTALL)
        for m in matches:
            try:
                val = float(m.replace(',', '').strip())
                if val > 0: found_amounts.append(val)
            except: continue

    extracted_total = 0.0
    if found_amounts:
        if "BALANCE" in text.upper():
            extracted_total = found_amounts[0]
        else:
            extracted_total = max(found_amounts)

    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 2]
    detected_header = lines[0] if lines else "Unknown"
    date_match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    extracted_date = date_match.group(1) if date_match else "Unknown"

    return {
        "Header": detected_header[:50], 
        "Date": extracted_date, 
        "Total": extracted_total
    }

# --- UI LOGIC ---
uploaded_file = st.file_uploader("Upload a Bill (JPG, PNG, or PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    with st.spinner("Scanning bill..."):
        data = extract_bill_info(uploaded_file)
    
    if data:
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader("🖼️ Bill Preview")
            if uploaded_file.type == "application/pdf":
                preview_images = convert_from_bytes(uploaded_file.getvalue(), first_page=1, last_page=1, poppler_path=POPPLER_PATH)
                st.image(preview_images[0], use_container_width=True)
            else:
                st.image(uploaded_file, use_container_width=True)

        with col_right:
            st.subheader("📝 Verify Data")
            final_header = st.text_input("Business Name", value=data["Header"])
            final_date = st.text_input("Bill Date", value=data["Date"])
            final_total = st.number_input("Total Amount (AED)", value=float(data["Total"]), format="%.2f")

            if st.button("💾 Save to Database", use_container_width=True):
                try:
                    db_op(final_header, final_date, final_total, mode="save")
                    st.success(f"Saved: {final_header}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Save Error: {e}")

# --- EXPORT & RESET ---
st.divider()
col_ex, col_rs = st.columns(2)

with col_ex:
    if st.button("📊 Export to Excel", use_container_width=True):
        df_export = db_op()
        out = io.BytesIO()
        with pd.ExcelWriter(out, engine='openpyxl') as w: 
            df_export.to_excel(w, index=False)
        st.download_button("📥 Download Excel", data=out.getvalue(), file_name="Statement.xlsx", use_container_width=True)

with col_rs:
    if st.button("🗑️ Reset Database", type="primary", use_container_width=True):
        db_op(mode="reset")
        st.warning("Database Cleared!")
        st.rerun()

# Preview Data
st.subheader("Recent Entries")
st.dataframe(db_op(), use_container_width=True)
