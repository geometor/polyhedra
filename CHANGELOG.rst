0.4.1 (2026-11-15)
------------------

- Overhauled the interactive 3D HTML5 ``<canvas>`` studio (``polyhedra_3d_codex.js``) across all 26 polyhedra and 5 geometric scenes:
  - Replaced legacy Renaissance/Latin UI labels with modern geometric controls (**Surfaces**, **Wireframe**, and **Frame** display modes, plus **Perspective**, **Isometric**, **Front**, and **Top** camera presets).
  - Implemented camera-locked **3-point studio lighting** (warm key light, cool sky fill, rim highlight, Fresnel edge sheen, Blinn–Phong specular highlights, radial studio stage backdrop, and luminous theme-aware crease strokes) eliminating back-lit dark facets during 3D orbit.
  - Added a continuous **Opacity** (surface transparency) slider (``0%``–``100%``) with exact back-to-front painter's sorting of rear and front facets, alongside a **Vertices** toggle rendering depth-sorted 3D vertex spheres across all display modes.

0.4.0 (2026-11-15)
------------------

- Added :mod:`geometor.polyhedra.catalog` cataloging **26 exact symbolic polyhedra across 5 geometric families** (``01-platonic``, ``02-archimedean``, ``03-catalan``, ``04-elevated``, ``05-pyramids``), including :func:`~geometor.polyhedra.catalog.build_rhombicuboctahedron_solid` (*Vigintisex Basium* over :math:`\mathbb{Q}(\sqrt{2})`), :func:`~geometor.polyhedra.catalog.build_pentagonal_pyramid_solid` (Johnson Solid :math:`J_2` / Euclid XIII.16 icosahedral cap over :math:`\mathbb{Q}(\phi)`), and uniform Truncated Dodecahedron at :math:`t = (3 - \phi)/5 \in \mathbb{Q}(\phi)`.
- Reorganized the entire Book Codex into a **one-polyhedron-per-page** architecture (``docsrc/solids/<family>/<slug>/index.rst``) powered by ``photon-platform/publish`` ``.. collection::`` grids (Cards / Banners / List switcher, inline ``.euclid-graphic`` SVG thumbnails, and automatic ``/types/``, ``/categories/``, and ``/tags/`` taxonomy pages), accompanied by a 26-solid :doc:`Master Comparative Ledger <solids/comparative_table>`.
- Atomized ``docsrc/leonardo/`` into **20 individual Tabula-Pair folio studies** (adding Folios ``0283``/``0287`` for the Quadrangular Pyramid and ``0293``/``0295`` for the Pentagonal Pyramid), split ``docsrc/golden/`` into 5 single-theorem collection pages, and upgraded ``docsrc/pyramid/`` to ``.. collection::``.
- Extended ``polyhedra_3d_codex.js`` so ``data-solid="<slug>"`` natively renders all 26 cataloged polyhedra in both *Solidum* and *Vacuum* (genus :math:`g = F - 1` hollow wooden frame) modes with live aperture control and polar dual wireframes.

0.3.0 (2026-11-15)
------------------

- Added :mod:`geometor.polyhedra.pyramid` implementing exact symbolic models over :math:`\mathbb{Q}(\sqrt{\phi})`, :math:`\mathbb{Q}(\pi)`, and :math:`\mathbb{Q}` for the **Great Pyramid**, **1597 Kepler Right Triangle** :math:`(1, \sqrt{\phi}, \phi)`, **Squaring the Circle** (:math:`8 = 2\pi h`, :math:`\pi_{\phi} = 4/\sqrt{\phi}`, :math:`\pi_{22/7} = 22/7`), **Earth–Moon 11:3 Cosmogram**, and **Old Kingdom 14:11 Seked** mensuration.
- Certified 11 exact algebraic identities (:func:`~geometor.polyhedra.pyramid.verify_kepler_pyramid_identities`), including the Herodotus area law (:math:`A_{\text{face}} = h^2 = \phi`), continuous golden surface chain (:math:`A_{\text{base}} : A_{\text{lateral}} : A_{\text{total}} = 1 : \phi : \phi^2`), Icosahedron circumradius edge bridge (:math:`Q_{\text{edge}} = \phi + 2`), and pure :math:`\mathbb{Q}(\phi)` / :math:`\mathbb{Q}` dihedral spreads (:math:`3\phi - 4` and :math:`85848/100489`).
- Added 3D ``Solid3D`` builders (:func:`~geometor.polyhedra.pyramid.build_kepler_pyramid_solid`, :func:`~geometor.polyhedra.pyramid.build_seked_pyramid_solid`, :func:`~geometor.polyhedra.pyramid.build_kepler_bipyramid_solid`), 2D ``geometor.model.Model`` constructions (:func:`~geometor.polyhedra.pyramid.build_kepler_triangle_model`, :func:`~geometor.polyhedra.pyramid.build_pyramid_squaring_circle_model`), interactive 3D scene ``data-scene="great_pyramid_kepler"``, 6 ``.euclid-graphic`` SVGs, and the dedicated ``Great Pyramid`` Book Codex monograph (`docsrc/pyramid/`).

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
