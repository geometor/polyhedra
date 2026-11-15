==================
geometor-polyhedra
==================

**Exact symbolic Platonic, Archimedean, and Keplerian polyhedral geometry, Golden Ratio proportions, Leonardo da Vinci Corpora Vacua, and multi-engine 3D exports in SymPy.**

Overview
--------

``geometor-polyhedra`` models three-dimensional constructive geometry, regular and semi-regular polyhedra, and spatial proportion in **100% exact symbolic algebra** (zero floating-point approximations) using `SymPy <https://www.sympy.org/>`_, ``geometor.model``, and ``geometor.divine``.

From Euclid's *Elements* Book XIII to Plato's *Timaeus*, Luca Pacioli and Leonardo da Vinci's *De Divina Proportione* (1509), and Johannes Kepler's *Strena* (1611) and *Harmonices Mundi* (1619), polyhedra unite exact algebraic invariants over $\mathbb{Z}$ and $\mathbb{Q}(\phi)$ ($\phi = \frac{1 + \sqrt{5}}{2}$) with multi-engine 2D and 3D visualization.

The Five Platonic Solids
------------------------

All five regular solids $\{p, q\}$ are modeled symbolically over $\mathbb{Z}$ and $\mathbb{Q}(\phi)$ with pure rational dihedral spreads:

.. list-table::
   :header-rows: 1
   :widths: 16 10 8 8 8 10 12 14 14

   * - Solid
     - Element
     - $\{p, q\}$
     - $V$
     - $E$
     - $F$
     - Euclid
     - Spread
     - $Q_{\text{in}} / Q_{\text{out}}$
   * - **Tetrahedron**
     - Fire
     - $\{3, 3\}$
     - 4
     - 6
     - 4
     - XIII.13
     - $8/9$
     - $1/9$
   * - **Hexahedron**
     - Earth
     - $\{4, 3\}$
     - 8
     - 12
     - 6
     - XIII.15
     - $1$
     - $1/3$
   * - **Octahedron**
     - Air
     - $\{3, 4\}$
     - 6
     - 12
     - 8
     - XIII.14
     - $8/9$
     - $1/3$
   * - **Icosahedron**
     - Water
     - $\{3, 5\}$
     - 12
     - 30
     - 20
     - XIII.16
     - $4/9$
     - $(4\phi+3)/15$
   * - **Dodecahedron**
     - Aether
     - $\{5, 3\}$
     - 20
     - 30
     - 12
     - XIII.17
     - $4/5$
     - $(4\phi+3)/15$

Key Capabilities
----------------

- **Exact 3D Kernel & 2D Bridge** (``geometor.polyhedra.model3d``):
  Zero-float ``Vector3D``, ``Point3D``, ``Line3D``, ``Plane3D``, ``Sphere3D``, and ``Solid3D`` primitives, ``slice_solid_to_model`` for exact planar cross-sections into 2D ``geometor.model.Model``, and ``unfold_net_2d`` for non-overlapping dihedral-hinge 2D nets.
- **Conway, Pacioli & Leonardo Operators** (``geometor.polyhedra.operators``):
  - ``vacuate(solid, aperture, shell)``: Reconstructs Leonardo da Vinci's hollow mitered wooden frames (*Corpora Vacua*) as exact orientable manifolds of $V_{\text{vac}} = 2V + 4E$ vertices, $6E$ strictly coplanar trapezoids, Euler characteristic $\chi = 4 - 2F$, and genus $g = F - 1$.
  - ``rectify`` (*Abscisum*), ``truncate``, ``elevate`` (*Elevatum*, e.g. *Stella Octangula* on the Octahedron), and ``polar_dual`` (yielding Kepler's Rhombic Dodecahedron and Rhombic Triacontahedron).
- **Golden Proportions in the Polyhedra** (``geometor.polyhedra.golden``):
  Six certified theorems with SymPy algebraic proofs and ``geometor.divine`` hooks:
  1. Three mutually orthogonal $1:\phi$ Golden Rectangles spanning the Icosahedron.
  2. $1:\phi$ golden edge division transforming the $\phi^2$-Octahedron into the Icosahedron.
  3. Euclid XIII.17 pentagonal hipped roofs and the compound of 5 inscribed Cubes in the Dodecahedron.
  4. Kepler's 30-face Rhombic Triacontahedron ($Q_{\text{long}} / Q_{\text{short}} = \phi^2$).
  5. George Odom's 1983 equilateral triangle & Tetrahedron circumsphere golden section.
  6. 2D Kepler–Pacioli Golden Meridian Hexagon and Equatorial Pentagon/Pentagram sections.
- **Multi-Backend Renderers & Interactive 3D Codex** (``geometor.polyhedra.render``):
  Theme-adaptive ``.euclid-graphic`` SVGs (``render_solid_svg``, ``render_net_svg``, ``render_model2d_svg``), Wavefront ``.obj``/``.mtl`` export, runnable **IngeTrazo 0.6.0** and **Blender 5.x** studio generators, 38 curated 1509 Leonardo da Vinci woodcut plates, and a zero-dependency interactive HTML5 ``<canvas>`` 3D Book Codex viewer (``polyhedra_3d_codex.js``).

Quickstart
----------

.. code-block:: python

   from geometor.polyhedra import (
       Solid3D,
       build_dodecahedron_five_cubes,
       build_octahedron_golden_icosahedron,
       get_platonic_solid,
       polar_dual,
       rectify,
       vacuate,
   )

   # Reconstruct Leonardo's Dodecahedron Vacuum (Folio 0245, genus g = 11)
   dodec = Solid3D.from_regular_solid(get_platonic_solid("dodecahedron"))
   dodec_vac = vacuate(dodec)
   print(dodec_vac.num_vertices, dodec_vac.num_faces, dodec_vac.genus)  # 160 180 11

   # Construct Kepler's 30-face Rhombic Triacontahedron via polar duality
   triaconta = polar_dual(rectify(dodec))
   print(triaconta.num_vertices, triaconta.num_faces)  # 32 30

   # Verify all 5 Euclid XIII.17 Cubes inscribed in the Dodecahedron
   five_cubes = build_dodecahedron_five_cubes()
   print(len(five_cubes.cubes))  # 5

CLI & Book Codex
----------------

.. code-block:: bash

   # Display summary table of all 5 Platonic solids
   polyhedra

   # Inspect specific solid details
   polyhedra dodecahedron

   # Build the interactive Sphinx Book Codex into docs/
   publish build
