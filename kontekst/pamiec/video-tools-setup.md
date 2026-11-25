---
name: video-tools-setup
description: "Where the video-editing toolchain (ffmpeg, yt-dlp, whisper.cpp, HyperFrames, Remotion) lives on the user's Mac and how it was installed"
metadata:
  node_type: memory
  type: reference
  originSessionId: 86deeb8d-c257-42cc-9214-7efdf8a192fb
  modified: 2026-11-17T16:46:31.663Z
---

Zainstalowane 2026-11-07 bez Homebrew (brak sudo bez hasła) — wszystko w `~/.local`, które jest w PATH przez `~/.local/bin/env` w `~/.zshrc`.

- **FFmpeg n9.0.2** + libx264 zbudowane ze źródeł (`~/.local/src/FFmpeg`, `~/.local/src/x264`), bez libass/freetype/libx265. Są h264/hevc_videotoolbox.
- **yt-dlp** 2026.10.26 — oficjalny binarny release w `~/.local/bin/yt-dlp`; config `~/.config/yt-dlp/config` wskazuje node 22 jako JS runtime (YouTube tego wymaga).
- **whisper.cpp v1.9.5** — `whisper-cli` w `~/.local/bin`, Metal działa (Apple M5). Modele w `~/.local/share/whisper.cpp/models/`: `ggml-large-v3-turbo-q5_0.bin` (domyślny wybór, poprawny dla polskiego) oraz `ggml-base.bin` (słaby dla polskiego, tylko do szybkich testów). DTW (`-dtw large.v3.turbo`) działa tylko z `-nfa`: flash attention jest domyślnie włączone i po cichu wyłącza DTW (t_dtw = −1). W tej wersji t_dtw tokenu wypada mniej więcej na jego końcu.
- **HyperFrames 0.9.20** — wymaga Node >= 22, a domyślny node to 20; dlatego `~/.local/bin/hyperframes` to wrapper na node v22.23.3 (`~/.local/lib/hyperframes`).
  - **Wspólna kolejka i pamięć klatek (17.11.2026, IMG_0585):** na tym Macu bywa kilka sesji montażu naraz. HyperFrames puszcza jeden render naraz na całe konto (`~/.cache/hyperframes/locks/render.lock`), a klatki A-rollu trzyma w `$TMPDIR/hyperframes-extract-cache-501/hfcache-v8-*` (PNG, ok. 3,3 GB na 55 s rolki, 6 GB na 93 s). Przy sześciu renderach urosło to do 37 GB i dysk się zapełnił (render pada z „Low disk space”). Przed renderem sprawdź `df -h`, a po udanym renderze usuń własny wpis (rozpoznasz go po liczbie klatek = długość × 30). Cudzych wpisów i procesów nie ruszaj: `pkill -f "hyperframes render"` przerwał rendery dwóch innych sesji. Własny proces zatrzymuj po PID.
- **Remotion 4.0.541** — instalowany per projekt (`npm i remotion @remotion/cli react react-dom`), brak globalnej instalacji; przykład w `/Users/jd/Montażysta AI/testy/remotion`.
- cmake i pkgconf przez `uv tool install` (potrzebne do buildów).
- **Sidon** (AI do odtwarzania „studyjnej” mowy, MIT, pobrany za zgodą użytkownika 13.11.2026). Wagi `sarulab-speech/sidon-v0.1` (wersje CPU, ok. 1 GB) leżą w `~/.cache/huggingface`. Uruchamiam bez instalacji globalnej, w środowisku uv: `uv run --no-project --python 3.12 --with torch --with torchaudio --with transformers --with huggingface_hub --with numpy python -I sidon_infer.py WEJ.wav WYJ.wav` (skrypt w `projekty/IMG_0526/skrypty/`). 48 s głosu przetwarza w ok. 12 s na CPU, wynik 48 kHz z opóźnieniem ok. 8 ms do wyrównania.

**How to apply:** nie sugeruj `brew install` ani globalnego `npm i -g` dla tych narzędzi; do HyperFrames używaj node 22.
