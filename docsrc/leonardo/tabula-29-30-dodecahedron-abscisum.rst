:layout: book
:type: plate
:order: 15
:title: Tabulae XXIX–XXX: Dodecahedron Abscisum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0247.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XXIX Folio 0247 - Dodecahedron Abscisum Solidum
:categories: leonardo-1509, archimedean
:tags: pacioli, woodcut, solidum, vacuum, icosidodecahedron, dodecahedron-abscisum, archimedean-solids
:excerpt: Leonardo da Vinci's woodcut plates of the Icosidodecahedron (Dodecahedron Abscisum), created by edge-midpoint truncation of the dodecahedron to produce 12 pentagons and 20 triangles, paired with its genus g = 31 vacuum cage.

================================================================
Tabulae XXIX–XXX: Dodecahedron Abscisum Solidum et Vacuum (1509)
================================================================

*The Icosidodecahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Dodecahedron abscisum solidum fit quando a singulis viginti angulis dodecahedri abscinditur portio usque ad medietates laterum confluentium...*

   *The solid truncated dodecahedron is made when from each of the twenty angles of the dodecahedron a portion is cut away up to the midpoints of the converging edges...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XL (Venice, 1509)

.. enunciation::

   By truncating the regular dodecahedron at the midpoints of its 30 edges (Pacioli's edge rectification), the 20 vertices become 20 equilateral triangles, while the 12 pentagonal faces are reduced to 12 smaller regular pentagons. The resulting Archimedean semi-regular solid is the **Icosidodecahedron** (:math:`V = 30, E = 60, F = 32`), illustrated by Leonardo da Vinci in **Tabula XXIX (Folio 0247)** as *Dodecahedron Abscisum Solidum* and in **Tabula XXX (Folio 0249)** as *Dodecahedron Abscisum Vacuum* (genus :math:`g = 31`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0247.g1.png
          :align: center
          :alt: Tabula XXIX (Folio 0247) - Dodecahedron Abscisum Solidum

          **Tabula XXIX (Folio 0247)**: *Dodecahedron Abscisum Solidum*.
     - .. figure:: plates/0249.g1.png
          :align: center
          :alt: Tabula XXX (Folio 0249) - Dodecahedron Abscisum Vacuum

          **Tabula XXX (Folio 0249)**: *Dodecahedron Abscisum Vacuum*.

The Icosidodecahedron & Golden Interplay
----------------------------------------

The icosidodecahedron represents the quasi-regular intersection between the icosahedron and the dodecahedron. Every edge is shared by exactly one regular pentagon and one equilateral triangle.

In Tabula XXIX, Leonardo renders the thirty-two planar facets with striking volumetric depth, capturing the contrast between the five-fold pentagons and three-fold triangles.

In Tabula XXX, the hollow wooden framework comprises 32 window reveals (12 pentagonal apertures and 20 triangular apertures) framed by 60 mitered wooden rails. By the Vacuate Manifold Theorem, this carpentry framework possesses topological genus :math:`g = 31`.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow icosidodecahedron framework satisfies:

- **Base Solid Invariants**: :math:`V = 30`, :math:`E = 60`, :math:`F = 32` (12 pentagons, 20 triangles)
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(30) + 4(60) = 300`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(60) = 720`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(60) = 360` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 300 - 720 + 360 = -60`
- **Topological Genus**: :math:`g = F - 1 = 32 - 1 = 31`
- **Coordinate Field**: Quadratic extension field :math:`\mathbb{Q}(\phi)`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}(\phi)`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Icosidodecahedron </solids/02-archimedean/icosidodecahedron/index>`
