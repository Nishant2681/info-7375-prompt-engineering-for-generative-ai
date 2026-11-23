# BUILD-PROMPT — final-project-film-nishant-u

The prompts I gave Claude Code on 2026-11-23, in order, then the exact commands that rebuild the film.
Local paths are written with `~` (my home folder).

## Prompts

### 1. The build request

> I'm making the INFO 7375 "Final Project Film" (25 pts, due Monday 11:30 PM; no length limit stated, so
> I'm using my pitch film's 2–4 minutes, target 3:30–3:50). Four parts in order: Executive summary,
> Introduction, Methods, Evaluation. Use my Brutalist setup at ~/brutalist.art exactly as for my pitch film
> (branch nishant-u-final-project-film, folder fall-2026/nishant-u/final-project-film/): show-tell format
> without the persona, Kokoro voice am_michael, my name spelled "Nee-shaant" for the voice only, no
> BHTF/BOUT, closing BEND beat, my Windows fixes (see final-project-film/brutalist-fixes.diff).
>
> 1. Print today's date. Git: fetch origin, create branch nishant-u-project-film from origin/main with
>    --no-track, folder fall-2026/nishant-u/project-film/. Don't touch my JS1, JS2 or pitch-film branches.
> 2. Brutalist: git status and pull in ~/brutalist.art without discarding my local fixes (stash and
>    re-apply if needed); confirm ffmpeg, Kokoro and Manim work. Log anything that breaks.
> 3. Write beat_sheet.json (via a make_sheet.py, as before). Narration is EXACTLY the script below, split
>    into beats of about 5–15 s each, grouped in order under the four parts. Each part starts with a beat
>    whose on-screen label names the part ("Executive summary", "Introduction", "Methods", "Evaluation").
>    Pictures: one simple isometric drawing per beat, labels of 1–3 words, at most 3 per beat. Any picture
>    of something not yet built (filter/shortlist, tool server, planner and memory, human gate, the
>    final-project evaluation plan) must carry an on-screen "constructed" label. Don't draw LinkedIn,
>    Jobright or other logos; use generic shapes with text names. On the Jobright beat add a small
>    "careery.pro review, 2026" label.
> 4. Generate the audio first. If the total is between 2:00 and 3:55, continue; if not, stop and show me
>    per-beat durations.
> 5. Write manim scenes, run the pre-render gates, art run, then art final into the project-film folder,
>    fixing scenes (never weakening gates) when something fails. Look at the contact sheets yourself for
>    visual bugs.
> 6. Create FACTCHECK.md (every factual claim with its source: JS1 commits and files in nishant-u-js1, JS2
>    commits and files in nishant-u-js2, PR #30 and #44, the careery.pro review; mark each "unverified —
>    Nishant to sign off"), SHOTLIST.md, PROMPTS.md, BUILD-PROMPT.md, SOURCES.md, FRICTIONAL.md (dated
>    entries), and a README.md (what this is, runtime, how to rebuild).
> 7. Commit in logical steps with author and committer Nishant U
>    <70760845+Nishant2681@users.noreply.github.com>. Don't push. Report the final mp4 path, the runtime,
>    every gate's pass/fail, the contact-sheet paths, and the commits.
>
> SCRIPT (verbatim): […the full script, as it now appears in `make_sheet.py` `SCRIPT`…]

### 2. After a dropped connection

> The connection dropped mid-response. Continue from where you stopped: all 22 scenes passed Gates A and
> W, and you were writing FACTCHECK.md, SHOTLIST.md and PROMPTS.md.
>
> One correction: the résumé JSON has no visa field, but Priya Nair's
> ~/the-reallocation-engine/search/examples/priya-nair/profile.yml does (visa.current_status F-1 OPT,
> unemployment days used and ceiling). Cite that as the source for "international graduate" in
> FACTCHECK, and don't flag it as unsupported.
>
> First run git status and list which files exist in project-film/, so we know nothing was half-written.
> Then finish steps 5–7 of my original request (art run, art final, docs, commits) and report as asked.

## Rebuild commands

Tested on Windows 11 with Git Bash, Python 3.12.10, Manim Community 0.18.1, ffmpeg 9.0.2. Everything is
free and local: no API keys, no paid calls, no uploads.

```bash
# 1. Brutalist toolkit at the commit this film was built on, plus my local fixes
git clone https://github.com/nikbearbrown/brutalist.art ~/brutalist.art
cd ~/brutalist.art
git checkout 3a6d397
git apply ~/info-7375-prompt-engineering-for-generative-ai/fall-2026/nishant-u/project-film/brutalist-fixes.diff
./setup --install            # Python packages, Remotion node_modules, the free Kokoro model

# 2. Environment for every command below
export PYTHONUTF8=1
export PATH="$(python3 -c 'import sysconfig; print(sysconfig.get_path("scripts", "nt_user"))'):$PATH"
# Kokoro's new espeak path-length guard (upstream 16fb263) stops on this machine's 169-character data
# path; pin the bundled library explicitly (the guard's own override), as the pitch film effectively did:
export PHONEMIZER_ESPEAK_LIBRARY="$(python3 -c 'import espeakng_loader; print(espeakng_loader.get_library_path())')"
F=~/info-7375-prompt-engineering-for-generative-ai/fall-2026/nishant-u/project-film

# 3. Beat sheet (the verbatim script lives in make_sheet.py SCRIPT)
cd "$F" && python3 make_sheet.py

# 4. Narration: Kokoro am_michael, local; then the 2.0 s silent tail on BEND
python3 ~/brutalist.art/runtime/scripts/generate_audio_kokoro.py "$F"
python3 pad_bend.py

# 5. Review cut: Gates build_safety, F, L, A, W, B, then compile and Gate V
cd ~/brutalist.art && ./art run "$F"

# 6. Clean 4K master into the film folder: Gate T, then encode, render-integrity, Gate V, .verified.json
./art final "$F" --out "$F"
```

Notes:
- `art run` renders only beats whose `manim/<BID>.mp4` is missing; after editing a scene, move its clip
  and `media/videos/` aside before re-running.
- Optional: `python3 ~/brutalist.art/runtime/qc/factcheck_check.py "$F"`. Until I sign off, it reports
  every "unverified" row as a blocker. That is expected; it is not part of `art run` or `art final`.
