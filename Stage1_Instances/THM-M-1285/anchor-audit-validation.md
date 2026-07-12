# Anchor-audit validation record

Item: `S56-M-1285-ANCHOR_AUDIT`  
Base revision: `4ac441e7be0c42ea78cddc541390953fa7318de7`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Verdict

The exact frozen target remains only the proposition definition
`Stage1Instances.THM_M_1285.SchwarzRearrangementTarget`. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains useful ingredients for a constructive route:
measurable norm and strict superlevels, exact Euclidean ball volume, positivity and finiteness of
ball measure, and strict/non-strict layer-cake formulas. The eight probes in `AnchorAudit.lean`
elaborate, but none supplies the existential rearrangement witness.

A bounded source search of repo-local Lean and all materialized pinned dependencies found no
Schwarz/symmetric-decreasing rearrangement declaration. Public Sourcegraph and GitHub repository
metadata searches found no candidate, while GitHub code search required authentication and is
recorded as blocked. The complete immutable tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` had 1204 entries and
no matching path. These negative results are bounded discovery evidence, not a claim of global
absence.

The exact root therefore remains `M3`: checked supporting interfaces exist, but no terminal body or
checked reduction closes the target. This completes only the assigned anchor-audit phase pending
master acceptance. It does not complete the theorem or the full audit.

## Commands and results

Lean reused the existing pinned `.lake` artifacts. No dependency update, fetch, clone, or build was
performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1285/AnchorAudit.lean` | 0 | all eight pinned support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1285/Statement.lean` | 0 | exact target and statement transport re-elaborated |
| `python3 Stage1_Instances/THM-M-1285/check_anchor_audit.py` | 0 | target fingerprint, manifest pin, installed HEAD, license hash, probes, candidates, and status boundary agreed |
| scoped `rg` over repo-local and all materialized pinned dependency Lean source | 0 | only unrelated finite rearrangement inequality/Schwartz-space names and the local statement appeared; no exact candidate |
| Sourcegraph public Lean search | 0 | `matchCount=0`; response SHA-256 `e3add3c1...45d97` |
| GitHub REST repository search | 0 | `total_count=0`, complete response; SHA-256 `08c082f...600b2` |
| GitHub REST code search | 0 | captured HTTP 401 authentication blocker; SHA-256 `b7dbd17...e29e` |
| immutable formal-conjectures recursive-tree query | 0 | commit confirmed, untruncated 1204-entry tree, zero matching paths; SHA-256 `76fa3f9...efc61` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-1285` | 0 | rank 456, planned, hard anchor/wrapper lane, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1285 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

The downstream proof architecture must account for the distribution function, its generalized
inverse, radii realizing finite superlevel volumes, measurability of the constructed witness,
radial antitonicity, and exact strict-superlevel equimeasurability. An external candidate can be
credited only after immutable revision, exact-type, dependency, license, proof-body, placeholder,
axiom, unsafe/oracle, and local wrapper checks.
