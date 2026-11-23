# SOURCES — final-project-film-nishant-u

## Tools and licences

Versions as installed on 2026-11-23. Licences as recorded in my pitch film's `SOURCES.md` (checked there
on 2026-10-14); not re-read today.

| Tool | Version used | Licence, as stated |
|---|---|---|
| Brutalist toolkit (`github.com/nikbearbrown/brutalist.art`) | commit `3a6d397` (pulled 2026-11-23), plus my `brutalist-fixes.diff` | No licence stated in the checkout |
| Kokoro: `kokoro-onnx` package | 0.6.1 | MIT License |
| Kokoro model files `kokoro-v1.0.onnx`, `voices-v1.0.bin` | v1.0 | Described by the toolkit as Apache-2.0; no licence file ships with them |
| Manim Community | 0.18.1 (the toolkit now pins 0.20; not upgraded) | MIT License |
| ManimPango | 0.5.0 | MIT License |
| ffmpeg / ffprobe (gyan.dev full build) | 9.0.2 | GPL v3 or later |
| EB Garamond font (toolkit copy) | static build | SIL Open Font License 1.1 |
| `faster-whisper`, Whisper `base.en` | 1.2.1 | MIT License. Used only to transcribe narration for a pronunciation check |

Remotion and Chrome are installed but no beat in this film uses Remotion.

## Sources of the film's facts

Full claim-by-claim mapping: `FACTCHECK.md`.

- **My JS1:** branch `nishant-u-js1`, final commit `d63ee48`, folder `fall-2026/nishant-u/js1-contract-and-watch/`;
  PR #30 (open, not merged on 2026-11-23).
- **My JS2:** branch `nishant-u-js2`, final commit `f956e22`, folder `fall-2026/nishant-u/js2-loop-tools-diff/`;
  PR #44 (open, not merged on 2026-11-23).
- **My pitch film:** branch `nishant-u-final-project-film`, folder `fall-2026/nishant-u/final-project-film/`
  (LinkedIn Job Alerts and Jobright as tools I used; the planned evaluation).
- **careery.pro review of Jobright (2026):** <https://careery.pro/blog/ai-job-search/jobright-ai-review>.
  A third-party review, credited on screen as "careery.pro review, 2026". Not opened in this session.
- **Lectern**, the instructor's collector: `fall-2026/nik-bear-brown/lectern/collect.py` on `origin/main`.
- **The Reallocation Engine:** <https://github.com/nikbearbrown/the-reallocation-engine>, and
  `assignments/assignment-reallocation-engine-recipe-design.md` on `origin/main`. The fictional persona
  Priya Nair: `search/examples/priya-nair/profile.yml` and `resume.example.json` (commit `d08afdd`).
- **Course assignments JS3–JS5** on `origin/main` (`assignments/`), for what comes next.

## Who made what

- **Nishant U:** the script, word for word; the four-part structure; the visual rules (one drawing per
  beat, 1–3 word labels, "constructed" labels, no logos, the careery.pro credit); the voice and the
  "Nee-shaant" spelling; JS1, JS2 and every result the film reports.
- **Claude Code (Claude Opus 5.5), 2026-11-23:** split the script into beats; wrote `make_sheet.py`,
  `pad_bend.py` and `scenes.py` (several scenes adapted from my pitch film's `scenes.py`); ran the audio,
  the gates and the renders; drafted `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md`, `BUILD-PROMPT.md`,
  this file, `FRICTIONAL.md` and `README.md`. All of these are drafts for me to review.
- No Claude responses appear in the film.
