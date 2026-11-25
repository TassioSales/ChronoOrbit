"""
ChronoOrbit: Test Suite
Validates orbital physics, energy conservation, Keplerian element conversions,
Hohmann delta-v budgets, and Lagrange point calculations.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import math
from chrono_orbit.constants import AU, MU_SUN, MU_EARTH, RADIUS_EARTH
from chrono_orbit.kepler import vis_viva, orbital_period, solve_kepler, elements_to_cartesian, specific_orbital_energy
from chrono_orbit.maneuvers import hohmann_transfer, gravity_assist, lagrange_points, synodic_period
from chrono_orbit.nbody import NBodySystem


def test_vis_viva_earth_circular():
    # Earth orbital speed around Sun at 1 AU is ~29.78 km/s
    v = vis_viva(AU, AU, MU_SUN)
    assert 29700.0 < v < 29900.0


def test_orbital_period_earth():
    # Earth orbital period around Sun is ~365.25 days
    p_sec = orbital_period(AU, MU_SUN)
    days = p_sec / 86400.0
    assert 364.5 < days < 366.0


def test_kepler_solver_circular():
    # For circular orbit (e=0), M = E
    E = solve_kepler(math.pi / 4, 0.0)
    assert abs(E - math.pi / 4) < 1e-10


def test_kepler_solver_elliptic():
    # M = 1.0, e = 0.5 -> test M == E - e*sin(E)
    E = solve_kepler(1.0, 0.5)
    recovered_M = E - 0.5 * math.sin(E)
    assert abs(recovered_M - 1.0) < 1e-10


def test_hohmann_earth_to_mars():
    r1 = 1.0 * AU
    r2 = 1.524 * AU
    res = hohmann_transfer(r1, r2, MU_SUN)
    # NASA standard: dv1 ~ 2.94 km/s, dv2 ~ 2.65 km/s, total ~ 5.59 km/s
    assert 2900.0 < res["delta_v1_mps"] < 3000.0
    assert 2600.0 < res["delta_v2_mps"] < 2700.0
    assert 250.0 < res["transfer_time_days"] < 265.0


def test_synodic_period_earth_mars():
    # Earth-Mars synodic period is ~780 days
    T_syn = synodic_period(1.0 * AU, 1.524 * AU, MU_SUN)
    days = T_syn / 86400.0
    assert 770.0 < days < 790.0


def test_gravity_assist_deflection():
    # Deflection angle must be positive and bounded by 180 degrees
    res = gravity_assist(
        v_inf=10000.0,
        periapsis_altitude=500000000.0,
        body_radius=69911000.0,
        body_mu=1.26686534e17,
        body_orbital_speed=13000.0
    )
    assert 0.0 < res["deflection_angle_deg"] < 180.0
    assert res["max_velocity_boost_mps"] > 0.0


def test_lagrange_points_earth_sun():
    res = lagrange_points(AU, 1.98847e30, 5.9722e24)
    # L1 and L2 are ~1.5 million km from Earth
    d_l1 = res["L1_distance_from_secondary_m"] / 1000.0
    d_l2 = res["L2_distance_from_secondary_m"] / 1000.0
    assert 1400000.0 < d_l1 < 1600000.0
    assert 1400000.0 < d_l2 < 1600000.0


def test_nbody_energy_conservation():
    sys = NBodySystem()
    # Sun
    sys.add_body("Sun", 1.989e30, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    # Earth at 1 AU
    v_circ = math.sqrt(6.67430e-11 * 1.989e30 / AU)
    sys.add_body("Earth", 5.972e24, [AU, 0.0, 0.0], [0.0, v_circ, 0.0])

    initial_energy = sys.total_energy()
    dt = 3600.0 * 24.0  # 1 day steps
    for _ in range(30):
        sys.step_verlet(dt)

    final_energy = sys.total_energy()
    rel_error = abs((final_energy - initial_energy) / initial_energy)
    assert rel_error < 1e-4  # Symplectic verlet maintains high energy stability


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    print(f"Running {len(tests)} ChronoOrbit unit tests...")
    for t in tests:
        t()
        print(f"  ✓ {t.__name__}")
    print("\nAll tests passed successfully!")
