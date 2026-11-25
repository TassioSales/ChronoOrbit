"""
ChronoOrbit: Keplerian Mechanics & Two-Body Orbital Dynamics
Formulas implement Vis-Viva equation, Kepler's equation solver via Newton-Raphson,
and Cartesian State Vector <-> Orbital Elements conversions.
"""

import math
from typing import Tuple, Dict, Any


def vis_viva(r: float, a: float, mu: float) -> float:
    """
    Computes orbital velocity using Vis-Viva equation:
    v = sqrt(mu * (2/r - 1/a))
    """
    if r <= 0:
        raise ValueError("Orbital radius r must be positive.")
    term = 2.0 / r - 1.0 / a
    if term < 0:
        raise ValueError("Parabolic/hyperbolic condition invalid for bound orbit.")
    return math.sqrt(mu * term)


def orbital_period(a: float, mu: float) -> float:
    """
    Computes Keplerian orbital period:
    T = 2 * pi * sqrt(a^3 / mu)
    """
    if a <= 0:
        raise ValueError("Semi-major axis must be positive.")
    return 2.0 * math.pi * math.sqrt((a ** 3) / mu)


def solve_kepler(M: float, e: float, tolerance: float = 1e-12, max_iter: int = 100) -> float:
    """
    Solves Kepler's Equation: M = E - e * sin(E) for Eccentric Anomaly E
    using iterative Newton-Raphson method.
    """
    # Initial estimate
    E = M if e < 0.8 else math.pi
    for _ in range(max_iter):
        f = E - e * math.sin(E) - M
        f_prime = 1.0 - e * math.cos(E)
        delta = f / f_prime
        E -= delta
        if abs(delta) < tolerance:
            return E
    return E


def true_anomaly_from_eccentric(E: float, e: float) -> float:
    """
    Converts Eccentric Anomaly E to True Anomaly nu (radians).
    tan(nu / 2) = sqrt((1 + e) / (1 - e)) * tan(E / 2)
    """
    factor = math.sqrt((1.0 + e) / (1.0 - e))
    return 2.0 * math.atan2(factor * math.sin(E / 2.0), math.cos(E / 2.0))


def elements_to_cartesian(
    a: float,
    e: float,
    i: float,
    omega_node: float,
    arg_periapsis: float,
    true_anomaly: float,
    mu: float
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """
    Converts 6 Keplerian elements into Cartesian State Vectors (r_vec, v_vec).
    Inputs:
        a: semi-major axis (m)
        e: eccentricity (0 <= e < 1)
        i: inclination (rad)
        omega_node: longitude of ascending node (rad)
        arg_periapsis: argument of periapsis (rad)
        true_anomaly: true anomaly nu (rad)
        mu: standard gravitational parameter (m^3/s^2)
    Returns:
        ((rx, ry, rz), (vx, vy, vz)) in meters and meters/sec.
    """
    p = a * (1.0 - e ** 2)
    r = p / (1.0 + e * math.cos(true_anomaly))

    # Position in orbital plane (perifocal frame)
    rx_p = r * math.cos(true_anomaly)
    ry_p = r * math.sin(true_anomaly)
    rz_p = 0.0

    # Velocity in perifocal frame
    h = math.sqrt(mu * p)
    vx_p = - (mu / h) * math.sin(true_anomaly)
    vy_p = (mu / h) * (e + math.cos(true_anomaly))
    vz_p = 0.0

    # Rotation matrix from perifocal to inertial equatorial coordinates
    cos_O, sin_O = math.cos(omega_node), math.sin(omega_node)
    cos_w, sin_w = math.cos(arg_periapsis), math.sin(arg_periapsis)
    cos_i, sin_i = math.cos(i), math.sin(i)

    # Direction cosine matrix elements
    P11 = cos_O * cos_w - sin_O * sin_w * cos_i
    P12 = -cos_O * sin_w - sin_O * cos_w * cos_i
    P21 = sin_O * cos_w + cos_O * sin_w * cos_i
    P22 = -sin_O * sin_w + cos_O * cos_w * cos_i
    P31 = sin_w * sin_i
    P32 = cos_w * sin_i

    # Inertial Cartesian Position
    x = P11 * rx_p + P12 * ry_p
    y = P21 * rx_p + P22 * ry_p
    z = P31 * rx_p + P32 * ry_p

    # Inertial Cartesian Velocity
    vx = P11 * vx_p + P12 * vy_p
    vy = P21 * vx_p + P22 * vy_p
    vz = P31 * vx_p + P32 * vy_p

    return ((x, y, z), (vx, vy, vz))


def specific_orbital_energy(r: float, v: float, mu: float) -> float:
    """
    Computes specific mechanical orbital energy (epsilon in J/kg):
    epsilon = (v^2 / 2) - (mu / r) = - mu / (2 * a)
    """
    return (v ** 2) / 2.0 - (mu / r)
