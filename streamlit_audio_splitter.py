import os
import streamlit as st
from pydub import AudioSegment
import math
import tempfile
import zipfile
import io

st.title("🎵 Audio Splitter")
st.write("Rozdělte velké audio soubory na menší části")

def split_audio_file(input_file, max_size_mb=70):
    try:
        # Načtení audio souboru
        file_extension = input_file.name.lower().split('.')[-1]
        if file_extension == 'm4a':
            audio = AudioSegment.from_file(input_file, format='m4a')
        else:
            audio = AudioSegment.from_mp3(input_file)
        
        # Výpočet velikosti jedné milisekundy audia
        file_size = input_file.size
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
            with tempfile.TemporaryDirectory() as temp_dir:
                for i in range(total_segments):
                    start = i * segment_length_ms
                    end = min((i + 1) * segment_length_ms, len(audio))
                    
                    segment = audio[start:end]
                    output_filename = f"{os.path.splitext(input_file.name)[0]}_part{i+1}.{file_extension}"
                    temp_path = os.path.join(temp_dir, output_filename)
                    
                    if file_extension == 'm4a':
                        segment.export(temp_path, format='ipod')
                    else:
                        segment.export(temp_path, format='mp3')
                    
                    # Přidání souboru do ZIP archivu
                    zip_file.write(temp_path, output_filename)
                    
                    # Aktualizace progress baru
                    progress = (i + 1) / total_segments
                    progress_bar.progress(progress)
                    status_text.text(f"Zpracovávám část {i+1} z {total_segments}")
            
            status_text.text("Hotovo! Klikněte na tlačítko níže pro stažení všech částí.")
        
        # Nabídnutí ZIP souboru ke stažení
        zip_buffer.seek(0)
        base_name = os.path.splitext(input_file.name)[0]
        st.download_button(
            label="📥 Stáhnout všechny části (ZIP)",
            data=zip_buffer,
            file_name=f"{base_name}_parts.zip",
            mime="application/zip"
        )
                
    except Exception as e:
        st.error(f"Došlo k chybě při zpracování souboru: {str(e)}")

# Uživatelské rozhraní
uploaded_file = st.file_uploader("Vyberte audio soubor (MP3 nebo M4A)", type=['mp3', 'm4a'])
max_size = st.slider("Maximální velikost části (MB)", min_value=10, max_value=100, value=70)

if uploaded_file is not None:
    if st.button("Rozdělit soubor"):
        split_audio_file(uploaded_file, max_size) 