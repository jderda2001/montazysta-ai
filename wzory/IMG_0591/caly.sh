#!/bin/zsh
# Caly przebieg jednego wariantu: ./caly.sh <folder> (. albo hookB): A-roll, falstarty, czasy slow, potem render.sh (obie wersje).
set -e
cd "$1"
python3 -I skrypty/aroll.py > aroll/render.log 2>&1; tail -1 aroll/render.log
ln -f aroll/aroll.mp4 hf/aroll.mp4
uv run --no-project --with numpy python3 -I skrypty/kawalki.py > analiza/kawalki.log 2>&1
uv run --no-project --with numpy python3 -I skrypty/slowa.py > analiza/slowa.log 2>&1
cd - > /dev/null
./render.sh "$1"
