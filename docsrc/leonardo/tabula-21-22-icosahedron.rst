:layout: book
:type: plate
:order: 11
:title: Tabulae XXI–XXII: Icosahedron Planum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0231.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XXI Folio 0231 - Icosahedron Planum Solidum
:categories: leonardo-1509, platonic
:tags: pacioli, woodcut, solidum, vacuum, icosahedron, platonic-solids, golden-ratio
:excerpt: Leonardo da Vinci's woodcut plates of the regular icosahedron, representing Water in Platonic cosmology, governed by three orthogonal golden rectangles over Q(phi) and presented as a solid body and genus g = 19 wooden cage.

=============================================================
Tabulae XXI–XXII: Icosahedron Planum Solidum et Vacuum (1509)
=============================================================

*The Regular Icosahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Icosahedron planum solidum est corpus viginti basibus triangularibus aequilateris contentum...*

   *The solid plane icosahedron is a body contained by twenty equilateral triangular bases...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXXVI (Venice, 1509)

.. enunciation::

   The regular icosahedron :math:`\{3, 5\}` is composed of 20 equilateral triangular faces, 30 edges, and 12 vertices defined by three mutually perpendicular golden rectangles over :math:`\mathbb{Q}(\phi)`. Leonardo da Vinci illustrates this Platonic solid in **Tabula XXI (Folio 0231)** as *Icosahedron Planum Solidum* and in **Tabula XXII (Folio 0233)** as *Icosahedron Planum Vacuum*. In vacuate form, the 20 triangular window apertures form a wooden framework of topological genus :math:`g = F - 1 = 19`, the highest among the five Platonic solids.

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0231.g1.png
          :align: center
          :alt: Tabula XXI (Folio 0231) - Icosahedron Planum Solidum

          **Tabula XXI (Folio 0231)**: *Icosahedron Planum Solidum*.
     - .. figure:: plates/0233.g1.png
          :align: center
          :alt: Tabula XXII (Folio 0233) - Icosahedron Planum Vacuum

          **Tabula XXII (Folio 0233)**: *Icosahedron Planum Vacuum* (:math:`g = 19`).

Water Cosmology & The Three Golden Rectangles
---------------------------------------------

In Plato's *Timaeus* (55b), the icosahedron represents **Water** (*Aqua*), possessing the greatest number of faces and the smoothest rolling mobility among the four terrestrial elements.

Algebraically, the icosahedron cannot be embedded over the rational field :math:`\mathbb{Q}`: its 12 vertices are defined by three mutually perpendicular **golden rectangles** having aspect ratio :math:`1 : \phi`:

.. math::

   (0, \pm 1, \pm \phi), \quad (\pm 1, \pm \phi, 0), \quad (\pm \phi, 0, \pm 1)

In Tabula XXI, Leonardo showcases the sphere-like curvature of the 20 triangular facets with subtle parallel hatching.

In Tabula XXII, Leonardo hollows out each facet into mitered wooden frames. The central cavity exposes the complex web of converging beams, where every window reveals the antipodal faces with perfect perspective depth.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow icosahedron framework satisfies:

- **Base Solid Invariants**: :math:`V = 12`, :math:`E = 30`, :math:`F = 20` equilateral triangular faces
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(12) + 4(30) = 144`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(30) = 360`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(30) = 180` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 144 - 360 + 180 = -36`
- **Topological Genus**: :math:`g = F - 1 = 20 - 1 = 19`
- **Coordinate Field**: Quadratic extension field :math:`\mathbb{Q}(\phi)`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}(\phi)`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Regular Icosahedron </solids/01-platonic/icosahedron/index>`
