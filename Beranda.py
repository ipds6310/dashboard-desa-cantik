# -- coding: utf-8 --
import streamlit as st
from config.utils import pilih_desa_sidebar
from config.style_utils import inject_custom_css, section_header, info_banner, metric_row_spacer
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import leafmap.foliumap as leafmap
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge
import base64

st.set_page_config(
    page_title="Dashboard Desa Cantik Tanah Bumbu",
    page_icon='desa_cantik.png',
    layout="wide"
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
        content: "";
        display: block;
        margin: 0 auto 20px auto;
        height: 120px; width: 120px;
        background-image: url("data:image/png;base64,{logo_base64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}
</style>
""", unsafe_allow_html=True)

config = pilih_desa_sidebar()

# ── Header Halaman ─────────────────────────────────────────────────────
t1, t2 = st.columns((0.18, 1))
t1.image(config["logo"], width=100)
t2.title(config["title"])
t2.markdown(f"**{config['subtitle']}**")
t2.markdown(
    f"Kunjungi website desa: [{config['website']}]({config['website']})"
)

st.markdown("---")

# ── Koneksi Data ───────────────────────────────────────────────────────
conn = st.connection("gsheets", type=GSheetsConnection)

url = config["url_data"]
datadesa = pd.DataFrame(conn.read(spreadsheet=url))

url2 = config["url_penduduk"]
datap2024 = pd.DataFrame(conn.read(spreadsheet=url2))
datap2024.iloc[:, 1] = pd.to_numeric(datap2024.iloc[:, 1], errors='coerce')
datap2024.iloc[:, 2] = pd.to_numeric(datap2024.iloc[:, 2], errors='coerce')

jp2024 = datap2024.iloc[0:16, 1:3].sum().sum()
pd2024laki = int(datap2024.iloc[0:16, 1:2].sum().sum())
pd2024pere = int(datap2024.iloc[0:16, 2:3].sum().sum())

# ── Rekap Kependudukan ─────────────────────────────────────────────────
st.write(f"## 📊 Rekap Data {config['label_wilayah']} {config['nmdesa']}")

col_kk, col_jp, col_lk, col_pr = st.columns(4)
col_kk.metric(label="Total KK",              value="📋 " + str(int(datap2024.iloc[18, 1])))
col_jp.metric(label="Total Penduduk (jiwa)", value="🚻 " + str(int(datap2024.iloc[19, 1])))
col_lk.metric(label="Penduduk Laki-laki",   value="🚹 " + str(int(datap2024.iloc[20, 1])))
col_pr.metric(label="Penduduk Perempuan",   value="🚺 " + str(int(datap2024.iloc[21, 1])))

metric_row_spacer()
st.write(
    f"Berdasarkan data desa, jumlah KK di {config['nmdesa']} tahun "
    f"{int(datadesa.iloc[20,1])} sebanyak **{int(datap2024.iloc[18,1])}**, "
    f"dengan total penduduk **{int(datap2024.iloc[19, 1])} jiwa** "
    f"(Laki-laki: {int(datap2024.iloc[19, 1])} | Perempuan: {int(datap2024.iloc[19, 1])})."
)

st.markdown("---")

# ── Rekap Fasilitas Pendidikan ─────────────────────────────────────────
url9 = config["url_fasilitas"]
fas23 = pd.DataFrame(conn.read(spreadsheet=url9)).iloc[1:94, 0:3]

sd  = int(fas23.iloc[2, 1]);  mi  = int(fas23.iloc[14, 1]); sdt  = sd  + mi
smp = int(fas23.iloc[3, 1]);  mts = int(fas23.iloc[15, 1]); smpt = smp + mts
sma = int(fas23.iloc[4, 1]);  ma  = int(fas23.iloc[16, 1]); smat = sma + ma

section_header("Fasilitas Pendidikan", "🎓")
f1, f2, f3 = st.columns(3)
f1.metric(label="SD / MI",      value="🎒 " + str(sdt))
f2.metric(label="SMP / MTs",   value="🏫 " + str(smpt))
f3.metric(label="SMA / MA",    value="📘 " + str(smat))

st.write(
    f"Jumlah sekolah tahun {int(datadesa.iloc[21,1])}: "
    f"SD/sederajat **{sdt}** (termasuk {mi} MI), "
    f"SMP/sederajat **{smpt}** (termasuk {mts} MTs), "
    f"SMA/SMK/sederajat **{smat}** (termasuk {ma} MA)."
)

st.markdown("---")

# ── Top 5 Komoditas Pertanian ──────────────────────────────────────────
url10 = config["url_pertanian"]
pt23 = pd.DataFrame(conn.read(spreadsheet=url10)).iloc[0:65, 0:4]
pt23.index = list(pt23.iloc[0:65, 0])
pt23 = pt23.iloc[0:65, 1:4]
pt23.iloc[:, 1] = pd.to_numeric(pt23.iloc[:, 1], errors='coerce')
top5 = pt23.sort_values(by=pt23.columns[1], ascending=False).head(5)

section_header("5 Komoditas Hasil Panen Tertinggi", "🌟")
cols = st.columns(5)
for i, (idx, row) in enumerate(top5.iterrows()):
    # Gunakan .iloc[0] dan .iloc[1] agar mengambil berdasarkan posisi kolom
    luas_panen = row.iloc[0]
    produksi = row.iloc[1]
    
    cols[i].metric(
        label=f"{idx}\n({luas_panen} Ha)",
        value=f"{produksi} Ton/Ha"
    )

st.markdown("---")

# ── Profil Wilayah ─────────────────────────────────────────────────────
st.write(f"## 🏘️ Profil {config['nmdesa']}")
st.image(config["foto"])

datadesa1 = pd.DataFrame(datadesa.iloc[0:12, 0:2])
desa = datadesa1.style.hide(axis=0).hide(axis=1)
st.markdown(desa.to_html(index=False), unsafe_allow_html=True)

# ── Peta Batas RT ──────────────────────────────────────────────────────
st.write("## 📍 Peta Batas RT")

gdf = gpd.read_file("data/final_sls_6310_202401.geojson")
gdf_kel = gdf[
    (gdf["nmkec"] == config["kecamatan"]) &
    (gdf["nmdesa"] == config["nmdesa"])
].copy()

center = gdf_kel.geometry.unary_union.centroid.coords[0][::-1]

def style_function(feature):
    return {"color": "red", "weight": 2, "fillOpacity": 0, "dashArray": "5, 5"}

m = leafmap.Map(center=center, zoom=15)
m.add_basemap("HYBRID")
m.add_geojson(
    gdf_kel.__geo_interface__,
    layer_name=f"Batas RT - {config['nmdesa']}",
    style_function=style_function,
    info_mode=None
)
for _, row in gdf_kel.iterrows():
    centroid = row.geometry.centroid
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f"""
            <div style="font-size:10px;color:white;font-weight:bold;
                        text-shadow:1px 1px 2px black;white-space:nowrap;">
                {row['nmsls']}
            </div>
        """)
    ).add_to(m)

m.to_streamlit(height=600)
info_banner(f"{config['nmdesa']}, Kecamatan {config['kecamatan']}, Kabupaten Tanah Bumbu", "📌")

# ── Tabel Lanjutan Profil ──────────────────────────────────────────────
datadesa2 = pd.DataFrame(datadesa.iloc[12:18, 0:2])
desa2 = datadesa2.style.hide(axis=0).hide(axis=1)
html_wrapped = f"""
<div style="width:100%;overflow-x:auto;border-radius:10px;border:1px solid #dee2e6;">
    <style>table{{width:100%!important;border-collapse:collapse;font-size:0.88rem;}}
    th,td{{padding:0.5rem 0.75rem;border-bottom:1px solid #e9ecef;}}
    tr:last-child td{{border-bottom:none;}}
    </style>
    {desa2.to_html()}
</div>
"""
st.write(html_wrapped, unsafe_allow_html=True)

# ── Kunjungi Kami ──────────────────────────────────────────────────────
st.markdown("---")
st.write("## 🌐 Kunjungi Kami")

ig  = "https://cdn4.iconfinder.com/data/icons/social-messaging-ui-color-shapes-2-free/128/social-instagram-new-circle-512.png"
yt  = "https://www.pngkey.com/png/full/3-32240_logo-youtube-png-transparent-background-youtube-icon.png"
web = "https://cdn-icons-png.flaticon.com/512/5339/5339181.png"
url_ig  = "https://www.instagram.com/desa_cibiruwetan"
url_yt  = "https://youtube.com/@desa_cibiruwetan"
url_web = "https://cibiruwetan.desa.id"

pd1, pd2, pd3, pd4, pd5 = st.columns((1, 1, 1, 1, 1))
pd1.write("")
pd2.markdown(f'<a href="{url_ig}"  target="_blank"><img src="{ig}"  style="width:72px;border-radius:50%;"></a>', unsafe_allow_html=True)
pd3.markdown(f'<a href="{url_yt}"  target="_blank"><img src="{yt}"  style="width:72px;border-radius:8px;"></a>', unsafe_allow_html=True)
pd4.markdown(f'<a href="{url_web}" target="_blank"><img src="{web}" style="width:72px;border-radius:8px;"></a>', unsafe_allow_html=True)
pd5.write("")

st.markdown(f"""
<div style="margin-top:1rem;font-size:0.9rem;line-height:1.9;color:#343a40;">
📧 <b>{config['email']}</b><br>
🏢 <a href="{config['maps']}" target="_blank" style="color:#4a6cf7;text-decoration:none;">
Lihat Lokasi Kantor di Maps
</a>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header(f"Dashboard {config['nmdesa']}")
    st.caption(
        f"Dashboard menyediakan data kewilayahan dan karakteristik penduduk di "
        f"{config['label_wilayah']} {config['nmdesa']}, "
        f"Kecamatan {config['kecamatan']}, Kabupaten Tanah Bumbu."
    )
