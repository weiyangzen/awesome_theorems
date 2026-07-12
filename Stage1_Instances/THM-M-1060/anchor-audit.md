# Anchor audit record

Item: `S56-M-1060-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Base revision: `205d13cfc35c45883410c569709a91cb34edce16`

## Frozen scope and search order

The exact comparison target is
`Stage1Instances.THM_M_1060.SchilderTarget` in `Statement.lean`: the full
small-noise LDP for every finite-dimensional-distribution-characterized Wiener
measure on based continuous paths over `[0,1]`, including open lower bounds,
closed upper bounds, and compactness of all real Cameron-Martin-rate sublevels.

The audit searched repo-local Lean first, the existing pinned mathlib tree
second, and public Lean 4 sources third. Exact and alias queries were
`Schilder`, `SchilderTarget`, `LargeDeviation`, `large deviation`, `LDP`,
`RateFunction`, `rate function`, `CameronMartin`, `Cameron-Martin`, `Wiener`,
`Brownian`, `Varadhan`, `Sanov`, `Cramer`, and `LaplacePrinciple`.

## Candidate inventory

| Candidate | Immutable identity | Exact comparison and trust result | Classification |
|---|---|---|---|
| repo-local exact-name search | base `205d13cfc35c45883410c569709a91cb34edce16` | No proof body for `SchilderTarget`. `S1_M_250.lean` defines a generic, sequence-indexed LDP and proves only that a structure already containing upper/lower bounds projects to that LDP. It has neither the small-noise filter normalization, Wiener law, Cameron-Martin energy, nor goodness proof. | `M3` interface, not terminal |
| pinned mathlib | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`; Lean `v4.29.0` | Recursive search of 7,871 Lean files found no Schilder or probabilistic large-deviation theorem family. Checked substrate includes `gaussianReal`, `gaussianReal_map_const_mul`, `Measure.map`, `liminf`, and `limsup`. These do not discharge either LDP bound or rate goodness. Imported declarations are ordinary checked mathlib declarations; no exact candidate body exists on which an axiom/placeholder closure could be claimed. | `M3` substrate, not `M0-W` |
| RemyDegenne/brownian-motion | commit `91885e6172648ea7f9c6a16b3a7069f92c88e023` (2026-05-01) | GitHub's recursive immutable tree response was complete (`truncated=false`, 178 entries). It contains Brownian construction/Gaussian/continuity/stochastic-integral modules, but no path containing Schilder, deviation, or Cameron. Relevant declarations reported by the already inspected source are `IsBrownian`, `IsBrownian_brownian`, and `hasLaw_brownian_eval`; none is the target. The project pins Lean `v4.30.0-rc1`, mathlib `f23306121184717ace04f3ac514be974e3224c8b`, and `kolmogorov_extension4` `e236e968c2b038b952444df54075a6e8b1058380`, outside this Lake closure. | anchor-only `M5` integration blocker, not `M1`/`M0-P` |
| public GitHub discovery | queries run 2026-07-12 | Repository searches for `Schilder theorem Lean`, `schilder lean4`, `"large deviation" lean4`, and `cameron-martin lean4` returned zero repositories before the unauthenticated API limit. REST code search returned HTTP 401 `Requires authentication`; therefore discovery saturation is not claimed. | no candidate; explicit access limitation |

No row is an exact external kernel closure, so there is no terminal proof body,
wrapper, axiom set, or transitive proof provenance to credit. In particular,
Brownian infrastructure is not promoted to `M1`, and the assumed-obligations
wrapper in `S1_M_250.lean` is not a proof of either analytic bound.

## Audit decision

The bounded inventory is complete for this phase and every retained candidate
is classified. The exact theorem remains `M3`: its statement and supporting
interfaces elaborate, but no usable terminal formal proof was located. Human
source fidelity remains outside this formal-anchor phase; the intake's source
pinpoint/errata gaps remain, so this record does not assert `H0`. Audit-wide and
theorem completion both remain false.

Reopen external integration only when an immutable Lean 4 repository, module,
and declaration with an exact statement is identified. It must then be pinned
or vendored, checked through an exact local wrapper, and audited for
placeholders, axioms, unsafe/oracle boundaries, dependencies, and license.

## Commands and results

All Lean commands used the existing dependency closure. No Lake update, build,
clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `rg -n -i 'schilder|large.?deviation|large deviations|cameron.?martin|small.?noise.?ldp' . --glob '*.lean' --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1060/**'` | 0 | only neighboring Stage1 interfaces/scaffolds; no exact Schilder proof |
| `rg -l -i 'schilder|large.?deviation|large deviations|rate function|cameron.?martin' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | two incidental English hits only; no probabilistic LDP/Schilder module |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| GitHub repository-search API queries listed above | 0 | zero repositories for each completed query; later unauthenticated rate limit recorded, not hidden |
| GitHub code-search API query `Schilder language:Lean` | HTTP 401 | `Requires authentication`; negative saturation not claimed |
| GitHub recursive-tree API for `RemyDegenne/brownian-motion` at `91885e...` | 0 | complete 178-entry tree; Brownian modules present, no Schilder/deviation/Cameron path |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1060/AnchorAudit.lean` | 0 | checked substrate declarations and both negative-completion guards |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1060/Statement.lean` | 0 | rechecked and printed the exact comparison target |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1060` | 0 | rank 503; L0/rework-required; planned; theorem incomplete |

## Status boundary

This is self-tested anchor-audit evidence pending master acceptance. It does
not change generated checklist/DAG state, claim `AUDIT-Z`, or claim theorem
completion.
