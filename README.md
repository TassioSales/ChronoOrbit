# 🛰️ ChronoOrbit

> **High-Precision Astrodynamics, Orbital Mechanics & Interplanetary Trajectory Simulator**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)]()
[![Tests: Passing](https://img.shields.io/badge/Tests-9%2F9%20Passing-success.svg)]()
[![Engine: Symplectic](https://img.shields.io/badge/Integrator-Velocity--Verlet-purple.svg)]()

```
          .                                            .
                  *   .                  .              .        .   *
  .       *               .     _..._         *                 .
                           .-'     '-.                 .
                         .'           '.
                        /   SUN (Sol)   \       *             .
                       |      ☉          |
                        \               /                 *
     *                   '.           .'
           .               '-._   _.-'          .                    *
                               '''        .
           (Earth) ⊕  ----------> [Hohmann Ellipse] ----------> ♂ (Mars)
```

ChronoOrbit is an open-source Python engine and interactive visual simulator for calculating real orbital trajectories, delta-v ($\Delta v$) budgets, planetary gravity assists (slingshots), and equilibrium Lagrange points across the Solar System.

---

## 🌟 Key Features

* **Hohmann Transfer Trajectories:** Calculates exact two-impulse coplanar transfers, delta-v burns ($\Delta v_1$, $\Delta v_2$), transfer times, and synodic launch windows.
* **Planetary Slingshots (Gravity Assist):** Computes hyperbolic flyby geometries, deflection angles ($\delta$), periapsis velocities, and asymptotic excess speeds ($v_\infty$) around Jupiter, Venus, and Earth.
* **Lagrange Equilibrium Points (L1 – L5):** Analytical locations and Hill sphere radius determinations for Sun-Earth and Earth-Moon systems.
* **Symplectic N-Body Gravity Integrator:** Implements Velocity-Verlet and 4th-Order Runge-Kutta numerical integration conserving total mechanical energy ($\Delta E / E_0 < 10^{-4}$).
* **Real-Time Interactive HUD:** Visualizes orbital tracks, probe trajectories, and telemetry HUD on an interactive canvas.

---

## 🚀 Quick Start

### 1. Installation
Clone the repository:
```bash
git clone https://github.com/TassioSales/ChronoOrbit.git
cd ChronoOrbit
```
No external heavy dependencies required (pure standard Python library)!

---

## 💻 CLI Commands

### 🪐 Hohmann Transfer (e.g. Earth to Mars)
Calculate the exact delta-v budget and flight duration:
```bash
python main.py hohmann --origin Earth --target Mars
```
**Output:**
```text
=================================================================
 🚀 ChronoOrbit • Hohmann Interplanetary Transfer Calculator
=================================================================
Origin:             Earth (1.000 AU)
Target:             Mars (1.524 AU)
Transfer Semi-Axis: 1.262 AU
-----------------------------------------------------------------
Initial Burn (Δv1): 2.945 km/s  (10,601 km/h)
Arrival Burn (Δv2): 2.649 km/s  (9,536 km/h)
Total Delta-V:      5.594 km/s  (20,137 km/h)
-----------------------------------------------------------------
Transfer Duration:  258.9 Earth days (8.5 months)
Synodic Window:     Every 779.9 days (2.14 years)
=================================================================
```

---

### 🛰️ Voyager Gravity Assist (e.g. Jupiter Slingshot)
Simulate hyperbolic flyby velocity gain:
```bash
python main.py slingshot --planet Jupiter --v_inf 12.5 --altitude 500000
```
**Output:**
```text
=================================================================
 🪐 ChronoOrbit • Planetary Gravity Assist / Slingshot Simulator
=================================================================
Target Body:        Jupiter
Approach Speed:     12.50 km/s (Hyperbolic Excess v_inf)
Closest Altitude:   500,000 km above surface
-----------------------------------------------------------------
Flyby Eccentricity: 1.7029
Deflection Angle:   71.92°
Max Speed Boost:    +14.681 km/s (+52,851 km/h)
Periapsis Velocity: 24.51 km/s
=================================================================
```

---

### ⚖️ Lagrange Points (Sun-Earth & Earth-Moon)
Find gravitational equilibrium positions:
```bash
python main.py lagrange --system Sun-Earth
```

---

### 🌍 Launch Interactive Visual Simulator
Launch the real-time space telemetry canvas dashboard:
```bash
python main.py web --port 8700
```
Opens an interactive dark-space HUD in your default browser at `http://localhost:8700/index.html`.

---

## 🧪 Running the Test Suite
```bash
python tests/test_chrono_orbit.py
```
Validates Keplerian equations, energy conservation, Vis-viva formula, and NASA ephemeris comparisons.

---

## 📜 Mathematical Foundations

* **Vis-Viva Equation:**
  $$v = \sqrt{\mu \left( \frac{2}{r} - \frac{1}{a} \right)}$$

* **Hohmann Transfer Delta-V:**
  $$\Delta v_1 = \sqrt{\frac{\mu}{r_1}} \left( \sqrt{\frac{2 r_2}{r_1 + r_2}} - 1 \right)$$
  $$\Delta v_2 = \sqrt{\frac{\mu}{r_2}} \left( 1 - \sqrt{\frac{2 r_1}{r_1 + r_2}} \right)$$

* **Hyperbolic Deflection Angle:**
  $$\sin\left(\frac{\delta}{2}\right) = \frac{1}{e} = \frac{1}{1 + \frac{r_p v_\infty^2}{\mu}}$$

---

## 📄 License
MIT License © 2026 Tássio Sales.
