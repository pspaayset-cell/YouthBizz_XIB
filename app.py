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
if "is_login" not in st.session_state:
    st.session_state.is_login = False

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
        harga = st.text_input("Harga Produk *")
        deskripsi = st.text_area("Deskripsi Produk *")
        no_telp = st.text_input("Nomor Telepon Penjual *")
        link = st.text_input("Link Eksternal (opsional)")

        files = st.file_uploader(
            "Upload Foto / Video Produk (maks. 5)",
            type=["jpg", "png", "mp4"],
            accept_multiple_files=True
        )

        submit = st.form_submit_button("Posting Produk")

        if submit:
            if not (nama and harga and deskripsi and no_telp):
                st.error("Semua kolom bertanda * wajib diisi")
            elif not files or len(files) > 5:
                st.error("Upload 1–5 foto/video produk")
            else:
                st.session_state.products.append({
                    "nama": nama,
                    "harga": harga,
                    "deskripsi": deskripsi,
                    "no_telp": no_telp,
                    "link": link,
                    "files": files,
                    "penjual": st.session_state.username
                })
                st.success("✅ Produk berhasil di-upload")
                st.rerun()

# =====================
# SLIDE MEDIA PRODUK
# =====================
def media_slider(files):
    tabs = st.tabs([f"Media {i+1}" for i in range(len(files))])
    for tab, file in zip(tabs, files):
        with tab:
            if file.type.startswith("image"):
                st.image(file, use_container_width=True)
            elif file.type.startswith("video"):
                st.video(file)

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
            st.write(f"📞 Kontak: {p['no_telp']}")

            if p["link"]:
                st.markdown(f"🔗 [Link Produk]({p['link']})")

            media_slider(p["files"])

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
    st.write(f"Username: **{st.session_state.username}**")

    st.subheader("📦 Produk yang Saya Jual")
    jualanku = [
        p for p in st.session_state.products
        if p["penjual"] == st.session_state.username
    ]

    if jualanku:
        for p in jualanku:
            st.write(f"- {p['nama']} ({p['harga']})")
    else:
        st.write("Belum ada produk")

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
        st.session_state.clear()
        st.success("Logout berhasil")
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
if st.session_state.is_login:
    navigasi()
else:
    halaman_login()
