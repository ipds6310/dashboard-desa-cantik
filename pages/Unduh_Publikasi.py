# -- coding: utf-8 --
from config.utils import pilih_desa_sidebar
from config.style_utils import inject_custom_css, section_header
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import base64
import os

st.set_page_config(
    page_title="Unduh Publikasi",
    page_icon="📚",
)

# ── Inject CSS kustom ──────────────────────────────────────────────────
inject_custom_css()

# ── Tambahan CSS khusus halaman ini ───────────────────────────────────
st.markdown("""
<style>
.pub-card {
    background: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s ease;
    height: 100%;
}
.pub-card:hover {
    box-shadow: 0 4px 14px rgba(0,0,0,0.09);
}
.pub-card img {
    width: 100%;
    border-radius: 8px;
    object-fit: cover;
    margin-bottom: 0.6rem;
}
.pub-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 0.4rem;
    line-height: 1.4;
}
.pub-link a {
    font-size: 0.84rem;
    color: #4a6cf7;
    text-decoration: none;
    font-weight: 500;
}
.pub-link a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ── Logo sidebar ───────────────────────────────────────────────────────
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("desa_cantik.png")
st.markdown(f"""
<style>
    [data-testid="stSidebarNav"] {{ margin-top: 20px; }}
    [data-testid="stSidebarNav"]::before {{
        content: ""; display: block;
        margin: 0 auto 20px auto;
        height: 120px; width: 120px;
        background-image: url("data:image/png;base64,{logo_base64}");
        background-size: contain; background-repeat: no-repeat; background-position: center;
    }}
</style>
""", unsafe_allow_html=True)

config = pilih_desa_sidebar()

# ── Koneksi Data ───────────────────────────────────────────────────────
conn = st.connection("gsheets", type=GSheetsConnection)
publikasi = pd.DataFrame(conn.read(spreadsheet=config['url_buku'], ttl=0))

# ── Header Halaman ─────────────────────────────────────────────────────
t1, t2 = st.columns((0.18, 1))
t1.image('logo pemkab tanbu.png', width=100)
t2.title(config['title'])
t2.markdown(f"**Halaman Unduh Publikasi {config['nmdesa']}**")

st.markdown("---")
section_header("Publikasi Tersedia", "📚")
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Helper Convert Gambar Lokal ke Base64 ─────────────────────────────
def get_image_src(image_path):
    # Jika berupa URL internet (http/https), pakai langsung
    if str(image_path).startswith("http://") or str(image_path).startswith("https://"):
        return image_path
    
    # Jika file lokal ada di folder project, konversi ke base64
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = image_path.split('.')[-1].lower()
            mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"
            return f"data:image/{mime};base64,{encoded}"
    
    # Return string kosong jika file tidak ditemukan
    return ""

# ── Grid Publikasi ─────────────────────────────────────────────────────
i = 0
while i < len(publikasi):
    cols = st.columns(3)

    for j in range(3):
        idx = i + j
        if idx < len(publikasi):
            judul = str(publikasi.iloc[idx, 0])
            link  = str(publikasi.iloc[idx, 1])
            # Mengambil path gambar dari kolom D (indeks 3)
            cover_path = str(publikasi.iloc[idx, 3])

            # Konversi path gambar ke Base64
            cover_src = get_image_src(cover_path)

            with cols[j]:
                st.markdown(f"""
                <div class="pub-card">
                    <img src="{cover_src}" alt="{judul}"/>
                    <div class="pub-title">{judul}</div>
                    <div class="pub-link"><a href="{link}" target="_blank">⬇️ Unduh Publikasi</a></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            cols[j].write("")

    i += 3

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header(f"Unduh Publikasi {config['nmdesa']}")
    st.caption(
        f"Menu Unduh Publikasi menyediakan publikasi yang berisikan kompilasi informasi dan data di "
        f"{config['label_wilayah']} {config['nmdesa']}, "
        f"Kecamatan {config['kecamatan']}, Kabupaten Tanah Bumbu."
    )
