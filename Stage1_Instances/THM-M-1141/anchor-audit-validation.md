# THM-M-1141 anchor-audit validation

Item: `S56-M-1141-ANCHOR_AUDIT`  
Base revision: `b08e4eb319008c958d529196907c5f193beee335`  
Validation date: 2026-07-12 (`Asia/Shanghai`)

## Decision

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact `HarmonicOnNhd` predicate, continuity, and checked complex-disc
mean-value and Poisson formulas. A complete case-insensitive search of its Lean
sources found no `Harnack` occurrence. The disc formulas are real proof-route
anchors, but they do not close the arbitrary-dimensional compact-subset target.

The external `scottnarmstrong/DeGiorgi` project was inspected at immutable
revision `4c1b3077d3782b24065184df4ba59501b2e56fc7`. Its source contains checked
`harnack` and `harnack_of_homogeneousWeakSolution` declarations and no `sorry`,
`admit`, or `axiom` declaration. Those theorems concern divergence-form weak
solutions on nested balls in dimension greater than two and conclude an
essential-supremum/essential-infimum estimate. They neither consume mathlib's
`HarmonicOnNhd` nor state the selected compact-set theorem. The external
toolchain and mathlib pins also differ from this repository, so it is not an
exact import candidate and was not added to `.lake`.

Thus the exact root remains `M3`, with no proof or theorem-completion claim.
The candidate inventory is complete for this phase subject to the explicitly
recorded public-search rate/authentication limitations.

## Commands and outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1141` | 0 | rank 346, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `rg -ni 'harnack' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 1 | no occurrence in pinned mathlib Lean sources |
| harmonic-module file and declaration inventory using `find` and `rg` | 0 | located `Basic`, `Analytic`, `Constructions`, `HarmonicContOnCl`, plus complex `MeanValue` and `Poisson`; no terminal compact-set comparison |
| `git ls-remote https://github.com/scottnarmstrong/DeGiorgi.git refs/heads/main` | 0 | resolved immutable revision `4c1b3077d3782b24065184df4ba59501b2e56fc7` |
| GitHub commit-archive download, `sha256sum`, extraction under `/tmp`, and source scan | 0 | archive SHA-256 `50eedbf2b7900bb45991f1871f6a3583a201aebdaf77b57fabff5f45f4ea996a`; theorem bodies and dependency pins inspected; no proof placeholders found |
| GitHub repository search `Harnack Lean4` | 0 | zero repository results |
| GitHub unauthenticated code search for `Harnack language:Lean` | 22 | HTTP 401; limitation recorded |
| grep.app Lean search for `Harnack` | 22 | HTTP 429; limitation recorded |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1141/AnchorAudit.lean` | 0 | all four pinned declarations and both typed probes elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1141/anchor-audit.json` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1141 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No dependency update, clone, fetch, or `.lake` mutation was performed. The
external archive was source-audited only in `/tmp`; it supplies no local kernel
evidence for this target.
