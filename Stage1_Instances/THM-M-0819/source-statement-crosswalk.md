# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6019-6024` supplies exactly the title `Dilworth定理`, attribution
to Robert Dilworth, year 1950, gloss `偏序集分解为链的最小数目` ("the minimum number for
decomposing a partially ordered set into chains"), importance high, and status `已验证`. Git history
places all six uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record does
not say what the minimum equals and gives no domain, definitions, quantifiers, boundary cases,
bibliography, proof boundary, or formal declaration.

`Docs/Stage0_Blueprint.md:22361-22386` repeats the gloss while leaving exact definitions and
premises, proof route, dependency graph, alternate forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Primary statement lead

The inspected source is R. P. Dilworth, *A Decomposition Theorem for Partially Ordered Sets*,
*Annals of Mathematics*, second series, volume 51, number 1 (January 1950), pages 161-166, DOI
`10.2307/1969503`. Crossref confirms the author, title, journal, volume, issue, year, and first page.

A publisher-hosted preview of the 1990 Springer reprint in *The Dilworth Theorems*, DOI
`10.1007/978-1-4899-3558-8_1`, exposes original pages 161-162. The observed 442264-byte PDF has
SHA-256 `6af3f64b82c9788779586fbc43d8fa845b24c3ff8f34414c5518aa3545b78243`.
On original page 161 the paper defines comparable elements, independent and dependent subsets, and
chains. Theorem 1.1 then says: if every `(k + 1)`-element subset of a poset `P` is dependent while
at least one `k`-element subset is independent, then `P` is a set sum of `k` disjoint chains. The
next paragraph proves the necessity of the no-`k + 1`-independent-set clause by the pigeonhole
argument. Section 2 says the proof first handles finite `P` and then obtains the general case by a
transfinite argument.

This precisely identifies the historical statement family and its lower-bound clause. It does not
yet justify `H0`: the lawful preview omits original pages 163-166, the full proof and transfinite
argument were not inspected, correction and errata status are unresolved, and no independent
reviewer has approved a modern equality transport.

## Modern and formal leads

Abhishek Kr. Singh, *Fully Mechanized Proofs of Dilworth's Theorem and Mirsky's Theorem*, arXiv
`1703.06133v1` (2017), states in Section 2.2 that the maximum size of an antichain equals the minimum
number of chains in a chain cover. Section 3.2 displays the Coq declaration `Dilworth`; the associated
immutable Git repository at commit
`74c0cde97967149b7f44b775fabdc7d909760ebd` contains `FiniteDilworth.v`. This is a secondary
source and finite-poset (`FPO U`) cross-system formal lead, not Lean 4 evidence and not repo-local
closure.

Pinned mathlib's curated `docs/1000.yaml` records a 2025 Lean 4 formalization by Vlad Tsyrklevich.
At immutable commit `f82f920f05a381bb1ce5e8903bde33e27f4365b6`,
`MiscLeanProofs/Dilworth.lean` defines `IsChainPartition`, `minChainPartition`, and
`antichainWidth`, then states:

```text
theorem minChainPartition_eq_antichainWidth [PartialOrder alpha] [Finite alpha] :
  minChainPartition alpha (fun x y => x <= y) =
    antichainWidth alpha (fun x y => x <= y)
```

The 674-line source SHA-256 is
`4bc86897588087f472b358830bba157b92994e2b0dd44c66805f57c29211c985`; a textual scan finds no
`sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration. Its lock uses
Lean `v4.28.0-rc1` and mathlib `3234d21e85d1c08e42db46555be77bc3a051a61b`. Direct elaboration
under this repository's Lean 4.29.0 and mathlib `8a178386...` fails at source lines 397, 404, and
597. The failed run reports `sorryAx` for the terminal declarations because Lean recovers from those
errors with holes. The candidate is therefore blocked under the current local closure and supplies
no `M0` or `M1` credit.

## Component crosswalk

| Catalog or source component | Primary meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| partially ordered set `P` | reflexive, antisymmetric, transitive order | `[PartialOrder alpha]`; optionally `[Finite alpha]` | finite type versus arbitrary finite-width carrier open |
| independent set | distinct elements pairwise non-comparable | `IsAntichain (fun x y => x <= y) A` | adjacent pinned definition elaborates |
| chain | every two elements comparable | `IsChain (fun x y => x <= y) C` | adjacent pinned definition elaborates |
| width `k` | some independent `k`-set and no independent `(k+1)`-set | maximum set cardinality or `iSup` of `encard` | definition and attainment transport open |
| set sum of `k` disjoint chains | carrier partitioned into exactly `k` chains | unique-membership family or finite partition predicate | no pinned root definition located |
| minimum chain number | lower bound plus existence of a width-sized partition | `minChainPartition` via `iInf` or a witness/minimality predicate | candidate exists externally but fails current pin |
| primary generality | arbitrary `P` of finite width, general proof uses transfinite argument | likely cardinal/foundation-sensitive target | stronger domain than candidate's finite type |
| modern finite equality | minimum chain partition size equals maximum antichain size | external declaration above | standard finite restriction; source transport not frozen |
| `已验证` | untrusted catalog status | accepted receipts would be required | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Order.Height` provides `Set.chainHeight` and finite attainment lemmas;
`Mathlib.Order.Preorder.Chain` defines `IsChain`; `Mathlib.Order.Antichain` defines `IsAntichain`
and exposes the fact that a chain and an antichain intersect in a subsingleton. A bounded exact-topic
search found no pinned `Dilworth`,
`antichainWidth`, `IsChainPartition`, or `minChainPartition` declaration. `IntakeProbe.lean`
authenticates only these adjacent APIs. Neither those checks nor the failed external candidate run
declare or prove the target.

Before statement freeze, reviewers must preserve and inspect a complete lawful primary edition,
audit corrections, select finite equality or primary finite-width scope, map every definition,
binder, hypothesis, conclusion, optimization convention, and boundary case, approve any transport,
and independently reconcile the external candidate with the current pinned APIs.
