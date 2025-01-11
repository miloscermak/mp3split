# mp3split
# 🎵 Audio Splitter

Jednoduchá Streamlit aplikace pro rozdělení velkých audio souborů (MP3, M4A) na menší části. Aplikace automaticky rozdělí soubor na části o maximální velikosti, kterou si zvolíte, a poskytne je ke stažení v ZIP archivu.

## 🚀 Demo
Aplikaci můžete vyzkoušet na [Streamlit Cloud](váš-odkaz-zde)

## ⚙️ Instalace

### Požadavky
- Python 3.11 nebo novější
- ffmpeg

### Postup instalace

1. Naklonujte repozitář:
bash
git clone <váš-repozitář>
cd <složka-projektu>

2. Vytvořte virtuální prostředí:
bash
python -m venv .venv
Pro macOS/Linux:
source .venv/bin/activate
Pro Windows:
.venv\Scripts\activate

3. Nainstalujte závislosti:
bash
pip install -r requirements.txt

4. Nainstalujte ffmpeg:
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`
- Windows: Stáhněte z [ffmpeg.org](https://ffmpeg.org/download.html)

## 🎮 Použití

### Lokální spuštění
bash
streamlit run streamlit_audio_splitter.py


### Jak používat aplikaci
1. Nahrajte audio soubor (MP3 nebo M4A)
2. Pomocí posuvníku nastavte maximální velikost částí (10-100 MB)
3. Klikněte na tlačítko "Rozdělit soubor"
4. Počkejte na dokončení zpracování
5. Stáhněte si ZIP soubor obsahující všechny části

## 🛠 Funkce
- Podpora formátů MP3 a M4A
- Nastavitelná maximální velikost částí
- Progress bar zobrazující průběh zpracování
- Automatické zabalení všech částí do ZIP archivu
- Zachování kvality původního audio souboru

## 📝 Poznámky
- Velikost výsledných souborů se může mírně lišit od nastavené maximální velikosti
- Aplikace zachovává původní formát souboru
- Rozdělení probíhá bez překódování, což zajišťuje zachování kvality

## 📜 Licence
Tento projekt je licencován pod [MIT licencí](LICENSE).
