#!/bin/zsh
# Caly przebieg dla jednego wariantu: ./przebieg.sh <folder projektu> (np. . albo hookB).
# OD=kompozycja ./przebieg.sh .   -> pomija A-roll, glos i czasy slow (gdy zmienila sie tylko kompozycja)
# Kazdy krok zapisuje wynik do pliku i dopiero potem jest skracany, zeby blad kroku zatrzymal przebieg
# (potok z head/grep gubi kod wyjscia; tak poszedl render ze stara kompozycja przy pierwszej probie).
set -e
cd "$1"
if [[ "$OD" != "kompozycja" ]]; then
  python3 -I skrypty/aroll.py > aroll/render.log 2>&1; tail -1 aroll/render.log
  ln -f aroll/aroll.mp4 hf/aroll.mp4
  uv run --no-project --with numpy python3 -I skrypty/kawalki.py > analiza/kawalki.log 2>&1
  uv run --no-project --with numpy python3 -I skrypty/sprawdz_sync.py > analiza/sync.log 2>&1; tail -2 analiza/sync.log
  if [[ "$GLOS_AI" == "1" ]]; then  # wariant C (Sidon + lancuch radiowy) tylko na zyczenie; domyslnie glos naturalny z aroll.wav
    uv run --no-project --with numpy python3 -I -c "import importlib.util,json,subprocess; from pathlib import Path; s=importlib.util.spec_from_file_location('g','skrypty/glos.py'); g=importlib.util.module_from_spec(s); s.loader.exec_module(g); Path('audio/studio').mkdir(exist_ok=True); g.raw_concat(json.loads(Path('aroll/edl.json').read_text()), Path('audio/studio/surowe32.wav').resolve()); subprocess.run(['ffmpeg','-v','error','-y','-i','audio/studio/surowe32.wav','-c:a','pcm_s16le','audio/studio/surowe.wav'],check=True)"
    uv run --no-project --python 3.12 --with torch --with torchaudio --with transformers --with huggingface_hub --with numpy python -I skrypty/sidon_infer.py audio/studio/surowe.wav audio/studio/sidon.wav > audio/studio/sidon.log 2>&1; tail -1 audio/studio/sidon.log
    uv run --no-project --with numpy python3 -I skrypty/studio.py > audio/studio/studio.log 2>&1; grep -E "wyrownaniu|F0|gleboki" audio/studio/studio.log
  fi
  uv run --no-project --with numpy python3 -I skrypty/slowa.py > analiza/slowa.log 2>&1
fi
python3 -I skrypty/kompozycja.py > analiza/kompozycja.log 2>&1 || { cat analiza/kompozycja.log; exit 1; }
head -1 analiza/kompozycja.log
cd hf
~/.local/bin/hyperframes check > ../analiza/check.log 2>&1 || true
grep -E "error\(s\)|StaticGuard" ../analiza/check.log | cut -c1-200
if grep -qE "^ +[1-9][0-9]* error\(s\)" ../analiza/check.log; then echo "CHECK: bledy, stop"; exit 1; fi
~/.local/bin/hyperframes render -o renders/final.mp4 --quality delivery --video-frame-format png > renders/render.log 2>&1
uv run --no-project --with numpy python3 -I ../skrypty/kontrola_eksportu.py renders/final.mp4 glos.wav
echo PRZEBIEG_OK
