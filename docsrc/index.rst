:site_title: Polyhedra

.. container:: author-overline

   semantic digital archive • mathematical catalog

=========
Polyhedra
=========

.. epigraph::

   *Quinque corpora regularia sunt: tetraedron, exaedron sive cubus, octaedron, icosaedron, et dodecaedron. Quorum quodlibet intra sphaeram comprehendi potest.*

   *There are five regular solids: the tetrahedron, hexahedron or cube, octahedron, icosahedron, and dodecahedron. Every one of them can be comprehended within a sphere.*

   — **Luca Pacioli**, *De Divina Proportione* (Venice, 1509)

Overview
--------

The mathematical catalog models three-dimensional constructive geometry, regular and semi-regular polyhedra, and spatial proportion in 100% exact symbolic algebra using SymPy, Rational Trigonometry dihedral spreads, and exact number fields. Within the interconnected `GEOMETOR <https://geometor.com/books/>`_ semantic digital archive, classical treatises—from Euclid's *Elements* Book XIII and Plato's *Timaeus* to Luca Pacioli's *De Divina Proportione* and Johannes Kepler's *Harmonices Mundi*—are liberated into 26 exact symbolic solids, interactive 3D HTML5 viewports, theme-adaptive vector diagrams, and Leonardo da Vinci woodcut folios speaking one shared geometric language.

Interactive 3D Polyhedra Explorer
---------------------------------

.. raw:: html

   <div class="polyhedra-3d-mount" data-solid="dodecahedron"></div>

The Five Polyhedral Families (26 Canonical Solids)
--------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 10 24 44

   * - Family Collection
     - Solids
     - Exact Algebraic Fields
     - Representative Polyhedra
   * - :doc:`Platonic Solids <solids/01-platonic/index>`
     - **5**
     - :math:`\mathbb{Z}`, :math:`\mathbb{Q}(\phi)`
     - :doc:`Tetrahedron <solids/01-platonic/tetrahedron/index>` · :doc:`Hexahedron <solids/01-platonic/hexahedron/index>` · :doc:`Octahedron <solids/01-platonic/octahedron/index>` · :doc:`Icosahedron <solids/01-platonic/icosahedron/index>` · :doc:`Dodecahedron <solids/01-platonic/dodecahedron/index>`
   * - :doc:`Archimedean Solids <solids/02-archimedean/index>`
     - **8**
     - :math:`\mathbb{Q}`, :math:`\mathbb{Q}(\sqrt{2})`, :math:`\mathbb{Q}(\phi)`
     - :doc:`Cuboctahedron <solids/02-archimedean/cuboctahedron/index>` · :doc:`Truncated Octahedron <solids/02-archimedean/truncated-octahedron/index>` · :doc:`Rhombicuboctahedron <solids/02-archimedean/rhombicuboctahedron/index>` · :doc:`Icosidodecahedron <solids/02-archimedean/icosidodecahedron/index>` · :doc:`Truncated Icosahedron <solids/02-archimedean/truncated-icosahedron/index>`
   * - :doc:`Catalan Duals <solids/03-catalan/index>`
     - **2**
     - :math:`\mathbb{Q}`, :math:`\mathbb{Q}(\phi)`
     - :doc:`Rhombic Dodecahedron <solids/03-catalan/rhombic-dodecahedron/index>` · :doc:`Rhombic Triacontahedron <solids/03-catalan/rhombic-triacontahedron/index>`
   * - :doc:`Elevated & Stellated <solids/04-elevated/index>`
     - **7**
     - :math:`\mathbb{Z}`, :math:`\mathbb{Q}`, :math:`\mathbb{Q}(\sqrt{2})`, :math:`\mathbb{Q}(\phi, \sqrt{6})`
     - :doc:`Stella Octangula <solids/04-elevated/stella-octangula/index>` · :doc:`Tetrahedron Elevatum <solids/04-elevated/tetrahedron-elevatum/index>` · :doc:`Icosahedron Elevatum <solids/04-elevated/icosahedron-elevatum/index>` · :doc:`Dodecahedron Elevatum <solids/04-elevated/dodecahedron-elevatum/index>`
   * - :doc:`Pyramids & Bipyramids <solids/05-pyramids/index>`
     - **4**
     - :math:`\mathbb{Q}`, :math:`\mathbb{Q}(\phi)`, :math:`\mathbb{Q}(\sqrt{\phi})`
     - :doc:`Kepler Golden Pyramid <solids/05-pyramids/kepler-pyramid/index>` · :doc:`Seked 14:11 Great Pyramid <solids/05-pyramids/seked-pyramid/index>` · :doc:`Golden Square Bipyramid <solids/05-pyramids/golden-bipyramid/index>` · :doc:`Regular Pentagonal Pyramid <solids/05-pyramids/pentagonal-pyramid/index>`

Book Codices & Collections
--------------------------

* :doc:`solids/index` — **Master Polyhedra Catalog (26 Solids, One Polyhedron Per Page)** organized into 5 collection families with inline SVG cards, interactive 3D *Solidum* / *Vacuum* studios, unfolded 2D nets, and :doc:`Master Comparative Ledger <solids/comparative_table>`.
* :doc:`golden/index` — Collection of certified Golden Ratio (:math:`\phi`) theorems across 3D polyhedra and 2D cross-sections: :doc:`Golden Rectangles of the Icosahedron <golden/golden_rectangles>`, :doc:`Golden Division of the Octahedron <golden/octahedron_icosahedron>`, :doc:`Euclid XIII.17 & the Five Cubes in the Dodecahedron <golden/dodecahedron_five_cubes>`, :doc:`Kepler's Rhombic Triacontahedron <golden/rhombic_triacontahedron>`, and :doc:`Odom's Tetrahedron Section <golden/odom_tetrahedron_section>`.
* :doc:`leonardo/index` — Visual museum collection of **20 paired 1509 woodcut folio studies** by **Leonardo da Vinci** from Luca Pacioli's *De Divina Proportione*, paired with exact genus :math:`g = F - 1` *Corpora Vacua* proofs.
* :doc:`pyramid/index` — Collection of treatises on **Kepler, Squaring the Circle & the Great Pyramid**: :doc:`The 1597 Kepler Right Triangle <pyramid/kepler_triangle>` (:math:`1, \sqrt{\phi}, \phi`; :math:`A_{\text{face}} = h^2 = \phi`), :doc:`Squaring the Circle & the Earth–Moon Cosmogram <pyramid/squaring_the_circle>` (:math:`8 = 2\pi h`, :math:`\pi_{\phi} = 4/\sqrt{\phi}`, :math:`r_M/r_E = 3/11`), and :doc:`Egyptian 14:11 Seked Mensuration & Polyhedral Spreads <pyramid/seked_and_octahedron>`.
* :doc:`pipeline/index` — Architecture of ``geometor.polyhedra.model3d``, Conway/Pacioli operators (``vacuate``, ``rectify``, ``truncate``, ``elevate``, ``polar_dual``), and multi-engine exports to 2D SVG, HTML5 3D Canvas, **IngeTrazo 0.6.0**, and **Blender 5.x**.
* :doc:`modules/index` · :doc:`log/index` · :doc:`changelog` — Symbolic Python API reference, research log collection, and release history.
