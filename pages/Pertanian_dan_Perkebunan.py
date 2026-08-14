# -- coding: utf-8 --
from config.utils import pilih_desa_sidebar
from config.style_utils import inject_custom_css, section_header, info_banner
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import base64

st.set_page_config(
    page_title="Pertanian dan Perkebunan",
    page_icon="🌴",
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
datadesa = pd.DataFrame(conn.read(spreadsheet=config['url_data']))

# ── Header Halaman ─────────────────────────────────────────────────────
t1, t2 = st.columns((0.18, 1))
t1.image('logo pemkab tanbu.png', width=100)
t2.title(config['title'])
t2.markdown(f"**Halaman Pertanian dan Perkebunan {config['nmdesa']}**")

st.markdown("---")

# ── Load Data ──────────────────────────────────────────────────────────
url10 = config['url_pertanian']
pt23_raw = pd.DataFrame(conn.read(spreadsheet=url10))

lahan23 = pt23_raw.iloc[68:73, 0:2].copy()
lahan23.index = list(lahan23.iloc[0:3, 0])
lahan23 = lahan23.iloc[0:3, 1:2]

pt23 = pt23_raw.iloc[0:65, 0:4].copy()
pt23.index = list(pt23.iloc[0:65, 0])
pt23 = pt23.iloc[0:65, 1:4]

import altair as alt

# ── Luas Lahan ─────────────────────────────────────────────────────────
section_header("Luas Lahan Berdasarkan Jenis Produksi", "🗺️")

data = pd.melt(lahan23.reset_index(), id_vars=["index"])
chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title="", sort="descending"),
        color=alt.Color("variable", type="nominal", title=""),
    )
)
text = chart.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(chart + text, use_container_width=True)

datapie = data.copy()
datapie['value'] = datapie['value'].div(float(data['value'].sum().sum() / 100)).round(2)
piechart = (
    alt.Chart(datapie, title=alt.TitleParams('Persentase (%) Luas Lahan Berdasarkan Jenis Produksi', anchor='middle'))
    .mark_arc(outerRadius=120)
    .encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="index", type="nominal"),
    )
)
textpie = piechart.mark_text(radius=140, size=20).encode(text="value")
if st.checkbox("Tampilkan grafik dalam persentase (%)"):
    st.altair_chart(piechart + textpie, use_container_width=True)

st.markdown("---")

# ── Tanaman Pangan ─────────────────────────────────────────────────────
section_header("Tanaman Pangan Berdasarkan Komoditas", "🌾")

pilih1 = st.radio("Tampilkan:", ['Luas Lahan (Ha)', 'Hasil Panen (Ton/Ha)'], key="pangan")
datatp1 = pt23.iloc[0:31, 0] if pilih1 == 'Luas Lahan (Ha)' else pt23.iloc[0:31, 1]
datatp1 = pd.melt(datatp1.reset_index(), id_vars=["index"])

if st.checkbox("Sembunyikan data bernilai 0", value=True, key="pangan0"):
    datatp1 = datatp1[datatp1['value'] != 0]

charttp1 = (
    alt.Chart(datatp1, title=alt.TitleParams(pilih1, anchor='middle'))
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title="", sort="descending"),
        color=alt.Color("variable", type="nominal", title="", legend=None),
    )
)
text1 = charttp1.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(charttp1 + text1, use_container_width=True)

st.markdown("---")

# ── Tanaman Buah ───────────────────────────────────────────────────────
section_header("Tanaman Buah-buahan Berdasarkan Komoditas", "🍌")

pilih2 = st.radio("Tampilkan:", ['Luas Lahan (Ha)', 'Hasil Panen (Ton/Ha)'], key="buah")
datatp2 = pt23.iloc[31:58, 0] if pilih2 == 'Luas Lahan (Ha)' else pt23.iloc[31:58, 1]
datatp2 = pd.melt(datatp2.reset_index(), id_vars=["index"])

if st.checkbox("Sembunyikan data bernilai 0", value=True, key="buah0"):
    datatp2 = datatp2[datatp2['value'] != 0]

charttp2 = (
    alt.Chart(datatp2, title=alt.TitleParams(pilih2, anchor='middle'))
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title="", sort="descending"),
        color=alt.Color("variable", type="nominal", title="", legend=None),
    )
)
text2 = charttp2.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(charttp2 + text2, use_container_width=True)

st.markdown("---")

# ── Perkebunan ─────────────────────────────────────────────────────────
section_header("Perkebunan Berdasarkan Komoditas", "🌴")

pilih3 = st.radio("Tampilkan:", ['Luas Lahan (Ha)', 'Hasil Panen (Ton/Ha)'], key="kebun")
datatp3 = pt23.iloc[58:65, 0] if pilih3 == 'Luas Lahan (Ha)' else pt23.iloc[58:65, 1]
datatp3 = pd.melt(datatp3.reset_index(), id_vars=["index"])

if st.checkbox("Sembunyikan data bernilai 0", value=True, key="kebun0"):
    datatp3 = datatp3[datatp3['value'] != 0]

charttp3 = (
    alt.Chart(datatp3, title=alt.TitleParams(pilih3, anchor='middle'))
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title=""),
        y=alt.Y("index", type="nominal", title="", sort="descending"),
        color=alt.Color("variable", type="nominal", title="", legend=None),
    )
)
text3 = charttp3.mark_text(align='left', baseline='middle', dx=3).encode(text='value')
st.altair_chart(charttp3 + text3, use_container_width=True)

st.markdown("---")

# ── Tabel Lengkap ──────────────────────────────────────────────────────
section_header("Tabel Luas Lahan & Hasil Panen Selengkapnya", "📋")
st.dataframe(pt23, use_container_width=True)
info_banner(f"Data tahun {int(datadesa.iloc[22, 1])}", "📅")

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header(f"Dashboard Pertanian {config['nmdesa']}")
    st.caption(
        f"Menu pertanian dan perkebunan menyediakan data luas lahan serta hasil panen "
        f"dari berbagai komoditas tanaman pangan, buah-buahan, dan hasil perkebunan di "
        f"{config['label_wilayah']} {config['nmdesa']}, "
        f"Kecamatan {config['kecamatan']}, Kabupaten Tanah Bumbu."
    )
