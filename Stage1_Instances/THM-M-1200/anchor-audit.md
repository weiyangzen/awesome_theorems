# Anchor audit

Item: `S56-M-1200-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Repository base: `7c261cad5ed43a724864ac5581564164750b865c`  
Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

## Verdict

No exact mathlib or credible external Lean 4 closure was identified for
`Stage1Instances.THM_M_1200.RankineHugoniotTarget`. The machine status remains
`not_repo_local_closed`, with `formalization_debt`. This is not
`repo_local_integration_debt`: there is no located external proof to pin or import.

The audit did identify usable pinned mathlib infrastructure. `ContDiffBump` and its
`contDiff`, `hasCompactSupport`, `one_of_mem_closedBall`, and `nonneg` declarations can supply a spacetime bump whose
trace is nonzero. `Continuous.integral_pos_of_hasCompactSupport_nonneg_nonzero` can turn the
corresponding continuous, compactly supported, nonnegative, nonzero one-dimensional trace into a
strictly positive integral. These are plausible ingredients for the reverse implication of the
frozen equivalence. They do not state Rankine-Hugoniot, do not derive the interface defect from a
piecewise weak solution, and receive no closure credit.

## Search record

The pinned mathlib source tree was searched case-insensitively for `rankine`, `hugoniot`,
`conservation law`, `weak solution`, and `shock`. There was no Rankine-Hugoniot or scalar
conservation-law shock theorem. The generic `weak solutions` occurrence is documentation for
distribution test functions, not this target.

External discovery used GitHub's repository search API and Sourcegraph's global Lean code search.
GitHub returned zero repositories for quoted `Rankine-Hugoniot` with `language:Lean`, for
`Rankine Hugoniot Lean4`, and for quoted `weak solution` plus PDE with `language:Lean`. Its quoted
`conservation law` Lean query returned three unrelated repositories whose descriptions concern
radix, sequence, or language conservation rather than PDEs. Sourcegraph completed both the
`RankineHugoniot` and quoted `Rankine-Hugoniot` Lean searches with `matchCount: 0`.

These bounded negative searches are not a claim that no formalization exists anywhere. They are
enough to show that this audit found no exact candidate eligible for pin/import/check. Exact query
terms and structured conclusions are preserved in `anchor-audit.json`.

## Validation

Commands ran inside this worker clone. The Lean command used only the existing pinned environment;
no update, build, clone, fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exactly `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'rankine|hugoniot|conservation law|weak solution|shock' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | generic distribution `weak solutions` documentation only; no exact candidate |
| `lake env lean ../../Stage1_Instances/THM-M-1200/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | all seven selected declarations resolved and their types printed |
| GitHub repository search API queries recorded above | 0 | three exact-topic queries returned 0; broad conservation-law results were unrelated |
| Sourcegraph global Lean code searches recorded above | 0 | both completed with `matchCount: 0` |
| `python3 -m json.tool Stage1_Instances/THM-M-1200/anchor-audit.json` | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546 |
| `git diff --check -- Stage1_Instances/THM-M-1200 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is anchor-audit evidence pending master acceptance. It does not complete the obligation tree,
proof, validation, release, source-fidelity, or theorem gates.
