:layout: book
:type: family
:order: 4
:title: P-04 · Elevated Solids (Corpora Elevata)
:featured_image: solids/04-elevated/stella-octangula/stella-octangula.svg
:featured_image_alt: Stella Octangula (Octahedron Elevatum)
:excerpt: Seven equilateral-pyramid stellations drawn by Leonardo da Vinci in De Divina Proportione (1509) and analyzed by Johannes Kepler (1619).

========================================
P-04 · Elevated Solids (Corpora Elevata)
========================================

*Renaissance Stellations of Plato and Archimedes by Luca Pacioli & Leonardo da Vinci*

.. epigraph::

   *Corpus elevatum dicitur quando super qualibet eius basi erigitur una pyramis... quae quidem pyramides omnes eiusdem altitudinis existunt et bases aequales habent.*

   *An elevated body is said to be formed when upon each of its bases a pyramid is erected... which pyramids all exist of the same height and have equal bases.*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXVIII (Venice, 1509)

.. enunciation::

   The **Elevated Solids** (*Corpora Elevata*) are non-convex stellated polyhedra created by erecting equilateral-triangle pyramids upon every planar facet of a convex Platonic or Archimedean solid. Systematically cataloged by **Fra Luca Pacioli** and illustrated with perspective mastery by **Leonardo da Vinci** in *De Divina Proportione* (1509), these seven canonical stellations bridge classical Euclidean polyhedra with early modern projective and star geometry.

.. picture:: /solids/04-elevated/stella-octangula/stella-octangula.svg
   :alt: Stella Octangula Hero Graphic

The Renaissance Elevation Operator (Elevatio)
---------------------------------------------

In constructive geometry, the elevation operator :math:`\operatorname{elevate}(S)` erects a right pyramid of altitude :math:`h_k` upon each :math:`k`-gonal face of a base polyhedron :math:`S` with edge length :math:`s`. To ensure that every lateral face of the erected pyramid forms an equilateral triangle of edge length :math:`s`, the pyramid altitude :math:`h_k` must satisfy the exact Pythagorean relation:

.. math::

   h_k^2 + r_k^2 = s^2 \implies h_k = \sqrt{s^2 - r_k^2}

where :math:`r_k = \frac{s}{2 \sin(\pi/k)}` is the circumradius of the regular :math:`k`-gon. For the regular faces encountered in Platonic and Archimedean solids:

- **Triangular Faces (:math:`k=3`)**: :math:`r_3 = \frac{s}{\sqrt{3}} \implies h_3 = s \sqrt{1 - \frac{1}{3}} = s \frac{\sqrt{6}}{3}`
- **Square Faces (:math:`k=4`)**: :math:`r_4 = \frac{s}{\sqrt{2}} \implies h_4 = s \sqrt{1 - \frac{1}{2}} = s \frac{\sqrt{2}}{2}`
- **Pentagonal Faces (:math:`k=5`)**: :math:`r_5 = \frac{s}{\sqrt{5 - \sqrt{5}}} \implies h_5 = s \sqrt{\frac{5 - \sqrt{5}}{10}}`

Radical Cancellation & Algebraic Collapse (:math:`\mathbb{Z}` and :math:`\mathbb{Q}`)
-------------------------------------------------------------------------------------

Remarkably, although the altitude formulas involve square roots, the resulting 3D coordinates undergo profound algebraic collapses:

1. **Stella Octangula (Octahedron Elevatum, P-04.03)**:
   When equilateral pyramids of altitude :math:`h_3 = \frac{2}{\sqrt{6}}` are erected on the 8 triangular faces of a regular octahedron with edge :math:`\sqrt{2}`, the apex displacement along the face normal :math:`\mathbf{n} = (\pm 1, \pm 1, \pm 1)` cancels all square roots:

   .. math::

      \mathbf{apex} = \mathbf{c}_f + \frac{h_3}{\|\mathbf{n}\|} \mathbf{n} = \left(\frac{1}{3}, \frac{1}{3}, \frac{1}{3}\right) + \frac{2}{3}(1, 1, 1) = (1, 1, 1) \in \mathbb{Z}^3

   The 8 apices together form the 8 integer vertices of a cube :math:`(\pm 1, \pm 1, \pm 1)`. The resulting manifold is the **Stella Octangula**, the regular compound of two dual tetrahedra, living entirely in the integer ring :math:`\mathbb{Z}`!

2. **Tetrahedron Elevatum (P-04.01)**:
   Erecting pyramids on the 4 faces of a regular tetrahedron of edge :math:`\sqrt{8}` produces 4 apices at :math:`\left(\pm \frac{5}{3}, \pm \frac{5}{3}, \pm \frac{5}{3}\right)`. All 8 vertices lie strictly in the rational field :math:`\mathbb{Q}`.

3. **Cuboctahedron Elevatum (P-04.06)**:
   Erecting equilateral pyramids on the 8 triangular faces and 6 square faces of the Archimedean cuboctahedron generates apices at :math:`\left(\pm \frac{4}{3}, \pm \frac{4}{3}, \pm \frac{4}{3}\right)` and :math:`(\pm 2, 0, 0)`, placing the entire 26-vertex manifold within :math:`\mathbb{Q}`!

Leonardo da Vinci's Paired 1509 Woodcuts
----------------------------------------

In *De Divina Proportione*, **Leonardo da Vinci** illustrated each elevated body twice:
first as a solid form (*Solidum*) featuring intricate chiaroscuro perspective and cast shadows,
and second as a hollow framework (*Corpus Vacuum*) carved from mitered wooden beams.
The hollow lattice framework reveals the internal polyhedral cavity while increasing the topological genus to :math:`g = F - 1`.

Canonical Elevated Solids in this Collection
--------------------------------------------

.. collection::
   :type: solid
   :sort: order
