import streamlit as st
from config.desa_config import DESA_CONFIG

def pilih_desa_sidebar():
    # 1. Baca parameter 'desa' dari URL jika ada (contoh: ?desa=Gunung+Tinggi)
    query_params = st.query_params
    desa_dari_url = query_params.get("desa", None)
    
    # 2. Tentukan desa default (jika parameter URL sesuai dengan key di DESA_CONFIG)
    pilihan_list = list(DESA_CONFIG.keys())
    
    if desa_dari_url in DESA_CONFIG:
        default_index = pilihan_list.index(desa_dari_url)
    else:
        default_index = 0  # Default ke desa pertama ("Gunung Tinggi")

    # 3. Tampilkan Selectbox di Sidebar
    pilihan = st.sidebar.selectbox(
        "Pilih Wilayah / Desa:",
        pilihan_list,
        index=default_index
    )
    
    # 4. Update parameter URL secara otomatis saat user mengganti desa di dropdown
    st.query_params["desa"] = pilihan

    return DESA_CONFIG[pilihan]