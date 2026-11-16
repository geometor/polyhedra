:layout: book
:type: plate
:order: 4
:title: Tabulae VII–VIII: Exahedron Planum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0199.g1.png
:featured_image_alt: Leonardo da Vinci Tabula VII Folio 0199 - Exahedron Planum Solidum
:categories: leonardo-1509, platonic
:tags: pacioli, woodcut, solidum, vacuum, hexahedron, cube, platonic-solids
:excerpt: Leonardo da Vinci's woodcut plates for the regular hexahedron (cube), embodying Earth in Platonic cosmology, rendered as an opaque six-sided solid and as an open wooden carpentry framework of genus g = 5.

===========================================================
Tabulae VII–VIII: Exahedron Planum Solidum et Vacuum (1509)
===========================================================

*The Regular Hexahedron (Cube) in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Exahedron planum solidum sive cubus est corpus sex basibus quadratis aequilateris et aequiangulis contentum...*

   *The solid plane hexahedron or cube is a body contained by six square equilateral and equiangular bases...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXIX (Venice, 1509)

.. enunciation::

   The regular hexahedron (cube) :math:`\{4, 3\}` possesses 8 vertices, 12 edges, and 6 square faces. Leonardo da Vinci illustrates this fundamental Platonic solid in **Tabula VII (Folio 0199)** as *Exahedron sive Cubus Planum Solidum* and in **Tabula VIII (Folio 0201)** as *Exahedron Planum Vacuum*. Hollowing the 6 square faces transforms the cube into a 2-manifold wooden framework of topological genus :math:`g = F - 1 = 5`.

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0199.g1.png
          :align: center
          :alt: Tabula VII (Folio 0199) - Exahedron Planum Solidum

          **Tabula VII (Folio 0199)**: *Exahedron sive Cubus Planum Solidum*.
     - .. figure:: plates/0201.g1.png
          :align: center
          :alt: Tabula VIII (Folio 0201) - Exahedron Planum Vacuum

          **Tabula VIII (Folio 0201)**: *Exahedron Planum Vacuum* (:math:`g = 5`).

Earth Cosmology & Carpenter Perspective
---------------------------------------

In Plato's *Timaeus* (55d), the cube is the embodiment of **Earth** (*Terra*) because of its immovable stability, right angles, and square foundation.

Leonardo depicts the cube in two-point perspective, tilted slightly forward so that the top square face, the brightly illuminated left face, and the deeply shaded right face are all visible simultaneously.

In Tabula VIII, the hollow framework consists of 12 square beams joined at the 8 cube corners with mitered joints. Looking through the front square aperture reveals the interior faces of the rear, top, bottom, and side frame members, demonstrating Leonardo's complete mastery of spatial recession and light transmission.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow cube framework satisfies:

- **Base Solid Invariants**: :math:`V = 8`, :math:`E = 12`, :math:`F = 6` square faces
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(8) + 4(12) = 64`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(12) = 144`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(12) = 72` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 64 - 144 + 72 = -8`
- **Topological Genus**: :math:`g = F - 1 = 6 - 1 = 5`
- **Coordinate Field**: Pure rational field :math:`\mathbb{Q}`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Regular Hexahedron (Cube) </solids/01-platonic/hexahedron/index>`
