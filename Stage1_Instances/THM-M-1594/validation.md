# Intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic observation metadata, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, a turbo-code formalization, a proof, an accepted receipt,
audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, or other target path was modified.

## Environment

- Repository base: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`
- Base tree: `9d7c8fe49a4c859d90f3069dc47973ffc5ced768`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

The 1993 paper metadata was inspected as a bounded bibliographic lead. The observed Crossref
response SHA-256 was `6f41318b05a543742d3e89197c3b3d93644b90a8c78d109fce2a97b639b0a277`.
The observed Unpaywall response SHA-256 was
`84fc3a15abece1efce02b7e619c9858109c6c3f79b2e4b22927b0c2c32c07dcb` and reported no open
repository copy. These mutable external responses were not vendored and are nonrelease discovery
evidence, not primary-source or H0 evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1594` | 0 | rank 1214, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit and tree matched the values above |
| bounded `rg` over pinned mathlib and repo-local Lean | 0/1 by query | no exact turbo/RSC/BCJR/BER/FER/SNR/capacity terminal declaration located; generic neighboring APIs only; not an absence proof |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1594/IntakeProbe.lean` | 0 | 12 adjacent pinned APIs elaborated; no target theorem or proof body introduced |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=<temporary-cache> python3 -m py_compile Stage1_Instances/THM-M-1594/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1594/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token |
| `git diff --check -- Stage1_Instances/THM-M-1594 .stage1-worker-selftest.json` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structural and whitespace results are recorded after receipt and worker-packet creation.
The Lean probe's exact stdout SHA-256 is
`3db7597b3db88bb80baf4f7451a17c41d31c867014ec8959a1c0a5070cf27e45`.

## Known failures and boundary

Master acceptance is pending. The catalog family/performance gloss still lacks a selected exact
proposition. Primary-source admission, independent source/coding-theory review, formal target and
mutation certificate, exhaustive anchor audit, obligation registry, typed graphs, proof,
composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle, and
independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
