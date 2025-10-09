# -- coding: utf-8 --
"""
Created on Wed Oct  4 11:54:31 2023

@author: Asus
"""

import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import leafmap.foliumap as leafmap
from shapely.geometry import LineString, MultiLineString
from shapely.ops import linemerge


st.set_page_config(
    page_title="Dashboard Data Kelurahan Gunung Tinggi",
    page_icon="🏠",
)

#this is the header


t1, t2 = st.columns((0.25,1))

t1.image('logo pemkab tanbu.png', width=100)
t2.title("Kelurahan Cantik Gunung Tinggi")
t2.markdown("**Halaman Utama Dashboard Data Kelurahan Gunung Tinggi**")
t2.markdown(
    "Jika ingin mengakses website desa bisa klik pada link berikut: "
    "[https://gunungtinggi.website.desa.id/](https://gunungtinggi.website.desa.id/)"
)


#this is content
 #st.image('https://www.desawisata-cibiruwetan.com/wp-content/uploads/2023/01/branding-cibiru-wetan-WISATA-1-800x197.png')
### Import Data Lengkap
url = 'https://docs.google.com/spreadsheets/d/1n6RkwCmYWQm4Uc21GtgZ0Tc6BracOxevkqgtEq8lMoY/edit?usp=sharing'
conn  = st.connection("gsheets", type=GSheetsConnection)
datadesa = conn.read(spreadsheet=url)
datadesa = pd.DataFrame(datadesa)                       #convert ke panda df
st.write("# Rekap Data Kelurahan Gunung Tinggi")

url2='https://docs.google.com/spreadsheets/d/1Lq_4bictqMTRzKmFAQ5K4i6Tb_W9nTC07bbz-tM_HTU/edit?usp=sharing'
datap2024 = conn.read(spreadsheet=url2)
datap2024 = pd.DataFrame(datap2024)                       #convert ke panda df

# Konversi ke numerik (otomatis ubah teks menjadi NaN jika tak bisa dikonversi)
datap2024.iloc[:, 1] = pd.to_numeric(datap2024.iloc[:, 1], errors='coerce')
datap2024.iloc[:, 2] = pd.to_numeric(datap2024.iloc[:, 2], errors='coerce')

# Hitung total
jp2024 = datap2024.iloc[0:16, 1:3].sum().sum()


datapiramida = datap2024.iloc[0:16,1:3]
jk = list(["Laki-laki","Perempuan"])
datapiramida.iloc[0:16,0]=-datapiramida.iloc[0:16,0]
datapiramida.index = list(datap2024.iloc[0:16,0])
datapiramida.columns = jk

pd2024laki = int(datap2024.iloc[0:16,1:2].sum().sum())
pd2024pere = int(datap2024.iloc[0:16,2:3].sum().sum())
lakipere2024 = pd.DataFrame({"laki":[pd2024laki],"perempuan":[pd2024pere]})
lakipere2024.columns = list(["Laki-laki","Perempuan"])

m1, m2, m3 = st.columns((1,1,1))
m1.write("")
m2.metric(label = 'Total KK',value = "📋"+str(int(datap2024.iloc[18,1])))
m3.write("")

m1, m2, m3 = st.columns((1,1,1))
m1.write("")
m2.metric(label ='Total Penduduk (jiwa)',value = "🚻"+str(int(jp2024)))
m3.write("")

m1, m2, m3, m4 = st.columns((1,1,1,1))
m1.write("")
m2.metric(label ='Penduduk Laki-laki',value = "🚹"+str(int(pd2024laki)))
m3.metric(label = 'Penduduk Perempuan',value = "🚺"+str(int(pd2024pere)))
m4.write("")
st.write("Berdasarkan data Kementerian Dalam Negeri (Kemendagri), jumlah kartu keluarga (KK) yang terdaftar di Kelurahan Gunung Tinggi pada tahun ",str(int(datadesa.iloc[20,1]))," sebanyak ",str(int(datap2024.iloc[18,1])),". Jumlah penduduk pada periode tersebut sebanyak ",str(int(jp2024))," jiwa dengan penduduk laki-laki sebanyak ",str(int(pd2024laki))," jiwa dan penduduk perempuan sebanyak",str(pd2024pere)," jiwa.")

url9='https://docs.google.com/spreadsheets/d/1KFo2hs7pTIqJ555BCx-tpn2foaFpV3i7K9PcKVbFR7A/edit?usp=sharing'
fas23 = conn.read(spreadsheet=url9)
fas23 = pd.DataFrame(fas23)                       #convert ke panda df
fas23 = fas23.iloc[1:94,0:3]
sd=int(fas23.iloc[2,1]);mi=int(fas23.iloc[14,1]);sdt=int(fas23.iloc[2,1]+fas23.iloc[14,1])
smp=int(fas23.iloc[3,1]);mts=int(fas23.iloc[15,1]);smpt=int(fas23.iloc[3,1]+fas23.iloc[15,1])
sma=int(fas23.iloc[4,1]);ma=int(fas23.iloc[16,1]);smat=int(fas23.iloc[4,1]+fas23.iloc[16,1])

pd1,pd2,pd3,pd4,pd5 = st.columns((1,1,1,1,1))
pd1.write("")
pd2.metric(label='SD',value="🎒"+str(sdt))
pd3.metric(label='SMP',value="🏫"+str(smpt))
pd4.metric(label='SMA/K',value="📘"+str(smat))
pd5.write("")
st.write("Berdasarkan data Kementerian Pendidikan dan Budaya (Kemendikbud) dan Kementerian Agama, jumlah sekolah yang terdaftar di Kelurahan Gunung Tinggi pada tahun ",str(int(datadesa.iloc[21,1])),", antara lain SD/sederajat sebanyak ",str(sdt)," (termasuk ",str(mi)," Madrasah Ibtidaiyah/MI), SMP/sederajat sebanyak ",str(smpt)," (termasuk ",str(mts)," Madrasah Tsanawiyah/MTs), dan SMA/SMK/sederajat sebanyak ",str(smat)," (termasuk ",str(ma)," Madrasah Aliyah/MA).")

url10='https://docs.google.com/spreadsheets/d/1n4OhTNKWiVf6zRYJgzcHU3hXcwTG0CCmEBQFML49ENc/edit?usp=sharing'
conn  = st.connection("gsheets", type=GSheetsConnection)
pt23 = conn.read(spreadsheet=url10)
pt23 = pd.DataFrame(pt23)                       #convert ke panda df
pt23 = pt23.iloc[0:65,0:4]
pt23.index = list(pt23.iloc[0:65,0])
pt23 = pt23.iloc[0:65,1:4]
# Pastikan kolom "Hasil Panen (Ton per Ha)" menjadi numeric
pt23.iloc[:, 1] = pd.to_numeric(pt23.iloc[:, 1], errors='coerce')

# Ambil 5 komoditas teratas berdasarkan hasil panen per hektar
top5 = pt23.sort_values(by=pt23.columns[1], ascending=False).head(5)

# Tampilkan di Streamlit
st.subheader("🌟 5 Komoditas dengan Hasil Panen Tertinggi (Ton/Ha)")

for idx, row in top5.iterrows():
    st.metric(
        label=f"{idx} ({row[0]} Ha)",
        value=f"{row[1]} Ton/Ha",
        delta=f"{row[2]}" if len(row) > 2 else None
    )

# Narasi tambahan
top_list = ", ".join([f"**{idx}** ({row[1]} Ton/Ha)" for idx, row in top5.iterrows()])
st.write(f"Komoditas dengan produktivitas tertinggi adalah {top_list}.")

import pydeck as pdk
st.write("# Profil Kelurahan Gunung Tinggi")
with st.sidebar:
    st.image('desa_cantik.png',width=100)
    st.header("Dashboard Kelurahan Gunung Tinggi")
    st.caption("""Dashboard ini menyediakan data kewilayahan dan karakteristik penduduk di Kelurahan Gunung Tinggi, Kecamatan Batulicin, Kabupaten Tanah Bumbu.""")


datadesa1 = pd.DataFrame(datadesa.iloc[0:12,0:2])                       #convert ke panda df
desa = datadesa1.style.hide(axis=0).hide(axis=1)                     #menyembunyikan nomor tabel dan header                                   #menyembunyikan header
st.image('kelgunting.jpeg')
# st.write(desa.to_html(),unsafe_allow_html=True,use_container_width=True)         #menyembunyikan nomor tabel dari .to_html sampe True)
st.markdown(desa.to_html(index=False), unsafe_allow_html=True)


st.title("📍 Peta Batas RT di Kabupaten Tanah Bumbu")

# Load GeoData
gdf = gpd.read_file("data/final_sls_6310_202401.geojson")

# # --- Dropdown Kecamatan ---
# kecamatan_list = sorted(gdf["nmkec"].unique().tolist())
# default_kec = "BATU LICIN" if "BATU LICIN" in kecamatan_list else kecamatan_list[0]
# kecamatan_terpilih = st.selectbox("Pilih Kecamatan", kecamatan_list, index=kecamatan_list.index(default_kec))

# # --- Dropdown Kelurahan yang sesuai Kecamatan ---
# kelurahan_list = sorted(gdf[gdf["nmkec"] == kecamatan_terpilih]["nmdesa"].unique().tolist())
# default_kel = "GUNUNG TINGGI" if "GUNUNG TINGGI" in kelurahan_list else kelurahan_list[0]
# kelurahan_terpilih = st.selectbox("Pilih Kelurahan/Desa", kelurahan_list, index=kelurahan_list.index(default_kel))


# Filter berdasarkan kecamatan & kelurahan
gdf_kel = gdf[(gdf["nmkec"] == "BATU LICIN") & (gdf["nmdesa"] == "GUNUNG TINGGI")].copy()


# Titik tengah kelurahan
center = gdf_kel.geometry.unary_union.centroid.coords[0][::-1]  # (lat, lon)

# Style garis batas merah putus-putus (tanpa isi)
def style_function(feature):
    return {
        "color": "red",
        "weight": 2,
        "fillOpacity": 0,
        "dashArray": "5, 5"
    }

# Buat peta dengan basemap satelit
m = leafmap.Map(center=center, zoom=15)
m.add_basemap("HYBRID")

# Tambahkan GeoJSON ke peta tanpa popup/tooltip
m.add_geojson(
    gdf_kel.__geo_interface__,
    layer_name=f"Batas RT - GUNUNG TINGGI",
    style_function=style_function,
    info_mode=None  # Tidak ada popup atau hover info
)

# Tambahkan label RT di tengah tiap polygon
for _, row in gdf_kel.iterrows():
    centroid = row.geometry.centroid
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f"""
            <div style="font-size:10px; color:white; font-weight:bold; text-shadow:1px 1px 2px black;white-space:nowrap;">
                {row['nmsls']}
            </div>
        """)
    ).add_to(m)

# Tampilkan peta di Streamlit
m.to_streamlit(height=600)

# ------------------------------------------------------------------------------------------------------------------------

# st.title("🗺️ Peta Wilayah SLS dan Blok Sensus")

# # Load data
# gdf_sls = gpd.read_file("data/final_sls_6310_202401.geojson")
# gdf_bs = gpd.read_file("data/final_bs_202416310.geojson")

# # --- Dropdown Kecamatan ---
# kecamatan_list2 = sorted(gdf_sls["nmkec"].unique().tolist())
# default_kec2 = "BATU LICIN" if "BATU LICIN" in kecamatan_list2 else kecamatan_list2[0]
# kecamatan_terpilih2 = st.selectbox(
#     "Pilih Kecamatan",
#     kecamatan_list2,
#     index=kecamatan_list2.index(default_kec2),
#     key="kecamatan_select"  # <--- Tambahkan key unik
# )

# # --- Dropdown Kelurahan yang sesuai Kecamatan ---
# kelurahan_list2 = sorted(gdf_sls[gdf_sls["nmkec"] == kecamatan_terpilih2]["nmdesa"].unique().tolist())

# # Tambahkan opsi "Semua Kelurahan"
# kelurahan_list2.insert(0, "Semua Kelurahan")

# default_kel2 = "GUNUNG TINGGI" if "GUNUNG TINGGI" in kelurahan_list2 else kelurahan_list2[0]

# kelurahan_terpilih2 = st.selectbox(
#     "Pilih Kelurahan/Desa",
#     kelurahan_list2,
#     index=kelurahan_list2.index(default_kel2),
#     key="kelurahan_select"
# )

# # --- Filter data sesuai pilihan ---
# if kelurahan_terpilih2 == "Semua Kelurahan":
#     filtered_rt = gdf_sls[gdf_sls["nmkec"] == kecamatan_terpilih2]
#     filtered_jalan = gdf_bs[gdf_bs["nmkec"] == kecamatan_terpilih2]
# else:
#     filtered_rt = gdf_sls[
#         (gdf_sls["nmkec"] == kecamatan_terpilih2) &
#         (gdf_sls["nmdesa"] == kelurahan_terpilih2)
#     ]
#     filtered_jalan = gdf_bs[
#         (gdf_bs["nmkec"] == kecamatan_terpilih2) &
#         (gdf_bs["nmdesa"] == kelurahan_terpilih2)
#     ]


# # Titik tengah peta
# center = filtered_rt.geometry.unary_union.centroid.coords[0][::-1] if not filtered_rt.empty else [0, 0]

# # Buat peta
# m = leafmap.Map(center=center, zoom=15)
# m.add_basemap("HYBRID")

# # --- Tambahkan Layer RT ---
# def style_rt(feature):
#     return {
#         "color": "red",
#         "weight": 2,
#         "fillOpacity": 0,
#         "dashArray": "5,5"
#     }

# folium.GeoJson(
#     data=filtered_rt.__geo_interface__,
#     name="Batas SLS",
#     style_function=style_rt,
# ).add_to(m)

# # Label RT (nmsls)
# for _, row in filtered_rt.iterrows():
#     centroid = row.geometry.centroid
#     if not centroid.is_empty:
#         folium.Marker(
#             location=[centroid.y, centroid.x],
#             icon=folium.DivIcon(html=f"""
#                 <div style="font-size:10px;color:white;white-space:nowrap;">
#                     {row['nmdesa']}<br>{row['nmsls']}
#                 </div>
#             """)
#         ).add_to(m)

# # --- Tambahkan Layer Jalan ---
# def style_jalan(feature):
#     return {
#         "color": "yellow",
#         "weight": 2,
#         "fillOpacity": 0,
#         "dashArray": "3",
#     }

# folium.GeoJson(
#     data=filtered_jalan.__geo_interface__,
#     name="Batas Blok Sensus",
#     style_function=style_jalan,
#     tooltip=folium.GeoJsonTooltip(fields=["kdbs"], aliases=["BS"])
# ).add_to(m)

# # Label Jalan (kdbs)
# for _, row in filtered_jalan.iterrows():
#     geom = row.geometry
#     if geom.is_empty:
#         continue
#     if geom.geom_type == "LineString":
#         point = geom.interpolate(0.5, normalized=True)
#     elif geom.geom_type == "MultiLineString":
#         # Gabungkan semua garis jadi satu
#         merged = linemerge(geom)
#         point = merged.interpolate(0.5, normalized=True) if merged.length > 0 else merged.centroid
#     else:
#         continue

#     if not point.is_empty:
#         folium.Marker(
#             location=[point.y, point.x],
#             icon=folium.DivIcon(html=f"""
#                 <div style="font-size:10px;color:white;white-space:nowrap;">
#                     {row['nmdesa']}<br>{row['kdbs']}
#                 </div>
#             """)
#         ).add_to(m)


# # Tampilkan di Streamlit
# m.to_streamlit(height=650)

# # Pastikan gdf_sls memiliki kolom 'nmkec' dan 'nmdesa'
# desa_centroids = filtered_rt.dissolve(by=["nmkec", "nmdesa"]).reset_index()

# # Hitung centroid
# desa_centroids["latitude"] = desa_centroids.centroid.y
# desa_centroids["longitude"] = desa_centroids.centroid.x

# # Pilih kolom untuk ditampilkan
# df_koordinat = desa_centroids[["nmkec", "nmdesa", "latitude", "longitude"]]

# st.subheader("📍 Koordinat Titik Tengah (Centroid) per Desa")
# st.dataframe(df_koordinat.style.format({"latitude": "{:.6f}", "longitude": "{:.6f}"}))



st.write("Kelurahan Gunung Tinggi, Kecamatan Batulicin, Kabupaten Tanah Bumbu")

datadesa2 = pd.DataFrame(datadesa.iloc[12:18,0:2])                       #convert ke panda df
desa2 = datadesa2.style.hide(axis=0).hide(axis=1)                        #menyembunyikan header dan nomor tabel
# Render HTML dengan lebar penuh
html_table = desa2.to_html()
html_wrapped = f"""
<div style="width: 100%;">
    <style>table {{ width: 100% !important; }}</style>
    {html_table}
</div>
"""

st.write(html_wrapped, unsafe_allow_html=True)

st.write("# Kunjungi Kami")
ig = "https://cdn4.iconfinder.com/data/icons/social-messaging-ui-color-shapes-2-free/128/social-instagram-new-circle-512.png"
yt = 'https://www.pngkey.com/png/full/3-32240_logo-youtube-png-transparent-background-youtube-icon.png'
web = 'https://cdn-icons-png.flaticon.com/512/5339/5339181.png'
url_ig = 'https://www.instagram.com/desa_cibiruwetan?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=='
url_yt = 'https://youtube.com/@desa_cibiruwetan?si=js2kX36jVxCMI64F'
url_web = 'https://cibiruwetan.desa.id'
#st.write("[instagram](%s)" % url_ig," | [youtube](%s)" % url_yt," | [website](%s)" % url_web)
pd1,pd2,pd3,pd4,pd5 = st.columns((1,1,1,1,1))

# Menggunakan HTML untuk membuat gambar yang dapat diklik
pd1.write('')
pd2.markdown(f'<a href="{url_ig}" target="_blank"><img src="{ig}" alt="Clickable Image" style="width:80px;"></a>', unsafe_allow_html=True)
pd3.markdown(f'<a href="{url_yt}" target="_blank"><img src="{yt}" alt="Clickable Image" style="width:80px;"></a>', unsafe_allow_html=True)
pd4.markdown(f'<a href="{url_web}" target="_blank"><img src="{web}" alt="Clickable Image" style="width:80px;"></a>', unsafe_allow_html=True)
pd5.write('')
st.write("**📧: gunungtinggikel@gmail.com**")
urlkantor = 'https://maps.app.goo.gl/ovawuniWpb4gkhQs9'
st.write("🏢: **[Jl. Dharma Praja, Pd. Butun, Kec. Batulicin, Kabupaten Tanah Bumbu, Kalimantan Selatan 72273, Kode Pos 72211](%s)**"%urlkantor)


