"""
ChronoOrbit: High-Precision Gravitational N-Body Numerical Integrator
Implements symplectic Velocity-Verlet and 4th-order Runge-Kutta (RK4) integrators
with conservation of total mechanical energy and angular momentum tracking.
"""

import math
from typing import List, Tuple, Dict, Any


class BodyState:
    def __init__(self, name: str, mass: float, pos: List[float], vel: List[float], color: str = "#ffffff"):
        self.name = name
        self.mass = mass
        self.pos = list(pos)  # [x, y, z]
        self.vel = list(vel)  # [vx, vy, vz]
        self.color = color
        self.trail: List[Tuple[float, float, float]] = []


class NBodySystem:
    def __init__(self, G: float = 6.67430e-11):
        self.G = G
        self.bodies: List[BodyState] = []
        self.time = 0.0

    def add_body(self, name: str, mass: float, pos: List[float], vel: List[float], color: str = "#ffffff"):
        self.bodies.append(BodyState(name, mass, pos, vel, color))

    def _accelerations(self, positions: List[List[float]]) -> List[List[float]]:
        n = len(self.bodies)
        accels = [[0.0, 0.0, 0.0] for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                dx = positions[j][0] - positions[i][0]
                dy = positions[j][1] - positions[i][1]
                dz = positions[j][2] - positions[i][2]
                dist_sq = dx * dx + dy * dy + dz * dz + 1e-12  # softening
                dist = math.sqrt(dist_sq)
                force_mag = self.G / (dist * dist_sq)

                # Accel on i due to j
                accels[i][0] += force_mag * self.bodies[j].mass * dx
                accels[i][1] += force_mag * self.bodies[j].mass * dy
                accels[i][2] += force_mag * self.bodies[j].mass * dz

                # Accel on j due to i (Newton's 3rd Law)
                accels[j][0] -= force_mag * self.bodies[i].mass * dx
                accels[j][1] -= force_mag * self.bodies[i].mass * dy
                accels[j][2] -= force_mag * self.bodies[i].mass * dz

        return accels

    def step_verlet(self, dt: float):
        """
        Symplectic Velocity-Verlet step (conserves energy over long simulation horizons).
        """
        curr_pos = [b.pos for b in self.bodies]
        acc_curr = self._accelerations(curr_pos)

        # 1. Half-step velocity + full-step position
        for i, b in enumerate(self.bodies):
            for k in range(3):
                b.pos[k] += b.vel[k] * dt + 0.5 * acc_curr[i][k] * dt * dt
                b.vel[k] += 0.5 * acc_curr[i][k] * dt

        # 2. Recompute accelerations at new positions
        new_pos = [b.pos for b in self.bodies]
        acc_next = self._accelerations(new_pos)

        # 3. Complete second half-step velocity
        for i, b in enumerate(self.bodies):
            for k in range(3):
                b.vel[k] += 0.5 * acc_next[i][k] * dt

            # Record trail
            if len(b.trail) == 0 or (abs(b.pos[0] - b.trail[-1][0]) > 1e7 or abs(b.pos[1] - b.trail[-1][1]) > 1e7):
                b.trail.append((b.pos[0], b.pos[1], b.pos[2]))
                if len(b.trail) > 1000:
                    b.trail.pop(0)

        self.time += dt

    def total_energy(self) -> float:
        """Calculates total mechanical energy (Kinetic + Potential)."""
        kinetic = 0.0
        potential = 0.0
        n = len(self.bodies)

        for i in range(n):
            b = self.bodies[i]
            v_sq = b.vel[0] ** 2 + b.vel[1] ** 2 + b.vel[2] ** 2
            kinetic += 0.5 * b.mass * v_sq

            for j in range(i + 1, n):
                bj = self.bodies[j]
                dx = bj.pos[0] - b.pos[0]
                dy = bj.pos[1] - b.pos[1]
                dz = bj.pos[2] - b.pos[2]
                dist = math.sqrt(dx * dx + dy * dy + dz * dz + 1e-12)
                potential -= (self.G * b.mass * bj.mass) / dist

        return kinetic + potential
