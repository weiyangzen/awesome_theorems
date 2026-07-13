# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11714-11719` supplies exactly the title `循环码`, attribution
`众多数学家`, period `20世纪`, gloss `循环移位不变的码`, importance "high," and status `已验证`.
Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
formula, ordered binders, hypotheses, conclusion, proof boundary, correction history, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:43228-43253` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest records rank 1211, baseline
`L0 / rework_required`, no legacy slot, `lifecycle_mode: planned`, and `theorem_complete: false`.
It preserves `已验证` only as untrusted source metadata.

## Clause crosswalk

| Catalog component | Mathematical information fixed | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `码` (code) | some family of words | `Set (Fin n -> A)`, `Finset`, `AddSubgroup`, or `Submodule` | alphabet and code structure absent |
| `循环移位` (cyclic shift) | some cyclic coordinate permutation | `finRotate`, `finCycle`, precomposition, list rotation, or a checked equivalent | length, direction, and action convention absent |
| `不变` (invariant) | stability under that operation | membership closure, set equality, or invariant subobject | exact predicate and quantifier order absent |
| `循环码` (cyclic code) | conventional class label | a future definition plus one selected theorem | object/family label, not a proposition |
| `已验证` | untrusted inventory value | exact source and kernel receipts would be required | no H or M credit |

## Modern source-family lead

W. Cary Huffman and Vera Pless, *Fundamentals of Error-Correcting Codes*, Cambridge University
Press, 2003, has a chapter titled "Cyclic codes," pages 121-167, DOI
`10.1017/CBO9780511807077.005`. Crossref metadata and the publisher's chapter landing page were
observed on 2026-07-13. This is an authoritative modern source-family lead, but the repository does
not cite it, and the accessible metadata exposes no definition, theorem statement, assumptions, or
proof text. It therefore does not select the catalog root and receives no H1 or H0 credit. A future
source audit must lawfully inspect an immutable edition, record exact definition and theorem/page
locators, map every incorporated premise and conclusion, check corrections, and obtain independent
review.

Historical origin is likewise unresolved. The catalog's collective attribution and century do not
identify a primary paper or distinguish the shift-closure definition from later polynomial,
generator, duality, or decoding results. Intake does not invent an attribution or primary-source
claim.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `finRotate` and `finCycle`, `LinearEquiv.piCongrLeft`, `hammingDist`, and
`Matrix.circulant`. These provide coordinate permutations, linear transport, a coding metric, and
a related matrix construction. They do not define a cyclic code or state a code-characterization
theorem.

A bounded lexical search of repo-local Lean and pinned mathlib found no exact cyclic-code
declaration. This negative result is intake discovery only, not a precommitted or exhaustive anchor
audit and not a global absence claim. List rotation and circulant matrices are explicit
non-substitutes; similarly named cyclic algebra does not establish a code predicate.

## Source gate

The received wording is provisionally `H5`: it is not one stable truth-valued proposition. That is
a target-correction classification, not a claim that established results about cyclic codes are
false or open. Before statement work, accountable reviewers must select and preserve one immutable
source proposition, freeze every definition, binder, hypothesis, conclusion, transport, and
boundary case listed in `scope-map.md`, reconcile neighboring target ownership, audit corrections,
and independently approve fidelity to `THM-M-1590`.
