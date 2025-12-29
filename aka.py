import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt

# Fungsi Perkalian Matriks Rekursif (Divide and Conquer)
def multiply_recursive(A, B):
    n = len(A)
    if n == 1:
        return A * B

    mid = n // 2
    # Membagi matriks menjadi 4 kuadran
    a11, a12 = A[:mid, :mid], A[:mid, mid:]
    a21, a22 = A[mid:, :mid], A[mid:, mid:]
    b11, b12 = B[:mid, :mid], B[:mid, mid:]
    b21, b22 = B[mid:, :mid], B[mid:, mid:]

    # Rekursi untuk 8 perkalian sub-matriks
    c11 = multiply_recursive(a11, b11) + multiply_recursive(a12, b21)
    c12 = multiply_recursive(a11, b12) + multiply_recursive(a12, b22)
    c21 = multiply_recursive(a21, b11) + multiply_recursive(a22, b21)
    c22 = multiply_recursive(a21, b12) + multiply_recursive(a22, b22)

    # Menggabungkan kembali hasil perkalian
    top = np.hstack((c11, c12))
    bottom = np.hstack((c21, c22))
    return np.vstack((top, bottom))

# Fungsi Perkalian Iteratif
def multiply_iterative(A, B):
    n = len(A)
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

# UI Streamlit
st.set_page_config(page_title="Matrix Square Calculator", layout="wide")
st.title("Matrix Square: Recursive vs Iterative")
st.write("Aplikasi ini menghitung kuadrat matriks $A^2$ (yaitu $A \\times A$) menggunakan dua pendekatan berbeda.")

# Sidebar untuk Input
st.sidebar.header("Konfigurasi Matriks")
size = st.sidebar.selectbox("Pilih Ukuran Matriks (n x n):", [2, 4, 8, 16, 32], index=1)
st.sidebar.info("Catatan: Metode rekursif ini memerlukan ukuran matriks pangkat 2.")

# Generate Matriks Random
if 'matrix' not in st.session_state or st.sidebar.button("Generate Matriks Baru"):
    st.session_state.matrix = np.random.randint(1, 10, size=(size, size))

A = st.session_state.matrix
tab1, tab2 = st.tabs(["🎯 Kalkulator Hasil", "📈 Algoritma & Grafik Performa"])
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Matriks Input (A)")
        st.write(A)

    # Tombol Kalkulasi
    if st.button("Hitung Perbandingan"):
        # 1. Hitung Rekursif
        start_rec = time.time()
        res_rec = multiply_recursive(A, A)
        end_rec = time.time()
        time_rec = end_rec - start_rec

        # 2. Hitung Iteratif
        start_iter = time.time()
        res_iter = multiply_iterative(A, A)
        end_iter = time.time()
        time_iter = end_iter - start_iter

        # Tampilkan Hasil
        st.divider()
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.success(f"**Metode Rekursif**")
            st.metric("Waktu Eksekusi", f"{time_rec:.6f} detik")
            st.write("Hasil Matriks:")
            st.write(res_rec)

        with col_res2:
            st.info(f"**Metode Iteratif**")
            st.metric("Waktu Eksekusi", f"{time_iter:.6f} detik")
            st.write("Hasil Matriks:")
            st.write(res_iter)

        # Perbandingan singkat
        st.subheader("Analisis Singkat")
        if time_rec < time_iter:
            st.write(f"Pada ukuran {size}x{size}, metode **Rekursif** lebih cepat {time_iter/time_rec:.2f}x. Dengan selisih {time_iter-time_rec:.6f} detik.")
        else:
            st.write(f"Pada ukuran {size}x{size}, metode **Iteratif** lebih cepat {time_rec/time_iter:.2f}x. Dengan selisih {time_rec-time_iter:.6f} detik.")
with tab2:
    st.header("Perbandingan Struktur & Runtime")
    
    # Baris 1: Kode Algoritma
    col_code1, col_code2 = st.columns(2)
    with col_code1:
        st.subheader("Bentuk Iteratif")
        st.code("""
for i in range(n):
    for j in range(n):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]
        """, language="python")

    with col_code2:
        st.subheader("Bentuk Rekursif")
        st.code("""
c11 = multiply_recursive(a11, b11) + multiply_recursive(a12, b21)
c12 = multiply_recursive(a11, b12) + multiply_recursive(a12, b22)
c21 = multiply_recursive(a21, b11) + multiply_recursive(a22, b21)
c22 = multiply_recursive(a21, b12) + multiply_recursive(a22, b22)
        """, language="python")

    st.divider()
    with st.spinner("Menghasilkan grafik perbandingan..."):
        test_sizes = [2, 4, 8, 16, 32, 64]
        t_rec, t_iter = [], []
        
        for s in test_sizes:
            M = np.random.randint(1, 10, size=(s, s))
            # Rekursif
            st_r = time.time()
            multiply_recursive(M, M)
            t_rec.append(time.time() - st_r)
            # Iteratif
            st_i = time.time()
            multiply_iterative(M, M)
            t_iter.append(time.time() - st_i)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(test_sizes, t_rec, 'o-', label='Rekursif', color='red')
        ax.plot(test_sizes, t_iter, 's-', label='Iteratif', color='blue')
        ax.set_title("Efisiensi Waktu: Rekursif vs Iteratif")
        ax.set_xlabel("Ukuran Matriks (n x n)")
        ax.set_ylabel("Waktu (detik)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)