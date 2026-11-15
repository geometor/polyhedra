:navigation: header
:order: 2
:nav_title: Golden Proportions
:layout: book
:title: Golden Proportions in Polyhedra
:book_title: Golden Proportions in Polyhedra
:book_subtitle: Exact Symbolic Geometry · Divine Proportion Invariants · Keplerian Compounds

===============================
Golden Proportions in Polyhedra
===============================

*Exact Algebraic Embeddings of the Divine Proportion across Regular and Dual Solids*

.. epigraph::

   *Una ipsa eademque convenientia est proportionis divinae qua corpus viginti basium pentagonalium et corpus duodecim basium triangularium conformantur.*

   *The very same correspondence of the divine proportion shapes both the body of twenty pentagonal bases and the body of twelve triangular bases.*

   — :person:`Luca Pacioli`, *De Divina Proportione*, Cap. XXVII (Venice, 1509)

The Golden Ratio in Three Dimensions
------------------------------------

The golden ratio (the divine proportion) :math:`\phi = \frac{1 + \sqrt{5}}{2}` is the fundamental algebraic root of the quadratic equation:

.. math::

   \phi^2 - \phi - 1 = 0 \iff \phi^2 = \phi + 1 \iff \phi^{-1} = \phi - 1

While in two dimensions :math:`\phi` manifests in the regular pentagon, the golden rectangle, and logarithmic spirals, in three-dimensional constructive geometry :math:`\phi` serves as the indispensable structural bridge between the Platonic solids, their compounds, and their duals.

In particular, the regular icosahedron :math:`\{3, 5\}` and regular dodecahedron :math:`\{5, 3\}` cannot be coordinated over the rational field :math:`\mathbb{Q}`, but require the quadratic extension field:

.. math::

   \mathbb{Q}(\phi) = \{ a + b\phi \mid a, b \in \mathbb{Q} \}

In the GEOMETOR architecture, all coordinates, quadrances, face normals, and dihedral spreads are certified symbolically with **zero floating-point approximations**, guaranteeing 100% exact algebraic truth.

Golden Invariants across the Platonic Solids
--------------------------------------------

The Platonic solids exhibit profound internal and mutual golden relationships:

1. **The Icosahedron's Three Orthogonal Golden Rectangles**:
   The twelve vertices of the regular icosahedron form the vertices of three mutually perpendicular golden rectangles of aspect ratio :math:`1 : \phi`. The diagonals of these rectangles intersect at the center of the solid and equal the circumdiameter of the icosahedron.

2. **Continuous Morphism from Octahedron to Icosahedron**:
   Dividing the twelve edges of an octahedron of scale :math:`\phi^2 = \phi + 1` in extreme and mean ratio (:math:`1 : \phi`) generates the exact twelve vertices of the regular icosahedron. When the division parameter :math:`\tau` varies from :math:`1/2` to :math:`\phi^{-1}`, the solid smoothly morphs from the Archimedean cuboctahedron into the Platonic icosahedron.

3. **Euclid's Compound of Five Inscribed Cubes**:
   In *Elements* Book XIII, Proposition 17, Euclid demonstrates that the twenty vertices of the regular dodecahedron contain the vertices of five distinct regular cubes. The sixty edges of these five cubes partition the sixty pentagonal face diagonals into five disjoint subsets. The ratio of the cube edge quadrance to the dodecahedron edge quadrance is exactly :math:`\phi^2`.

4. **Kepler's Rhombic Triacontahedron**:
   In *Strena Seu de Nive Sexangula* (1611), Johannes Kepler united the twenty vertices of the regular dodecahedron with the twelve vertices of its dual regular icosahedron to form the thirty-two vertices of the rhombic triacontahedron. Its thirty faces are congruent golden rhombi whose diagonal quadrance ratio is :math:`\phi^2`.

5. **Planar Sections and George Odom's Theorem**:
   In 1983, George Odom discovered that extending the segment connecting two midpoints of an equilateral triangular face of a tetrahedron to its circumcircle divides the chord in the divine proportion. Similarly, the principal meridian of the icosahedron and the diagonal intersections of the regular pentagon exhibit exact algebraic golden sections.

Certified Golden Polyhedra Theorems
-----------------------------------

The ``geometor.polyhedra.golden`` module implements and algebraically certifies seven canonical golden theorems over :math:`\mathbb{Q}(\phi)`:

.. list-table::
   :header-rows: 1
   :widths: 22 26 24 28

   * - Theorem Slug
     - Title
     - Historical Source
     - Key Golden Identity
   * - ``icosahedron_golden_rectangles``
     - Golden Rectangles of the Icosahedron
     - Euclid XIII.16 · Pacioli Cap. XLIX
     - :math:`Q_{\text{long}} / Q_{\text{short}} = \phi^2`
   * - ``octahedron_golden_icosahedron``
     - Golden Division of Octahedral Edges
     - Pacioli *De Divina Proportione* · Jessen
     - :math:`Q(A, B) / Q(G, B) = \phi^2`
   * - ``dodecahedron_five_cubes``
     - Five Inscribed Cubes in the Dodecahedron
     - Euclid *Elements* XIII.17
     - :math:`Q_{\text{cube}} / Q_{\text{dod}} = \phi^2`
   * - ``rhombic_triacontahedron_golden``
     - Kepler's Rhombic Triacontahedron
     - Kepler *Strena* (1611)
     - :math:`Q_{\text{long}} / Q_{\text{short}} = \phi^2`
   * - ``odom_tetrahedron_section``
     - George Odom's Golden Construction
     - Odom (1983) · Plato *Timaeus*
     - :math:`Q(M_1, M_2) / Q(M_2, G_2) = \phi^2`
   * - ``icosahedron_meridian``
     - Icosahedron Principal Meridian Section
     - Euclid XIII.16 · Pappus *Synagoge* VII
     - :math:`Q_{\text{long}} / Q_{\text{short}} = \phi^2`
   * - ``pentagon_cross_section``
     - Regular Pentagon & Pentagram Sections
     - Euclid *Elements* XIII.8
     - :math:`Q_{\text{diag}} / Q_{\text{side}} = \phi^2`

Codex Sections
--------------

.. toctree::
   :maxdepth: 2

   golden_rectangles
   octahedron_icosahedron
   dodecahedron_five_cubes
   rhombic_triacontahedron_odom
