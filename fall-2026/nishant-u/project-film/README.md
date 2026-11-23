# A job-search agent that shows its evidence — Final Project Film

**Nishant U** · INFO 7375, Fall 2026 · runtime **3:20.75** (200.75 s) · 3840×2160, 24 fps · 14.0 MB

## What this is

My Final Project Film, in four parts: **Executive summary, Introduction, Methods, Evaluation**. It
describes the job-search agent I am building for international data and machine-learning graduates. The
agent watches public job boards at e-commerce companies (Faire, Instacart and Poshmark on Greenhouse and
Ashby) for one fictional graduate, Priya Nair. It reports only new postings and gives each one two
verdicts: a rule anyone can recompute, and Claude's judgment in a fixed format that a validator checks.
The film separates what is built (JS1, the watch: PR #30; JS2, the bounded loop with a permission
policy in code: PR #44) from what comes next: the filter and shortlist, the tool server, the planner and
memory, the human approval gate, and the "insufficient" label. Every picture of something not yet built
carries an on-screen **constructed** label. The Evaluation part reports the JS1 held-out result (10/10,
95% interval 69–100%) and the JS2 finished-wrong-answer that an independent check caught, then the
final-project evaluation plan.

It is a show-tell film (Brutalist toolkit): one isometric Manim drawing per beat, labels of a few
words, and my script read word for word by the free local Kokoro voice `am_michael`, with my name
spelled "Nee-shaant" for the voice only. No persona, no Your Turn, no title outro; the film closes on a
drawn beat, BEND. No Claude responses appear in the film. No logos are drawn.

**Not yet signed off:** every row of `FACTCHECK.md` is "unverified — Nishant to sign off".

## Files

| File | What it is |
|---|---|
| `final-project-film-nishant-u.mp4` | The final 4K master |
| `final-project-film-nishant-u.verified.json` | The toolkit's render-integrity record: `status: ready`, SHA-256, input hashes (local paths replaced with `~`) |
| `make_sheet.py` | Generates `beat_sheet.json`; holds my script verbatim in `SCRIPT` and checks that the beats reproduce it exactly |
| `beat_sheet.json` | 22 beats: narration, part, labels, "constructed" flags, measured durations, build stamps |
| `pad_bend.py` | Adds a 2.0 s silent tail to BEND's audio so the name card holds |
| `scenes.py` | The 22 isometric Manim scenes (the show-tell kit `iso_kit.py` pasted in, then the film's scenes) |
| `mp3/timings.json` | Measured narration duration of each beat (the mp3s are regenerated, not committed) |
| `SHOTLIST.md` | Beat-by-beat: start, part, duration, labels, constructed flag, picture |
| `FACTCHECK.md` | Every factual claim with its source (JS1, JS2, PR #30, PR #44, careery.pro review, …), unsigned |
| `PROMPTS.md` | "Generation prompts: none", plus the build commands |
| `BUILD-PROMPT.md` | The prompts I gave Claude Code, in order, and the exact rebuild commands |
| `SOURCES.md` | Tools and licences, sources, who made what |
| `FRICTIONAL.md` | Dated log of what went wrong and what was done |
| `brutalist-fixes.diff` | My local Windows fixes to the toolkit (font path in ffmpeg filters, review timecode position, `npx` on Windows), against Brutalist `3a6d397` |

## Gate reports

| Report | Gate | Result |
|---|---|---|
| `_qc/REPORT.md`, `_qc/contact_sheet.png` | Gate V, frame-level visual QC, run by `art final` on the master | 44 frames, 0 BLOCKER, 0 MAJOR (the sheet shows the first 16 sampled frames) |
| `qc-sheet.png` | Review contact sheet, one mid-frame per beat (all 22) | — |
| `TYPECHECK.md` | Gate T, type lock | PASS, 22 beats, 0 FAILs |
| `layout_audit.md`, `layout_audit.json` | Gate B, Manim layout audit (holds the **last** scenes audited, B02 and B04; every scene passed before its clip was slotted) | clean |
| `final-project-film-nishant-u.verified.json` | Render-integrity | `status: ready` |

Also passed in `art run` (terminal output only): build_safety, Gate F (paperwork), Gate L (beat mix),
Gate SHAPE (not a finance reel), Gate A (static pre-check, 22/22 clean), Gate W (contrast and margins;
it skips `BEND_Close` by name, and a renamed copy was clean). `factcheck_check.py` (optional, not part of
`art run`/`art final`) reports every row as unresolved until I sign off.

## Rebuild

See [BUILD-PROMPT.md](BUILD-PROMPT.md) for the exact commands, from a fresh Brutalist checkout at
`3a6d397`: apply `brutalist-fixes.diff`, set `PYTHONUTF8=1` and `PHONEMIZER_ESPEAK_LIBRARY`, put Manim
on PATH, then `make_sheet.py`, Kokoro audio, `pad_bend.py`, `art run` and `art final`. Everything is free
and local: no API keys, no paid generation, no uploads.
