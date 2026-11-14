"""GEOMETOR Polyhedra.

Exact symbolic Platonic, Archimedean, and Keplerian polyhedral geometry in
SymPy, Rational Trigonometry, and the GEOMETOR Digital Scriptorium.
"""

from __future__ import annotations

from geometor.polyhedra.platonic import (
    PHI,
    RegularSolid,
    cross_3d,
    dihedral_spread_3d,
    dot_3d,
    face_normal_3d,
    get_platonic_solid,
    get_platonic_solids,
    quadrance_3d,
)

__version__: str = "0.1.0"

__all__: list[str] = [
    "PHI",
    "RegularSolid",
    "__version__",
    "cross_3d",
    "dihedral_spread_3d",
    "dot_3d",
    "face_normal_3d",
    "get_platonic_solid",
    "get_platonic_solids",
    "quadrance_3d",
]
