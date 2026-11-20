#!/usr/bin/env python3
"""Sidon (sarulab-speech/sidon-v0.1, MIT, ICASSP 2026): odtworzenie mowy "jakosci studyjnej" z nagrania z pokoju.
Kod jak w demo autorow (huggingface.co/spaces/sarulab-speech/sidon_demo_beta, app.py), ale na wersjach CPU modeli
(feature_extractor_cpu.pt ok. 795 MB, decoder_cpu.pt ok. 210 MB; cache Hugging Face w ~/.cache/huggingface).

Uzycie (srodowisko izolowane przez uv, nic globalnie):
  uv run --no-project --python 3.12 --with torch --with torchaudio --with transformers --with huggingface_hub \
         --with numpy python -I sidon_infer.py WEJSCIE.wav WYJSCIE.wav
Wejscie: WAV 16 lub 32 bit (dowolna czestotliwosc). Wyjscie: 48 kHz mono 16 bit, ta sama dlugosc co wejscie.
"""
import sys
import time
import wave

import numpy as np
import torch
import torchaudio
import transformers
from huggingface_hub import hf_hub_download


def read_wav(path):
    with wave.open(path) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if sw == 2:
        x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    elif sw == 4:
        x = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2 ** 31
    else:
        raise SystemExit("Obslugiwane sa WAV 16 i 32 bit")
    return sr, x.reshape(-1, ch).mean(axis=1)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    t0 = time.time()
    fe_path = hf_hub_download("sarulab-speech/sidon-v0.1", filename="feature_extractor_cpu.pt")
    dec_path = hf_hub_download("sarulab-speech/sidon-v0.1", filename="decoder_cpu.pt")
    pre = transformers.SeamlessM4TFeatureExtractor.from_pretrained("facebook/w2v-bert-2.0")
    fe = torch.jit.load(fe_path, map_location="cpu").eval()
    dec = torch.jit.load(dec_path, map_location="cpu").eval()
    t1 = time.time()

    sr, x = read_wav(src)
    peak = float(np.abs(x).max())
    x = 0.9 * x / peak
    target = int(48_000 / sr * len(x))
    with torch.inference_mode():
        wav = torch.tensor(x, dtype=torch.float32).view(1, -1)
        wav = torchaudio.functional.highpass_biquad(wav, sr, 50)
        wav16 = torchaudio.functional.resample(wav, sr, 16_000)
        wav16 = torch.nn.functional.pad(wav16, (0, 24000))
        outs, cache = [], None
        for chunk in wav16.view(-1).split(16000 * 96):
            inputs = pre(torch.nn.functional.pad(chunk, (160, 160)).numpy(), sampling_rate=16000, return_tensors="pt")
            feat = fe(inputs["input_features"])["last_hidden_state"]
            if cache is not None:
                feat = torch.cat([cache, feat], dim=1)
            outs.append(dec(feat.transpose(1, 2)).view(-1)[:-960])
            cache = feat[:, -1:]
        y = torch.cat(outs, dim=0).numpy()[:target]

    y = np.clip(y, -1.0, 1.0)
    with wave.open(dst, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(48_000)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    print(f"sidon: {len(x) / sr:.2f} s -> {dst} | modele {t1 - t0:.1f} s, przetwarzanie {time.time() - t1:.1f} s | "
          f"torch {torch.__version__}, watki {torch.get_num_threads()}")


if __name__ == "__main__":
    main()
