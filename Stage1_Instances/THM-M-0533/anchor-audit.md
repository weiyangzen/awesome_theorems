# Immutable formal-anchor audit

Item: `S56-M-0533-ANCHOR_AUDIT`  
Theorem: `THM-M-0533`  
Audit cutoff: `2026-07-12` (Asia/Shanghai)  
Worker base revision: `b17067c5d92786b270337cbdd3bfaf74df7773f9`

## Frozen target and search protocol

The audited target is exactly
`AwesomeTheorems.THM_M_0533.MayerVietorisSequence` from `Statement.lean`: the
ordinary integral **singular-homology** long exact sequence for an open cover.
The audit did not substitute sheaf cohomology, a relative-pair sequence, or a
statement which assumes the connecting maps or exactness.

Search order and query families were frozen before classification:

1. repository Lean files, excluding this target and `.lake`, for
   `mayer.?vietoris`, `MayerVietoris`, singular/excision combinations, and
   relative singular homology;
2. every Lean source in the pinned Lake packages, then the singular-homology
   modules and declarations specifically;
3. the official mathlib GitHub issue/PR index and immutable public Git refs for
   `Mayer-Vietoris`, `relative singular homology`, `excision singular homology`;
4. GitHub repository and commit search for English aliases and Lean 4;
5. grep.app Lean search for the same aliases (access result recorded below).

This is a bounded, reproducible inventory at the stated cutoff, not a claim
that all private repositories or all unindexed source hosts were searched.

## Pinned environment

| Component | Immutable revision / digest | Observation |
|---|---|---|
| project | `b17067c5d92786b270337cbdd3bfaf74df7773f9` | worker base |
| Lean | `leanprover/lean4:v4.29.0` | from `Formalizations/Lean/lean-toolchain` |
| mathlib | `8a178386ffc0f5fef0b77738bb5449d50efeea95` | clean pinned package tree; Apache-2.0 |
| singular homology source | SHA-256 `655867a11ed5ec706a554ac32f8f273c5227cafd4b47f0de42d84e24b0d33c7c` | `Mathlib/AlgebraicTopology/SingularHomology/Basic.lean` |
| sheaf MV source | SHA-256 `625500b4c737b778d7c64eec48953e13b23f7400ae233f350f342f9bf3311e76` | `Mathlib/CategoryTheory/Sites/SheafCohomology/MayerVietoris.lean` |
| mathlib license | SHA-256 `b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1` | Apache-2.0 license file |

No dependency was fetched, cloned, updated, or modified during this audit.

## Candidate inventory and classification

### C1: repository-local target statement

- Location: `Stage1_Instances/THM-M-0533/Statement.lean`.
- Declaration: `AwesomeTheorems.THM_M_0533.MayerVietorisSequence`.
- Role: exact elaborated proposition and checked alternate encoding only.
- Proof-body provenance: none; it is a `def : Prop`, not a theorem proving that
  proposition.
- Classification: root `M3` (exact statement/interface exists, proof open).
- Integration decision: retain as canonical target; no proof credit.

The repository-wide scoped search found no other repo-local Lean declaration
which proves this singular-homology target. Hits in legacy Stage1 files were
prose/API inventories; the sheaf-cohomology mention is not a wrapper.

### C2: pinned mathlib singular homology

- Project/revision: mathlib at
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- Module: `Mathlib.AlgebraicTopology.SingularHomology.Basic`.
- Relevant declarations:
  `AlgebraicTopology.singularChainComplexFunctor` and
  `AlgebraicTopology.singularHomologyFunctor`.
- Type/scope: definitions of absolute singular chains and degreewise homology;
  the remainder of the module computes the totally disconnected case.
- Missing target material: no open-cover chain short exact sequence, excision
  theorem, relative singular homology, target connecting morphism, or
  Mayer-Vietoris exactness declaration was found at this revision.
- Classification: supporting interface only (`M3`), not root closure.

### C3: pinned mathlib sheaf-cohomology Mayer-Vietoris theorem

- Project/revision: same pinned mathlib revision.
- Module/declaration:
  `Mathlib.CategoryTheory.Sites.SheafCohomology.MayerVietoris`,
  `CategoryTheory.GrothendieckTopology.MayerVietorisSquare.sequence_exact`.
- Terminal body: repo-external pinned mathlib theorem body in that module;
  `#print axioms` reports `[propext, Classical.choice, Quot.sound]`.
- Type/scope: exactness of a six-object segment built from derived `Ext` for an
  abelian sheaf on a Grothendieck site and a `MayerVietorisSquare`.
- Statement comparison: it is cohomological and contravariant, uses sheaves and
  site squares, and does not mention `singularHomologyFunctor`, an open cover of
  `TopCat`, integral singular chains, or the target degree-zero endpoint.
- Classification: checked adjacent theorem but exact-target mismatch (`M5` as
  a candidate); it supplies **zero** machine closure for the target.
- Integration decision: excluded; no legitimate exact wrapper/transport is
  available.

`Statement.lean` and `AnchorAudit.lean` separately elaborate the target and
adjacent declaration in the same pinned environment. Their printed types make
this boundary independently elaborator-visible without manufacturing a wrapper.

### C4: official mathlib relative-singular-homology pull request

- Project: `leanprover-community/mathlib4`, PR `#37659`, titled
  `feat(AlgebraicTopology): relative singular homology`.
- Immutable audited head: `01b33ef8a476b54c7d1538ff14e245d097577b7d`
  from `refs/pull/37659/head`; the public merge ref observed was
  `4101c4a24080a323163592fb45cb8ea5989d0ed2`.
- Patch SHA-256 at cutoff:
  `a0c3373cf8a085fcfbacfbb056e1c5e239fabdc38394bf5fdc7f78a747112806`.
- Proposed module: `Mathlib.AlgebraicTopology.SingularHomology.Relative`.
- Relevant proposed declarations: `relativeSingularHomologyFunctor`,
  `SingularHomology.δ`, `exact_δ_map`, `exact_map_δ`, and `exact_π_δ`.
- Scope: a long exact sequence for one injected topological pair. The audited
  patch contains no Mayer-Vietoris or excision theorem and therefore cannot
  derive the target without substantial new chain/excision/composition work.
- Dependency feasibility: not in the pinned Lake closure and still represented
  by a PR ref at cutoff. Worker policy forbids fetching it; no local build,
  axiom audit, or transitive trust closure was performed.
- Classification: credible future supporting interface only (`E3`/`M3` for
  infrastructure), not an exact external theorem and not `M1` root evidence.
- Integration decision: do not pin/import: it does not prove the target even
  on its immutable audited head. Reopen if a pinned revision adds excision plus
  an exact Mayer-Vietoris wrapper compatible with the canonical target.

### C5: other external Lean 4 projects

GitHub repository searches for `Mayer Vietoris Lean 4` and `singular homology
Lean 4` returned `total_count: 0`. GitHub commit searches for
`"Mayer-Vietoris" language:Lean`, `MayerVietoris language:Lean`,
`singularHomologyFunctor language:Lean`, and `"relative singular homology"
language:Lean` returned `total_count: 0`. A broader repository query returned
one unrelated project and was rejected by title/scope inspection. These API
negative results are discovery evidence only, not proof of global absence.

grep.app returned HTTP `429` for every attempted Lean query. This is an explicit
access limitation, not a negative search result. No exact external Lean 4
closure was located by the available indexed searches.

## Result and debt boundary

The complete frozen candidate inventory above is classified, so the assigned
anchor-audit phase is self-tested. It does **not** complete the broader theorem
audit. The exact root remains `M3`: its statement is present, while no usable
repo-local, pinned mathlib, or immutable external proof body was located.
There is no `M1` integration debt because the only unintegrated formal
candidate is partial relative-homology infrastructure, not the target theorem.

No `H0`, `M0-*`, `R0`, audit completion, lifecycle transition, accepted receipt,
or theorem completion is claimed. The next root cut consists of constructing
the open-cover singular-chain short exact sequence/excision bridge, deriving
the connecting maps and all exactness segments including degree zero, and only
then checking their composition against `MayerVietorisSequence`.

## Validation receipt

Commands were run from the repository root unless noted.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0533` | exit 0; rank 590, planned, theorem complete false |
| scoped `rg` repository and pinned-package query families listed above | exit 0/1 by match presence; no exact singular-homology Mayer-Vietoris proof found; all matches classified above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git ls-remote https://github.com/leanprover-community/mathlib4.git refs/pull/37659/head refs/pull/37659/merge` | exit 0; immutable refs recorded under C4 |
| GitHub search API query families listed above | exit 0; results recorded under C4/C5; later PR-detail requests hit HTTP 403 rate limiting |
| grep.app API query families listed above | exit 22; HTTP 429, recorded access limitation |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0533/Statement.lean` | exit 0; target printed as `Prop`; three mutation-fixture unused-variable warnings |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0533/AnchorAudit.lean` | exit 0; adjacent theorem type and its three axioms printed |
| `rg -n '\bsorry\b|^[[:space:]]*(axiom|constant)[[:space:]]' Stage1_Instances/THM-M-0533 --glob '*.lean'` | exit 1; no placeholder or bodyless declaration matches |
| `python3 -m json.tool Stage1_Instances/THM-M-0533/task-dag.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0533` | exit 0; no output |

Known failures are intentional and bounded: no exact proof candidate exists in
the audited inventory; external index coverage was limited by grep.app HTTP 429
and later GitHub HTTP 403; PR `#37659` was not fetched or built because it is
outside the pinned closure and does not contain the target theorem.
