#!/bin/zsh
# Oczy na pierwszej klatce (zasada 11: klatka 0 to pierwsze wrazenie i miniaturka w feedzie).
# C4529 B i C4537 A (24-25.11.2026): dubel zaczynal sie od mrugniecia, wiec klatka 0 miala zamkniete oczy.
#
# Podglad:   zsh skrypty/oczy.sh pokaz [N=12]          -> analiza/oczy.jpg (pierwsze N klatek A-rollu, okolice oczu)
# Naprawa:   zsh skrypty/oczy.sh napraw K Z            -> klatki 0..K-1 zastapione klatka Z (oczy otwarte)
#   K ustaw tak, zeby nie wchodzic na mowe (pierwsze slowo w audio/slowa.json; przy 30 kl./s klatka = 0,033 s):
#   zamrozenie pod mowa psuje synchronizacje ust. Reszta mrugniecia po starcie mowy wyglada naturalnie.
#   Dzwiek i liczba klatek bez zmian (sprawdz sprawdz_sync.py). Po kazdym aroll.py naprawe trzeba powtorzyc.
# Kadr oczu (crop) dobrany do ujec z C45xx (twarz w gornej czesci); przy innym kadrze popraw CROP.
set -e
CROP="600:300:240:330"
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 aroll/aroll.mp4 | python3 -c "import sys;a,b=sys.stdin.read().strip().split('/');print(round(int(a)/int(b)))")
case "$1" in
  pokaz)
    N=${2:-12}
    ffmpeg -v error -y -i aroll/aroll.mp4 -vf "select='lt(n\,$N)',crop=$CROP,scale=150:-1,tile=${N}x1" -frames:v 1 analiza/oczy.jpg
    echo "analiza/oczy.jpg ($N klatek, $FPS kl./s)";;
  napraw)
    K=$2; Z=$3
    ffmpeg -v error -y -i aroll/aroll.mp4 -filter_complex \
      "[0:v]split[a][b];[a]trim=start_frame=$Z:end_frame=$((Z+1)),setpts=PTS-STARTPTS,loop=loop=$((K-1)):size=1:start=0,setpts=N/$FPS/TB[f];[b]trim=start_frame=$K,setpts=PTS-STARTPTS[r];[f][r]concat=n=2:v=1:a=0[v]" \
      -map "[v]" -map 0:a -r $FPS -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -color_range tv -colorspace bt709 \
      -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart aroll/aroll_oczy.mp4
    a=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 aroll/aroll_oczy.mp4)
    b=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 aroll/aroll.mp4)
    [[ "$a" == "$b" ]] || { echo "rozna liczba klatek ($a vs $b), nie podmieniam"; exit 1; }
    mv aroll/aroll_oczy.mp4 aroll/aroll.mp4 && ln -f aroll/aroll.mp4 hf/aroll.mp4
    echo "klatki 0..$((K-1)) = klatka $Z; liczba klatek $a bez zmian";;
  *) echo "uzycie: oczy.sh pokaz [N] | napraw K Z"; exit 1;;
esac
