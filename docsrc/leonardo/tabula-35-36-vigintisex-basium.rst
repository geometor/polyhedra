:layout: book
:type: plate
:order: 18
:title: Tabulae XXXV–XXXVI: Vigintisex Basium Planum Solidum et Vacuum (1509)
:featured_image: leonardo/plates/0259.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XXXV Folio 0259 - Vigintisex Basium Planum Solidum
:categories: leonardo-1509, archimedean
:tags: pacioli, woodcut, solidum, vacuum, rhombicuboctahedron, vigintisex-basium, archimedean-solids
:excerpt: Leonardo da Vinci's architectural climax of the 1509 De Divina Proportione, the 26-Base Body (Vigintisex Basium / Rhombicuboctahedron), celebrated for Pacioli's giant 1489 suspended model in Venice, rendered in solid form and as a genus g = 25 wooden cage.

=====================================================================
Tabulae XXXV–XXXVI: Vigintisex Basium Planum Solidum et Vacuum (1509)
=====================================================================

*The 26-Base Body (Rhombicuboctahedron) in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Questo nobilissimo corpo de 26 base fu per noi prima composto in la inclita cita de Venetia ne li anni del nostro Signore 1489... E fu suspenso in alto in una bella sala appresso la chiesa de San Marco, dove concorse quasi tutta la cita ad admirarlo, maestri de legname, muratori, et architetti con grandissimo stupore della sua armonia e leggerezza...*

   *This most noble body of 26 bases was first constructed by us in the renowned city of Venice in the year of our Lord 1489... And it was suspended aloft in a beautiful hall near the church of San Marco, where almost the entire city came together to marvel at it—master carpenters, masons, and architects with the greatest wonder at its harmony and lightness...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. LI (Venice, 1509)

.. enunciation::

   The **26-Base Body** (*Vigintisex Basium*), known in modern geometry as the Archimedean **Rhombicuboctahedron**, consists of 26 faces (8 equilateral triangles and 18 squares: 6 axial squares aligned with the cube and 12 belt squares aligned with the cuboctahedron), 48 edges, and 24 vertices over :math:`\mathbb{Q}(\sqrt{2})`. In Luca Pacioli's *De Divina Proportione* (1509), this architectural climax of the treatise is illustrated by Leonardo da Vinci in **Tabula XXXV (Folio 0259)** as *Vigintisex Basium Planum Solidum* and in **Tabula XXXVI (Folio 0261)** as *Vigintisex Basium Planum Vacuum* (genus :math:`g = 25`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0259.g1.png
          :align: center
          :alt: Tabula XXXV (Folio 0259) - Vigintisex Basium Planum Solidum

          **Tabula XXXV (Folio 0259)**: *Vigintisex Basium Planum Solidum*.
     - .. figure:: plates/0261.g1.png
          :align: center
          :alt: Tabula XXXVI (Folio 0261) - Vigintisex Basium Planum Vacuum

          **Tabula XXXVI (Folio 0261)**: *Vigintisex Basium Planum Vacuum* (:math:`g = 25`).

The Piazza San Marco Sensation (1489)
-------------------------------------

In Chapter LI of *De Divina Proportione*, Pacioli recounts the legendary reception in Venice of the giant hollow model of the 26-base solid crafted by him twenty years prior to the book's publication. Suspended aloft near St. Mark's Basilica, its combination of lightness, structural rigidity, and harmonious proportions drew architects, sculptors, and woodworkers from across northern Italy.

In Tabula XXXV, Leonardo renders the solid rhombicuboctahedron with dramatic spatial presence, emphasizing the eight equilateral triangles nested between the eighteen square facets.

In Tabula XXXVI, the vacuate structure exhibits 26 window apertures framed by 48 wooden boundary beams. By the Vacuate Manifold Theorem, this open carpentry model forms an orientable surface of topological genus :math:`g = 25`.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow 26-base framework satisfies:

- **Base Solid Invariants**: :math:`V = 24`, :math:`E = 48`, :math:`F = 26` (8 triangles, 18 squares)
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(24) + 4(48) = 240`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(48) = 576`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(48) = 288` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 240 - 576 + 288 = -48`
- **Topological Genus**: :math:`g = F - 1 = 26 - 1 = 25`
- **Coordinate Field**: Quadratic extension field :math:`\mathbb{Q}(\sqrt{2})`

Canonical Solid Codex
---------------------

For the complete interactive 3D model, exact symbolic coordinates over :math:`\mathbb{Q}(\sqrt{2})`, face normals, and dihedral angles, consult the canonical solid codex:

- :doc:`Rhombicuboctahedron </solids/02-archimedean/rhombicuboctahedron/index>`
