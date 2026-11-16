:layout: book
:title: Master Comparative Ledger

=========================
Master Comparative Ledger
=========================

*Exact Symbolic Ledger of All Twenty-Six Polyhedra in the GEOMETOR Canon*

This master comparative ledger catalogs all twenty-six canonical polyhedra modeled in ``geometor.polyhedra``. Every metric invariant is computed with 100% exact symbolic precision over its native algebraic number field with zero floating-point approximations.

.. list-table::
   :widths: 8 16 12 10 10 16 12 10 8 10
   :header-rows: 1

   * - ID
     - Solid
     - Family
     - Exact Field
     - $(V, E, F)$
     - Face Composition
     - Edge Quadrance(s)
     - Dihedral Spread
     - Vacua $g$
     - Leonardo Tabulae
   * - ``P-01.01``
     - :doc:`Tetrahedron </solids/01-platonic/tetrahedron/index>`
     - Platonic Solids
     - :math:`\mathbb{Z}`
     - (4, 6, 4)
     - 4 equilateral triangles
     - :math:`8`
     - :math:`\frac{8}{9}`
     - :math:`g = 3`
     - Tabula I, Tabula II
   * - ``P-01.02``
     - :doc:`Hexahedron (Cube) </solids/01-platonic/hexahedron/index>`
     - Platonic Solids
     - :math:`\mathbb{Z}`
     - (8, 12, 6)
     - 6 squares
     - :math:`4`
     - :math:`1`
     - :math:`g = 5`
     - Tabula VII, Tabula VIII
   * - ``P-01.03``
     - :doc:`Octahedron </solids/01-platonic/octahedron/index>`
     - Platonic Solids
     - :math:`\mathbb{Z}`
     - (6, 12, 8)
     - 8 equilateral triangles
     - :math:`2`
     - :math:`\frac{8}{9}`
     - :math:`g = 7`
     - Tabula XV, Tabula XVI
   * - ``P-01.04``
     - :doc:`Icosahedron </solids/01-platonic/icosahedron/index>`
     - Platonic Solids
     - :math:`\mathbb{Q}(\phi)`
     - (12, 30, 20)
     - 20 equilateral triangles
     - :math:`4`
     - :math:`\frac{4}{9}`
     - :math:`g = 19`
     - Tabula XXI, Tabula XXII
   * - ``P-01.05``
     - :doc:`Dodecahedron </solids/01-platonic/dodecahedron/index>`
     - Platonic Solids
     - :math:`\mathbb{Q}(\phi)`
     - (20, 30, 12)
     - 12 regular pentagons
     - :math:`6 - 2 \sqrt{5}`
     - :math:`\frac{4}{5}`
     - :math:`g = 11`
     - Tabula XXVII, Tabula XXVIII
   * - ``P-02.01``
     - :doc:`Truncated Tetrahedron </solids/02-archimedean/truncated-tetrahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}`
     - (12, 18, 8)
     - 4 equilateral triangles + 4 regular hexagons
     - :math:`\frac{8}{9}`
     - :math:`\frac{8}{9}`
     - :math:`g = 7`
     - Tabula III, Tabula IIII
   * - ``P-02.02``
     - :doc:`Cuboctahedron </solids/02-archimedean/cuboctahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}`
     - (12, 24, 14)
     - 8 equilateral triangles + 6 squares
     - :math:`2`
     - :math:`\frac{2}{3}`
     - :math:`g = 13`
     - Tabula VIIII, Tabula X
   * - ``P-02.03``
     - :doc:`Truncated Hexahedron </solids/02-archimedean/truncated-hexahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}(\sqrt{2})`
     - (24, 36, 14)
     - 8 equilateral triangles + 6 regular octagons
     - :math:`12 - 8 \sqrt{2}`
     - :math:`1`
     - :math:`g = 13`
     - —
   * - ``P-02.04``
     - :doc:`Truncated Octahedron </solids/02-archimedean/truncated-octahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}`
     - (24, 36, 14)
     - 6 squares + 8 regular hexagons
     - :math:`\frac{2}{9}`
     - :math:`\frac{8}{9}`
     - :math:`g = 13`
     - Tabula XVII, Tabula XVIII
   * - ``P-02.05``
     - :doc:`Rhombicuboctahedron </solids/02-archimedean/rhombicuboctahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}(\sqrt{2})`
     - (24, 48, 26)
     - 8 equilateral triangles + 18 squares
     - :math:`4`
     - :math:`\frac{1}{2}`
     - :math:`g = 25`
     - Tabula XXXV, Tabula XXXVI
   * - ``P-02.06``
     - :doc:`Icosidodecahedron </solids/02-archimedean/icosidodecahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}(\phi)`
     - (30, 60, 32)
     - 20 equilateral triangles + 12 regular pentagons
     - :math:`1`
     - :math:`\frac{2}{3} - \frac{2 \sqrt{5}}{15}`
     - :math:`g = 31`
     - Tabula XXIX, Tabula XXX
   * - ``P-02.07``
     - :doc:`Truncated Icosahedron </solids/02-archimedean/truncated-icosahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}(\phi)`
     - (60, 90, 32)
     - 12 regular pentagons + 20 regular hexagons
     - :math:`\frac{4}{9}`
     - :math:`\frac{4}{9}`
     - :math:`g = 31`
     - Tabula XXIII, Tabula XXIIII
   * - ``P-02.08``
     - :doc:`Truncated Dodecahedron </solids/02-archimedean/truncated-dodecahedron/index>`
     - Archimedean Solids
     - :math:`\mathbb{Q}(\phi)`
     - (60, 90, 32)
     - 20 equilateral triangles + 12 regular decagons
     - :math:`\frac{6}{5} - \frac{2 \sqrt{5}}{5}`
     - :math:`\frac{4}{5}`
     - :math:`g = 31`
     - —
   * - ``P-03.01``
     - :doc:`Rhombic Dodecahedron </solids/03-catalan/rhombic-dodecahedron/index>`
     - Catalan Solids
     - :math:`\mathbb{Q}`
     - (14, 24, 12)
     - 12 rhombi
     - :math:`\frac{27}{16}`
     - :math:`\frac{3}{4}`
     - :math:`g = 11`
     - —
   * - ``P-03.02``
     - :doc:`Rhombic Triacontahedron </solids/03-catalan/rhombic-triacontahedron/index>`
     - Catalan Solids
     - :math:`\mathbb{Q}(\phi)`
     - (32, 60, 30)
     - 30 golden rhombi
     - :math:`\frac{5 \sqrt{5}}{32} + \frac{25}{32}`
     - :math:`\frac{5}{8} - \frac{\sqrt{5}}{8}`
     - :math:`g = 29`
     - —
   * - ``P-04.01``
     - :doc:`Tetrahedron Elevatum </solids/04-elevated/tetrahedron-elevatum/index>`
     - Elevated Solids (Corpora Elevata)
     - :math:`\mathbb{Q}`
     - (8, 18, 12)
     - 12 equilateral triangles
     - :math:`8`
     - :math:`\frac{8}{9}`
     - :math:`g = 11`
     - Tabula V, Tabula VI
   * - ``P-04.02``
     - :doc:`Hexahedron Elevatum </solids/04-elevated/hexahedron-elevatum/index>`
     - Elevated Solids (Corpora Elevata)
     - :math:`\mathbb{Q}(\sqrt{2})`
     - (14, 36, 24)
     - 24 equilateral triangles
     - :math:`4`
     - :math:`\frac{8}{9}`
     - :math:`g = 23`
     - Tabula XI, Tabula XII
   * - ``P-04.03``
     - :doc:`Stella Octangula (Octahedron Elevatum) </solids/04-elevated/stella-octangula/index>`
     - Elevated Solids (Corpora Elevata)
     - :math:`\mathbb{Z}`
     - (14, 36, 24)
     - 24 equilateral triangles
     - :math:`2`
     - :math:`\frac{8}{9}`
     - :math:`g = 23`
     - Tabula XIX, Tabula XX
   * - ``P-04.04``
     - :doc:`Icosahedron Elevatum </solids/04-elevated/icosahedron-elevatum/index>`
     - Elevated Solids (Corpora Elevata)
     - :math:`\mathbb{Q}(\phi, \sqrt{2})`
     - (32, 90, 60)
     - 60 equilateral triangles
     - :math:`4`
     - :math:`\frac{8}{9}`
     - :math:`g = 59`
     - Tabula XXV, Tabula XXVI
   * - ``P-04.05``
     - :doc:`Dodecahedron Elevatum </solids/04-elevated/dodecahedron-elevatum/index>`
     - Elevated Solids (Corpora Elevata)
     - :math:`\mathbb{Q}(\sqrt{5 - \sqrt{5}})`
     - (32, 90, 60)
     - 60 equilateral triangles
     - :math:`6 - 2 \sqrt{5}`
     - :math:`\frac{4}{9}`
     - :math:`g = 59`
     - Tabula XXXI, Tabula XXXII
   * - ``P-04.06``
     - :doc:`Cuboctahedron Elevatum </solids/04-elevated/cuboctahedron-elevatum/index>`
     - Elevated Solids (Corpora Elevata)
     - :math:`\mathbb{Q}`
     - (26, 72, 48)
     - 48 equilateral triangles
     - :math:`2`
     - :math:`\frac{8}{9}`
     - :math:`g = 47`
     - Tabula XIII, Tabula XIIII
   * - ``P-04.07``
     - :doc:`Icosidodecahedron Elevatum </solids/04-elevated/icosidodecahedron-elevatum/index>`
     - Elevated Solids (Corpora Elevata)
     - :math:`\mathbb{Q}(\sqrt{5 - \sqrt{5}}, \sqrt{2})`
     - (62, 180, 120)
     - 120 equilateral triangles
     - :math:`1`
     - :math:`\frac{8}{9}`
     - :math:`g = 119`
     - Tabula XXXIII, Tabula XXXIIII
   * - ``P-05.01``
     - :doc:`Kepler Golden Pyramid </solids/05-pyramids/kepler-pyramid/index>`
     - Pyramids & Bipyramids
     - :math:`\mathbb{Q}(\sqrt{\phi})`
     - (5, 8, 5)
     - 1 square + 4 Kepler golden triangles
     - :math:`\frac{\sqrt{5}}{2} + \frac{5}{2}`, :math:`4`
     - :math:`- \frac{5}{2} + \frac{3 \sqrt{5}}{2}`
     - :math:`g = 4`
     - Tabula XLVII, Tabula XLVIII
   * - ``P-05.02``
     - :doc:`Seked 14:11 Pyramid </solids/05-pyramids/seked-pyramid/index>`
     - Pyramids & Bipyramids
     - :math:`\mathbb{Q}`
     - (5, 8, 5)
     - 1 square + 4 Seked 14:11 triangles
     - :math:`\frac{438}{121}`, :math:`4`
     - :math:`\frac{85848}{100489}`
     - :math:`g = 4`
     - Tabula XLVII, Tabula XLVIII
   * - ``P-05.03``
     - :doc:`Golden Square Bipyramid </solids/05-pyramids/golden-bipyramid/index>`
     - Pyramids & Bipyramids
     - :math:`\mathbb{Q}(\sqrt{\phi})`
     - (6, 12, 8)
     - 8 Kepler golden triangles
     - :math:`\frac{\sqrt{5}}{2} + \frac{5}{2}`, :math:`4`
     - :math:`- \frac{5}{2} + \frac{3 \sqrt{5}}{2}`
     - :math:`g = 7`
     - —
   * - ``P-05.04``
     - :doc:`Regular Pentagonal Pyramid (Johnson J2) </solids/05-pyramids/pentagonal-pyramid/index>`
     - Pyramids & Bipyramids
     - :math:`\mathbb{Q}(\phi)`
     - (6, 10, 6)
     - 1 regular pentagon + 5 equilateral triangles
     - :math:`4`
     - :math:`\frac{2}{3} - \frac{2 \sqrt{5}}{15}`
     - :math:`g = 5`
     - Tabula LI, Tabula LII
