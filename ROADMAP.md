# Roadmap — `geometor/polyhedra`

## v0.1.0 — Initial Platonic Solids Registry & Seed Kernel (Completed)
- Exact symbolic modeling of all five Platonic solids over $\mathbb{Z}$ and $\mathbb{Q}(\phi)$.
- Rational Trigonometry 3D vector invariants (`quadrance_3d`, `cross_3d`, `dot_3d`, `face_normal_3d`, `dihedral_spread_3d`).
- Polar duality invariant proofs ($\text{Cube} = \text{Octahedron}$, $\text{Dodecahedron} = \text{Icosahedron}$, $\text{Tetrahedron}$ self-dual).
- Direct concordance with Leonardo da Vinci's polyhedral plates in Luca Pacioli's *De Divina Proportione* (1509).
- Rich CLI interface (`polyhedra`) and Sphinx Book Codex (`:layout: book`).

## v0.2.0 — `model3d` Kernel, Golden Proportions, Leonardo *Vacua* & Multi-Engine Codex (Completed)
- **Exact 3D Symbolic Kernel & 2D Bridge** (`geometor.polyhedra.model3d`): `Vector3D`, `Point3D`, `Line3D`, `Plane3D`, `Sphere3D`, `Solid3D`, `slice_solid_to_model` ($\text{3D} \to \text{2D}$ `geometor.model.Model`), and `unfold_net_2d`.
- **Conway, Pacioli & Leonardo Operators** (`geometor.polyhedra.operators`): Exact `vacuate` (Leonardo's *Corpora Vacua* hollow manifolds of genus $g = F - 1$), `rectify` (*Abscisum*), `truncate`, `elevate` (*Elevatum*), and `polar_dual`.
- **Golden Proportions in the Polyhedra** (`geometor.polyhedra.golden`): Six certified $\phi$ theorems (3 orthogonal golden rectangles in the icosahedron, $1:\phi$ octahedron-to-icosahedron edge division, Euclid XIII.17 5-cube compound in the dodecahedron, Kepler's 30-face rhombic triacontahedron, Odom's tetrahedron section, and 2D meridian/pentagonal cross-sections).
- **Multi-Backend Renderers & Interactive 3D Book Codex**: 25 `.euclid-graphic` SVGs, Wavefront `.obj`/`.mtl` export, IngeTrazo 0.6.0 & Blender 5.x script generators, 38 curated 1509 Leonardo woodcut plates, zero-dependency `polyhedra_3d_codex.js` viewer, and 15 dedicated `:layout: book` pages.

## v0.3.0 — Complete 13 Archimedean & 13 Catalan Solids Registry
- Complete registry of all 13 Archimedean solids over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \phi)$ and cubic snub extensions (including chiral Snub Cube and Snub Dodecahedron via tribonacci / golden-tribonacci constants).
- Full Catalan duals and Leonardo's remaining *De Divina Proportione* plates (`Tabulae XXXVII–LX`, including the 72-base elevated bodies and Pacioli's architectural *Mazzocchio* / columns).

## v0.4.0 — Kepler–Poinsot Regular Star Polyhedra & `publish` Native 3D Directive Promotion
- Implement the 4 regular star polyhedra ($\{5/2, 5\}$, $\{5/2, 3\}$, $\{5, 5/2\}$, $\{3, 5/2\}$) and self-intersecting stellation plane lattices from Kepler's *Harmonices Mundi* (1619) and Poinsot (1810).
- Promote `polyhedra_3d_codex.js` into a native `.. model3d::` Sphinx directive in `photon-platform/publish` and factor `geometor.polyhedra.model3d` into standalone `geometor/model3d` once downstream consumers (`kepler`, `pacioli`, `walter-russell`) converge on its API.
- Native `2560x1440` QHD slide and motion choreography for `photon-platform/studio`.
