:layout: book
:type: plate
:order: 20
:title: Tabulae LI–LII: Pyramis Penthagona Solida et Vacua (1509)
:featured_image: leonardo/plates/0293.g1.png
:featured_image_alt: Leonardo da Vinci Tabula LI Folio 0293 - Pyramis Laterata Penthagona Solida
:categories: leonardo-1509, pyramids
:tags: pacioli, woodcut, solidum, vacuum, pentagonal-pyramid, pyramis-penthagona, johnson-solids, pyramids
:excerpt: Leonardo da Vinci's woodcut pair of the Regular Pentagonal Pyramid (Pyramis Laterata Penthagona / Johnson Solid J2), governed by the golden ratio in its pentagonal base, shown in solid perspective and as a hollow wooden lattice of genus g = 5.

=============================================================
Tabulae LI–LII: Pyramis Penthagona Solida et Vacua (1509)
=============================================================

*The Pentagonal Pyramid in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Pyramis laterata penthagona solida est corpus sex basibus contentum, quarum una est penthagonalis et quinque sunt triangulares...*

   *The solid five-sided pyramid is a body contained by six bases, of which one is pentagonal and five are triangular...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. LXV (Venice, 1509)

.. enunciation::

   The regular pentagonal pyramid (*Pyramis Laterata Penthagona*), classified in modern geometry as the **Johnson Solid** :math:`J_2`, possesses 6 vertices, 10 edges, and 6 faces (1 regular pentagonal base and 5 equilateral triangular lateral faces). Because its base is a regular pentagon, its proportions are intrinsically governed by the golden ratio :math:`\phi`. In Luca Pacioli's *De Divina Proportione* (1509), Leonardo da Vinci illustrates this body in **Tabula LI (Folio 0293)** as *Pyramis Laterata Penthagona Solida* and in **Tabula LII (Folio 0295)** as *Pyramis Laterata Penthagona Vacua* (genus :math:`g = 5`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0293.g1.png
          :align: center
          :alt: Tabula LI (Folio 0293) - Pyramis Laterata Penthagona Solida

          **Tabula LI (Folio 0293)**: *Pyramis Laterata Penthagona Solida*.
     - .. figure:: plates/0295.g1.png
          :align: center
          :alt: Tabula LII (Folio 0295) - Pyramis Laterata Penthagona Vacua

          **Tabula LII (Folio 0295)**: *Pyramis Laterata Penthagona Vacua* (:math:`g = 5`).

The Golden Pyramid & Johnson Solid J₂
-------------------------------------

When the lateral faces of the pentagonal pyramid are equilateral triangles, the pyramid is an apex cap of the regular icosahedron: removing one vertex and its five incident triangles from a regular icosahedron leaves a pentagonal antiprism, while the removed cap is precisely :math:`J_2`.

In Tabula LI, Leonardo captures the five-fold symmetry of the converging lateral edges, using cross-hatching to model the sloping surfaces of the equilateral facets.

In Tabula LII, the hollow carpentry lattice creates 6 window openings (1 pentagonal base and 5 triangular roofs) bordered by 10 mitered wooden rails. By the Vacuate Manifold Theorem, this hollow structure forms an orientable surface of topological genus :math:`g = 5`.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow pentagonal pyramid framework satisfies:

- **Base Solid Invariants**: :math:`V = 6`, :math:`E = 10`, :math:`F = 6` (1 pentagon, 5 triangles)
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(6) + 4(10) = 52`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(10) = 120`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(10) = 60` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 52 - 120 + 60 = -8`
- **Topological Genus**: :math:`g = F - 1 = 6 - 1 = 5`
- **Coordinate Field**: Quadratic extension field :math:`\mathbb{Q}(\phi)`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}(\phi)`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Regular Pentagonal Pyramid </solids/05-pyramids/pentagonal-pyramid/index>`
