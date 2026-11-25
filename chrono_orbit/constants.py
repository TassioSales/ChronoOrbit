"""
ChronoOrbit: Astronomical Constants & Solar System Gravitational Parameters
Data sourced from NASA JPL Horizon Ephemerides & IAU standards.
"""

import math

# Universal Gravitational Constant (m^3 kg^-1 s^-2)
G = 6.67430e-11

# Astronomical Unit (meters)
AU = 149597870700.0

# Speed of Light in vacuum (m/s)
C_LIGHT = 299792458.0

# Standard Gravitational Parameters (mu = G * M in m^3 / s^2)
MU_SUN = 1.32712440018e20
MU_MERCURY = 2.2032e13
MU_VENUS = 3.24859e14
MU_EARTH = 3.986004418e14
MU_MOON = 4.9048695e12
MU_MARS = 4.282837e13
MU_JUPITER = 1.26686534e17
MU_SATURN = 3.7931187e16

# Planetary Mean Radii (meters)
RADIUS_SUN = 6.9634e8
RADIUS_EARTH = 6.378137e6
RADIUS_MOON = 1.7374e6
RADIUS_MARS = 3.3895e6
RADIUS_JUPITER = 6.9911e7

# Semi-Major Axes of Orbits around Sun (meters)
ORBIT_MERCURY_A = 0.387098 * AU
ORBIT_VENUS_A = 0.723332 * AU
ORBIT_EARTH_A = 1.000000 * AU
ORBIT_MARS_A = 1.523679 * AU
ORBIT_JUPITER_A = 5.2044 * AU
ORBIT_SATURN_A = 9.5826 * AU

# Standard Celestial Bodies Dictionary
BODIES = {
    "sun": {
        "name": "Sun",
        "mu": MU_SUN,
        "radius": RADIUS_SUN,
        "color": "#ffcc00",
        "mass": 1.98847e30
    },
    "earth": {
        "name": "Earth",
        "mu": MU_EARTH,
        "radius": RADIUS_EARTH,
        "a": ORBIT_EARTH_A,
        "e": 0.0167,
        "period": 365.256 * 86400,
        "color": "#3399ff",
        "mass": 5.9722e24
    },
    "moon": {
        "name": "Moon",
        "mu": MU_MOON,
        "radius": RADIUS_MOON,
        "a": 384400000.0,
        "e": 0.0549,
        "period": 27.3216 * 86400,
        "color": "#cccccc",
        "mass": 7.342e22
    },
    "mars": {
        "name": "Mars",
        "mu": MU_MARS,
        "radius": RADIUS_MARS,
        "a": ORBIT_MARS_A,
        "e": 0.0934,
        "period": 686.980 * 86400,
        "color": "#ff5533",
        "mass": 6.4171e23
    },
    "jupiter": {
        "name": "Jupiter",
        "mu": MU_JUPITER,
        "radius": RADIUS_JUPITER,
        "a": ORBIT_JUPITER_A,
        "e": 0.0489,
        "period": 4332.59 * 86400,
        "color": "#e0a96d",
        "mass": 1.89813e27
    }
}
