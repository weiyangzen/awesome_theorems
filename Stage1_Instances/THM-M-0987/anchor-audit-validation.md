# Anchor-audit validation record

Item: `S56-M-0987-ANCHOR_AUDIT`  
Base revision: `a946660d1b30093bec2ff64b9c71d32f5109943e`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact formal
candidate `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`. The direct wrapper
`Stage1Instances.THM_M_0987.AnchorAudit.pinnedMathlibCandidate` elaborates with the statement
phase's binders, assumptions, normalization, zero-variance-inclusive Gaussian law, and convergence
conclusion. Lean reports the same axioms for the upstream theorem and wrapper: `propext`,
`Classical.choice`, and `Quot.sound`. The terminal module contains no `sorry`, `axiom` declaration,
`admit`, or `unsafe` marker.

The legacy `S1_M_267` wrapper is discovery evidence only. The adjacent external project
`uw-math-ai/central_limit_theorem@0ed57e943d642eaa95fe547780024b9e3a0dfbdf` is not usable: its
`CLT` statement differs from the canonical target, uses Lean `v4.13.0-rc3` with an unpinned moving
mathlib dependency, and its terminal proof is `sorry`. Supporting files also contain `sorry`.
Raw immutable source files and the immutable commit patch were inspected without cloning or
fetching. GitHub API queries returned HTTP 403 rate limits, so this audit makes no API-wide negative
search claim.

The eligible mathlib declaration is therefore an `M0-W` candidate, not an accepted `M0-W` root.
The canonical artifact remains `M3` until the proof phase adds the exact root wrapper and later
validation closes full provenance, trust, composition, and release gates. No human-source status or
theorem completion is claimed.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. All Lean checks used the existing pinned
`.lake` artifacts read-only. No `lake update`, build, dependency clone, or dependency fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0987/AnchorAudit.lean` | 0 | Exact candidate wrapper and six route declarations elaborated; upstream and wrapper axiom reports both contained only `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0987/Statement.lean` | 0 | Canonical statement and pinned-source shape re-elaborated |
| `python3 Stage1_Instances/THM-M-0987/check_anchor_audit.py` | 0 | Four candidates, conservative status, probe inventory, manifest pin, installed HEAD, source blob, and terminal-module placeholder scan agreed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to `lake-manifest.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib ls-tree HEAD Mathlib/Probability/CentralLimitTheorem.lean` | 0 | Immutable source blob `e0cfc897a4679025f71712abbf8834c1f318b2c1` |
| `rg -n '\\bsorry\\b\|\\baxiom\\b\|\\badmit\\b\|unsafe' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/CentralLimitTheorem.lean` | 1 | Expected no-match result in pinned terminal module |
| Raw immutable `curl` reads of six files under `uw-math-ai/central_limit_theorem@0ed57e...` | 0 | Terminal `CLT` and supporting route contain `sorry`; `main_theorem.lean` SHA-256 is `abe8ba1275a542ac81441453ec9bc6645a3f7fd956172ed3cf7a6f84393090ba`; toolchain is `v4.13.0-rc3` |
| `curl .../commit/0ed57e....patch` | 0 | Immutable commit patch available; SHA-256 `40af446d861ae7db66e0a9b006b654c296cdbcec2fd263fe05423ab664f1af43` |
| GitHub REST commit/tree/ref requests | 22 | HTTP 403 rate-limit access failure; explicitly not treated as negative discovery evidence |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard structure and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0987` | 0 | Rank 267, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0987` | 0 | No whitespace errors |

## Downstream boundary

The proof phase may unfold `CentralLimitTheoremTarget` and directly apply the pinned mathlib
candidate. It must not inherit the legacy wrapper's status. Before any accepted `M0-W` or theorem
completion claim, downstream phases still owe the obligation registry, exact root proof,
transitive declaration/import and terminal-body provenance, foundation/TCB acceptance, composition,
hermetic reproduction, readability, freshness, and independent verification.
