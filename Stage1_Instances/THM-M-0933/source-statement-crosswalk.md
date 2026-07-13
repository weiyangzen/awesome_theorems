# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6819-6824` supplies exactly the title `Olson定理`, John Olson,
1969, gloss `有限阿贝尔群的Davenport常数`, importance `高`, and status `已验证`. Git history
attributes all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
The entry contains no formula, definition of the Davenport constant, group subclass, sequence
model, binders, hypotheses, conclusion, bibliography, proof locator, correction history, reviewer,
or formal artifact.

`Docs/Stage0_Blueprint.md:25444-25469` repeats the gloss while explicitly leaving definitions and
premises, proof route, dependencies, alternate forms, axioms, machine state, and artifact links
open. The rev-5.6 manifest records rank 1472, `L0 / rework_required`, `planned`, no legacy slot,
and `theorem_complete: false`; its `已验证` field is explicitly untrusted.

## Inspected source leads

David J. Grynkiewicz, *A Generalization of the Chevalley-Warning and Ax-Katz Theorems with a View
Towards Combinatorial Number Theory*, arXiv:2208.12895v1 (26 August 2022), was inspected from its
32-page PDF (380049 bytes, SHA-256
`7a6806ca2a5675d75c2e024faf8acc35a029bee6ce4b1889e1d77a3980ea4bb4`).

- PDF page 5 defines `D(G)` as the minimum length forcing a nontrivial/nonempty zero-sum
  subsequence, defines `D*(G) = 1 + sum_i (n_i - 1)` after writing
  `G = (Z/n1Z) x ... x (Z/nrZ)` with `n1 | ... | nr`, and states Theorem 1.5:
  `If G is a finite abelian p-group, then D(G) = D*(G)`.
- The text calls this a classical result of Olson and also van Emde Boas-Kruyswijk, and says both
  original proofs used ideals and group algebras.
- PDF pages 17-18 give a proof: the standard basis sequence gives the lower bound; Proposition 3.1
  contradicts the assumption that a sequence of length `D*(G)` is zero-sum-free, giving the upper
  bound.
- Reference [35] pinpoints J. E. Olson, *A Combinatorial Problem on Finite Abelian Groups I*,
  *Journal of Number Theory* 1 (1969), 8-10.

Crossref confirms John E. Olson, January 1969, volume 1 issue 1, pages 8-10, DOI
`10.1016/0022-314X(69)90021-3`. Elsevier metadata confirms the same PII and open-archive status.
CORE's publisher record gives the abstract: for a finite abelian group, find the least `s` such
that every length-`s` sequence has a subsequence whose product is one; "This question is answered
for p-groups." The original full text was not successfully retrieved in this worker run, so its
exact notation, theorem numbering, proof body, premises, and any correction history were not
inspected.

This supports provisional `H1`, not `H0`: a complete modern proof and a pinpointed primary-source
lead exist, but the uncited catalog does not select the p-group equality over other Olson results,
the original proof was not audited, and exact source-to-root identity, premise mapping,
corrections/errata, and independent review remain open.

Two further published modern cross-checks make the ambiguity explicit. Benjamin Girard,
*An Asymptotically Tight Bound for the Davenport Constant*, *Journal de l'Ecole polytechnique -
Mathematiques* 5 (2018), 605-611, DOI `10.5802/jep.79`, defines `D(G)` as the least positive
length forcing a nonempty zero-sum subsequence and states that the standard lower bound is exact
for p-groups by Olson Part I, but for rank at most two by Corollary 1.1 of Olson Part II. Guoqing
Wang, *A Generalization of Kruyswijk-Olson Theorem on Davenport Constant in Commutative
Semigroups*, *AIMS Mathematics* 5(4) (2020), 2992-3001, DOI `10.3934/math.2020193`, prints the
rank-two result as Theorem A and the p-group result as Theorem B, citing Parts II and I
respectively. These are corroborating secondary sources, not a substitute for the primary scan.

## Clause crosswalk

| Catalog/source phrase | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| finite abelian group | additive commutative group plus finiteness | `[AddCommGroup G] [Finite G]` or explicit decomposition | catalog does not select all finite abelian groups versus p-groups/rank two |
| Davenport constant | least forcing length | a future definition over `Multiset G`, `List G`, or another sequence type | definition absent from catalog and pinned mathlib |
| p-group | every invariant factor has prime-power order | `IsPGroup p (Multiplicative G)` or explicit `ZMod (p ^ e i)` decomposition | strong source candidate, not catalog-selected root |
| `D*(G)` | `1 + sum_i (n_i - 1)` for a decomposition | finite sum over checked invariant factors | decomposition invariance and boundary conventions need proof |
| zero-sum subsequence | nonempty subobject whose sum is zero | `t <= s`, `t != 0`, `t.sum = 0` for multisets | adjacent APIs exist; no Davenport theorem located |
| equality | lower construction plus upper forcing result | two inequalities or exact equality after definitions | proof architecture not frozen |
| Olson / 1969 | historical attribution | source ledger only | DOI and pages confirmed; original body not audited |
| `已验证` | untrusted inventory value | accepted source and kernel receipts would be required | no H0 or M0 credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded
case-insensitive searches of repository-local and pinned mathlib Lean found no declaration named
for Olson, the Davenport constant, zero-sum-free sequences, or the p-group Davenport equality.
Mathlib does provide adjacent substrate:

| Module/declaration | Role | Boundary |
|---|---|---|
| `Mathlib.GroupTheory.FiniteAbelian.Basic`; `AddCommGroup.equiv_directSum_zmod_of_finite` | finite abelian group decomposition | does not define or evaluate `D(G)` |
| `Mathlib.GroupTheory.PGroup`; `IsPGroup`, `IsPGroup.iff_card` | multiplicative p-group predicate and finite-cardinality characterization | not the additive Olson theorem |
| `Mathlib.Algebra.BigOperators.Group.Multiset.Basic`; `Multiset.sum` | additive sum of a multiset | no nonempty zero-sum forcing bound |
| core multiset APIs; `Multiset.card`, `Multiset.card_le_card` | sequence length and submultiset monotonicity | no Davenport constant |
| `Mathlib.Combinatorics.Additive.ErdosGinzburgZiv`; `ZMod.erdos_ginzburg_ziv_multiset` | a pinned zero-sum theorem with prescribed length | different target owned by `THM-M-0931` |

`IntakeProbe.lean` authenticates these names and types in the existing pinned environment. It does
not define the Davenport constant, state a candidate Olson equality, or prove the repository root.
The truthful machine classification is `M4`.

## Remaining statement and source gate

Independent reviewers must select one exact Olson proposition, admit a source, map every
definition, binder, premise, conclusion, proof boundary, correction, and degenerate case, and then
freeze a mutation-tested Lean expression with checked transports. Until that happens, the p-group,
rank-two, and `(Z/nZ)^2` formulas are uncredited candidates rather than a broadened or substituted
theorem.
