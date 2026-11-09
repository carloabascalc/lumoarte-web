#!/usr/bin/env python3
"""Genera src/assets/art/*.svg: las ilustraciones de home, heroes y secciones de proceso.

Usa el mismo modelador que tools/printer_art.py (milímetros reales + axonométrico).

Uso: python3 tools/site_art.py [nombre ...]
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import printer_art as pa
from printer_art import Art, CREAM, RUST, add3, gear_outline, mul3, n, spool_x, stage

ART = pathlib.Path(__file__).resolve().parent.parent / "src/assets/art"

NAVY = ("#3a4668", "#27324f", "#1b2339", "#121829")
STEEL = ("#d8d5cf", "#a9a69f", "#77756f")
MDF = ("#d8ab78", "#c89669", "#a97c50", "#8a6238")


def fit_points(view, points, w, h, mx=16, my=16):
    """Escala y origen para que estos puntos 3D queden centrados en el cuadro."""
    pa.set_view(*view)
    probe = Art("_", S=1, ox=0, oy=0, w=w, h=h)
    pts = [probe.p(*q) for q in points]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    S = min((w - 2 * mx) / (max(xs) - min(xs)), (h - 2 * my) / (max(ys) - min(ys)))
    return S, w / 2 - S * (min(xs) + max(xs)) / 2, h / 2 - S * (min(ys) + max(ys)) / 2


def fit(view, box, w, h, mx=16, my=16):
    """Igual que fit_points, para una caja ((x0, x1), (y0, y1), (z0, z1))."""
    return fit_points(view, [(x, y, z) for x in box[0] for y in box[1] for z in box[2]], w, h, mx, my)


def catmull(points, u):
    """Interpola una curva suave por puntos (u, valor) con u creciente."""
    pts = [points[0]] + points + [points[-1]]
    for i in range(1, len(pts) - 2):
        if u <= pts[i + 1][0] or i == len(pts) - 3:
            p0, p1, p2, p3 = pts[i - 1][1], pts[i][1], pts[i + 1][1], pts[i + 2][1]
            t = (u - pts[i][0]) / ((pts[i + 1][0] - pts[i][0]) or 1)
            return 0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (3 * p1 - p0 - 3 * p2 + p3) * t * t * t)
    return points[-1][1]


def mix(c0, c1, t):
    a_, b_ = [int(c0[i:i + 2], 16) for i in (1, 3, 5)], [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a_, b_))


def ramp(stops, u):
    for (u0, c0), (u1, c1) in zip(stops, stops[1:]):
        if u <= u1:
            return mix(c0, c1, (u - u0) / ((u1 - u0) or 1))
    return stops[-1][1]


def laser_cutter(name="cortadora-laser", w=480, h=360, S=0.178, ox=30, oy=274):
    """CO2 de 130 × 90 cm: pórtico azul marino, cama de cuchillas y cadena portacables, como la del taller."""
    pa.set_view(26, 28)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    W, D = 1900, 1240
    Z0, Zb, Zt = 110, 800, 1090
    stage(a, shadow=a.p(W * 0.54, D * 0.4, 0) + (w * 0.46, h * 0.2))

    LX0, LX1, LY0, LY1 = 150, 1410, 130, 950
    Zbed = 850
    TAGW, TAGH, GAPX, GAPY = 300, 250, 110, 110
    ox0 = LX0 + (LX1 - LX0 - 3 * TAGW - 2 * GAPX) / 2
    oy0 = LY0 + (LY1 - LY0 - 2 * TAGH - GAPY) / 2
    tags = [(ox0 + i * (TAGW + GAPX), oy0 + j * (TAGH + GAPY)) for j in (1, 0) for i in range(3)]
    hx0, hy0 = 780, 540
    v = 620.0
    travel = 0.34
    t = 0.3
    headx, heady, burns = [(0.0, tags[0][0] - hx0)], [(0.0, tags[0][1] - hy0)], []
    for tx, ty in tags:
        pts = [(tx, ty), (tx + TAGW, ty), (tx + TAGW, ty + TAGH), (tx, ty + TAGH), (tx, ty)]
        t += travel
        headx.append((t, tx - hx0))
        heady.append((t, ty - hy0))
        start = t
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            t += math.hypot(x1 - x0, y1 - y0) / v
            headx.append((t, x1 - hx0))
            heady.append((t, y1 - hy0))
        burns.append((start, t))
    t_end = t
    T = round(t_end + 2.6, 1)
    headx += [(t_end + 0.8, 0), (T - 0.3, 0), (T, tags[0][0] - hx0)]
    heady += [(t_end + 0.8, 0), (T - 0.3, 0), (T, tags[0][1] - hy0)]
    kf = a.translate_kf("hx", T, [(tt, *a.along("x", d)) for tt, d in headx])
    a.animate(f"{name}-hx", kf, T)
    kf = a.translate_kf("hy", T, [(tt, *a.along("y", d)) for tt, d in heady])
    a.animate(f"{name}-hy", kf, T)
    stops = [(0, "opacity:0")]
    for s0, s1 in burns:
        stops += [(s0, "opacity:1"), (s1, "opacity:0")]
    stops.append((T, "opacity:0"))
    kf = a.keyframes("beam", T, stops)
    a.animate(f"{name}-beam", kf, T, "step-end")
    for k, (s0, s1) in enumerate(burns):
        kf = a.keyframes(f"cut{k}", T, [(0, "stroke-dashoffset:100"), (s0, "stroke-dashoffset:100"), (s1, "stroke-dashoffset:0"), (T, "stroke-dashoffset:0")])
        a.animate(f"{name}-cut{k}", kf, T)
    kf = a.keyframes("sheet", T, [(0, "opacity:1"), (T - 1.2, "opacity:1"), (T - 0.6, "opacity:0"), (T - 0.01, "opacity:0"), (T, "opacity:1")])
    a.animate(f"{name}-cuts", kf, T)
    kf = a.keyframes("spark", 0.5, [(0, "opacity:1;transform:translate(0,0)"), (0.5, "opacity:0;transform:translate(var(--sx),var(--sy))")])
    a.css.append(f".{name}-sp{{animation:{kf} .5s ease-out infinite;animation-play-state:var(--play,running)}}")

    for (cx, cy) in ((90, 90), (W - 90, 90), (W - 90, D - 90)):
        a.path(a.cylz_path(cx, cy, 0, Z0, 34), a.cylz_grad(cx, cy, 0, 34, [(0, "#14100c"), (0.5, "#4a4037"), (1, "#14100c")]))
        a.path(a.ellipse_z(cx, cy, Z0, 40), "#3a3027")

    side = a.lin3((W, 0, Zb), (W, D, Z0), [(0, NAVY[1]), (1, NAVY[2])])
    front = a.lin3((0, 0, Zb), (0, 0, Z0), [(0, NAVY[0]), (1, NAVY[1])])
    a.path(a.poly([(W, 0, Z0), (W, D, Z0), (W, D, Zt - 40), (W, 0, Zt - 40)]), side)
    a.path(a.poly([(0, 0, Z0), (W, 0, Z0), (W, 0, Zb), (0, 0, Zb)]), front)
    for dx0, dx1 in ((60, 640), (660, 1240), (1260, 1840)):
        a.path(a.rr((dx0, 0, Z0 + 40), (1, 0, 0), (0, 0, 1), dx1 - dx0, Zb - Z0 - 90, 10), NAVY[0], stroke=NAVY[3], sw=0.7)
        a.path(a.poly([(dx0 + 2, 0, Zb - 52), (dx1 - 2, 0, Zb - 52)], close=False), stroke="#6d7796", sw=0.6)
        mx = dx1 - 44
        a.path(a.rr((mx, -2, Z0 + 250), (1, 0, 0), (0, 0, 1), 18, 130, 6), STEEL[1], stroke=NAVY[3], sw=0.5)
    d = ""
    for vz in range(Z0 + 110, Z0 + 240, 26):
        d += a.poly([(1300, 0, vz), (1500, 0, vz)], close=False)
    a.path(d, stroke=NAVY[3], sw=1.1, op=0.8)
    a.path(a.rr((W, 150, Z0 + 60), (0, 1, 0), (0, 0, 1), D - 300, Zb - Z0 - 130, 10), stroke=NAVY[3], sw=0.8)
    d = ""
    for vz in range(Z0 + 120, Z0 + 330, 30):
        d += a.poly([(W, 300, vz), (W, 760, vz)], close=False)
    a.path(d, stroke=NAVY[3], sw=1.1)

    a.path(a.poly([(0, 0, Zb), (W, 0, Zb), (W, 0, Zb + 70), (0, 0, Zb + 70)]), STEEL[1])
    a.path(a.poly([(0, 0, Zb + 70), (W, 0, Zb + 70)], close=False), stroke="#f2efe9", sw=0.7)

    Yl = 950
    a.path(a.poly([(0, Yl, Zt - 40), (W, Yl, Zt - 40), (W, D, Zt - 40), (0, D, Zt - 40)]), a.lin3((0, D, Zt), (W, Yl, Zt), [(0, NAVY[0]), (1, NAVY[1])]))
    a.path(a.poly([(0, D, Zt - 40), (W, D, Zt - 40)], close=False), stroke="#6d7796", sw=0.7)
    d = ""
    for yy in (Yl + 90, D - 90):
        d += a.poly([(120, yy, Zt - 40), (1780, yy, Zt - 40)], close=False)
    a.path(d, stroke=NAVY[3], sw=0.7, op=0.8)
    ex, ey = 1640, D - 150
    a.path(a.cylz_path(ex, ey, Zt - 40, Zt + 90, 66), a.cylz_grad(ex, ey, 0, 66, [(0, "#8d8a84"), (0.4, "#e8e5df"), (1, "#7a7771")]))
    d = ""
    for rz in range(Zt - 20, Zt + 90, 26):
        d += a.arc((ex, ey, rz), (66, 0, 0), (0, 66, 0), math.degrees(pa.AZ) - 180, math.degrees(pa.AZ))
    a.path(d, stroke="#6d6a64", sw=0.6)
    a.path(a.ellipse_z(ex, ey, Zt + 90, 66), "#c9c6c0", stroke="#6d6a64", sw=0.5)
    a.path(a.ellipse_z(ex, ey, Zt + 90, 52), "#2a2622")

    Xc = 1560
    a.path(a.poly([(Xc, 0, Zb + 70), (W, 0, Zb + 70), (W, 300, Zt - 40), (Xc, 300, Zt - 40)]), a.lin3((0, 0, Zb + 70), (0, 300, Zt - 40), [(0, NAVY[2]), (1, NAVY[1])]))
    a.path(a.poly([(Xc, 300, Zt - 40), (W, 300, Zt - 40), (W, Yl, Zt - 40), (Xc, Yl, Zt - 40)]), NAVY[0])
    px0 = Xc + 40
    pv = (0, 300 / math.hypot(300, Zt - 40 - Zb - 70), (Zt - 40 - Zb - 70) / math.hypot(300, Zt - 40 - Zb - 70))
    po = (px0, 20, Zb + 70 + 20 * (Zt - 40 - Zb - 70) / 300)
    a.path(a.rr(po, (1, 0, 0), pv, 260, 300, 8), "#14100c", stroke="#5e5347", sw=0.6)
    scr = a.matrix(add3(po, mul3(pv, 280)), (1, 0, 0), mul3(pv, -1))
    a.open(tf=scr)
    a.rect(18, 16, 130, 92, "#27455f", rx=4)
    a.rect(26, 26, 70, 7, "#a9d2de", rx=2)
    a.rect(26, 40, 50, 6, "#6f9fb0", rx=2)
    a.rect(26, 54, 88, 6, "#6f9fb0", rx=2)
    a.rect(26, 72, 112, 10, "#3a3027", rx=3)
    a.add(f'<rect x="26" y="72" width="112" height="10" rx="3" fill="#e09a4a" class="{name}-prog"/>')
    for r_ in range(3):
        for c_ in range(3):
            a.rect(168 + c_ * 26, 18 + r_ * 26, 18, 18, "#3a3027" if (r_ + c_) % 2 else "#5e5347", rx=3)
    a.add('<circle cx="52" cy="200" r="26" fill="#b02a14" stroke="#ece6da" stroke-width="5"/>')
    a.add('<circle cx="124" cy="200" r="16" fill="#d9d4ca"/><rect x="118" y="196" width="12" height="8" rx="2" fill="#3a3027"/>')
    a.add('<circle cx="188" cy="200" r="16" fill="#1a1612" stroke="#b3a798" stroke-width="3"/>')
    a.close()
    kf = a.keyframes("prog", T, [(0, "transform:scaleX(0)"), (t_end, "transform:scaleX(1)"), (T - 0.6, "transform:scaleX(1)"), (T, "transform:scaleX(0)")])
    a.animate(f"{name}-prog", kf, T)
    a.css.append(f".{name}-prog{{transform-origin:26px 77px}}")

    Xl0, Xl1 = 30, Xc - 10
    Ys0, Zs0 = 14, Zb + 80
    Ys1, Zs1 = 520, Zt
    lid_slope = a.poly([(Xl0, Ys0, Zs0), (Xl1, Ys0, Zs0), (Xl1, Ys1, Zs1), (Xl0, Ys1, Zs1)])
    lid_top = a.poly([(Xl0, Ys1, Zs1), (Xl1, Ys1, Zs1), (Xl1, Yl, Zs1), (Xl0, Yl, Zs1)])
    cl = a.clip(lid_slope + lid_top)
    a.path(lid_slope + lid_top, "#120e0a")
    a.open(clip=cl)
    a.path(a.poly([(Xl0, 1040, Zbed - 60), (Xl1, 1040, Zbed - 60), (Xl1, 1040, Zt + 60), (Xl0, 1040, Zt + 60)]), a.lin3((0, 1040, Zt + 60), (0, 1040, Zbed), [(0, "#6e6256"), (1, "#3a3027")]))
    a.path(a.poly([(Xl0, 0, Zbed - 60), (Xl0, 1040, Zbed - 60), (Xl0, 1040, Zt + 60), (Xl0, 0, Zt + 60)]), a.lin3((Xl0, 0, Zt), (Xl0, 1040, Zbed), [(0, "#55493e"), (1, "#2a231d")]))
    a.path(a.poly([(LX0 - 40, LY0 - 60, Zbed - 6), (LX1 + 40, LY0 - 60, Zbed - 6), (LX1 + 40, LY1 + 60, Zbed - 6), (LX0 - 40, LY1 + 60, Zbed - 6)]), "#14100c")
    d = ""
    for sx in range(LX0, LX1 + 1, 42):
        d += a.poly([(sx, LY0 - 60, Zbed - 4), (sx, LY1 + 60, Zbed - 4)], close=False)
    a.path(d, stroke="#6e6256", sw=0.8)
    sheet = [(LX0, LY0, Zbed), (LX1, LY0, Zbed), (LX1, LY1, Zbed), (LX0, LY1, Zbed)]
    a.path(a.poly(sheet), a.lin3(sheet[0], sheet[2], [(0, MDF[0]), (1, MDF[1])]), stroke=MDF[3], sw=0.4)
    d = ""
    for gy in range(LY0 + 40, LY1, 70):
        d += a.poly([(LX0, gy, Zbed), (LX1, gy, Zbed)], close=False)
    a.path(d, stroke=MDF[3], sw=0.3, op=0.35)
    a.open(cls=f"{name}-cuts")
    for k, (tx, ty) in enumerate(tags):
        tag = [(tx, ty, Zbed), (tx + TAGW, ty, Zbed), (tx + TAGW, ty + TAGH, Zbed), (tx, ty + TAGH, Zbed)]
        a.add(f'<path d="{a.poly(tag)}" fill="none" stroke="#3d1806" stroke-width="1.1" stroke-linejoin="round" pathLength="100" stroke-dasharray="100" class="{name}-cut{k}"/>')
    a.close()
    cx = LX1 + 62
    a.box(cx - 16, cx + 16, 60, 1020, Zbed + 2, Zbed + 26, side="#14100c", top="#2a2622")
    d = ""
    for cy in range(70, 1010, 40):
        d += a.poly([(cx - 16, cy, Zbed + 26), (cx + 16, cy, Zbed + 26)], close=False)
    a.path(d, stroke="#6e6256", sw=0.6)
    for rx in (Xl0 + 34, LX1 + 104):
        a.box(rx - 12, rx + 12, 30, 1030, Zbed + 70, Zbed + 92, side=NAVY[2], top=STEEL[0])
    gy0, gz = hy0, Zbed + 96
    a.open(cls=f"{name}-hy")
    a.box(Xl0 + 22, LX1 + 116, gy0 + 20, gy0 + 90, gz - 24, gz + 24, front=a.lin3((0, gy0 + 20, gz + 24), (0, gy0 + 20, gz - 24), [(0, NAVY[0]), (1, NAVY[2])]), top=NAVY[1])
    a.path(a.poly([(Xl0 + 22, gy0 + 20, gz + 8), (LX1 + 116, gy0 + 20, gz + 8)], close=False), stroke=STEEL[0], sw=1)
    d = ""
    for bx in range(Xl0 + 60, LX1 + 100, 140):
        q = a.p(bx, gy0 + 20, gz - 8)
        d += f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r=".8"/>'
    a.add(f'<g fill="#c9a267">{d}</g>')
    a.open(cls=f"{name}-hx")
    a.box(hx0 - 44, hx0 + 44, hy0 - 4, hy0 + 24, gz - 34, gz + 34, front=a.lin3((hx0 - 44, hy0 - 4, 0), (hx0 + 44, hy0 - 4, 0), [(0, NAVY[0]), (1, NAVY[1])]), side=NAVY[2], top=STEEL[1])
    a.path(a.cylz_path(hx0, hy0 + 8, gz - 60, gz - 34, 16), a.cylz_grad(hx0, hy0 + 8, 0, 16, [(0, "#8a5a18"), (0.5, "#f0c27c"), (1, "#8a5a18")]))
    a.path(a.poly([(hx0 - 11, hy0 + 8, gz - 60), (hx0 + 11, hy0 + 8, gz - 60), (hx0 + 3, hy0 + 8, gz - 78), (hx0 - 3, hy0 + 8, gz - 78)]), "#c9a267")
    a.close()
    a.close()
    a.close()

    amber = a.lin3((0, Ys0, Zs0), (0, Yl, Zs1), [(0, "#e8912f", 0.26), (0.55, "#c87a2a", 0.3), (1, "#a85f1c", 0.5)])
    a.path(lid_slope + lid_top, amber)
    a.open(clip=cl)
    a.path(a.poly([(200, Ys0, Zs0), (520, Ys0, Zs0), (1020, Ys1, Zs1), (700, Ys1, Zs1)]), "#fff6e6", op=0.09)
    a.path(a.poly([(600, Ys0, Zs0), (680, Ys0, Zs0), (1180, Ys1, Zs1), (1100, Ys1, Zs1)]), "#fff6e6", op=0.07)
    # El haz va sobre el ámbar para que se vea encendido a través de la tapa.
    a.open(cls=f"{name}-hy")
    a.open(cls=f"{name}-hx")
    tip = a.p(hx0, hy0, Zbed)
    a.open(cls=f"{name}-beam")
    top_ = a.p(hx0, hy0 + 8, gz - 78)
    a.add(f'<path d="M{n(top_[0])} {n(top_[1])}L{n(tip[0])} {n(tip[1])}" stroke="#ff7a2a" stroke-width="4.5" opacity=".4" stroke-linecap="round"/>')
    a.add(f'<path d="M{n(top_[0])} {n(top_[1])}L{n(tip[0])} {n(tip[1])}" stroke="#ffe7c4" stroke-width="1.3" stroke-linecap="round"/>')
    gl = a.rad(tip[0], tip[1], 13, [(0, "#fff3d8", 1), (0.35, "#ff9a3c", 0.8), (1, "#ff7a2a", 0)])
    a.add(f'<circle cx="{n(tip[0])}" cy="{n(tip[1])}" r="13" fill="{gl}"/>')
    for i, (sx, sy) in enumerate(((-11, -8), (9, -10), (13, -3), (-6, -13))):
        a.add(f'<circle cx="{n(tip[0])}" cy="{n(tip[1])}" r="1" fill="#ffd28a" class="{name}-sp" style="--sx:{sx}px;--sy:{sy}px;animation-delay:{-i * 0.125}s"/>')
    a.close()
    a.close()
    a.close()
    a.close()
    fr = NAVY[1]
    a.path(a.poly([(0, 0, Zb + 70), (Xl0, Ys0, Zs0), (Xl0, Ys1, Zs1), (Xl0, Yl, Zs1), (0, Yl, Zt - 40), (0, 500, Zt - 40)]), NAVY[2])
    a.path(a.poly([(Xl0, 0, Zb + 70), (Xl1, 0, Zb + 70), (Xl1, Ys0, Zs0), (Xl0, Ys0, Zs0)]), NAVY[1])
    bar = 28
    a.path(a.poly([(Xl0, Ys1 - bar, Zs1 - bar * 0.4), (Xl1, Ys1 - bar, Zs1 - bar * 0.4), (Xl1, Ys1, Zs1), (Xl0, Ys1, Zs1)]), fr)
    a.path(a.poly([(Xl0, Yl, Zs1), (Xl1, Yl, Zs1), (Xl1, Yl + 30, Zs1), (Xl0, Yl + 30, Zs1)]), fr)
    for xb in (Xl0, Xl1 - 26):
        a.path(a.poly([(xb, Ys0, Zs0), (xb + 26, Ys0, Zs0), (xb + 26, Ys1, Zs1), (xb, Ys1, Zs1)]), fr)
        a.path(a.poly([(xb, Ys1, Zs1), (xb + 26, Ys1, Zs1), (xb + 26, Yl, Zs1), (xb, Yl, Zs1)]), fr)
    a.path(a.poly([(Xl1, 0, Zb + 70), (Xc, 0, Zb + 70), (Xc, Ys0, Zs0), (Xl1, Ys0, Zs0)]), NAVY[1])
    a.path(a.poly([(Xl1, Ys0, Zs0), (Xc, Ys0, Zs0), (Xc, 300, Zt - 40), (Xl1, Ys1, Zs1)]), NAVY[2])
    a.path(a.poly([(Xl1, Ys1, Zs1), (Xc, 300, Zt - 40), (Xc, Yl, Zt - 40), (Xl1, Yl, Zs1)]), NAVY[1])
    a.path(a.rr((560, Ys0 + 8, Zs0 + 10), (1, 0, 0), (0, 0.78, 0.62), 460, 22, 8), STEEL[0], stroke=NAVY[3], sw=0.5)
    return a.write(ART)


def h2c_wide():
    """La H2C con un segundo AMS en el piso: la versión apaisada para la tarjeta de la home."""
    return pa.h2c(name="impresion-3d", w=480, h=360, S=0.318, ox=78, oy=304, outdir=ART, floor_ams=True)


def plate_mini(a, x0, x1, y0, y1, z):
    """Cama como la de las fotos del taller: PEI dorado texturizado, línea blanca y aviso de superficie caliente."""
    a.box(x0 - 5, x1 + 5, y0 - 5, y1 + 5, z - 13, z - 1, front=a.lin3((x0, y0, 0), (x1, y0, 0), [(0, "#2e2620"), (1, "#14100c")]), side="#100c09", top="#231d18")
    d = a.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)])
    a.path(d, a.lin3((x0, y0, z), (x1, y1, z), [(0, "#cdb17c"), (0.5, "#b0935f"), (1, "#957a4a")]))
    pid = a.nid()
    a.defs.append(
        f'<pattern id="{pid}" width="11" height="11" patternUnits="userSpaceOnUse" patternTransform="{a.matrix((x0, y0, z), (1, 0, 0), (0, 1, 0))}">'
        '<circle cx="1.6" cy="2.4" r=".8" fill="#fff4d8" opacity=".6"/><circle cx="6.8" cy="1.4" r=".7" fill="#5a4522" opacity=".45"/>'
        '<circle cx="9.4" cy="6.2" r=".9" fill="#fff4d8" opacity=".4"/><circle cx="3.9" cy="7.6" r=".7" fill="#5a4522" opacity=".5"/>'
        '<circle cx="7.3" cy="9.6" r=".6" fill="#fff4d8" opacity=".55"/></pattern>'
    )
    a.path(d, f"url(#{pid})")
    a.path(d, a.lin3((x0, y1, z), (x1, y0, z), [(0.3, "#fff6e0", 0), (0.5, "#fff6e0", 0.3), (0.68, "#fff6e0", 0)]))
    a.path(a.poly([(x0 + 8, y0 + 13, z), (x1 - 8, y0 + 13, z)], close=False), stroke="#f6efe0", sw=0.9)
    a.path(a.rr((x0 + 8, y0 + 2.5, z), (1, 0, 0), (0, 1, 0), 58, 8.5, 1.5), "#f6efe0")
    a.open(tf=a.matrix((x0 + 37, y0 + 4.4, z), (1, 0, 0), (0, -1, 0)))
    a.add('<text text-anchor="middle" font-family="DM Sans,system-ui,sans-serif" font-size="6.6" font-weight="700" letter-spacing=".5" fill="#2b1d12">HOT SURFACE</text>')
    a.close()


def hot_end(a, cx, cy, z, tube=True, glow_attr=""):
    """Cabezal de la boquilla hacia arriba: latón, ducto negro con ventilador y carcasa plateada."""
    if tube:
        q = a.p(cx + 8, cy + 6, z + 104)
        tube_d = f"M{n(q[0])} {n(q[1])}c2 -18 16 -30 38 -40s44 -46 60 -110"
        a.add(f'<path d="{tube_d}" fill="none" stroke="#6d6458" stroke-width="3.4" stroke-linecap="round"/><path d="{tube_d}" fill="none" stroke="#efe9df" stroke-width="2" stroke-linecap="round"/>')
    shell = a.lin3((cx - 27, cy - 19, 0), (cx + 27, cy - 19, 0), [(0, "#f4efe6"), (0.55, "#d4cec2"), (1, "#a9a296")])
    a.rbox(cx - 27, cx + 27, cy - 19, cy + 21, z + 50, z + 106, 7, shell, "#7f786d", "#efe9df", shade_f="#b5aea2", shade_s="#8c857a", edge="#3b3027", sw=0.5)
    a.path(a.poly([(cx + 13, cy - 19, z + 52), (cx + 13, cy - 19, z + 104)], close=False), stroke="#6d665c", sw=0.5)
    a.path(a.rr((cx - 22, cy - 19, z + 88), (1, 0, 0), (0, 0, 1), 30, 12, 3), "#8c857a", op=0.5)
    a.open(tf=a.matrix((cx - 22, cy - 19, z + 74), (1, 0, 0), (0, 0, -1)))
    a.add('<text font-family="DM Sans,system-ui,sans-serif" font-size="6.8" font-weight="600" fill="#463a2e">Bambu Lab</text>')
    a.close()
    d = ""
    for k in range(4):
        d += a.poly([(cx + 27, cy - 8 + k * 7, z + 58), (cx + 27, cy - 8 + k * 7, z + 96)], close=False)
    a.path(d, stroke="#5e584f", sw=0.7)
    a.rbox(cx - 23, cx + 23, cy - 16, cy + 18, z + 13, z + 50, 5, "#1e1916", "#100c09", "#2d2620", edge="#050403", sw=0.4)
    a.path(a.ellipse_x(cx + 23, cy + 1, z + 31, 13), "#231d18", stroke="#5c5146", sw=0.4)
    a.path(a.ellipse_x(cx + 23, cy + 1, z + 31, 3.6), "#5c5146")
    d = ""
    for k in range(5):
        t = k * math.pi * 2 / 5
        d += a.poly([(cx + 23, cy + 1 + 4 * math.cos(t), z + 31 + 4 * math.sin(t)), (cx + 23, cy + 1 + 11 * math.cos(t + 0.5), z + 31 + 11 * math.sin(t + 0.5))], close=False)
    a.path(d, stroke="#5c5146", sw=0.6)
    a.path(a.rr((cx - 12, cy - 17, z + 20), (1, 0, 0), (0, 0, 1), 24, 21, 3), "#312a24", stroke="#5c5146", sw=0.35)
    a.path(a.poly([(cx - 7, cy, z + 13), (cx + 7, cy, z + 13), (cx + 2.4, cy, z + 3), (cx, cy, z), (cx - 2.4, cy, z + 3)]), a.lin3((cx - 7, cy, 0), (cx + 7, cy, 0), [(0, "#f6cf8e"), (1, "#8a5a18")]))
    q = a.p(cx, cy, z)
    g = a.rad(q[0], q[1], 8, [(0, "#ffdca8", 1), (0.35, "#ff8a2a", 0.7), (1, "#ff8a2a", 0)])
    a.add(f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="8" fill="{g}"{glow_attr}/>')


def x_rail(a, x0, x1, cy, zr):
    a.box(x0, x1, cy + 22, cy + 42, zr - 13, zr + 13, front="#1b1612", top="#352c25")
    rail = a.lin3((0, cy + 22, zr + 10), (0, cy + 22, zr - 2), [(0, "#e6e0d5"), (1, "#8d8478")])
    a.path(a.poly([(x0, cy + 22, zr - 2), (x1, cy + 22, zr - 2), (x1, cy + 22, zr + 10), (x0, cy + 22, zr + 10)]), rail)
    d = ""
    for bx in range(int(x0) + 12, int(x1), 26):
        q = a.p(bx, cy + 22, zr + 4)
        d += f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r=".9"/>'
    a.add(f'<g fill="#3a3027">{d}</g>')


def path_motion(a, name, cx, cy, zb, path, T):
    """El carro sigue el recorrido real (t, x, y, z); el riel lo acompaña en Y y Z, como en una CoreXY."""
    kf = a.translate_kf("hxy", T, [(t, *a.v(x - cx, y - cy, z - zb)) for t, x, y, z in path])
    a.animate(f"{name}-hxy", kf, T)
    kf = a.translate_kf("rail", T, [(t, *a.v(0, y - cy, z - zb)) for t, _, y, z in path])
    a.animate(f"{name}-rail", kf, T)


VASE = [(0, 44), (0.1, 56), (0.32, 80), (0.56, 70), (0.76, 46), (0.88, 40), (1, 54)]


def vase_layers(a, cx, cy, Zh, N, group):
    """Capas del florero acanalado; group(k, u) abre el grupo de cada una para que cada sección decida cómo aparece."""
    colors = [(0, "#7d2b02"), (0.28, "#a53a04"), (0.55, "#c9641c"), (0.8, "#e09a4a"), (1, "#f3cf95")]
    h_ = Zh / N
    RIBS, TWIST = 14, 2.2
    cam = math.atan2(-pa.CA, pa.SA)
    az = math.degrees(pa.AZ)
    for k in range(N):
        z0, z1 = k * h_, (k + 1) * h_ + 0.5
        u = (k + 0.5) / N
        r = catmull(VASE, u)
        base = ramp(colors, u)
        light, dark = mix(base, "#fff1dc", 0.42), mix(base, "#1a0a02", 0.52)
        group(k, u)
        a.path(a.cylz_path(cx, cy, z0, z1, r), a.lin_box([(0, dark), (0.26, base), (0.44, light), (0.64, base), (1, dark)]))
        dd, dl = "", ""
        for i in range(RIBS):
            t0 = i * 2 * math.pi / RIBS + TWIST * z0 / Zh
            t1 = i * 2 * math.pi / RIBS + TWIST * (z0 + h_) / Zh
            if math.cos((t0 + t1) / 2 - cam) < 0.08:
                continue
            dd += a.poly([(cx + r * math.cos(t0), cy + r * math.sin(t0), z0), (cx + r * math.cos(t1), cy + r * math.sin(t1), z1)], close=False)
            t0 += 0.07
            t1 += 0.07
            dl += a.poly([(cx + r * math.cos(t0), cy + r * math.sin(t0), z0), (cx + r * math.cos(t1), cy + r * math.sin(t1), z1)], close=False)
        a.path(dd, stroke=dark, sw=0.8, op=0.7)
        a.path(dl, stroke=light, sw=0.6, op=0.6)
        a.path(a.arc((cx, cy, z0), (r, 0, 0), (0, r, 0), az - 180, az), stroke=dark, sw=0.25, op=0.75)
        a.ell_z(cx, cy, z1, r, light)
        a.ell_z(cx, cy, z1, r - 3.2, mix(base, "#140802", 0.72))
        a.close()


def spec_vase(name="pieza-florero", w=320, h=400):
    """Florero acanalado multicolor: la boquilla camina sobre el borde mientras cada capa aparece a su tiempo."""
    Zh = 300
    S, ox, oy = fit((24, 20), ((-14, 286), (-6, 234), (-13, Zh + 132)), w, h, mx=14, my=12)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    stage(a, shadow=a.p(136, 110, -14) + (w * 0.5, h * 0.11), floor=False)
    T, t_print = 15, 11.5
    t_f0, t_f1 = 13.2, 14.2
    cx, cy = 136, 114
    N = 36
    plate_mini(a, 0, 272, 0, 228, 0)

    def group(k, u):
        t_k = 0.5 + (t_print - 0.5) * k / N
        kf = a.keyframes(f"l{k}", T, [(0, "opacity:0"), (t_k, "opacity:0"), (t_k + 0.04, "opacity:1"), (t_f0, "opacity:1"), (t_f1, "opacity:0"), (T, "opacity:0")])
        a.animate(f"{name}-l{k}", kf, T)
        a.open(cls=f"{name}-l{k}", op=None if u < 0.62 else 0)

    vase_layers(a, cx, cy, Zh, N, group)
    h_ = Zh / N
    cam = math.atan2(-pa.CA, pa.SA)
    radius = lambda u: catmull(VASE, u)
    # Una vuelta de la boquilla cada tres capas: va sobre la pared, no flotando en el hueco.
    zb = Zh * 0.62
    start = (cx + radius(0) * math.cos(cam), cy + radius(0) * math.sin(cam), h_)
    path = [(0, *start)]
    steps = 132
    for i in range(1, steps + 1):
        u = i / steps
        t = 0.5 + (t_print - 0.5) * u
        ang = cam + u * 12 * 2 * math.pi
        r = radius(u)
        path.append((t, cx + r * math.cos(ang), cy + r * math.sin(ang), u * Zh + h_))
    park = (cx + 130, cy + 30, Zh + 24)
    path += [(t_print + 0.9, *park), (T - 0.4, *park), (T, *start)]
    path_motion(a, name, cx, cy, zb, path, T)
    a.open(cls=f"{name}-rail")
    x_rail(a, -240, 620, cy, zb + 84)
    a.close()
    a.open(cls=f"{name}-hxy")
    hot_end(a, cx, cy, zb)
    a.close()
    return a.write(ART)


def spec_gear(name="pieza-engrane", w=320, h=320):
    """Engrane técnico: la pared queda quieta y sube una ventana de recorte, como crece una pieza de verdad."""
    Hp, base = 70, 0.68
    S, ox, oy = fit((24, 26), ((-14, 262), (-8, 232), (-13, Hp + 126)), w, h, mx=14, my=12)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    stage(a, shadow=a.p(124, 112, -14) + (w * 0.5, h * 0.14), floor=False)
    T, t_print = 12, 9
    t_f0, t_f1 = 10.4, 11.2
    cx, cy = 124, 112
    outline = gear_outline(cx, cy, 72, 94, 14)
    plate_mini(a, 0, 248, 0, 224, 0)
    top = base * Hp
    dz = lambda pr: a.along("z", (pr - base) * Hp)[1]
    kf = a.translate_kf("up", T, [(0, 0, dz(0)), (t_print, 0, dz(1)), (t_f1, 0, dz(1)), (T, 0, dz(0))])
    a.animate(f"{name}-up", kf, T)
    kf = a.translate_kf("dn", T, [(0, 0, -dz(0)), (t_print, 0, -dz(1)), (t_f1, 0, -dz(1)), (T, 0, -dz(0))])
    a.animate(f"{name}-dn", kf, T)
    fade = a.keyframes("fade", T, [(0, "opacity:1"), (t_f0, "opacity:1"), (t_f1, "opacity:0"), (T - 0.02, "opacity:0"), (T, "opacity:1")])
    a.animate(f"{name}-fade", fade, T)
    scr = [a.p(px, py, top) for px, py in outline]
    li = min(range(len(scr)), key=lambda k: scr[k][0])
    ri = max(range(len(scr)), key=lambda k: scr[k][0])
    step = 1 if scr[(li + 1) % len(scr)][1] > scr[(li - 1) % len(scr)][1] else -1
    chain, k = [], li
    while True:
        chain.append(outline[k])
        if k == ri:
            break
        k = (k + step) % len(outline)
    # Lo impreso es lo que queda bajo el contorno frontal del plano de la boquilla.
    cq = [a.p(px, py, top) for px, py in chain]
    cut = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in cq) + f"L{n(cq[-1][0])} {n(cq[-1][1] + 400)}L{n(cq[0][0])} {n(cq[0][1] + 400)}Z"
    cid = a.clip(cut)
    a.open(cls=f"{name}-fade")
    a.open(clip=cid, cls=f"{name}-up")
    a.open(cls=f"{name}-dn")
    # Las paredes se pintan de atrás hacia adelante para que cada diente tape al de junto.
    walls = []
    for i, p_ in enumerate(outline):
        q_ = outline[(i + 1) % len(outline)]
        ex, ey = q_[0] - p_[0], q_[1] - p_[1]
        ln = math.hypot(ex, ey) or 1
        nx, ny = ey / ln, -ex / ln
        if nx * pa.SA - ny * pa.CA <= 0:
            continue
        depth = (p_[1] + q_[1]) / 2 * pa.CA - (p_[0] + q_[0]) / 2 * pa.SA
        walls.append((depth, p_, q_, max(0.0, -0.55 * nx - 0.83 * ny)))
    tones = ["#7a3a10", "#9a5116", "#c87a2a", "#dc9543"]
    for _, p_, q_, shade in sorted(walls, key=lambda w: -w[0]):
        tone = tones[min(3, int(shade * 4))]
        a.path(a.poly([(p_[0], p_[1], 0), (q_[0], q_[1], 0), (q_[0], q_[1], Hp), (p_[0], p_[1], Hp)]), tone)
        d = ""
        for lz in range(5, Hp, 5):
            d += a.poly([(p_[0], p_[1], lz), (q_[0], q_[1], lz)], close=False)
        a.path(d, stroke=mix(tone, "#2a1204", 0.45), sw=0.3)
    a.close()
    a.close()
    a.open(cls=f"{name}-up")
    ring = gear_outline(cx, cy, 68, 89, 14)
    a.path(a.poly([(px, py, top) for px, py in outline]), "#eeaa58")
    a.path(a.poly([(px, py, top) for px, py in ring]), stroke="#c87a2a", sw=0.6)
    a.path(a.ellipse_z(cx, cy, top, 60), "#e8a250", stroke="#c87a2a", sw=0.5)
    d = ""
    for s_ in range(-6, 7):
        off = s_ * 8.6
        half = math.sqrt(max(0, 58 * 58 - 2 * off * off))
        if half > 0:
            d += a.poly([(cx + off - half * 0.7, cy + off + half * 0.7, top), (cx + off + half * 0.7, cy + off - half * 0.7, top)], close=False)
            d += a.poly([(cx + off - half * 0.7, cy - off - half * 0.7, top), (cx + off + half * 0.7, cy - off + half * 0.7, top)], close=False)
    a.path(d, stroke="#b56a1e", sw=0.42, op=0.8)
    for i in range(6):
        t = i * math.pi / 3 + 0.3
        hx, hy = cx + 42 * math.cos(t), cy + 42 * math.sin(t)
        a.path(a.ellipse_z(hx, hy, top, 10), "#6b2c0a")
        a.path(a.ellipse_z(hx, hy, top - 7, 10), "#2a1605")
    a.path(a.ellipse_z(cx, cy, top, 21), "#6b2c0a")
    a.path(a.ellipse_z(cx, cy, top - 11, 21), "#2a1605")
    a.close()
    a.close()
    k = a.translate_kf("ox", 1, [(0, *a.along("x", -66)), (1, *a.along("x", 66))])
    a.css.append(f".{name}-ox{{animation:{k} .9s cubic-bezier(.45,.05,.55,.95) infinite alternate;animation-play-state:var(--play,running)}}")
    k = a.translate_kf("oy", 1, [(0, *a.along("y", -44)), (1, *a.along("y", 44))])
    a.css.append(f".{name}-oy{{animation:{k} 2.1s cubic-bezier(.45,.05,.55,.95) infinite alternate;animation-play-state:var(--play,running)}}")
    a.open(cls=f"{name}-up")
    x_rail(a, -240, 560, cy, top + 84)
    a.open(cls=f"{name}-oy")
    a.open(cls=f"{name}-ox")
    hot_end(a, cx, cy, top)
    a.close()
    a.close()
    a.close()
    return a.write(ART)


def spec_maqueta(name="pieza-maqueta", w=320, h=320):
    """Maqueta multicolor: casa, base y árboles salen por capas, y la boquilla recorre el contorno de cada una."""
    Zmax = 128
    S, ox, oy = fit((32, 24), ((-14, 262), (-8, 216), (-13, Zmax + 96)), w, h, mx=14, my=12)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    stage(a, shadow=a.p(124, 104, -14) + (w * 0.5, h * 0.14), floor=False)
    T, t_print = 15, 12
    t_f0, t_f1 = 13.4, 14.2
    plate_mini(a, 0, 248, 0, 208, 0)
    BX0, BX1, BY0, BY1 = 12, 236, 14, 194
    X0, X1, Y0, Y1 = 70, 196, 74, 160
    Hb, Hw, Hr = 8, 66, 50
    eave = 9
    hl = 4.0
    N = int(round((Hb + Hw + Hr) / hl))
    WALL = ("#f7eedd", "#d9c9ad", "#c7b292")
    ROOF = ("#b8481a", "#8a3508", "#d9713a")
    GRASS = ("#7f8a3e", "#5e6830", "#9aa552")
    PATH = "#e0d2b8"
    WOOD = "#6b2c0a"
    GLASS = "#3a5a68"
    door = (X0 + 52, X0 + 74, 0, 40)
    wins_f = [(X0 + 14, X0 + 40, 16, 44), (X0 + 86, X0 + 112, 16, 44)]
    wins_s = [(Y0 + 18, Y0 + 44, 16, 44), (Y0 + 58, Y0 + 76, 16, 44)]
    trees = [(38, 58, 26), (220, 46, 22), (34, 150, 20)]
    layer_t = lambda k: 0.4 + (t_print - 0.4) * k / N
    path = []

    def opening(segments, x_or_y, z0, z1, wall_face, fill, frame=None):
        d, fr = "", ""
        for (u0, u1, zo0, zo1) in segments:
            za, zb_ = max(z0, zo0 + Hb), min(z1, zo1 + Hb)
            if za >= zb_:
                continue
            if wall_face == "f":
                pts = [(u0, x_or_y, za), (u1, x_or_y, za), (u1, x_or_y, zb_), (u0, x_or_y, zb_)]
            else:
                pts = [(x_or_y, u0, za), (x_or_y, u1, za), (x_or_y, u1, zb_), (x_or_y, u0, zb_)]
            d += a.poly(pts)
            if frame:
                um = (u0 + u1) / 2
                if wall_face == "f":
                    fr += a.poly([(um, x_or_y, za), (um, x_or_y, zb_)], close=False)
                else:
                    fr += a.poly([(x_or_y, um, za), (x_or_y, um, zb_)], close=False)
        if d:
            a.path(d, fill)
        if fr:
            a.path(fr, stroke=frame, sw=0.7)

    for k in range(N):
        z0, z1 = k * hl, (k + 1) * hl
        zc = (z0 + z1) / 2
        t_k = layer_t(k)
        kf = a.keyframes(f"l{k}", T, [(0, "opacity:0"), (t_k, "opacity:0"), (t_k + 0.04, "opacity:1"), (t_f0, "opacity:1"), (t_f1, "opacity:0"), (T, "opacity:0")])
        a.animate(f"{name}-l{k}", kf, T)
        a.open(cls=f"{name}-l{k}", op=None if zc < (Hb + Hw + Hr) * 0.64 else 0)
        if zc < Hb:
            a.box(BX0, BX1, BY0, BY1, z0, z1 + 0.3, front=GRASS[0], side=GRASS[1], top=GRASS[2])
            if z1 >= Hb:
                a.path(a.poly([(door[0] - 4, BY0, Hb), (door[1] + 4, BY0, Hb), (door[1] + 4, Y0, Hb), (door[0] - 4, Y0, Hb)]), PATH)
                d = ""
                for py in range(BY0 + 8, Y0, 10):
                    d += a.poly([(door[0] - 4, py, Hb), (door[1] + 4, py, Hb)], close=False)
                a.path(d, stroke="#b5a586", sw=0.5)
            area = (BX0, BY0, BX1, BY1)
        elif zc < Hb + Hw:
            a.box(X0, X1, Y0, Y1, z0, z1 + 0.3, front=a.lin3((X0, Y0, 0), (X1, Y0, 0), [(0, WALL[0]), (1, "#ece0c9")]), side=WALL[1], top=WALL[0])
            a.path(a.poly([(X0, Y0, z0), (X1, Y0, z0)], close=False) + a.poly([(X1, Y0, z0), (X1, Y1, z0)], close=False), stroke=WALL[2], sw=0.25)
            opening([door], Y0, z0, z1 + 0.3, "f", WOOD)
            opening(wins_f, Y0, z0, z1 + 0.3, "f", GLASS, "#f7eedd")
            opening(wins_s, X1, z0, z1 + 0.3, "s", mix(GLASS, "#000000", 0.2), "#d9c9ad")
            area = (X0, Y0, X1, Y1)
        else:
            j = (zc - Hb - Hw) / Hr
            ya = Y0 - eave + (Y1 - Y0 + 2 * eave) / 2 * j
            yb = Y1 + eave - (Y1 - Y0 + 2 * eave) / 2 * j
            xa, xb = X0 - eave, X1 + eave
            # Tejas: cada capa del techo alterna tono para que se lea el escalón de impresión.
            tone = ROOF[0] if k % 2 else mix(ROOF[0], ROOF[1], 0.35)
            a.box(xa, xb, ya, yb, z0, z1 + 0.3, front=tone, side=ROOF[1], top=ROOF[2])
            area = (xa, ya, xb, yb)
        if Hb + Hw + 14 <= z0 < Hb + Hw + Hr + 2:
            a.box(X1 - 40, X1 - 22, Y0 + 56, Y0 + 72, z0, z1 + 0.3, front="#a53a04", side="#6b2c0a", top="#d9713a")
        for (tx, ty, tr) in trees:
            if z0 < Hb:
                continue
            if zc < Hb + 18:
                a.path(a.cylz_path(tx, ty, z0, z1 + 0.3, 3.4), WOOD)
            else:
                u_ = (zc - Hb - 18) / (tr * 2.4)
                if u_ <= 1:
                    rt = tr * math.sqrt(max(0.02, 1 - (2 * u_ - 1) ** 2))
                    a.path(a.cylz_path(tx, ty, z0, z1 + 0.3, rt), a.lin_box([(0, GRASS[1]), (0.4, GRASS[0]), (1, GRASS[1])]))
                    a.ell_z(tx, ty, z1 + 0.3, rt, GRASS[2])
        a.close()
        if k % 2 == 0:
            xa, ya, xb, yb = area
            dt = (layer_t(min(N, k + 2)) - t_k) / 4
            for c, (px, py) in enumerate(((xa, ya), (xb, ya), (xb, yb), (xa, yb))):
                path.append((t_k + c * dt, px, py, z1))
    zb = (Hb + Hw + Hr) * 0.64
    cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
    park = (cx + 90, cy + 10, Hb + Hw + Hr + 24)
    path = [(0, *path[0][1:])] + path[1:]
    path += [(t_print + 0.8, *park), (T - 0.4, *park), (T, *path[0][1:])]
    path_motion(a, name, cx, cy, zb, path, T)
    a.open(cls=f"{name}-rail")
    x_rail(a, -240, 560, cy, zb + 84)
    a.close()
    a.open(cls=f"{name}-hxy")
    hot_end(a, cx, cy, zb)
    a.close()
    return a.write(ART)


def souvenirs(name="souvenirs", w=480, h=360):
    """Exhibidor de mostrador en MDF con los llaveros que salen del taller; los flexis se doblan en sus juntas."""
    PW, PH = 640, 500
    S, ox, oy = fit((22, 14), ((-40, PW + 40), (-90, 190), (0, 26 + PH)), w, h, mx=12, my=12)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    stage(a, shadow=a.p(PW * 0.52, 40, 0) + (w * 0.5, h * 0.1))

    grey = a.lin_box([(0, "#8f9496"), (0.38, "#d4d6d5"), (0.62, "#c3c6c6"), (1, "#83888a")])
    wings = a.lin_box([(0, "#868b8d"), (1, "#b4b7b8")])
    def vgrad(stops):
        i = a.nid()
        ss = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        a.defs.append(f'<linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1">{ss}</linearGradient>')
        return f"url(#{i})"
    yellow = vgrad([(0, "#f7c23a"), (1, "#d98a12")])
    teal = vgrad([(0, "#3fbdb0"), (0.55, "#2c8fb0"), (1, "#2b6aa8")])
    silk = vgrad([(0, "#2b6aa8"), (0.34, "#4b3f98"), (0.62, "#262c6a"), (1, "#171b42")])
    orange = vgrad([(0, "#f58a2a"), (1, "#d9530d")])
    orange2 = vgrad([(0, "#ee7420"), (1, "#c9470a")])

    defs = {
        "ring": '<circle cy="9" r="9" fill="none" stroke="#6d6a64" stroke-width="2.8"/><circle cy="9" r="9" fill="none" stroke="#efece6" stroke-width="1.1"/>',
        "stail": f'<rect x="-3" y="15" width="6" height="11" rx="2" fill="{wings}"/><path d="M-22 17C-12 21-6 28-4 46L4 46C6 28 12 21 22 17C13 18 6 21 0 26C-6 21-13 18-22 17Z" fill="{grey}" stroke="#6f7476" stroke-width=".8"/>',
        "srear": f'<path d="M-5 43C-13 51-22 62-24 79C-12 73 12 73 24 79C22 62 13 51 5 43Z" fill="{grey}" stroke="#6f7476" stroke-width=".8"/><path d="M-13 58C-6 55 6 55 13 58M-18 68C-8 64 8 64 18 68" fill="none" stroke="#fff" stroke-width=".7" opacity=".4"/>',
        "smid": f'<path d="M-29 91C-41 101-51 113-57 126C-44 126-32 120-25 108Z" fill="{wings}" stroke="#6f7476" stroke-width=".8"/><path d="M29 91C41 101 51 113 57 126C44 126 32 120 25 108Z" fill="{wings}" stroke="#6f7476" stroke-width=".8"/>'
                f'<path d="M-25 76C-34 88-34 104-30 117C-15 111 15 111 30 117C34 104 34 88 25 76C12 70-12 70-25 76Z" fill="{grey}" stroke="#4f5456" stroke-width="1.1"/><path d="M-27 90C-12 85 12 85 27 90M-29 102C-14 97 14 97 29 102" fill="none" stroke="#fff" stroke-width=".7" opacity=".4"/>'
                '<path d="M-7 107C-4 96-2 86 0 76C2 86 4 96 7 107C2 110-2 110-7 107Z" fill="#e6e7e5" stroke="#6f7476" stroke-width=".8"/>',
        "shead": f'<path d="M-30 115C-39 129-35 151-19 161C-6 168 6 168 19 161C35 151 39 129 30 115C14 108-14 108-30 115Z" fill="{grey}" stroke="#4f5456" stroke-width="1.1"/>'
                 '<path d="M-29 146C-15 157 15 157 29 146C25 156 13 167 0 167C-13 167-25 156-29 146Z" fill="#f6f4ee" stroke="#a9acac" stroke-width=".6"/>'
                 '<path d="M-24 128C-10 122 10 122 24 128" fill="none" stroke="#fff" stroke-width=".7" opacity=".4"/>'
                 '<circle cx="-21" cy="133" r="8" fill="#f6f4ee" stroke="#6f7476" stroke-width=".7"/><circle cx="-21" cy="133" r="5.2" fill="#1b1f21"/><circle cx="-19.3" cy="131.3" r="1.7" fill="#fff"/>'
                 '<circle cx="21" cy="133" r="8" fill="#f6f4ee" stroke="#6f7476" stroke-width=".7"/><circle cx="21" cy="133" r="5.2" fill="#1b1f21"/><circle cx="22.7" cy="131.3" r="1.7" fill="#fff"/>',
        "ftail": f'<rect x="-3" y="15" width="6" height="11" rx="2" fill="#d98a12"/><path d="M-24 18C-15 20-7 24-3 34L-3 46L3 46L3 34C7 24 15 20 24 18C18 32 11 40 0 45C-11 40-18 32-24 18Z" fill="{yellow}" stroke="#a9650c" stroke-width=".8"/><path d="M-13 25L-3 40M13 25L3 40M0 28V44" stroke="#a9650c" stroke-width=".6" opacity=".7"/>',
        "frear": f'<path d="M-8 43C-22 54-34 70-37 89C-20 83 20 83 37 89C34 70 22 54 8 43Z" fill="{teal}" stroke="#123e5a" stroke-width=".9"/><path d="M-21 62C-12 58-4 62 2 70M8 54C16 60 20 70 20 78" fill="none" stroke="#7a4ca0" stroke-width="2" opacity=".75"/><path d="M0 44C1 58 1 72 0 86" stroke="#123e5a" stroke-width="2" fill="none"/><path d="M-20 66C-26 74-29 80-31 87" fill="none" stroke="#fff" stroke-width="2" opacity=".28"/>',
        "ffront": f'<path d="M-38 99C-52 90-62 98-63 112C-53 116-44 114-36 108Z" fill="{yellow}" stroke="#a9650c" stroke-width=".8"/><path d="M38 99C52 90 62 98 63 112C53 116 44 114 36 108Z" fill="{yellow}" stroke="#a9650c" stroke-width=".8"/>'
                  f'<path d="M-37 87C-44 105-39 131-25 147C-12 157 12 157 25 147C39 131 44 105 37 87C20 80-20 80-37 87Z" fill="{silk}" stroke="#11183c" stroke-width="1"/><path d="M-30 96C-34 110-32 122-26 132" fill="none" stroke="#fff" stroke-width="2.4" opacity=".24"/><path d="M-22 92C-12 100-10 108-14 118M24 94C16 102 14 110 18 118" fill="none" stroke="#7a4ca0" stroke-width="2" opacity=".8"/>'
                  '<path d="M-4 92C-6 112-6 136-3 153L3 153C6 136 6 112 4 92Z" fill="#d8c9a6" opacity=".92"/>'
                  '<circle cx="-20" cy="127" r="11" fill="#dbe4cf" stroke="#11183c" stroke-width="1.4"/><circle cx="-20" cy="127" r="7" fill="#7f9f92"/><circle cx="-20" cy="127" r="4.2" fill="#10122a"/><circle cx="-18.2" cy="125" r="1.6" fill="#fff"/>'
                  '<circle cx="20" cy="127" r="11" fill="#dbe4cf" stroke="#11183c" stroke-width="1.4"/><circle cx="20" cy="127" r="7" fill="#7f9f92"/><circle cx="20" cy="127" r="4.2" fill="#10122a"/><circle cx="21.8" cy="125" r="1.6" fill="#fff"/>',
        "ctail": f'<rect x="-3" y="15" width="6" height="11" rx="2" fill="#c9470a"/><path d="M-23 19C-14 21-7 25-3 35L-3 46L3 46L3 35C7 25 14 21 23 19C18 32 11 40 0 45C-11 40-18 32-23 19Z" fill="{orange}" stroke="#1c1410" stroke-width="1.4"/>',
        "crear": f'<path d="M-8 43C-21 54-32 70-35 89C-20 83 20 83 35 89C32 70 21 54 8 43Z" fill="{orange}" stroke="#1c1410" stroke-width="1.1"/><path d="M-22 58C-10 54 10 54 22 58C25 62 27 66 28 71C12 66-12 66-28 71C-27 66-25 62-22 58Z" fill="#f8f4ea" stroke="#1c1410" stroke-width="1.2"/>',
        "cfront": f'<path d="M-37 99C-50 90-60 98-61 112C-51 116-43 114-35 108Z" fill="{orange}" stroke="#1c1410" stroke-width="1.2"/><path d="M37 99C50 90 60 98 61 112C51 116 43 114 35 108Z" fill="{orange}" stroke="#1c1410" stroke-width="1.2"/>'
                  f'<path d="M-36 87C-43 105-38 131-24 147C-12 157 12 157 24 147C38 131 43 105 36 87C20 80-20 80-36 87Z" fill="{orange2}" stroke="#1c1410" stroke-width="1.1"/>'
                  '<path d="M-38 96C-20 90 20 90 38 96L39 112C20 106-20 106-39 112Z" fill="#f8f4ea" stroke="#1c1410" stroke-width="1.2"/><path d="M-27 96C-30 106-29 114-27 122" fill="none" stroke="#fff" stroke-width="2" opacity=".2"/>'
                  '<circle cx="-18" cy="128" r="9" fill="#f8f4ea" stroke="#1c1410" stroke-width="1.2"/><circle cx="-18" cy="128" r="5.6" fill="#120c08"/><circle cx="-16.2" cy="126" r="1.7" fill="#fff"/>'
                  '<circle cx="18" cy="128" r="9" fill="#f8f4ea" stroke="#1c1410" stroke-width="1.2"/><circle cx="18" cy="128" r="5.6" fill="#120c08"/><circle cx="19.8" cy="126" r="1.7" fill="#fff"/>'
                  '<path d="M-7 145C-3 148 3 148 7 145" fill="none" stroke="#1c1410" stroke-width="1.4" stroke-linecap="round"/>',
    }
    # Llavero de la foto: pastilla negra con letras en relieve verde, blanco y rojo.
    letters = ""
    for i, (ch, col, dk) in enumerate(zip("CANCÚN", ("#2fa84f", "#f6f3ea", "#e8344a", "#2fa84f", "#f6f3ea", "#e8344a"), ("#14632c", "#a9a598", "#8e1626", "#14632c", "#a9a598", "#8e1626"))):
        for dx, fill in ((1.1, dk), (0, col)):
            letters += f'<text transform="translate({dx} {n(62 + i * 20.5)}) rotate(90)" text-anchor="middle" dy=".35em" font-family="DM Sans,system-ui,sans-serif" font-size="25" font-weight="800" fill="{fill}">{ch}</text>'
    defs["pill"] = ('<rect x="-19" y="15" width="43" height="160" rx="21" fill="#0c0d0e"/><rect x="-22" y="13" width="44" height="160" rx="22" fill="#26282b" stroke="#43464a" stroke-width=".8"/>'
                    '<circle cy="32" r="6" fill="#efe6d6" stroke="#0c0d0e" stroke-width="1.4"/>' + letters)
    defs["pillback"] = '<rect x="-22" y="13" width="44" height="160" rx="22" fill="#17181a" stroke="#43464a" stroke-width=".8"/>'
    rays = "".join(f'<line x1="{n(13 * math.cos(t))}" y1="{n(62 + 13 * math.sin(t))}" x2="{n(20 * math.cos(t))}" y2="{n(62 + 20 * math.sin(t))}"/>' for t in [i * math.pi / 5 for i in range(10)])
    defs["wood"] = (f'<rect x="-40" y="17" width="86" height="136" rx="18" fill="#8a6238"/><rect x="-43" y="15" width="86" height="136" rx="18" fill="#d9ad7a" stroke="#7d5730" stroke-width="1.3"/>'
                    '<path d="M-41 44C-20 40 16 48 41 42M-42 84C-16 80 12 90 42 82M-42 118C-14 114 16 124 42 116" fill="none" stroke="#b48a58" stroke-width=".8"/>'
                    '<circle cy="29" r="5.5" fill="#efe6d6" stroke="#7d5730" stroke-width="1.2"/>'
                    f'<g stroke="#5a2c0c" stroke-width="2" fill="none" stroke-linecap="round"><circle cy="62" r="9.5" fill="#5a2c0c" fill-opacity=".85"/>{rays}'
                    '<path d="M-24 134C-18 129-12 129-6 134S6 139 12 134S20 129 25 133"/><path d="M-19 141C-13 137-8 137-2 141S9 145 15 141"/></g>'
                    '<text y="108" text-anchor="middle" font-family="Playfair Display,Georgia,serif" font-size="16" font-weight="700" letter-spacing="1" fill="#5a2c0c">CANCÚN</text>')
    sil = {
        "pill": '<rect x="-22" y="13" width="44" height="160" rx="22"/>',
        "wood": '<rect x="-43" y="15" width="86" height="136" rx="18"/>',
        "shark": '<path d="M-22 17L22 17L24 79L30 91L57 126L30 120L19 161L0 168L-19 161L-30 120L-57 126L-30 91L-24 79Z"/>',
        "fish": '<path d="M-24 18L24 18L37 87L63 112L36 110L25 147L0 156L-25 147L-36 110L-63 112L-37 87Z"/>',
    }
    a.defs.append("".join(f'<g id="{name}-{k}">{v}</g>' for k, v in defs.items()))
    a.defs.append("".join(f'<g id="{name}-sil-{k}">{v}</g>' for k, v in sil.items()))
    use = lambda k: f'<use href="#{name}-{k}"/>'
    sway = a.keyframes("sway", 1, [(0, "transform:rotate(-4deg)"), (1, "transform:rotate(4deg)")])
    flex = a.keyframes("flex", 1, [(0, "transform:rotate(-5deg)"), (1, "transform:rotate(5deg)")])

    def swing(cls, kf, dur, delay, origin=None):
        rule = f".{cls}{{animation:{kf} {dur}s cubic-bezier(.37,0,.63,1) infinite alternate;animation-delay:{delay}s;animation-play-state:var(--play,running)"
        if origin:
            rule += f";transform-origin:0 {origin}px"
        a.css.append(rule + "}")

    a.rbox(-40, PW + 40, -90, 190, 0, 26, 12, MDF[1], MDF[2], MDF[0], edge=MDF[3], sw=0.7, shade_f=MDF[1], shade_s=MDF[2])
    d = ""
    for gy in range(-70, 190, 40):
        d += a.poly([(-30, gy, 26), (PW + 30, gy, 26)], close=False)
    a.path(d, stroke=MDF[3], sw=0.3, op=0.3)
    a.path(a.poly([(PW - 8, 20, 26), (PW - 8, 170, 26), (PW - 8, 20, 360)]), MDF[2], stroke=MDF[3], sw=0.6)
    a.box(0, PW, 0, 20, 26, 26 + PH, front=a.lin3((0, 0, 26 + PH), (PW, 0, 26), [(0, "#e4bb88"), (0.6, "#d3a673"), (1, "#c49264")]), side=MDF[2], top=MDF[0], stroke=MDF[3], sw=0.7)
    d = ""
    for tx in range(30, PW - 40, 96):
        d += a.poly([(tx, -0.5, 26), (tx + 48, -0.5, 26), (tx + 48, -0.5, 40), (tx, -0.5, 40)])
    a.path(d, MDF[2], stroke=MDF[3], sw=0.4)
    d = ""
    for gz in range(62, PH, 34):
        d += a.poly([(6, 0, gz), (PW - 6, 0, gz + 6)], close=False)
    a.path(d, stroke=MDF[3], sw=0.3, op=0.26)
    a.path(a.rr((10, 0, 46), (1, 0, 0), (0, 0, 1), PW - 20, PH - 30, 8), stroke=MDF[3], sw=0.5, op=0.5)
    Zl0, Zl1 = 26 + PH - 92, 26 + PH - 16
    a.box(18, PW - 18, -12, 0, Zl0, Zl1, front=a.lin3((18, -12, 0), (PW - 18, -12, 0), [(0, "#cf5a1e"), (0.5, "#A53A04"), (1, "#7d2b02")]), top="#e07a3d", side="#5a1d00")
    a.open(tf=a.matrix((PW / 2, -12, Zl0 + 20), (1, 0, 0), (0, 0, -1)))
    a.add('<text x="2" y="2" text-anchor="middle" font-family="Playfair Display,Georgia,serif" font-size="50" font-weight="700" letter-spacing="10" fill="#4a1800" opacity=".55">CANCÚN</text>')
    a.add(f'<text text-anchor="middle" font-family="Playfair Display,Georgia,serif" font-size="50" font-weight="700" letter-spacing="10" fill="{CREAM}">CANCÚN</text>')
    a.close()
    bolts = ""
    for bx in (34, PW - 34):
        for bz in (Zl0 + 14, Zl1 - 14):
            q = a.p(bx, -12, bz)
            bolts += f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="2.2" fill="#e8e5df" stroke="#6d6a64" stroke-width=".5"/><path d="M{n(q[0] - 1.2)} {n(q[1])}h2.4" stroke="#6d6a64" stroke-width=".5"/>'
    a.add(bolts)

    COLS = [84 + i * 118 for i in range(5)]
    ROWS = [26 + PH - 118, 26 + PH - 304]
    grid = [("pill", "wood"), ("shark", "fish"), ("fish", "pill"), ("clown", "shark"), ("wood", "clown")]

    def item_static(kind):
        parts = {"pill": ["pill"], "wood": ["wood"], "shark": ["stail", "srear", "smid", "shead"], "fish": ["ftail", "frear", "ffront"], "clown": ["ctail", "crear", "cfront"]}[kind]
        return "".join(use(k) for k in parts)

    def item_live(kind, tag, dur):
        if kind in ("pill", "wood"):
            return use(kind)
        if kind == "shark":
            swing(f"{tag}a", flex, round(dur * 0.9, 2), -0.3, 44)
            swing(f"{tag}b", flex, round(dur * 0.76, 2), -0.8, 78)
            swing(f"{tag}c", flex, round(dur * 0.64, 2), -0.2, 113)
            return use("stail") + f'<g class="{tag}a">' + use("srear") + f'<g class="{tag}b">' + use("smid") + f'<g class="{tag}c">' + use("shead") + "</g></g></g>"
        t_, r_, f_ = ("ftail", "frear", "ffront") if kind == "fish" else ("ctail", "crear", "cfront")
        swing(f"{tag}a", flex, round(dur * 0.84, 2), -0.5, 45)
        swing(f"{tag}b", flex, round(dur * 0.68, 2), -0.1, 86)
        return use(t_) + f'<g class="{tag}a">' + use(r_) + f'<g class="{tag}b">' + use(f_) + "</g></g>"

    def hook(cx, z):
        q = a.p(cx, 0, z)
        hole = f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="3" fill="#3d2a18"/>'
        tip = a.p(cx, -16, z)
        peg = f'<path d="M{n(q[0])} {n(q[1])}L{n(tip[0])} {n(tip[1])}" stroke="#55524c" stroke-width="3.2" stroke-linecap="round"/><path d="M{n(q[0])} {n(q[1])}L{n(tip[0])} {n(tip[1])}" stroke="#d8d5cf" stroke-width="1.3" stroke-linecap="round"/>'
        return hole, peg

    durs = [2.3, 2.9, 2.5, 3.1, 2.1, 2.7, 3.3, 2.2, 2.8, 2.4]
    delays = [-0.4, -1.3, -2.1, -0.9, -1.7, -0.2, -2.6, -1.1, -0.6, -1.9]
    idx = 0
    # Fila de arriba primero: los de abajo tapan la punta de los que cuelgan encima.
    for r_, z in enumerate(ROWS):
        for col, (top_kind, low_kind) in zip(COLS, grid):
            kind = top_kind if r_ == 0 else low_kind
            hole, peg = hook(col, z)
            a.add(hole)
            shape = {"clown": "fish"}.get(kind, kind)
            tf = a.matrix((col, -9, z), (1, 0, 0), (0, 0, -1))
            # Un segundo llavero detrás, quieto: en el mostrador nunca hay uno solo.
            a.open(tf=tf)
            a.add(f'<g transform="rotate(5) translate(4 3)" opacity=".2" fill="#1a0f06"><use href="#{name}-sil-{shape}"/></g>')
            a.add(f'<g transform="rotate(5) translate(2 1)">{use("pillback") if kind == "pill" else item_static(kind)}</g>')
            a.close()
            tag = f"{name}-i{idx}"
            dur, delay = durs[idx], delays[idx]
            swing(tag, sway, dur, delay, 9)
            a.open(tf=tf)
            a.open(cls=tag)
            a.add(f'<g transform="translate(6 8)" opacity=".24" fill="#1a0f06"><use href="#{name}-sil-{shape}"/></g>')
            a.add(use("ring"))
            a.add(item_live(kind, tag, dur))
            a.close()
            a.close()
            a.add(peg)
            idx += 1
    return a.write(ART)


def tresd_proceso(name="tresd-proceso", w=560, h=640):
    """«Capa por capa»: el scroll decide cuántas capas hay y dónde va la boquilla (ver TresDAssembly.astro)."""
    Zh, N = 300, 44
    S, ox, oy = fit((24, 20), ((-44, 322), (-6, 234), (-13, Zh + 186)), w, h, mx=4, my=4)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    cx, cy = 136, 114
    q = a.p(cx + 8, cy, -30)
    sh = a.rad(q[0], q[1], w * 0.52, [(0, "#1a0f06", 0.3), (0.6, "#1a0f06", 0.12), (1, "#1a0f06", 0)], ry=h * 0.11)
    a.add(f'<ellipse cx="{n(q[0])}" cy="{n(q[1])}" rx="{n(w * 0.52)}" ry="{n(h * 0.11)}" fill="{sh}"/>')

    # Columnas del pórtico; se desvanecen arriba para no cortarse contra la orilla del dibujo.
    top = Zh + 180

    def column(x0):
        x1, y0, y1 = x0 + 24, cy + 20, cy + 44
        fade = lambda col: a.lin3((x0, y0, top), (x0, y0, -13), [(0, col, 0), (0.28, col, 1), (1, col, 1)])
        a.path(a.poly([(x1, y0, -13), (x1, y1, -13), (x1, y1, top), (x1, y0, top)]), fade("#100c09"))
        a.path(a.poly([(x0, y0, -13), (x1, y0, -13), (x1, y0, top), (x0, y0, top)]), fade("#231d18"))
        a.path(a.poly([(x0 + 8, y0 - 0.5, -13), (x1 - 8, y0 - 0.5, -13), (x1 - 8, y0 - 0.5, top), (x0 + 8, y0 - 0.5, top)]), fade("#a9a296"))

    column(-44)
    plate_mini(a, 0, 272, 0, 228, 0)
    column(292)

    # La malla del modelo digital va detrás de las capas: así se va llenando al imprimir.
    d = ""
    for i in range(0, 16):
        z = i * Zh / 15
        r = catmull(VASE, z / Zh)
        d += a.ellipse_z(cx, cy, z, r)
    for j in range(10):
        ang = j * math.pi / 5 + 0.3
        pts = []
        for i in range(0, 13):
            z = i * Zh / 12
            r = catmull(VASE, z / Zh)
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang), z))
        d += a.poly(pts, close=False)
    left, right = [], []
    for i in range(0, 25):
        z = i * Zh / 24
        r = catmull(VASE, z / Zh)
        qc = a.p(cx, cy, z)
        left.append((qc[0] - r * a.S, qc[1]))
        right.append((qc[0] + r * a.S, qc[1]))
    sil = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in left) + "M" + "L".join(f"{n(x)} {n(y)}" for x, y in right)
    bx0, bx1, by0, by1 = cx - 84, cx + 84, cy - 84, cy + 84
    box = ""
    for (p0, p1) in (((bx0, by0), (bx1, by0)), ((bx1, by0), (bx1, by1)), ((bx1, by1), (bx0, by1)), ((bx0, by1), (bx0, by0))):
        box += a.poly([(*p0, 0), (*p1, 0)], close=False) + a.poly([(*p0, Zh), (*p1, Zh)], close=False) + a.poly([(*p0, 0), (*p0, Zh)], close=False)
    a.add('<g data-wire="" opacity="0">')
    a.path(box, stroke=RUST, sw=0.6, op=0.4)
    a.path(d, stroke=RUST, sw=0.55, op=0.55)
    a.path(sil, stroke=RUST, sw=1.1)
    dots = ""
    for (px, py) in ((bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)):
        for pz in (0, Zh):
            q = a.p(px, py, pz)
            dots += f'<rect x="{n(q[0] - 2)}" y="{n(q[1] - 2)}" width="4" height="4" fill="#fff" stroke="{RUST}" stroke-width=".8"/>'
    a.add(dots)
    a.add("</g>")

    def group(k, u):
        a.add(f'<g data-layer="{k}">')

    vase_layers(a, cx, cy, Zh, N, group)

    outline = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in left) + "L" + "L".join(f"{n(x)} {n(y)}" for x, y in reversed(right)) + "Z"
    clip = a.clip(outline)
    qb = a.p(cx, cy, Zh / 2)
    band = a.lin(qb[0] - 60, qb[1], qb[0] + 60, qb[1], [(0, "#fff8ea", 0), (0.5, "#fff8ea", 0.75), (1, "#fff8ea", 0)])
    a.open(clip=clip)
    a.add(f'<path data-shine="" opacity="0" d="M{n(qb[0] - 60)} {n(qb[1] - 300)}h70l50 600h-70Z" fill="{band}" transform="translate(-140 0)"/>')
    a.close()

    park = (110.0, 10.0, Zh + 44.0)
    gr = a.v(0, 0, park[2])
    gh = a.v(park[0], park[1], park[2])
    a.add(f'<g data-rail="" transform="translate({gr[0]:.1f} {gr[1]:.1f})">')
    x_rail(a, -40, 312, cy, 84)
    a.box(-48, -16, cy + 16, cy + 48, 66, 102, front="#1b1612", side="#100c09", top="#352c25")
    a.box(288, 320, cy + 16, cy + 48, 66, 102, front="#1b1612", side="#100c09", top="#352c25")
    a.add("</g>")
    a.add(f'<g data-head="" transform="translate({gh[0]:.1f} {gh[1]:.1f})">')
    hot_end(a, cx, cy, 0, glow_attr=' data-glow="" opacity="0"')
    a.add("</g>")

    radii = ",".join(n(catmull(VASE, (k + 0.5) / N)) for k in range(N))
    a.root_attrs = {
        "data-v": projection_attr(a),
        "data-radii": radii,
        "data-h": n(Zh / N),
        "data-park": ",".join(n(v) for v in park),
    }
    return a.write(ART)


def projection_attr(a):
    """Lo que necesita src/scripts/assembly.ts para mover piezas en milímetros: pantalla = (xx·x + xy·y, yx·x + yy·y + yz·z)."""
    return ",".join(f"{v:.4f}" for v in (a.S * pa.CA, a.S * pa.SA, a.S * pa.SA * pa.SE, -a.S * pa.CA * pa.SE, -a.S * pa.CE))


def cone(a, x, y, z0, z1, r0, r1, fill):
    """Cono vertical: su silueta llega a los extremos horizontales de pantalla, no a los del eje X."""
    side = lambda r, z, s: (x + s * r * pa.CA, y + s * r * pa.SA, z)
    a.path(a.poly([side(r0, z0, -1), side(r0, z0, 1), side(r1, z1, 1), side(r1, z1, -1)]), fill)


def laser_proceso(name="laser-proceso", w=640, h=556):
    """«De la lámina a la serie»: el scroll mueve el pórtico, corta los hexágonos y apila las piezas (ver LaserAssembly.astro)."""
    W, D, Zf, Hh = 900, 700, 70, 150
    Xw0, Xw1, Yw0, Yw1 = 50, 850, 34, 680
    Zbed, T = 44, 9
    Zs = Zbed + T
    SX0, SX1, SY0, SY1 = 110, 790, 56, 656
    S, ox, oy = fit_points((24, 34), [(0, 0, 0), (28, 786, Hh + 300), (W, D + 90, 0), (W, D + 90, Hh), (W, 0, 0), (44, -196, 0), (594, -196, 0)], w, h, mx=8, my=6)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)

    q = a.p(W * 0.46, D * 0.3, -10)
    sh = a.rad(q[0], q[1], w * 0.47, [(0, "#1a0f06", 0.34), (0.62, "#1a0f06", 0.16), (1, "#1a0f06", 0)], ry=h * 0.33)
    a.add(f'<ellipse cx="{n(q[0])}" cy="{n(q[1])}" rx="{n(w * 0.47)}" ry="{n(h * 0.33)}" fill="{sh}"/>')

    a.path(a.poly([(0, D, Hh), (W, D, Hh), (W, D + 90, Hh), (0, D + 90, Hh)]), NAVY[1])
    Lx0, Lx1, Ly0, Ly1, Lz0, Lz1 = 28, W - 28, 738, 786, Hh, Hh + 300
    lid = lambda x, t: (x, Ly0 + (Ly1 - Ly0) * t, Lz0 + (Lz1 - Lz0) * t)
    a.path(a.poly([lid(Lx1, 0), lid(Lx1, 1), add3(lid(Lx1, 1), (0, 12, 0)), add3(lid(Lx1, 0), (0, 12, 0))]), NAVY[3])
    pane = a.poly([lid(Lx0, 0), lid(Lx1, 0), lid(Lx1, 1), lid(Lx0, 1)])
    a.path(pane, a.lin3(lid(0, 1), lid(0, 0), [(0, "#e8912f", 0.5), (0.6, "#d0822c", 0.58), (1, "#9a5518", 0.72)]))
    a.open(clip=a.clip(pane))
    for x0, wd, op in ((150, 150, 0.16), (340, 54, 0.12), (620, 96, 0.1)):
        a.path(a.poly([lid(x0, 0), lid(x0 + wd, 0), lid(x0 + wd + 170, 1), lid(x0 + 170, 1)]), "#fff6e6", op=op)
    a.close()
    bar, tb = 22, 22 / (Lz1 - Lz0)
    a.path(a.poly([lid(Lx0, 0), lid(Lx1, 0), lid(Lx1, tb), lid(Lx0, tb)]), NAVY[2])
    a.path(a.poly([lid(Lx0, 0), lid(Lx0 + bar, 0), lid(Lx0 + bar, 1), lid(Lx0, 1)]), NAVY[2])
    a.path(a.poly([lid(Lx1 - bar, 0), lid(Lx1, 0), lid(Lx1, 1), lid(Lx1 - bar, 1)]), NAVY[1])
    a.path(a.poly([lid(Lx0, 1 - tb), lid(Lx1, 1 - tb), lid(Lx1, 1), lid(Lx0, 1)]), NAVY[0])
    a.path(a.rr(lid(W / 2 - 110, 0.905), (1, 0, 0), (0, (Ly1 - Ly0) / 303.8, (Lz1 - Lz0) / 303.8), 220, 13, 6), STEEL[0], stroke=NAVY[3], sw=0.5)
    p0, p1, p2 = a.p(Lx1 + 8, Ly0 - 26, Hh), a.p(Lx1 + 8, Ly0 - 8, Hh + 92), a.p(Lx1 + 8, Ly0 + 16, Hh + 186)
    a.add(f'<path d="M{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}" stroke="{STEEL[0]}" stroke-width="1.5" stroke-linecap="round"/>')
    a.add(f'<path d="M{n(p0[0])} {n(p0[1])}L{n(p1[0])} {n(p1[1])}" stroke="{NAVY[3]}" stroke-width="3.4" stroke-linecap="round"/>')
    a.path(a.poly([(0, D, Zf), (W, D, Zf), (W, D, Hh), (0, D, Hh)]), a.lin3((0, D, Hh), (0, D, Zf), [(0, NAVY[0]), (1, NAVY[2])]))
    a.path(a.poly([(0, D, Hh), (W, D, Hh)], close=False), stroke="#6d7796", sw=0.7)
    d = ""
    for vz in range(Zf + 22, Hh - 14, 11):
        d += a.poly([(90, D, vz), (300, D, vz)], close=False)
    a.path(d, stroke=NAVY[3], sw=1.1)

    Zw = Zbed - 14
    a.path(a.poly([(Xw0, Yw1, Zw), (Xw1, Yw1, Zw), (Xw1, Yw1, Zf), (Xw0, Yw1, Zf)]), a.lin3((0, Yw1, Zf), (0, Yw1, Zw), [(0, "#6e6256"), (1, "#2a231d")]))
    a.path(a.poly([(Xw0, Yw0, Zw), (Xw0, Yw1, Zw), (Xw0, Yw1, Zf), (Xw0, Yw0, Zf)]), a.lin3((Xw0, Yw0, Zf), (Xw0, Yw1, Zw), [(0, "#55493e"), (1, "#1f1914")]))
    a.path(a.poly([(Xw0, Yw0, Zw), (Xw1, Yw0, Zw), (Xw1, Yw1, Zw), (Xw0, Yw1, Zw)]), "#100c09")
    blades = lambda ys, y0, y1, dz=0: "".join(a.poly([(sx, y0, Zbed + dz), (sx, y1, Zbed + dz)], close=False) for sx in ys)
    grid = range(Xw0 + 12, Xw1, 20)
    a.path(blades(grid, Yw0, Yw1, -5), stroke="#2c241d", sw=1.2)
    a.path(blades(grid, Yw0, Yw1), stroke="#85786a", sw=0.7)

    cx0, cx1 = 806, 838
    a.box(cx0, cx1, 44, 668, Zbed + 2, Zbed + 24, side="#14100c", top="#2a2622")
    d = ""
    for cy_ in range(52, 660, 22):
        d += a.poly([(cx0, cy_, Zbed + 24), (cx1, cy_, Zbed + 24)], close=False)
    a.path(d, stroke="#6e6256", sw=0.6)

    a.path(a.poly([(SX0 + 8, SY0 - 10, Zbed), (SX1 + 10, SY0 - 10, Zbed), (SX1 + 10, SY1 - 6, Zbed), (SX0 + 8, SY1 - 6, Zbed)]), "#060403", op=0.55)
    a.path(a.poly([(SX0, SY0, Zbed), (SX1, SY0, Zbed), (SX1, SY0, Zs), (SX0, SY0, Zs)]), MDF[2])
    a.path(a.poly([(SX1, SY0, Zbed), (SX1, SY1, Zbed), (SX1, SY1, Zs), (SX1, SY0, Zs)]), MDF[3])
    sheet = a.poly([(SX0, SY0, Zs), (SX1, SY0, Zs), (SX1, SY1, Zs), (SX0, SY1, Zs)])
    a.path(sheet, a.lin3((SX0, SY1, Zs), (SX1, SY0, Zs), [(0, "#e2b98a"), (0.55, MDF[0]), (1, "#c79a68")]))
    d = ""
    for i, gy in enumerate(range(SY0 + 16, SY1, 34)):
        wob = (i * 37) % 11 - 5
        d += a.poly([(SX0, gy, Zs), (SX1, gy + wob, Zs)], close=False)
    a.path(d, stroke=MDF[3], sw=0.35, op=0.3)

    R, web = 60, 20
    hh = R * math.sqrt(3) / 2
    HEXV = [(-R / 2, -hh), (R / 2, -hh), (R, 0), (R / 2, hh), (-R / 2, hh), (-R, 0)]
    col_pitch, row_pitch = 1.5 * R + web * math.sqrt(3) / 2, 2 * hh + web
    COLS, ROWS = 5, 4
    x0_ = (SX0 + SX1) / 2 - (COLS - 1) * col_pitch / 2
    y0_ = (SY0 + SY1) / 2 - ((ROWS - 1) * row_pitch + row_pitch / 2) / 2
    cells = []
    # De adelante hacia atrás y en zigzag: es el recorrido corto, y al levantar las piezas
    # en este orden ninguna vuela por encima de otra que siga en su lugar.
    for j in range(ROWS):
        for i in range(COLS) if j % 2 == 0 else reversed(range(COLS)):
            cells.append((x0_ + i * col_pitch, y0_ + j * row_pitch + (row_pitch / 2 if i % 2 else 0)))
    hex_at = lambda cx, cy, z: [(cx + vx, cy + vy, z) for vx, vy in HEXV]
    lengths = [math.hypot(*a.v(HEXV[(i + 1) % 6][0] - HEXV[i][0], HEXV[(i + 1) % 6][1] - HEXV[i][1], 0)) for i in range(6)]
    fr, acc = [0.0], 0.0
    for ln in lengths:
        acc += ln
        fr.append(acc / sum(lengths))
    edges = []
    for i in range(6):
        (x0, y0), (x1, y1) = HEXV[i], HEXV[(i + 1) % 6]
        nx, ny = (y1 - y0) / R, -(x1 - x0) / R
        edges.append(((x0, y0), (x1, y1), nx * pa.SA - ny * pa.CA))

    # Huecos: lo que se ve abajo sale de las mismas coordenadas, así el paralaje es el real.
    for k, (cx, cy) in enumerate(cells):
        a.add(f'<g data-hole="{k}" clip-path="url(#{a.clip(a.poly(hex_at(cx, cy, Zs)))})">')
        a.path(a.poly(hex_at(cx, cy, Zs)), "#14100c")
        ys = [sx for sx in grid if cx - R - 40 < sx < cx + R + 40]
        a.path(blades(ys, cy - hh - 40, cy + hh + 40, -5), stroke="#2c241d", sw=1.2)
        a.path(blades(ys, cy - hh - 40, cy + hh + 40), stroke="#85786a", sw=0.7)
        for (x0, y0), (x1, y1), facing in edges:
            if facing < 0:
                tone = "#3f2410" if facing > -0.5 else "#7a4a22" if y0 + y1 > R else "#5f3717"
                a.path(a.poly([(cx + x0, cy + y0, Zs), (cx + x1, cy + y1, Zs), (cx + x1, cy + y1, Zbed), (cx + x0, cy + y0, Zbed)]), tone)
        a.close()

    # El corte que deja el láser: el script revela cada trazo conforme pasa la boquilla.
    for k, (cx, cy) in enumerate(cells):
        a.add(f'<path data-cut="{k}" data-c="{n(cx)},{n(cy)}" d="{a.poly(hex_at(cx, cy, Zs))}" fill="none" stroke="#2f1405" stroke-width="1.15" stroke-linejoin="round" pathLength="100" stroke-dasharray="100"/>')
    a.add('<path data-hot="" style="display:none" fill="none" stroke="#ff9a3c" stroke-width="2" stroke-linecap="round" pathLength="100" stroke-dasharray="9 200"/>')

    # El cuerpo va después de la lámina: lo más cercano a la cámara tapa la orilla de la cama.
    ring = a.poly([(0, 0, Zf), (W, 0, Zf), (W, D, Zf), (0, D, Zf)]) + a.poly([(Xw0, Yw0, Zf), (Xw1, Yw0, Zf), (Xw1, Yw1, Zf), (Xw0, Yw1, Zf)])
    a.add(f'<path d="{ring}" fill="{NAVY[0]}" fill-rule="evenodd"/>')
    a.path(a.poly([(Xw0, Yw0, Zf), (Xw1, Yw0, Zf), (Xw1, Yw1, Zf), (Xw0, Yw1, Zf)]), stroke="#6d7796", sw=0.7)
    a.path(a.poly([(W, 0, 0), (W, D, 0), (W, D + 90, 0), (W, D + 90, Hh), (W, D, Hh), (W, D, Zf), (W, 0, Zf)]), a.lin3((W, 0, Zf), (W, D, 0), [(0, NAVY[1]), (1, NAVY[3])]))
    a.path(a.poly([(0, 0, 0), (W, 0, 0), (W, 0, Zf), (0, 0, Zf)]), a.lin3((0, 0, Zf), (0, 0, 0), [(0, NAVY[1]), (1, NAVY[2])]))
    a.path(a.poly([(0, 0, Zf), (W, 0, Zf)], close=False), stroke=STEEL[0], sw=1)
    a.path(a.poly([(W, 0, Zf), (W, D, Zf)], close=False), stroke="#6d7796", sw=0.7)
    d = ""
    for vz in (20, 32, 44):
        d += a.poly([(650, 0, vz), (850, 0, vz)], close=False)
    a.path(d, stroke=NAVY[3], sw=1.2)
    a.path(a.rr((60, 0, 22), (1, 0, 0), (0, 0, 1), 110, 26, 3), STEEL[1], stroke=NAVY[3], sw=0.4)
    d = ""
    for rx in range(Xw0 + 20, Xw1, 40):
        d += a.poly([(rx, 16 if (rx - Xw0 - 20) % 200 == 0 else 24, Zf), (rx, Yw0 - 2, Zf)], close=False)
    a.path(d, stroke="#c4cbdc", sw=0.6, op=0.8)

    for rx in (18, W - 54):
        a.box(rx, rx + 36, 6, D - 6, Zf, Zf + 12, front=NAVY[2], side=NAVY[3], top=STEEL[0])
        d = ""
        for by in range(30, D - 10, 60):
            qb = a.p(rx + 18, by, Zf + 12)
            d += f'<circle cx="{n(qb[0])}" cy="{n(qb[1])}" r=".9"/>'
        a.add(f'<g fill="#5e5a54">{d}</g>')

    # La sombra del pórtico se recorta a la lámina: al viajar, no debe caer sobre el cuerpo de la máquina.
    Gy = 640
    Zg = Zs + 122
    hx, hy = 450, Gy - 33
    a.open(clip=a.clip(sheet))
    a.add('<g data-gantry-shadow="">')
    a.path(a.poly([(SX0 - 20, Gy - 24, Zs), (SX1 + 20, Gy - 24, Zs), (SX1 + 20, Gy + 44, Zs), (SX0 - 20, Gy + 44, Zs)]), "#1a0f06", op=0.16)
    a.close()
    a.close()
    a.add('<g data-gantry="">')
    leg = a.lin3((0, Gy - 8, Zg + 24), (0, Gy - 8, Zf + 12), [(0, NAVY[0]), (1, NAVY[2])])
    a.box(14, 58, Gy - 8, Gy + 62, Zf + 12, Zg + 24, front=leg, side=NAVY[2], top=NAVY[0])
    a.box(58, W - 58, Gy, Gy + 50, Zg - 22, Zg + 22, front=a.lin3((0, Gy, Zg + 22), (0, Gy, Zg - 22), [(0, NAVY[0]), (1, NAVY[2])]), top=NAVY[1])
    a.path(a.poly([(58, Gy, Zg + 6), (W - 58, Gy, Zg + 6), (W - 58, Gy, Zg - 4), (58, Gy, Zg - 4)]), a.lin3((0, Gy, Zg + 6), (0, Gy, Zg - 4), [(0, STEEL[0]), (1, STEEL[2])]))
    d = ""
    for bx in range(80, W - 70, 56):
        qb = a.p(bx, Gy, Zg + 1)
        d += f'<circle cx="{n(qb[0])}" cy="{n(qb[1])}" r=".8"/>'
    a.add(f'<g fill="#4a4640">{d}</g>')
    a.box(W - 58, W - 14, Gy - 8, Gy + 62, Zf + 12, Zg + 24, front=leg, side=NAVY[3], top=NAVY[0])

    a.add('<g data-head="">')
    az = math.degrees(pa.AZ)
    a.box(hx - 48, hx + 48, Gy - 14, Gy, Zg - 36, Zg + 36, front=a.lin3((hx - 48, Gy - 14, 0), (hx + 48, Gy - 14, 0), [(0, STEEL[0]), (1, STEEL[1])]), side=STEEL[2], top="#efece6")
    d = ""
    for (bx, bz) in ((hx - 40, Zg + 28), (hx + 40, Zg + 28), (hx - 40, Zg - 28), (hx + 40, Zg - 28)):
        qb = a.p(bx, Gy - 14, bz)
        d += f'<circle cx="{n(qb[0])}" cy="{n(qb[1])}" r="1"/>'
    a.add(f'<g fill="#55524c">{d}</g>')
    a.path(a.cylz_path(hx, hy, Zs + 150, Zs + 168, 15), a.cylz_grad(hx, hy, 0, 15, [(0, "#6d6a64"), (0.42, "#f2efe9"), (1, "#6d6a64")]))
    a.ell_z(hx, hy, Zs + 168, 15, "#d8d5cf", stroke="#6d6a64", sw=0.4)
    a.ell_z(hx, hy, Zs + 168, 9, "#8d8a84")
    a.rbox(hx - 28, hx + 28, hy - 19, hy + 19, Zs + 84, Zs + 150, 6, a.lin3((hx - 28, hy - 19, 0), (hx + 28, hy - 19, 0), [(0, NAVY[0]), (1, NAVY[1])]), NAVY[3], NAVY[0], edge=NAVY[3], sw=0.4, shade_f=NAVY[1], shade_s=NAVY[3])
    a.path(a.rr((hx - 20, hy - 19, Zs + 128), (1, 0, 0), (0, 0, 1), 22, 12, 2), "#7f8bb0", op=0.55)
    a.path(a.cylz_path(hx, hy, Zs + 48, Zs + 84, 13), a.cylz_grad(hx, hy, 0, 13, [(0, "#77756f"), (0.42, "#f2efe9"), (1, "#77756f")]))
    d = ""
    for rz in range(Zs + 56, Zs + 84, 6):
        d += a.arc((hx, hy, rz), (13, 0, 0), (0, 13, 0), az - 180, az)
    a.path(d, stroke="#6d6a64", sw=0.5)
    brass = a.cylz_grad(hx, hy, 0, 9, [(0, "#8a5a18"), (0.45, "#f6cf8e"), (1, "#8a5a18")])
    a.path(a.cylz_path(hx, hy, Zs + 38, Zs + 48, 9), brass)
    cone(a, hx, hy, Zs + 38, Zs + 26, 9, 3, brass)
    h0, h1, h2, h3 = a.p(hx + 26, hy - 19, Zs + 96), a.p(hx + 56, hy - 30, Zs + 86), a.p(hx + 36, hy - 24, Zs + 40), a.p(hx + 9, hy, Zs + 43)
    tube = f"M{n(h0[0])} {n(h0[1])}C{n(h1[0])} {n(h1[1])} {n(h2[0])} {n(h2[1])} {n(h3[0])} {n(h3[1])}"
    a.add(f'<path d="{tube}" fill="none" stroke="#6d6458" stroke-width="2.6" stroke-linecap="round"/><path d="{tube}" fill="none" stroke="#efe9df" stroke-width="1.4" stroke-linecap="round"/>')

    tip = a.p(hx, hy, Zs)
    beam = a.v(0, 0, 26)
    a.add(f'<g data-tip="" style="display:none" transform="translate({tip[0]:.1f} {tip[1]:.1f})">')
    a.add(f'<path d="M0 0L{n(beam[0])} {n(beam[1])}" stroke="#ff7a2a" stroke-width="4.6" opacity=".42" stroke-linecap="round"/><path d="M0 0L{n(beam[0])} {n(beam[1])}" stroke="#ffe7c4" stroke-width="1.3" stroke-linecap="round"/>')
    halo = a.rad(0, 0, 17, [(0, "#fff5d8", 0.95), (0.35, "#ffb060", 0.55), (1, "#a53a04", 0)])
    kf = a.keyframes("halo", 1, [(0, "opacity:.7;transform:scale(.9)"), (1, "opacity:1;transform:scale(1.2)")])
    a.css.append(f".{name}-halo{{animation:{kf} .5s ease-in-out infinite alternate;animation-play-state:var(--play,running)}}")
    kf = a.keyframes("ring", 1, [(0, "opacity:.85;transform:scale(.8)"), (1, "opacity:0;transform:scale(5)")])
    a.css.append(f".{name}-ring{{animation:{kf} .85s ease-out infinite;animation-play-state:var(--play,running)}}")
    kf = a.keyframes("spark", 1, [(0, "opacity:1;transform:translate(0,0) scale(1)"), (0.6, "opacity:.6"), (1, "opacity:0;transform:translate(var(--dx),var(--dy)) scale(.3)")])
    a.css.append(f".{name}-spark{{animation:{kf} .6s ease-out infinite;animation-play-state:var(--play,running)}}")
    for i, op in enumerate((0.6, 0.5, 0.4)):
        a.add(f'<ellipse rx="2.4" ry="{n(2.4 * pa.SE)}" fill="none" stroke="#ffc882" stroke-width=".7" opacity="{op}" class="{name}-ring" style="animation-delay:{i * 0.18:.2f}s"/>')
    a.add(f'<ellipse rx="17" ry="{n(17 * 0.8)}" fill="{halo}" class="{name}-halo"/>')
    a.add('<circle r="3.2" fill="#ffe6b4" opacity=".75"/><circle r="1.4" fill="#fff"/>')
    sparks = ((14, -12, "#fff", 1.3), (-11, -14, "#ffcc70", 1.1), (15, -2, "#fff5d8", 1.4), (-8, 4, "#ffb060", 1), (6, -18, "#fff", 1.2), (-15, -5, "#ffa040", 0.9), (10, 6, "#fff5d8", 1.2), (-5, -10, "#ffcc70", 0.9))
    for i, (dx, dy, col, r_) in enumerate(sparks):
        a.add(f'<circle r="{r_}" fill="{col}" class="{name}-spark" style="--dx:{dx}px;--dy:{dy}px;animation-delay:{i * 0.075:.3f}s"/>')
    a.add("</g>")
    a.add("</g>")
    a.add("</g>")

    TX0, TX1, TY0, TY1 = 44, 594, -196, -44
    PILES = [(120 + i * 133, -120) for i in range(4)]
    q = a.p((TX0 + TX1) / 2, (TY0 + TY1) / 2, -2)
    sh = a.rad(q[0], q[1], 190 * a.S / 0.5, [(0, "#1a0f06", 0.3), (1, "#1a0f06", 0)], ry=70 * a.S / 0.5)
    a.add(f'<ellipse cx="{n(q[0])}" cy="{n(q[1])}" rx="{n(190 * a.S / 0.5)}" ry="{n(70 * a.S / 0.5)}" fill="{sh}"/>')
    Zt = 14
    a.rbox(TX0, TX1, TY0, TY1, 0, Zt, 10, MDF[1], MDF[2], MDF[0], edge=MDF[3], sw=0.6, shade_f=MDF[1], shade_s=MDF[2])
    a.path(a.rr((TX0 + 12, TY0 + 12, Zt), (1, 0, 0), (0, 1, 0), TX1 - TX0 - 24, TY1 - TY0 - 24, 5), stroke=MDF[3], sw=0.5, op=0.6)
    d = "".join(a.poly(hex_at(px, py, Zt)) for px, py in PILES)
    a.path(d, "#a97c50", stroke=MDF[3], sw=0.5, op=0.55)

    # Sin el script las piezas se quedan en su pila: es la pose para quien pide menos movimiento.
    side_tone = lambda facing, mid_y: "#6a3f1b" if mid_y < -hh * 0.9 else "#4a2911" if facing > 0.9 else "#573114"
    top_fill = "#dcae7c"
    for k, (cx, cy) in enumerate(cells):
        px, py = PILES[k % len(PILES)]
        level = k // len(PILES)
        dz = Zt + (level + 1) * T - Zs
        tx, ty = a.v(px - cx, py - cy, dz)
        a.add(f'<g data-piece="{k}" data-to="{n(px - cx)},{n(py - cy)},{n(dz)}" transform="translate({tx:.1f} {ty:.1f})">')
        for (x0, y0), (x1, y1), facing in edges:
            if facing > 0:
                a.path(a.poly([(cx + x0, cy + y0, Zs - T), (cx + x1, cy + y1, Zs - T), (cx + x1, cy + y1, Zs), (cx + x0, cy + y0, Zs)]), side_tone(facing, (y0 + y1) / 2), stroke="#2a1505", sw=0.3)
        a.path(a.poly(hex_at(cx, cy, Zs)), top_fill, stroke="#7a4a22", sw=0.5)
        a.close()

    a.root_attrs = {
        "data-v": projection_attr(a),
        "data-hex": " ".join(f"{n(vx)},{n(vy)}" for vx, vy in HEXV),
        "data-fr": ",".join(f"{f:.3f}" for f in fr),
        "data-park": f"{n(hx)},{n(hy)}",
    }
    return a.write(ART)


def cross3(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot3(u, v):
    return sum(p * q for p, q in zip(u, v))


def plate(a, face, back, fill, tones):
    """Placa con espesor: face es la cara que ve la cámara y back el vector hacia su cara trasera."""
    cam = (pa.SA * pa.CE, -pa.CA * pa.CE, pa.SE)
    normal = mul3(back, -1 / math.sqrt(dot3(back, back)))
    area = sum(dot3(cross3(face[i], face[(i + 1) % len(face)]), normal) for i in range(len(face)))
    quads = []
    for i, p in enumerate(face):
        q = face[(i + 1) % len(face)]
        edge = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
        out = mul3(cross3(edge, normal), 1 if area > 0 else -1)
        if dot3(out, cam) > 1e-6:
            quads.append((dot3(add3(p, q, back), cam), [p, q, add3(q, back), add3(p, back)], out))
    # Las orillas de un contorno dentado se tapan entre sí: primero las más lejanas.
    for _, pts, out in sorted(quads, key=lambda t: t[0]):
        a.path(a.poly(pts), tones(out))
    a.path(a.poly(face), fill, stroke="#5a3c1e", sw=0.35)


def burnt_edge(out):
    """El láser deja la orilla del MDF tostada; la de arriba recibe más luz."""
    if out[2] > 0:
        return "#b58a58"
    return "#8a5f34" if out[1] < 0 else "#6f4a26"


def materiales(name="materiales", w=640, h=560):
    """«Fabricamos tu producto»: cuatro materiales que se juntan y una caja que se arma en vista explotada (ver MaterialAssembly.astro)."""
    BW, BD, BH, TH = 260, 190, 110, 9
    EXP = {"back": (0, 150, 0), "left": (-165, 0, 0), "floor": (0, 0, -120), "right": (165, 0, 0), "front": (0, -150, 0), "label": (0, -215, 0), "lid": (0, 0, 135), "knob": (0, 0, 205)}
    view = (30, 28)
    S, ox, oy = fit_points(view, [(-165, -150, 0), (-165, BD + 150, BH), (BW + 165, -150, 0), (BW + 165, BD + 150, BH), (BW, 0, -120), (BW / 2, BD / 2, BH + 240), (0, BD, BH + 145), (BW, -215, 0)], w, h, mx=8, my=8)
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    az = math.degrees(pa.AZ)

    # Armada, la caja deja mucho aire en un cuadro pensado para la vista explotada: la cámara se acerca.
    center = a.p(BW / 2, BD / 2, BH / 2 + 10)
    zoom = 1.5
    a.add(f'<g data-zoom="" transform="translate({w / 2} {h / 2}) scale({zoom}) translate({-center[0]:.1f} {-center[1]:.1f})">')

    q = a.p(BW / 2, BD / 2, -8)
    sh = a.rad(q[0], q[1], 215 * S, [(0, "#1a0f06", 0.4), (0.6, "#1a0f06", 0.16), (1, "#1a0f06", 0)], ry=112 * S)
    a.add(f'<ellipse data-shadow="" cx="{n(q[0])}" cy="{n(q[1])}" rx="{n(215 * S)}" ry="{n(112 * S)}" fill="{sh}"/>')

    d = ""
    for (x, y, z), (dx, dy, dz) in (
        ((BW / 2, BD / 2, BH), (0, 0, EXP["knob"][2] + 16)),
        ((BW / 2, BD / 2, 0), (0, 0, EXP["floor"][2])),
        ((BW, BD / 2, BH / 2), (EXP["right"][0], 0, 0)),
        ((0, BD / 2, BH / 2), (EXP["left"][0], 0, 0)),
        ((BW / 2, 0, BH / 2), (0, EXP["label"][1], 0)),
        ((BW / 2, BD, BH / 2), (0, EXP["back"][1], 0)),
    ):
        d += a.poly([(x, y, z), (x + dx, y + dy, z + dz)], close=False)
    a.add(f'<path data-guides="" opacity="0" d="{d}" fill="none" stroke="{RUST}" stroke-width=".9" stroke-dasharray="3 4"/>')

    rows = 5
    rh = BH / rows

    def comb(span):
        up, down = [], []
        for r in range(rows):
            up += [(span(r)[1], r * rh), (span(r)[1], (r + 1) * rh)]
        for r in reversed(range(rows)):
            down += [(span(r)[0], (r + 1) * rh), (span(r)[0], r * rh)]
        return up + down

    # Espigas: donde el frente llega a la esquina el costado se recorta, y al revés.
    along_x = comb(lambda r: (0, BW) if r % 2 == 0 else (TH, BW - TH))
    along_y = comb(lambda r: (TH, BD - TH) if r % 2 == 0 else (0, BD))

    def part(key, order):
        dx, dy, dz = EXP[key]
        a.add(f'<g data-part="{order}" data-from="{dx},{dy},{dz}">')

    def grain(p0, p1, u, count, op=0.24):
        d = ""
        for i in range(1, count):
            t = i / count
            start = add3(p0, mul3(u, t))
            end = add3(p1, mul3(u, t + (i % 3 - 1) * 0.012))
            d += a.poly([start, end], close=False)
        a.path(d, stroke=MDF[3], sw=0.35, op=op)

    part("back", 1)
    plate(a, [(u, BD - TH, v) for u, v in along_x], (0, TH, 0), a.lin3((0, BD - TH, BH), (0, BD - TH, 0), [(0, "#c49a68"), (1, "#a97f52")]), burnt_edge)
    grain((14, BD - TH, 0), (BW - 14, BD - TH, 0), (0, 0, BH), 6)
    a.close()

    part("left", 2)
    plate(a, [(TH, u, v) for u, v in along_y], (-TH, 0, 0), a.lin3((TH, 0, BH), (TH, BD, 0), [(0, "#b98e5e"), (1, "#9a7148")]), burnt_edge)
    grain((TH, 14, 0), (TH, BD - 14, 0), (0, 0, BH), 6)
    a.close()

    part("floor", 0)
    plate(a, [(TH, TH, TH), (BW - TH, TH, TH), (BW - TH, BD - TH, TH), (TH, BD - TH, TH)], (0, 0, -TH), a.lin3((TH, BD, TH), (BW, TH, TH), [(0, "#c9a070"), (1, "#b58a5c")]), burnt_edge)
    grain((TH + 6, TH, TH), (BW - TH - 6, TH, TH), (0, BD - 2 * TH, 0), 8)
    a.close()

    part("right", 3)
    plate(a, [(BW, u, v) for u, v in along_y], (-TH, 0, 0), a.lin3((BW, 0, BH), (BW, BD, 0), [(0, "#c3966a"), (1, "#a67b4f")]), burnt_edge)
    grain((BW, 14, 0), (BW, BD - 14, 0), (0, 0, BH), 6)
    a.close()

    part("front", 4)
    plate(a, [(u, 0, v) for u, v in along_x], (0, TH, 0), a.lin3((0, 0, BH), (BW, 0, 0), [(0, "#e4bb88"), (1, "#cda070")]), burnt_edge)
    grain((14, 0, 0), (BW - 14, 0, 0), (0, 0, BH), 6, 0.2)
    a.close()

    part("label", 5)
    LX0, LZ0, LW, LH = 68, 24, 124, 62
    a.path(a.rr((LX0 + 2, -0.2, LZ0 - 2), (1, 0, 0), (0, 0, 1), LW, LH, 4), "#2b1d12", op=0.2)
    a.path(a.rr((LX0, -0.4, LZ0), (1, 0, 0), (0, 0, 1), LW, LH, 4), "#fbf6ea", stroke="#cdbfa6", sw=0.5)
    a.path(a.rr((LX0 + 5, -0.4, LZ0 + 5), (1, 0, 0), (0, 0, 1), LW - 10, LH - 10, 2), stroke=RUST, sw=0.5, op=0.7)
    a.open(tf=a.matrix((BW / 2, -0.4, LZ0 + 24), (1, 0, 0), (0, 0, -1)))
    a.add('<text text-anchor="middle" font-family="Playfair Display,Georgia,serif" font-size="29" font-weight="700" fill="#2b1d12">Lumo</text>')
    a.close()
    a.close()

    part("lid", 6)
    Zl0, Zl1 = BH, BH + 7
    top_rr = a.rr((-7, -7, Zl1), (1, 0, 0), (0, 1, 0), BW + 14, BD + 14, 11)
    a.rbox(-7, BW + 7, -7, BD + 7, Zl0, Zl1, 11, "#8a3205", "#5e2103", None, edge="#3f1602", sw=0.4, shade_f="#8a3205", shade_s="#5e2103")
    a.path(top_rr, a.lin3((-7, BD, Zl1), (BW + 7, -7, Zl1), [(0, "#d9743a"), (0.5, "#b84a12"), (1, "#962f02")]))
    cl = a.clip(top_rr)
    a.open(clip=cl)
    for x0, wd, op in ((36, 44, 0.18), (92, 16, 0.14), (196, 30, 0.1)):
        a.path(a.poly([(x0, -7, Zl1), (x0 + wd, -7, Zl1), (x0 + wd + 70, BD + 7, Zl1), (x0 + 70, BD + 7, Zl1)]), "#fff4e6", op=op)
    a.close()
    Cx, Cy = BW / 2, BD / 2
    frost = "#fbdcb8"
    a.path(a.ellipse_z(Cx, Cy, Zl1, 31), stroke=frost, sw=1.3, op=0.95)
    d = ""
    for i in range(16):
        t = i * math.pi / 8
        r0, r1 = 38, 54 if i % 2 == 0 else 47
        d += a.poly([(Cx + r0 * math.cos(t), Cy + r0 * math.sin(t), Zl1), (Cx + r1 * math.cos(t), Cy + r1 * math.sin(t), Zl1)], close=False)
    a.path(d, stroke=frost, sw=1.3, op=0.95, cap="round")
    a.path(a.rr((-1, -1, Zl1), (1, 0, 0), (0, 1, 0), BW + 2, BD + 2, 7), stroke=frost, sw=0.5, op=0.5)
    qs = a.p(Cx, Cy, Zl1)
    band = a.lin(qs[0] - 46, qs[1], qs[0] + 46, qs[1], [(0, "#fff8ea", 0), (0.5, "#fff8ea", 0.7), (1, "#fff8ea", 0)])
    a.open(clip=cl)
    a.add(f'<path data-shine="" opacity="0" d="M{n(qs[0] - 46)} {n(qs[1] - 200)}h56l36 400h-56Z" fill="{band}" transform="translate(-220 0)"/>')
    a.close()
    a.close()

    part("knob", 7)
    Kz0, Kz1, Kr = Zl1, Zl1 + 24, 19
    a.path(a.cylz_path(Cx, Cy, Kz0, Kz1, Kr), a.cylz_grad(Cx, Cy, 0, Kr, [(0, "#8d5413"), (0.32, "#d98f3a"), (0.5, "#f0b263"), (1, "#7d4708")]))
    d = ""
    for lz in range(Kz0 + 3, Kz1, 3):
        d += a.arc((Cx, Cy, lz), (Kr, 0, 0), (0, Kr, 0), az - 180, az)
    a.path(d, stroke="#6d3f0c", sw=0.45, op=0.55)
    a.ell_z(Cx, Cy, Kz1, Kr, "#e9a955", stroke="#a9650c", sw=0.5)
    a.ell_z(Cx, Cy, Kz1, Kr - 5, "#f2bd76")
    a.ell_z(Cx, Cy, Kz1, Kr - 11, "#f8d39d")
    a.close()
    a.add("</g>")

    # Cada material se dibuja alrededor de su propio origen para que el script pueda girarlo y escalarlo.
    a.ox, a.oy = 0, 0
    bob = a.keyframes("bob", 1, [(0, "transform:translate(0,-5px)"), (1, "transform:translate(0,5px)")])

    def material(k, at, rot, dur, delay):
        cls = f"{name}-b{k}"
        a.css.append(f".{cls}{{animation:{bob} {dur}s ease-in-out infinite alternate;animation-delay:{delay}s;animation-play-state:var(--play,running)}}")
        a.add(f'<g data-mat="{at[0]},{at[1]},{rot}" opacity="0" transform="translate({at[0]} {at[1]})"><g class="{cls}">')

    def end_material():
        a.add("</g></g>")

    def blob(rx, ry, dy=0):
        i = a.rad(0, dy, rx, [(0, "#1a0f06", 0.22), (1, "#1a0f06", 0)], ry=ry)
        a.add(f'<ellipse cy="{dy}" rx="{rx}" ry="{ry}" fill="{i}"/>')

    material(0, (150, 150), -8, 3.4, -0.6)
    blob(128, 62, 34)
    for i, (dx, dy) in enumerate(((10, -7), (-7, 5), (0, 0))):
        x0, x1, y0, y1 = -95 + dx, 95 + dx, -66 + dy, 66 + dy
        z0 = i * 10 - 10
        a.box(x0, x1, y0, y1, z0, z0 + 9, front=MDF[1], side=MDF[2], top=a.lin3((x0, y1, 0), (x1, y0, 0), [(0, "#e6bf8e"), (1, MDF[1])]), stroke=MDF[3], sw=0.35)
    d = ""
    for i, gy in enumerate(range(-58, 62, 15)):
        d += a.poly([(-95, gy, 19), (95, gy + (i % 3 - 1) * 2, 19)], close=False)
    a.path(d, stroke=MDF[3], sw=0.4, op=0.32)
    end_material()

    material(1, (490, 142), 7, 3.9, -1.5)
    blob(116, 44, 66)
    AW, AH = 150, 122
    AX0, AZ0 = -AW / 2, -AH / 2
    a.box(AX0 + 16, AX0 + AW + 16, 16, 21, AZ0 + 6, AZ0 + AH + 6, front=a.lin3((AX0, 16, AZ0 + AH), (AX0 + AW, 16, AZ0), [(0, "#f3efe6", 0.75), (1, "#cfd8d4", 0.55)]), side="#aeb6b0", top="#eef0ea", stroke="#9aa39d", sw=0.35)
    a.box(AX0, AX0 + AW, 0, 5, AZ0, AZ0 + AH, front=a.lin3((AX0, 0, AZ0 + AH), (AX0 + AW, 0, AZ0), [(0, "#d9743a"), (0.55, "#b84a12"), (1, "#8a3205")]), side="#5e2103", top="#e88f55")
    a.open(clip=a.clip(a.poly([(AX0, 0, AZ0), (AX0 + AW, 0, AZ0), (AX0 + AW, 0, AZ0 + AH), (AX0, 0, AZ0 + AH)])))
    for x0, wd, op in ((-60, 34, 0.2), (-14, 12, 0.16)):
        a.path(a.poly([(x0, 0, AZ0), (x0 + wd, 0, AZ0), (x0 + wd + 60, 0, AZ0 + AH), (x0 + 60, 0, AZ0 + AH)]), "#fff4e6", op=op)
    a.close()
    fx, fz = AX0 + AW, AZ0 + AH
    a.path(a.poly([(fx - 40, 0, fz), (fx, 0, fz), (fx, 0, fz - 36)]), "#4a1800", op=0.4)
    a.path(a.poly([(fx - 40, 0, fz), (fx, 0, fz - 36), (fx - 16, -14, fz - 18)]), a.lin3((fx - 40, 0, fz), (fx, 0, fz - 36), [(0, "#fbf7ee"), (1, "#d8d2c6")]), stroke="#a59d8f", sw=0.4)
    end_material()

    material(2, (140, 420), 6, 3.1, -2.2)
    blob(112, 56, 40)
    PW, PD, PH = 128, 168, 26
    Px0, Py0, Pz0 = -PW / 2, -PD / 2, -PH / 2
    a.box(Px0, Px0 + PW, Py0, Py0 + PD, Pz0, Pz0 + PH, front="#ece4d3", side="#d6ccb8", top="#fbf8f0", stroke="#a59b88", sw=0.35)
    d = ""
    for lz in range(int(Pz0) + 3, int(Pz0 + PH), 3):
        d += a.poly([(Px0, Py0, lz), (Px0 + PW, Py0, lz), (Px0 + PW, Py0 + PD, lz)], close=False)
    a.path(d, stroke="#a59b88", sw=0.35, op=0.7)

    def loose(angle, z, fill):
        t = math.radians(angle)
        c, s_ = math.cos(t), math.sin(t)
        pts = [(x * c - y * s_, x * s_ + y * c, z) for x, y in ((Px0, Py0), (Px0 + PW, Py0), (Px0 + PW, Py0 + PD), (Px0, Py0 + PD))]
        a.path(a.poly(pts), "#2b1d12", op=0.1)
        a.path(a.poly([(x, y, z + 1.4) for x, y, _ in pts]), fill, stroke="#b5ab98", sw=0.4)

    loose(-7, Pz0 + PH, "#fffdf7")
    loose(5, Pz0 + PH + 2, "#ffffff")
    t5 = math.radians(5)
    cc, ss = math.cos(t5), math.sin(t5)
    rot = lambda x, y: (x * cc - y * ss, x * ss + y * cc)
    zt = Pz0 + PH + 3.4
    c0, c1, c2 = rot(Px0 + PW, Py0), rot(Px0 + PW - 30, Py0), rot(Px0 + PW, Py0 + 30)
    a.path(a.poly([(*c1, zt), (*c0, zt), (*c2, zt)]), "#d8ceb9")
    a.path(a.poly([(*c1, zt), (*c2, zt), (c1[0] + 8, c2[1] - 6, zt + 13)]), a.lin3((*c1, zt), (*c2, zt), [(0, "#f6f1e6"), (1, "#ded5c3")]), stroke="#b5ab98", sw=0.4)
    d = ""
    for yy in range(-60, 40, 13):
        x0_, y0_ = rot(Px0 + 16, yy)
        x1_, y1_ = rot(Px0 + PW - 22 - (yy % 3) * 8, yy)
        d += a.poly([(x0_, y0_, zt), (x1_, y1_, zt)], close=False)
    a.path(d, stroke="#c9beab", sw=0.7, op=0.8)
    end_material()

    material(3, (500, 412), -6, 3.6, -0.9)
    blob(112, 50, 84)
    kf = a.keyframes("spin", 1, [(0, "transform:rotate(0deg)"), (1, "transform:rotate(360deg)")])
    a.css.append(f".{name}-spin{{animation:{kf} 16s linear infinite;animation-play-state:var(--play,running)}}")
    spool_x(a, -36, 36, 0, 0, 86, "honey", spin=f"{name}-spin")
    q0, q1, q2, q3 = a.p(-8, 0, 80), a.p(-40, -36, 136), a.p(-110, -30, 92), a.p(-84, -14, 40)
    tail = f"M{n(q0[0])} {n(q0[1])}C{n(q1[0])} {n(q1[1])} {n(q2[0])} {n(q2[1])} {n(q3[0])} {n(q3[1])}"
    a.add(f'<path d="{tail}" fill="none" stroke="#9a5a18" stroke-width="2.4" stroke-linecap="round"/><path d="{tail}" fill="none" stroke="#e8a956" stroke-width="1.3" stroke-linecap="round"/>')
    end_material()
    a.ox, a.oy = ox, oy

    a.root_attrs = {"data-v": projection_attr(a), "data-center": f"{n(center[0])},{n(center[1])}", "data-size": f"{w},{h}", "data-zoom": zoom}
    return a.write(ART)


ALL = {
    "cortadora-laser": laser_cutter,
    "impresion-3d": h2c_wide,
    "souvenirs": souvenirs,
    "pieza-florero": spec_vase,
    "pieza-engrane": spec_gear,
    "pieza-maqueta": spec_maqueta,
    "tresd-proceso": tresd_proceso,
    "laser-proceso": laser_proceso,
    "materiales": materiales,
}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(ALL)
    for key in wanted:
        print(key, ALL[key]())
