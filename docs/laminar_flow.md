# Laminar Flow Hood — Design & Sizing

This document explains the airflow math behind the hood and how to size the
filter and blower for **your** frame. The numbers in the worked examples come
straight from the model — run `uv run python -m hood` to reprint the spec
sheet. The math itself lives in `hood/airflow.py`; the dimensions in
`hood/config.py`.

---

## 1. The frame you have

| Qty | Profile | Length | Role in the box            | Axis |
|-----|---------|--------|----------------------------|------|
| 4   | 2020    | 405 mm | depth rails (airflow path) | Y    |
| 4   | 2040    | 460 mm | vertical corner posts      | Z    |
| 4   | 2040    | 550 mm | width rails (filter face)  | X    |

A rectangular box has exactly **three sets of four parallel edges**, and your
inventory is exactly three sets of four — so the parts build a cuboid with no
cutting. The chosen assignment is *optimal* for two reasons:

1. **The big face carries the filter.** The `550 × 460 mm` face is the largest,
   and both of its axes are the stiff **2040** profile. The HEPA filter is the
   heaviest single part; you want it on the most rigid, best-supported face.
2. **The short axis is the airflow depth.** The `405 mm` **2020** rails become
   the front-to-back depth. A short flow path keeps the discharged air uniform,
   and the depth rails carry the least load — fine for lighter 2020.

**Assembled outer envelope: `550 (W) × 405 (D) × 460 (H) mm`.**

This is a **horizontal-flow** bench: the HEPA filter blows a sheet of clean air
horizontally toward the open front where you work.

The filter/plenum/blower stack is mounted **off the back of the frame** rather
than inside it, so the whole `405 mm` interior is usable work space (the filter
front sits flush with the back wall). Everything behind that hangs out the back:

```
   open work zone     back wall
   ┌───────────────┐╎                                    (looking down, top view)
   │               │╎ HEPA  │ plenum │ blower │ pre-filter    air ◀── ◀── into room
   │   you work    │╎ filter│  gap   │ (fan)  │   pad
   └───────────────┘╎                                    intake ──▶ ──▶ from behind
    │  405 mm (Y)  │  70 mm    40 mm    90 mm     20 mm
        interior        └──── sticks out behind frame ────┘
```

---

## 2. What "laminar" really means here

A quick honesty check, because the term is misleading. In fluid mechanics,
"laminar" means a low **Reynolds number**:

$$Re = \frac{v \, D_h}{\nu}$$

- `v` = air velocity ≈ `0.45 m/s`
- `D_h` = hydraulic diameter of the opening = `4A / P`
  For the `0.47 × 0.38 m` opening: `A = 0.179 m²`, perimeter `P = 1.70 m`,
  so `D_h = 4 × 0.179 / 1.70 ≈ 0.42 m`.
- `ν` = kinematic viscosity of air ≈ `1.5 × 10⁻⁵ m²/s` at 20 °C

$$Re = \frac{0.45 \times 0.42}{1.5\times10^{-5}} \approx 12{,}600$$

That is well into the **turbulent** range (internal flow goes turbulent above
~4000). So a "laminar flow hood" is **not** mathematically laminar.

What it actually delivers is **unidirectional, low-turbulence-intensity flow**:
every streamline points the same way at nearly the same speed. That is achieved
by two things — a **HEPA filter** (its dense media straightens and evens out the
flow as it exits) and a **sealed, pressurized plenum** behind it (so air arrives
at the whole filter face at equal pressure). Your design goals are therefore
**uniform face velocity** and **HEPA-clean air**, not a low Reynolds number.

---

## 3. Face velocity — the target

The single most important spec is the **face velocity**: how fast the clean air
leaves the filter face.

| Standard / practice        | Target face velocity          |
|----------------------------|-------------------------------|
| ISO 14644 / clean bench    | `0.45 m/s` (90 ft/min), ±20 % |
| Practical acceptable range | `0.30 – 0.50 m/s`             |

- **Too slow** (`< 0.3 m/s`): room air and your own movements disturb the flow;
  contaminants drift back into the work zone.
- **Too fast** (`> 0.5 m/s`): the sheet becomes turbulent, wastes fan power, and
  dries out / chills the work.

**Design target: `v = 0.45 m/s`.**

---

## 4. Required airflow — sizing the blower

Airflow equals velocity times the area it flows through:

$$Q = v \times A$$

`A` is the **clear filter opening**, not the outer envelope. On the back face the
2040 perimeter presents its 40 mm side inward, so each edge steals 40 mm:

- Clear width  = `550 − 2 × 40 = 470 mm`
- Clear height = `460 − 2 × 40 = 380 mm`
- `A = 0.470 × 0.380 = 0.179 m²`

Then:

$$Q = 0.45 \times 0.179 = 0.0804 \ \text{m}^3/\text{s}$$

Converting to the units fan datasheets use:

| Face velocity | Q (m³/s) | Q (m³/h) | Q (CFM) |
|---------------|----------|----------|---------|
| 0.30 m/s      | 0.054    | 193      | 114     |
| **0.45 m/s**  | **0.080**| **289**  | **170** |
| 0.50 m/s      | 0.089    | 322      | 189     |

**Design point: ~170 CFM (≈ 290 m³/h).** Size the blower for **≈ 190 CFM** so it
still hits target once the filter loads up and adds resistance (see §5).

> Conversions used: `1 m³/s = 3600 m³/h = 2118.9 CFM`.

---

## 5. Static pressure — why an axial fan won't do

`Q = v·A` tells you the *volume*, but a fan only moves that volume if it can push
against the system's **static pressure** (resistance). Almost all of the
resistance is the HEPA filter itself.

- A clean H13/H14 panel drops roughly **60 – 130 Pa** at this low face velocity
  (`0.25 – 0.5 in. w.g.`). A **loaded** filter can reach **250 Pa** or more.
- The system resistance rises with the square of flow: `ΔP ∝ Q²`.

The fan actually runs at its **operating point** — where its pressure/flow curve
crosses the system's resistance curve:

```
 ΔP │ fan curve
    │ \        system curve (∝ Q²)
    │  \      /
    │   \    /
    │    \  ●   <- operating point (your real Q)
    │     \/ \
    │     /\  \
    └───────────── Q
```

**Consequence:** a cheap axial fan (PC/box fan) makes lots of flow at ~0 Pa but
collapses to almost nothing against a HEPA filter. You want a fan that still
delivers your `Q` at the filter's `ΔP`:

- **Best:** a **centrifugal / radial ("squirrel-cage") blower** rated for
  **~190 CFM at ≥ 250 Pa (1.0 in. w.g.)**. These hold flow under back-pressure.
- **Workable:** several **high-static-pressure server/industrial 120 mm fans**
  (rated ~2–3 in. w.g. static) in **parallel** inside a sealed plenum. Ordinary
  case fans in parallel add flow but *not* pressure, so they still stall on HEPA
  — check the fan's static-pressure spec, not just its free-air CFM.

Always read the fan's CFM **at the pressure you need**, never the headline
free-air CFM.

---

## 6. The plenum (the sealed box behind the filter)

Even flow needs even pressure behind the filter. Build a **sealed plenum**
between the blower and the HEPA:

- It is a separate `~40 mm`-deep box **bolted to the back of the frame**, not
  carved out of the interior — that is what keeps the full 405 mm interior open
  as work space. Make it from sheet material (acrylic/PVC/coroplast) with the
  HEPA as its front wall, gasketed all round.
- Blow **into** the plenum, not straight at the filter — let it pressurize the
  box so air exits the whole filter face uniformly. A diffuser plate or simply
  aiming the blower off-axis helps avoid a hot jet in the middle. The shallower
  the plenum, the more a diffuser matters.
- Seal every seam. Any leak upstream of the filter is unfiltered air bypassing
  into the "clean" zone.

---

## 7. Filter selection

- **Rating:** **HEPA H13** (99.95 % @ 0.3 µm) is the practical standard; **H14**
  (99.995 %) if you want margin. "True HEPA" consumer panels are usually ~H13.
- **Size:** match the clear opening, **≈ 470 × 380 mm**. Exact HEPA panels are
  rarely off-the-shelf; common options:
  - a custom-cut **panel/box HEPA** trimmed to fit, or
  - the nearest standard panel *mounted over* the opening and sealed around the
    excess (e.g. an 18 × 16 in ≈ `457 × 406 mm` panel, gasketed to the frame).
- **Prefilter:** put a cheap MERV-7/8 or coarse foam **prefilter** on the blower
  intake. It catches lint and dust so the expensive HEPA lasts far longer.
- **Gasketing:** the filter must seal to the frame all the way around (closed-cell
  foam or a bead of RTV). An unsealed edge is a leak path — see §6.

---

## 8. Build checklist

1. Assemble the `550 × 405 × 460 mm` box (corner brackets + T-nuts on the
   2040 face, the 2020 depth rails tying front to back).
2. Panel in the **rear ~100 mm** as a sealed plenum; gasket every seam.
3. Mount the **HEPA (H13, ~470 × 380 mm)** on the plenum's front face, sealed all
   round. Add a **prefilter** on the blower intake.
4. Fit a **centrifugal blower ≈ 190 CFM @ ≥ 1 in. w.g.** blowing into the plenum.
5. **Verify** face velocity with an anemometer: sweep the filter face on a grid;
   every reading should land in **0.3 – 0.5 m/s** and be reasonably uniform.
   If it's low, you're under-powered or leaking; if it's a jet in the middle,
   improve the diffuser.
6. Optional (see `readme.md`): LED strip, internal power strip, USB, and linear
   rails / panels for the side walls to reduce cross-drafts.

---

## 9. How this maps to the model

Each physical part above is its own module, all driven by `hood/config.py`:

| Part           | Module              | Builder          |
|----------------|---------------------|------------------|
| Extrusion box  | `hood/frame.py`     | `build_frame()`  |
| HEPA filter    | `hood/filter.py`    | `build_filter()` |
| Sealed plenum  | `hood/plenum.py`    | `build_plenum()` |
| Blower         | `hood/blower.py`    | `build_blower()` |
| Intake pre-filter | `hood/prefilter.py` | `build_prefilter()` |
| Walls + deck   | `hood/panels.py`    | `build_walls()`  |
| Sizing math    | `hood/airflow.py`   | `required_airflow()`, `reynolds()` |

Change a dimension in `config.py` and every part and every number in this
doc's tables moves with it. `uv run python -m hood` rebuilds and reprints.

---

## Symbol reference

| Symbol | Meaning              | Value / unit                 |
|--------|----------------------|------------------------------|
| `v`    | face velocity        | target 0.45 m/s              |
| `A`    | clear filter opening | 0.179 m² (0.470 × 0.380 m)   |
| `Q`    | volumetric airflow   | `Q = v·A` → 170 CFM          |
| `ΔP`   | static pressure drop | HEPA ≈ 60–250 Pa             |
| `Re`   | Reynolds number      | ≈ 12,600 (turbulent — see §2)|
| `ν`    | air kinematic visc.  | 1.5 × 10⁻⁵ m²/s @ 20 °C      |
| `D_h`  | hydraulic diameter   | `4A/P` ≈ 0.42 m              |
