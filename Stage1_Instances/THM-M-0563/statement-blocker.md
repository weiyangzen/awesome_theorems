# Exact-statement gate: blocked

Item: `S56-M-0563-STATEMENT`  
Base revision: `d30ab383279f10fe53d90d3c5b5421638c550b25`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the repository record.
The complete mathematical wording is `流形的配边分类` ("classification of manifolds by
cobordism"), attributed to Rene Thom in 1954. As frozen by the accepted intake, this phrase does
not identify one proposition. It may mean the unoriented Stiefel-Whitney-number criterion, an
oriented characteristic-number criterion, a Pontryagin-Thom correspondence, or a computation of a
cobordism group or ring. These alternatives have different domains, hypotheses, coefficient and
orientation conventions, and conclusions.

Choosing one of those branches here would invent missing mathematics and would violate section
5.1's source-identity requirement. In particular, stating only that characteristic numbers are
cobordism invariants would weaken a completeness/classification claim, while an abstract predicate
or classifier supplied as a parameter would assume rather than encode the desired theorem. The
intake's `instance.json` accordingly leaves exact theorem selection open with machine status `M4`.

The candidate primary source recorded by intake, Rene Thom's *Quelques proprietes globales des
varietes differentiables* (1954), has no accepted pinpoint theorem/page, exact wording, definition
crosswalk, or independent source review in this dossier. Thus no ordered binders, canonical human
claim, canonical Lean expression, expression hash, alternate-form transport, or meaningful
removed-hypothesis/domain/scope/boundary mutations can be frozen.

## Pinned Lean boundary

`StatementProbe.lean` uses the single nearest mathlib import:

```lean
import Mathlib.Geometry.Manifold.Bordism
```

It elaborates checks of `SingularManifold`, `SingularManifold.toPUnit`, and
`SingularManifold.sum`. The pinned module describes itself as only "the beginnings of unoriented
bordism theory" and its TODO explicitly leaves the bordism type, bordism relation, bordism groups,
ring structure, and extraordinary homology theory unimplemented. Therefore this probe establishes
only that the singular-manifold substrate exists; it is neither the source-selected theorem nor a
substitute for it.

The environment is Lean `4.29.0`, repository base
`d30ab383279f10fe53d90d3c5b5421638c550b25`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, reused from the canonical pinned `.lake` artifact.
No dependency update, fetch, clone, or build was performed.

## Validation evidence

Commands were run from the worker clone on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0563` | exit 0; rank 611, planned, theorem_complete false |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0563/StatementProbe.lean)` | exit 0; printed the elaborated types of the three checked declarations |
| `git diff --check -- Stage1_Instances/THM-M-0563` | exit 0; no output |

## Gate result

First failed gate: section 5 exact canonical-claim identity, before Lean expression elaboration.
Machine status remains `M4`; no statement credit, proof credit, audit completion, or theorem
completion is claimed. Retry requires an accountable source reviewer to select and transcribe a
pinpoint primary theorem and freeze smoothness, compactness, boundary, dimension, orientation or
tangential structure, coefficient and characteristic-number conventions, and the exact
classification conclusion.

Because the assigned statement phase is not complete, no `.stage1-worker-selftest.json` is
emitted.
