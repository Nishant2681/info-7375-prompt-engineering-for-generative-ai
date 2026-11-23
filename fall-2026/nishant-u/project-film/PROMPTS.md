# PROMPTS — final-project-film-nishant-u

## Generation prompts: none

No AI image, video or voice-clone generation is used. No pantry assets, no Higgsfield, no API keys, no
paid calls. Narration is local Kokoro (`am_michael`), reading Nishant's script verbatim. Every visual is a
deterministic Manim scene in `scenes.py`. No logos are drawn. The prompts I gave Claude Code to build the
film are in `BUILD-PROMPT.md`.

## Build commands (free, local)

```bash
python make_sheet.py                                                     # beat sheet from the verbatim script
python ~/brutalist.art/runtime/scripts/generate_audio_kokoro.py <this folder>   # narration
python pad_bend.py                                                       # 2.0 s silent tail on BEND
cd ~/brutalist.art
PYTHONUTF8=1 ./art run   <this folder>                                   # Gates F, L, A, W, B, V; review cut
PYTHONUTF8=1 ./art final <this folder> --out <this folder>               # Gate T, then the 4K master
```

Scene classes: B00_Summary · B01_Watches · B02_NeverApplies · B03_VisaClock · B04_Insufficient ·
B05_Alerts · B06_Jobright · B07_Lectern · B08_Missing · B09_Data · B10_Watch · B11_TwoVerdicts ·
B12_Loop · B13_NextTools · B14_NextPlanner · B15_Needs · B16_Labels · B17_Interval · B18_Check ·
B19_Plan · B20_WorksIf · BEND_Close.
