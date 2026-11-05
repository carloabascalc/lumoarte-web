#!/usr/bin/env python3
"""Genera src/assets/printers/{h2c,a2l,h3c}.svg (tarjetas de «Equipo del taller»).

Las máquinas se modelan en milímetros, con sus medidas reales, y se proyectan en
axonométrico: así cada eje se mueve en línea recta en pantalla y las animaciones
CSS (translate) siguen el movimiento físico de la máquina sin JavaScript.

Uso: python3 tools/printer_art.py
"""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/assets/printers"

def set_view(az_deg=24, el_deg=16):
    global AZ, EL, CA, SA, CE, SE
    AZ, EL = math.radians(az_deg), math.radians(el_deg)
    CA, SA, CE, SE = math.cos(AZ), math.sin(AZ), math.cos(EL), math.sin(EL)


set_view()

# Paleta del sitio (Base.astro) + neutros cálidos para los materiales de cada máquina.
LINE = "#2b1d12"
HONEY = "#c87a2a"
RUST = "#A53A04"
RUST_D = "#7d2b02"
CREAM = "#f5e9d8"
SPOOLS = {
    "cream": ("#f4eee3", "#c9bfae"),
    "honey": ("#d98f3a", "#9a5a18"),
    "rust": ("#b8481a", "#74280a"),
    "teal": ("#3f7f80", "#234d4f"),
    "olive": ("#8a9344", "#555b26"),
    "ink": ("#4a3a2c", "#241a12"),
}
GLYPHS = {
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    "2": [[(0, 0), (4, 0), (4, 3), (0, 3), (0, 6), (4, 6)]],
    "3": [[(0, 0), (4, 0), (4, 6), (0, 6)], [(1, 3), (4, 3)]],
    "C": [[(4, 0), (0, 0), (0, 6), (4, 6)]],
    "A": [[(0, 6), (0, 1.2), (1.2, 0), (2.8, 0), (4, 1.2), (4, 6)], [(0, 3.8), (4, 3.8)]],
    "L": [[(0, 0), (0, 6), (4, 6)]],
    "M": [[(0, 6), (0, 0), (2, 3), (4, 0), (4, 6)]],
    "S": [[(4, 0), (0, 0), (0, 3), (4, 3), (4, 6), (0, 6)]],
    "P": [[(0, 6), (0, 0), (4, 0), (4, 3), (0, 3)]],
    "R": [[(0, 6), (0, 0), (4, 0), (4, 3), (0, 3)], [(2, 3), (4, 6)]],
    "O": [[(0, 0), (4, 0), (4, 6), (0, 6), (0, 0)]],
    "0": [[(0, 0), (4, 0), (4, 6), (0, 6), (0, 0)]],
    "5": [[(4, 0), (0, 0), (0, 3), (4, 3), (4, 6), (0, 6)]],
}


def n(v):
    s = f"{v:.1f}"
    if s.endswith(".0"):
        s = s[:-2]
    return "0" if s == "-0" else s


def add3(*vs):
    return tuple(sum(c) for c in zip(*vs))


def mul3(v, k):
    return tuple(c * k for c in v)


def cross2(a, b):
    return a[0] * b[1] - a[1] * b[0]


class Art:
    def __init__(self, name, S, ox, oy, w=480, h=560):
        self.name, self.S, self.ox, self.oy, self.w, self.h = name, S, ox, oy, w, h
        self.defs, self.body, self.css, self.uid = [], [], [], 0
        self.root_attrs = {}

    def p(self, x, y, z):
        return (
            self.ox + self.S * (x * CA + y * SA),
            self.oy - self.S * (z * CE + (y * CA - x * SA) * SE),
        )

    def v(self, dx, dy, dz):
        return (
            self.S * (dx * CA + dy * SA),
            -self.S * (dz * CE + (dy * CA - dx * SA) * SE),
        )

    def pt(self, q):
        s = self.p(*q)
        return f"{n(s[0])} {n(s[1])}"

    def matrix(self, o, u, v):
        a, b = self.v(*u)
        c, d = self.v(*v)
        e, f = self.p(*o)
        return f"matrix({a:.3f} {b:.3f} {c:.3f} {d:.3f} {e:.1f} {f:.1f})"

    def poly(self, pts, close=True):
        d = "M" + "L".join(self.pt(q) for q in pts)
        return d + ("Z" if close else "")

    def arc(self, c, U, V, t0, t1, start="M"):
        steps = max(1, math.ceil(abs(t1 - t0) / 90 - 1e-6))
        dt = math.radians((t1 - t0) / steps)
        k = 4 / 3 * math.tan(dt / 4)
        P = lambda t: add3(c, mul3(U, math.cos(t)), mul3(V, math.sin(t)))
        T = lambda t: add3(mul3(U, -math.sin(t)), mul3(V, math.cos(t)))
        t = math.radians(t0)
        out = [start + self.pt(P(t))]
        for _ in range(steps):
            t2 = t + dt
            c1 = add3(P(t), mul3(T(t), k))
            c2 = add3(P(t2), mul3(T(t2), -k))
            out.append(f"C{self.pt(c1)} {self.pt(c2)} {self.pt(P(t2))}")
            t = t2
        return "".join(out)

    def rr(self, o, u, v, w, h, r):
        """Rectángulo redondeado en el plano (o, u, v)."""
        at = lambda a, b: add3(o, mul3(u, a), mul3(v, b))
        ru, rv = mul3(u, r), mul3(v, r)
        d = "M" + self.pt(at(r, 0))
        d += "L" + self.pt(at(w - r, 0))
        d += self._corner(at(w - r, r), ru, rv, -90, 0)
        d += "L" + self.pt(at(w, h - r))
        d += self._corner(at(w - r, h - r), ru, rv, 0, 90)
        d += "L" + self.pt(at(r, h))
        d += self._corner(at(r, h - r), ru, rv, 90, 180)
        d += "L" + self.pt(at(0, r))
        d += self._corner(at(r, r), ru, rv, 180, 270)
        return d + "Z"

    def _corner(self, c, U, V, t0, t1):
        s = self.arc(c, U, V, t0, t1, "M")
        return s[s.index("C"):]

    def circle(self, c, U, V):
        return self.arc(c, U, V, 0, 360) + "Z"

    def nid(self):
        self.uid += 1
        return f"{self.name}{self.uid}"

    def lin(self, x1, y1, x2, y2, stops):
        i = self.nid()
        ss = ""
        for st in stops:
            op = f' stop-opacity="{st[2]}"' if len(st) > 2 else ""
            ss += f'<stop offset="{st[0]}" stop-color="{st[1]}"{op}/>'
        self.defs.append(
            f'<linearGradient id="{i}" gradientUnits="userSpaceOnUse" x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}">{ss}</linearGradient>'
        )
        return f"url(#{i})"

    def lin_box(self, stops):
        """Degradado horizontal relativo al objeto: una sola definición sirve para muchas capas."""
        i = self.nid()
        ss = "".join(f'<stop offset="{st[0]}" stop-color="{st[1]}"/>' for st in stops)
        self.defs.append(f'<linearGradient id="{i}">{ss}</linearGradient>')
        return f"url(#{i})"

    def ell_z(self, x, y, z, R, fill, stroke=None, sw=None):
        """Círculo horizontal: en esta proyección siempre es una elipse sin girar."""
        q = self.p(x, y, z)
        extra = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<ellipse cx="{n(q[0])}" cy="{n(q[1])}" rx="{n(R * self.S)}" ry="{n(R * self.S * SE)}" fill="{fill}"{extra}/>')

    def lin3(self, a, b, stops):
        p, q = self.p(*a), self.p(*b)
        return self.lin(p[0], p[1], q[0], q[1], stops)

    def rad(self, cx, cy, r, stops, ry=None):
        i = self.nid()
        ss = ""
        for st in stops:
            op = f' stop-opacity="{st[2]}"' if len(st) > 2 else ""
            ss += f'<stop offset="{st[0]}" stop-color="{st[1]}"{op}/>'
        tf = ""
        if ry is not None:
            tf = f' gradientTransform="translate({n(cx)} {n(cy)}) scale(1 {ry / r:.3f}) translate({n(-cx)} {n(-cy)})"'
        self.defs.append(
            f'<radialGradient id="{i}" gradientUnits="userSpaceOnUse" cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}"{tf}>{ss}</radialGradient>'
        )
        return f"url(#{i})"

    def clip(self, d):
        i = self.nid()
        self.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        return i

    def add(self, s):
        self.body.append(s)

    def path(self, d, fill="none", stroke=None, sw=None, op=None, cls=None, cap=None):
        a = f'<path d="{d}"'
        if fill != "none" or stroke is None:
            a += f' fill="{fill}"'
        else:
            a += ' fill="none"'
        if stroke:
            a += f' stroke="{stroke}"'
        if sw is not None:
            a += f' stroke-width="{sw}"'
        if cap:
            a += f' stroke-linecap="{cap}" stroke-linejoin="round"'
        if op is not None:
            a += f' opacity="{op}"'
        if cls:
            a += f' class="{cls}"'
        self.add(a + "/>")

    def rect(self, x, y, w, h, fill, rx=None, cls=None, op=None, stroke=None, sw=None):
        a = f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="{fill}"'
        if rx:
            a += f' rx="{n(rx)}"'
        if op is not None:
            a += f' opacity="{op}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if cls:
            a += f' class="{cls}"'
        self.add(a + "/>")

    def open(self, cls=None, tf=None, clip=None, op=None, style=None):
        a = "<g"
        if cls:
            a += f' class="{cls}"'
        if tf:
            a += f' transform="{tf}"'
        if clip:
            a += f' clip-path="url(#{clip})"'
        if op is not None:
            a += f' opacity="{op}"'
        if style:
            a += f' style="{style}"'
        self.add(a + ">")

    def close(self):
        self.add("</g>")

    def box(self, x0, x1, y0, y1, z0, z1, front=None, side=None, top=None, stroke=None, sw=0.6):
        if top:
            self.path(self.poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]), top, stroke, sw if stroke else None)
        if side:
            self.path(self.poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]), side, stroke, sw if stroke else None)
        if front:
            self.path(self.poly([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)]), front, stroke, sw if stroke else None)

    def rbox(self, x0, x1, y0, y1, z0, z1, r, front, side, top=None, edge=None, sw=0.8, shade_f=None, shade_s=None):
        """Prisma con esquinas verticales redondeadas; dibuja solo lo que ve la cámara."""
        az = math.degrees(AZ)
        fc = shade_f or front
        sc = shade_s or side
        self.path(self.poly([(x1, y0 + r, z0), (x1, y1 - r, z0), (x1, y1 - r, z1), (x1, y0 + r, z1)]), side)
        self.path(self.poly([(x0 + r, y0, z0), (x1 - r, y0, z0), (x1 - r, y0, z1), (x0 + r, y0, z1)]), front)
        U, V = (r, 0, 0), (0, r, 0)

        def band(cx, cy, t0, t1, c0, c1):
            top_a = self.arc((cx, cy, z1), U, V, t0, t1)
            bot_a = self.arc((cx, cy, z0), U, V, t1, t0, "L")
            g = self.lin3(
                (cx + r * math.cos(math.radians(t0)), cy + r * math.sin(math.radians(t0)), (z0 + z1) / 2),
                (cx + r * math.cos(math.radians(t1)), cy + r * math.sin(math.radians(t1)), (z0 + z1) / 2),
                [(0, c0), (1, c1)],
            )
            self.path(top_a + bot_a + "Z", g)

        band(x1 - r, y0 + r, -90, 0, fc, sc)
        band(x0 + r, y0 + r, 180 + az, 270, sc, fc)
        band(x1 - r, y1 - r, 0, az, sc, sc)
        if top:
            self.path(self.rr((x0, y0, z1), (1, 0, 0), (0, 1, 0), x1 - x0, y1 - y0, r), top)
        if edge:
            sil = self.arc((x0 + r, y0 + r, z1), U, V, 180 + az, 270)
            sil += "L" + self.pt((x1 - r, y0, z1))
            sil += self._corner((x1 - r, y0 + r, z1), U, V, -90, 0)
            sil += "L" + self.pt((x1, y1 - r, z1))
            sil += self._corner((x1 - r, y1 - r, z1), U, V, 0, az)
            sil += self.arc((x1 - r, y1 - r, z0), U, V, az, 0, "L")
            sil += "L" + self.pt((x1, y0 + r, z0))
            sil += self._corner((x1 - r, y0 + r, z0), U, V, 0, -90)
            sil += "L" + self.pt((x0 + r, y0, z0))
            sil += self._corner((x0 + r, y0 + r, z0), U, V, 270, 180 + az)
            self.path(sil + "Z", stroke=edge, sw=sw)

    def visible_x(self):
        """Ángulo central (plano YZ) de la cara de un cilindro en X que mira a la cámara."""
        return math.degrees(math.atan2(SE, -CA * CE))

    def cylx_path(self, x0, x1, y, z, R):
        tc = self.visible_x()
        U, V = (0, R, 0), (0, 0, R)
        d = self.arc((x0, y, z), U, V, tc - 90, tc + 90)
        d += self.arc((x1, y, z), U, V, tc + 90, tc + 270, "L")
        return d + "Z"

    def cylx_grad(self, x, y, z, R, stops):
        tc = math.radians(self.visible_x())
        a = (x, y + R * math.cos(tc - math.pi / 2), z + R * math.sin(tc - math.pi / 2))
        b = (x, y + R * math.cos(tc + math.pi / 2), z + R * math.sin(tc + math.pi / 2))
        return self.lin3(a, b, stops)

    def cylz_path(self, x, y, z0, z1, R):
        az = math.degrees(AZ)
        U, V = (R, 0, 0), (0, R, 0)
        d = self.arc((x, y, z1), U, V, az - 180, az)
        d += self.arc((x, y, z0), U, V, az, az - 180, "L")
        return d + "Z"

    def cylz_grad(self, x, y, z, R, stops):
        p = self.p(x, y, z)
        return self.lin(p[0] - R * self.S, p[1], p[0] + R * self.S, p[1], stops)

    def ellipse_x(self, x, y, z, R):
        return self.circle((x, y, z), (0, R, 0), (0, 0, R))

    def ellipse_z(self, x, y, z, R):
        return self.circle((x, y, z), (R, 0, 0), (0, R, 0))

    def glyphs(self, text, o, size, color, sw=None, u=(1, 0, 0), v=(0, 0, -1), track=1.5):
        k = size / 6
        d, cx = "", 0.0
        for ch in text:
            if ch == " ":
                cx += 3 * k
                continue
            for line in GLYPHS[ch]:
                pts = [add3(o, mul3(u, cx + px * k), mul3(v, py * k)) for px, py in line]
                d += self.poly(pts, close=False)
            cx += (4 + track) * k
        self.path(d, stroke=color, sw=sw if sw is not None else max(0.7, size * self.S * 0.13), cap="square")

    def keyframes(self, name, T, stops):
        """stops = [(t_seg, 'css')]; devuelve el nombre con prefijo de la máquina."""
        full = f"{self.name}-{name}"
        body = "".join(f"{(t / T) * 100:.2f}%{{{css}}}" for t, css in stops)
        self.css.append(f"@keyframes {full}{{{body}}}")
        return full

    def animate(self, cls, kf, T, timing="linear", origin=None, delay=None, extra=""):
        rule = f".{cls}{{animation:{kf} {T}s {timing} infinite;animation-play-state:var(--play,running)"
        if origin:
            rule += f";transform-origin:{origin}"
        if delay:
            rule += f";animation-delay:{delay}"
        self.css.append(rule + extra + "}")

    def translate_kf(self, name, T, stops):
        return self.keyframes(name, T, [(t, f"transform:translate({dx:.2f}px,{dy:.2f}px)") for t, dx, dy in stops])

    def along(self, axis, amount):
        vec = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
        return self.v(*mul3(vec, amount))

    def write(self, outdir=None):
        reduced = f"@media (prefers-reduced-motion:reduce){{svg.{self.name}-art *{{animation:none!important}}}}"
        style = "".join(self.css) + reduced
        attrs = "".join(f' {k}="{v}"' for k, v in self.root_attrs.items())
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" class="{self.name}-art" viewBox="0 0 {self.w} {self.h}" '
            f'preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false"{attrs}>'
            f"<style>{style}</style><defs>{''.join(self.defs)}</defs>{''.join(self.body)}</svg>\n"
        )
        folder = outdir or OUT
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{self.name}.svg").write_text(svg)
        return len(svg)


def zigzag(t0, t1, step, amp, phase=1, settle=0.0):
    """Barridos ida y vuelta entre t0 y t1 con amplitud ±amp."""
    out, t, s = [], t0, phase
    while t < t1 - 1e-6:
        out.append((t, s * amp))
        t += step
        s = -s
    out.append((t1, settle))
    return out


def stage(a, shadow, floor=True):
    bg = a.lin(0, 0, 0, a.h, [(0, "#f8f2e7"), (1, "#ece1cf")])
    a.add(f'<rect width="{a.w}" height="{a.h}" fill="{bg}"/>')
    glow = a.rad(a.w * 0.5, a.h * 0.38, a.w * 0.62, [(0, "#fffdf8", 0.85), (1, "#fffdf8", 0)])
    a.add(f'<rect width="{a.w}" height="{a.h}" fill="{glow}"/>')
    if floor:
        d = ""
        for i in range(-3, 13):
            d += a.poly([(i * 100, -320, 0), (i * 100, 900, 0)], close=False)
        for j in range(-3, 10):
            d += a.poly([(-420, j * 100, 0), (1100, j * 100, 0)], close=False)
        a.path(d, stroke=LINE, sw=0.5, op=0.05)
    cx, cy, rx, ry = shadow
    sh = a.rad(cx, cy, rx, [(0, "#1a0f06", 0.42), (0.55, "#1a0f06", 0.18), (1, "#1a0f06", 0)], ry=ry)
    a.add(f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" fill="{sh}"/>')


def spool_x(a, x0, x1, y, z, R, color, flange="#efe9dd", holes=False, spin=None, core=0.4):
    """Bobina con eje en X. La cara +X es la que ve la cámara."""
    light, dark = SPOOLS[color]
    f = 5
    a.path(a.ellipse_x(x0, y, z, R), flange, stroke="#8d8373", sw=0.4)
    g = a.cylx_grad((x0 + x1) / 2, y, z, R * 0.92, [(0, dark), (0.22, light), (0.6, light), (1, dark)])
    a.path(a.cylx_path(x0 + f, x1 - f, y, z, R * 0.92), g)
    tc = a.visible_x()
    d = ""
    steps = 5
    for i in range(1, steps):
        xi = x0 + f + (x1 - x0 - 2 * f) * i / steps
        d += a.arc((xi, y, z), (0, R * 0.92, 0), (0, 0, R * 0.92), tc - 88, tc + 88)
    a.path(d, stroke=dark, sw=0.45, op=0.55)
    a.path(a.ellipse_x(x1, y, z, R), flange, stroke="#8d8373", sw=0.4)
    if holes or spin:
        tf = a.matrix((x1, y, z), (0, 1, 0), (0, 0, -1))
        a.open(tf=tf)
        if spin:
            a.open(cls=spin)
        dots = ""
        rings = [(R * 0.82, 26), (R * 0.68, 22), (R * 0.54, 16)]
        for rr_, cnt in rings:
            for i in range(cnt):
                t = 2 * math.pi * i / cnt
                dots += f'<circle cx="{n(rr_ * math.cos(t))}" cy="{n(rr_ * math.sin(t))}" r="{n(R * 0.022)}"/>'
        a.add(f'<g fill="#a79d8c">{dots}</g>')
        a.add(f'<circle r="{n(R * core)}" fill="#d9d1c2"/><circle r="{n(R * core * 0.62)}" fill="#3a3027"/>')
        a.add(f'<rect x="{n(R * core * 0.62)}" y="-3" width="{n(R * 0.5)}" height="6" rx="2" fill="#b9ae9c"/>')
        if spin:
            a.close()
        a.close()
    else:
        a.path(a.ellipse_x(x1, y, z, R * core), "#d9d1c2")
        a.path(a.ellipse_x(x1, y, z, R * core * 0.62), "#3a3027")


def gear_outline(cx, cy, r_root, r_tip, teeth):
    pts = []
    for i in range(teeth):
        step = 2 * math.pi / teeth
        t = i * step
        for frac, r in ((0.0, r_root), (0.18, r_root), (0.28, r_tip), (0.62, r_tip), (0.72, r_root)):
            ang = t + frac * step
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def prism_sides(a, pts, z0, z1, tones):
    """Caras laterales visibles de un prisma (contorno antihorario visto desde arriba)."""
    view = (SA, -CA)
    light = (-0.55, -0.83)
    buckets = {t: "" for t in tones}
    m = len(pts)
    for i in range(m):
        p, q = pts[i], pts[(i + 1) % m]
        ex, ey = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(ex, ey) or 1
        nx, ny = ey / ln, -ex / ln
        if nx * view[0] + ny * view[1] <= 0:
            continue
        shade = max(0.0, nx * light[0] + ny * light[1])
        tone = tones[min(len(tones) - 1, int(shade * len(tones)))]
        buckets[tone] += a.poly([(p[0], p[1], z0), (q[0], q[1], z0), (q[0], q[1], z1), (p[0], p[1], z1)])
    for tone, d in buckets.items():
        if d:
            a.path(d, tone, stroke=tone, sw=0.3)


def ams2(a, x0, x1, y0, y1, z0, colors, active, pulse_cls):
    base_h, lid_h = 104, 118
    zb = z0 + base_h
    yc = (y0 + y1) / 2
    U, V = (0, (y1 - y0) / 2, 0), (0, 0, lid_h)
    vu, vv, vx = a.v(*U), a.v(*V), a.v(1, 0, 0)
    tA = math.degrees(math.atan2(cross2(vv, vx), cross2(vu, vx)))
    while tA < 0:
        tA += 180
    while tA > 180:
        tA -= 180
    lid = a.arc((x0, yc, zb), U, V, 180, tA)
    lid += a.arc((x1, yc, zb), U, V, tA, 0, "L")
    lid += "L" + a.pt((x1, y0, zb)) + "L" + a.pt((x0, y0, zb)) + "Z"
    a.path(lid, "#2e2620")
    clip = a.clip(lid)
    a.open(clip=clip)
    sw = (x1 - x0 - 16) / len(colors)
    R = 96
    for i, col in enumerate(colors):
        sx0 = x0 + 8 + i * sw
        spool_x(a, sx0 + 3, sx0 + sw - 3, yc, zb + 8, R, col)
    gl = a.lin3((x0, yc, zb + lid_h), (x0, y0, zb), [(0, "#fffaf2", 0.34), (0.3, "#fffaf2", 0.06), (1, "#1a0f06", 0.1)])
    a.path(lid, gl)
    a.close()
    cap = a.arc((x1, yc, zb), U, V, 0, 180) + "Z"
    capg = a.lin3((x1, y1, zb + lid_h * 0.6), (x1, y0, zb), [(0, "#4a4037", 0.97), (1, "#2b241e", 0.92)])
    a.path(cap, capg)
    a.path(a.arc((x1, yc, zb), U, V, 12, 170), stroke="#8c8072", sw=0.7, op=0.8)
    a.path(a.arc((x0, yc, zb), U, V, 172, tA) + a.arc((x1, yc, zb), U, V, tA, 8, "L"), stroke="#fff6e8", sw=1, op=0.75)
    a.path(a.poly([(x1, y0, z0), (x1, y1, z0), (x1, y1, zb), (x1, y0, zb)]), a.lin3((x1, y1, zb), (x1, y0, z0), [(0, "#453b32"), (1, "#231d18")]))
    a.path(a.poly([(x0, y0, z0), (x1, y0, z0), (x1, y0, zb), (x0, y0, zb)]), "#161210")
    win = a.rr((x0 + 8, y0, z0 + 7), (1, 0, 0), (0, 0, 1), x1 - x0 - 16, base_h - 33, 5)
    a.path(win, "#0c0907")
    fw = (x1 - x0 - 16) / len(colors)
    for i in range(len(colors)):
        fx = x0 + 8 + fw * (i + 0.5)
        cyl = a.lin3((fx - 17, y0, z0), (fx + 17, y0, z0), [(0, "#17130f"), (0.45, "#5a4f44"), (1, "#14100c")])
        a.path(a.rr((fx - 17, y0, z0 + 10), (1, 0, 0), (0, 0, 1), 34, 30, 3), cyl)
        glow = a.lin3((fx, y0, z0 + 66), (fx, y0, z0 + 40), [(0, "#f2a24a"), (1, "#a53a04")])
        cls = pulse_cls if i == active else None
        a.path(a.rr((fx - 12, y0, z0 + 43), (1, 0, 0), (0, 0, 1), 24, 24, 3), glow, cls=cls)
        a.path(a.poly([(fx - 7, y0, z0 + 50), (fx + 7, y0, z0 + 50)], close=False), stroke="#fbd6a3", sw=0.7, op=0.8)
    a.path(a.poly([(x0, y0, zb - 22), (x1, y0, zb - 22), (x1, y0, zb), (x0, y0, zb)]), "#26201b")
    a.path(a.poly([(x0, y0, zb), (x1, y0, zb)], close=False), stroke="#6e6256", sw=0.7)
    a.glyphs("AMS 2", (x1 - 118, y0, zb - 7), 10, CREAM)
    a.path(a.rr(((x0 + x1) / 2 - 42, y0 - 2, zb - 10), (1, 0, 0), (0, 0, 1), 84, 8, 3), "#4b4137")


def h2c(name="h2c", w=480, h=560, S=0.525, ox=78, oy=497, outdir=None, floor_ams=False):
    set_view()
    W, D, H = 492, 514, 626
    a = Art(name, S=S, ox=ox, oy=oy, w=w, h=h)
    T = 18
    t_print = 14.5
    t_fade0, t_fade1 = 16, 17
    stage(a, shadow=a.p(W * (0.9 if floor_ams else 0.56), D * 0.42, 0) + ((S * 620, S * 170) if floor_ams else (205, 74)))

    Zp = 322
    Hp = 112
    base = 0.62
    z_bed = Zp - base * Hp
    up = base * Hp
    down = (1 - base) * Hp

    def bed_stops():
        _, dyu = a.along("z", up)
        _, dyd = a.along("z", -down)
        return [(0, 0, dyu), (t_print, 0, dyd), (t_fade1, 0, dyd), (T, 0, dyu)]

    kf = a.translate_kf("bed", T, bed_stops())
    a.animate(f"{name}-bed", kf, T)
    kf = a.keyframes("pfade", T, [(0, "opacity:1"), (t_fade0, "opacity:1"), (t_fade1, "opacity:0"), (T - 0.01, "opacity:0"), (T, "opacity:1")])
    a.animate(f"{name}-pfade", kf, T)
    kf = a.keyframes("cap", T, [(0, "opacity:0"), (0.25, "opacity:1"), (t_fade0, "opacity:1"), (t_fade1, "opacity:0"), (T, "opacity:0")])
    a.animate(f"{name}-cap", kf, T)
    xs = zigzag(0, t_print, 0.95, 46)
    ys = zigzag(0, t_print, 2.4, 20)
    park = [(t_print + 1.1, -112), (T - 0.9, -112), (T, 46)]
    kf = a.translate_kf("hx", T, [(t, *a.along("x", d)) for t, d in xs + park])
    a.animate(f"{name}-hx", kf, T, "cubic-bezier(.45,.05,.55,.95)")
    kf = a.translate_kf("hy", T, [(t, *a.along("y", d)) for t, d in ys + [(t_print + 1.1, 34), (T - 0.9, 34), (T, 20)]])
    a.animate(f"{name}-hy", kf, T, "cubic-bezier(.45,.05,.55,.95)")
    kf = a.keyframes("tip", T, [(0, "opacity:.95"), (t_print, "opacity:.95"), (t_print + 0.6, "opacity:0"), (T - 0.5, "opacity:0"), (T, "opacity:.95")])
    a.animate(f"{name}-tip", kf, T)
    kf = a.keyframes("pulse", 2.4, [(0, "opacity:1"), (1.2, "opacity:.55"), (2.4, "opacity:1")])
    a.animate(f"{name}-pulse", kf, 2.4, "ease-in-out")
    kf = a.keyframes("prog", T, [(0, "transform:scaleX(0)"), (t_print, "transform:scaleX(1)"), (t_fade1, "transform:scaleX(1)"), (T, "transform:scaleX(0)")])
    a.animate(f"{name}-prog", kf, T)

    side = a.lin3((W, 0, H), (W, D, 0), [(0, "#4a4138"), (0.55, "#37302a"), (1, "#27211c")])
    top = a.lin3((0, 0, H), (W, D, H), [(0, "#3c342d"), (1, "#2c2520")])
    a.rbox(0, W, 0, D, 0, H, 34, "#231e1a", side, top, shade_f="#2e2822", shade_s="#3f372f")

    win_o = (W, 62, 150)
    win = a.rr(win_o, (0, 1, 0), (0, 0, 1), 392, 424, 28)
    wg = a.lin3((W, 62, 574), (W, 454, 150), [(0, "#2d2620"), (0.5, "#15110d"), (1, "#0d0a07")])
    a.path(win, wg)
    cl = a.clip(win)
    a.open(clip=cl)
    d = a.poly([(W, 62, 452), (W, 454, 452)], close=False)
    d += a.poly([(W, 120, 150), (W, 120, 574)], close=False)
    d += a.poly([(W, 392, 150), (W, 392, 574)], close=False)
    a.path(d, stroke="#6e6256", sw=1.1, op=0.22)
    a.path(a.poly([(W, 62, 560), (W, 190, 574), (W, 62, 300)]), "#fff6e8", op=0.05)
    a.close()
    a.path(win, stroke="#0a0705", sw=1.2)
    a.path(a.rr((W, 60, 148), (0, 1, 0), (0, 0, 1), 396, 428, 30), stroke="#6a5e52", sw=0.5, op=0.7)
    a.open(tf=a.matrix((W, 214, 556), (0, 1, 0), (0, 0, -1)))
    a.add(f'<text font-family="DM Sans,system-ui,sans-serif" font-size="14" font-weight="600" fill="{CREAM}" opacity=".85">Bambu Lab</text>')
    a.close()

    a.path(a.rr((62, 112, H), (1, 0, 0), (0, 1, 0), 396, 300, 12), "#191512", op=0.55)
    ams2(a, 66, 454, 118, 404, H + 2, ["cream", "teal", "olive", "honey"], 3, f"{name}-pulse")

    # Profundidad comprimida: en axonométrico estricto la pared izquierda taparía medio interior.
    DOOR = (30, 24, 410, 512)
    door = a.rr((DOOR[0], 0, DOOR[1]), (1, 0, 0), (0, 0, 1), DOOR[2], DOOR[3], 9)
    a.path(door, "#0d0a07")
    cl = a.clip(door)
    a.open(clip=cl)
    IY = 236
    x0, x1, z0, z1 = 30, 470, 24, 540
    back = a.lin3((0, IY, z1), (0, IY, z0), [(0, "#54483d"), (0.5, "#2c241e"), (1, "#14100c")])
    a.path(a.poly([(x0, IY, z0), (x1, IY, z0), (x1, IY, z1), (x0, IY, z1)]), back)
    left = a.lin3((x0, 0, z1), (x0, IY, z0), [(0, "#3a3028"), (1, "#1a1511")])
    a.path(a.poly([(x0, 0, z0), (x0, IY, z0), (x0, IY, z1), (x0, 0, z1)]), left)
    a.path(a.poly([(x0, 0, z0), (x1, 0, z0), (x1, IY, z0), (x0, IY, z0)]), "#0f0c09")
    lg = a.lin3((0, IY, z1), (0, IY, z1 - 200), [(0, "#ffe9c9", 0.28), (1, "#ffe9c9", 0)])
    a.path(a.poly([(x0, IY, z1 - 200), (x1, IY, z1 - 200), (x1, IY, z1), (x0, IY, z1)]), lg)
    d = ""
    for xx in (112, 392):
        d += a.poly([(xx, IY - 2, z0), (xx, IY - 2, z1)], close=False)
    a.path(d, stroke="#85796c", sw=1.6, op=0.5)
    a.path(a.poly([(x0 + 1, 8, Zp + 94), (x0 + 1, IY, Zp + 94)], close=False), stroke="#a3968a", sw=1.6, op=0.8)
    for i in range(6):
        hx = 148 + i * 34
        c = a.lin3((hx - 9, IY - 4, 0), (hx + 9, IY - 4, 0), [(0, "#2a231d"), (0.5, "#85796c"), (1, "#231c17")])
        a.path(a.rr((hx - 9, IY - 4, 150), (1, 0, 0), (0, 0, 1), 18, 58, 3), c)
        a.path(a.poly([(hx - 7, IY - 4, 176), (hx + 7, IY - 4, 176)], close=False), stroke=HONEY, sw=1.4)
        a.path(a.poly([(hx, IY - 4, 150), (hx, IY - 4, 140)], close=False), stroke="#a3968a", sw=1.3)
    a.path(a.poly([(136, IY - 6, 144), (346, IY - 6, 144)], close=False), stroke="#0d0a07", sw=3.2)

    BX0, BX1, BY0, BY1 = 72, 424, 10, 214
    cx, cy = 246, 112
    a.open(cls=f"{name}-bed")
    a.box(104, 126, BY1, IY, z_bed - 20, z_bed - 8, side="#2a231d", top="#4a4036")
    a.box(384, 406, BY1, IY, z_bed - 20, z_bed - 8, side="#2a231d", top="#4a4036")
    a.box(BX0, BX1, BY0, BY1, z_bed - 16, z_bed, front="#1a1612", side="#120e0b")
    plate = a.lin3((BX0, BY0, z_bed), (BX1, BY1, z_bed), [(0, "#4b4036"), (1, "#332a23")])
    a.path(a.poly([(BX0, BY0, z_bed), (BX1, BY0, z_bed), (BX1, BY1, z_bed), (BX0, BY1, z_bed)]), plate)
    d = ""
    for gx in range(BX0 + 32, BX1, 32):
        d += a.poly([(gx, BY0, z_bed), (gx, BY1, z_bed)], close=False)
    for gy in range(BY0 + 28, BY1, 28):
        d += a.poly([(BX0, gy, z_bed), (BX1, gy, z_bed)], close=False)
    a.path(d, stroke="#fff3df", sw=0.3, op=0.13)
    a.path(a.poly([(96, BY0, z_bed - 8), (236, BY0, z_bed - 8)], close=False), stroke="#d9cfc0", sw=0.8, op=0.65)
    a.glyphs("330 320 320", (250, BY0, z_bed - 3), 8, "#d9cfc0", sw=0.55, track=1.1)
    led_y = BY0 - 2
    glow = a.lin3((0, led_y, z_bed - 18), (0, led_y, z_bed - 50), [(0, "#ffe9c9", 0.45), (1, "#ffe9c9", 0)])
    a.path(a.poly([(BX0 + 8, led_y, z_bed - 18), (BX1 - 8, led_y, z_bed - 18), (BX1 - 8, led_y, z_bed - 50), (BX0 + 8, led_y, z_bed - 50)]), glow)
    a.path(a.rr((BX0 + 8, led_y, z_bed - 24), (1, 0, 0), (0, 0, 1), BX1 - BX0 - 16, 6, 3), "#fff7e8")
    a.close()

    # La cama baja y el recorte se queda en el plano de la boquilla: así la pieza crece por arriba.
    plane = a.p(cx, cy, Zp)
    cut = f"M0 {n(plane[1])}H{a.w}V{a.h}H0Z"
    cc = a.clip(cut)
    outline = gear_outline(cx, cy, 58, 72, 12)
    a.open(clip=cc)
    a.open(cls=f"{name}-pfade")
    a.open(cls=f"{name}-bed")
    prism_sides(a, outline, z_bed, z_bed + Hp, ["#8a4a14", "#a85f1c", "#c87a2a", "#dc9543"])
    a.close()
    a.close()
    a.close()
    a.open(cls=f"{name}-cap")
    capd = a.poly([(px, py, Zp) for px, py in outline])
    a.path(capd, "#eeaa58")
    a.path(a.ellipse_z(cx, cy, Zp, 44), stroke="#c87a2a", sw=0.5, op=0.9)
    d = ""
    for k in range(-5, 6):
        off = k * 11
        half = math.sqrt(max(0, 44 * 44 - off * off))
        if half > 0:
            d += a.poly([(cx + off - half * 0.7, cy + off + half * 0.7, Zp), (cx + off + half * 0.7, cy + off - half * 0.7, Zp)], close=False)
    a.path(d, stroke="#c87a2a", sw=0.4, op=0.8)
    a.path(a.ellipse_z(cx, cy, Zp, 18), "#6b2c0a")
    a.path(a.ellipse_z(cx, cy, Zp - 6, 18), "#3d1806")
    a.close()

    by = cy + 44
    bz = Zp + 96
    a.open(cls=f"{name}-hy")
    a.box(x0, x1, by - 14, by + 14, bz - 15, bz + 15, front="#1b1612", top="#352c25")
    rail = a.lin3((0, by - 14, bz + 11), (0, by - 14, bz - 2), [(0, "#e6e0d5"), (1, "#8d8478")])
    a.path(a.poly([(x0, by - 14, bz - 2), (x1, by - 14, bz - 2), (x1, by - 14, bz + 11), (x0, by - 14, bz + 11)]), rail)
    bolts = ""
    for bx in range(x0 + 14, x1, 26):
        q = a.p(bx, by - 14, bz + 4.5)
        bolts += f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="1.1"/>'
    a.add(f'<g fill="#3a3027">{bolts}</g>')
    a.open(cls=f"{name}-hx")
    hy = cy
    tg = a.lin3((cx - 46, hy - 30, 0), (cx + 46, hy - 30, 0), [(0, "#f0ebe2"), (0.55, "#cfc9bd"), (1, "#a9a296")])
    a.rbox(cx - 46, cx + 46, hy - 30, hy + 36, Zp + 58, Zp + 156, 14, tg, "#7f786d", "#efe9df", shade_f="#b5aea2", shade_s="#8c857a", edge="#3b3027", sw=0.7)
    a.path(a.poly([(cx + 20, hy - 30, Zp + 62), (cx + 20, hy - 30, Zp + 152)], close=False), stroke="#6d665c", sw=0.8)
    a.open(tf=a.matrix((cx - 40, hy - 30, Zp + 84), (1, 0, 0), (0, 0, -1)))
    a.add('<text font-family="DM Sans,system-ui,sans-serif" font-size="11" font-weight="600" fill="#463a2e">Bambu Lab</text>')
    a.close()
    a.path(a.rr((cx - 40, hy - 30, Zp + 124), (1, 0, 0), (0, 0, 1), 52, 20, 4), "#8c857a", op=0.55)
    a.rbox(cx - 38, cx + 38, hy - 26, hy + 30, Zp + 16, Zp + 58, 8, "#1e1916", "#100c09", "#2d2620", edge="#050403", sw=0.5)
    a.path(a.ellipse_x(cx + 38, hy + 2, Zp + 38, 14), "#2c2520", stroke="#5c5146", sw=0.5)
    a.path(a.rr((cx - 18, hy - 26, Zp + 24), (1, 0, 0), (0, 0, 1), 36, 24, 3), "#312a24", stroke="#5c5146", sw=0.4)
    a.path(a.poly([(cx - 8, hy, Zp + 16), (cx + 8, hy, Zp + 16), (cx + 3, hy, Zp + 3), (cx, hy, Zp), (cx - 3, hy, Zp + 3)]), a.lin3((cx - 8, hy, 0), (cx + 8, hy, 0), [(0, "#f0c27c"), (1, "#8a5a18")]))
    q = a.p(cx, hy, Zp)
    tip = a.rad(q[0], q[1], 9, [(0, "#ffdca8", 1), (0.35, "#ff8a2a", 0.7), (1, "#ff8a2a", 0)])
    a.add(f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="9" fill="{tip}" class="{name}-tip"/>')
    a.close()
    a.close()
    a.close()  # clip interior

    glass = a.lin3((30, 0, 536), (440, 0, 24), [(0, "#fff8ec", 0.1), (0.4, "#fff8ec", 0.02), (1, "#000", 0.2)])
    a.path(door, glass)
    a.open(clip=cl)
    a.path(a.poly([(52, 0, 540), (160, 0, 540), (36, 0, 300), (30, 0, 300)]), "#fff8ec", op=0.055)
    a.path(a.poly([(186, 0, 540), (214, 0, 540), (66, 0, 24), (38, 0, 24)]), "#fff8ec", op=0.04)
    a.close()
    a.path(door, stroke="#050403", sw=1.5)

    lp = a.lin3((0, 0, 0), (30, 0, 0), [(0, "#6e6358"), (0.5, "#4a4037"), (1, "#26201b")])
    a.path(a.poly([(0, 0, 24), (30, 0, 24), (30, 0, 536), (0, 0, 536)]), lp)
    rp = a.lin3((440, 0, 0), (W - 30, 0, 0), [(0, "#1c1814"), (1, "#332c26")])
    a.path(a.poly([(440, 0, 24), (W - 30, 0, 24), (W - 30, 0, 536), (440, 0, 536)]), rp)
    a.path(a.poly([(0, 0, 0), (W - 30, 0, 0), (W - 30, 0, 24), (0, 0, 24)]), "#181411")
    band = a.lin3((0, 0, H), (0, 0, 536), [(0, "#26201b"), (1, "#14100c")])
    a.path(a.poly([(0, 0, 536), (W - 30, 0, 536), (W - 30, 0, H), (0, 0, H)]), band)
    a.path(a.poly([(0, 0, H), (W - 30, 0, H)], close=False), stroke="#6e6358", sw=0.8)
    hg = a.lin3((424, 0, 0), (438, 0, 0), [(0, "#0b0806"), (0.6, "#2a241f"), (1, "#50463c")])
    a.path(a.rr((424, -4, 262), (1, 0, 0), (0, 0, 1), 14, 136, 6), hg, stroke="#050403", sw=0.5)
    for sx in (44, 62):
        q = a.p(sx, 0, 44)
        a.add(f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="1.5" fill="#5e5347"/>')
    a.open(tf=a.matrix((330, 0, 590), (1, 0, 0), (0, 0, -1)))
    a.add(f'<text font-family="DM Sans,system-ui,sans-serif" font-size="10.5" font-weight="600" fill="{CREAM}" opacity=".85"><tspan x="0" y="0">Bambu</tspan><tspan x="0" y="12">Lab</tspan></text>')
    a.close()
    a.glyphs("H2C", (372, 0, 606), 25, CREAM, track=1.2)
    SX, SZ, SW, SH = 10, 530, 146, 84
    a.path(a.rr((SX + 4, 0, SZ - 3), (1, 0, 0), (0, 0, 1), SW, SH, 9), "#050403", op=0.7)
    a.path(a.rr((SX, -9, SZ), (1, 0, 0), (0, 0, 1), SW, SH, 9), "#0b0806", stroke="#5a4f44", sw=0.7)
    a.open(tf=a.matrix((SX, -9, SZ + SH), (1, 0, 0), (0, 0, -1)))
    a.rect(6, 6, SW - 12, SH - 12, "#16110d", rx=4)
    for i in range(5):
        a.rect(12, 12 + i * 11, 8, 7, "#c87a2a" if i == 1 else "#6e6256", rx=1.5)
        a.rect(24, 13 + i * 11, 26 if i % 2 else 34, 2.2, "#b3a798", rx=1)
        a.rect(24, 17 + i * 11, 18, 1.6, "#6e6256", rx=0.8)
    a.rect(72, 12, 62, 40, "#2c241d", rx=3)
    a.add('<path d="M84 42 L118 42 L126 30 L94 30Z" fill="#6e6256"/><path d="M100 36 l6 -14 l6 14Z" fill="#e09a4a"/>')
    a.rect(12, 67, SW - 24, 4.4, "#3a3027", rx=2.2)
    a.add(f'<rect x="12" y="67" width="{SW - 24}" height="4.4" rx="2.2" fill="#e09a4a" class="{name}-prog"/>')
    a.close()
    a.css.append(f".{name}-prog{{transform-origin:12px 69px}}")

    if floor_ams:
        ams2(a, W + 36, W + 36 + 388, 40, 326, 0, ["cream", "honey", "olive", "rust"], 1, f"{name}-pulse")
    return a.write(outdir)


def touch_screen(a, x, z, w, h, y, prog_cls):
    a.path(a.rr((x + 4, y + 9, z - 3), (1, 0, 0), (0, 0, 1), w, h, 8), "#14100c", op=0.55)
    a.path(a.rr((x, y, z), (1, 0, 0), (0, 0, 1), w, h, 8), "#0b0806", stroke="#6a5e52", sw=0.7)
    a.open(tf=a.matrix((x, y, z + h), (1, 0, 0), (0, 0, -1)))
    a.rect(5, 5, w - 10, h - 10, "#17120e", rx=4)
    rows = int((h - 26) / 11)
    for i in range(rows):
        a.rect(10, 10 + i * 11, 8, 7, HONEY if i == 1 else "#6e6256", rx=1.5)
        a.rect(22, 11 + i * 11, 24 if i % 2 else 32, 2.2, "#b3a798", rx=1)
        a.rect(22, 15 + i * 11, 16, 1.6, "#6e6256", rx=0.8)
    a.rect(w * 0.5, 10, w * 0.42, h * 0.5, "#2c241d", rx=3)
    a.rect(10, h - 15, w - 20, 4.4, "#3a3027", rx=2.2)
    a.add(f'<rect x="10" y="{n(h - 15)}" width="{n(w - 20)}" height="4.4" rx="2.2" fill="#e09a4a" class="{prog_cls}"/>')
    a.close()
    a.css.append(f".{prog_cls}{{transform-origin:10px {n(h - 13)}px}}")


def h3c():
    set_view()
    W, D, Hb = 493, 571, 548
    a = Art("h3c", S=0.5, ox=70, oy=512)
    stage(a, shadow=a.p(W * 0.56, D * 0.42, 0) + (200, 70))

    TOOLS = [("honey", 1), ("teal", 3), ("rust", 5), ("cream", 7)]
    FILL = {"honey": ("#d98f3a", "#f0b267"), "teal": ("#3f7f80", "#6aa9a9"), "rust": ("#b8481a", "#dc7440"), "cream": ("#efe7d8", "#fbf6ec")}
    t_seg, t_chg = 4.2, 2.6
    Zp, Hp = 176, 112
    base = 0.62
    z_bed = Zp - base * Hp
    slot_w = 384 / 9
    slot_x = lambda i: 56 + slot_w * (i + 0.5)
    cx, cy = 242, 128
    rack_y = 40
    bands = len(TOOLS)
    events = []
    t = 0.0
    for k in range(bands):
        events.append(("print", t, t + t_seg, k))
        t += t_seg
        if k < bands - 1:
            events.append(("change", t, t + t_chg, k))
            t += t_chg
    t_end = t
    T = round(t_end + 3.6, 1)
    t_fade0, t_fade1 = t_end + 1.4, t_end + 2.4

    def prog_at(k):
        return k / bands

    dz = lambda pr: (base - pr) * Hp
    bed = []
    for ev, t0, t1, k in events:
        if ev == "print":
            bed += [(t0, 0, a.along("z", dz(prog_at(k)))[1]), (t1, 0, a.along("z", dz(prog_at(k + 1)))[1])]
    bed += [(t_fade1, 0, a.along("z", dz(1))[1]), (T, 0, a.along("z", dz(0))[1])]
    kf = a.translate_kf("bed", T, bed)
    a.animate("h3c-bed", kf, T)

    xs, ys, rack = [], [], [(0, 0, 0)]
    drop = a.along("z", -48)
    for ev, t0, t1, k in events:
        if ev == "print":
            for tt, d in zigzag(t0 + 0.2, t1, 0.92, 46, settle=0)[:-1]:
                xs.append((tt, d))
            for tt, d in zigzag(t0 + 0.2, t1, 2.1, 20, settle=0)[:-1]:
                ys.append((tt, d))
            xs.append((t1, 0))
            ys.append((t1, 0))
        else:
            sa_, sb = slot_x(TOOLS[k][1]) - cx, slot_x(TOOLS[k + 1][1]) - cx
            yd = rack_y - cy
            xs += [(t0 + 0.6, sa_), (t0 + 1.25, sa_), (t0 + 1.75, sb), (t1 - 0.45, sb), (t1 - 0.05, 0)]
            ys += [(t0 + 0.6, yd), (t1 - 0.45, yd), (t1 - 0.05, 0)]
            rack += [(t0 + 0.45, 0, 0), (t0 + 0.8, *drop), (t1 - 0.65, *drop), (t1 - 0.3, 0, 0)]
    xs += [(t_end + 1.1, -128), (T - 0.5, -128), (T, 0)]
    ys += [(t_end + 1.1, 56), (T - 0.5, 56), (T, 0)]
    rack.append((T, 0, 0))
    kf = a.translate_kf("hx", T, [(tt, *a.along("x", d)) for tt, d in xs])
    a.animate("h3c-hx", kf, T, "cubic-bezier(.45,.05,.55,.95)")
    kf = a.translate_kf("hy", T, [(tt, *a.along("y", d)) for tt, d in ys])
    a.animate("h3c-hy", kf, T, "cubic-bezier(.45,.05,.55,.95)")
    kf = a.translate_kf("rack", T, rack)
    a.animate("h3c-rack", kf, T, "ease-in-out")

    swap_times = {}
    for ev, t0, t1, k in events:
        if ev == "change":
            swap_times[k] = (t0 + 0.95, t0 + 1.5)
    for k, (col, slot) in enumerate(TOOLS):
        t_pick = 0.0 if k == 0 else swap_times[k - 1][1]
        t_drop = swap_times[k][0] if k in swap_times else t_end + 0.2
        on = lambda v: f"opacity:{v}"
        stops = []
        if k == 0:
            stops = [(0, on(1)), (t_drop, on(1)), (t_drop + 0.01, on(0)), (T - 0.01, on(0)), (T, on(1))]
        else:
            stops = [(0, on(0)), (t_pick, on(0)), (t_pick + 0.01, on(1)), (t_drop, on(1)), (t_drop + 0.01, on(0)), (T, on(0))]
        kf = a.keyframes(f"on{k}", T, stops)
        a.animate(f"h3c-on{k}", kf, T, "step-end")
        inv = [(tt, css.replace("opacity:1", "opacity:X").replace("opacity:0", "opacity:1").replace("opacity:X", "opacity:0")) for tt, css in stops]
        kf = a.keyframes(f"off{k}", T, inv)
        a.animate(f"h3c-off{k}", kf, T, "step-end")

    cap_stops = []
    for ev, t0, t1, k in events:
        if ev == "print":
            cap_stops.append((t0, f"fill:{FILL[TOOLS[k][0]][1]}"))
    cap_stops.append((T, f"fill:{FILL[TOOLS[-1][0]][1]}"))
    kf = a.keyframes("capc", T, cap_stops)
    a.animate("h3c-capc", kf, T, "step-end")
    kf = a.keyframes("cap", T, [(0, "opacity:0"), (0.25, "opacity:1"), (t_fade0, "opacity:1"), (t_fade1, "opacity:0"), (T, "opacity:0")])
    a.animate("h3c-cap", kf, T)
    kf = a.keyframes("pfade", T, [(0, "opacity:1"), (t_fade0, "opacity:1"), (t_fade1, "opacity:0"), (T - 0.01, "opacity:0"), (T, "opacity:1")])
    a.animate("h3c-pfade", kf, T)
    tip_stops = []
    for ev, t0, t1, k in events:
        val = 0.95 if ev == "print" else 0
        tip_stops += [(t0, f"opacity:{val}"), (t1 - 0.01, f"opacity:{val}")]
    tip_stops += [(t_end, "opacity:0"), (T, "opacity:0")]
    kf = a.keyframes("tip", T, tip_stops)
    a.animate("h3c-tip", kf, T)
    kf = a.keyframes("prog", T, [(0, "transform:scaleX(0)"), (t_end, "transform:scaleX(1)"), (t_fade1, "transform:scaleX(1)"), (T, "transform:scaleX(0)")])
    a.animate("h3c-prog", kf, T)
    kf = a.keyframes("spin", 9, [(0, "transform:rotate(0deg)"), (9, "transform:rotate(360deg)")])
    a.animate("h3c-spin", kf, 9)

    side = a.lin3((W, 0, Hb), (W, D, 0), [(0, "#d8d3ca"), (0.5, "#c3bdb3"), (1, "#a9a398")])
    a.rbox(0, W, 0, D, 0, Hb, 32, "#dcd7ce", side, "#d1ccc2", shade_f="#d5d0c7", shade_s="#bdb7ad", edge=LINE, sw=0.9)
    win = a.rr((W, 58, 338), (0, 1, 0), (0, 0, 1), 456, 176, 22)
    a.path(win, a.lin3((W, 58, 514), (W, 514, 338), [(0, "#2d2620"), (1, "#0f0c09")]), stroke="#6d665c", sw=0.8)
    cl = a.clip(win)
    a.open(clip=cl)
    for i, (yy, ww, hh) in enumerate(((96, 70, 52), (182, 44, 70), (246, 96, 44), (360, 60, 66), (432, 54, 40))):
        zz = 366 + (i % 2) * 24
        a.path(a.rr((W, yy, zz), (0, 1, 0), (0, 0, 1), ww, hh, 5), "#3a3027", op=0.45)
    a.close()
    a.open(tf=a.matrix((W, 256, 494), (0, 1, 0), (0, 0, -1)))
    a.add(f'<text font-family="DM Sans,system-ui,sans-serif" font-size="14" font-weight="600" fill="{CREAM}">Bambu Lab</text>')
    a.close()
    a.path(a.poly([(W, 236, 0), (W, 330, 0), (W, 318, 24), (W, 248, 24)]), "#1c1713")

    xa, xb = 6, W - 6
    zl = Hb + 168  # altura media del reborde
    C_y, U, V = 286, (0, 279, 30), (0, 0, 118)
    dome_c = lambda x: (x, C_y, zl + 30)
    vu, vv, vx = a.v(*U), a.v(*V), a.v(1, 0, 0)
    tA = math.degrees(math.atan2(cross2(vv, vx), cross2(vu, vx)))
    while tA < 0:
        tA += 180
    while tA > 180:
        tA -= 180
    dome = a.arc(dome_c(xa), U, V, 180, tA)
    dome += a.arc(dome_c(xb), U, V, tA, 0, "L")
    dome += "L" + a.pt((xb, 7, zl)) + "L" + a.pt((xa, 7, zl)) + "Z"
    rear = [(xb, D - 8, Hb), (xb, D - 72, Hb), (xb, D - 64, zl + 26), (xb, D - 6, zl + 58)]
    a.path(a.poly([(xa, 20, Hb), (xb, 20, Hb), (xb, D - 8, Hb), (xb, D - 8, zl + 30), (xa, D - 8, zl + 30)]), "#1d1814")
    a.path(dome, "#2a231d")
    clip_d = a.clip(dome)
    a.open(clip=clip_d)
    for i, col in enumerate(("ink", "honey", "rust")):
        sx0 = 22 + i * 78
        spool_x(a, sx0, sx0 + 72, 404, zl + 10, 86, col)
    a.box(262, 470, 330, 480, zl - 20, zl + 70, front="#2a231d", side="#201a15", top="#3f362e")
    front_row = ["cream", "honey", "teal", "olive", "rust", "cream"]
    sw_ = (xb - xa - 12) / len(front_row)
    for i, col in enumerate(front_row):
        sx0 = xa + 6 + i * sw_
        spool_x(a, sx0 + 2, sx0 + sw_ - 2, 170, zl + 8, 90, col, holes=(i == 5), spin="h3c-spin" if i == 5 else None)
    a.close()
    neck = [(xa, 12, Hb), (xb, 12, Hb), (xb, 16, zl - 8), (xa, 16, zl - 8)]
    ng = a.lin3((0, 14, zl), (0, 14, Hb), [(0, "#17120e"), (1, "#2e2620")])
    a.path(a.poly(neck), ng)
    cl_n = a.clip(a.poly(neck))
    a.open(clip=cl_n)
    d = ""
    for i in range(9):
        sx = 56 + (i + 0.5) * slot_w
        top_x = 300 + (i - 4) * 22
        p0, p3 = a.p(sx, 14, Hb), a.p(top_x, 14, zl - 8)
        c1, c2 = a.p(sx, 14, Hb + 96), a.p(top_x - 96, 14, zl - 30)
        d += f"M{n(p0[0])} {n(p0[1])}C{n(c1[0])} {n(c1[1])} {n(c2[0])} {n(c2[1])} {n(p3[0])} {n(p3[1])}"
    a.path(d, stroke="#e7dfd1", sw=0.8, op=0.62)
    a.path(a.poly([(xa, 12, Hb + 60), (150, 12, Hb), (xa, 12, Hb)]), "#fff8ec", op=0.05)
    gl = a.lin3((0, 14, zl), (0, 14, Hb), [(0, "#fff8ec", 0), (1, "#fff8ec", 0.1)])
    a.path(a.poly(neck), gl)
    a.close()
    a.path(a.poly([(xa, 12, Hb), (xa, 16, zl - 8)], close=False), stroke="#6e6256", sw=0.8, op=0.7)
    side_win = [(xb, 16, Hb), (xb, D - 74, Hb), (xb, D - 66, zl + 34), (xb, 16, zl - 6)]
    a.path(a.poly(side_win), a.lin3((xb, 16, zl), (xb, D - 80, Hb), [(0, "#3a3027", 0.96), (1, "#17120e", 0.96)]))
    d = a.poly([(xb, 60, Hb + 8), (xb, 250, zl - 4)], close=False)
    d += a.poly([(xb, 440, Hb + 8), (xb, 250, zl - 4)], close=False)
    a.path(d, stroke="#6e6256", sw=2, op=0.3)
    rg = a.lin3((xb, D - 78, 0), (xb, D - 8, 0), [(0, "#1c1713"), (1, "#3a3027")])
    a.path(a.poly(rear), rg, stroke="#100c09", sw=0.6)
    glass = a.lin3((0, C_y, zl + 170), (0, 8, zl - 2), [(0, "#fffaf2", 0.36), (0.36, "#fffaf2", 0.07), (1, "#1a0f06", 0.14)])
    a.path(dome, glass)
    cap = a.arc(dome_c(xb), U, V, 0, 180) + "Z"
    a.path(cap, a.lin3((xb, D, zl + 90), (xb, 8, zl + 10), [(0, "#4a4037", 0.9), (1, "#231d18", 0.62)]))
    a.path(a.arc(dome_c(xa), U, V, 174, tA) + a.arc(dome_c(xb), U, V, tA, 6, "L"), stroke="#fff6e8", sw=1.1, op=0.8)
    a.path(a.arc(dome_c(xb), U, V, 4, 176), stroke="#9b8f81", sw=0.7, op=0.75)
    lip_h = 27
    lip_f = [(xa, 6, zl - 12), (xb, 6, zl - 12), (xb, 6, zl - 12 + lip_h), (xa, 6, zl - 12 + lip_h)]
    a.path(a.poly(lip_f), a.lin3((0, 6, zl + 15), (0, 6, zl - 12), [(0, "#322a23"), (1, "#14100c")]))
    lip_s = [(xb, 6, zl - 12), (xb, D - 4, zl + 48), (xb, D - 4, zl + 48 + lip_h), (xb, 6, zl - 12 + lip_h)]
    a.path(a.poly(lip_s), a.lin3((xb, 6, 0), (xb, D, 0), [(0, "#2a231d"), (1, "#3f362e")]))
    a.path(a.poly([(xa, 6, zl + 15), (xb, 6, zl + 15), (xb, D - 4, zl + 75)], close=False), stroke="#7a6e62", sw=0.7, op=0.85)
    a.path(a.rr(((xa + xb) / 2 - 86, 3, zl - 6), (1, 0, 0), (0, 0, 1), 172, 13, 4), a.lin3((0, 3, zl + 7), (0, 3, zl - 6), [(0, "#6e6256"), (1, "#3a3027")]))
    a.glyphs("AMS 3H", (xb - 104, 6, zl + 8), 11, "#b3a798", sw=0.7, track=1.2)

    a.path(a.poly([(0 + 32, 0, 0), (W - 32, 0, 0), (W - 32, 0, Hb), (32, 0, Hb)]), a.lin3((0, 0, Hb), (0, 0, 0), [(0, "#e4dfd6"), (1, "#cfcac0")]))
    DX0, DX1, DZ0, DZ1 = 34, W - 30, 28, 452
    frame = a.rr((DX0, 0, DZ0), (1, 0, 0), (0, 0, 1), DX1 - DX0, DZ1 - DZ0, 7)
    a.path(frame, "#0c0907", stroke=LINE, sw=0.8)
    door = a.rr((DX0 + 7, 0, DZ0 + 7), (1, 0, 0), (0, 0, 1), DX1 - DX0 - 14, DZ1 - DZ0 - 14, 4)
    cl = a.clip(door)
    a.open(clip=cl)
    IY = 244
    x0, x1, z0, z1 = DX0, DX1 + 20, DZ0, DZ1
    back = a.lin3((0, IY, z1), (0, IY, z0), [(0, "#4f443a"), (0.45, "#2a221c"), (1, "#120e0a")])
    a.path(a.poly([(x0, IY, z0), (x1, IY, z0), (x1, IY, z1), (x0, IY, z1)]), back)
    left = a.lin3((x0, 0, z1), (x0, IY, z0), [(0, "#3a3028"), (1, "#181310")])
    a.path(a.poly([(x0, 0, z0), (x0, IY, z0), (x0, IY, z1), (x0, 0, z1)]), left)
    a.path(a.poly([(x0, 0, z0), (x1, 0, z0), (x1, IY, z0), (x0, IY, z0)]), "#0e0b08")
    d = ""
    for xx in (106, 384):
        d += a.poly([(xx, IY - 2, z0), (xx, IY - 2, z1)], close=False)
    a.path(d, stroke="#85796c", sw=1.6, op=0.5)
    d = ""
    for yy in (40, 120):
        d += a.poly([(x0 + 1, yy, z0), (x0 + 1, yy, z1)], close=False)
    a.path(d, stroke="#a3968a", sw=1.2, op=0.45)

    BX0, BX1, BY0, BY1 = 72, 424, 10, 214
    a.open(cls="h3c-bed")
    a.box(BX0, BX1, BY0, BY1, z_bed - 16, z_bed, front="#1a1612", side="#120e0b")
    plate = a.lin3((BX0, BY0, z_bed), (BX1, BY1, z_bed), [(0, "#4b4036"), (1, "#332a23")])
    a.path(a.poly([(BX0, BY0, z_bed), (BX1, BY0, z_bed), (BX1, BY1, z_bed), (BX0, BY1, z_bed)]), plate)
    d = ""
    for gx in range(BX0 + 32, BX1, 32):
        d += a.poly([(gx, BY0, z_bed), (gx, BY1, z_bed)], close=False)
    for gy in range(BY0 + 28, BY1, 28):
        d += a.poly([(BX0, gy, z_bed), (BX1, gy, z_bed)], close=False)
    a.path(d, stroke="#fff3df", sw=0.3, op=0.13)
    a.glyphs("330 320 325", (250, BY0, z_bed - 3), 8, "#d9cfc0", sw=0.55, track=1.1)
    led_y = BY0 - 2
    glow = a.lin3((0, led_y, z_bed - 18), (0, led_y, z_bed - 50), [(0, "#ffe9c9", 0.45), (1, "#ffe9c9", 0)])
    a.path(a.poly([(BX0 + 8, led_y, z_bed - 18), (BX1 - 8, led_y, z_bed - 18), (BX1 - 8, led_y, z_bed - 50), (BX0 + 8, led_y, z_bed - 50)]), glow)
    a.path(a.rr((BX0 + 8, led_y, z_bed - 24), (1, 0, 0), (0, 0, 1), BX1 - BX0 - 16, 6, 3), "#fff7e8")
    a.close()

    Rp = 66
    plane = a.p(cx, cy, Zp)
    cc = a.clip(f"M0 {n(plane[1])}H{a.w}V{a.h}H0Z")
    a.open(clip=cc)
    a.open(cls="h3c-pfade")
    a.open(cls="h3c-bed")
    for k, (col, _) in enumerate(TOOLS):
        zk0 = z_bed + Hp * k / bands
        zk1 = z_bed + Hp * (k + 1) / bands
        c0, c1 = FILL[col]
        dk = SPOOLS[col][1]
        g = a.cylz_grad(cx, cy, zk0, Rp, [(0, dk), (0.3, c0), (0.55, c1), (1, dk)])
        a.path(a.cylz_path(cx, cy, zk0, zk1 + 0.6, Rp), g)
    d = ""
    for lz in range(0, Hp, 7):
        d += a.arc((cx, cy, z_bed + lz), (Rp, 0, 0), (0, Rp, 0), math.degrees(AZ) - 180, math.degrees(AZ))
    a.path(d, stroke="#1a0f06", sw=0.3, op=0.22)
    a.close()
    a.close()
    a.close()
    a.open(cls="h3c-cap")
    a.path(a.ellipse_z(cx, cy, Zp, Rp), FILL[TOOLS[2][0]][1], cls="h3c-capc")
    a.path(a.ellipse_z(cx, cy, Zp, Rp - 7), "#4a2a14")
    a.path(a.ellipse_z(cx, cy, Zp - 7, Rp - 7), "#2a1605")
    a.close()

    by = cy + 46
    bz = Zp + 80
    a.open(cls="h3c-hy")
    a.box(x0, x1, by - 13, by + 13, bz - 13, bz + 13, front="#1b1612", top="#352c25")
    rail = a.lin3((0, by - 13, bz + 10), (0, by - 13, bz - 2), [(0, "#e6e0d5"), (1, "#8d8478")])
    a.path(a.poly([(x0, by - 13, bz - 2), (x1, by - 13, bz - 2), (x1, by - 13, bz + 10), (x0, by - 13, bz + 10)]), rail)
    a.open(cls="h3c-hx")
    hy = cy
    a.rbox(cx - 50, cx + 50, hy - 24, hy + 30, Zp + 32, Zp + 118, 12, "#2a241f", "#16120e", "#3a322b", edge="#050403", sw=0.5, shade_f="#2f2822", shade_s="#1a1612")
    a.path(a.rr((cx - 28, hy - 25, Zp + 40), (1, 0, 0), (0, 0, 1), 56, 72, 4), "#14100c", stroke="#5c5146", sw=0.5)
    q = a.p(cx, hy - 25, Zp + 92)
    a.add(f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="2.1" fill="#fff7e8"/>')
    for k, (col, _) in enumerate(TOOLS):
        a.open(cls=f"h3c-on{k}", op=None if k == 2 else 0)
        c0 = SPOOLS[col][0]
        a.path(a.rr((cx - 15, hy - 27, Zp + 14), (1, 0, 0), (0, 0, 1), 30, 42, 4), "#3a322b", stroke="#6e6256", sw=0.4)
        a.path(a.rr((cx - 12, hy - 28, Zp + 44), (1, 0, 0), (0, 0, 1), 24, 12, 2), c0, stroke="#1a0f06", sw=0.3)
        a.path(a.poly([(cx - 8, hy, Zp + 14), (cx + 8, hy, Zp + 14), (cx + 3, hy, Zp + 3), (cx, hy, Zp), (cx - 3, hy, Zp + 3)]), a.lin3((cx - 8, hy, 0), (cx + 8, hy, 0), [(0, "#f0c27c"), (1, "#8a5a18")]))
        a.close()
    q = a.p(cx, hy, Zp)
    tip = a.rad(q[0], q[1], 9, [(0, "#ffdca8", 1), (0.35, "#ff8a2a", 0.7), (1, "#ff8a2a", 0)])
    a.add(f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="9" fill="{tip}" class="h3c-tip"/>')
    a.close()
    a.close()

    tool_of_slot = {slot: (k, col) for k, (col, slot) in enumerate(TOOLS)}
    a.open(cls="h3c-rack")
    for i in range(9):
        sx = slot_x(i)
        drawn_cls = f"h3c-off{tool_of_slot[i][0]}" if i in tool_of_slot else None
        col = tool_of_slot[i][1] if i in tool_of_slot else ("ink" if i % 2 else "cream")
        a.open(cls=drawn_cls, op=0 if i == TOOLS[2][1] else None)
        a.path(a.rr((sx - 12, rack_y, 318), (1, 0, 0), (0, 0, 1), 24, 44, 3), "#3a322b", stroke="#6e6256", sw=0.4)
        a.path(a.rr((sx - 9, rack_y - 1, 344), (1, 0, 0), (0, 0, 1), 18, 11, 2), SPOOLS[col][0], stroke="#1a0f06", sw=0.3)
        a.path(a.poly([(sx - 5, rack_y, 318), (sx + 5, rack_y, 318), (sx, rack_y, 306)]), "#c9a267")
        a.close()
    a.box(54, 442, rack_y, rack_y + 26, 362, 438, front="#1a1612", top="#2e2620")
    for i in range(9):
        sx = slot_x(i)
        a.path(a.rr((sx - 16, rack_y, 384), (1, 0, 0), (0, 0, 1), 32, 46, 3), "#0b0806", stroke="#4a4037", sw=0.5)
        a.path(a.rr((sx - 2, rack_y, 394), (1, 0, 0), (0, 0, 1), 4, 28, 2), "#fff7e8", op=0.9)
        a.path(a.poly([(sx - 1.5, rack_y, 368), (sx + 1.5, rack_y, 368), (sx + 1.5, rack_y, 376), (sx - 1.5, rack_y, 376)]), "#e7dfd1")
    a.close()
    a.close()  # clip puerta

    gl = a.lin3((DX0, 0, DZ1), (DX1, 0, DZ0), [(0, "#fff8ec", 0.09), (0.45, "#fff8ec", 0.015), (1, "#000", 0.16)])
    a.path(door, gl)
    a.open(clip=cl)
    a.path(a.poly([(70, 0, DZ1), (150, 0, DZ1), (41, 0, 240), (41, 0, 290)]), "#fff8ec", op=0.05)
    a.close()
    a.open(tf=a.matrix((336, 0, 505), (1, 0, 0), (0, 0, -1)))
    a.add(f'<text font-family="DM Sans,system-ui,sans-serif" font-size="9.5" font-weight="600" fill="#3a3027"><tspan x="0" y="0">Bambu</tspan><tspan x="0" y="11">Lab</tspan></text>')
    a.close()
    a.glyphs("H3C", (374, 0, 520), 23, "#2a2019", track=1.2)
    touch_screen(a, 14, 442, 136, 84, -10, "h3c-prog")
    a.path(a.poly([(32, 0, Hb), (W - 32, 0, Hb)], close=False), stroke="#fff", sw=0.8, op=0.7)

    return a.write()


A2L_T = 20
A2L_XS = 1.55
A2L_YS = 2.7
A2L_HX = 104
A2L_BY = 58
A2L_PLATE = 86
A2L_HP = 118
A2L_BASE = 0.6


def a2l_unit(a, full=True):
    """Una A2L completa. El marco queda en y≈300; la cama corre en Y y el pórtico sube en Z."""
    col_y0, col_y1 = 282, 318
    Zp = A2L_PLATE + A2L_BASE * A2L_HP
    zr = Zp + 76
    bx0, bx1, by0, by1 = 78, 428, 46, 386
    tcx, tcy = 253, 240

    a.path(a.rr((4, 4, 0), (1, 0, 0), (0, 1, 0), 496, 462, 24), "#2a231d")
    a.rbox(0, 505, 0, 470, 8, 62, 24, "#f7f3ea", "#d8d1c3", "#fdfaf3", shade_f="#efe9dd", shade_s="#cfc7b7", edge=LINE, sw=0.8)
    d = ""
    for xx in (150, 356):
        d += a.poly([(xx, 28, 62), (xx, 446, 62)], close=False)
    a.path(d, stroke="#b9b0a0", sw=1.4)
    a.path(a.poly([(240, 40, 62), (266, 40, 62), (266, 440, 62), (240, 440, 62)]), "#e6e0d3")

    for xc in (54, 450):
        a.path(a.poly([(xc - 7, col_y1, 330), (xc + 7, col_y1, 330), (xc + 7, 452, 62), (xc - 7, 452, 62)]), a.lin3((xc, col_y1, 330), (xc, 452, 62), [(0, "#5e5347"), (1, "#3a3027")]), stroke="#241c15", sw=0.5)

    a.box(36, 74, col_y0, col_y1, 58, 505, front=a.lin3((36, col_y0, 0), (74, col_y0, 0), [(0, "#e8e4db"), (1, "#c3bdb2")]), side="#1c1713")
    a.path(a.poly([(74, col_y0 + 8, 62), (74, col_y1 - 8, 62), (74, col_y1 - 8, 500), (74, col_y0 + 8, 500)]), "#0e0b08")

    a.open(cls="a2l-bedy")
    a.box(150, 356, by0 + 40, by1 - 40, 62, 74, front="#3a3027", side="#2a231d")
    a.box(bx0, bx1, by0, by1, A2L_PLATE - 11, A2L_PLATE, front=a.lin3((bx0, by0, 0), (bx1, by0, 0), [(0, "#2e2620"), (1, "#1a1612")]), side="#14100c")
    pei = a.lin3((bx0, by0, A2L_PLATE), (bx1, by1, A2L_PLATE), [(0, "#cdb07a"), (0.5, "#b89a66"), (1, "#a58a58")])
    a.path(a.poly([(bx0, by0, A2L_PLATE), (bx1, by0, A2L_PLATE), (bx1, by1, A2L_PLATE), (bx0, by1, A2L_PLATE)]), pei)
    if full:
        d = ""
        for gx in range(bx0 + 25, bx1, 25):
            d += a.poly([(gx, by0, A2L_PLATE), (gx, by1, A2L_PLATE)], close=False)
        for gy in range(by0 + 25, by1, 25):
            d += a.poly([(bx0, gy, A2L_PLATE), (bx1, gy, A2L_PLATE)], close=False)
        a.path(d, stroke="#6b4a1e", sw=0.28, op=0.28)
        a.path(a.poly([(bx0 + 10, by0, A2L_PLATE - 5), (bx0 + 120, by0, A2L_PLATE - 5)], close=False), stroke="#d9cfc0", sw=0.7, op=0.8)

    # Un prisma que sube recortado por su base se ve igual que uno que crece capa por capa.
    R = 36
    hexo = lambda cx, cy: [(cx + R * math.cos(math.radians(60 * k + 30)), cy + R * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    grid = [(143 + i * 110, 112 + j * 104) for j in (2, 1, 0) for i in range(3)]
    top_z = A2L_PLATE + A2L_BASE * A2L_HP
    a.open(cls="a2l-pieces")
    for (cx, cy) in grid:
        outline = hexo(cx, cy)
        scr = [a.p(px, py, A2L_PLATE) for px, py in outline]
        li = min(range(6), key=lambda k: scr[k][0])
        ri = max(range(6), key=lambda k: scr[k][0])
        cand_a, k = [], li
        while True:
            cand_a.append(k)
            if k == ri:
                break
            k = (k + 1) % 6
        cand_b, k = [], li
        while True:
            cand_b.append(k)
            if k == ri:
                break
            k = (k - 1) % 6
        avg = lambda c: sum(scr[i][1] for i in c) / len(c)
        lower = cand_a if avg(cand_a) > avg(cand_b) else cand_b
        pts = [scr[i] for i in lower]
        d = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in pts)
        d += f"L{n(pts[-1][0])} {n(pts[-1][1] - 400)}L{n(pts[0][0])} {n(pts[0][1] - 400)}Z"
        cid = a.clip(d)
        a.open(clip=cid)
        a.open(cls="a2l-rise")
        prism_sides(a, outline, top_z - A2L_HP, top_z, ["#8a4a14", "#a85f1c", "#c87a2a", "#dc9543"])
        a.path(a.poly([(px, py, top_z) for px, py in outline]), "#eeaa58", stroke="#a85f1c", sw=0.3)
        a.path(a.ellipse_z(cx, cy, top_z, R * 0.52), "#6b2c0a")
        a.close()
        a.close()
    a.close()
    a.close()  # cama

    a.box(432, 470, col_y0, col_y1, 58, 505, front=a.lin3((432, col_y0, 0), (470, col_y0, 0), [(0, "#efebe3"), (1, "#c9c3b8")]), side=a.lin3((470, col_y0, 505), (470, col_y1, 58), [(0, "#d6d1c7"), (1, "#a8a297")]))
    a.box(428, 474, col_y0 - 3, col_y1 + 3, 58, 118, front="#5e5347", side="#463c33", top="#6e6256")
    a.box(36, 470, col_y0, col_y1, 478, 505, front=a.lin3((0, col_y0, 505), (0, col_y0, 478), [(0, "#eeeae2"), (1, "#c0baaf")]), side="#b7b1a6", top="#f4f1ea", stroke="#7d756a", sw=0.4)

    a.open(cls="a2l-gz")
    ry0, ry1 = 262, 282
    a.box(-14, 470, ry0, ry1, zr - 15, zr + 15, front=a.lin3((0, ry0, zr + 15), (0, ry0, zr - 15), [(0, "#f2efe8"), (0.5, "#d8d3c9"), (1, "#a6a095")]), top="#faf8f3", stroke="#6d665c", sw=0.4)
    if full:
        bolts = ""
        for bx in range(2, 462, 38):
            q = a.p(bx, ry0, zr)
            bolts += f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="1.1"/>'
        a.add(f'<g fill="#5e5347">{bolts}</g>')
        a.path(a.poly([(-14, ry0, zr - 8), (470, ry0, zr - 8)], close=False), stroke="#8d8478", sw=0.5)
    a.box(-30, -8, ry0 - 8, ry1 + 4, zr - 18, zr + 18, front="#2a231d", side="#14100c", top="#3a3027")
    if full:
        a.box(-46, -14, ry0 - 2, ry0 + 8, zr - 52, zr - 40, front="#1c1713", top="#3a3027")
        a.box(-24, -14, ry0 - 2, ry0 + 8, zr - 52, zr - 16, front="#231c17", side="#14100c")
    a.rbox(462, 548, 242, 300, zr - 34, zr + 30, 9, "#faf7f0", "#d2cbbd", "#fffdf8", edge=LINE, sw=0.7, shade_f="#efe9dd", shade_s="#c9c1b1")
    if full:
        a.glyphs("A2L", (480, 242, zr + 4), 15, "#2a2019", sw=0.9, track=1.1)
        a.path(a.poly([(480, 242, zr + 16), (500, 242, zr + 16)], close=False), stroke="#6e6256", sw=0.8)

    a.open(cls="a2l-hx")
    a.rbox(tcx - 36, tcx + 36, tcy - 16, tcy + 24, zr - 40, zr + 42, 7, a.lin3((tcx - 36, tcy - 16, 0), (tcx + 36, tcy - 16, 0), [(0, "#fffdf8"), (1, "#e9e3d7")]), "#c9c1b1", "#fffdf8", edge=LINE, sw=0.8, shade_f="#e4ddd0", shade_s="#c9c1b1")
    if full:
        kc = (tcx - 2, tcy - 16, zr + 8)
        a.path(a.circle(kc, (13, 0, 0), (0, 0, 13)), "#3a3027")
        a.path(a.circle(kc, (9.5, 0, 0), (0, 0, 9.5)), a.lin3((tcx - 11, tcy - 16, zr + 17), (tcx + 7, tcy - 16, zr - 1), [(0, "#f0c27c"), (1, "#8a5a18")]))
        a.path(a.circle(kc, (3.5, 0, 0), (0, 0, 3.5)), "#3a3027")
        a.open(tf=a.matrix((tcx - 30, tcy - 16, zr - 22), (1, 0, 0), (0, 0, -1)))
        a.add('<text font-family="DM Sans,system-ui,sans-serif" font-size="10" font-weight="600" fill="#463a2e">Bambu Lab</text>')
        a.close()
        a.path(a.poly([(tcx + 22, tcy - 16, zr - 36), (tcx + 22, tcy - 16, zr + 38)], close=False), stroke="#b9b0a0", sw=0.6)
    a.rbox(tcx - 38, tcx + 32, tcy - 22, tcy + 22, Zp + 14, zr - 40, 7, "#231c17", "#100c09", "#3a3027", edge="#050403", sw=0.5)
    a.path(a.poly([(tcx - 8, tcy, Zp + 14), (tcx + 8, tcy, Zp + 14), (tcx + 3, tcy, Zp + 3), (tcx, tcy, Zp), (tcx - 3, tcy, Zp + 3)]), a.lin3((tcx - 8, tcy, 0), (tcx + 8, tcy, 0), [(0, "#f0c27c"), (1, "#8a5a18")]))
    q = a.p(tcx, tcy, Zp)
    tip = a.rad(q[0], q[1], 8, [(0, "#ffdca8", 1), (0.35, "#ff8a2a", 0.65), (1, "#ff8a2a", 0)])
    a.add(f'<circle cx="{n(q[0])}" cy="{n(q[1])}" r="8" fill="{tip}"/>')
    a.box(tcx - 16, tcx + 2, tcy - 4, tcy + 14, zr + 42, zr + 74, front="#f4efe5", side="#c9c1b1", top="#fffdf8", stroke=LINE, sw=0.5)
    a.box(tcx + 8, tcx + 22, tcy - 2, tcy + 12, zr + 42, zr + 60, front="#231c17", side="#100c09", top="#3a3027")
    a.close()
    a.close()  # pórtico

    if full:
        sx, sy = 366, -14
        a.path(a.poly([(sx, sy, 58), (sx + 116, sy, 58), (sx + 116, sy - 2, 112), (sx, sy - 2, 112)]), a.lin3((sx, sy, 112), (sx, sy, 58), [(0, "#fdfaf3"), (1, "#d8d1c3")]), stroke=LINE, sw=0.7)
        a.open(tf=a.matrix((sx, sy - 2, 112), (1, 0, 0), (0, 0, -1)))
        a.rect(5, 4, 106, 46, "#17120e", rx=3)
        for i in range(4):
            a.rect(10, 9 + i * 8, 7, 5, HONEY if i == 1 else "#6e6256", rx=1)
            a.rect(20, 10 + i * 8, 24 if i % 2 else 32, 2, "#b3a798", rx=1)
        a.rect(60, 9, 44, 24, "#2c241d", rx=2)
        a.rect(60, 40, 44, 3, "#3a3027", rx=1.5)
        a.add('<rect x="60" y="40" width="44" height="3" rx="1.5" fill="#e09a4a" class="a2l-prog"/>')
        a.close()


def ams_lite(a, x, y):
    """Soporte con cuatro bobinas. Devuelve la posición de los cuatro acoples de latón."""
    a.path(a.poly([(x - 100, y + 30, 0), (x + 100, y + 30, 0), (x + 100, y + 56, 0), (x - 100, y + 56, 0)]), "#6e6256", stroke="#3a3027", sw=0.5)
    a.path(a.poly([(x - 14, y - 110, 0), (x + 14, y - 110, 0), (x + 14, y + 230, 0), (x - 14, y + 230, 0)]), "#857a6d", stroke="#3a3027", sw=0.5)
    yb = y + 104
    spool_x(a, x - 116, x - 42, yb, 246, 96, "olive", holes=True)
    spool_x(a, x + 42, x + 116, yb, 246, 96, "cream", holes=True, spin="a2l-spin2")
    a.rbox(x - 30, x + 30, y - 6, yb + 26, 0, 318, 14, "#faf7f0", "#d2cbbd", "#fffdf8", edge=LINE, sw=0.8, shade_f="#efe9dd", shade_s="#c9c1b1")
    a.path(a.poly([(x - 30, y + 8, 110), (x + 30, y + 8, 110)], close=False), stroke="#c9c1b1", sw=0.8)
    spool_x(a, x - 116, x - 42, y, 106, 100, "teal", holes=True)
    spool_x(a, x + 42, x + 116, y, 106, 100, "honey", holes=True, spin="a2l-spin1")
    anchors = []
    for (mx, my) in ((x - 62, yb - 16), (x + 62, yb - 16), (x - 62, y + 22), (x + 62, y + 22)):
        mz = 318 if my > y + 40 else 226
        a.rbox(mx - 21, mx + 21, my - 15, my + 15, mz, mz + 28, 6, "#8d8478", "#5e5347", "#b3a798", edge="#2a231d", sw=0.5, shade_f="#7d7366", shade_s="#5e5347")
        a.path(a.ellipse_z(mx, my, mz + 28, 8), "#d9cfc0")
        a.path(a.poly([(mx - 5, my, mz + 28), (mx + 5, my, mz + 28), (mx + 3, my, mz + 42), (mx - 3, my, mz + 42)]), a.lin3((mx - 5, my, 0), (mx + 5, my, 0), [(0, "#f0c27c"), (1, "#8a5a18")]))
        anchors.append(a.p(mx, my, mz + 42))
    return anchors


def a2l():
    set_view()
    a = Art("a2l", S=0.5, ox=20, oy=486)
    T = A2L_T
    t_print = 16.5
    t_fade0, t_fade1 = 17.6, 18.6
    stage(a, shadow=a.p(430, 230, 0) + (262, 74))

    prog_dy = lambda pr: a.along("z", (pr - A2L_BASE) * A2L_HP)[1]
    stops = [(0, 0, prog_dy(0)), (t_print, 0, prog_dy(1)), (t_fade1, 0, prog_dy(1)), (T, 0, prog_dy(0))]
    kf = a.translate_kf("z", T, stops)
    a.animate("a2l-gz", kf, T, delay="var(--d,0s)")
    a.animate("a2l-rise", kf, T, delay="var(--d,0s)", extra="")
    k = a.keyframes("fade", T, [(0, "opacity:1"), (t_fade0, "opacity:1"), (t_fade1, "opacity:0"), (T - 0.01, "opacity:0"), (T, "opacity:1")])
    a.animate("a2l-pieces", k, T, delay="var(--d,0s)")
    hx0, hx1 = a.along("x", -A2L_HX), a.along("x", A2L_HX)
    k = a.translate_kf("x", 1, [(0, *hx0), (1, *hx1)])
    a.css.append(f".a2l-hx{{animation:{k} {A2L_XS}s cubic-bezier(.45,.05,.55,.95) infinite alternate;animation-delay:var(--d,0s);animation-play-state:var(--play,running)}}")
    by0, by1 = a.along("y", -A2L_BY), a.along("y", A2L_BY)
    k = a.translate_kf("y", 1, [(0, *by0), (1, *by1)])
    a.css.append(f".a2l-bedy{{animation:{k} {A2L_YS}s cubic-bezier(.45,.05,.55,.95) infinite alternate;animation-delay:var(--d,0s);animation-play-state:var(--play,running)}}")
    k = a.keyframes("prog", T, [(0, "transform:scaleX(0)"), (t_print, "transform:scaleX(1)"), (t_fade1, "transform:scaleX(1)"), (T, "transform:scaleX(0)")])
    a.animate("a2l-prog", k, T)
    a.css.append(".a2l-prog{transform-origin:60px 41px}")
    k = a.keyframes("spin", 11, [(0, "transform:rotate(0deg)"), (11, "transform:rotate(360deg)")])
    a.animate("a2l-spin1", k, 11)
    a.animate("a2l-spin2", k, 15)

    main_ox, main_oy = a.ox, a.oy
    for (dx, dy), op, delay in (
        ((-760, 660), 0.42, "-7s"),
        ((-60, 760), 0.5, "-3.2s"),
    ):
        ox_, oy_ = a.v(dx, dy, 0)
        a.ox, a.oy = main_ox + ox_, main_oy + oy_
        a.open(op=op, style=f"--d:{delay}")
        a2l_unit(a, full=False)
        a.close()
    a.ox, a.oy = main_ox, main_oy

    a2l_unit(a, full=True)
    anchors = ams_lite(a, 716, 196)

    # Los tubos tienen un extremo fijo en el AMS y el otro sigue al cabezal.
    # Una escala con origen en el acople mantiene fijo ese extremo y mueve el otro en línea recta.
    Zp = A2L_PLATE + A2L_BASE * A2L_HP
    zr = Zp + 76
    tcx, tcy = 253, 240
    head = a.p(tcx - 7, tcy + 5, zr + 74)
    colors = ["#a9b35f", "#cfc5b2", "#5f9fa0", "#dd9f55"]
    dzu, dzd = prog_dy(0), prog_dy(1)
    for i, (ax, ay) in enumerate(anchors):
        hx = head[0] + (i - 1.5) * 1.6
        hy = head[1]
        dx = hx - ax
        # La escala en X lleva el extremo del cabezal; el sesgo en Y lo sube y baja sin mover el acople.
        s0, s1 = 1 + hx0[0] / dx, 1 + hx1[0] / dx
        t0 = math.degrees(math.atan(hx0[1] / (s0 * dx)))
        t1 = math.degrees(math.atan(hx1[1] / (s1 * dx)))
        k = a.keyframes(f"t{i}", 1, [(0, f"transform:skewY({t0:.3f}deg) scaleX({s0:.4f})"), (1, f"transform:skewY({t1:.3f}deg) scaleX({s1:.4f})")])
        a.css.append(f".a2l-t{i}{{animation:{k} {A2L_XS}s cubic-bezier(.45,.05,.55,.95) infinite alternate;animation-play-state:var(--play,running);transform-origin:{ax:.1f}px {ay:.1f}px}}")
        zu, zd = math.degrees(math.atan(dzu / dx)), math.degrees(math.atan(dzd / dx))
        k = a.keyframes(f"z{i}", T, [(0, f"transform:skewY({zu:.3f}deg)"), (t_print, f"transform:skewY({zd:.3f}deg)"), (t_fade1, f"transform:skewY({zd:.3f}deg)"), (T, f"transform:skewY({zu:.3f}deg)")])
        a.css.append(f".a2l-z{i}{{animation:{k} {T}s linear infinite;animation-play-state:var(--play,running);transform-origin:{ax:.1f}px {ay:.1f}px}}")
        rise = 150 + i * 22
        d = f"M{n(ax)} {n(ay)}C{n(ax + 14 - i * 6)} {n(ay - rise)} {n(hx + 44 + i * 8)} {n(hy - rise - 34)} {n(hx)} {n(hy)}"
        a.open(cls=f"a2l-z{i}")
        a.path(d, stroke=colors[i], sw=1.4, cap="round", cls=f"a2l-t{i}")
        a.close()

    # Mismo truco que los tubos: el extremo del travesaño queda fijo.
    ca = a.p(452, 300, 505)
    ch = a.p(tcx + 15, tcy + 5, zr + 60)
    dx = ch[0] - ca[0]
    s0, s1 = 1 + hx0[0] / dx, 1 + hx1[0] / dx
    t0 = math.degrees(math.atan(hx0[1] / (s0 * dx)))
    t1 = math.degrees(math.atan(hx1[1] / (s1 * dx)))
    k = a.keyframes("tc", 1, [(0, f"transform:skewY({t0:.3f}deg) scaleX({s0:.4f})"), (1, f"transform:skewY({t1:.3f}deg) scaleX({s1:.4f})")])
    a.css.append(f".a2l-tc{{animation:{k} {A2L_XS}s cubic-bezier(.45,.05,.55,.95) infinite alternate;animation-play-state:var(--play,running);transform-origin:{ca[0]:.1f}px {ca[1]:.1f}px}}")
    zu, zd = math.degrees(math.atan(dzu / dx)), math.degrees(math.atan(dzd / dx))
    k = a.keyframes("zc", T, [(0, f"transform:skewY({zu:.3f}deg)"), (t_print, f"transform:skewY({zd:.3f}deg)"), (t_fade1, f"transform:skewY({zd:.3f}deg)"), (T, f"transform:skewY({zu:.3f}deg)")])
    a.css.append(f".a2l-zc{{animation:{k} {T}s linear infinite;animation-play-state:var(--play,running);transform-origin:{ca[0]:.1f}px {ca[1]:.1f}px}}")
    a.open(cls="a2l-zc")
    d = f"M{n(ca[0])} {n(ca[1])}C{n(ca[0] - 14)} {n(ca[1] - 40)} {n(ch[0] + 46)} {n(ch[1] - 90)} {n(ch[0])} {n(ch[1])}"
    a.path(d, stroke="#1c1713", sw=2, cap="round", cls="a2l-tc")
    a.close()

    return a.write()


if __name__ == "__main__":
    print("h2c", h2c())
    print("h3c", h3c())
    print("a2l", a2l())
