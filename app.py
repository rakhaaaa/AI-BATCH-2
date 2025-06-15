import streamlit as st
import time
import pandas as pd
import os

# Konfigurasi halaman
st.set_page_config(page_title="Mini Quiz Profesi", layout="centered")
st.title("🔍 Mini Quiz: Profesi yang Cocok Untukmu!")

# Mode tampilan
mode = st.sidebar.radio("🌸 Pilih Mode Tampilan", ["Light", "Dark"])

if mode == "Dark":
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #0e1117;
            color: white;
        }
        .element-container h3, .element-container p {
            color: white !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: white;
            color: black;
        }
        .element-container h3, .element-container p {
            color: black !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #f0f2f6 !important;
            color: black !important;
        }
        section[data-testid="stSidebar"] * {
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Inisialisasi session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = []
if "user_name" not in st.session_state:
    user_name_input = st.text_input("Masukkan nama kamu terlebih dahulu:")
    if user_name_input:
        st.session_state.user_name = user_name_input
        st.rerun()

# Quiz hanya bisa dimulai jika nama sudah dimasukkan
if "user_name" in st.session_state:
    user_name = st.session_state.user_name
    st.write(f"Hai, **{user_name}**! Jawab pertanyaan berikut ini ya 👇")

    QUIZ_DURATION = 60

    questions = {
        "1. Apa yang paling kamu sukai?": {
            "Programmer": "Menulis kode dan membuat aplikasi",
            "Designer": "Mendesain poster, UI, atau ilustrasi",
            "Data Scientist": "Menganalisis data dan membuat grafik"
        },
        "2. Aktivitas favorit di waktu senggang?": {
            "Programmer": "Mencoba tools atau bahasa pemrograman baru",
            "Designer": "Membuat sketsa atau desain di Canva/Figma",
            "Data Scientist": "Membaca statistik atau bermain dengan data"
        },
        "3. Mana yang paling kamu kuasai?": {
            "Programmer": "Algoritma dan logika",
            "Designer": "Desain visual dan warna",
            "Data Scientist": "Angka, data, dan interpretasinya"
        },
        "4. Software favoritmu?": {
            "Programmer": "Visual Studio Code / GitHub",
            "Designer": "Figma / Adobe Illustrator",
            "Data Scientist": "Jupyter Notebook / Excel"
        },
        "5. Apa tujuan karier impianmu?": {
            "Programmer": "Membuat aplikasi populer",
            "Designer": "Menjadi desainer brand ternama",
            "Data Scientist": "Menemukan insight dari data besar"
        }
    }

    if not st.session_state.start_time:
        st.session_state.start_time = time.time()

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = QUIZ_DURATION - elapsed

    if remaining > 0 and not st.session_state.submitted:
        st.info(f"⏳ Waktu tersisa: {remaining} detik")
        st.session_state.answers = []

        with st.form("quiz_form"):
            for question, options in questions.items():
                st.markdown(f"**{question}**")
                answer = st.radio("", list(options.values()), key=question)
                st.session_state.answers.append(answer)
            submitted = st.form_submit_button("🎯 Lihat Hasil")
            if submitted:
                st.session_state.submitted = True
                st.rerun()
    elif not st.session_state.submitted:
        st.warning("⏰ Waktu habis! Silakan mulai ulang halaman untuk mencoba lagi.")

    if st.session_state.submitted:
        scores = {"Programmer": 0, "Designer": 0, "Data Scientist": 0}
        for i, (question, options) in enumerate(questions.items()):
            answer = st.session_state.answers[i]
            for role, option_text in options.items():
                if option_text == answer:
                    scores[role] += 1

        chosen_role = max(scores, key=scores.get)

        st.subheader(f"🎯 Hasil Kuis untuk {user_name}:")
        st.image("https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif", caption="🎉 Selamat!")
        st.success(f"✨ {user_name}, kamu cocok menjadi **{chosen_role}**!")

        if chosen_role == "Programmer":
            st.image("https://cdn-icons-png.flaticon.com/512/2721/2721295.png", width=150)
            st.write("Kamu suka memecahkan masalah dan berpikir logis.")
        elif chosen_role == "Designer":
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135768.png", width=150)
            st.write("Kamu punya mata yang tajam untuk estetika dan kreativitas.")
        elif chosen_role == "Data Scientist":
            st.image("https://cdn-icons-png.flaticon.com/512/4259/4259760.png", width=150)
            st.write("Kamu hebat dalam menganalisis data dan menyusun insight.")

        hasil_data = {
            "Nama": user_name,
            "Waktu Submit": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Profesi Cocok": chosen_role,
            "Skor Programmer": scores["Programmer"],
            "Skor Designer": scores["Designer"],
            "Skor Data Scientist": scores["Data Scientist"]
        }

        hasil_file = "hasil_kuis.csv"
        if not os.path.exists(hasil_file):
            pd.DataFrame([hasil_data]).to_csv(hasil_file, index=False)
        else:
            df_lama = pd.read_csv(hasil_file)
            df_baru = pd.DataFrame([hasil_data])
            pd.concat([df_lama, df_baru], ignore_index=True).to_csv(hasil_file, index=False)

        st.success("📁 Hasil kamu telah disimpan ke file `hasil_kuis.csv`")

        if st.button("🔄 Mulai Ulang"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
