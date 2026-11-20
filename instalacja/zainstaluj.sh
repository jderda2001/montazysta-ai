#!/bin/zsh
# Instalator Montażysty AI na nowym Macu (macOS, Apple Silicon albo Intel).
# Uruchom z folderu repo:  zsh instalacja/zainstaluj.sh
# Skrypt można uruchamiać wielokrotnie: pomija to, co już jest, i niczego nie kasuje (stare skille przenosi do kopii).

set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DOM="$HOME/Montażysta AI"            # folder roboczy Claude Code (projekty, CLAUDE.md)
PULPIT="$HOME/Desktop/Montażysta AI"  # nagrania i eksporty
LOCAL="$HOME/.local"
DZIS="$(date +%Y-%m-%d)"

ok()   { print -P "%F{green}✓%f $*"; }
info() { print -P "%F{cyan}→%f $*"; }
stop() { print -P "%F{red}✗%f $*"; exit 1; }

[[ "$(uname)" == "Darwin" ]] || stop "Ten zestaw działa tylko na macOS (pomiar twarzy i miniatury korzystają z Apple Vision)."

# 1. Narzędzia Xcode (swiftc do pomiaru twarzy i do skilla miniatur)
if ! xcode-select -p >/dev/null 2>&1; then
  xcode-select --install 2>/dev/null
  stop "Zainstaluj narzędzia Xcode (okno właśnie się otworzyło), potem uruchom skrypt jeszcze raz."
fi
ok "Narzędzia Xcode"

# 2. Homebrew
if ! command -v brew >/dev/null 2>&1; then
  for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do [[ -x $b ]] && eval "$($b shellenv)"; done
fi
command -v brew >/dev/null 2>&1 || stop 'Brak Homebrew. Zainstaluj go (poprosi o hasło do Maca):
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
i uruchom ten skrypt jeszcze raz.'
ok "Homebrew"

# 3. Pakiety: ffmpeg, whisper.cpp, Node 22 (HyperFrames), uv (Python), gh (GitHub)
for p in ffmpeg whisper-cpp node@22 uv gh; do
  if brew list --versions $p >/dev/null 2>&1; then ok "$p"; else info "instaluję $p"; brew install $p || stop "brew install $p się nie udał"; fi
done
NODE22="$(brew --prefix node@22)/bin"

# 4. PATH: ~/.local/bin (hyperframes, twarz) i ścieżka repo
mkdir -p "$LOCAL/bin"
if ! grep -q 'HOME/.local/bin' "$HOME/.zshrc" 2>/dev/null; then
  print '\n# Montażysta AI\nexport PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
fi
if [[ "$REPO" != "$DOM/montazysta-ai" ]] && ! grep -q MONTAZ_REPO "$HOME/.zshrc" 2>/dev/null; then
  print "export MONTAZ_REPO=\"$REPO\"" >> "$HOME/.zshrc"
fi
export PATH="$LOCAL/bin:$PATH"
ok "PATH (~/.local/bin w ~/.zshrc)"

# 5. Model whispera (ok. 550 MB)
MODEL="$LOCAL/share/whisper.cpp/models/ggml-large-v3-turbo-q5_0.bin"
if [[ -s "$MODEL" ]]; then ok "model whispera"; else
  info "pobieram model whispera large-v3-turbo-q5_0 (ok. 550 MB)"
  mkdir -p "${MODEL:h}"
  curl -fL --progress-bar -o "$MODEL.part" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin" && mv "$MODEL.part" "$MODEL" \
    || stop "nie udało się pobrać modelu whispera"
  ok "model whispera"
fi

# 6. HyperFrames 0.9.20 na Node 22 (+ Chrome do renderu)
HFDIR="$LOCAL/lib/hyperframes"
if [[ ! -f "$HFDIR/node_modules/hyperframes/bin/hyperframes.mjs" ]]; then
  info "instaluję HyperFrames 0.9.20"
  mkdir -p "$HFDIR"
  PATH="$NODE22:$PATH" "$NODE22/npm" --prefix "$HFDIR" install hyperframes@0.9.20 >/dev/null || stop "instalacja HyperFrames się nie udała"
fi
if [[ ! -x "$LOCAL/bin/hyperframes" ]]; then
  cat > "$LOCAL/bin/hyperframes" <<EOF
#!/bin/bash
# HyperFrames wymaga Node >= 22, dlatego uruchamiamy go przez Node 22 z Homebrew.
exec "$NODE22/node" "$HFDIR/node_modules/hyperframes/bin/hyperframes.mjs" "\$@"
EOF
  chmod +x "$LOCAL/bin/hyperframes"
fi
hyperframes browser install >/dev/null 2>&1 || true
ok "HyperFrames $(hyperframes --version 2>/dev/null | head -1)"

# 7. Pomiar twarzy (Apple Vision)
if [[ ! -x "$LOCAL/bin/twarz" ]]; then
  swiftc -O -o "$LOCAL/bin/twarz" "$REPO/skills/montaz-rolek/scripts/twarz.swift" || stop "kompilacja twarz.swift się nie udała"
fi
ok "twarz (pomiar twarzy)"

# 8. Foldery robocze
mkdir -p "$DOM/projekty" "$PULPIT/Nagrania " "$PULPIT/Referencje i wytyczne" \
         "$PULPIT/Eksporty/Rolki" "$PULPIT/Eksporty/Reklamy adGen" "$PULPIT/Eksporty/YouTube"
ok "foldery: ~/Montażysta AI/projekty i ~/Desktop/Montażysta AI (Nagrania, Eksporty, Referencje)"

# 9. Wzorcowe projekty (skrypty, notatki, branding, szkielet hf) do ~/Montażysta AI/projekty
rsync -a --ignore-existing "$REPO/wzory/" "$DOM/projekty/"
ok "wzorcowe projekty w ~/Montażysta AI/projekty"

# 10. Skille Claude Code jako linki do repo (stara wersja trafia do kopii)
mkdir -p "$HOME/.claude/skills"
for s in montaz-rolek miniatury; do
  cel="$HOME/.claude/skills/$s"
  if [[ -L "$cel" ]]; then rm "$cel"
  elif [[ -e "$cel" ]]; then mkdir -p "$HOME/.claude/skills-kopia-$DZIS"; mv "$cel" "$HOME/.claude/skills-kopia-$DZIS/"; info "stary skill $s przeniesiony do ~/.claude/skills-kopia-$DZIS"; fi
  ln -s "$REPO/skills/$s" "$cel"
done
ok "skille montaz-rolek i miniatury podpięte z repo"

# 11. Zasady zespołu jako CLAUDE.md folderu roboczego
if [[ -e "$DOM/CLAUDE.md" && ! -L "$DOM/CLAUDE.md" ]]; then mv "$DOM/CLAUDE.md" "$DOM/CLAUDE.md.kopia-$DZIS"; fi
ln -sfn "$REPO/ZASADY.md" "$DOM/CLAUDE.md"
ok "~/Montażysta AI/CLAUDE.md → ZASADY.md"

# 12. Kontrola
print
ffmpeg -hide_banner -version 2>/dev/null | head -1
whisper-cli --help 2>&1 | grep -q -- "-nfa" && ok "whisper-cli (z -nfa)" || print -P "%F{yellow}!%f whisper-cli bez flagi -nfa: daj znać Jakubowi"
[[ -s "$HOME/.config/kie/api_key" || -n "${KIE_API_KEY:-}" ]] && ok "klucz kie.ai" \
  || print -P "%F{yellow}!%f brak klucza kie.ai (potrzebny tylko do miniatur): zapisz go w ~/.config/kie/api_key i ustaw chmod 600"
print
ok "Gotowe. Otwórz nowe okno terminala (albo Claude Code) w folderze: $DOM"
