#!/usr/bin/env python3
"""pad_bend.py — add a silent tail to BEND's narration so the closing picture holds.

"I'm Nee-shaant." voices in about 1.3 s, too short for the name card to be read. The show-tell skill
pads its closing beat with a silent tail and re-measures it (it does this for BOUT); this does the same
for BEND. Run after generate_audio_kokoro.py, and again after any re-voice of BEND.
Idempotent: the unpadded voice is kept as mp3/beat-BEND.voice.mp3 and the pad is rebuilt from it.
"""
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAIL_S = 2.0
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"


def dur(p):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


sheet_p, timings_p = HERE / "beat_sheet.json", HERE / "mp3" / "timings.json"
sheet = json.loads(sheet_p.read_text(encoding="utf-8"))
bend = next(b for b in sheet["beats"] if b["beat_id"] == "BEND")
mp3, voice = HERE / "mp3" / "beat-BEND.mp3", HERE / "mp3" / "beat-BEND.voice.mp3"
if not voice.exists() or bend.get("tail_pad_s") is None:
    shutil.copyfile(mp3, voice)          # fresh Kokoro output: keep it as the unpadded voice
tmp = mp3.with_suffix(".tmp.mp3")
subprocess.run([FFMPEG, "-y", "-v", "error", "-i", str(voice), "-af", f"apad=pad_dur={TAIL_S}",
                "-c:a", "libmp3lame", "-q:a", "2", str(tmp)], check=True)
tmp.replace(mp3)
d = round(dur(mp3), 2)
bend["actual_duration_s"], bend["tail_pad_s"] = d, TAIL_S
sheet_p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
t = json.loads(timings_p.read_text(encoding="utf-8"))
t["BEND"] = d
timings_p.write_text(json.dumps(t, indent=2) + "\n", encoding="utf-8")
total = sum(b["actual_duration_s"] for b in sheet["beats"])
print(f"[pad] BEND {dur(voice):.2f}s voice + {TAIL_S}s tail = {d}s; film total {total:.2f}s "
      f"({int(total // 60)}:{total % 60:04.1f})")
