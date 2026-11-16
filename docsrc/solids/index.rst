:navigation: header
:order: 1
:nav_title: Solids
:layout: book
:title: Catalog of Polyhedra
:book_title: Catalog of Polyhedra
:book_subtitle: Twenty-Six Exact Symbolic Solids Across Five Geometric Families

====================
Catalog of Polyhedra
====================

*Twenty-Six Exact Symbolic Solids Across Five Geometric Families*

.. epigraph::

   *No other figure can be constructed from equilateral and equiangular plane figures, except these five solids alone.*

   — **Euclid of Alexandria**, *Elements* Book XIII, Proposition 18a (Porism)

.. epigraph::

   *Quinque corpora regularia sunt: tetraedron, exaedron sive cubus, octaedron, icosaedron, et dodecaedron. Quorum quodlibet intra sphaeram comprehendi potest.*

   *There are five regular solids: the tetrahedron, hexahedron or cube, octahedron, icosahedron, and dodecahedron. Every one of them can be comprehended within a sphere.*

   — **Luca Pacioli**, *De Divina Proportione*, Cap. I (Venice, 1509)

The GEOMETOR Polyhedra Canon
----------------------------

The GEOMETOR catalog provides an exact symbolic registry of twenty-six canonical polyhedra across five geometric families. Grounded in 100% exact symbolic algebra with SymPy and Norman Wildberger's 3D Rational Trigonometry, every vertex coordinate, edge quadrance, circumquadrance, and dihedral spread is represented as an exact algebraic number over the integer ring :math:`\mathbb{Z}`, the rational field :math:`\mathbb{Q}`, quadratic extensions :math:`\mathbb{Q}(\sqrt{2})`, the golden field :math:`\mathbb{Q}(\phi)`, or closed-form radical towers. Zero floating-point numbers or approximations are permitted within the core symbolic kernel.

This catalog unites three historic geometric traditions:

1. **The Classical Euclidean and Platonic Foundation**: Euclid's *Elements* Book XIII constructions of the five regular convex solids inside a given sphere (Propositions XIII.13–18).
2. **The Archimedean and Renaissance Synthesis**: Luca Pacioli's *De Divina Proportione* (Venice, 1509), illustrated by Leonardo da Vinci's sixty pearwood block woodcuts depicting both solid opaque forms (*Planum Solidum*) and hollow open-lattice beam frameworks (*Planum Vacuum*).
3. **Modern Rational Trigonometry and Topological Manifolds**: Systematic replacement of transcendental angles and trigonometric functions with exact planar dihedral spreads :math:`s = \sin^2\theta \in \mathbb{Q}`, accompanied by the Vacuate Manifold Theorem establishing the hollow frame genus :math:`g = F - 1`.

The Five Polyhedral Families
----------------------------

.. collection::
   :type: family
   :sort: order

Master Invariant Ledger
-----------------------

For a comprehensive cross-family comparison of all twenty-six solids—including exact number fields, topology :math:`(V, E, F)`, face compositions, edge quadrances, dihedral spreads, hollow vacuum genus :math:`g`, and Leonardo da Vinci 1509 woodcut plates—consult the :doc:`Master Comparative Ledger <comparative_table>`.

.. toctree::
   :hidden:

   comparative_table
