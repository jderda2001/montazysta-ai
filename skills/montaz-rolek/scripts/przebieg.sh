#!/bin/zsh
# Przebieg od A-rollu do gotowej kompozycji dla jednego folderu wersji (projekt albo projekt/hookB).
# Uzycie: zsh skrypty/przebieg.sh <folder_wersji>
# Kolejnosc: aroll.py -> link do hf -> powtorzenia.py -> slowa.py (ostatnia kwestia przycieta do konca mowy) ->
# kompozycja.py -> strefa.py -> kompozycja.py (strefa.py zostawia tryb kontrolny) -> hyperframes check.
# Dlaczego slowa.py na przycietej ostatniej kwestii: ogon END_HOLD (2,5 s pod plansza koncowa) zawiera zwykle
# "Dobra, lecimy dalej" itp.; whisper z promptem potrafil wtedy pominac cale CTA (C4528, 24.11.2026).
# Po przebiegu: obejrzyj klatki (hyperframes snapshot), sprawdz przerwy (przerwy.py) i oczy na klatce 0 (oczy.sh).
set -e
cd "$1"
python3 -I skrypty/aroll.py | tail -1
ln -f aroll/aroll.mp4 hf/aroll.mp4
uv run --no-project --with numpy python3 -I skrypty/powtorzenia.py 2>&1 | grep -v "^Każde" | tail -8 || true
cp aroll/edl.json aroll/edl_full.json
python3 - <<'PY'
import json
e = json.load(open("aroll/edl.json")); l = e[-1]
cut = l["speech"][1] + 0.3
l["a_out"] = round(cut, 4); l["t_out"] = round(l["t_in"] + cut - l["a_in"], 4)
l["shots"][-1]["dur"] = round(l["t_out"] - l["shots"][-1]["t_in"], 4)
json.dump(e, open("aroll/edl.json", "w"), ensure_ascii=False, indent=1)
PY
uv run --no-project --with numpy python3 -I skrypty/slowa.py > /dev/null 2>&1
cp aroll/edl_full.json aroll/edl.json
python3 -I skrypty/kompozycja.py 2>&1 | grep -E "sceny|UWAGA|Traceback|Error|Niezgod|Brak slow|Nieprzyp|Nie znal" || true
uv run --no-project --with numpy python3 -I skrypty/strefa.py 2>&1 | grep -A6 "strefa bezpieczna" || true
python3 -I skrypty/kompozycja.py > /dev/null 2>&1
(cd hf && ~/.local/bin/hyperframes check 2>&1 | grep -E "✗|Check (passed|failed)")
