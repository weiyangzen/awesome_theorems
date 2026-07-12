# Anchor-audit validation

Item: `S56-M-0529-ANCHOR_AUDIT`  
Base revision: `b86b7c60888b8506233bd2a07adc4f7c277ad675`

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains an exact
compositional anchor. `TopCat.isoOfHomeo e` makes the homeomorphism an isomorphism in `TopCat`, and
`Functor.map_isIso` makes its image under the exact degreewise integral singular-homology functor an
isomorphism. `AnchorAudit.lean` checks these declarations and proves an exact-conclusion audit probe
with `infer_instance`; Lean reports the standard mathlib foundation set `propext`,
`Classical.choice`, and `Quot.sound`. Thus the candidate is suitable for a later
local wrapper (`M0-W_candidate`), but this anchor-audit node does not claim the proof node or theorem
completion.

The external search also located `facebookresearch/atlas-lean` at immutable commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its
`HomotopyTheory.homotopyEquivHomologyIso` is a stronger related result for homotopy equivalences and
general coefficients, but its conclusion is an object-level `Iso`, not the exact map-level `IsIso`
target. It remains anchor-only and is unnecessary for integration. GitHub code search was
rate-limited, so that lane is recorded as blocked rather than negative.

## Commands and results

Commands ran on 2026-07-12. Lean used only the existing pinned `.lake` artifacts; no update, build,
fetch, clone, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0529/AnchorAudit.lean` | 0 | Four anchor declarations and exact probe elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0529/Statement.lean` | 0 | Canonical target re-elaborated unchanged |
| `python3 Stage1_Instances/THM-M-0529/check_anchor_audit.py` | 0 | Audit boundary, installed mathlib HEAD, manifest pin, probe, and three source hashes agreed |
| `rg -n 'isoOfHomeo|singularHomologyFunctor|map_isIso' Formalizations/Lean/.lake/packages/mathlib/Mathlib ...` | 0 | Located the exact pinned compositional anchors and related mathlib uses |
| Sourcegraph API query recorded in `anchor-audit.json` | 0 | `matchCount=78`; response SHA-256 `d01870cb77fb235818e304f21efa4b9fa1a631cb6e12852e6baa50a4f771d6ae` |
| GitHub REST repository search recorded in `anchor-audit.json` | 0 | `total_count=0`, complete response; SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| GitHub REST code search recorded in `anchor-audit.json` | 0 | Rate-limit blocker captured; SHA-256 `1db366a292a73aaa6963398fe4e4bdb2b42e9b7a2d745a0878210569945e386e` |
| Immutable raw retrieval of `atlas-lean/.../Section5.lean` | 0 | Source SHA-256 `9eda91502c1f529fa4acb213ca0b3a2759b6d03966b3cd6b1d74e1af31f19514`; toolchain and mathlib pin match the local environment |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0529` | 0 | Rank 586; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0529 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Boundary

This is a bounded, self-tested formal-anchor audit. The exact proof declaration, frozen obligation
tree, complete transitive provenance/trust closure, human-source `H0`, readability, release replay,
independent verification, and theorem-completion decision remain open.
