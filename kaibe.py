# Professional Streamlit Cosmetics Invoice App

import streamlit as st
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import tempfile
import os
import requests
from PIL import Image
from io import BytesIO

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Luxury Cosmetics Invoice",
    page_icon="🧴",
    layout="wide"
)

# =========================
# WATERMARK IMAGE (URL ONLY)
# =========================

WATERMARK_URL = "https://drive.google.com/uc?export=download&id=116j_pRgzSW_hAJvJwqatx32E8kkwzFMI"  # ← حط اللوجو هنا

def get_watermark():

    response = requests.get(WATERMARK_URL)
    img = Image.open(BytesIO(response.content)).convert("RGBA")

    # make transparent watermark
    alpha = img.split()[3]
    alpha = alpha.point(lambda p: p * 0.15)
    img.putalpha(alpha)

    path = os.path.join(tempfile.gettempdir(), "wm.png")
    img.save(path)

    return path


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #f6ede8;
}

.block-container {
    padding-top: 2rem;
}

.title-box {
    background: linear-gradient(135deg, #d8b4a0, #e8cfc2);
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.1);
}

.section-box {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    border: 1px solid #eadfd8;
}

.stButton>button {
    width: 100%;
    background-color: #d8b4a0;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
}

.stDownloadButton>button {
    width: 100%;
    background-color: #2a2a2a;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="title-box">
    <h1>Luxury Cosmetics Invoice System</h1>
    <p>Create Professional PDF Invoices Easily</p>
</div>
""", unsafe_allow_html=True)

# =========================
# STORE INFO
# =========================

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("🏪 Store Information")

col1, col2 = st.columns(2)

with col1:
    store_name = st.text_input("Store Name", "KAI BEAUTY")
    store_phone = st.text_input("Phone Number")

with col2:
    store_address = st.text_input("Store Address")
    store_website = st.text_input("Website", "www.kaibedaily.com")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CUSTOMER INFO
# =========================

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("👤 Customer Information")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("Customer Name")
    customer_phone = st.text_input("Customer Phone")

with col2:
    customer_address = st.text_input("Customer Address")
    invoice_number = st.text_input("Invoice Number", f"INV-{datetime.now().strftime('%Y%m%d%H%M')}")

invoice_date = st.date_input("Invoice Date")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PRODUCTS
# =========================

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("🛍 Product Details")

num_products = st.number_input(
    "Number of Products",
    min_value=1,
    max_value=20,
    value=3
)

products = []

for i in range(num_products):

    st.markdown(f"### Product {i+1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        product_name = st.text_input(f"Product Name {i}", key=f"name_{i}")

    with col2:
        quantity = st.number_input(f"Quantity {i}", min_value=1, value=1, key=f"qty_{i}")

    with col3:
        price = st.number_input(f"Price {i}", min_value=0.0, value=0.0, key=f"price_{i}")

    total = quantity * price

    with col4:
        st.metric("Total", f"{total:.2f} EGP")

    products.append([product_name, quantity, price, total])

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PAYMENT SECTION
# =========================

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("💰 Payment Details")

col1, col2, col3 = st.columns(3)

subtotal = sum([p[3] for p in products])

with col1:
    shipping = st.number_input("Shipping", value=0.0)

with col2:
    discount = st.number_input("Discount", value=0.0)

with col3:
    tax = st.number_input("Tax", value=0.0)

final_total = subtotal + shipping + tax - discount

st.markdown(f"""
<div style="
background:#fff5ef;
padding:20px;
border-radius:18px;
text-align:center;
margin-top:20px;
border:1px solid #eadfd8;
">
<h2 style="color:#d8b4a0;">Grand Total</h2>
<h1 style="color:#2a2a2a;">{final_total:.2f} EGP</h1>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# PDF CLASS (WITH WATERMARK)
# =========================

class PDF(FPDF):

    def header(self):

        # WATERMARK
        wm_path = get_watermark()
        self.image(wm_path, x=35, y=60, w=140)

        self.set_fill_color(216, 180, 160)
        self.rect(0, 0, 220, 40, 'F')

        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 24)
        self.cell(0, 15, store_name, ln=True, align='C')

        self.set_font('Helvetica', '', 12)
        self.cell(0, 10, 'Luxury Cosmetics Invoice', ln=True, align='C')

        self.ln(15)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, 'Thank You For Your Order', align='C')


# =========================
# GENERATE PDF
# =========================

if st.button("✨ Generate Professional PDF Invoice"):

    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(42, 42, 42)
    pdf.cell(0, 10, 'Customer Information', ln=True)

    pdf.set_font('Helvetica', '', 12)

    pdf.cell(100, 8, f'Customer: {customer_name}', ln=True)
    pdf.cell(100, 8, f'Phone: {customer_phone}', ln=True)
    pdf.cell(100, 8, f'Address: {customer_address}', ln=True)

    pdf.ln(5)

    pdf.cell(100, 8, f'Invoice Number: {invoice_number}', ln=True)
    pdf.cell(100, 8, f'Date: {invoice_date}', ln=True)

    pdf.ln(10)

    pdf.set_fill_color(216, 180, 160)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 12)

    pdf.cell(70, 10, 'Product', 1, 0, 'C', True)
    pdf.cell(30, 10, 'Qty', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Price', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Total', 1, 1, 'C', True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 11)

    for item in products:
        pdf.cell(70, 10, str(item[0]), 1)
        pdf.cell(30, 10, str(item[1]), 1, 0, 'C')
        pdf.cell(40, 10, f'{item[2]:.2f} EGP', 1, 0, 'C')
        pdf.cell(40, 10, f'{item[3]:.2f} EGP', 1, 1, 'C')

    pdf.ln(10)

        # =========================
    # PAYMENT SUMMARY
    # =========================

    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(42, 42, 42)
    pdf.cell(0, 10, 'Payment Summary', ln=True)

    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)

    pdf.cell(0, 8, f'Subtotal: {subtotal:.2f} EGP', ln=True)
    pdf.cell(0, 8, f'Shipping: {shipping:.2f} EGP', ln=True)
    pdf.cell(0, 8, f'Tax: {tax:.2f} EGP', ln=True)
    pdf.cell(0, 8, f'Discount: {discount:.2f} EGP', ln=True)

    pdf.ln(5)

    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(216, 180, 160)

    pdf.cell(0, 12, f'Grand Total: {final_total:.2f} EGP', ln=True)

    pdf.ln(10)

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100, 100, 100)

    pdf.multi_cell(
        0,
        8,
        f'{store_name}\n{store_phone}\n{store_address}\n{store_website}',
        align='C'
    )

    pdf_bytes = pdf.output(dest='S')

    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode('latin-1')

    st.session_state["pdf_data"] = pdf_bytes
    st.session_state["invoice_name"] = f"{invoice_number}.pdf"

    st.success("PDF Invoice Generated Successfully! 🎉")


# =========================
# DOWNLOAD
# =========================

if st.session_state.get("pdf_data"):

    st.download_button(
        label="📥 Download Professional Invoice PDF",
        data=st.session_state["pdf_data"],
        file_name=st.session_state["invoice_name"],
        mime="application/pdf"
    )