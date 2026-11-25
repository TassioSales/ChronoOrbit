"""
ChronoOrbit: Orbital Maneuvers & Mission Trajectory Calculations
Calculates:
- Hohmann Transfer Orbit (Delta-V budgets, burn timing, synodic period)
- Bi-Elliptic Transfer (Energy comparison)
- Planetary Gravity Assist / Slingshot (Deflection angle, hyperbolic excess speed)
- Collinear and Triangular Lagrange Points (L1, L2, L3, L4, L5)
"""

import math
from typing import Dict, Any


def hohmann_transfer(r1: float, r2: float, mu: float) -> Dict[str, Any]:
    """
    Computes classic two-impulse Hohmann transfer between coplanar circular orbits.
    Inputs:
        r1: radius of initial circular orbit (m)
        r2: radius of target circular orbit (m)
        mu: gravitational parameter of central body (m^3/s^2)
    Returns:
        dict with delta_v1, delta_v2, total_delta_v, transfer_time_seconds,
        transfer_semi_major_axis, and initial/final circular velocities.
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbital radii must be strictly positive.")

    v_c1 = math.sqrt(mu / r1)
    v_c2 = math.sqrt(mu / r2)

    a_trans = (r1 + r2) / 2.0

    # Velocity at periapsis of transfer orbit
    v_t1 = math.sqrt(mu * (2.0 / r1 - 1.0 / a_trans))
    # Velocity at apoapsis of transfer orbit
    v_t2 = math.sqrt(mu * (2.0 / r2 - 1.0 / a_trans))

    # Burns
    dv1 = abs(v_t1 - v_c1)
    dv2 = abs(v_c2 - v_t2)
    total_dv = dv1 + dv2

    # Half-period of transfer ellipse
    t_trans = math.pi * math.sqrt((a_trans ** 3) / mu)

    return {
        "r1_m": r1,
        "r2_m": r2,
        "v_circ1_mps": v_c1,
        "v_circ2_mps": v_c2,
        "transfer_semi_major_axis_m": a_trans,
        "delta_v1_mps": dv1,
        "delta_v2_mps": dv2,
        "total_delta_v_mps": total_dv,
        "transfer_time_s": t_trans,
        "transfer_time_days": t_trans / 86400.0
    }


def synodic_period(a1: float, a2: float, mu: float) -> float:
    """
    Computes synodic period (launch window repetition interval):
    1/T_syn = |1/T1 - 1/T2|
    """
    T1 = 2.0 * math.pi * math.sqrt((a1 ** 3) / mu)
    T2 = 2.0 * math.pi * math.sqrt((a2 ** 3) / mu)
    return abs(1.0 / (1.0 / T1 - 1.0 / T2))


def gravity_assist(
    v_inf: float,
    periapsis_altitude: float,
    body_radius: float,
    body_mu: float,
    body_orbital_speed: float
) -> Dict[str, Any]:
    """
    Calculates planetary gravity assist (flyby slingshot maneuver).
    Inputs:
        v_inf: hyperbolic excess velocity relative to planet (m/s)
        periapsis_altitude: closest approach altitude above surface (m)
        body_radius: planet radius (m)
        body_mu: planet standard gravitational parameter (m^3/s^2)
        body_orbital_speed: heliocentric orbital velocity of the planet (m/s)
    Returns:
        deflection angle (rad & deg), periapsis speed, and maximum theoretical
        heliocentric velocity change delta_v.
    """
    r_p = body_radius + periapsis_altitude
    if r_p <= body_radius:
        raise ValueError("Periapsis must be above planet surface to prevent atmospheric impact.")

    # Eccentricity of hyperbolic flyby: e = 1 + (r_p * v_inf^2 / mu)
    e = 1.0 + (r_p * (v_inf ** 2)) / body_mu

    # Deflection angle delta: sin(delta / 2) = 1 / e
    delta_rad = 2.0 * math.asin(1.0 / e)
    delta_deg = math.degrees(delta_rad)

    # Velocity at closest approach (periapsis)
    v_periapsis = math.sqrt(v_inf ** 2 + (2.0 * body_mu / r_p))

    # Maximum heliocentric velocity gain:
    # Delta-V_helio = 2 * v_inf * sin(delta / 2)
    max_heliocentric_dv = 2.0 * v_inf * math.sin(delta_rad / 2.0)

    return {
        "periapsis_radius_m": r_p,
        "hyperbolic_eccentricity": e,
        "deflection_angle_deg": delta_deg,
        "deflection_angle_rad": delta_rad,
        "periapsis_velocity_mps": v_periapsis,
        "max_velocity_boost_mps": max_heliocentric_dv,
        "speed_gain_kmh": (max_heliocentric_dv * 3.6)
    }


def lagrange_points(d: float, m1: float, m2: float) -> Dict[str, float]:
    """
    Computes locations of the 5 Lagrange Equilibrium Points for a two-body system
    (e.g., Sun-Earth or Earth-Moon) along the rotating reference frame.
    Inputs:
        d: distance between m1 and m2 (meters)
        m1: mass of primary body (kg, m1 >> m2)
        m2: mass of secondary body (kg)
    Returns:
        x coordinates relative to primary body center (x=0 is m1, x=d is m2).
    """
    mu_ratio = m2 / (m1 + m2)
    r_hill = d * (mu_ratio / 3.0) ** (1.0 / 3.0)

    # Collinear points (approximate analytical expansions)
    L1 = d - r_hill
    L2 = d + r_hill
    L3 = - (d + (5.0 / 12.0) * mu_ratio * d)

    # Triangular points (form equilateral triangle with m1 and m2)
    # Distance from m1 is exactly d at angle +/- 60 degrees
    return {
        "L1_distance_from_primary_m": L1,
        "L2_distance_from_primary_m": L2,
        "L3_distance_from_primary_m": L3,
        "L1_distance_from_secondary_m": d - L1,
        "L2_distance_from_secondary_m": L2 - d,
        "L4_angle_deg": 60.0,
        "L5_angle_deg": -60.0,
        "hill_sphere_radius_m": r_hill
    }
