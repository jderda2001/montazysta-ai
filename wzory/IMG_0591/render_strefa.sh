#!/bin/zsh
# Render i kontrola jednego wariantu (efekty + napisy): ./render_strefa.sh <folder> (. albo hookB). Jak render.sh z projektu
# IMG_0591, tylko z kontrola strefy i sprzataniem WLASNEJ pamieci klatek HyperFrames (wpisy nowsze niz znacznik, gdy nikt inny nie renderuje).
set -e
cd "$1"
ZN=$(mktemp)
for tryb in efekty napisy; do
  d=hf; [[ $tryb == napisy ]] && d=hfn
  python3 -I skrypty/kompozycja.py $tryb > analiza/kompozycja_$tryb.log 2>&1 || { tail -5 analiza/kompozycja_$tryb.log; exit 1; }
  tail -1 analiza/kompozycja_$tryb.log | cut -c1-200
  (cd $d && ~/.local/bin/hyperframes check > ../analiza/check_$tryb.log 2>&1 || true)
  grep -E "error\(s\)" analiza/check_$tryb.log | head -3
  if grep -qE "^ +[1-9][0-9]* error\(s\)" analiza/check_$tryb.log; then echo "CHECK: bledy, stop"; exit 1; fi
  (cd $d && ~/.local/bin/hyperframes render -o renders/final.mp4 --quality delivery --video-frame-format png > renders/render.log 2>&1)
  (cd $d && uv run --no-project --with numpy python3 -I ../skrypty/kontrola_eksportu.py renders/final.mp4 glos.wav) > analiza/kontrola_$tryb.log 2>&1
  head -2 analiza/kontrola_$tryb.log
  if ! pgrep -f "hyperframes render" > /dev/null; then
    find "${TMPDIR%/}/hyperframes-extract-cache-$(id -u)" -maxdepth 1 -name 'hfcache-v8-*' -newer "$ZN" -exec rm -rf {} + 2>/dev/null || true
  fi
done
rm -f "$ZN"
echo RENDER_OK
