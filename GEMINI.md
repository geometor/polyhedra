# GEOMETOR • `polyhedra`

Exact symbolic Platonic, Archimedean, and Keplerian polyhedral geometry in [SymPy](https://www.sympy.org/) and the GEOMETOR Digital Scriptorium.

---

## 1. Purpose & Guiding Principles

`geometor-polyhedra` (`v0.1.0`) provides the foundational 3D polyhedral models and rational invariants for the GEOMETOR ecosystem:

- **100% Exact Symbolic Precision**: All vertices, face normals, edge midpoints, face centroids, and sphere quadrances are modeled symbolically over $\mathbb{Z}$ and $\mathbb{Q}(\phi)$ ($\phi = \frac{1+\sqrt{5}}{2}$). Zero `float` or `sp.Float` approximations.
- **Euclidean & Scriptorium Lineage**: Direct alignment with Euclid's *Elements* Book XIII (props XIII.13–XIII.18), Plato's *Timaeus*, Luca Pacioli's *De Divina Proportione* (1509 woodcuts by Leonardo da Vinci), and Johannes Kepler's *Harmonices Mundi* (1619).
- **Rational Trigonometry Invariants**: Quantifying dihedral angles via rational spreads:
  - Tetrahedron: $s = 8/9$
  - Hexahedron: $s = 1$
  - Octahedron: $s = 8/9$
  - Dodecahedron: $s = 4/5$
  - Icosahedron: $s = 4/9$

---

## 2. Package Architecture (`src/geometor/polyhedra/`)

- [`__init__.py`](src/geometor/polyhedra/__init__.py): Public exports and `__version__ = "0.1.0"`.
- [`platonic.py`](src/geometor/polyhedra/platonic.py): Exact symbolic seed kernel, frozen dataclass `RegularSolid`, all 5 regular solids, and 3D Rational Trigonometry vector helpers (`quadrance_3d`, `cross_3d`, `dot_3d`, `face_normal_3d`, `dihedral_spread_3d`, `get_platonic_solids`, `get_platonic_solid`).
- [`cli.py`](src/geometor/polyhedra/cli.py): Rich terminal interface and table formatter.
- [`__main__.py`](src/geometor/polyhedra/__main__.py): Entrypoint for `polyhedra` CLI.

---

## 3. Development & Verification Commands

All commands run on Python 3.13 via the GEOMETOR `uv` workspace environment:

```bash
# Lint (enforces E, F, I, ANN, and Google-convention D rules)
ruff check src tests demos

# Run test suite
/home/phi/PROJECTS/geometor/.venv/bin/python -m pytest

# Build Sphinx Book Codex
publish build
```
