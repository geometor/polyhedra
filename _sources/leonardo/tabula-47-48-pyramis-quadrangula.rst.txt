:layout: book
:type: plate
:order: 19
:title: Tabulae XLVII–XLVIII: Pyramis Quadrangula Solida et Vacua (1509)
:featured_image: leonardo/plates/0283.g1.png
:featured_image_alt: Leonardo da Vinci Tabula XLVII Folio 0283 - Pyramis Laterata Quadrangula Solida
:categories: leonardo-1509, pyramids
:tags: pacioli, woodcut, solidum, vacuum, square-pyramid, pyramis-quadrangula, pyramids
:excerpt: Leonardo da Vinci's woodcut pair illustrating the Square-Based Pyramid (Pyramis Laterata Quadrangula), uniting Euclidean solid geometry with Renaissance perspective, rendered as an opaque solid and as an open wooden framework of genus g = 4.

================================================================
Tabulae XLVII–XLVIII: Pyramis Quadrangula Solida et Vacua (1509)
================================================================

*The Square Pyramid in Solid and Hollow Perspective by Leonardo da Vinci*

.. epigraph::

   *Pyramis laterata quadrangula solida est corpus quinque basibus contentum, quarum una est quadrata et quatuor sunt triangulares...*

   *The solid four-sided pyramid is a body contained by five bases, of which one is square and four are triangular...*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. LXI (Venice, 1509)

.. enunciation::

   The square-based pyramid (*Pyramis Laterata Quadrangula*) possesses 5 vertices, 8 edges, and 5 faces (1 square base and 4 triangular lateral faces). In Luca Pacioli's *De Divina Proportione* (1509), Leonardo da Vinci illustrates this fundamental architectural form in **Tabula XLVII (Folio 0283)** as *Pyramis Laterata Quadrangula Solida* and in **Tabula XLVIII (Folio 0287)** as *Pyramis Laterata Quadrangula Vacua* (genus :math:`g = 4`).

The Paired Folios: Solidum and Vacuum
-------------------------------------

.. list-table::
   :widths: 50 50

   * - .. figure:: plates/0283.g1.png
          :align: center
          :alt: Tabula XLVII (Folio 0283) - Pyramis Laterata Quadrangula Solida

          **Tabula XLVII (Folio 0283)**: *Pyramis Laterata Quadrangula Solida*.
     - .. figure:: plates/0287.g1.png
          :align: center
          :alt: Tabula XLVIII (Folio 0287) - Pyramis Laterata Quadrangula Vacua

          **Tabula XLVIII (Folio 0287)**: *Pyramis Laterata Quadrangula Vacua* (:math:`g = 4`).

Euclidean Architecture & Monumental Form
----------------------------------------

In Euclid's *Elements* Book XI, the pyramid is defined as a solid figure contained by planes that are constructed from one plane to one point. Across architectural history, the square pyramid is the archetype of monumental geometry, seen in the Old Kingdom Great Pyramid of Giza and in Renaissance obelisk finials.

In Tabula XLVII, Leonardo positions the pyramid so that two lateral triangular faces and the square base are visible, with the apex pointing upward and the shading indicating directional sunlight from the upper left.

In Tabula XLVIII, the hollow carpentry framework strips the solid to reveal 5 window apertures (1 square floor and 4 triangular roofs) framed by 8 mitered wooden beams.

Topological Invariants of the Hollow Framework
----------------------------------------------

By the Vacuate Manifold Theorem, the hollow square pyramid framework satisfies:

- **Base Solid Invariants**: :math:`V = 5`, :math:`E = 8`, :math:`F = 5` (1 square, 4 triangles)
- **Hollow Frame Vertices**: :math:`V_{\text{vac}} = 2V + 4E = 2(5) + 4(8) = 42`
- **Hollow Frame Edges**: :math:`E_{\text{vac}} = 12E = 12(8) = 96`
- **Hollow Frame Faces**: :math:`F_{\text{vac}} = 6E = 6(8) = 48` planar trapezoids
- **Euler Characteristic**: :math:`\chi_{\text{vac}} = 42 - 96 + 48 = -6`
- **Topological Genus**: :math:`g = F - 1 = 5 - 1 = 4`
- **Coordinate Field**: Pure rational field :math:`\mathbb{Q}` (or :math:`\mathbb{Q}(\sqrt{\phi})` for the Kepler Golden Pyramid)

Canonical Solid Codex
---------------------

For interactive 3D models, exact symbolic coordinates, face normals, and dihedral angles of square pyramids, consult the canonical pyramid codices:

- :doc:`Kepler Golden Pyramid </solids/05-pyramids/kepler-pyramid/index>`
- :doc:`Seked Great Pyramid </solids/05-pyramids/seked-pyramid/index>`
