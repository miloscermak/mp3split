import os
import streamlit as st
from pydub import AudioSegment
import math
import tempfile
import zipfile
import io

# Nastavení stránky
st.set_page_config(
    page_title="Audio Splitter",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Audio Splitter")
st.write("Rozdělte velké audio soubory na menší části")

@st.cache_data
def split_audio_file(input_file, max_size_mb=70):
    try:
        # Načtení audio souboru do paměti
        audio_bytes = input_file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{input_file.name.split(".")[-1]}') as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name

        # Načtení audio souboru
        file_extension = input_file.name.lower().split('.')[-1]
        if file_extension == 'm4a':
            audio = AudioSegment.from_file(tmp_file_path, format='m4a')
        else:
            audio = AudioSegment.from_mp3(tmp_file_path)
        
        # Odstranění dočasného souboru
        os.unlink(tmp_file_path)
        
        # Výpočet velikosti jedné milisekundy audia
        file_size = len(audio_bytes)
        ms_per_byte = len(audio) / file_size
        
        # Výpočet délky každé části
        max_size_bytes = max_size_mb * 1024 * 1024
        segment_length_ms = math.floor(ms_per_byte * max_size_bytes)
        
        # Rozdělení souboru
        total_segments = math.ceil(len(audio) / segment_length_ms)
        
        # Vytvoření ZIP souboru v paměti
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Rozdělení a uložení částí
            for i in range(total_segments):
                start = i * segment_length_ms
                end = min((i + 1) * segment_length_ms, len(audio))
                
                segment = audio[start:end]
                
                # Export do dočasného souboru v paměti
                segment_buffer = io.BytesIO()
                if file_extension == 'm4a':
                    segment.export(segment_buffer, format='ipod')
                else:
                    segment.export(segment_buffer, format='mp3')
                
                # Přidání do ZIP
                zip_file.writestr(
                    f"{os.path.splitext(input_file.name)[0]}_part{i+1}.{file_extension}",
                    segment_buffer.getvalue()
                )
                
                # Aktualizace progress baru
                progress = (i + 1) / total_segments
                progress_bar.progress(progress)
                status_text.text(f"Zpracovávám část {i+1} z {total_segments}")
            
            status_text.text("Hotovo! Klikněte na tlačítko níže pro stažení všech částí.")
        
        return zip_buffer.getvalue()
                
    except Exception as e:
        st.error(f"Došlo k chybě při zpracování souboru: {str(e)}")
        return None

# Uživatelské rozhraní
uploaded_file = st.file_uploader("Vyberte audio soubor (MP3 nebo M4A)", type=['mp3', 'm4a'])
max_size = st.slider("Maximální velikost části (MB)", min_value=10, max_value=100, value=70)

if uploaded_file is not None:
    if st.button("Rozdělit soubor"):
        zip_data = split_audio_file(uploaded_file, max_size)
        if zip_data:
            st.download_button(
                label="📥 Stáhnout všechny části (ZIP)",
                data=zip_data,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_parts.zip",
                mime="application/zip"
            )