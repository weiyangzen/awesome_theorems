# Anchor audit record

Item: `S56-M-1057-ANCHOR_AUDIT`  
Base revision: `8b61d0242da6b4b6810daf423a82881bc4a5c956`

## Immutable audit surface

The local environment pins mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` under Lean 4.29.0. The manifest
SHA-256 is `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
No Lake dependency update, fetch, or clone was performed.

| Candidate | Exact role | Audit verdict |
|---|---|---|
| `Mathlib.Analysis.Subadditive.Subadditive.tendsto_lim` | Fekete convergence for a deterministic subadditive real sequence | Checked through `deterministic_fekete_candidate`; useful only after expectation subadditivity, not pointwise Kingman |
| `MeasureTheory.MeasurePreserving.iterate` | Measure preservation for `T^[n]` | Checked through `iterate_measure_preserving_candidate`; infrastructure only |
| `Ergodic.ae_eq_const_of_ae_eq_comp_ae` | Constancy of an already measurable, invariant limit | Checked through `ergodic_constancy_candidate`; does not construct the limit or prove invariance |
| Legacy `S1_M_249.lean` at the base revision | Earlier statement package and supporting wrappers | Discovery only; it explicitly has no terminal Kingman proof |

All three checked wrappers report only `propext`, `Classical.choice`, and
`Quot.sound`. A case-insensitive search of every pinned `Mathlib/**/*.lean` for
`Kingman`, `subadditive ergodic theorem`, or `SubadditiveErgodic` returned zero
matches. Thus pinned mathlib has useful adjacent APIs but no located terminal
declaration for `KingmanTarget`.

## External Lean 4 audit

The audit queried GitHub repository search for quoted `subadditive ergodic`
plus `lean` (zero repositories), attempted GitHub code searches for `Kingman
language:Lean` and the quoted theorem name, and searched the available local
external source tree. No terminal Lean 4 candidate was found locally. Anonymous
GitHub code search required sign-in and its REST endpoint returned HTTP 403, so
the negative external result is explicitly bounded by that access limitation;
there is no immutable external candidate revision to credit or integrate.

This is therefore `formalization_debt`, not `repo_local_integration_debt`:
Kingman's theorem is known mathematics, but the audit found no existing Lean 4
terminal proof awaiting local integration. Machine status remains
`not_repo_local_closed`, and the root vector remains `[H1, M3, R3]`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework targets passed |
| `python3 scripts/stage1_target.py show THM-M-1057` | 0 | Rank 249, planned, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1057/AnchorAudit.lean` (cwd `Formalizations/Lean`) | 0 | Three wrappers elaborated; exact upstream types and axiom profiles printed |
| `rg -n -i 'kingman\|subadditive ergodic theorem\|SubadditiveErgodic' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean' \| wc -l` | 0 | `0` terminal-name/text matches in pinned mathlib |
| GitHub repository search API for quoted `subadditive ergodic` plus `lean` | 0 | `total_count: 0` |
| GitHub REST code search for `Kingman language:Lean` | 22 | HTTP 403; recorded search-coverage limitation, not evidence of absence |

## Boundary

The anchor inventory is self-tested and ready for master review. It does not
prove `KingmanTarget`. The first open machine gate is the substantive
almost-everywhere convergence and invariance branch; neither deterministic
Fekete convergence nor ergodic constancy supplies that branch.
