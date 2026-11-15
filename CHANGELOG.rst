0.2.1 (2026-11-15)
------------------

- Configured top-level header navigation menus (``Platonic Solids``, ``Golden Proportions``, ``Leonardo Plates``, ``3D Pipeline``, ``Log``, ``Modules``) with active section highlighting and clean Book Codex breadcrumb inheritance across all child chapters.

0.2.0 (2026-11-15)
------------------

- Added exact 3D symbolic modeling kernel :mod:`geometor.polyhedra.model3d` (:class:`~geometor.polyhedra.model3d.Point3D`, :class:`~geometor.polyhedra.model3d.Vector3D`, :class:`~geometor.polyhedra.model3d.Line3D`, :class:`~geometor.polyhedra.model3d.Plane3D`, :class:`~geometor.polyhedra.model3d.Sphere3D`, :class:`~geometor.polyhedra.model3d.Solid3D`) plus 2D Dimensional Bridge (:func:`~geometor.polyhedra.model3d.slice_solid_to_model` and :func:`~geometor.polyhedra.model3d.unfold_net_2d`).
- Implemented exact Conway/Pacioli/Leonardo polyhedral operators in :mod:`geometor.polyhedra.operators`: :func:`~geometor.polyhedra.operators.vacuate` (genus :math:`g = F - 1` hollow wooden manifold), :func:`~geometor.polyhedra.operators.rectify`, :func:`~geometor.polyhedra.operators.truncate`, :func:`~geometor.polyhedra.operators.elevate` (equilateral stellations including *Stella Octangula*), and :func:`~geometor.polyhedra.operators.polar_dual`.
- Added :mod:`geometor.polyhedra.golden` proving six canonical Golden Proportion theorems across 3D polyhedra and 2D cross-sections (3 orthogonal golden rectangles in the icosahedron, golden division of the 12 octahedron edges, Euclid XIII.17 compound of 5 cubes in the dodecahedron, Kepler's 30-face rhombic triacontahedron, Odom's tetrahedron section, meridian hexagon, and equatorial pentagon/pentagram).
- Built multi-backend visualization & CAD export suite :mod:`geometor.polyhedra.render` (`.euclid-graphic` 3D solid/vacuum SVGs, 2D unfolded net SVGs, 2D section SVGs, Wavefront `.obj`/`.mtl`, IngeTrazo 0.6.0 live builder, and Blender 5.x `bpy` studio script) plus zero-dependency interactive HTML5 `<canvas>` 3D Book Codex engine (`polyhedra_3d_codex.js`).
- Authored 15 dedicated `:layout: book` codex pages across `docsrc/platonic/`, `docsrc/golden/`, `docsrc/leonardo/` (with 38 curated 1509 Leonardo da Vinci woodcut plates), and `docsrc/pipeline/`.

0.1.0 (2026-11-14)
------------------

- Initial release of ``geometor-polyhedra`` (v0.1.0) strictly adhering to GEOMETOR exact symbolic standards (zero ``float`` / ``sp.Float``).
- Implemented exact symbolic Platonic solids registry in :mod:`geometor.polyhedra.platonic` (:class:`~geometor.polyhedra.platonic.RegularSolid`) with all 5 regular solids (Tetrahedron, Hexahedron, Octahedron, Icosahedron, Dodecahedron) over :math:`\mathbb{Z}` and :math:`\mathbb{Q}(\phi)`.
- Defined exact 3D Rational Trigonometry vector helpers: :func:`~geometor.polyhedra.platonic.quadrance_3d`, :func:`~geometor.polyhedra.platonic.cross_3d`, :func:`~geometor.polyhedra.platonic.dot_3d`, :func:`~geometor.polyhedra.platonic.face_normal_3d`, and :func:`~geometor.polyhedra.platonic.dihedral_spread_3d`.
- Verified polar-duality ratios (:math:`Q_{\text{in}}/Q_{\text{out}} = 1/3` for Cube and Octahedron, :math:`Q_{\text{in}}/Q_{\text{out}} = (4\phi+3)/15 = 1/3 + 2\sqrt{5}/15` for Dodecahedron and Icosahedron, :math:`Q_{\text{in}}/Q_{\text{out}} = 1/9` for self-dual Tetrahedron), all rational dihedral spreads (:math:`8/9, 1, 8/9, 4/5, 4/9`), Schläfli counts (:math:`pF = 2E = qV`), and Euler characteristic :math:`V - E + F = 2`.
- Linked all 60 Leonardo da Vinci polyhedral plates from Luca Pacioli's *De Divina Proportione* (1509) across primary variants (*solidum*, *vacuum*, *abscisum*, *elevatum*).
- Added ``polyhedra`` Rich CLI and runnable demonstration in ``demos/demo_platonic.py``.
- Authored multi-track Book Codex in ``docsrc/`` with Sphinx AutoAPI reference, Leonardo plates guide, and local intersphinx cross-links.
