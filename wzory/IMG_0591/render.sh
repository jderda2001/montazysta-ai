#!/bin/zsh
# Render i kontrola jednego wariantu: ./render.sh <folder wariantu> (np. . albo hookB). Robi obie wersje: hf (efekty) i hfn (napisy).
# Wynik kazdego kroku idzie do pliku, zeby blad zatrzymal przebieg (potok z head gubi kod wyjscia).
set -e
cd "$1"
for tryb in efekty napisy; do
  d=hf; [[ $tryb == napisy ]] && d=hfn
  python3 -I skrypty/kompozycja.py $tryb > analiza/kompozycja_$tryb.log 2>&1 || { tail -5 analiza/kompozycja_$tryb.log; exit 1; }
  tail -1 analiza/kompozycja_$tryb.log
  (cd $d && ~/.local/bin/hyperframes check > ../analiza/check_$tryb.log 2>&1 || true)
  grep -E "error\(s\)|StaticGuard" analiza/check_$tryb.log | cut -c1-200
  if grep -qE "^ +[1-9][0-9]* error\(s\)" analiza/check_$tryb.log; then echo "CHECK: bledy, stop"; exit 1; fi
  (cd $d && ~/.local/bin/hyperframes render -o renders/final.mp4 --quality delivery --video-frame-format png > renders/render.log 2>&1)
  (cd $d && uv run --no-project --with numpy python3 -I ../skrypty/kontrola_eksportu.py renders/final.mp4 glos.wav) > analiza/kontrola_$tryb.log 2>&1
  head -2 analiza/kontrola_$tryb.log
  # sprzatanie klatek, ktore HyperFrames zostawia w katalogu tymczasowym (ok. 6 GB na render): tylko wpisy nowsze niz znacznik
  # ustawiony przez wywolujacego (HF_ZNACZNIK) i tylko gdy nikt inny akurat nie renderuje
  if [[ -n $HF_ZNACZNIK ]] && ! pgrep -f "hyperframes render" > /dev/null; then
    find "${TMPDIR%/}/hyperframes-extract-cache-$(id -u)" -maxdepth 1 -name 'hfcache-v8-*' -newer "$HF_ZNACZNIK" -exec rm -rf {} + 2>/dev/null || true
  fi
done
echo RENDER_OK
