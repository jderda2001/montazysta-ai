#!/bin/zsh
# Glos C dla jednej wersji: surowe ciecia -> Sidon -> lancuch radiowy (studio.py). Uzycie: skrypty/glos_c.sh A
cd "$(dirname "$0")/.."
export HOOK=$1
mkdir -p $HOOK/audio/studio
uv run --no-project --with numpy python3 -I -c "
import importlib.util, json, subprocess
from pathlib import Path
s = importlib.util.spec_from_file_location('g', 'skrypty/glos.py'); g = importlib.util.module_from_spec(s); s.loader.exec_module(g)
d = g.P / 'audio/studio'
g.raw_concat(json.loads((g.P / 'aroll/edl.json').read_text()), (d / 'surowe32.wav').resolve())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(d / 'surowe32.wav'), '-c:a', 'pcm_s16le', str(d / 'surowe.wav')], check=True)
(d / 'surowe32.wav').unlink()
" || exit 1
uv run --no-project --python 3.12 --with torch --with torchaudio --with transformers --with huggingface_hub --with numpy \
   python -I skrypty/sidon_infer.py $HOOK/audio/studio/surowe.wav $HOOK/audio/studio/sidon.wav || exit 1
uv run --no-project --with numpy python3 -I skrypty/studio.py
