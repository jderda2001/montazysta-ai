#!/bin/zsh
# Glos C i czasy slow dla jednej wersji: ./przebieg_glos.sh A|B|C   (po aroll.py)
set -e
cd "${0:A:h}/$1"
uv run --no-project --with numpy python3 -I skrypty/kawalki.py > analiza/kawalki.log
uv run --no-project --with numpy python3 -I -c "import importlib.util,json,subprocess; from pathlib import Path; s=importlib.util.spec_from_file_location('g','skrypty/glos.py'); g=importlib.util.module_from_spec(s); s.loader.exec_module(g); Path('audio/studio').mkdir(exist_ok=True); g.raw_concat(json.loads(Path('aroll/edl.json').read_text()), Path('audio/studio/surowe32.wav').resolve()); subprocess.run(['ffmpeg','-v','error','-y','-i','audio/studio/surowe32.wav','-c:a','pcm_s16le','audio/studio/surowe.wav'],check=True)"
uv run --no-project --python 3.12 --with torch --with torchaudio --with transformers --with huggingface_hub --with numpy python -I skrypty/sidon_infer.py audio/studio/surowe.wav audio/studio/sidon.wav 2>&1 | grep sidon:
uv run --no-project --with numpy python3 -I skrypty/studio.py | grep -E "przesuniecie|wyrownaniu|F0|gleboki"
uv run --no-project --with numpy python3 -I skrypty/slowa.py > analiza/slowa.log
echo "GLOS_OK $1"
