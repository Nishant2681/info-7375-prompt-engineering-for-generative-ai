"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills,
and a WRITING KIT (quill, inkwell, paper, scribble lines, branching outline + the write_lines /
grow_tree animations that make the quill write). A PERSON IS NEVER AN ICON: `professor_bear(ratio, …)`
places a random Professor Bear portrait of the right aspect ratio (PROFESSOR BEAR LAW).
Pacing helpers read the reel's beat_sheet.json so scenes wait for their spoken phrase.

Every rule in ../SKILL.md "DRAWING LAWS" is already obeyed by these primitives; keep it that
way when you add one (label beside, never inside; terracotta never under text; dim greys
with gaps for chart blocks; type floor 32).
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ WRITING KIT (quill, ink, paper, scribble) ═════════════════════════════
# Added 2026-10-07 from Bear's two reference drawings: a quill drawing a branching outline on a
# scroll, and three scattered pages of scribbled handwriting with a quill. Use when a beat is
# about writing, drafting, authorship, notes, a manuscript, a log, a letter, a signature.
# Terracotta here is only the ink drop and the outline's nodes (dots) — never the lines.


def quill(x, y, s=1.0, angle=0.0, color=INK, fill=BOX_TOP):
    """A drawn quill with its NIB at (x, y); the feather points up-right. `g.nib` is the nib point.
    Kraft-filled feather, ink outline, a shaft line and one barb. Rotate with `angle` (radians)."""
    o = np.array([x, y, 0.0])
    def P(u, v):  # icon units (0..1) → scene, nib at origin, tip at (1, 1.1)·s
        return o + np.array([u * s, v * s, 0.0])
    body = VMobject(fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)
    body.set_points_smoothly([P(0.00, 0.00), P(0.12, 0.62), P(0.55, 1.02), P(1.00, 1.10),
                              P(0.95, 0.68), P(0.62, 0.22), P(0.00, 0.00)])
    shaft = Line(P(0.02, 0.02), P(0.98, 1.06), color=color, stroke_width=3)
    barb = Line(P(0.46, 0.50), P(0.40, 0.72), color=color, stroke_width=2.5)
    g = VGroup(body, shaft, barb)
    if angle:
        g.rotate(angle, about_point=o)
    g.nib = o.copy()
    return g


def inkwell(iso, x0=0.0, y0=0.0, z0=0.0, s=0.7):
    """A dark ink bottle (iso box + narrow neck) with one terracotta ink dot on the lid."""
    body = iso.box(x0, y0, z0, s, s, s * 0.9, DARK_TOP, DARK_L, DARK_R)
    neck = iso.box(x0 + s * 0.3, y0 + s * 0.3, z0 + s * 0.9, s * 0.4, s * 0.4, s * 0.25, DARK_TOP, DARK_L, DARK_R)
    drop = Dot(iso.p(x0 + s * 0.5, y0 + s * 0.5, z0 + s * 1.15), radius=0.07, color=TERRA)
    return VGroup(body, neck, drop)


def paper(x, y, w=2.4, h=3.0, tilt=0.0, fill=PAGE_TOP):
    """A flat 2-D sheet (the scattered-pages drawing): white page, ink outline, kraft drop shadow.
    `tilt` in radians. Returns a VGroup; `.sheet` is the page rectangle for placing lines on it."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    g = VGroup(shadow, sheet)
    if tilt:
        g.rotate(tilt, about_point=[x, y, 0])
    g.sheet = sheet
    g.cx, g.cy, g.w, g.h, g.tilt = float(x), float(y), float(w), float(h), float(tilt)   # read these; never ask the stub for vertices
    return g


def scribble(x, y, w, amp=0.07, waves=None, color=INK, sw=4):
    """One wavy handwriting line from (x, y) rightwards for `w` units. Reads as script, never as type."""
    n = waves or max(3, int(round(w * 3)))
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append([x + w * t, y + amp * np.sin(t * n * 2 * np.pi) * (0.6 + 0.4 * np.cos(t * 5.3)), 0])
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def scribble_block(x, y, w, n=3, gap=0.34, last=0.62, color=INK, sw=4):
    """`n` scribble lines stacked downward from (x, y); the last one is `last`× as long (a paragraph end)."""
    return VGroup(*[scribble(x, y - i * gap, w * (last if i == n - 1 else 1.0), color=color, sw=sw) for i in range(n)])


def scribbles_on(page, n=3, inset=0.3, gap=0.34, color=INK, sw=4):
    """Scribble lines laid on a `paper()` group, following its tilt (uses the page's stored geometry)."""
    w = page.w - 2 * inset
    g = scribble_block(page.cx - w / 2, page.cy + page.h / 2 - inset - 0.1, w, n=n, gap=gap, color=color, sw=sw)
    if abs(page.tilt) > 1e-3:
        g.rotate(page.tilt, about_point=[page.cx, page.cy, 0])
    return g


def outline_tree(x, y, h=1.6, levels=2, spread=0.55, color=INK, node=TERRA):
    """A branching outline (the scroll drawing): a trunk rising from (x, y), forking `levels` times,
    a terracotta dot at every tip. Returns VGroup(lines, dots) — draw lines first, dots last."""
    lines, dots = VGroup(), VGroup()
    def grow(px, py, length, lvl, dx):
        qx, qy = px + dx, py + length
        lines.add(Line([px, py, 0], [qx, qy, 0], color=color, stroke_width=4))
        if lvl == 0:
            dots.add(Dot([qx, qy, 0], radius=0.075, color=node))
            return
        for d in (-spread, spread):
            grow(qx, qy, length * 0.62, lvl - 1, d * (0.75 ** (levels - lvl)))
    grow(x, y, h * 0.42, levels, 0.0)
    g = VGroup(lines, dots)
    g.lines, g.dots = lines, dots
    return g


def write_lines(self, q, lines, speed=1.6, hop=0.22, dip=0.06):
    """Animate the quill `q` WRITING each line in `lines`: the nib hops to the line's start, then the
    line draws while the nib rides its tip (the writing motion). `speed` is scene units per second.
    Call between `until()` phrases so each line lands on its words. Works with the midpoint guard."""
    for ln in lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=hop, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        try:
            length = float(ln.get_arc_length())
        except Exception:          # Gate A's stub has no arc length; any positive number keeps the check moving
            length = 2.0
        rt = max(0.35, length / speed)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=rt, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
        # the small lift between lines keeps the quill from fusing with the ink at GATE T's midpoint
        q.shift([0, dip, 0]); q.nib = q.nib + np.array([0, dip, 0])


def grow_tree(self, q, tree, per=0.45):
    """Animate the quill drawing an `outline_tree`: each segment draws as the nib rides it; dots land last."""
    for ln in tree.lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=0.18, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=per, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
    self.play(LaggedStart(*[GrowFromCenter(d) for d in tree.dots], lag_ratio=0.15), run_time=0.6)


# ═════════════════════════════ PROFESSOR BEAR (a person is never an icon) ═════════════════════════════
# PROFESSOR BEAR LAW (Bear, 2026-10-07): when a beat needs an icon of a person, or Professor Bear himself,
# do not draw a person token and do not pull a person icon. Show one of the Professor Bear portraits in
# brutalist.art/professor-bear/, chosen at random among those of the right aspect ratio (1x1 · 2x3 · 16x9).
# `./art bear <ratio> --seed <beat>` picks the same way from the shell.
def _pb_dir():
    env = _os.environ.get("ART_HOME")
    cands = [env and _os.path.join(env, "professor-bear")]
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(8):
        cands.append(_os.path.join(here, "brutalist.art", "professor-bear"))
        cands.append(_os.path.join(here, "professor-bear"))
        here = _os.path.dirname(here)
    cands.append("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/professor-bear")
    for c in cands:
        if c and _os.path.isdir(c):
            return c
    return cands[-1]


_PB_RATIOS = {"1x1": (1.0, 287), "2x3": (2 / 3, 46), "16x9": (16 / 9, 13)}


def _pb_circle(path):
    """A circular cut (alpha outside the circle), cached beside the set in _crops/. Cropping is fine (Bear, 2026-10-07)."""
    from PIL import Image as _Im, ImageDraw as _Dr
    out_dir = _os.path.join(_os.path.dirname(path), "_crops"); _os.makedirs(out_dir, exist_ok=True)
    out = _os.path.join(out_dir, _os.path.splitext(_os.path.basename(path))[0] + "-circle.png")
    if not _os.path.exists(out):
        im = _Im.open(path).convert("RGBA"); w, h = im.size; s = min(w, h); top = max(0, (h - s) // 3)
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s))
        mask = _Im.new("L", (s, s), 0); _Dr.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
        im.putalpha(mask); im.save(out)
    return out


def professor_bear(ratio="2x3", height=3.0, seed=None, x=0.0, y=0.0, frame=True, shape="rect"):
    """A Professor Bear portrait (random within `ratio`; `seed` = the beat id for a stable pick across re-renders).
    Returns a Group: kraft drop shadow, the photo, an ink frame. Place with `x, y`; size with `height`.
    `shape="circle"` gives a round cut (use a 1x1 portrait). Cropping is fine: circle, rounded square, tight head shot."""
    import random as _random
    ar, n = _PB_RATIOS[ratio]
    k = _random.Random(str(seed) if seed is not None else None).randint(1, n)
    path = _os.path.join(_pb_dir(), f"professor-bear-{ratio}-{k:02d}.png")
    circle = shape == "circle"
    if circle:
        ar = 1.0
    w = height * ar
    if circle:
        shadow = Circle(radius=height / 2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Circle(radius=height / 2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    else:
        shadow = Rectangle(width=w, height=height, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Rectangle(width=w, height=height, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    try:
        img = ImageMobject(_pb_circle(path) if circle else path)
        img.height = height
        img.move_to([x, y, 0])
    except Exception:
        img = Rectangle(width=w, height=height, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = Group(shadow, img, border) if frame else Group(img)
    g.path = path
    return g


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)


# ═════════════════════════════ final-project-film-nishant-u ═════════════════════════════
# The film's own scenes, pasted after the kit. One isometric drawing per beat; labels and
# "constructed" flags follow beat_sheet.json exactly. Labels are on stage from the first frame;
# every move is held off the clip midpoint, where GATE T and Gate V sample. Helpers and several
# scenes are adapted from my pitch film (nishant-u-final-project-film, scenes.py).

# EB Garamond is not installed system-wide here: register the toolkit's copy for this process.
try:
    import manimpango as _mp
    _ART = _os.environ.get("ART_HOME") or _os.path.join(_os.path.expanduser("~"), "brutalist.art")
    _EBG = _os.path.join(_ART, "runtime", "fonts", "EB_Garamond", "static", "EBGaramond-Regular.ttf")
    if _os.path.exists(_EBG):
        _mp.register_font(_EBG)
except Exception:
    pass

KRAFT_DEEP = "#9C8462"   # connectors and belts: never ink, or they fuse with what they join (GATE T)


def _bid(scene):
    return type(scene).__name__.split("_")[0]


def go(scene, *anims, rt=0.8):
    """play(), held clear of the clip midpoint (GATE T / Gate V sample there)."""
    mid = _TARGET.get(_bid(scene), 10) / 2
    now = _elapsed(scene)
    if now < mid + 0.3 and now + rt > mid - 0.3:
        scene.wait(max(0.01, mid + 0.35 - now))
    scene.play(*anims, run_time=rt)


def done(scene):
    gap = _TARGET.get(_bid(scene), 10) - _elapsed(scene) - 0.10
    if gap > 0:
        scene.wait(gap)


def L(s, x, y, size=52):
    return T(s, size).move_to([x, y, 0])


def stamp():
    """The on-screen 'constructed' label: this part of the agent is not built yet."""
    return T("constructed", 44).move_to([4.6, 3.0, 0])


def sheet(x, y, w, h, fill=PAGE_TOP):
    return paper(x, y, w, h, 0.0, fill)


def lines_on(x, y, w, n, gap=0.36, color=GHOST, sw=5):
    return VGroup(*[Line([x, y - i * gap, 0], [x + w, y - i * gap, 0], color=color, stroke_width=sw) for i in range(n)])


def ring(x, y, r=0.3, color=INK):
    return Circle(radius=r, color=color, stroke_width=6).move_to([x, y, 0])


def xmark(x, y, s=0.22, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def strike(x, y, w=1.0, h=0.5):
    return Line([x - w, y - h, 0], [x + w, y + h, 0], color=INK, stroke_width=8)


def kpage(iso, x0=0.0, y0=0.0, z0=0.0, w=1.1, d=1.4):
    """A résumé page: kraft slab with dim lines (the skill page, but kraft, so it reads as a different paper)."""
    slab = iso.box(x0, y0, z0, w, d, 0.06, BOX_TOP, BOX_L, BOX_R, sw=2)
    zt = z0 + 0.06
    ln = VGroup(*[Line(iso.p(x0 + 0.2, y0 + d * f, zt), iso.p(x0 + w - 0.2, y0 + d * f, zt), color=DIM, stroke_width=4)
                  for f in (0.35, 0.6)])
    return VGroup(slab, ln)


def envelope(x, y, w=2.8, h=1.8):
    return VGroup(Rectangle(width=w, height=h, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0]),
                  Line([x - w / 2, y + h / 2, 0], [x, y - h / 12, 0], color=INK, stroke_width=4),
                  Line([x, y - h / 12, 0], [x + w / 2, y + h / 2, 0], color=INK, stroke_width=4))


def gate(x, y, w=1.0, h=1.7):
    """Two posts and a bar: the gate a send arrow can't pass, or a step waiting on approval."""
    return VGroup(Line([x, y, 0], [x, y + h, 0], color=INK, stroke_width=8),
                  Line([x + w, y, 0], [x + w, y + h, 0], color=INK, stroke_width=8),
                  Line([x, y + h * 0.82, 0], [x + w, y + h * 0.82, 0], color=INK, stroke_width=8))


def bracket(x, y, h=0.5):
    """A quote bracket around one line of a posting."""
    return VGroup(Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=INK, stroke_width=6),
                  Line([x, y - h / 2, 0], [x + 0.15, y - h / 2, 0], color=INK, stroke_width=6),
                  Line([x, y + h / 2, 0], [x + 0.15, y + h / 2, 0], color=INK, stroke_width=6))


def posting(x, y, w=3.4, h=4.6, rows=(0.38, 0.23, -0.36)):
    """A posting page with a few text rows (fractions of h above or below the centre) and a blank stretch."""
    return VGroup(sheet(x, y, w, h),
                  *[lines_on(x - w / 2 + 0.4, y + f * h, w - 0.8, 1, color=BAR1) for f in rows])


def laptop(x, y):
    screen = Rectangle(width=3.2, height=2.0, fill_color=DIM, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    base = Polygon([x - 1.7, y - 1.15, 0], [x + 1.7, y - 1.15, 0], [x + 2.1, y - 1.65, 0], [x - 2.0, y - 1.65, 0],
                   fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return screen, base


def ghost_box(iso, w=2.2, d=2.2, h=1.0):
    edges = (((0, 0, 0), (w, 0, 0)), ((0, 0, 0), (0, d, 0)), ((0, 0, 0), (0, 0, h)),
             ((w, 0, 0), (w, 0, h)), ((0, d, 0), (0, d, h)),
             ((0, 0, h), (w, 0, h)), ((0, 0, h), (0, d, h)),
             ((w, 0, h), (w, d, h)), ((0, d, h), (w, d, h)))
    return VGroup(*[DashedLine(iso.p(*a), iso.p(*b), color=DIM, stroke_width=5, dash_length=0.18) for a, b in edges])


# ──────────────────────────────── Executive summary ────────────────────────────────

class B00_Summary(Scene):
    def construct(self):
        iso = Iso(-1.2, -2.5, 0.9)
        plinth = iso.box(-0.2, -0.2, 0, 2.6, 2.6, 0.35)
        self.add(plinth, L("Executive summary", -3.0, 2.7, 60), L("job-search agent", 3.4, -2.5))
        self.wait(0.2)
        agent = iso.mcp(0.35, 0.35, 0.35, 1.5, 1.5, 0.9)
        target = np.array(agent.get_center(), dtype=float)
        agent.shift(UP * 1.6)
        until(self, "building")
        go(self, FadeIn(agent), rt=0.3)
        go(self, agent.animate.move_to(target), rt=0.6)
        go(self, FadeIn(Dot(iso.p(1.1, 1.1, 1.25), radius=0.1, color=TERRA)), rt=0.3)
        until(self, "international")
        resume = kpage(Iso(2.6, -0.6, 0.7))
        go(self, FadeIn(resume, shift=DOWN * 0.4), rt=0.6)
        done(self)


class B01_Watches(Scene):
    def construct(self):
        b1, l1 = Iso(-5.3, -0.2, 0.55).server(0, 0, 0)
        b2, l2 = Iso(-3.8, -1.8, 0.55).server(0, 0, 0)
        agent = Iso(-0.7, -1.6, 0.8).mcp(0, 0, 0, 1.4, 1.4, 0.8)
        post = posting(3.7, 0.3, 3.2, 4.2, rows=(0.36, 0.18, 0.0, -0.3))
        self.add(b1, l1, b2, l2, agent, post, L("job boards", -4.5, 1.9), L("evidence", 3.7, -2.75))
        self.wait(0.2)
        belt = Line([-3.0, -1.1, 0], [-1.6, -0.75, 0], color=KRAFT_DEEP, stroke_width=8)
        go(self, Create(belt), rt=0.5)
        until(self, "watches public job boards")
        go(self, *[d.animate.set_color(TERRA) for d in list(l1) + list(l2)], rt=0.5)
        until(self, "picks out")
        pg = Iso(-3.6, -1.1, 0.4).page(0, 0, 0)
        go(self, FadeIn(pg), rt=0.3)
        go(self, pg.animate.move_to([-1.6, -0.6, 0]), rt=0.9)
        self.remove(pg)
        until(self, "Priya Nair")
        go(self, FadeIn(kpage(Iso(0.6, 0.9, 0.5)), shift=DOWN * 0.3), rt=0.5)
        until(self, "exact line")
        y = 0.3 + 0.18 * 4.2
        go(self, Create(bracket(2.15, y)), rt=0.4)
        go(self, Create(check(5.6, y, 0.22)), rt=0.4)
        done(self)


class B02_NeverApplies(Scene):
    def construct(self):
        send = Arrow([-5.4, 1.2, 0], [-3.0, 1.2, 0], buff=0, color=INK, stroke_width=8)
        env = envelope(-4.2, -0.6, 2.0, 1.3)
        self.add(send, env, L("never applies", -4.2, -2.3), L("human gate", 3.0, -2.4), stamp())
        self.wait(0.2)
        go(self, Create(strike(-4.2, 1.2, 1.3, 0.55)), rt=0.35)
        go(self, Create(strike(-4.2, -0.6, 1.3, 0.65)), rt=0.35)
        path = Line([-1.4, -1.0, 0], [2.2, -1.0, 0], color=KRAFT_DEEP, stroke_width=8)
        go(self, Create(path), rt=0.4)
        until(self, "a person will approve")
        go(self, Create(gate(2.5, -1.6, 1.1, 1.9)), rt=0.5)
        go(self, Create(check(3.0, 1.0, 0.26)), rt=0.4)
        done(self)


class B03_VisaClock(Scene):
    def construct(self):
        c = np.array([-3.4, 0.4, 0.0])
        face = Circle(radius=1.6, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to(c)
        ticks = VGroup(*[Line(c + 1.3 * np.array([np.cos(a), np.sin(a), 0]), c + 1.5 * np.array([np.cos(a), np.sin(a), 0]),
                              color=DIM, stroke_width=5) for a in np.linspace(0, 2 * PI, 12, endpoint=False)])
        hand = Line(c, c + np.array([0.0, 1.15, 0]), color=INK, stroke_width=9)
        hub = Dot(c, radius=0.12, color=INK)
        self.add(face, ticks, hand, hub, L("visa clock", -3.4, -1.75), L("bad fit", 3.0, -2.7))
        self.wait(0.2)
        until(self, "visa clock")
        go(self, Rotate(hand, angle=-PI * 0.7, about_point=c), rt=0.9)
        until(self, "lose hours")
        xs = (1.2, 3.0, 4.8)
        for x in xs:
            go(self, FadeIn(VGroup(sheet(x, 0.4, 1.5, 2.0), lines_on(x - 0.45, 0.85, 0.9, 3, gap=0.34, color=BAR1)),
                            shift=DOWN * 0.3), rt=0.3)
        go(self, Rotate(hand, angle=-PI * 0.5, about_point=c), rt=0.6)
        until(self, "bad fit")
        go(self, Create(xmark(1.2, -1.0)), rt=0.3)
        go(self, Create(xmark(3.0, -1.0)), rt=0.3)
        until(self, "never mention sponsorship")
        go(self, Create(xmark(4.8, -1.0)), rt=0.3)
        done(self)


class B04_Insufficient(Scene):
    def construct(self):
        post = posting(-3.0, -0.1, 3.0, 4.0, rows=(0.36,))
        self.add(post, L("insufficient", 1.4, -0.1), stamp())
        self.wait(0.2)
        big = check(-3.2, 0.0, 0.7, w=12)
        go(self, Create(big), rt=0.5)
        until(self, "insufficient")
        self.remove(big)
        go(self, Create(ring(-3.0, -0.1, 0.6)), rt=0.5)
        done(self)


# ──────────────────────────────── Introduction ────────────────────────────────

class B05_Alerts(Scene):
    def construct(self):
        env = envelope(-4.2, 0.6)
        self.add(env, L("Introduction", -4.2, 2.75, 60), L("LinkedIn Job Alerts", -3.3, -1.0), L("why?", 4.3, 2.45))
        self.wait(0.2)
        until(self, "email new postings")
        xs = (0.6, 2.7, 4.8)
        for x in xs:
            p = VGroup(sheet(x, -0.6, 1.6, 2.0), lines_on(x - 0.5, -0.1, 1.0, 3, color=BAR1))
            target = np.array(p.get_center(), dtype=float)
            p.move_to([-4.2, 0.6, 0])
            go(self, FadeIn(p), rt=0.2)
            go(self, p.animate.move_to(target), rt=0.5)
        until(self, "never say why")
        for x in xs:
            go(self, GrowFromCenter(RoundedRectangle(width=0.9, height=0.45, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                                                     stroke_color=INK, stroke_width=4).move_to([x + 0.35, 1.05, 0])), rt=0.3)
        done(self)


class B06_Jobright(Scene):
    def construct(self):
        c = np.array([-3.6, 0.5, 0.0])
        dial = Circle(radius=1.25, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(c)
        ticks = VGroup(*[Line(c + 1.0 * np.array([np.cos(a), np.sin(a), 0]), c + 1.2 * np.array([np.cos(a), np.sin(a), 0]),
                              color=DIM, stroke_width=5) for a in np.linspace(PI * 0.15, PI * 0.85, 5)])
        needle = Line(c, c + np.array([-0.85, 0.35, 0]), color=INK, stroke_width=8)
        hub = Dot(c, radius=0.1, color=INK)
        funnel = Polygon([0.2, 1.6, 0], [3.0, 1.6, 0], [1.95, -0.3, 0], [1.25, -0.3, 0],
                         fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
        spout = Rectangle(width=0.7, height=0.6, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([1.6, -0.6, 0])
        self.add(dial, ticks, needle, hub, funnel, spout, L("Jobright", -3.6, -1.35),
                 L("careery.pro review, 2026", 1.8, -2.9, 40))
        self.wait(0.2)
        until(self, "a match score")
        go(self, Rotate(needle, angle=-1.6, about_point=c), rt=0.9)
        mark = Dot(c + 1.2 * np.array([np.cos(PI * 0.32), np.sin(PI * 0.32), 0]), radius=0.1, color=TERRA)
        go(self, FadeIn(mark), rt=0.3)
        until(self, "filter")
        for k in range(2):
            card = VGroup(sheet(1.6, 2.6, 0.9, 0.7), lines_on(1.35, 2.75, 0.5, 2, gap=0.25, color=BAR1))
            go(self, FadeIn(card), rt=0.2)
            go(self, card.animate.move_to([1.6, -1.6, 0]), rt=0.7)
            self.remove(card)
        out = VGroup(sheet(1.6, -1.7, 0.9, 0.7), lines_on(1.35, -1.55, 0.5, 2, gap=0.25, color=BAR1))
        go(self, FadeIn(out), rt=0.3)
        until(self, "past sponsorship")
        ledger = VGroup(sheet(4.9, 1.0, 1.7, 2.2), lines_on(4.3, 1.75, 1.2, 5, gap=0.32, color=BAR1))
        go(self, FadeIn(ledger, shift=LEFT * 0.4), rt=0.5)
        feed = Line([4.05, 0.6, 0], [2.75, 0.9, 0], color=KRAFT_DEEP, stroke_width=8)
        go(self, Create(feed), rt=0.5)
        until(self, "doesn't guarantee")
        go(self, Create(ring(4.9, -0.55, 0.28)), rt=0.4)
        done(self)


class B07_Lectern(Scene):
    def construct(self):
        stacks = [Iso(x, 0.7, 0.42).server(0, 0, 0, n=2) for x in (-5.3, -3.8, -2.3)]
        bk, fr = Iso(-3.8, -2.7, 0.75).open_box(0, 0, 0, 1.9, 1.9, 0.6)
        ledger = VGroup(sheet(3.6, 0.5, 3.2, 3.4), *[Line([2.3 + i * 0.65, -0.9, 0], [2.3 + i * 0.65, 1.9, 0], color=GHOST, stroke_width=4) for i in range(5)],
                        *[Line([2.2, -0.6 + j * 0.6, 0], [5.0, -0.6 + j * 0.6, 0], color=GHOST, stroke_width=4) for j in range(5)])
        self.add(*[s for s, _ in stacks], *[l for _, l in stacks], bk, fr, ledger,
                 L("Lectern", -0.6, -2.0), L("Reallocation Engine", 3.6, -1.85, 48))
        self.wait(0.2)
        until(self, "reads public boards")
        for _, lights in stacks:
            go(self, *[d.animate.set_color(TERRA) for d in lights], rt=0.3)
        until(self, "three job systems")
        for x in (-5.3, -3.8, -2.3):
            pg = Iso(x - 0.3, 0.5, 0.3).page(0, 0, 0)
            go(self, FadeIn(pg), rt=0.15)
            go(self, pg.animate.move_to([-3.8, -1.9, 0]), rt=0.45)
            self.remove(pg)
        go(self, FadeIn(VGroup(*[Iso(-3.8, -2.7, 0.75).page(0.3 + 0.35 * k, 0.4, 0.06 * k, 1.0, 1.2) for k in range(2)])), rt=0.3)
        until(self, "maps sponsorship history")
        for (i, j) in ((0, 3), (2, 1), (3, 4), (4, 2)):
            go(self, FadeIn(Dot([2.3 + i * 0.65, -0.6 + j * 0.6, 0], radius=0.11, color=TERRA)), rt=0.2)
        done(self)


class B08_Missing(Scene):
    def construct(self):
        post = posting(-3.2, 0.0, 3.4, 4.6, rows=(0.38, 0.23, -0.36))
        self.add(post, L("cites the posting", 2.5, 1.05), L("can't tell", 1.5, -0.45), stamp())
        self.wait(0.2)
        until(self, "cites the posting")
        go(self, Create(bracket(-4.75, 0.23 * 4.6 + 0.0)), rt=0.4)
        go(self, Create(check(-0.75, 1.05, 0.24)), rt=0.4)
        until(self, "can't tell")
        go(self, Create(ring(-0.6, -0.45)), rt=0.5)
        until(self, "worth building")
        agent = Iso(3.4, -3.0, 0.7).mcp(0, 0, 0, 1.4, 1.4, 0.8)
        go(self, FadeIn(agent, shift=DOWN * 0.4), rt=0.5)
        done(self)


# ──────────────────────────────── Methods ────────────────────────────────

class B09_Data(Scene):
    def construct(self):
        stacks = [Iso(x, -0.6, 0.5).server(0, 0, 0) for x in (-5.2, -3.5, -1.8)]
        self.add(*[s for s, _ in stacks], *[l for _, l in stacks], L("Methods", -4.6, 2.75, 60),
                 L("public boards", -3.5, -2.4), L("fictional résumé", 2.0, -1.9))
        self.wait(0.2)
        for (_, lights), phrase in zip(stacks, ("Faire", "Instacart", "Poshmark")):
            until(self, phrase)
            go(self, *[d.animate.set_color(TERRA) for d in lights], rt=0.3)
        until(self, "fictional résumé")
        go(self, FadeIn(kpage(Iso(1.9, -0.6, 0.75)), shift=DOWN * 0.4), rt=0.5)
        until(self, "No real personal data")
        card = VGroup(RoundedRectangle(width=2.2, height=1.4, corner_radius=0.15, fill_color=CARD, fill_opacity=1,
                                       stroke_color=INK, stroke_width=4).move_to([4.6, 1.0, 0]),
                      Circle(radius=0.3, stroke_color=BAR1, stroke_width=4).move_to([4.0, 1.1, 0]),
                      lines_on(4.5, 1.25, 0.8, 2, gap=0.3, color=BAR1))
        go(self, FadeIn(card), rt=0.3)
        go(self, Create(strike(4.6, 1.0, 1.35, 0.85)), rt=0.35)
        done(self)


class B10_Watch(Scene):
    def construct(self):
        board, lights = Iso(-4.8, -1.6, 0.65).server(0, 0, 0)
        si = Iso(-0.3, -2.3, 0.8)
        base = si.box(0, 0, 0, 1.4, 1.6, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=2)
        self.add(board, lights, base, L("watch", -4.8, 1.6), L("raw responses", -0.3, -2.85))
        self.wait(0.2)
        go(self, *[d.animate.set_color(TERRA) for d in lights], rt=0.3)
        until(self, "saves every raw response")
        for k in range(1, 4):
            slab = si.box(0, 0, 0.1 * k, 1.4, 1.6, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=2)
            go(self, FadeIn(slab, shift=DOWN * 0.3), rt=0.25)
        until(self, "only new postings")
        new = Iso(0.1, -1.3, 0.55).page(0, 0, 0)
        go(self, FadeIn(new), rt=0.2)
        go(self, new.animate.move_to([4.2, -0.2, 0]), rt=0.7)
        go(self, Create(check(4.4, 1.0, 0.26)), rt=0.3)
        done(self)


class B11_TwoVerdicts(Scene):
    def construct(self):
        post = VGroup(sheet(-0.4, 1.9, 2.0, 1.6), lines_on(-1.0, 2.2, 1.2, 3, gap=0.3, color=BAR1))
        rule = VGroup(sheet(-4.4, -0.5, 2.0, 2.4), lines_on(-5.0, 0.2, 1.2, 4, gap=0.36, color=BAR1))
        g = gate(2.6, -1.6, 1.1, 2.0)
        self.add(post, rule, g, L("rule", -4.4, -2.4), L("judgment", 0.0, -2.4), L("validator", 3.15, 1.0))
        self.wait(0.2)
        until(self, "a rule anyone")
        go(self, Create(check(-4.3, -1.35, 0.24)), rt=0.4)
        until(self, "Claude's judgment")
        card = VGroup(RoundedRectangle(width=1.6, height=1.1, corner_radius=0.12, fill_color=BOX_TOP, fill_opacity=1,
                                       stroke_color=BAR1, stroke_width=4).move_to([0.0, -0.8, 0]),
                      lines_on(-0.5, -0.6, 1.0, 2, gap=0.32, color=BAR1))
        go(self, FadeIn(card, shift=DOWN * 0.3), rt=0.4)
        until(self, "validator checks")
        go(self, card.animate.move_to([5.0, -0.8, 0]), rt=0.9)
        go(self, Create(check(5.0, 0.35, 0.24)), rt=0.4)
        done(self)


class B12_Loop(Scene):
    def construct(self):
        c = np.array([-2.2, -0.6, 0.0])
        track = Ellipse(width=5.6, height=2.6, color=KRAFT_DEEP, stroke_width=10).move_to(c)
        meter = Rectangle(width=0.8, height=2.8, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([5.3, -0.6, 0])
        segs = [Rectangle(width=0.6, height=0.55, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([5.3, -1.65 + i * 0.7, 0])
                for i in range(4)]
        hinge = np.array([1.4, 0.1, 0.0])
        bar = Line(hinge, hinge + np.array([0, -1.4, 0]), color=INK, stroke_width=9)
        post = Dot(hinge, radius=0.1, color=INK)
        port = Iso(-5.6, 1.6, 0.55).box(0, 0, 0, 0.9, 0.9, 0.6, GHOST, BOX_IN1, BOX_IN2, sw=4)
        fb, ff = Iso(2.7, 1.3, 0.6).open_box(0, 0, 0, 1.6, 1.6, 0.5)
        self.add(track, meter, *segs, bar, post, port, fb, ff,
                 L("loop", -2.2, -2.45), L("budget", 5.3, -2.55), L("policy", -2.6, 2.6))
        self.wait(0.2)
        block = Iso(0.0, 0.0, 0.42).mcp(0, 0, 0, 1.2, 1.2, 0.7)
        block.move_to(c + np.array([2.8, 0, 0]))
        until(self, "bounded loop")
        go(self, FadeIn(block), rt=0.3)
        path = Ellipse(width=5.6, height=2.6).move_to(c)
        until(self, "budgets")
        for k in range(2):
            go(self, MoveAlongPath(block, path), rt=1.4)
            self.remove(segs[-1 - k])
        until(self, "exit status")
        go(self, Rotate(bar, angle=PI / 2, about_point=hinge), rt=0.5)
        go(self, block.animate.move_to([2.6, -0.6, 0]), rt=0.6)
        until(self, "permission policy")
        lock = VGroup(Rectangle(width=0.7, height=0.55, fill_color=DARK_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-4.2, 2.0, 0]),
                      Arc(radius=0.24, start_angle=0, angle=PI, color=INK, stroke_width=7).move_to([-4.2, 2.4, 0]))
        go(self, FadeIn(lock, shift=DOWN * 0.3), rt=0.4)
        until(self, "writes only inside")
        pg = Iso(2.7, 1.3, 0.6).page(0.25, 0.25, 0.0, 1.1, 1.1)
        pg.set_z_index(1)
        pg.shift(UP * 1.0)
        go(self, FadeIn(pg), rt=0.2)
        go(self, pg.animate.shift(DOWN * 1.0), rt=0.5)
        done(self)


class B13_NextTools(Scene):
    def construct(self):
        funnel = Polygon([-5.6, 2.2, 0], [-3.4, 2.2, 0], [-4.2, 0.7, 0], [-4.8, 0.7, 0],
                         fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
        tb, tf = Iso(-4.5, -2.4, 0.75).open_box(0, 0, 0, 1.8, 1.8, 0.5)
        agent = Iso(2.4, -1.4, 0.8).mcp(0, 0, 0, 1.4, 1.4, 0.8)
        self.add(funnel, tb, tf, agent, L("shortlist", -1.6, -2.4), L("tool server", 3.0, -2.55), stamp())
        self.wait(0.2)
        for k in range(2):
            pg = VGroup(sheet(-4.5, 2.6, 0.9, 0.7), lines_on(-4.75, 2.75, 0.5, 2, gap=0.25, color=BAR1))
            go(self, FadeIn(pg), rt=0.15)
            go(self, pg.animate.move_to([-4.5, -1.5, 0]), rt=0.5)
            self.remove(pg)
        go(self, Create(check(-2.6, -0.2, 0.26)), rt=0.3)
        until(self, "tool server")
        server = Iso(-0.6, 0.6, 0.5).mcp(0, 0, 0, 1.0, 1.0, 0.6)
        go(self, FadeIn(server, shift=DOWN * 0.3), rt=0.3)
        cable = Line([0.25, 0.7, 0], [2.0, 0.0, 0], color=KRAFT_DEEP, stroke_width=8)
        go(self, Create(cable), rt=0.4)
        done(self)


class B14_NextPlanner(Scene):
    def construct(self):
        plan = sheet(-3.6, 0.3, 2.8, 3.4)
        boxes = [Square(side_length=0.34, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-4.5, 1.2 - i * 0.75, 0]) for i in range(3)]
        rows = [Line([-4.1, 1.2 - i * 0.75, 0], [-2.6, 1.2 - i * 0.75, 0], color=GHOST, stroke_width=5) for i in range(3)]
        drawer = Iso(-1.4, -2.4, 0.6).box(0, 0, 0, 1.4, 1.2, 0.7)
        self.add(plan, *boxes, *rows, drawer, L("planner", -3.6, -2.25), L("human gate", 3.2, -2.4), stamp())
        self.wait(0.1)
        for i in range(3):
            go(self, Create(check(-4.5, 1.2 - i * 0.75, 0.15, w=6)), rt=0.25)
        until(self, "human approval gate")
        go(self, Create(gate(2.7, -1.6, 1.1, 1.9)), rt=0.4)
        go(self, Create(check(3.2, 1.0, 0.26)), rt=0.3)
        done(self)


class B15_Needs(Scene):
    def construct(self):
        screen, base = laptop(-3.8, 0.8)
        code = VGroup(sheet(0.9, 1.2, 1.8, 2.2), lines_on(0.35, 1.8, 1.0, 4, gap=0.36, color=BAR1))
        self.add(screen, base, code, L("laptop", -3.8, -1.35), L("no API key", 3.8, -2.5))
        self.wait(0.2)
        until(self, "my laptop")
        prompt = VGroup(Line([-5.0, 1.25, 0], [-4.8, 1.1, 0], color=CARD, stroke_width=6),
                        Line([-4.8, 1.1, 0], [-5.0, 0.95, 0], color=CARD, stroke_width=6))
        go(self, Create(prompt), rt=0.3)
        until(self, "Claude Code login")
        go(self, Create(Line([-4.55, 1.1, 0], [-2.7, 1.1, 0], color=CARD, stroke_width=8)), rt=0.8)
        until(self, "no API key")
        key = VGroup(Circle(radius=0.34, stroke_color=INK, stroke_width=7).move_to([2.6, -0.8, 0]),
                     Line([2.94, -0.8, 0], [4.0, -0.8, 0], color=INK, stroke_width=7),
                     Line([3.7, -0.8, 0], [3.7, -1.1, 0], color=INK, stroke_width=7))
        go(self, FadeIn(key), rt=0.3)
        go(self, Create(strike(3.2, -0.8, 1.0, 0.45)), rt=0.3)
        until(self, "no paid compute")
        coin = VGroup(Circle(radius=0.5, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([5.1, 0.6, 0]),
                      Circle(radius=0.32, stroke_color=INK, stroke_width=4).move_to([5.1, 0.6, 0]))
        go(self, FadeIn(coin), rt=0.3)
        go(self, Create(strike(5.1, 0.6, 0.7, 0.55)), rt=0.3)
        done(self)


# ──────────────────────────────── Evaluation ────────────────────────────────

class B16_Labels(Scene):
    def construct(self):
        def card(x, y):
            return Rectangle(width=0.8, height=1.0, fill_color=PAGE_TOP, fill_opacity=1, stroke_color=BAR1, stroke_width=4).move_to([x, y, 0])
        top = VGroup(*[card(-5.4 + i * 1.2, 1.45) for i in range(10)])
        low = VGroup(*[card(-5.4 + i * 1.2, 0.15) for i in range(10)])
        bk, fr = Iso(-4.6, -3.0, 0.7).open_box(0, 0, 0, 2.0, 2.0, 0.7)
        self.add(top, low, bk, fr, L("Evaluation", -4.0, 2.75, 60), L("sealed", -1.4, -2.6), L("10/10", 4.0, -2.75))
        self.wait(0.2)
        until(self, "hand-labeled")
        go(self, *[Create(Line([x - 0.25, 1.65, 0], [x + 0.25, 1.65, 0], color=BAR1, stroke_width=4))
                   for x in [-5.4 + i * 1.2 for i in range(10)]], rt=0.4)
        until(self, "kept ten sealed")
        go(self, low.animate.scale(0.35).move_to([-4.6, -1.95, 0]), rt=0.6)
        self.remove(low)
        tape = Iso(-4.6, -3.0, 0.7).tape(0, 0, 0.7, 2.0, 2.0, drop=0.3, t=0.18)
        lid = Iso(-4.6, -3.0, 0.7).quad([(0, 0, 0.7), (2.0, 0, 0.7), (2.0, 2.0, 0.7), (0, 2.0, 0.7)], BOX_TOP)
        go(self, FadeIn(lid), rt=0.3)
        go(self, FadeIn(tape), rt=0.3)
        until(self, "ten out of ten")
        go(self, *[Create(check(0.8 + i * 0.5, -1.65, 0.14, w=6)) for i in range(10)], rt=0.5)
        done(self)


class B17_Interval(Scene):
    def construct(self):
        def X(v):
            return -5.0 + 10.0 * v / 100.0
        axis = Line([X(0), -0.8, 0], [X(100), -0.8, 0], color=INK, stroke_width=6)
        ticks = VGroup(*[Line([X(v), -1.05, 0], [X(v), -0.55, 0], color=DIM, stroke_width=5) for v in (0, 25, 50, 75, 100)])
        self.add(axis, ticks, L("95% interval", -2.6, 1.4), L("69–100%", 3.45, 1.4))
        self.wait(0.2)
        until(self, "interval")
        go(self, FadeIn(Dot([X(100), -0.8, 0], radius=0.14, color=TERRA)), rt=0.3)
        until(self, "69 to 100")
        band = VGroup(Line([X(69), 0.3, 0], [X(100), 0.3, 0], color=INK, stroke_width=10),
                      Line([X(69), 0.0, 0], [X(69), 0.6, 0], color=INK, stroke_width=10),
                      Line([X(100), 0.0, 0], [X(100), 0.6, 0], color=INK, stroke_width=10))
        go(self, GrowFromEdge(band, RIGHT), rt=0.7)
        until(self, "can't prove much")
        go(self, Create(DashedLine([X(69), -0.55, 0], [X(69), 0.0, 0], color=DIM, stroke_width=5, dash_length=0.12)), rt=0.4)
        done(self)


class B18_Check(Scene):
    def construct(self):
        agent = Iso(-4.4, -1.4, 0.8).mcp(0, 0, 0, 1.4, 1.4, 0.8)
        board, lights = Iso(-1.2, -2.6, 0.55).server(0, 0, 0, n=2)
        raw = VGroup(sheet(3.6, 0.2, 2.6, 3.2), lines_on(2.75, 1.2, 1.7, 2, gap=0.4, color=BAR1))
        self.add(agent, board, lights, raw, L("finished, 0 new", -3.6, 2.2), L("independent check", 3.6, -2.55))
        self.wait(0.2)
        until(self, "for an empty board")
        tray_b, tray_f = Iso(-1.2, -0.9, 0.55).open_box(0, 0, 0, 1.4, 1.4, 0.35)
        go(self, FadeIn(tray_b), FadeIn(tray_f), rt=0.4)
        until(self, "independent check")
        lens = VGroup(Circle(radius=0.6, stroke_color=INK, stroke_width=8).move_to([2.2, 1.6, 0]),
                      Line([2.62, 1.18, 0], [3.2, 0.6, 0], color=INK, stroke_width=10))
        go(self, FadeIn(lens), rt=0.3)
        go(self, lens.animate.shift(RIGHT * 1.6 + DOWN * 0.9), rt=0.8)
        until(self, "caught it")
        go(self, Create(xmark(-0.95, 2.2, 0.26, 8)), rt=0.35)
        done(self)


class B19_Plan(Scene):
    def construct(self):
        hi = Iso(-4.4, -1.9, 0.75)
        stack = VGroup(hi.box(0, 0, 0, 1.4, 1.7, 1.1, PAGE_TOP, PAGE_L, PAGE_R, sw=3),
                       *[Line(hi.p(0, 0.15, 0.09 * k), hi.p(0, 1.55, 0.09 * k), color=BAR2, stroke_width=2) for k in range(1, 12)])
        ev = sheet(0.6, -0.1, 3.4, 3.9)
        rows = VGroup(*[VGroup(Square(side_length=0.3, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-0.6, 1.3 - i * 0.62, 0]),
                               Line([-0.2, 1.3 - i * 0.62, 0], [1.7, 1.3 - i * 0.62, 0], color=GHOST, stroke_width=5)) for i in range(5)])
        readme = VGroup(sheet(4.6, 0.2, 1.8, 2.3), lines_on(4.05, 0.8, 1.1, 4, gap=0.36, color=BAR1))
        self.add(ev, rows, readme, L("held-out set", -4.4, -2.55), L("5 failures", 0.6, -2.65), stamp())
        self.wait(0.2)
        until(self, "larger held-out set")
        go(self, FadeIn(stack, shift=DOWN * 0.4), rt=0.5)
        until(self, "five deliberate failure")
        for i in range(5):
            go(self, FadeIn(Square(side_length=0.2, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-0.6, 1.3 - i * 0.62, 0])), rt=0.15)
        until(self, "predict and trigger")
        y = 1.3 - 2 * 0.62
        go(self, Create(xmark(2.05, y, 0.2)), rt=0.4)
        until(self, "a stranger")
        go(self, FadeIn(cursor(4.9, -0.2, 0.55)), rt=0.3)
        go(self, Create(check(4.5, -1.6, 0.24)), rt=0.3)
        done(self)


class B20_WorksIf(Scene):
    def construct(self):
        lab = VGroup(RoundedRectangle(width=1.8, height=1.2, corner_radius=0.12, fill_color=PAGE_TOP, fill_opacity=1,
                                      stroke_color=INK, stroke_width=4).move_to([-4.4, 0.3, 0]),
                     lines_on(-4.9, 0.5, 1.0, 2, gap=0.35, color=BAR1))
        post = VGroup(sheet(-0.6, 0.3, 1.8, 2.4), lines_on(-1.1, 1.0, 1.0, 1, color=BAR1))
        report = VGroup(sheet(3.4, 0.6, 1.8, 2.2), lines_on(2.9, 1.2, 1.0, 3, gap=0.36, color=BAR1))
        self.add(lab, post, report, L("agrees", -4.4, -2.3), L("abstains", -0.6, -2.3), stamp())
        self.wait(0.2)
        until(self, "agrees")
        go(self, Create(check(-4.4, -1.0, 0.26)), rt=0.4)
        until(self, "abstains")
        go(self, Create(ring(-0.6, -0.1, 0.45)), rt=0.5)
        until(self, "every failure")
        checker = Iso(4.6, -2.9, 0.6).mcp(0, 0, 0, 1.2, 1.2, 0.7)
        go(self, FadeIn(checker, shift=UP * 0.3), rt=0.4)
        until(self, "the agent's own report")
        go(self, Create(xmark(3.4, -0.2, 0.24)), rt=0.4)
        done(self)


class BEND_Close(Scene):
    def construct(self):
        iso = Iso(-3.2, -2.3, 0.9)
        plinth = iso.box(-0.2, -0.2, 0, 2.6, 2.6, 0.35)
        agent = iso.mcp(0.35, 0.35, 0.35, 1.5, 1.5, 0.9)
        self.add(plinth, agent)
        self.wait(0.2)
        go(self, FadeIn(L("Nishant U", 2.6, 0.6, 64)), FadeIn(L("Job-search agent", 2.6, -0.4, 52)), rt=0.5)
        go(self, FadeIn(Dot(iso.p(1.1, 1.1, 1.25), radius=0.1, color=TERRA)), rt=0.3)
        done(self)
