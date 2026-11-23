#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for final-project-film-nishant-u (INFO 7375 Final Project Film).

Show-tell format (brutalist.art skills/make/show-tell/, schema as in my pitch film's make_sheet.py)
without the persona: Nishant narrates in the first person, Kokoro am_michael throughout; no Liam/Bear
greeting, no channel, no hesitant-writer or terms bookends, no BHTF Your Turn, no BOUT
(ClaudeTitleOutro hard-codes @NikBearBrown). Every beat is one isometric Manim drawing; the film
closes on a drawn beat, BEND.

Narration is EXACTLY Nishant's script (SCRIPT below), split into beats. Revised by Nishant on
2026-11-23 before the final render: "a person will approve every step" and "will say \"insufficient\""
(future tense: neither is built yet). The script asserts that the
beats, joined with single spaces, reproduce SCRIPT character for character. The only voice-only
spelling is "Nee-shaant", which is already in the script; on-screen text and every written file say
"Nishant".

Four parts, in order: Executive summary, Introduction, Methods, Evaluation. The first beat of each
part carries the part's name as an on-screen label. A picture of anything not yet built (the
insufficient label, the filter and shortlist, the tool server, the planner and memory, the human
gate, the final-project evaluation plan) carries an on-screen "constructed" label.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "final-project-film-nishant-u"
TITLE = "A job-search agent that shows its evidence"
VOICE = "am_michael"

SCRIPT = """\
Hi, I'm Nee-shaant. I'm building a job-search agent for international data and machine-learning graduates. It watches public job boards at e-commerce companies, picks out the new postings that fit one fictional graduate, Priya Nair, and shows the exact line of evidence behind every verdict. It never applies or messages anyone, and a person will approve every step. Why it matters: graduates on a visa clock lose hours reading postings that turn out to be a bad fit, or that never mention sponsorship. This agent does that reading for them, and will say "insufficient" instead of guessing.

What already exists? LinkedIn Job Alerts email new postings that match a saved search, but never say why a job fits. Jobright adds a match score and an H-1B filter, but a 2026 review said that filter relies on sponsorship language or a company's past sponsorship, which doesn't guarantee this job will sponsor. My instructor's collector, Lectern, reads public boards across three job systems, and the Reallocation Engine maps sponsorship history from public records. What's missing is a verdict on each posting that cites the posting itself, and an agent that's honest when it can't tell. That's why mine is worth building.

The data is public: the job boards of Faire, Instacart and Poshmark on Greenhouse and Ashby, plus a fictional résumé. No real personal data. Step one, already built: a watch that saves every raw response and reports only new postings. Each posting gets two verdicts: a rule anyone can recompute, and Claude's judgment in a fixed format that a validator checks. Step two, also built: a bounded loop over five boards, with budgets, an exit status, and a permission policy enforced in code. Allowed hosts only, and writes only inside its own folder. Next comes a filter with an evidence-checked shortlist, a small tool server so Claude can call the agent, then a planner with memory, and a human approval gate. What I need: Python's standard library, my laptop, and my Claude Code login. The judge calls run there, with no API key and no paid compute.

How will I know it works? First, against my own labels. I hand-labeled twenty postings, kept ten sealed, and ran the prompt on them once: ten out of ten, but the 95 percent interval runs from 69 to 100 percent, so ten cases can't prove much. Second, with checks that don't trust the agent. In one live run, the loop said "finished, zero new" for an empty board, and an independent check of the raw responses caught it. For the final project I'll use a larger held-out set with harder, borderline postings, at least five deliberate failure cases, a failure I predict and trigger on purpose, and a stranger running it from the README. It works if it agrees with my labels on postings it hasn't seen, abstains instead of guessing, and every failure is caught by something other than the agent's own report. I'm Nee-shaant.
"""

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, "
                 "with the voice carrying the explanation. Only underfill and clustered are waived; "
                 "edge-bleed and contrast still apply.")

PARTS = ["Executive summary", "Introduction", "Methods", "Evaluation"]

# (beat id, scene class, part, narration, labels, constructed, visual intent, show events)
BEATS = [
 # ── Executive summary ──────────────────────────────────────────────────────────────────────
 ("B00", "B00_Summary", 0,
  "Hi, I'm Nee-shaant. I'm building a job-search agent for international data and machine-learning graduates.",
  ["Executive summary", "job-search agent"], False,
  "The dark agent block lands on a plinth; a kraft résumé page drops in beside it.",
  [{"at": 0.2, "event": "agent block lands"}, {"at": 0.7, "event": "résumé page drops in"}]),
 ("B01", "B01_Watches", 0,
  "It watches public job boards at e-commerce companies, picks out the new postings that fit one fictional graduate, Priya Nair, and shows the exact line of evidence behind every verdict.",
  ["job boards", "evidence"], False,
  "Two board stacks feed a posting page along a belt to the agent block; on a large posting page a quote "
  "bracket draws around one line and a check lands.",
  [{"at": 0.15, "event": "board lights turn on"}, {"at": 0.4, "event": "page rides the belt"},
   {"at": 0.75, "event": "quote bracket + check on one line"}]),
 ("B02", "B02_NeverApplies", 0,
  "It never applies or messages anyone, and a person will approve every step.",
  ["never applies", "human gate", "constructed"], True,
  "A send arrow and an envelope are struck through; a gate swings shut across a path, with a check above it.",
  [{"at": 0.2, "event": "send arrow + envelope struck through"}, {"at": 0.7, "event": "gate draws, check lands"}]),
 ("B03", "B03_VisaClock", 0,
  "Why it matters: graduates on a visa clock lose hours reading postings that turn out to be a bad fit, or that never mention sponsorship.",
  ["visa clock", "bad fit"], False,
  "A large clock face whose hand sweeps; posting pages pile up beside it and get crossed out.",
  [{"at": 0.2, "event": "clock hand sweeps"}, {"at": 0.5, "event": "pages pile up"},
   {"at": 0.8, "event": "pages crossed out"}]),
 ("B04", "B04_Insufficient", 0,
  "This agent does that reading for them, and will say \"insufficient\" instead of guessing.",
  ["insufficient", "constructed"], True,
  "A posting page with a blank stretch; a tall check starts to grow over it and is replaced by an open ring.",
  [{"at": 0.25, "event": "blank posting"}, {"at": 0.75, "event": "open ring replaces the check"}]),
 # ── Introduction ───────────────────────────────────────────────────────────────────────────
 ("B05", "B05_Alerts", 1,
  "What already exists? LinkedIn Job Alerts email new postings that match a saved search, but never say why a job fits.",
  ["Introduction", "LinkedIn Job Alerts", "why?"], False,
  "A generic envelope shape (no logo) drops posting pages onto the stage; a blank tag appears beside each.",
  [{"at": 0.3, "event": "postings slide out"}, {"at": 0.8, "event": "blank tags appear"}]),
 ("B06", "B06_Jobright", 1,
  "Jobright adds a match score and an H-1B filter, but a 2026 review said that filter relies on sponsorship language or a company's past sponsorship, which doesn't guarantee this job will sponsor.",
  ["Jobright", "careery.pro review, 2026"], False,
  "A generic dial-and-funnel machine (no logo): a needle swings (score), pages pass a funnel (filter); a "
  "history ledger feeds the funnel from behind.",
  [{"at": 0.15, "event": "needle swings"}, {"at": 0.4, "event": "pages pass the funnel"},
   {"at": 0.7, "event": "history ledger feeds the funnel"}]),
 ("B07", "B07_Lectern", 1,
  "My instructor's collector, Lectern, reads public boards across three job systems, and the Reallocation Engine maps sponsorship history from public records.",
  ["Lectern", "Reallocation Engine"], False,
  "Three board stacks in a row light up and feed an open collector box; on the right a records ledger "
  "draws dots on a small map grid.",
  [{"at": 0.2, "event": "three boards light"}, {"at": 0.45, "event": "pages into the collector"},
   {"at": 0.8, "event": "ledger dots appear"}]),
 ("B08", "B08_Missing", 1,
  "What's missing is a verdict on each posting that cites the posting itself, and an agent that's honest when it can't tell. That's why mine is worth building.",
  ["cites the posting", "can't tell", "constructed"], True,
  "One posting page: a quote bracket and check on one line, an open ring on a blank stretch; the agent "
  "block lands beside it.",
  [{"at": 0.2, "event": "quote bracket + check"}, {"at": 0.55, "event": "open ring"},
   {"at": 0.85, "event": "agent block lands"}]),
 # ── Methods ────────────────────────────────────────────────────────────────────────────────
 ("B09", "B09_Data", 2,
  "The data is public: the job boards of Faire, Instacart and Poshmark on Greenhouse and Ashby, plus a fictional résumé. No real personal data.",
  ["Methods", "public boards", "fictional résumé"], False,
  "Three board stacks light one by one; a kraft résumé page drops in; an ID card (no real personal "
  "data) is struck through.",
  [{"at": 0.2, "event": "three boards light"}, {"at": 0.65, "event": "résumé drops in"},
   {"at": 0.85, "event": "ID card struck through"}]),
 ("B10", "B10_Watch", 2,
  "Step one, already built: a watch that saves every raw response and reports only new postings.",
  ["watch", "raw responses"], False,
  "A board stack sends a raw page into a growing stack of saved pages; only one marked page slides out.",
  [{"at": 0.3, "event": "raw page into the saved stack"}, {"at": 0.75, "event": "only the new page slides out"}]),
 ("B11", "B11_TwoVerdicts", 2,
  "Each posting gets two verdicts: a rule anyone can recompute, and Claude's judgment in a fixed format that a validator checks.",
  ["rule", "judgment", "validator"], False,
  "A posting page; on the left a rule sheet gets a check; on the right a judgment card passes through a "
  "validator gate and gets a check.",
  [{"at": 0.3, "event": "rule check"}, {"at": 0.7, "event": "judgment through the validator"}]),
 ("B12", "B12_Loop", 2,
  "Step two, also built: a bounded loop over five boards, with budgets, an exit status, and a permission policy enforced in code. Allowed hosts only, and writes only inside its own folder.",
  ["loop", "budget", "policy"], False,
  "The agent block laps a loop track while a budget meter drains; an exit bar lifts; a padlock lands on a "
  "port; a page drops inside an open folder box.",
  [{"at": 0.2, "event": "block laps, meter drains"}, {"at": 0.55, "event": "exit bar lifts"},
   {"at": 0.8, "event": "padlock + page into the folder box"}]),
 ("B13", "B13_NextTools", 2,
  "Next comes a filter with an evidence-checked shortlist, a small tool server so Claude can call the agent,",
  ["shortlist", "tool server", "constructed"], True,
  "A funnel drops pages into a shortlist tray, each with a check; a small dark server with a plug cable "
  "draws to the agent block.",
  [{"at": 0.25, "event": "pages into the shortlist tray"}, {"at": 0.75, "event": "tool server cable draws"}]),
 ("B14", "B14_NextPlanner", 2,
  "then a planner with memory, and a human approval gate.",
  ["planner", "human gate", "constructed"], True,
  "A planner sheet with step boxes and a memory drawer; a gate with a check closes the path.",
  [{"at": 0.25, "event": "planner steps tick"}, {"at": 0.75, "event": "gate + check"}]),
 ("B15", "B15_Needs", 2,
  "What I need: Python's standard library, my laptop, and my Claude Code login. The judge calls run there, with no API key and no paid compute.",
  ["laptop", "no API key"], False,
  "A laptop lands; a code page and a terminal prompt appear; a key and a coin are struck through.",
  [{"at": 0.2, "event": "laptop lands"}, {"at": 0.5, "event": "prompt types"},
   {"at": 0.8, "event": "key and coin struck through"}]),
 # ── Evaluation ─────────────────────────────────────────────────────────────────────────────
 ("B16", "B16_Labels", 3,
  "How will I know it works? First, against my own labels. I hand-labeled twenty postings, kept ten sealed, and ran the prompt on them once: ten out of ten,",
  ["Evaluation", "sealed", "10/10"], False,
  "Twenty small cards in two rows; ten slide into a taped box (sealed); ten checks land.",
  [{"at": 0.25, "event": "twenty cards"}, {"at": 0.55, "event": "ten into the sealed box"},
   {"at": 0.85, "event": "ten checks"}]),
 ("B17", "B17_Interval", 3,
  "but the 95 percent interval runs from 69 to 100 percent, so ten cases can't prove much.",
  ["95% interval", "69–100%"], False,
  "A horizontal 0–100 scale; a bracket grows from 69 to 100 with a dot at 100.",
  [{"at": 0.3, "event": "scale draws"}, {"at": 0.75, "event": "interval bracket grows"}]),
 ("B18", "B18_Check", 3,
  "Second, with checks that don't trust the agent. In one live run, the loop said \"finished, zero new\" for an empty board, and an independent check of the raw responses caught it.",
  ["finished, 0 new", "independent check"], False,
  "The agent block shows a tag (finished, 0 new) beside an empty board; a separate magnifier passes over "
  "the saved raw page and a cross lands on the tag.",
  [{"at": 0.3, "event": "tag beside the empty board"}, {"at": 0.65, "event": "magnifier over the raw page"},
   {"at": 0.85, "event": "cross on the tag"}]),
 ("B19", "B19_Plan", 3,
  "For the final project I'll use a larger held-out set with harder, borderline postings, at least five deliberate failure cases, a failure I predict and trigger on purpose, and a stranger running it from the README.",
  ["held-out set", "5 failures", "constructed"], True,
  "A larger held-out stack; an evaluation sheet with five marked failure rows; one ink cross on the "
  "predicted row; a cursor on a README page.",
  [{"at": 0.2, "event": "held-out stack"}, {"at": 0.45, "event": "five failure rows"},
   {"at": 0.7, "event": "predicted row crossed"}, {"at": 0.9, "event": "cursor on the README"}]),
 ("B20", "B20_WorksIf", 3,
  "It works if it agrees with my labels on postings it hasn't seen, abstains instead of guessing, and every failure is caught by something other than the agent's own report.",
  ["agrees", "abstains", "constructed"], True,
  "Three criteria: a check beside a label card, an open ring, and a separate checker block catching a "
  "cross that the agent's report missed.",
  [{"at": 0.25, "event": "agrees: check"}, {"at": 0.55, "event": "abstains: ring"},
   {"at": 0.85, "event": "outside check catches the failure"}]),
 ("BEND", "BEND_Close", 3,
  "I'm Nee-shaant.",
  ["Nishant U", "Job-search agent"], False,
  "The agent block from B00 sits on its plinth; the name and working title land beside it.",
  [{"at": 0.2, "event": "agent block on plinth"}, {"at": 0.4, "event": "name and title land"}]),
]

# ── checks: verbatim script, part order, labels, constructed flags ────────────────────────────
joined = " ".join(b[3] for b in BEATS)
assert joined == " ".join(p.strip() for p in SCRIPT.strip().split("\n\n")), "beats do not reproduce SCRIPT verbatim"
paras = [p.strip() for p in SCRIPT.strip().split("\n\n")]
for i, para in enumerate(paras):
    assert " ".join(b[3] for b in BEATS if b[2] == i) == para, f"part {PARTS[i]} does not match paragraph {i + 1}"
for i, part in enumerate(PARTS):
    first = next(b for b in BEATS if b[2] == i)
    assert part in first[4], f"{first[0]}: first beat of {part} must carry the label"
for b in BEATS:
    assert 1 <= len(b[4]) <= 3, f"{b[0]}: 1-3 labels per beat"
    assert ("constructed" in b[4]) == b[5], f"{b[0]}: constructed flag and label disagree"
    assert b[1].startswith(b[0] + "_"), f"{b[0]}: class name must start with the beat id"


def est(text):
    return round(len(text.split()) / 2.5, 1)


def beat(bid, cls, part, text, labels, constructed, image, show):
    return {"beat_id": bid, "act": PARTS[part], "lane": "manim", "proof_gate": "SHOW",
            "narration_text": text, "estimated_duration_s": est(text),
            "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                     "manim": {"class": cls}, "motion_claim": image,
                     "labels": labels, "constructed": constructed},
            "qc": {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}}


B = [beat(*row) for row in BEATS]

# Carry measured audio forward, or `art run` refuses with "missing required audio" (show-tell gate
# trap 4). Only while the narration is unchanged: an edited line needs a re-voice
# (generate_audio_kokoro.py --only <BID>) before its old duration means anything.
old = {}
if (HERE / "beat_sheet.json").exists():
    old = {b["beat_id"]: b for b in json.loads((HERE / "beat_sheet.json").read_text(encoding="utf-8"))["beats"]}
for b in B:
    o = old.get(b["beat_id"], {})
    if o.get("narration_text") == b["narration_text"] and o.get("actual_duration_s"):
        b["actual_duration_s"], b["audio_file"] = o["actual_duration_s"], o.get("audio_file")
        if o.get("tail_pad_s"):
            b["tail_pad_s"] = o["tail_pad_s"]
    elif o.get("actual_duration_s"):
        print(f"[sheet] {b['beat_id']}: narration changed — re-voice it before the next run")

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT FILM", "skill": "show-tell", "style_preset": "show-tell",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none",
    "parts": PARTS,
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("I narrate as myself (Nishant), so the persona bookends are dropped: no Liam/Bear "
                              "greeting, no composer cold open, no verdict card, no Your Turn. Every beat is a "
                              "drawing, so the hesitant-writer and terms cards are dropped too. The ClaudeTitleOutro "
                              "(BOUT) is also dropped because its handle is hard-coded to @NikBearBrown; the film "
                              "closes on a drawn Manim beat, BEND. bookend_check.py's outro check cannot be exempted "
                              "and will fail by design; art run and art final do not call it."),
    "audience": "INFO 7375 instructor and TAs; hiring managers for data and machine-learning roles",
    "source_doc": "Nishant's verbatim script (2026-11-23); facts in FACTCHECK.md",
    "author": "Nishant U",
    "tags": ["job-search agent", "Claude", "agent loop", "evaluation", "source grounding"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
words = len(joined.split())
print(len(B), "beats;", words, "words; est", round(sum(b["estimated_duration_s"] for b in B)), "s; verbatim check OK")
