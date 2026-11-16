:layout: book
:type: plate
:order: 3
:title: Tabulae V–VI: Tetrahedron Elevatum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0195.g1.png
:featured_image_alt: Leonardo da Vinci Tabula V Folio 0195 - Tetrahedron Elevatum Solidum
:categories: leonardo-1509, elevated
:tags: pacioli, woodcut, solidum, vacuum, tetrahedron-elevatum, triakis-tetrahedron, elevated-solids
:excerpt: Leonardo da Vinci's woodcut pair depicting the Triakis Tetrahedron (Tetrahedron Elevatum), formed by erecting equilateral triangular pyramids on the four triangular facets of the tetrahedron, producing a 12-face stellated solid and hollow cage of genus g = 11.

===============================================================
Tabulae V–VI: Tetrahedron Elevatum Solidum et Vacuum (1509)
===============================================================

*The Triakis Tetrahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Tetrahedron elevatum solidum est quando super qualibet eius quatuor basium erigitur una pyramis triangularis...*

   *The solid elevated tetrahedron is when upon each of its four bases a triangular pyramid is erected...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXVIII (Venice, 1509)

.. enunciation::

   By erecting triangular pyramids over each of the 4 faces of a regular tetrahedron, Leonardo da Vinci produces the **Triakis Tetrahedron** (*Tetrahedron Elevatum*). Consisting of :math:`4 \times 3 = 12` triangular faces and :math:`4 + 4 = 8` vertices, this elevated solid is illustrated in **Tabula V (Folio 0195)** as *Tetrahedron Elevatum Solidum* and in **Tabula VI (Folio 0197)** as *Tetrahedron Elevatum Vacuum* (genus :math:`g = 11`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0195.g1.png
          :align: center
          :alt: Tabula V (Folio 0195) - Tetrahedron Elevatum Solidum

          **Tabula V (Folio 0195)**: *Tetrahedron Elevatum Solidum*.
     - .. figure:: plates/0197.g1.png
          :align: center
          :alt: Tabula VI (Folio 0197) - Tetrahedron Elevatum Vacuum

          **Tabula VI (Folio 0197)**: *Tetrahedron Elevatum Vacuum*.

Geometric Elevation & Chiaroscuro Dynamics
------------------------------------------

In Renaissance constructive geometry, stellation was understood as *elevatio*—erecting pyramidal roofs on existing polygonal facets. For the tetrahedron, erecting regular pyramids on all four faces triples the number of exterior facets from 4 to 12.

In Tabula V, Leonardo captures the acute three-dimensional peaks of the four pyramids, handling the cast shadows of the upper pyramids onto the lower facets with masterly perspective accuracy.

In Tabula VI, the hollow lattice cage exposes the interior tetrahedral cavity. Every triangular opening is bordered by mitered wooden frame beams, demonstrating how stellation increases the genus of the vacuate manifold from :math:`g = 3` to :math:`g = 11`.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow elevated framework satisfies:

- **Base Solid Invariants**: :math:`V = 8`, :math:`E = 18`, :math:`F = 12` triangular faces
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(8) + 4(18) = 88`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(18) = 216`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(18) = 108` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 88 - 216 + 108 = -20`
- **Topological Genus**: :math:`g = F - 1 = 12 - 1 = 11`
- **Coordinate Field**: Pure rational field :math:`\mathbb{Q}`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Tetrahedron Elevatum </solids/04-elevated/tetrahedron-elevatum/index>`
