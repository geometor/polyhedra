:layout: book
:type: family
:order: 3
:title: P-03 · Catalan Duals & Rhombic Zonohedra
:featured_image: solids/03-catalan/rhombic-triacontahedron/rhombic-triacontahedron.svg
:featured_image_alt: Rhombic Triacontahedron
:excerpt: Face-transitive polar duals of the quasi-regular Archimedean solids discovered by Johannes Kepler in Strena (1611) and Harmonices Mundi (1619).

========================================
P-03 · Catalan Duals & Rhombic Zonohedra
========================================

*Face-Transitive Duals of Archimedean Solids · Space-Filling Rhombic Manifolds*

.. epigraph::

   *Quod si cubum et octahedron conjungas, oritur corpus duodecim basium rhombicarum... At si icosahedron et dodecahedron copules, oritur triacontahedron rhombicum.*

   *For if you join the cube and the octahedron, there arises the body of twelve rhombic bases... But if you unite the icosahedron and the dodecahedron, there arises the rhombic triacontahedron.*

   — **Johannes Kepler**, *Harmonices Mundi*, Lib. II (Linz, 1619)

.. enunciation::

   The **Catalan solids** are the convex, face-transitive (isohedral) polar duals of the semi-regular Archimedean solids. While their vertices are not all equivalent, their faces are congruent non-regular polygons whose dihedral angles are uniform throughout. Among the Catalan solids, the two quasi-regular duals discovered by **Johannes Kepler**—the **Rhombic Dodecahedron** (1611) and the **Rhombic Triacontahedron** (1619)—occupy a unique place: they are equilateral zonohedra bounded by congruent rhombi whose diagonal quadrance ratios embody the fundamental square roots :math:`\sqrt{2}` and the Divine Proportion :math:`\phi`.

.. picture:: /solids/03-catalan/rhombic-triacontahedron/rhombic-triacontahedron.svg
   :alt: Rhombic Triacontahedron Hero Graphic

Polar Duality via Concentric Sphere Reciprocation
-------------------------------------------------

Every Archimedean solid with uniform circumradius :math:`R` and face planes :math:`\Pi_i` can be reciprocated across a concentric sphere of quadrance :math:`Q_0 = R_0^2` via the exact polar map:

.. math::

   \mathbf{v}^*_i = \frac{Q_0}{\mathbf{n}_i \cdot \mathbf{c}_i} \mathbf{n}_i

where :math:`\mathbf{n}_i` is the outward unit normal and :math:`\mathbf{c}_i` is the centroid of face :math:`i`. Each original regular polygon face becomes an ideal vertex of the dual solid, and each original vertex where :math:`k` faces meet becomes a planar :math:`k`-gonal face of the dual. Because Archimedean solids are vertex-transitive (isogonal), their Catalan duals are strictly face-transitive (isohedral).

The Two Keystone Rhombic Zonohedra
----------------------------------

1. **The Space-Filling Rhombic Dodecahedron (P-03.01)**:
   Discovered by **Johannes Kepler** in *Strena seu de Nive Sexangula* (1611) while investigating the optimal packing of spheres and the hexagonal geometry of snowflakes. It possesses 12 congruent rhombic faces whose diagonals have length ratio :math:`\sqrt{2} : 1` (quadrance ratio :math:`2 : 1`). It is the Voronoi cell of the face-centered cubic (FCC) lattice and tiles three-dimensional Euclidean space :math:`\mathbb{R}^3` without gaps or overlaps. Its coordinate field is the strictly rational field :math:`\mathbb{Q}`.

2. **The Golden Rhombic Triacontahedron (P-03.02)**:
   Introduced by **Johannes Kepler** in *Harmonices Mundi* (1619) as the polar dual to the quasi-regular icosidodecahedron. It is bounded by 30 congruent **golden rhombi** whose diagonals are in exact Divine Proportion :math:`\phi : 1` (quadrance ratio :math:`\phi^2 : 1`). As a 3D zonohedral projection of the 6-dimensional hypercube, its 32 vertices partition into 20 threefold vertices of the regular dodecahedron and 12 fivefold vertices of the regular icosahedron. Its coordinate field is the quadratic golden field :math:`\mathbb{Q}(\phi)`.

Canonical Catalan Solids in this Collection
-------------------------------------------

.. collection::
   :type: solid
   :sort: order
