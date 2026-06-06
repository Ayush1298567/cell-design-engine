"""Shared physics constants. Single source of truth (CLAUDE.md hygiene).

Imported by the simulator and the validation/convergence scripts so the converged
mesh, the discharge cutoff, and the ambient temperature cannot drift between files.
"""

# Converged spatial/particle mesh (see scripts/convergence_dfn.py: 32 pts/domain is
# within ~3.7 mV of the asymptotic solution, far below the physics error budget).
CONVERGED_MESH = {"x_n": 32, "x_s": 32, "x_p": 32, "r_n": 32, "r_p": 32}

DISCHARGE_CUTOFF_V = 2.5   # lower voltage cutoff for discharge experiments
AMBIENT_K = 298.15         # 25 C, used as both ambient and initial temperature
