#!/bin/zsh
# A-roll dla trzech wersji po kolei (kazda ok. 2-4 min ze zrodla 4K)
cd "$(dirname "$0")/.."
for h in A B C; do
  HOOK=$h python3 -I skrypty/aroll.py > $h/aroll/render.log 2>&1; echo "KONIEC $h $?" >> $h/aroll/render.log
  mkdir -p $h/hf/fonts $h/hf/renders
  cp -f hf/package.json hf/hyperframes.json hf/meta.json $h/hf/ 2>/dev/null
  cp -f hf/fonts/InterTight.ttf $h/hf/fonts/
  ln -f $h/aroll/aroll.mp4 $h/hf/aroll.mp4
done
