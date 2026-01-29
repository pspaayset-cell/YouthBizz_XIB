import streamlit as st

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
if "login" not in st.session_state:
    st.session_state.login = False

if "products" not in st.session_state:
    st.session_state.products = []

if "liked" not in st.session_state:
    st.session_state.liked = []

if "saved" not in st.session_state:
    st.session_state.saved = []

# =====================
# LOGIN
# =====================
def halaman_login():
    st.title("YouthBizz 🐝")
    st.subheader("Aplikasi Promosi Wirausaha Siswa")

    with st.form("login"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        phone = st.text_input("No. Telepon")
        submit = st.form_submit_button("Masuk")

        if submit:
            if username and email and phone:
                st.session_state.login = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Semua data wajib diisi")

# =====================
# UPLOAD PRODUK
# =====================
def upload_produk():
    st.title("Upload Produk 📤")

    nama = st.text_input("Nama Produk")
    harga = st.text_input("Harga Produk")
    deskripsi = st.text_area("Deskripsi Produk")

    files = st.file_uploader(
        "Upload Foto/Video Produk (maks. 5)",
        type=["jpg", "png", "mp4"],
        accept_multiple_files=True
    )

    if files and len(files) > 5:
        st.warning("Maksimal 5 file saja")

    if st.button("Posting Produk"):
        if nama and harga and deskripsi and files and len(files) <= 5:
            st.session_state.products.append({
                "nama": nama,
                "harga": harga,
                "deskripsi": deskripsi,
                "files": files,
                "penjual": st.session_state.username
            })
            st.success("Produk berhasil diposting")
            st.rerun()
        else:
            st.error("Lengkapi semua data dengan benar")

# =====================
# HOME / FEED
# =====================
def halaman_home():
    st.title("Beranda 🏠")

    if not st.session_state.products:
        st.info("Belum ada produk yang diposting")
        return

    for i, p in enumerate(st.session_state.products):
        with st.container():
            st.subheader(p["nama"])
            st.caption(f"Penjual: {p['penjual']}")
            st.write(p["deskripsi"])
            st.write(f"💰 Harga: {p['harga']}")

            for f in p["files"]:
                if f.type.startswith("image"):
                    st.image(f)
                elif f.type.startswith("video"):
                    st.video(f)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("❤️ Suka", key=f"like{i}"):
                    if p not in st.session_state.liked:
                        st.session_state.liked.append(p)

            with col2:
                if st.button("🔖 Simpan", key=f"save{i}"):
                    if p not in st.session_state.saved:
                        st.session_state.saved.append(p)

            st.divider()

# =====================
# PROFIL
# =====================
def halaman_profil():
    st.title("Profil 👤")
    st.write(f"Username: **{st.session_state.username}**")

    st.subheader("❤️ Produk Disukai")
    if st.session_state.liked:
        for p in st.session_state.liked:
            st.write(f"- {p['nama']}")
    else:
        st.write("Belum ada")

    st.subheader("🔖 Produk Disimpan")
    if st.session_state.saved:
        for p in st.session_state.saved:
            st.write(f"- {p['nama']}")
    else:
        st.write("Belum ada")

    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.products = []
        st.session_state.liked = []
        st.session_state.saved = []
        st.rerun()

# =====================
# NAVIGASI
# =====================
def navigasi():
    menu = st.sidebar.radio(
        "Menu",
        ["Beranda", "Upload Produk", "Profil"]
    )

    if menu == "Beranda":
        halaman_home()
    elif menu == "Upload Produk":
        upload_produk()
    elif menu == "Profil":
        halaman_profil()

# =====================
# MAIN
# =====================
if st.session_state.login:
    navigasi()
else:
    halaman_login()
