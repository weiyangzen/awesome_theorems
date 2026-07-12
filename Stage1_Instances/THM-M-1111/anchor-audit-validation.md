# Anchor-audit validation record

Item: `S56-M-1111-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Base revision: `cd7d0c47c19a08d85f4314833fd1e5a339230a3c`

## Result

The repo-local exact target is an elaborated proposition over `FourMomentSemantics`, not a theorem
body. Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies matrix, Hermitian,
Bochner-integration, and independence substrate checked in `AnchorAudit.lean`. A recursive search
of all pinned package Lean sources found no Four Moment, Tao-Vu, Wigner random-matrix, ordered
eigenvalue-statistics, or moment-matching terminal declaration. The one Tao/Vu text hit is an
unrelated bibliography entry in additive combinatorics.

Bounded public searches found no exact external Lean 4 candidate. Sourcegraph returned zero hits
for the exact theorem name, Tao-Vu spellings, and eigenvalue-statistics phrase. Its broad `Wigner`
query returned only quantum Wigner-function/symmetry and Breit-Wigner name collisions. GitHub
repository metadata searches returned zero relevant repositories. GitHub code search was
authentication-blocked and grep.app rate-limited, so neither lane is falsely reported as a
negative result. Search responses are dated discovery evidence, not immutable proof artifacts.

The root therefore remains `M3`: the exact statement/interface exists, but no semantic
implementation or terminal proof candidate was located. This completes the assigned bounded
anchor inventory pending master acceptance; it does not establish `AUDIT-Z`, `H0`, proof closure,
or theorem completion.

## Commands and results

All commands ran in this worker clone. Lean used only the existing pinned Lake closure; no update,
build, dependency clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1111/AnchorAudit.lean` | 0 | candidate boundary and four pinned mathlib substrate declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1111/Statement.lean` | 0 | exact target re-elaborated and explicit expression printed |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | audit boundary, candidates, probes, manifest pin, and installed mathlib HEAD agreed |
| `rg -l -i 'Four[ -]?Moment|Tao.?Vu|Wigner|random (Hermitian|matrix)|eigenvalue statistic|moment match' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | one unrelated Tao/Vu bibliography file; no formal candidate |
| five Sourcegraph queries recorded in `anchor-audit.json` | 0 | four exact/family queries had `matchCount=0`; broad Wigner hits were all irrelevant name collisions; responses content-hashed |
| GitHub repository searches recorded in `anchor-audit.json` | 0 | zero repositories for all three completed queries |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned; L0/rework-required; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1111 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Reopen condition

Reopen integration when a concrete Lean 4 repository, immutable commit, module, and exact
declaration is identified. It must then pass license, toolchain/dependency, exact-type transport,
placeholder, axiom, unsafe/oracle, terminal-body provenance, and repo-local wrapper checks.
