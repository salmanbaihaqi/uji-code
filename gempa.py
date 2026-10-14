import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="Simulasi Gedung Tahan Gempa",
    page_icon="🏗️",
    layout="wide"
)

def page_earthquake():
    st.header("🏗️ Simulasi Gedung Tahan Gempa")

    st.write("""
    **Mengapa simulasi ini penting bagi Kita sebagai mahasiswa Teknik Sipil Universitas Brawijaya?**

    Saat gempa bumi terjadi, tanah akan bergoyang ke samping. Gedung bertingkat
    harus dirancang fleksibel tetapi kokoh agar goyangan tersebut tidak
    meruntuhkan struktur bangunan. Mari kita uji seberapa besar simpangan yang
    terjadi pada struktur.
    """)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Pengaturan Bangunan & Gempa")

        tinggi = st.slider(
            "Tinggi Gedung (Jumlah Lantai)",
            3, 20, 10,
            key="eq_tinggi",
            help="Makin tinggi gedung, goyangan di lantai atas akan makin terasa."
        )

        material = st.selectbox(
            "Bahan Utama Struktur",
            [
                "Beton Biasa (Tanpa Besi Tulangan)",
                "Beton Bertulang (Standar Gedung Modern)",
                "Rangka Baja & Peredam Goyangan (Teknologi Canggih)"
            ],
            key="eq_material"
        )

        magnitudo = st.slider(
            "Kekuatan Gempa (Skala Richter)",
            1.0, 10.0, 6.0,
            step=0.5,
            key="eq_magnitudo",
            help="Nilai ini kami gunakan sebagai parameter simulasi, bukan prediksi gempa nyata."
        )

        st.info("""
        💡 **Informasi Material Yang Di Pakai:**

        * **Beton Biasa** sangat rapuh saat menerima gaya tarik/goyangan ke samping.
        * **Beton Bertulang** menggunakan besi tulangan untuk membantu menahan gaya tarik.
        * **Peredam Goyangan** membantu menyerap energi getaran.
        """)

    # Parameter simulasi
    if material == "Beton Biasa (Tanpa Besi Tulangan)":
        damping = 0.02
        kekakuan = 15.0
    elif material == "Beton Bertulang (Standar Gedung Modern)":
        damping = 0.07
        kekakuan = 10.0
    else:
        damping = 0.25
        kekakuan = 5.0

    with col2:
        plot_placeholder = st.empty()
        status_placeholder = st.empty()

        def plot_building(amplitude_t, t_val=0):
            fig, ax = plt.subplots(figsize=(6, 6))

            ax.axhline(0, color="black", lw=3)

            y_coords = np.linspace(0, tinggi * 3, tinggi + 1)
            denom = y_coords[-1] if y_coords[-1] != 0 else 1.0
            x_coords = amplitude_t * (y_coords / denom) ** 2

            offset = 1.5

            ax.plot(
                x_coords - offset,
                y_coords,
                color="#FF4B4B",
                lw=4,
                marker="o",
                label="Tiang Kiri Gedung"
            )
            ax.plot(
                x_coords + offset,
                y_coords,
                color="#FF4B4B",
                lw=4,
                marker="o",
                label="Tiang Kanan Gedung"
            )

            for y_val, x_val in zip(y_coords, x_coords):
                ax.plot(
                    [x_val - offset, x_val + offset],
                    [y_val, y_val],
                    color="gray",
                    linestyle="--",
                    alpha=0.5
                )

            # Batas sumbu aku buat dinamis yan biar gedung nya tetap keliatan.
            batas_x = max(15, abs(amplitude_t) + 5)
            ax.set_xlim(-batas_x, batas_x)
            ax.set_ylim(-1, (tinggi * 3) + 5)

            ax.set_xlabel("Simpangan / Geser Goyangan (Meter)")
            ax.set_ylabel("Tinggi Gedung (Meter)")
            ax.set_title(
                f"Goyangan Gedung Saat Gempa (Waktu: {t_val:.2f} detik)"
            )
            ax.grid(True, linestyle=":", alpha=0.6)
            ax.legend()

            fig.tight_layout()
            return fig

        # Tampilan awal sebelum tombol ditekan.
        fig_init = plot_building(0.0, 0.0)
        plot_placeholder.pyplot(fig_init, clear_figure=True)
        plt.close(fig_init)

        status_placeholder.info(
            "Klik tombol di bawah buat menyimulasikan getaran gempa pada gedung."
        )

        mulai = st.button(
            "🚀 MULAI SIMULASI GEMPA",
            use_container_width=True,
            type="primary"
        )

        if mulai:
            t_steps = np.linspace(0, 8, 40)
            selesai = False

            for t in t_steps:
                # Model getaran: gelombang sinus dengan redaman eksponensial.
                amplitude = (
                    magnitudo
                    * (kekakuan / 10)
                    * np.exp(-damping * t)
                    * np.sin(2 * np.pi * 0.5 * t)
                )

                fig = plot_building(amplitude, t)
                plot_placeholder.pyplot(fig, clear_figure=True)
                plt.close(fig)

                # Pemeriksaan ambang sesuai logika kode asli.
                if (
                    abs(amplitude) > 6.0
                    and material == "Beton Biasa (Tanpa Besi Tulangan)"
                ):
                    status_placeholder.error(
                        f"🚨 BAHAYA BESAR: Simpangan melewati 6 meter pada "
                        f"detik ke-{t:.2f}! "
                        f"Simpangan = {abs(amplitude):.2f} meter."
                    )
                    selesai = True
                    break

                elif abs(amplitude) > 4.0:
                    status_placeholder.warning(
                        f"⚠️ KERUSAKAN STRUKTUR: Simpangan melewati 4 meter "
                        f"pada detik ke-{t:.2f}. "
                        f"Simpangan = {abs(amplitude):.2f} meter."
                    )
                else:
                    status_placeholder.success(
                        f"✅ GEDUNG AMAN: Struktur masih berada dalam "
                        f"batas simulasi. "
                        f"Simpangan = {abs(amplitude):.2f} meter."
                    )

                time.sleep(0.04)

            if not selesai:
                status_placeholder.success(
                    "🏁 Simulasi selesai. Pilih parameter lain untuk mencoba skenario berbeda."
                )

page_earthquake()
