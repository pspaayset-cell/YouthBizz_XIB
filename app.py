import streamlit as st
import json
import os

# =====================
# KONFIGURASI
# =====================
st.set_page_config(
    page_title="YouthBizz",
    page_icon="🐝",
    layout="centered"
)

# =====================
# SESSION STATE
# =====================
DATA_FILE = "data.json"

def load_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_products(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if "is_login" not in st.session_state:
    st.session_state.is_login = False

if "products" not in st.session_state:
    st.session_state.products = load_products()

if "liked" not in st.session_state:
    st.session_state.liked = []

if "saved" not in st.session_state:
    st.session_state.saved = []

# =====================
# FUNGSI FORMAT RUPIAH
# =====================
def rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# =====================
# LOGIN
# =====================
def halaman_login():
    st.title("YouthBizz 🐝")
    st.subheader("Aplikasi Promosi Wirausaha Siswa")

    with st.form("login_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        phone = st.text_input("No. Telepon")
        submit = st.form_submit_button("Masuk")

        if submit:
            if username and email and phone:
                st.session_state.is_login = True
                st.session_state.username = username
                st.success("Login berhasil 🎉")
                st.rerun()
            else:
                st.error("Semua data wajib diisi")

# =====================
# UPLOAD PRODUK
# =====================
def upload_produk():
    st.title("Upload Produk 📤")

    with st.form("upload_form"):
        nama = st.text_input("Nama Produk *")
        harga = st.number_input("Harga Produk (Rp) *", min_value=0, step=1000)
        deskripsi = st.text_area("Deskripsi Produk *")
        no_telp = st.text_input("Nomor Telepon Penjual *")
        link = st.text_input("Link Produk (opsional)")

        files = st.file_uploader(
            "Upload Foto / Video Produk (maks. 5)",
            type=["jpg", "png", "mp4"],
            accept_multiple_files=True
        )

        submit = st.form_submit_button("Posting Produk")

        if submit:
            if not (nama and deskripsi and no_telp):
                st.error("Semua kolom bertanda * wajib diisi")

            elif not files or len(files) > 5:
                st.error("Upload 1–5 foto/video")

            else:
                produk_baru = {
                    "nama": nama,
                    "harga": harga,
                    "deskripsi": deskripsi,
                    "no_telp": no_telp,
                    "link": link,
                    "penjual": st.session_state.username
                }

                st.session_state.products.append(produk_baru)
                save_products(st.session_state.products)

                st.success("✅ Produk berhasil di-upload")
                st.rerun()

# =====================
# SLIDE MEDIA
# =====================
def media_slider(files):
    tabs = st.tabs([f"Media {i+1}" for i in range(len(files))])
    for tab, file in zip(tabs, files):
        with tab:
            if file.type.startswith("image"):
                st.image(file, use_container_width=True)
            else:
                st.video(file)

# =====================
# BERANDA + SEARCH
# =====================
def halaman_home():
    st.title("Beranda 🏠")

    keyword = st.text_input("🔍 Cari produk")

    produk = st.session_state.products
    if keyword:
        produk = [
            p for p in produk
            if keyword.lower() in p["nama"].lower()
        ]

    if not produk:
        st.info("Produk tidak ditemukan")
        return

    for i, p in enumerate(produk):
        st.subheader(p["nama"])
        st.caption(f"Penjual: {p['penjual']}")
        st.write(p["deskripsi"])
        st.write(f"💰 Harga: Rp {p['harga']:,.0f}".replace(",", "."))
        st.write(f"📞 Kontak: {p['no_telp']}")

        if p.get("link"):
            st.markdown(f"🔗 [Link Produk]({p['link']})")

        # Media hanya dari session (AMAN)
        if "media" in st.session_state and i in st.session_state.media:
            media_slider(st.session_state.media[i])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("❤️ Suka", key=f"like_{i}"):
                if p not in st.session_state.liked:
                    st.session_state.liked.append(p)
                    st.success("Produk ditambahkan ke Disukai")

        with col2:
            if st.button("🔖 Simpan", key=f"save_{i}"):
                if p not in st.session_state.saved:
                    st.session_state.saved.append(p)
                    st.success("Produk berhasil disimpan")

        st.divider()

# =====================
# PROFIL
# =====================
def halaman_profil():
    st.title("Profil 👤")
    st.write(f"👤 **{st.session_state.username}**")

    st.subheader("📦 Produk yang Saya Jual")
    jualanku = [p for p in st.session_state.products if p["penjual"] == st.session_state.username]
    for p in jualanku:
        st.write(f"- {p['nama']} ({rupiah(p['harga'])})")

    st.subheader("❤️ Produk Disukai")
    for p in st.session_state.liked:
        st.write(f"- {p['nama']}")

    st.subheader("🔖 Produk Disimpan")
    for p in st.session_state.saved:
        st.write(f"- {p['nama']}")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# =====================
# NAVIGASI
# =====================
def navigasi():
    menu = st.sidebar.radio("Menu", ["Beranda", "Upload Produk", "Profil"])
    if menu == "Beranda":
        halaman_home()
    elif menu == "Upload Produk":
        upload_produk()
    else:
        halaman_profil()

# =====================
# MAIN
# =====================
if st.session_state.is_login:
    navigasi()
else:
    halaman_login()
