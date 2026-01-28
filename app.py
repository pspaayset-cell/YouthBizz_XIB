import streamlit as st

# =====================
# KONFIGURASI APLIKASI
# =====================
st.set_page_config(
    page_title="YouthBizz",
    page_icon="🐝",
    layout="centered"
)

# =====================
# DATA CONTOH (DUMMY)
# =====================
products = [
    {
        "nama": "Es Coklat Premium",
        "penjual": "YouthBizz_Store",
        "harga": "Rp5.000",
        "deskripsi": "Es coklat dengan rasa premium, cocok diminum saat cuaca panas.",
        "kontak": "https://wa.me/6281234567890"
    },
    {
        "nama": "Dimsum Ayam",
        "penjual": "DimsumKu",
        "harga": "Rp10.000",
        "deskripsi": "Dimsum ayam homemade, halal dan bergizi.",
        "kontak": "https://wa.me/6289876543210"
    },
    {
        "nama": "Seblak Pedas",
        "penjual": "SeblakNampol",
        "harga": "Rp12.000",
        "deskripsi": "Seblak dengan level pedas yang bisa disesuaikan.",
        "kontak": "https://wa.me/6281112223333"
    }
]

# =====================
# SESSION STATE
# =====================
if "login" not in st.session_state:
    st.session_state.login = False

# =====================
# HALAMAN LOGIN
# =====================
def halaman_login():
    st.title("YouthBizz 🐝")
    st.subheader("Aplikasi Promosi Wirausaha Siswa")

    with st.form("login_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        no_hp = st.text_input("No. Telepon")

        submit = st.form_submit_button("Masuk")

        if submit:
            if username and email and no_hp:
                st.session_state.login = True
                st.session_state.username = username
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Semua field wajib diisi!")

# =====================
# HALAMAN HOME
# =====================
def halaman_home():
    st.title("Beranda 🏠")
    st.write(f"Selamat datang, **{st.session_state.username}** 👋")

    st.divider()

    for p in products:
        with st.container():
            st.subheader(p["nama"])
            st.caption(f"Penjual: {p['penjual']}")
            st.write(p["deskripsi"])
            st.write(f"💰 **Harga:** {p['harga']}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("❤️ Suka", key=p["nama"] + "like")
            with col2:
                st.button("🔖 Simpan", key=p["nama"] + "save")
            with col3:
                st.link_button("📞 Hubungi", p["kontak"])

            st.divider()

# =====================
# HALAMAN PROFIL
# =====================
def halaman_profil():
    st.title("Profil 👤")
    st.write("Informasi Pengguna")

    st.write(f"**Username:** {st.session_state.username}")
    st.write("**Peran:** Siswa Wirausaha")
    st.write("**Status:** Aktif")

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

# =====================
# NAVIGASI
# =====================
def navigasi():
    menu = st.sidebar.radio(
        "Menu",
        ["Home", "Profil"]
    )

    if menu == "Home":
        halaman_home()
    elif menu == "Profil":
        halaman_profil()

# =====================
# MAIN PROGRAM
# =====================
if st.session_state.login:
    navigasi()
else:
    halaman_login()
