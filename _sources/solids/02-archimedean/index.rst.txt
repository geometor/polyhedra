:layout: book
:type: family
:order: 2
:title: P-02 · Archimedean & Abscisa Solids
:featured_image: solids/02-archimedean/rhombicuboctahedron/rhombicuboctahedron.svg
:featured_image_alt: Rhombicuboctahedron (Vigintisex Basium)
:excerpt: Eight uniform semi-regular truncations, midpoint rectifications, and Leonardo da Vinci's 26-base body modeled over Q, Q(sqrt(2)), and Q(phi).

===================================
P-02 · Archimedean & Abscisa Solids
===================================

*Uniform Corner Truncations, Edge-Midpoint Rectifications, and Leonardo's Vigintisex Basium*

.. epigraph::

   *Archimedes discovered thirteen solids bounded by regular polygons of more than one kind, every vertex being surrounded in the same manner by the same figures.*

   — **Pappus of Alexandria**, *Synagoge* (Collection), Book V

.. epigraph::

   *Abscisa corpora sunt quae ex regularibus nascendo per abscisionem angulorum solidorum fiunt... inter quae eminet vigintisex basium planum solidum et vacuum.*

   *The truncated bodies are those which originate from the regular solids through the cutting away of their solid angles... among which the twenty-six base body, solid and hollow, stands supreme.*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. LXI (Venice, 1509)

The Archimedean Canon in GEOMETOR
---------------------------------

While the five Platonic solids are strictly isohedral (face-transitive) and isogonal (vertex-transitive) with a single regular polygon type, the **Archimedean Solids** are semi-regular convex polyhedra: their faces are regular polygons of two or more distinct types, yet every vertex is symmetrically equivalent under the action of the symmetry group (isogonal).

In the GEOMETOR formulation, eight canonical Archimedean and *Abscisa* polyhedra are modeled with 100% exact symbolic coordinates across three algebraic fields:

1. **The Rational Field** :math:`\mathbb{Q}`: The Truncated Tetrahedron, Cuboctahedron, and Truncated Octahedron.
2. **The Quadratic Extension** :math:`\mathbb{Q}(\sqrt{2})`: The Truncated Hexahedron and Leonardo's Rhombicuboctahedron (*Vigintisex Basium*).
3. **The Golden Algebraic Field** :math:`\mathbb{Q}(\phi)`: The Icosidodecahedron, Truncated Icosahedron (Fullerene Buckyball), and Truncated Dodecahedron.

Constructive Operators: Truncation and Rectification
----------------------------------------------------

Every Archimedean solid in this family is generated from a primary Platonic solid by an exact algebraic operator implemented in ``geometor.polyhedra.operators``:

Corner Truncation: ``truncate(solid, t)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cutting off each vertex of a solid along planes perpendicular to the vertex radius at an exact fractional edge depth :math:`t \in (0, 1/2)` replaces each :math:`n`-valent vertex with a regular :math:`n`-gon and transforms each original :math:`k`-gon into a :math:`2k`-gon:

- **Rational Truncation** (:math:`t = 1/3`):
  Cutting the regular tetrahedron at one-third edge length yields 4 triangles and 4 regular hexagons (**Truncated Tetrahedron**). Cutting the regular octahedron at :math:`t = 1/3` yields 6 squares and 8 regular hexagons (**Truncated Octahedron**, the Kelvin space-filling permutohedron).
- **Octagonal Truncation** (:math:`t = 1 - \frac{\sqrt{2}}{2}`):
  Cutting the cube at depth :math:`t = 1 - \frac{\sqrt{2}}{2} \in \mathbb{Q}(\sqrt{2})` yields 8 triangles and 6 regular octagons (**Truncated Hexahedron**).
- **Fullerene Truncation** (:math:`t = 1/3`):
  Cutting the regular icosahedron at one-third edge length yields 12 regular pentagons and 20 regular hexagons (**Truncated Icosahedron**, the canonical :math:`C_{60}` soccer ball / buckyball).
- **Golden Decagonal Truncation** (:math:`t = \frac{3 - \phi}{5}`):
  Cutting the regular dodecahedron at exact depth :math:`t = \frac{3 - \phi}{5} = \frac{5 - \sqrt{5}}{10} \in \mathbb{Q}(\phi)` yields 20 triangles and 12 regular decagons (**Truncated Dodecahedron**).

Edge-Midpoint Rectification: ``rectify(solid)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the truncation depth reaches the exact midpoint of every edge (:math:`t = 1/2`), the original faces contract into their centroids and vertices merge:

- **Cuboctahedron** (*Exahedron Abscisum*): Rectifying either the cube or the octahedron produces the unique 14-faceted body with 12 vertices, 24 edges of uniform quadrance 2, and 8 triangular + 6 square faces.
- **Icosidodecahedron** (*Dodecahedron Abscisum*): Rectifying either the dodecahedron or the icosahedron produces the unique 32-faceted golden ratio body with 30 vertices, 60 edges, and 20 triangular + 12 pentagonal faces.

Leonardo da Vinci's 26-Base Body: Vigintisex Basium
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Luca Pacioli's *De Divina Proportione* (Cap. LXI, Tabulae XXXV–XXXVI), Leonardo da Vinci celebrated the **Rhombicuboctahedron** under the name *Vigintisex Basium* (the 26-Base Body). Bounded by 18 squares (6 axial and 12 chamfer facets) and 8 equilateral octant triangles, it is modeled over :math:`\mathbb{Q}(\sqrt{2})` with 24 vertices and 48 edges of uniform quadrance 4.

Comparative Synthesis Ledger
----------------------------

.. list-table::
   :widths: 10 16 12 12 8 8 8 12 12
   :header-rows: 1

   * - ID
     - Solid
     - Latin Name
     - Field
     - $V$
     - $E$
     - $F$
     - Face Composition
     - Dual Solid
   * - ``P-02.01``
     - :doc:`Truncated Tetrahedron <truncated-tetrahedron/index>`
     - *Tetrahedron Abscisum*
     - :math:`\mathbb{Q}`
     - 12
     - 18
     - 8
     - 4 triangles + 4 hexagons
     - Triakis Tetrahedron
   * - ``P-02.02``
     - :doc:`Cuboctahedron <cuboctahedron/index>`
     - *Exahedron Abscisum*
     - :math:`\mathbb{Q}`
     - 12
     - 24
     - 14
     - 8 triangles + 6 squares
     - :doc:`Rhombic Dodecahedron </solids/03-catalan/rhombic-dodecahedron/index>`
   * - ``P-02.03``
     - :doc:`Truncated Hexahedron <truncated-hexahedron/index>`
     - *Exahedron Abscisum Octogonale*
     - :math:`\mathbb{Q}(\sqrt{2})`
     - 24
     - 36
     - 14
     - 8 triangles + 6 octagons
     - Triakis Octahedron
   * - ``P-02.04``
     - :doc:`Truncated Octahedron <truncated-octahedron/index>`
     - *Octahedron Abscisum*
     - :math:`\mathbb{Q}`
     - 24
     - 36
     - 14
     - 6 squares + 8 hexagons
     - Tetrakis Hexahedron
   * - ``P-02.05``
     - :doc:`Rhombicuboctahedron <rhombicuboctahedron/index>`
     - *Vigintisex Basium*
     - :math:`\mathbb{Q}(\sqrt{2})`
     - 24
     - 48
     - 26
     - 8 triangles + 18 squares
     - Deltoidal Icositetrahedron
   * - ``P-02.06``
     - :doc:`Icosidodecahedron <icosidodecahedron/index>`
     - *Dodecahedron Abscisum*
     - :math:`\mathbb{Q}(\phi)`
     - 30
     - 60
     - 32
     - 20 triangles + 12 pentagons
     - :doc:`Rhombic Triacontahedron </solids/03-catalan/rhombic-triacontahedron/index>`
   * - ``P-02.07``
     - :doc:`Truncated Icosahedron <truncated-icosahedron/index>`
     - *Icosahedron Abscisum*
     - :math:`\mathbb{Q}(\phi)`
     - 60
     - 90
     - 32
     - 12 pentagons + 20 hexagons
     - Pentakis Dodecahedron
   * - ``P-02.08``
     - :doc:`Truncated Dodecahedron <truncated-dodecahedron/index>`
     - *Dodecahedron Abscisum Decagonale*
     - :math:`\mathbb{Q}(\phi)`
     - 60
     - 90
     - 32
     - 20 triangles + 12 decagons
     - Triakis Icosahedron

.. picture:: /solids/02-archimedean/rhombicuboctahedron/rhombicuboctahedron.svg

The Eight Archimedean Monograph Folios
--------------------------------------

.. collection::
   :type: solid
   :sort: order
