# -- coding: utf-8 --
from config.utils import pilih_desa_sidebar
from config.style_utils import inject_custom_css, section_header, info_banner
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import base64

st.set_page_config(
    page_title="Fasilitas Umum",
    page_icon=":cityscape:",
)

# ── Inject CSS kustom ──────────────────────────────────────────────────
inject_custom_css()

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
datadesa = pd.DataFrame(conn.read(spreadsheet=config['url_data'], ttl=0))

# ── Header Halaman ─────────────────────────────────────────────────────
t1, t2 = st.columns((0.18, 1))
t1.image('logo pemkab tanbu.png', width=100)
t2.title(config['title'])
t2.markdown(f"**Halaman Data Fasilitas Umum {config['nmdesa']}**")

st.markdown("---")

# ── Load data fasilitas ────────────────────────────────────────────────
fas23 = pd.DataFrame(conn.read(spreadsheet=config['url_fasilitas'], ttl=0)).iloc[1:98, 0:3]

# ── Fasilitas Pendidikan ───────────────────────────────────────────────
section_header("Fasilitas Pendidikan", "🎓")

sag = st.checkbox("Termasuk sekolah keagamaan", value=True)

if sag:
    tk  = int(fas23.iloc[1, 1])  + int(fas23.iloc[13, 1])
    sd  = int(fas23.iloc[2, 1])  + int(fas23.iloc[14, 1])
    smp = int(fas23.iloc[3, 1])  + int(fas23.iloc[15, 1])
    sma = int(fas23.iloc[4, 1])  + int(fas23.iloc[16, 1])
    pt  = int(fas23.iloc[5, 1])  + int(fas23.iloc[6, 1]) + int(fas23.iloc[18, 1])
else:
    tk  = int(fas23.iloc[1, 1])
    sd  = int(fas23.iloc[2, 1])
    smp = int(fas23.iloc[3, 1])
    sma = int(fas23.iloc[4, 1])
    pt  = int(fas23.iloc[5, 1]) + int(fas23.iloc[6, 1])

pd1, pd2, pd3, pd4, pd5 = st.columns(5)
pd1.metric(label='TK',     value="🚸 " + str(tk))
pd2.metric(label='SD',     value="🎒 " + str(sd))
pd3.metric(label='SMP',    value="🏫 " + str(smp))
pd4.metric(label='SMA/K',  value="📘 " + str(sma))
pd5.metric(label='PT',     value="🎓 " + str(pt))

# ── Fasilitas Kesehatan ────────────────────────────────────────────────
section_header("Fasilitas Kesehatan", "🏥")

ks1, ks2, ks3, ks4, ks5 = st.columns(5)
ks1.metric(label='Poliklinik / Balai Kes.', value="🏥 " + str(int(fas23.iloc[24, 1])))
ks2.metric(label='Apotek',                  value="💊 " + str(int(fas23.iloc[25, 1])))
ks3.metric(label='Posyandu',                value="👶 " + str(int(fas23.iloc[26, 1])))
ks4.metric(label='Prak. Dokter',            value="🧑‍⚕️ " + str(int(fas23.iloc[30, 1])))
ks5.metric(label='Prak. Bidan',             value="👩‍⚕️ " + str(int(fas23.iloc[34, 1])))

# ── Fasilitas Keagamaan ────────────────────────────────────────────────
section_header("Fasilitas Keagamaan / Peribadatan", "🕌")

ag1, ag2, ag3, ag4 = st.columns(4)
ag1.metric(label='Masjid',          value="🕌 " + str(int(fas23.iloc[86, 1])))
ag2.metric(label='Mushola',         value="🕌 " + str(int(fas23.iloc[87, 1])))
ag3.metric(label='Gereja Kristen',  value="⛪ " + str(int(fas23.iloc[88, 1])))
ag4.metric(label='Gereja Katholik', value="⛪ " + str(int(fas23.iloc[89, 1])))

ag5, ag6, ag7 = st.columns(3)
ag5.metric(label='Wihara',   value="🛕 " + str(int(fas23.iloc[90, 1])))
ag6.metric(label='Pura',     value="☸️ " + str(int(fas23.iloc[91, 1])))
ag7.metric(label='Klenteng', value="☯️ " + str(int(fas23.iloc[92, 1])))

# ── Koperasi & Perbankan ───────────────────────────────────────────────
section_header("Koperasi, Perbankan & Lembaga Keuangan", "🏦")

pb1, pb2, pb3, pb4, pb5 = st.columns(5)
pb1.metric(label='KUD',             value="🏠 " + str(int(fas23.iloc[37, 1])))
pb2.metric(label='KSP',             value="💵 " + str(int(fas23.iloc[38, 1])))
pb3.metric(label='Bumdes',          value="🏢 " + str(int(fas23.iloc[40, 1])))
pb4.metric(label='Pegadaian',       value="⚖️ " + str(int(fas23.iloc[44, 1])))
pb5.metric(label='Bank Pemerintah', value="🏦 " + str(int(fas23.iloc[45, 1])))

# ── Jasa & Perdagangan ─────────────────────────────────────────────────
section_header("Fasilitas Jasa & Perdagangan", "🛍️")

pg1, pg2, pg3 = st.columns(3)
pg1.metric(label='Toko / Kios',    value="🛍️ " + str(int(fas23.iloc[50, 1])))
pg2.metric(label='Swalayan',       value="🏪 " + str(int(fas23.iloc[51, 1])))
pg3.metric(label='Toko Kelontong', value="🧃 " + str(int(fas23.iloc[53, 1])))

# ── Akomodasi ─────────────────────────────────────────────────────────
section_header("Fasilitas Akomodasi", "🏨")

ak1, ak2, ak3 = st.columns(3)
ak1.metric(label='Rumah Kontrakan', value="🏠 " + str(int(fas23.iloc[68, 1])))
ak2.metric(label='Hotel',           value="🏨 " + str(int(fas23.iloc[70, 1])))
ak3.metric(label='Villa',           value="🏡 " + str(int(fas23.iloc[72, 1])))

# ── Olahraga ──────────────────────────────────────────────────────────
section_header("Fasilitas Olahraga", "⚽")

or1, or2, or3, or4, or5 = st.columns(5)
or1.metric(label='Lap. Sepakbola',  value="⚽ " + str(int(fas23.iloc[76, 1])))
or2.metric(label='Lap. Bulutangkis',value="🏸 " + str(int(fas23.iloc[77, 1])))
or3.metric(label='Lap. Voli',       value="🏐 " + str(int(fas23.iloc[80, 1])))
or4.metric(label='Meja Pingpong',   value="🏓 " + str(int(fas23.iloc[78, 1])))
or5.metric(label='Lap. Basket',     value="🏀 " + str(int(fas23.iloc[83, 1])))

# ── Tabel Lengkap ─────────────────────────────────────────────────────
st.markdown("---")
section_header("Data Fasilitas Selengkapnya", "📋")
st.dataframe(fas23, use_container_width=True, hide_index=True)
info_banner(f"Data tahun {int(datadesa.iloc[21, 1])}", "📅")

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header(f"Dashboard Fasilitas {config['nmdesa']}")
    st.caption(
        f"Menu fasilitas umum menyediakan data jumlah fasilitas yang dapat diakses masyarakat "
        f"di {config['label_wilayah']} {config['nmdesa']}, "
        f"Kecamatan {config['kecamatan']}, Kabupaten Tanah Bumbu."
    )
