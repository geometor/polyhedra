:title: GEOMETOR • polyhedra

=========
polyhedra
=========

*Exact Symbolic Platonic Solids, Golden Proportions, 3D Rational Trigonometry, and Leonardo da Vinci's Polyhedral Woodcuts*

.. epigraph::

   *Quinque corpora regularia sunt: tetraedron, exaedron sive cubus, octaedron, icosaedron, et dodecaedron. Quorum quodlibet intra sphaeram comprehendi potest.*

   *There are five regular solids: the tetrahedron, hexahedron or cube, octahedron, icosahedron, and dodecahedron. Every one of them can be comprehended within a sphere.*

   — :person:`Luca Pacioli`, *De Divina Proportione* (Venice, 1509)

Overview
--------

**GEOMETOR Polyhedra** (``geometor-polyhedra``) models three-dimensional constructive geometry and regular solids in **100% exact symbolic algebra** (zero floating-point approximations) using `SymPy <https://www.sympy.org/>`_ and ``geometor.model``.

Grounding its algebraic foundations in Euclid's *Elements* Book XIII, Plato's *Timaeus*, Luca Pacioli's *De Divina Proportione* (1509), Johannes Kepler's *Strena* (1611), and Norman Wildberger's Rational Trigonometry, this edition unites classical geometric scholarship with symbolic computation over :math:`\mathbb{Z}` and :math:`\mathbb{Q}(\phi)` (:math:`\phi = \frac{1 + \sqrt{5}}{2}`).

Interactive 3D Polyhedra Explorer
---------------------------------

.. raw:: html

   <div class="polyhedra-3d-mount" data-solid="dodecahedron" data-initial-variant="vacuum"></div>

The Five Platonic Solids
------------------------

.. list-table::
   :header-rows: 1
   :widths: 16 10 10 8 8 8 12 14 14

   * - Solid
     - Greek
     - Element
     - $\{p, q\}$
     - $V$
     - $E$
     - $F$
     - Spread
     - $Q_{\text{in}} / Q_{\text{out}}$
   * - :doc:`platonic/tetrahedron`
     - Τετράεδρον
     - Fire
     - $\{3, 3\}$
     - 4
     - 6
     - 4
     - $8/9$
     - $1/9$
   * - :doc:`platonic/hexahedron`
     - Ἑξάεδρον
     - Earth
     - $\{4, 3\}$
     - 8
     - 12
     - 6
     - $1$
     - $1/3$
   * - :doc:`platonic/octahedron`
     - Ὀκτάεδρον
     - Air
     - $\{3, 4\}$
     - 6
     - 12
     - 8
     - $8/9$
     - $1/3$
   * - :doc:`platonic/icosahedron`
     - Εἰκοσάεδρον
     - Water
     - $\{3, 5\}$
     - 12
     - 30
     - 20
     - $4/9$
     - $\frac{4\phi+3}{15}$
   * - :doc:`platonic/dodecahedron`
     - Δωδεκάεδρον
     - Aether
     - $\{5, 3\}$
     - 20
     - 30
     - 12
     - $4/5$
     - $\frac{4\phi+3}{15}$

Book Codices & Architecture
---------------------------

* :doc:`platonic/index` — Dedicated monographs for the :doc:`Tetrahedron <platonic/tetrahedron>`, :doc:`Hexahedron <platonic/hexahedron>`, :doc:`Octahedron <platonic/octahedron>`, :doc:`Icosahedron <platonic/icosahedron>`, and :doc:`Dodecahedron <platonic/dodecahedron>`, with Euclid Book XIII constructions, pure rational dihedral spreads, interactive 3D solids, and non-overlapping 2D unfolded nets.
* :doc:`golden/index` — Six certified Golden Ratio ($\phi$) theorems across 3D polyhedra and 2D cross-sections: :doc:`Golden Rectangles of the Icosahedron <golden/golden_rectangles>`, :doc:`Golden Division of the Octahedron <golden/octahedron_icosahedron>`, :doc:`Euclid XIII.17 & the Five Cubes in the Dodecahedron <golden/dodecahedron_five_cubes>`, and :doc:`Kepler's Rhombic Triacontahedron & Odom's Tetrahedron Section <golden/rhombic_triacontahedron_odom>`.
* :doc:`leonardo/index` — Side-by-side Digital Scriptorium study of 38 original 1509 woodcut plates by **Leonardo da Vinci** (:doc:`Tabulae I–XX <leonardo/tetrahedron_cube_octahedron>` and :doc:`Tabulae XXI–XXXVI <leonardo/icosahedron_dodecahedron>`) paired with exact genus $g = F - 1$ *Corpora Vacua* reconstructions.
* :doc:`pipeline/index` — Architecture of ``geometor.polyhedra.model3d``, Conway/Pacioli operators (``vacuate``, ``rectify``, ``truncate``, ``elevate``, ``polar_dual``), and multi-engine exports to 2D SVG, HTML5 3D Canvas, **IngeTrazo 0.6.0**, and **Blender 5.x**.
* :doc:`modules/index` · :doc:`log/index` · :doc:`changelog` — Symbolic Python API reference, research log, and release history.
