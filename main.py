"""
ChronoOrbit: Command-Line Astrodynamics Engine & Simulation Launcher
"""

import sys
import os
import argparse
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

from chrono_orbit.constants import BODIES, AU, MU_SUN, MU_EARTH, MU_MARS, MU_JUPITER, MU_MOON
from chrono_orbit.maneuvers import hohmann_transfer, gravity_assist, lagrange_points, synodic_period
from chrono_orbit.kepler import vis_viva, orbital_period


def cmd_hohmann(args):
    print("\n" + "=" * 65)
    print(" 🚀 ChronoOrbit • Hohmann Interplanetary Transfer Calculator")
    print("=" * 65)

    origin = args.origin.lower()
    target = args.target.lower()

    if origin not in BODIES or target not in BODIES:
        print(f"Error: Valid bodies are: {', '.join(BODIES.keys())}")
        return

    b1 = BODIES[origin]
    b2 = BODIES[target]

    if "a" not in b1 or "a" not in b2:
        print("Error: Both bodies must have semi-major axis (a) around the Sun.")
        return

    res = hohmann_transfer(b1["a"], b2["a"], MU_SUN)
    syn = synodic_period(b1["a"], b2["a"], MU_SUN)

    print(f"\nOrigin:             {b1['name']} ({b1['a']/AU:.3f} AU)")
    print(f"Target:             {b2['name']} ({b2['a']/AU:.3f} AU)")
    print(f"Transfer Semi-Axis: {res['transfer_semi_major_axis_m']/AU:.3f} AU")
    print("-" * 65)
    print(f"Initial Burn (Δv1): {res['delta_v1_mps']/1000.0:.3f} km/s  ({res['delta_v1_mps']*3.6:.0f} km/h)")
    print(f"Arrival Burn (Δv2): {res['delta_v2_mps']/1000.0:.3f} km/s  ({res['delta_v2_mps']*3.6:.0f} km/h)")
    print(f"Total Delta-V:      {res['total_delta_v_mps']/1000.0:.3f} km/s  ({res['total_delta_v_mps']*3.6:.0f} km/h)")
    print("-" * 65)
    print(f"Transfer Duration:  {res['transfer_time_days']:.1f} Earth days ({res['transfer_time_days']/30.437:.1f} months)")
    print(f"Synodic Window:     Every {syn/86400.0:.1f} days ({syn/(86400.0*365.25):.2f} years)")
    print("=" * 65 + "\n")


def cmd_slingshot(args):
    print("\n" + "=" * 65)
    print(" 🪐 ChronoOrbit • Planetary Gravity Assist / Slingshot Simulator")
    print("=" * 65)

    planet_name = args.planet.lower()
    if planet_name not in BODIES:
        print(f"Error: Unknown planet. Choose: {', '.join(BODIES.keys())}")
        return

    b = BODIES[planet_name]
    v_inf = args.v_inf * 1000.0  # convert km/s to m/s
    altitude = args.altitude * 1000.0  # convert km to m

    # Approximate planet orbital speed
    v_planet = vis_viva(b.get("a", AU), b.get("a", AU), MU_SUN)

    res = gravity_assist(
        v_inf=v_inf,
        periapsis_altitude=altitude,
        body_radius=b["radius"],
        body_mu=b["mu"],
        body_orbital_speed=v_planet
    )

    print(f"\nTarget Body:        {b['name']}")
    print(f"Approach Speed:     {args.v_inf:.2f} km/s (Hyperbolic Excess v_inf)")
    print(f"Closest Altitude:   {args.altitude:,.0f} km above surface")
    print("-" * 65)
    print(f"Flyby Eccentricity: {res['hyperbolic_eccentricity']:.4f}")
    print(f"Deflection Angle:   {res['deflection_angle_deg']:.2f}°")
    print(f"Max Speed Boost:    +{res['max_velocity_boost_mps']/1000.0:.3f} km/s (+{res['speed_gain_kmh']:,.0f} km/h)")
    print(f"Periapsis Velocity: {res['periapsis_velocity_mps']/1000.0:.2f} km/s")
    print("=" * 65 + "\n")


def cmd_lagrange(args):
    print("\n" + "=" * 65)
    print(" ⚖️  ChronoOrbit • Lagrange Equilibrium Points (L1 - L5)")
    print("=" * 65)

    system = args.system.lower()
    if system == "earth-moon":
        d = 384400000.0
        m1 = BODIES["earth"]["mass"]
        m2 = BODIES["moon"]["mass"]
        p1, p2 = "Earth", "Moon"
    else:  # sun-earth
        d = AU
        m1 = BODIES["sun"]["mass"]
        m2 = BODIES["earth"]["mass"]
        p1, p2 = "Sun", "Earth"

    res = lagrange_points(d, m1, m2)

    print(f"\nSystem:             {p1} - {p2}")
    print(f"Orbital Separation: {d/1000.0:,.0f} km")
    print(f"Hill Sphere Radius: {res['hill_sphere_radius_m']/1000.0:,.0f} km")
    print("-" * 65)
    print(f"L1 Location:        {res['L1_distance_from_secondary_m']/1000.0:,.0f} km inside {p2}'s orbit (toward {p1})")
    print(f"L2 Location:        {res['L2_distance_from_secondary_m']/1000.0:,.0f} km outside {p2}'s orbit (space telescope zone)")
    print(f"L3 Location:        Opposite side behind {p1} ({abs(res['L3_distance_from_primary_m'])/1000.0:,.0f} km)")
    print(f"L4 (Trojan):        +60° along orbit ahead of {p2}")
    print(f"L5 (Greek):         -60° along orbit behind {p2}")
    print("=" * 65 + "\n")


def cmd_web(args):
    port = args.port
    web_dir = os.path.join(os.path.dirname(__file__), "web")
    os.chdir(web_dir)

    server = HTTPServer(("127.0.0.1", port), SimpleHTTPRequestHandler)
    url = f"http://localhost:{port}/index.html"
    print(f"\n🌍 ChronoOrbit Dashboard running at: {url}")
    print("Press Ctrl+C to stop.\n")

    def open_browser():
        time.sleep(0.5)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


def main():
    parser = argparse.ArgumentParser(description="ChronoOrbit: Astrodynamics & Orbital Mechanics Simulator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Hohmann
    h_parser = subparsers.add_parser("hohmann", help="Calculate Hohmann transfer delta-v budget")
    h_parser.add_argument("--origin", default="Earth", help="Origin planet (default: Earth)")
    h_parser.add_argument("--target", default="Mars", help="Target planet (default: Mars)")

    # Slingshot
    s_parser = subparsers.add_parser("slingshot", help="Calculate planetary gravity assist")
    s_parser.add_argument("--planet", default="Jupiter", help="Target flyby planet (default: Jupiter)")
    s_parser.add_argument("--v_inf", type=float, default=12.5, help="Approach excess velocity in km/s (default: 12.5)")
    s_parser.add_argument("--altitude", type=float, default=500000.0, help="Periapsis altitude in km (default: 500,000)")

    # Lagrange
    l_parser = subparsers.add_parser("lagrange", help="Calculate Lagrange points")
    l_parser.add_argument("--system", default="Sun-Earth", choices=["Sun-Earth", "Earth-Moon"], help="System name")

    # Web Dashboard
    w_parser = subparsers.add_parser("web", help="Launch interactive 2D orbital canvas dashboard")
    w_parser.add_argument("--port", type=int, default=8700, help="Port to run web server on (default: 8700)")

    args = parser.parse_args()

    if args.command == "hohmann":
        cmd_hohmann(args)
    elif args.command == "slingshot":
        cmd_slingshot(args)
    elif args.command == "lagrange":
        cmd_lagrange(args)
    elif args.command == "web":
        cmd_web(args)
    else:
        # Default banner
        print("\n" + "=" * 65)
        print(" 🛰️  ChronoOrbit: Open-Source Astrodynamics Engine")
        print("=" * 65)
        print("Usage:")
        print("  python main.py hohmann --origin Earth --target Mars")
        print("  python main.py slingshot --planet Jupiter --v_inf 12.5")
        print("  python main.py lagrange --system Sun-Earth")
        print("  python main.py web --port 8700")
        print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
