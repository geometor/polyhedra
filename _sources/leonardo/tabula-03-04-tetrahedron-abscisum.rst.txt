:layout: book
:type: plate
:order: 2
:title: Tabulae III–IIII: Tetrahedron Abscisum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0191.g1.png
:featured_image_alt: Leonardo da Vinci Tabula III Folio 0191 - Tetrahedron Abscisum Solidum
:categories: leonardo-1509, archimedean
:tags: pacioli, woodcut, solidum, vacuum, truncated-tetrahedron, tetrahedron-abscisum, archimedean-solids
:excerpt: Leonardo da Vinci's woodcut pair depicting the Truncated Tetrahedron (Tetrahedron Abscisum), obtained by rational vertex cutting at t = 1/3, presenting both the solid faceted body and the genus g = 7 hollow lattice framework.

===============================================================
Tabulae III–IIII: Tetrahedron Abscisum Solidum et Vacuum (1509)
===============================================================

*The Truncated Tetrahedron in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Tetrahedron abscisum solidum est quando a quolibet angulo tetrahedri abscinditur portio unius tertiae partis uniuscuiusque lateris...*

   *The solid truncated tetrahedron is when from each angle of the tetrahedron a portion of one-third part of each edge is cut away...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. XXVII (Venice, 1509)

.. enunciation::

   By truncating each of the 4 vertices of the regular tetrahedron at rational edge parameter :math:`t = 1/3`, the vertices are replaced by 4 equilateral triangular facets, while the 4 original triangles are truncated into 4 regular hexagons. Leonardo da Vinci illustrates the resulting Archimedean semi-regular solid in **Tabula III (Folio 0191)** as *Tetrahedron Abscisum Solidum* and in **Tabula IIII (Folio 0193)** as *Tetrahedron Abscisum Vacuum* (genus :math:`g = 7`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0191.g1.png
          :align: center
          :alt: Tabula III (Folio 0191) - Tetrahedron Abscisum Solidum

          **Tabula III (Folio 0191)**: *Tetrahedron Abscisum Solidum*.
     - .. figure:: plates/0193.g1.png
          :align: center
          :alt: Tabula IIII (Folio 0193) - Tetrahedron Abscisum Vacuum

          **Tabula IIII (Folio 0193)**: *Tetrahedron Abscisum Vacuum*.

Archimedean Truncation & Wooden Carpentry
-----------------------------------------

The truncated tetrahedron represents the simplest Archimedean semi-regular solid. In Pacioli's Latin nomenclature, truncation is termed *abscisio* (from *abscindere*, to cut off).

In Tabula III, Leonardo renders the eight faces with clear textural differentiation: the hexagonal faces retain their broad diagonal hatching, while the smaller triangular corner facets present subtle chiaroscuro gradations.

In Tabula IIII, the hollow carpentry lattice creates a through-hole at every face: 4 triangular windows and 4 hexagonal windows. Looking through any hexagonal aperture reveals the inner faces of opposite wooden frame members.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow lattice satisfies:

- **Base Solid Invariants**: :math:`V = 12`, :math:`E = 18`, :math:`F = 8` (4 triangles, 4 hexagons)
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(12) + 4(18) = 96`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(18) = 216`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(18) = 108` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 96 - 216 + 108 = -12`
- **Topological Genus**: :math:`g = F - 1 = 8 - 1 = 7`
- **Coordinate Field**: Pure rational field :math:`\mathbb{Q}`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Truncated Tetrahedron </solids/02-archimedean/truncated-tetrahedron/index>`
