# Source-statement crosswalk

## Repository source

`Docs/Stage0_Blueprint.md:14793-14796` names `THM-M-0540` as "奇异同调" and describes its content as
"拓扑空间的奇异同调" (the singular homology of a topological space). It classifies the record as a
mathematical theorem/proposition and labels formal verifiability as verified, but supplies neither
a proposition nor definitions, assumptions, source theorem, or proof. The rev-5.6 manifest carries
the same untrusted label. Neither label supplies H0 or machine-proof credit.

## Candidate primary and standard sources

- Samuel Eilenberg, "Singular Homology Theory," *Annals of Mathematics*, second series, volume 45,
  number 3 (1944), pages 407-447. This is the historical primary-source candidate suggested by the
  Stage0 date and attribution. Exact definitions/theorem anchors, coefficient conventions, and
  errata have not yet been inspected and independently reviewed.
- Allen Hatcher, *Algebraic Topology* (2002), Chapter 2, Section 2.1, "Simplicial and Singular
  Homology," is a stable modern construction and proof source candidate. Exact page-level mapping,
  edition fingerprint, conventions, and errata remain open.

These citations are discovery anchors only. Before H0, the anchor-audit phase must inspect an
immutable copy, record pinpoint pages and statements, map every assumption to formal binders, map
the proof/construction to obligation nodes, check errata, and obtain independent review.

## Crosswalk

| Repository component | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "topological space" | arbitrary space `X` | `X : Type` with `[TopologicalSpace X]`, passed as `TopCat.of X` | frozen for small spaces |
| "singular simplex" | continuous map from standard `q`-simplex to `X` | mathlib singular-set simplex model | included; exact type open |
| singular chains | free integral chains on singular simplices | `singularChainComplexFunctor (ModuleCat ℤ)` at `ModuleCat.of ℤ ℤ` | canonical left construction frozen |
| boundary | alternating sum of face restrictions | inherited from `SSet.singularChainComplexFunctor` / alternating face-map complex | construction convention frozen |
| "homology" | cycles modulo boundaries in degree `n` | `singularHomologyFunctor (ModuleCat ℤ) n` | canonical result frozen |
| continuous map | induced chain map and homology map | functorial `map` | included; exact formal conclusion open |

## Existing Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.AlgebraicTopology.SingularHomology.Basic` defines `SSet.singularChainComplexFunctor`,
`singularChainComplexFunctor`, and `singularHomologyFunctor`. `IntakeProbe.lean` checks that these
names elaborate in the repository toolchain. This establishes credible interface-level formal
material (`M3`), not exact-root closure: no canonical theorem expression, terminal proof body,
transitive provenance, axiom report, or source equivalence has been audited.

The statement phase chooses the construction identity in `Statement.lean`, with a checked direct
encoding transport and negative mutations. This is still interface-level `M3`: the definitional
witness establishes coherent elaboration and must not be credited as proof-phase closure or as all
mathematical properties ordinarily bundled under "singular homology."
