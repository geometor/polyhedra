:layout: book
:title: The Five Platonic Solids

========================
The Five Platonic Solids
========================

*Euclidean Constructions, Golden Ratio Coordinates, and 3D Rational Trigonometry*

.. epigraph::

   *No other figure can be constructed from equilateral and equiangular plane figures, except these five solids alone.*

   — :person:`Euclid of Alexandria`, *Elements* Book XIII, Proposition 18a (Porism)

.. epigraph::

   *Quinque corpora regularia sunt: tetraedron, exaedron sive cubus, octaedron, icosaedron, et dodecaedron. Quorum quodlibet intra sphaeram comprehendi potest.*

   *There are five regular solids: the tetrahedron, hexahedron or cube, octahedron, icosahedron, and dodecahedron. Every one of them can be comprehended within a sphere.*

   — :person:`Luca Pacioli`, *De Divina Proportione*, Cap. I (Venice, 1509)

Axiomatic Foundation & Euclidean Canon
--------------------------------------

In Book XIII of the *Elements*, Euclid constructs the five regular convex polyhedra inside a given sphere and proves in the celebrated Porism to Proposition XIII.18 that **no more than five regular convex solids can exist in Euclidean 3-space**:

1. **Proposition XIII.13** (G-Index: ``G.592``): Construction of the regular **Tetrahedron** inside a sphere (:math:`D^2 = \frac{3}{2} S^2`).
2. **Proposition XIII.14** (G-Index: ``G.594``): Construction of the regular **Octahedron** inside a sphere (:math:`D^2 = 2 S^2`).
3. **Proposition XIII.15** (G-Index: ``G.595``): Construction of the regular **Hexahedron (Cube)** inside a sphere (:math:`D^2 = 3 S^2`).
4. **Proposition XIII.16** (G-Index: ``G.597``): Construction of the regular **Icosahedron** inside a sphere (:math:`S = \text{minor}`).
5. **Proposition XIII.17** (G-Index: ``G.600``): Construction of the regular **Dodecahedron** inside a sphere (:math:`S = \text{apotome}`).

In the GEOMETOR formulation, these five solids are modeled with **zero floating-point numbers** over the rational integer ring :math:`\mathbb{Z}` and the golden algebraic field :math:`\mathbb{Q}(\phi)`, where :math:`\phi = \frac{1 + \sqrt{5}}{2}` satisfies the canonical quadratic minimal polynomial :math:`\phi^2 - \phi - 1 = 0`.

Dedicated Platonic Solid Monographs
-----------------------------------

Each of the five solids is treated in an exhaustive dedicated monograph combining interactive 3D WebGL rendering, exact symbolic coordinate ledgers, 3D Rational Trigonometry proofs, golden ratio analyses, Leonardo da Vinci 1509 woodcut comparisons, and 2D unfolded nets:

.. toctree::
   :maxdepth: 1

   tetrahedron
   hexahedron
   octahedron
   icosahedron
   dodecahedron

Comparative Synthesis Ledger
----------------------------

.. list-table::
   :widths: 14 10 12 10 8 6 6 6 10 12 10 12
   :header-rows: 1

   * - Solid
     - Greek
     - Latin
     - Element
     - $\{p, q\}$
     - $V$
     - $E$
     - $F$
     - Spread $s$
     - $Q_{\text{in}} / Q_{\text{out}}$
     - Dual
     - Vacuum $\chi, g$
   * - :doc:`tetrahedron`
     - Τετράεδρον
     - *Tetrahedron*
     - **Fire**
     - $\{3, 3\}$
     - 4
     - 6
     - 4
     - $8/9$
     - $1/9$
     - Self-dual
     - $\chi = -4, g = 3$
   * - :doc:`hexahedron`
     - Ἑξάεδρον
     - *Exahedron*
     - **Earth**
     - $\{4, 3\}$
     - 8
     - 12
     - 6
     - $1$
     - $1/3$
     - Octahedron
     - $\chi = -8, g = 5$
   * - :doc:`octahedron`
     - Ὀκτάεδρον
     - *Octahedron*
     - **Air**
     - $\{3, 4\}$
     - 6
     - 12
     - 8
     - $8/9$
     - $1/3$
     - Hexahedron
     - $\chi = -12, g = 7$
   * - :doc:`icosahedron`
     - Εἰκοσάεδρον
     - *Icosahedron*
     - **Water**
     - $\{3, 5\}$
     - 12
     - 30
     - 20
     - $4/9$
     - $\frac{4\phi+3}{15}$
     - Dodecahedron
     - $\chi = -36, g = 19$
   * - :doc:`dodecahedron`
     - Δωδεκάεδρον
     - *Dodecahedron*
     - **Aether**
     - $\{5, 3\}$
     - 20
     - 30
     - 12
     - $4/5$
     - $\frac{4\phi+3}{15}$
     - Icosahedron
     - $\chi = -20, g = 11$

3D Rational Trigonometry Dihedral Spread Proof
----------------------------------------------

In Norman Wildberger's Rational Trigonometry, angles between intersecting planes are replaced by the **planar spread** :math:`s = \sin^2\theta`. Given two adjacent planar faces with unnormalized outward normal vectors :math:`n_1` and :math:`n_2`, the spread is computed algebraically without transcendental trigonometric functions:

.. math::

   s(n_1, n_2) = 1 - \frac{(n_1 \cdot n_2)^2}{Q(n_1) Q(n_2)}

where :math:`Q(v) = v_x^2 + v_y^2 + v_z^2` denotes the 3D vector quadrance.

A universal consequence of regular polyhedral geometry is that **the dihedral spread of every Platonic solid is an exact rational number in** :math:`\mathbb{Q}`:

Tetrahedron Dihedral Spread Proof
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let :math:`F_0 = (V_0, V_1, V_2)` and :math:`F_1 = (V_0, V_3, V_1)` with normal vectors :math:`n_0 = (1, 1, -1)` and :math:`n_1 = (1, -1, 1)`.

.. math::

   n_0 \cdot n_1 = 1(1) + 1(-1) + (-1)(1) = -1

.. math::

   Q(n_0) = 1^2 + 1^2 + (-1)^2 = 3, \quad Q(n_1) = 1^2 + (-1)^2 + 1^2 = 3

.. math::

   s(\text{Tetrahedron}) = 1 - \frac{(-1)^2}{3 \times 3} = 1 - \frac{1}{9} = \frac{8}{9}

Hexahedron (Cube) Dihedral Spread Proof
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adjacent square faces meet along Cartesian axes with normal vectors :math:`n_0 = (1, 0, 0)` and :math:`n_2 = (0, 1, 0)`.

.. math::

   n_0 \cdot n_2 = 0, \quad Q(n_0) = 1, \quad Q(n_2) = 1

.. math::

   s(\text{Hexahedron}) = 1 - \frac{0^2}{1 \times 1} = 1

Octahedron Dihedral Spread Proof
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adjacent triangular faces have outward normals :math:`n_0 = (1, 1, 1)` and :math:`n_1 = (1, -1, 1)`.

.. math::

   n_0 \cdot n_1 = 1(1) + 1(-1) + 1(1) = 1

.. math::

   Q(n_0) = 3, \quad Q(n_1) = 3

.. math::

   s(\text{Octahedron}) = 1 - \frac{1^2}{3 \times 3} = 1 - \frac{1}{9} = \frac{8}{9}

.. note::

   The **Tetrahedron** and **Octahedron** share the exact same dihedral spread :math:`s = 8/9`, reflecting their mutual participation in the face-centered cubic lattice!

Icosahedron Dihedral Spread Proof
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The outward normals to two adjacent equilateral triangular faces in golden coordinates satisfy :math:`\cos\theta = -\frac{\sqrt{5}}{3}`.

.. math::

   \cos^2\theta = \frac{5}{9} \implies s(\text{Icosahedron}) = 1 - \frac{5}{9} = \frac{4}{9}

Dodecahedron Dihedral Spread Proof
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The outward normals to two adjacent regular pentagonal faces satisfy :math:`\cos\theta = -\frac{1}{\sqrt{5}}`.

.. math::

   \cos^2\theta = \frac{1}{5} \implies s(\text{Dodecahedron}) = 1 - \frac{1}{5} = \frac{4}{5}

Polar Duality and Symmetry Groups
---------------------------------

The five Platonic solids partition into three reflexive duality pairs governed by finite subgroups of :math:`O(3)`:

1. **Self-Duality (:math:`T_d` Symmetry, Order 24)**:
   The **Tetrahedron** is self-dual (:math:`\{3, 3\}^* = \{3, 3\}`). Connecting the four face centroids yields an inverted regular tetrahedron of edge quadrance :math:`Q = 8/9`.
2. **Cubic Duality (:math:`O_h` Symmetry, Order 48)**:
   The **Hexahedron (Cube)** :math:`\{4, 3\}` and the **Octahedron** :math:`\{3, 4\}` are polar duals. The six face centroids of the cube form the vertices of an inscribed regular octahedron, and the eight face centroids of an octahedron form the vertices of an inscribed cube.
3. **Icosahedral Duality (:math:`I_h` Symmetry, Order 120)**:
   The **Icosahedron** :math:`\{3, 5\}` and the **Dodecahedron** :math:`\{5, 3\}` are polar duals. The twelve face centroids of the dodecahedron form a regular icosahedron, and the twenty face centroids of the icosahedron form a regular dodecahedron. Both solids share the exact same inquadrance-to-circumquadrance ratio:

   .. math::

      \frac{Q_{\text{in}}}{Q_{\text{out}}} = \frac{4\phi + 3}{15} = \frac{5 + 2\sqrt{5}}{15}

Leonardo da Vinci's Structural Variations (1509)
------------------------------------------------

In Luca Pacioli's *De Divina Proportione* (1509), Leonardo da Vinci introduced four principal architectural variations for every regular solid:

- **Planum Solidum**: An opaque body with solid planar facets, shaded with Renaissance woodcut hatching indicating a single upper-left light source (*luce primaria*).
- **Planum Vacuum**: A hollow wooden armillary framework of beam width parameter :math:`\mu`, opening the faces to reveal internal spatial structure, opposite vertices, and dihedral joinery.
- **Abscisum (Truncatum)**: Vertices are cut off perpendicular to their radial vectors, yielding Archimedean semi-regular polyhedra.
- **Elevatum (Stellatum)**: Regular polygonal pyramids are erected on each face, producing Keplerian star polyhedra and triacontahedra.
