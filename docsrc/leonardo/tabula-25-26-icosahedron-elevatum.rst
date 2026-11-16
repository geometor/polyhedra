:layout: book
:type: plate
:order: 13
:title: Tabulae XXV–XXVI: Icosahedron Elevatum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0239.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XXV Folio 0239 - Icosahedron Elevatum Solidum
:categories: leonardo-1509, elevated
:tags: pacioli, woodcut, solidum, vacuum, icosahedron-elevatum, triakis-icosahedron, elevated-solids
:excerpt: Leonardo da Vinci's woodcut pair depicting the Triakis Icosahedron (Icosahedron Elevatum), erecting equilateral pyramids over all 20 triangular facets of the icosahedron to produce 60 triangular faces and a genus g = 59 hollow framework.

===============================================================
Tabulae XXV–XXVI: Icosahedron Elevatum Solidum et Vacuum (1509)
===============================================================

*The Triakis Icosahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Icosahedron elevatum solidum est quando super qualibet viginti basium icosahedri erigitur una pyramis triangularis...*

   *The solid elevated icosahedron is when upon each of the twenty bases of the icosahedron a triangular pyramid is erected...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXXVIII (Venice, 1509)

.. enunciation::

   By erecting equilateral triangular pyramids over each of the 20 triangular faces of a regular icosahedron, Leonardo da Vinci constructs the **Triakis Icosahedron** (*Icosahedron Elevatum*), consisting of :math:`20 \times 3 = 60` triangular facets, 90 edges, and :math:`12 + 20 = 32` vertices. In Luca Pacioli's *De Divina Proportione* (1509), this stellated star solid is illustrated in **Tabula XXV (Folio 0239)** as *Icosahedron Elevatum Solidum* and in **Tabula XXVI (Folio 0241)** as *Icosahedron Elevatum Vacuum* (genus :math:`g = 59`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0239.g1.png
          :align: center
          :alt: Tabula XXV (Folio 0239) - Icosahedron Elevatum Solidum

          **Tabula XXV (Folio 0239)**: *Icosahedron Elevatum Solidum*.
     - .. figure:: plates/0241.g1.png
          :align: center
          :alt: Tabula XXVI (Folio 0241) - Icosahedron Elevatum Vacuum

          **Tabula XXVI (Folio 0241)**: *Icosahedron Elevatum Vacuum*.

Icosahedral Stellation & Polyhedral Lattices
--------------------------------------------

The triakis icosahedron represents the stellation of the icosahedron and the Catalan dual of the truncated dodecahedron.

In Tabula XXV, Leonardo renders the sixty triangular facets with rhythmic light and shade, conveying the stellated points protruding into surrounding space.

In Tabula XXVI, the hollow framework represents one of Leonardo's most demanding woodcuts: 60 triangular window apertures framed by 90 wooden lattice beams meeting at 32 vertices, producing a vacuate manifold of topological genus :math:`g = 59`.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow elevated icosahedron framework satisfies:

- **Base Solid Invariants**: :math:`V = 32`, :math:`E = 60`, :math:`F = 60` triangular facets
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(32) + 4(60) = 304`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(60) = 720`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(60) = 360` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 304 - 720 + 360 = -56`
- **Topological Genus**: :math:`g = F - 1 = 60 - 1 = 59`
- **Coordinate Field**: Quadratic extension field :math:`\mathbb{Q}(\phi)`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}(\phi)`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Icosahedron Elevatum </solids/04-elevated/icosahedron-elevatum/index>`
