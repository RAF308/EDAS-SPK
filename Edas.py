import streamlit as st
import numpy as np
import pandas as pd
import pyDecision
from pyDecision.algorithm import edas_method

st.markdown("<h2 style='text-align: center; color: white;'>Sistem Pendukung Keputusan Menggunakan Evaluation Based on Distance from Average Solution (EDAS)</h2>", unsafe_allow_html=True)

# Define array variable
alt_name_value          = np.array([])    
alt_jarak_value         = np.array([])
alt_waktu_value         = np.array([])
alt_biaya_value         = np.array([])
alt_fasilitas_value     = np.array([])
alt_pengunjung_value    = np.array([])

intensitas_pengunjung   = {'Sangat Sepi': 1, 'Sepi': 2, 'Cukup Ramai': 3, 'Ramai': 4, 'Ramai Pisan': 5}
fasilitas_tempat        = {'Sangat Buruk': 1, 'Buruk': 2, 'Cukup Baik': 3, 'Baik': 4, 'Sangat Baik': 5}

alt_value = st.number_input('Input Jumlah Alternatif :', min_value=0, value=0, step=1)

# Inisialisasi list alt_name_value dengan panjang yang sesuai
alt_name_value = ["" for _ in range(int(alt_value))]

for i in range(int(alt_value)):
    alt_name_value[i] = st.text_input(f'Tempat Wisata ke {i+1}')


if alt_value != 0:
    st.title('Jarak Tempuh (Km) - C1')
    for i in range(int(alt_value)):
            
            jarak_tempuh = st.number_input(f"Tempat Wisata ke {i + 1}: {alt_name_value[i]}", min_value=0, value=0, step=1)

            if 0 > jarak_tempuh <= 100:
                c1 = 1
                alt_jarak_value = np.append(alt_jarak_value, c1)
            elif 100 > jarak_tempuh <= 300:
                c1 = 2
                alt_jarak_value = np.append(alt_jarak_value, c1)
            elif 300 > jarak_tempuh <= 500:
                c1 = 3
                alt_jarak_value = np.append(alt_jarak_value, c1)
            elif 500 > jarak_tempuh <= 700:
                c1 = 4
                alt_jarak_value = np.append(alt_jarak_value, c1)
            else:
                c1 = 5
                alt_jarak_value = np.append(alt_jarak_value, c1)

    st.title('Waktu Tempuh (Jam) - C2')
    for i in range(int(alt_value)):
        
        waktu = st.number_input(f"Tempat Wisata ke {i + 1}: {alt_name_value[i]}", min_value=2, value=2, step=1)

        if waktu <2:
            c2 = 1
            alt_waktu_value = np.append(alt_waktu_value, c2)
        elif 2 >= waktu < 4:
            c2 = 2
            alt_waktu_value = np.append(alt_waktu_value, c2)
        elif 4 >= waktu < 5:
            c2 = 3
            alt_waktu_value = np.append(alt_waktu_value, c2)
        elif 5 >= waktu < 6:
            c2 = 4
            alt_waktu_value = np.append(alt_waktu_value, c2)
        else:
            c2 = 5
            alt_waktu_value = np.append(alt_waktu_value, c2)
        
    st.title('Biaya - C3')
    for i in range(int(alt_value)):
        
        biaya = st.number_input(f"Tempat Wisata ke {i + 1}: {alt_name_value[i]}", min_value=2000000, value=2000000, step=1)

        if biaya <= 2000000:
            c3 = 3
            alt_biaya_value = np.append(alt_biaya_value, c3)
        else:
            c3 = 4
            alt_biaya_value = np.append(alt_biaya_value, c3)

    st.title('Fasilitas Tempat Wisata - C4')
    for i in range(int(alt_value)):
            
        fasilitas_tempat_options   = {'Sangat Buruk', 'Buruk', 'Cukup Baik', 'Baik', 'Sangat Baik'}
        selected_fasilitas_tempat_options = st.selectbox(f"Tempat wisata ke {i + 1}: {alt_name_value[i]}", fasilitas_tempat_options)
            
        c4 = fasilitas_tempat[selected_fasilitas_tempat_options]
        alt_fasilitas_value = np.append(alt_fasilitas_value, c4)

    st.title('Tingkat Keramaian Pengunjung - C5')
    for i in range(int(alt_value)):
            
        intensitas_pengunjung_options   = {'Sangat Sepi', 'Sepi', 'Cukup Ramai', 'Ramai', 'Ramai Pisan'}
        selected_intensitas_pengunjung_options = st.selectbox(f"Tempat wisata ke {i + 1}: {alt_name_value[i]}", intensitas_pengunjung_options)
            
        c5 = intensitas_pengunjung[selected_intensitas_pengunjung_options]
        alt_pengunjung_value = np.append(alt_pengunjung_value, c5)

button_clicked = st.button('Click me!')

# Check if the button is clicked
if button_clicked:
    #Bobot
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.header('Bobot :')     
    data_bobot = {
        'Jarak Tempuh': ['30%'],
        'Waktu Tempuh': ['20%'],
        'Biaya': ['20%'],
        'Fasilitas': ['15%'],
        'Keramaian': ['15%']
    }
    df_bobot = pd.DataFrame(data_bobot )
    st.markdown(df_bobot.to_html(index=False), unsafe_allow_html=True)

    #Tabel
    columns = ['Jarak Tempuh', 'Waktu Tempuh', 'Biaya', 'Fasilitas', 'Keramaian']
    dataset = np.vstack([alt_jarak_value, alt_waktu_value, alt_biaya_value, alt_fasilitas_value, alt_pengunjung_value]).T
    dataset_df = pd.DataFrame(dataset, columns=columns, index=alt_name_value)
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.header('Hasil Alternatif dan Kriteria :')
    st.write(dataset_df)
    # dataset = np.vstack([alt_jarak_value, alt_waktu_value, alt_biaya_value, alt_fasilitas_value, alt_pengunjung_value]).T
    # st.write('Array :')
    # st.write(dataset)
    
    # Weights
    weights = [0.2, 0.2, 0.3, 0.15, 0.15]

    # Load Criterion Type: 'max' or 'min'
    criterion_type = ['max', 'min', 'min', 'max', 'max']
    
    datasets = np.array([alt_jarak_value, alt_waktu_value, alt_biaya_value, alt_fasilitas_value, alt_pengunjung_value]).T
    # st.write(datasit)
    # st.write(alt_jarak_value)
    # st.write(datasets)

    #Ranking
    rank = edas_method(datasets, criterion_type, weights, graph = True, verbose = True)

    
    st.write(rank)
    max_row_index = np.argmax(rank)
    max_row_number = 0

    # Adding 1 to make it human-readable (assuming rows start from 1)
    max_row_number = alt_name_value[max_row_index]

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.header('Kesimpulan :')
    if max_row_number != 0 :
        st.write(f'Dari hasil perhitungan yang telah dilakukan, Tempat Wisata yang direkomendasikan untuk Study Tour adalah {max_row_number}')



