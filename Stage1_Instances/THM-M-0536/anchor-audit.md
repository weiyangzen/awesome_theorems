# THM-M-0536 Lean 4 anchor audit

## Scope and immutable revisions

This audit compares `Stage1.THM_M_0536.HomotopyInvarianceStatement` with repo-local Lean,
the pinned mathlib tree, and bounded public Lean 4 discovery surfaces. The environment is
`leanprover/lean4:v4.29.0`; `Formalizations/Lean/lake-manifest.json` locks mathlib to
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (Apache-2.0). The relevant upstream file first entered
mathlib at commit `f71a4059a8f0c29fac39f43a7376e94defcbe603`, PR #37091. No dependency was fetched,
updated, installed, or modified.

## Candidate inventory

| Candidate | Exact type/role | Provenance and exact-root verdict |
|---|---|---|
| `AlgebraicTopology.singularHomologyFunctor` | Coefficient object and degree indexed functor `C ⥤ TopCat ⥤ C` | Pinned mathlib `Basic.lean:47`; substrate defining the exact target map, not alone a proof. |
| `TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor` | A `TopCat.Homotopy f g` makes the two induced singular-homology maps equal for every coefficient object and `n : ℕ` | Pinned mathlib `HomotopyInvarianceTopCat.lean:57`; terminal homotopy-invariance bridge. Its body calls `H.singularChainComplexFunctorObjMap R` and then `Homotopy.homologyMap_eq`; it is not an axiom or placeholder. |
| `ContinuousMap.HomotopyEquiv.left_inv`, `.right_inv` | Homotopies from inverse-forward and forward-inverse composites to identity | Pinned mathlib `Topology/Homotopy/Equiv.lean:52-53`; exact premise destructors needed to use the bridge twice. |
| `Stage1.THM_M_0536.anchorCandidate` | Same quantified induced map and `IsIso` conclusion as the frozen target | Repo-local checked composition in `AnchorAudit.lean`. It chooses the inverse induced map, uses functoriality, both homotopies, and the equality bridge. This establishes an exact local candidate, but the proof-phase declaration and downstream gates remain open. |
| `HomotopyEquiv.toHomologyIso` | Isomorphism on homology induced by a chain-complex homotopy equivalence | Pinned mathlib `Algebra/Homology/Homotopy.lean:815`; nearby generic candidate. It is not directly applicable until a chain-complex `HomotopyEquiv` is constructed from the topological one, so the shorter checked composition above is selected. |

The repo-local search found no other theorem with this exact topological homotopy-equivalence and
integral singular-homology root. Existing Stage1 files only reference the same mathlib substrate;
they do not supply independent proof credit for this target.

## Provenance and trust boundary

The selected terminal bridge is source-visible at the locked revision. Its body is
`(H.singularChainComplexFunctorObjMap R).homologyMap_eq n`; the chain-homotopy constructor delegates
to the singular-simplicial-set homotopy implementation. `#print axioms anchorCandidate` reports only
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` and no target-specific axiom.
Mathlib's source header credits Joël Riou and Fabian Odermatt and records a prior Lean 3
formalization by Brendan Seamus Murphy. The current file was introduced by upstream commit
`f71a4059a8f0c29fac39f43a7376e94defcbe603` on 2026-03-30 and is present unchanged in the locked
mathlib snapshot for the audited lines.

## External discovery

On 2026-07-12, GitHub REST repository searches for `homotopy invariance singular homology Lean`,
`singular homology Lean 4`, and `homotopy equivalence homology Lean` each returned `total_count: 0`
and `incomplete_results: false`. grep.app requests for the two exact mathlib declarations, the
generic `HomotopyEquiv.toHomologyIso`, and a descriptive query all returned HTTP 429. The latter is
an access limitation, not negative evidence, and repository metadata search is not exhaustive code
search. No credible independent external Lean 4 candidate was discovered, so there is no external
revision, module, declaration, toolchain, license, or dependency to integrate.

## Classification

The bounded anchor-audit phase is complete pending master acceptance. Unlike an anchor-only hit,
the pinned mathlib bridge was composed in a repo-local Lean audit candidate of the exact target
shape. This identifies a feasible future state `local_wrapper_upstream_mathlib`, while the accepted
machine state remains `M4`: the assigned phase does not install the canonical proof declaration,
freeze the obligation registry, or provide proof/validation/release receipts. `H1` and `R4` are
unchanged. Full audit and theorem completion remain false.

## Validation receipt

Base revision: `b17067c5d92786b270337cbdd3bfaf74df7773f9`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0536` | 0 | Rank 593, planned, L0/rework-required, theorem incomplete. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Returned locked commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `rg -n -i 'homotopy equivalen.*homolog\|homology.*homotopy equivalen\|homotopy invarian\|congr_homologyMap_singular\|singularChainComplexFunctorObjMap' Formalizations/Lean/.lake/packages/mathlib --glob '*.lean'` | 0 | Located the exact bridge, its source-visible body, simplicial predecessors, and the generic chain-complex candidate; no more direct terminal topological theorem. |
| `lake env lean ../../Stage1_Instances/THM-M-0536/AnchorAudit.lean` from `Formalizations/Lean` | 0 | All named anchors elaborated; exact candidate checked; axioms were `[propext, Classical.choice, Quot.sound]`. |
| `lake env lean ../../Stage1_Instances/THM-M-0536/Target.lean` from `Formalizations/Lean` | 0 | Frozen target still elaborated. |
| GitHub REST repository searches listed above | 0 | Three complete zero-result metadata responses. |
| grep.app API searches listed above | 22 each | HTTP 429; recorded as an external-search limitation. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-0536` | 1 | Expected no-match status: no prohibited Lean declaration token. |
| `git diff --check -- Stage1_Instances/THM-M-0536 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Status boundary: this receipt supports only scoped candidate inventory, feasibility, and provenance.
It is not accepted proof-phase closure, H0, R0, audit completion, theorem completion, or release.
