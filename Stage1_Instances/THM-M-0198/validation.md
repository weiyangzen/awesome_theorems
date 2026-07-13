# Intake validation

## Scope and environment

This record validates only the `planned` intake dossier for `S56-M-0198-INTAKE`: target identity,
the literal forward source boundary, proposition-changing choices, adjacent noncredited pinned
interfaces, the discovery-only Lean probe, and the six open downstream tasks. It does not validate
a canonical Simson statement, a source-to-Lean transport, a proof body, or any theorem-completion
gate.

- Validation date: `2026-07-13`, timezone `Asia/Shanghai`.
- Base revision: `48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0`.
- Base tree: `0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`.
- Initial worker status contained only the automation-provided untracked
  `Formalizations/Lean/.lake` symlink. It was used read-only, making this nonrelease dirty-worker
  evidence.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake: `5.0.0-src+98dc76e`.
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0198` | 0 | rank 1530; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | initial status contained only the shared `.lake` symlink; base revision/tree as above |
| `git blame -L 1429,1434 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; clean package worktree |
| exact-topic `rg` search over pinned mathlib and repository Lean for Simson, Wallace-Simson, pedal-line, and projection-foot collinearity declarations | 1 | expected no-match; no exact root located in this bounded intake search |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0198/IntakeProbe.lean` | 0 | eight adjacent geometry interfaces elaborated; stdout 1864 bytes, SHA-256 `e93d8f2e41131d15910bfc7262bac71eedd9d604cb791aeb5d0772f75833aea9`; no target or proof body declared |
| `python3 -m json.tool` on the scoped JSON artifacts and worker packet | 0 | instance, open task DAG, provisional receipt, and packet parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0198-pycache python3 -m py_compile Stage1_Instances/THM-M-0198/check_intake.py` | 0 | checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0198/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, current hashes, null formal target, H1/M3/R4 boundary, exact inventory, packet, and six open tasks agreed |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 | no whitespace diagnostics; each no-index exit 1 represented only an expected new-file difference |

## Open gates

The first failed downstream gate is exact source-statement identity. No immutable, independently
reviewed theorem source fixes the ambient plane, triangle nondegeneracy, forward direction,
circumcircle encoding, circle-point boundary, supporting side lines rather than closed segments,
perpendicular-foot construction, collinearity packaging, historical attribution, proof boundary,
corrections, or errata. The canonical Lean expression, minimal imports, expression and environment
fingerprints, checked transports, and four statement mutation classes therefore remain open.

The exhaustive anchor and provenance audit, obligation registry, typed graphs, proof and
composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence
bundle, independent verification, master acceptance, audit completion, and theorem completion also
remain open. These failures do not invalidate this fail-closed self-tested `planned` intake.
