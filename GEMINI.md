# GEOMETOR • `polyhedra`

Exact symbolic Platonic, Archimedean, and Keplerian polyhedral geometry, Golden Ratio ($\phi$) proportions, Leonardo da Vinci *Corpora Vacua*, and multi-engine 3D exports in [SymPy](https://www.sympy.org/).

---

## 1. Purpose & Guiding Principles

`geometor-polyhedra` (`v0.2.0`) provides the 3D symbolic modeling kernel, polyhedral operator algebra, Golden Ratio theorem suite, and multi-engine visualization pipeline for the GEOMETOR ecosystem:

- **100% Exact Symbolic Precision**: All vertices, face normals, edge midpoints, face centroids, sphere quadrances, Conway/Leonardo operators, and 2D cross-sections are modeled symbolically over $\mathbb{Z}$, $\mathbb{Q}(\phi)$ ($\phi = \frac{1+\sqrt{5}}{2}$), and closed-form radical extensions. Zero `float` or `sp.Float` approximations in symbolic geometry (`.evalf()` is confined strictly to `render/` projection/export layers and cyclic sorting).
- **Euclidean & Scriptorium Lineage**: Direct alignment with Euclid's *Elements* Book XIII (`G.592`–`G.600`), Plato's *Timaeus*, Luca Pacioli's *De Divina Proportione* (1509 woodcuts by Leonardo da Vinci), and Johannes Kepler's *Strena* (1611) and *Harmonices Mundi* (1619).
- **Rational Trigonometry Invariants**: Pure rational dihedral spreads across all five regular solids:
  - Tetrahedron $\{3,3\}$: $s = 8/9$
  - Hexahedron $\{4,3\}$: $s = 1$
  - Octahedron $\{3,4\}$: $s = 8/9$
  - Icosahedron $\{3,5\}$: $s = 4/9$
  - Dodecahedron $\{5,3\}$: $s = 4/5$

---

## 2. Package Architecture (`src/geometor/polyhedra/`)

- [`__init__.py`](src/geometor/polyhedra/__init__.py): Public exports and `__version__ = "0.2.0"`.
- [`platonic.py`](src/geometor/polyhedra/platonic.py): Exact symbolic seed kernel (`RegularSolid`, `PHI`, `PHI_INV`, all 5 regular solids, Leonardo plate concordance, and 3D Rational Trigonometry helpers).
- [`model3d/`](src/geometor/polyhedra/model3d/):
  - [`primitives.py`](src/geometor/polyhedra/model3d/primitives.py): Exact zero-float `Vector3D`, `Point3D`, `Line3D`, `Plane3D`, `Sphere3D`, and `Solid3D`.
  - [`bridge.py`](src/geometor/polyhedra/model3d/bridge.py): Dimensional bridge `slice_solid_to_model` ($\text{3D} \to \text{2D}$ `geometor.model.Model`) and `unfold_net_2d` (non-overlapping spanning-tree 2D nets).
- [`operators.py`](src/geometor/polyhedra/operators.py): Exact symbolic `Solid3D -> Solid3D` operators: `vacuate` (Leonardo's hollow *Corpora Vacua*, genus $g = F - 1$), `rectify` (*Abscisum*), `truncate`, `elevate` (*Elevatum*), and `polar_dual`.
- [`golden.py`](src/geometor/polyhedra/golden.py): Six certified Golden Polyhedra theorems (`GoldenPolyhedronTheorem`) and builders (`build_icosahedron_golden_rectangles`, `build_octahedron_golden_icosahedron`, `build_dodecahedron_five_cubes`, `build_rhombic_triacontahedron_golden`, `build_odom_tetrahedron_section_model`, `build_icosahedron_meridian_model`, `build_pentagon_cross_section_model`) integrated with `geometor.divine`.
- [`render/`](src/geometor/polyhedra/render/):
  - [`svg3d.py`](src/geometor/polyhedra/render/svg3d.py): Theme-adaptive `.euclid-graphic` SVG generators (`render_solid_svg`, `render_net_svg`, `render_model2d_svg`).
  - [`exporters.py`](src/geometor/polyhedra/render/exporters.py): Wavefront `.obj`/`.mtl` exporter plus standalone **IngeTrazo 0.6.0** and **Blender 5.x (`bpy`)** studio script generators (`demos/exports/`).
- [`cli.py`](src/geometor/polyhedra/cli.py) & [`__main__.py`](src/geometor/polyhedra/__main__.py): Rich terminal interface (`polyhedra`).

---

## 3. Book Codex (`docsrc/`)

Compiled as a self-contained `:layout: book` codex via `publish build` (zero modifications required in `photon-platform/publish`):

- [`docsrc/_static/js/polyhedra_3d_codex.js`](docsrc/_static/js/polyhedra_3d_codex.js): Zero-dependency interactive HTML5 `<canvas>` 3D viewer (`data-solid` and `data-scene` modes with live *Vacuum* aperture $\mu$ morphing, $\tau \in (0,1)$ Octahedron-to-Icosahedron edge division, and 5-Cube compound toggles).
- [`docsrc/platonic/`](docsrc/platonic/): Overview + 5 dedicated Platonic solid monographs.
- [`docsrc/golden/`](docsrc/golden/): Overview + 4 dedicated Golden Proportions monographs.
- [`docsrc/leonardo/`](docsrc/leonardo/): 38 curated 1509 Leonardo woodcuts (`Tabulae I–XXXVI`) paired side-by-side with exact symbolic reconstructions.
- [`docsrc/pipeline/`](docsrc/pipeline/): 3D symbolic architecture and multi-engine pipeline documentation.

---

## 4. Development & Verification Commands

All commands run offline inside the Python 3.13 GEOMETOR `uv` workspace environment:

```bash
# Lint (enforces E, F, I, ANN, and Google-convention D rules)
ruff check src tests demos

# Run test suite (43 exact symbolic & rendering tests)
/home/phi/PROJECTS/geometor/.venv/bin/python -m pytest

# Build Sphinx Book Codex into docs/
publish build
```
