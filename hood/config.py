"""Single source of truth for every hood dimension and design target.

Coordinate system (mm), origin at the front-bottom-left corner:
    X  0..WIDTH   left  -> right   (filter-face width, 2040 rails)
    Y  0..DEPTH   front -> back    (airflow depth, 2020 rails)
    Z  0..HEIGHT  bottom -> top    (height, 2040 posts)

Y = 0 is the open front where you work; Y = DEPTH is the back wall. Air is
blown from the plenum through the HEPA filter and exits toward the front
(the -Y direction), giving a horizontal-flow clean bench.

The whole filter/plenum/blower stack hangs off the BACK of the frame so the
entire interior (0..DEPTH) is usable work space. Layout along Y, front->back:
    [ open work zone ] | back wall | [ HEPA filter ][ plenum ][ blower ][ pre-filter ]
                     Y=0..DEPTH        DEPTH ->  (everything past DEPTH sticks out)
"""

from __future__ import annotations

# --- Extrusion profiles (mm) ---------------------------------------------
PROFILE = 20.0        # 2020 face width (also the short side of a 2040)
PROFILE_LONG = 40.0   # 2040 long side (two 2020s ganged)

# --- Outer envelope (mm), from the real bill of materials ----------------
#   4x 2040 @ 550 -> X (width)   4x 2040 @ 460 -> Z (posts)
#   4x 2020 @ 405 -> Y (depth)
WIDTH = 550.0
DEPTH = 405.0
HEIGHT = 460.0

# --- Sheet / panel stock (mm) --------------------------------------------
PANEL_THICKNESS = 3.0   # acrylic/PVC walls and plenum skins
DECK_THICKNESS = 6.0    # work-surface deck

# --- Filter + plenum geometry (mm) ---------------------------------------
FILTER_THICKNESS = 70.0   # depth of the HEPA panel
PLENUM_GAP = 40.0         # sealed air gap between blower and filter back

# --- Blower placeholder (mm) ---------------------------------------------
BLOWER_SIZE = 150.0       # square housing face (X and Z)
BLOWER_DEPTH = 90.0       # scroll-housing depth along Y
BLOWER_INLET_R = 45.0     # intake throat radius
BLOWER_INLET_LEN = 25.0   # intake throat length

# --- Pre-filter (mm) -----------------------------------------------------
# Coarse pad on the blower intake; catches lint/dust so the HEPA lasts.
PREFILTER_THICKNESS = 20.0
PREFILTER_SIZE = 170.0    # square pad face (covers the intake)

# --- Laminar-flow design targets -----------------------------------------
FACE_VELOCITY = 0.45      # m/s, ISO/clean-bench target (accept 0.30-0.50)
AIR_VISCOSITY = 1.5e-5    # m^2/s, kinematic viscosity of air at ~20 C


# --- Derived geometry (do not edit; computed from the above) -------------
# Clear opening on the filter face: the 2040 perimeter eats PROFILE_LONG
# off every edge.
OPENING_W = WIDTH - 2 * PROFILE_LONG      # 470
OPENING_H = HEIGHT - 2 * PROFILE_LONG     # 380
OPENING_X0 = PROFILE_LONG                 # 40
OPENING_X1 = WIDTH - PROFILE_LONG         # 510
OPENING_Z0 = PROFILE_LONG                 # 40
OPENING_Z1 = HEIGHT - PROFILE_LONG        # 420

# Y positions of the stack, which hangs off the back wall (Y = DEPTH).
# The filter's front face is flush with the frame back, so the full interior
# depth is work space and everything from the filter onward sticks out.
WORK_ZONE_DEPTH = DEPTH                                 # 405 (full interior)
FILTER_FRONT_Y = DEPTH                                  # 405 (flush w/ back)
FILTER_BACK_Y = FILTER_FRONT_Y + FILTER_THICKNESS       # 475
PLENUM_BACK_Y = FILTER_BACK_Y + PLENUM_GAP              # 515
BLOWER_BACK_Y = PLENUM_BACK_Y + BLOWER_DEPTH            # 605
PREFILTER_FRONT_Y = BLOWER_BACK_Y + BLOWER_INLET_LEN    # 630
PREFILTER_BACK_Y = PREFILTER_FRONT_Y + PREFILTER_THICKNESS  # 650
