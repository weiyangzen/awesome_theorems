# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:277-282` records only:

- title: `阿廷-韦德尔本定理`;
- attribution: Emil Artin / Joseph Wedderburn;
- year: 1927;
- gloss: `中心单代数的分类` ("classification of central simple algebras");
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:1100-1125` repeats the
catalogue identity while explicitly leaving exact definitions and premises, proof route,
equivalent formulations, axioms, machine status, and formal artifact links open. These records
establish catalogue provenance only.

## Historical source lead

The year and Artin attribution point toward Emil Artin, *Zur Theorie der hyperkomplexen Zahlen*,
Abhandlungen aus dem Mathematischen Seminar der Universitaet Hamburg 5 (1927), 251-260, DOI
`10.1007/BF02952526`. This is a bibliographic discovery lead only. This intake has not pinned and
reviewed an immutable copy, located and translated the exact theorem and definition passages,
mapped its hypotheses and proof nodes, reconciled Wedderburn's earlier work and the catalogue's
joint attribution, audited corrections or errata, or obtained independent review. It supplies no
E4/H0 evidence and selects no canonical formulation.

## Component crosswalk

| Repository/source element | Prospective mathematical meaning | Prospective Lean component | Intake status |
|---|---|---|---|
| central simple algebra | finite-dimensional associative unital algebra over a field, simple as a ring and with center equal to the base | `A : CSA K`, or explicit `[Algebra K A] [Algebra.IsCentral K A] [IsSimpleRing A] [Module.Finite K A]` | Bundled versus explicit domain, finite-dimensional convention, and source definition are open |
| classification | matrix normal form over a division algebra | `Nonempty (A ≃ₐ[K] Matrix (Fin n) (Fin n) D)` | Existence direction is plausible but not source-selected |
| matrix size | a positive integer degree | `(n : Nat)` with `[NeZero n]` | Exact data and boundary conventions open |
| division-algebra representative | a division algebra finite over the base, possibly central | `[DivisionRing D] [Algebra K D] [Module.Finite K D]` and perhaps `[Algebra.IsCentral K D]` | Pinned finite candidate does not visibly include output centrality |
| classification strength | possible uniqueness of `D` and `n`, or an iff characterization | no accepted candidate | Catalogue does not say whether uniqueness or converse belongs to the root |

## Formal discovery candidates

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.RingTheory.SimpleModule.WedderburnArtin` exposes
`IsSimpleRing.exists_algEquiv_matrix_divisionRing` and
`IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite`. The latter requires a commutative
semiring base, an Artinian simple algebra finite as a module over the base, and yields an algebra
equivalence to a positive-size matrix algebra over a division algebra finite over the base.

`Mathlib.Algebra.BrauerGroup.Defs` exposes `CSA K`, bundling centrality, simplicity, and finite
dimension over a field. The foreign legacy declaration
`AwesomeTheorems.Stage1.S1_M_078.csa_wedderburn_artin_finite` combines that domain with the pinned
finite theorem. These exact declarations are valuable discovery inputs, but no one of them is
accepted as the catalogue's root: source identity, expression serialization, checked transport,
terminal proof-body provenance, transitive dependencies, and trust remain downstream work.

## Neighbor partition and open mapping

`THM-M-0027` owns the arbitrary semisimple-ring product structure theorem. `THM-M-0037` and
`THM-M-0424` concern Brauer classification of central simple algebras up to stable matrix
equivalence and related group structure. This target cannot absorb or borrow their statements or
evidence.

The statement phase must select one exact source assertion and map every domain, binder,
hypothesis, conclusion, and degenerate case to one elaborated Lean expression. The source audit
must then pin the edition or scan, provide theorem/page/definition/proof-node and errata crosswalks,
and obtain independent review. Until then the family supports H1 and the pinned interfaces support
M3 only; no H0 or machine closure is claimed.
