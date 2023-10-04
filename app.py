import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host='localhost',# Misalnya localhost
        user = 'root',
        password = '',
        database = 'db_dal'
    )
    return connection

def get_data_from_db():
    conn = get_connection()
    query = 'SELECT * FROM pddikti_example'
    df = pd.read_sql(query,conn)
    conn.close()
    return df

st.title('streamlit simple app')
page=st.sidebar.radio("pilih halaman",["dataset","visualisasi","Form Input"])

if page == "dataset":
    st.header("Halaman dataset")
    # data= pd.read_csv("pddikti_example.csv")
    data = get_data_from_db()
    st.write(data)

elif page == "visualisasi":
    st.header("halaman visualisasi")  
    st.set_option('deprecation.showPyplotGlobalUse',False)
    # data= pd.read_csv("pddikti_example.csv")
    data = get_data_from_db()
    selected_uni=st.selectbox('pilih universitas',data['universitas'].unique())
    filtered_data= data[data['universitas']==selected_uni]

    plt.figure(figsize=(12, 6))
    for prog_studi in filtered_data['program_studi'].unique():
        subset=filtered_data[filtered_data['program_studi'] == prog_studi]

        subset=subset.sort_values(by="id", ascending=False)

        plt.plot(subset['semester'],subset['jumlah'],label=prog_studi)
    plt.title(f"Visualisasi data untuk{selected_uni}")
    plt.xlabel("semester")
    plt.xticks(rotation=90)
    plt.ylabel("jumlah")
    plt.legend()
    st.pyplot()
elif page == "Form Input":
    st.header("Halaman Form Input")
    with st.form(key='input_form'):
        input_semester = st.text_input('Semester')
        input_jumlah = st.number_input('Jumlah',min_value = 0,format = '%d')
        input_program_studi = st.text_input('Program Studi')
        input_universitas = st.text_input('Universitas')
        submit_button = st.form_submit_button(label='Submit Data')
    if submit_button:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO pddikti_example(semester,jumlah,program_studi,universitas)
        VALUES (%s,%s,%s,%s)
        """
        cursor.execute(query,(input_semester,input_jumlah,input_program_studi,input_universitas))
        conn.commit()
        conn.close()
        st.success('Data successfully submitted to the database')