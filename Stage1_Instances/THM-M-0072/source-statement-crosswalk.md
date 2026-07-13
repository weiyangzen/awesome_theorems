# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:533-538` supplies exactly the title `汤普森转移引理`, attribution
to John Thompson, the year 1964, the gloss `关于群局部性质与整体性质的关系` ("about the relation
between local and global properties of groups"), high importance, and status `已验证`. Git history
attributes all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
The record contains no bibliography, theorem locator, formula, definitions, ordered binders,
hypotheses, conclusion, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:2082-2105` repeats the same gloss and explicitly leaves the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only as
untrusted metadata and resets this theorem to `L0 / rework_required`.

## Primary source lead

John G. Thompson, *Nonsolvable finite groups all of whose local subgroups are solvable*, Bulletin of
the American Mathematical Society 74 (1968), 383-437, DOI
`10.1090/S0002-9904-1968-11953-6`, was inspected in the AMS-hosted scan. Lemma 5.38(a)(i), printed
page 411, states:

> Suppose G is a finite group of even order with no subgroup of index 2. Let S be a Sylow
> 2-subgroup of G and let M be a maximal subgroup of S. Then each involution of S has a G-conjugate
> in M.

The source immediately proves the result by transfer from `G` to `S/M`: the image of an involution
is the nontrivial coset, the Sylow index is odd, and the transfer product over fixed cosets forces a
conjugate into `M`. The observed 55-page AMS PDF has SHA-256
`93f494417422c31b1bd5a5bd92f3741b7a41bbd8f1581b224d0a5459bc5da83d`.

This is a pinpoint primary mathematical proof source, but it is not yet accepted as `H0`. The
catalog does not cite it, its catalog year is 1964 rather than the publication year 1968, no
independent reviewer has approved the title-to-clause identity, and incorporated notation,
corrections, errata, and preservation have not completed the rev-5.6 source gate. Parts (a)(ii) and
(b) are additional consequences in the same numbered lemma; the target title does not itself say
whether it denotes only (a)(i) or the full package.

The date 1964 may reflect a conflation with Thompson's distinct paper *Normal p-complements for
finite groups*, Journal of Algebra 1 (1964), 43-46, DOI `10.1016/0021-8693(64)90006-7`. That paper
belongs to the normal-complement theorem family; a date coincidence cannot replace the pinpoint
1968 transfer/conjugacy clause or resolve the catalog identity.

## Eponym and formulation witness

Justin Lynd, *The Thompson-Lyons transfer lemma for fusion systems*, arXiv `1303.5996v2`, later
Bulletin of the London Mathematical Society 46 (2014), 1276-1282, DOI
`10.1112/blms/bdu083`, was inspected. Its introduction explicitly calls Thompson's Lemma 5.38 the
"classical Thompson transfer lemma" and gives the common formulation for a 2-perfect group: if
`S` is a Sylow 2-subgroup, `T` is maximal in `S`, and `u` is an involution in `S - T`, then `u` has
a group conjugate in `T`. The immutable arXiv v2 PDF has SHA-256
`eec187eea45d76cc424f43173e057d13398f72276f6253ce3fb491a3e8a6f9c8`.

Lynd supplies strong eponym and terminology evidence, but his paper proves a fusion-system
generalization, not the original group lemma as this repository's root. His restricted `u ∉ T`
form is the nontrivial part of Thompson's universal statement; the statement phase must preserve
the printed root or add a checked relationship rather than treating the two wordings as identical
by name alone.

## Clause crosswalk

| Repository or source component | Mathematical meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "finite group of even order" | finite group whose cardinality is even | `[Group G]`, `[Finite G]`, `Even (Nat.card G)` | primary-source premise located; exact encoding open |
| "no subgroup of index 2" / "2-perfect" | every subgroup has index different from two | `∀ H : Subgroup G, H.index ≠ 2` | do not substitute the stronger `Group.IsPerfect` |
| Sylow 2-subgroup `S` | maximal 2-subgroup of `G` | `S : Sylow 2 G` | pinned interface elaborated |
| maximal subgroup `M < S` | maximal proper element of the subgroup lattice of `S` | `M : Subgroup S`, `IsCoatom M` | representation plausible; source transport open |
| involution `u ∈ S` | element of order exactly two | `u : S`, `orderOf u = 2` | identity exclusion is carried by exact order |
| `G`-conjugate in `M` | some element of `M`, coerced to `G`, is conjugate to `u` in `G` | `∃ m : M, IsConj (u : G) ((m : S) : G)` | conjugation orientation and coercions must be frozen |
| Lynd's `u ∈ S - M` | nontrivial restricted formulation | `u ∉ M` | absent from printed universal clause; alternate-form relationship required |
| parts (a)(ii), (b) | centralizer and elementary-2-group consequences | separate possible obligations or out of scope | target boundary unresolved |
| catalog `已验证` | untrusted inventory status | receipts would be required | no H or M credit |

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.GroupTheory.Transfer` contains `MonoidHom.transfer` and its explicit computation, plus
Burnside's normal `p`-complement theorem `MonoidHom.ker_transferSylow_isComplement'` under a
normalizer-centralizer hypothesis. `Mathlib.GroupTheory.Focal` contains `Subgroup.transferFocal`
and `Subgroup.commutator_inf_eq_focalSubgroup`. General APIs cover `Sylow`, `Subgroup.index`,
`IsCoatom`, `orderOf`, and `IsConj`.

A bounded case-insensitive search over pinned mathlib and repo-local Lean found no Thompson-named
declaration, no `2-perfect` or `p-perfect` predicate, and no exact theorem concluding conjugacy into
a maximal subgroup of a Sylow 2-subgroup. The available transfer and focal results are substantive
proof substrate and justify provisional `M3`; they do not close or replace the source theorem.

## Source gate

Before the canonical claim is frozen, accountable reviewers must approve that this catalog title
denotes Thompson 1968 Lemma 5.38(a)(i), resolve the catalog's 1964/1968 conflict and full-lemma
boundary, preserve and audit the source and errata, map each definition and premise, and decide
whether the universal printed statement or restricted modern form is primary. Only the statement
phase may then freeze a minimal-import Lean expression, expression and environment fingerprints,
checked alternate transports, and the required removed-hypothesis, changed-domain, binder-scope,
and boundary mutations.
