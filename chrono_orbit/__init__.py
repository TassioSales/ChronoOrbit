"""
ChronoOrbit: Open-Source Astrodynamics & Orbital Mechanics Engine
"""

from .constants import G, AU, BODIES, MU_SUN, MU_EARTH, MU_MARS, MU_JUPITER, MU_MOON
from .kepler import vis_viva, orbital_period, elements_to_cartesian, specific_orbital_energy
from .maneuvers import hohmann_transfer, gravity_assist, lagrange_points, synodic_period
from .nbody import NBodySystem

__version__ = "1.0.0"
__all__ = [
    "G", "AU", "BODIES", "MU_SUN", "MU_EARTH", "MU_MARS", "MU_JUPITER", "MU_MOON",
    "vis_viva", "orbital_period", "elements_to_cartesian", "specific_orbital_energy",
    "hohmann_transfer", "gravity_assist", "lagrange_points", "synodic_period",
    "NBodySystem"
]
