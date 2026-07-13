# Intake validation

This file records the historical intake-phase validation. Statement-phase commands and results are
recorded separately in `statement-validation.md` and `statement-receipt.json`; later dossier
expansion does not retroactively change the scope or hashes of the intake receipt.
The receipt's bound public projections have since changed during this statement phase, so its
`current_unsuperseded_worker_report` field describes only the historical intake snapshot and is no
longer current authority for those files. `statement-receipt.json` records the superseding
provisional worker snapshot; neither receipt is master-accepted.

Base revision: `67d32ab26aba14b674ae8a1b919e6935812190c3` (tree
`8a1d264cf3331992fbbc3a4fffca285af0b88929`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, scoped intake invariants, and one narrow
pinned Lean discovery probe. It does not freeze or validate a canonical Wilson proposition, audit
a terminal proof body, or confer proof credit. The automation-provided canonical `.lake` symlink
was pre-existing and used read-only; no dependency update, build, clone, fetch, or other `.lake`
mutation was performed. This dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned Wilson module SHA-256:
  `7bd6ec0e909f037f8632e1b495f9647a61fe950f3bfe3af98a5a22914622aeb7`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0476` | exit 0; rank 1357, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 3497,3502 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded repository and pinned-mathlib search for Wilson/factorial congruence declarations | exit 0; direct forward candidate, product form, converse, and iff found in `Mathlib.NumberTheory.Wilson`; unrelated Richard Wilson design target kept outside scope |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0476/IntakeProbe.lean)` | exit 0; six exact-topic APIs elaborated, explicit-primality candidate wrapper and `p=2`, `p=4`, `p=1` boundaries kernel-checked; both inspected candidates reported `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `71ce97c56fdf08f7e416bf54bb2cce03706d0b16382057df4dae12685876d02a` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0476-pycache python3 -m py_compile Stage1_Instances/THM-M-0476/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0476/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest and DAG identity, pins, H1/M3/R4 null-target boundary, receipt, packet, exact inventory, Lean replay, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped `git diff --no-index --check /dev/null <new-file>` loop, followed by `git diff --check -- Stage1_Instances/THM-M-0476 .stage1-worker-selftest.json` | exit 0; every new owned file and the worker packet passed explicit whitespace validation, with no tracked-diff diagnostics |

## Known open gates

At this historical intake snapshot, the exact domain, prime premise, direction, encoding, binders,
fingerprints, transports, and mutations were open. `Statement.lean`, `statement.json`, and
`statement-receipt.json` now freeze and self-test the conventional formal target, while primary or
authoritative source fidelity, pinpoint theorem/page, historical attribution and date audit,
definitions, assumptions, correction or errata review, and independent source approval remain
open. So do formal-anchor and terminal-body provenance, dependency, axiom and TCB audits; discovery
and obligation freezes; typed graphs; proof and composition; readable reconstruction; hermetic
replay; deterministic bundle; independent verification; audit completion; theorem completion; and
master acceptance. These gates prevent any theorem-completion claim.
