# -- coding: utf-8 --
from config.utils import pilih_desa_sidebar
from config.style_utils import inject_custom_css, section_header, info_banner
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import base64

st.set_page_config(
    page_title="Kependudukan",
    page_icon=":family:",
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
t2.markdown(f"**Halaman Kependudukan {config['nmdesa']}**")

st.markdown("---")

# ── Data Penduduk 2024 ─────────────────────────────────────────────
section_header("Penduduk Berdasarkan Jenis Kelamin dan Kelompok Usia", "👥")
pilih1 = st.radio('Tahun :', [str(int(datadesa.iloc[18, 1])), str(int(datadesa.iloc[19, 1]))], horizontal=True)

url2 = config['url_penduduk']
datap2024 = pd.DataFrame(conn.read(spreadsheet=url2, ttl=0))
datap2024.iloc[:, 1] = pd.to_numeric(datap2024.iloc[:, 1], errors='coerce')
datap2024.iloc[:, 2] = pd.to_numeric(datap2024.iloc[:, 2], errors='coerce')
jp2024 = datap2024.iloc[0:16, 1:3].sum().sum()

url3 = config['url_penduduk_2023']
datap2023 = pd.DataFrame(conn.read(spreadsheet=url3, ttl=0))
datap2023.iloc[:, 1] = pd.to_numeric(datap2023.iloc[:, 1], errors='coerce')
datap2023.iloc[:, 2] = pd.to_numeric(datap2023.iloc[:, 2], errors='coerce')

# Ambil total penduduk dari baris rekap bawah (baris ke-21 / index 20)
jp2023 = datap2023.iloc[20, 1]
pd2023_laki = datap2023.iloc[21, 1]
pd2023_pere = datap2023.iloc[22, 1]

if pilih1 == str(int(datadesa.iloc[18, 1])):
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Penduduk", str(int(jp2024)) + " jiwa")
    c2.metric("Laki-laki", str(int(datap2024.iloc[0:16, 1].sum())) + " jiwa")
    c3.metric("Perempuan", str(int(datap2024.iloc[0:16, 2].sum())) + " jiwa")
    
    with st.expander("Lihat Tabel"):
        st.dataframe(datap2024.iloc[0:16, 0:3], use_container_width=True, hide_index=True)

elif pilih1 == str(int(datadesa.iloc[19, 1])):
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Penduduk", str(int(jp2023)) + " jiwa")
    c2.metric("Laki-laki", str(int(pd2023_laki)) + " jiwa")
    c3.metric("Perempuan", str(int(pd2023_pere)) + " jiwa")
    
    with st.expander("Lihat Tabel"):
        # Menampilkan data rekap per RT (baris 1 s.d 14 / index 0:14)
        st.dataframe(datap2023.iloc[0:14, 0:3], use_container_width=True, hide_index=True)

st.markdown("---")

# ── Angkatan Kerja ─────────────────────────────────────────────────────
url4 = config['url_pekerjaan']
kerja23 = pd.DataFrame(conn.read(spreadsheet=url4, ttl=0))
stkerja23 = kerja23.iloc[16:18, 0:4].copy()
kerja23 = kerja23.iloc[0:13, 0:4]

section_header(f"Angkatan Kerja Berdasarkan Status Pekerjaan Tahun {int(datadesa.iloc[20, 1])}", "💼")
stkerja23.index = list(stkerja23.iloc[0:2, 0])
stkerja23 = stkerja23.iloc[0:2, 1:4]

pilih2 = st.radio("Pilih Jenis Kelamin:", ['Laki & Perempuan', 'Laki-laki', 'Perempuan'], key="status kerja")
if pilih2 == 'Laki & Perempuan':
    datatp1 = stkerja23.iloc[0:2, 2]
elif pilih2 == 'Laki-laki':
    datatp1 = stkerja23.iloc[0:2, 0]
else:
    datatp1 = stkerja23.iloc[0:2, 1]

datatp1 = pd.melt(datatp1.reset_index(), id_vars=["index"])
charttp1 = (
    alt.Chart(datatp1, title=alt.TitleParams(pilih2, anchor='middle'))
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title="", sort="descending"),
        color=alt.Color("variable", type="nominal", title="", legend=None),
    )
)
text1 = charttp1.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(charttp1 + text1, use_container_width=True)
with st.expander("Lihat Tabel"):
    st.dataframe(stkerja23, use_container_width=True)

st.markdown("---")

# ── Jenis Pekerjaan ────────────────────────────────────────────────────
section_header(f"Penduduk Berdasarkan Jenis Pekerjaan Tahun {int(datadesa.iloc[20, 1])}", "🔧")
kerja23.index = list(kerja23.iloc[0:13, 0])
kerja23 = pd.DataFrame(kerja23.iloc[0:13, 1:4])

pilih3 = st.radio('Pilih Jenis Kelamin:', ['Laki & Perempuan', 'Laki-laki', 'Perempuan'], key="pekerjaan")
if pilih3 == 'Laki & Perempuan':
    datatp2 = kerja23.iloc[0:13, 2]
elif pilih3 == 'Laki-laki':
    datatp2 = kerja23.iloc[0:13, 0]
else:
    datatp2 = kerja23.iloc[0:13, 1]

datatp2 = pd.melt(datatp2.reset_index(), id_vars=["index"])
charttp2 = (
    alt.Chart(datatp2, title=alt.TitleParams(pilih3, anchor='middle'))
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title="", sort="descending"),
        color=alt.Color("variable", type="nominal", title="", legend=None),
    )
)
text2 = charttp2.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(charttp2 + text2, use_container_width=True)
with st.expander("Lihat Tabel"):
    st.dataframe(kerja23, use_container_width=True)

st.markdown("---")

# ── Pendidikan Tenaga Kerja ────────────────────────────────────────────
section_header(f"Pendidikan Tenaga Kerja Tahun {int(datadesa.iloc[20, 1])}", "📚")

url5 = config['url_pendidikan']
pdik23 = pd.DataFrame(conn.read(spreadsheet=url5, ttl=0)).iloc[0:6, 0:4]
pdik23.index = list(pdik23.iloc[0:6, 0])
pdik23 = pdik23.iloc[0:6, 1:4]

pilih4 = st.radio("Pilih Jenis Kelamin:", ['Laki & Perempuan', 'Laki-laki', 'Perempuan'], key="pendidikan")
if pilih4 == 'Laki & Perempuan':
    datatp3 = pdik23.iloc[0:6, 2]
elif pilih4 == 'Laki-laki':
    datatp3 = pdik23.iloc[0:6, 0]
else:
    datatp3 = pdik23.iloc[0:6, 1]

datatp3 = pd.melt(datatp3.reset_index(), id_vars=["index"])
charttp3 = (
    alt.Chart(datatp3, title=alt.TitleParams(pilih4, anchor='middle'))
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title=""),
        color=alt.Color("variable", type="nominal", title="", legend=None),
    )
)
text3 = charttp3.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(charttp3 + text3, use_container_width=True)
with st.expander("Lihat Tabel"):
    st.dataframe(pdik23, use_container_width=True)

st.markdown("---")

# ── Etnis ──────────────────────────────────────────────────────────────
section_header(f"Penduduk Menurut Etnis Tahun {int(datadesa.iloc[20, 1])}", "🌍")

url6 = config['url_etnis']
et23 = pd.DataFrame(conn.read(spreadsheet=url6, ttl=0))
et23.index = list(et23.iloc[0:21, 0])
et23 = et23.iloc[0:20, 1:4]

pilih5 = st.radio("Pilih Jenis Kelamin:", ['Laki & Perempuan', 'Laki-laki', 'Perempuan'], key="etnis")
if pilih5 == 'Laki & Perempuan':
    datatp4 = et23.iloc[0:20, 2]
elif pilih5 == 'Laki-laki':
    datatp4 = et23.iloc[0:20, 0]
else:
    datatp4 = et23.iloc[0:20, 1]

datatp4 = pd.melt(datatp4.reset_index(), id_vars=["index"])
et0 = st.checkbox("Sembunyikan data bernilai 0", value=True, key="et0")
if et0:
    datatp4 = datatp4[datatp4['value'] != 0]

charttp4 = (
    alt.Chart(datatp4, title=alt.TitleParams(pilih5, anchor='middle'))
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title=""),
        color=alt.Color("variable", type="nominal", title="", legend=None),
    )
)
text4 = charttp4.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(charttp4 + text4, use_container_width=True)
with st.expander("Lihat Tabel"):
    st.dataframe(et23, use_container_width=True)

st.markdown("---")

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header(f"Dashboard Kependudukan {config['nmdesa']}")
    st.caption(
        f"Menu kependudukan menyediakan data jumlah penduduk berdasarkan usia, jenis kelamin, "
        f"tingkat pendidikan dan status pekerjaan angkatan kerja di "
        f"{config['label_wilayah']} {config['nmdesa']}, "
        f"Kecamatan {config['kecamatan']}, Kabupaten Tanah Bumbu."
    )
