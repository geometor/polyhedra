# Roadmap — `geometor/polyhedra`

## v0.1.0 — Initial Platonic Solids Registry & Seed Kernel (Completed)
- Exact symbolic modeling of all five Platonic solids over $\mathbb{Z}$ and $\mathbb{Q}(\phi)$.
- Rational Trigonometry 3D vector invariants (`quadrance_3d`, `cross_3d`, `dot_3d`, `face_normal_3d`, `dihedral_spread_3d`).
- Polar duality invariant proofs ($\text{Cube} = \text{Octahedron}$, $\text{Dodecahedron} = \text{Icosahedron}$, $\text{Tetrahedron}$ self-dual).
- Direct concordance with Leonardo da Vinci's 60 polyhedral plates in Luca Pacioli's *De Divina Proportione* (1509).
- Rich CLI interface (``polyhedra``) and Sphinx Book Codex (:layout: ``book``).

## v0.2.0 — Archimedean Solids & Semi-Regular Polyhedra
- Implement all 13 Archimedean solids in exact symbolic algebra over $\mathbb{Q}(\sqrt{2}, \sqrt{3}, \phi)$:
  - Truncated Tetrahedron, Cuboctahedron, Truncated Cube, Truncated Octahedron, Rhombicuboctahedron, Truncated Cuboctahedron, Snub Cube.
  - Icosidodecahedron, Truncated Dodecahedron, Truncated Icosahedron (buckyball), Rhombicosidodecahedron, Truncated Icosidodecahedron, Snub Dodecahedron.
- Kepler's Catalan duals: Rhombic Dodecahedron and Rhombic Triacontahedron.

## v0.3.0 — Kepler-Poinsot Regular Star Polyhedra & Stellations
- Implement the 4 regular star polyhedra:
  - Small Stellated Dodecahedron $\{5/2, 5\}$
  - Great Stellated Dodecahedron $\{5/2, 3\}$
  - Great Dodecahedron $\{5, 5/2\}$
  - Great Icosahedron $\{3, 5/2\}$
- Exact self-intersecting face planes and stellation lineages from Kepler's *Harmonices Mundi* (1619) and Louis Poinsot (1810).

## v0.4.0 — 3D SVG Projection & Interactive Studio Choreography
- Exact symbolic orthographic, isometric, and stereographic projections to 2D `.euclid-graphic` SVGs.
- Native `2560x1440` QHD slide and motion choreography for `photon-platform/studio`.
