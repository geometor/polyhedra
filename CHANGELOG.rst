0.1.0 (2026-11-14)
------------------

- Initial release of ``geometor-polyhedra`` (v0.1.0) strictly adhering to GEOMETOR exact symbolic standards (zero ``float`` / ``sp.Float``).
- Implemented exact symbolic Platonic solids registry in :mod:`geometor.polyhedra.platonic` (:class:`~geometor.polyhedra.platonic.RegularSolid`) with all 5 regular solids (Tetrahedron, Hexahedron, Octahedron, Icosahedron, Dodecahedron) over :math:`\mathbb{Z}` and :math:`\mathbb{Q}(\phi)`.
- Defined exact 3D Rational Trigonometry vector helpers: :func:`~geometor.polyhedra.platonic.quadrance_3d`, :func:`~geometor.polyhedra.platonic.cross_3d`, :func:`~geometor.polyhedra.platonic.dot_3d`, :func:`~geometor.polyhedra.platonic.face_normal_3d`, and :func:`~geometor.polyhedra.platonic.dihedral_spread_3d`.
- Verified polar-duality ratios (:math:`Q_{\text{in}}/Q_{\text{out}} = 1/3` for Cube and Octahedron, :math:`Q_{\text{in}}/Q_{\text{out}} = (4\phi+3)/15 = 1/3 + 2\sqrt{5}/15` for Dodecahedron and Icosahedron, :math:`Q_{\text{in}}/Q_{\text{out}} = 1/9` for self-dual Tetrahedron), all rational dihedral spreads (:math:`8/9, 1, 8/9, 4/5, 4/9`), Schläfli counts (:math:`pF = 2E = qV`), and Euler characteristic :math:`V - E + F = 2`.
- Linked all 60 Leonardo da Vinci polyhedral plates from Luca Pacioli's *De Divina Proportione* (1509) across primary variants (*solidum*, *vacuum*, *abscisum*, *elevatum*).
- Added ``polyhedra`` Rich CLI and runnable demonstration in ``demos/demo_platonic.py``.
- Authored multi-track Book Codex in ``docsrc/`` with Sphinx AutoAPI reference, Leonardo plates guide, and local intersphinx cross-links.
