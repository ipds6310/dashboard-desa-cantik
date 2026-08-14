# config/style_utils.py
# Inject custom CSS ke semua halaman Streamlit

import streamlit as st

def inject_custom_css():
    """
    Muat dan injeksi file style.css ke halaman Streamlit.
    Panggil di awal setiap halaman setelah st.set_page_config().
    """
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Tidak error jika file tidak ditemukan


def section_header(title: str, icon: str = ""):
    """
    Tampilkan header section dengan garis bawah rapi.
    Contoh: section_header("Fasilitas Pendidikan", "🎓")
    """
    label = f"{icon} {title}".strip() if icon else title
    st.markdown(f"""
    <div style="
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #dee2e6;
    ">
        <h2 style="
            margin: 0;
            font-size: 1.15rem;
            font-weight: 700;
            color: #1a1a2e;
            letter-spacing: -0.01em;
        ">{label}</h2>
    </div>
    """, unsafe_allow_html=True)


def card_container(content_html: str, padding: str = "1rem 1.25rem"):
    """
    Bungkus konten HTML dalam card putih dengan border dan radius.
    """
    st.markdown(f"""
    <div style="
        background: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: {padding};
        margin-bottom: 1rem;
    ">
        {content_html}
    </div>
    """, unsafe_allow_html=True)


def info_banner(text: str, icon: str = "ℹ️"):
    """
    Banner keterangan di bawah tabel/chart.
    Contoh: info_banner("Data tahun 2024", "📅")
    """
    st.markdown(f"""
    <div style="
        background: #f0f4ff;
        border-left: 4px solid #4a6cf7;
        border-radius: 0 8px 8px 0;
        padding: 0.6rem 1rem;
        font-size: 0.84rem;
        color: #3a4a7a;
        margin: 0.5rem 0 1rem 0;
    ">
        {icon} {text}
    </div>
    """, unsafe_allow_html=True)


def metric_row_spacer():
    """Tambah spasi vertikal ringan antara baris metric."""
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)


def page_header(logo_path: str, title: str, subtitle: str, logo_width: int = 100):
    """
    Header halaman standar: logo kiri + judul & subtitle kanan.
    Menggantikan pola t1, t2 = st.columns(...) yang berulang.
    """
    t1, t2 = st.columns((0.18, 1))
    t1.image(logo_path, width=logo_width)
    t2.title(title)
    t2.markdown(f"**{subtitle}**")
