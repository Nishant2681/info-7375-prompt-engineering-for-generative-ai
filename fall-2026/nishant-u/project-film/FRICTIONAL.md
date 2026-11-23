# FRICTIONAL — final-project-film-nishant-u

Dated log of what went wrong and what was done about it. Entries were drafted by Claude Code from the
session on 2026-11-23; "I" is Nishant where it says so. My own reflection is still to be added.

## 2026-11-23

**Branch.** `git fetch origin`, then `git switch --no-track -c nishant-u-project-film origin/main`
(`fc5b4b1`). My JS1, JS2 and pitch-film branches were not touched. The untracked
`fall-2026/nishant-u/js1-contract-and-watch/` copy in my working tree came along as untracked and is not
committed here.

**Brutalist pull.** `~/brutalist.art` had my three local edits uncommitted (`compile.py`,
`remotion_scenes.py`, `runtime/remotion/package-lock.json`). Claude Code saved the diff, stashed, pulled
(fast-forward `519fcbb` → `3a6d397`, 35 upstream commits), and popped the stash. The pop conflicted only
on `package-lock.json`, an npm side effect that is not one of my fixes, so it took upstream's lockfile.
My two code fixes re-applied unchanged (same hunks; only index hashes and line offsets differ). The
stash entry is still kept as a backup. The updated diff is `brutalist-fixes.diff` in this folder.

**Upstream changes that matter here.** (1) Gate V now also waives `empty-frame` on beats marked
`sparse_by_design` (upstream `final_frame_check.py`). That is the toolkit's change, not mine; my sheet's
waiver reason still names only underfill and clustered. (2) The toolkit pins Manim 0.20; I still have
0.18.1, the version my pitch film was built with. Not upgraded without asking me.

**Kokoro stopped on a new espeak path guard.** `setup_smoke_kokoro.py` exited: "espeak-ng's data path is
169 characters; the bundled library only accepts 159". The guard came with upstream `16fb263`, written
for macOS. The same 169-character path voiced my whole pitch film on 2026-10-14. Workaround, with no
toolkit edit: set `PHONEMIZER_ESPEAK_LIBRARY` to the bundled `espeak-ng.dll`
(`espeakng_loader.get_library_path()`), the override the guard itself honours. The smoke test then
passed: `kokoro synth OK — mean_volume -21.8 dB`, the same as for the pitch film. The setting is in
`BUILD-PROMPT.md`'s rebuild commands.

**Manim and ffmpeg.** Manim 0.18.1 rendered a test scene; ffmpeg/ffprobe 9.0.2 work. Building a contact
sheet with ffmpeg's `drawtext` crashed (segfault, no fontconfig on Windows), so the sheets were built with
PIL instead.

**`gh` is not installed.** PR #30 and PR #44 were looked up through GitHub's public API instead. Both are
open, not merged.

**Audio first.** All 22 beats voiced; total 197.82 s. BEND ("I'm Nee-shaant.") is only 1.28 s, so
`pad_bend.py` adds a 2.0 s silent tail (the skill does this for its closing beat): 199.82 s, 3:19.8.
That is inside my 2:00–3:55 band but under my 3:30–3:50 target. The narration is my script verbatim at
Kokoro's default speed, so it wasn't slowed down. Short beats: B14 3.37 s, BEND 3.28 s; B06 is 15.21 s.

**Check by ear: "Faire, Instacart".** A whisper (`base.en`) transcript of B09 heard "the job boards a fair
in Stackart and Poshmark". Espeak's phonemes for the line are right (`fˈɛɹ, ɪnstˈækɑːɹt`), so this may
be whisper's mistake and not Kokoro's. *Nishant to check by ear.* Everything else transcribed cleanly,
including "Nee-shaant", "H1B" and "read-me".

**Pre-render gates.** Gate A warned on B16: the tenth check mark sat at x ≈ 6.5, outside the safe area.
The row was tightened (0.5 apart). Gate W: all clean, but it skips `BEND_Close` because the name has no
digit. That is the same gap my pitch film had. As an extra check, W was run on a copy renamed
`B99_Close`: clean.

**Gate B stopped the first `art run`.** In strict mode, B05's "LinkedIn Job Alerts" label box reached
x = −6.35, 0.05 past the ±6.3 audit edge. The label moved 0.3 right and the three posting pages moved
right to keep clear. No gate was changed. The second run passed every gate (Gate V: 44 frames,
0 BLOCKER, 0 MAJOR).

**Tense: my script, caught by the fact-check.** My script said "a person approves every step" and "says
'insufficient' instead of guessing" in the present tense. Neither the human gate nor the "insufficient"
label is built yet. Claude Code's FACTCHECK draft flagged both rows. I changed them to "a person will
approve every step" and "will say 'insufficient'" before the final render. B02 and B04 were re-voiced
(5.01 s, 5.06 s; transcripts clean) and re-rendered; the B02 scene's timing cue moved to the new phrase.
New total: 200.31 s, 3:20.3.

**Final render.** The third `art run` re-rendered only B02 and B04 and passed every gate (Gate B clean on
both; Gate V 44 frames, 0 BLOCKER, 0 MAJOR). Claude Code looked at both contact sheets and found no
visual bug. `art final`: Gate T PASS (22 beats, 0 FAILs), 4K master
`final-project-film-nishant-u.mp4`, 200.75 s, render-integrity `ready`, and Gate V on the master,
44 frames, 0 BLOCKER, 0 MAJOR. The two SKIN LINT lines (no ClaudeComposerAsk cold open, no
ClaudeTitleOutro) are advisory and expected without the persona bookends. `verified.json` had absolute
local paths; my user folder was replaced with `~` before committing. `make_sheet.py` must not be re-run
now: it would wipe the build stamps in `beat_sheet.json` (show-tell skill note).

**Not checked.** I haven't watched the master yet. The FACTCHECK rows are unsigned. The careery.pro review
was not reopened. `scripts/validate_course.py` exits 1, but only on files outside my folder that are
already on `origin/main` (glossary deck links, other students' `.tsx`/`.ts` files).
