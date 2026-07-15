import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

st.title("Distribusi Hasil Analisis Sentimen Kendaraan Listrik")

# Upload file
uploaded_file = st.file_uploader("Upload file hasil analisis (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Baca file
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    # Validasi kolom
    if 'clean_text' not in df.columns or not any(col in df.columns for col in ['sentimen', 'polarity']):
        st.error("File harus memiliki kolom 'clean_text' dan 'sentimen' atau 'polarity'.")
    else:
        # Gunakan kolom sentimen
        sentimen_col = 'sentimen' if 'sentimen' in df.columns else 'polarity'
        df[sentimen_col] = df[sentimen_col].str.lower()

        # Preview
        st.subheader("Preview Data")
        st.dataframe(df[['clean_text', sentimen_col]], use_container_width=True, height=400)

        # Filter sentimen
        filter_sentimen = st.selectbox(
            "Pilih Sentimen yang Ingin Ditampilkan:",
            ("Positif", "Negatif")
        )

        if filter_sentimen == "Positif":
            df_filtered = df[df[sentimen_col] == 'positive']
        else:
            df_filtered = df[df[sentimen_col] == 'negative']

        st.subheader(f"Data {filter_sentimen}")
        st.dataframe(df_filtered[['clean_text', sentimen_col]], use_container_width=True, height=400)

        # Bar chart
        st.subheader("Visualisasi Sentimen Kendaraan Listrik")
        total_positif = 951
        total_negatif = 849
        labels = ['Positif', 'Negatif']
        counts = [total_positif, total_negatif]
        colors = ['dodgerblue', 'red']

        fig, ax = plt.subplots()
        bars = ax.bar(labels, counts, color=colors)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 10,
                    str(int(bar.get_height())),
                    ha='center')
        ax.set_title('Distribusi Sentimen Kendaraan Listrik')
        ax.set_xlabel('Kategori Sentimen')
        ax.set_ylabel('Jumlah Tweet')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)

        # Pilihan kategori WordCloud
        filter_wordcloud = st.selectbox(
            "Pilih Kategori WordCloud yang Ingin Ditampilkan:",
            ("Positif", "Negatif")
        )

        def plot_cloud(text, title, colormap):
            wordcloud = WordCloud(
                width=1000,
                height=600,
                background_color='black',
                stopwords=STOPWORDS,
                colormap=colormap,
                collocations=False
            ).generate(text)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(title, fontsize=14)
            st.pyplot(fig)

        # WordCloud
        positif_tweets = df[df[sentimen_col] == 'positive']['clean_text']
        negatif_tweets = df[df[sentimen_col] == 'negative']['clean_text']
        all_positif = ' '.join(positif_tweets.dropna().astype(str))
        all_negatif = ' '.join(negatif_tweets.dropna().astype(str))

        if filter_wordcloud == "Positif":
            st.subheader("WordCloud Tweet Positif")
            plot_cloud(all_positif, "WordCloud Tweet Positif", "Blues")
        else:
            st.subheader("WordCloud Tweet Negatif")
            plot_cloud(all_negatif, "WordCloud Tweet Negatif", "Reds")
