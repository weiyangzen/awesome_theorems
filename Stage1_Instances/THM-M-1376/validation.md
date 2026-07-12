# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and duplicate-scope boundary, open task DAG,
JSON and scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical
Poincare recurrence statement or proof because neither has been frozen. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. The dirty worker evidence is nonrelease evidence.

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

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1376` | 0 | rank 986; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; final status contains it plus the owned intake and root packet |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 10027,10032 -- Docs/researches/math_theorems.md`; same for lines 11108-11113 | 0 | both six-line catalog records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded repository source, duplicate dossier, and candidate inspection | 0 | confirmed absent exact proposition, identical THM-M-1521 metadata, stronger physics wording, historical lead, foreign candidate, and open physical bridges; discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status check | 0 | pinned revision and tree recorded above; source status clean |
| `sha256sum` on the toolchain, manifest, pinned recurrence source, legacy foreign wrapper, and duplicate intake/statement | 0 | all hashes match `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1376/IntakeProbe.lean)` | 0 | nine adjacent APIs and the foreign candidate expression type elaborated; 30-line output SHA-256 `8eeaf030f3e9c63f3b1944dd36c636561ef1e1ed9ccb57afa882c561ea9d1f4f`; no theorem declared |
| bounded exact-topic `rg` search in pinned mathlib, repo-local Lean, and the foreign dossier | 0 | found the pinned recurrence family and THM-M-1521 wrappers; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| Python `ast.parse` of `check_intake.py` | 0 | scoped validator parses without bytecode output |
| `python3 -B Stage1_Instances/THM-M-1376/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/duplicate identity, hashes, H1/M4/R4 null target, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1376/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 | no whitespace diagnostics for any changed artifact |

## Known open gates

Canonical root selection, an accepted immutable source edition and proposition, complete definition,
premise, conclusion, proof-boundary, translation, and correction crosswalk, `THM-M-1521` identity
and root-ownership reconciliation, and independent source review remain open. So do the canonical
Lean expression and environment fingerprints, checked transports, statement mutations, exhaustive
formal anchor audit, discovery protocol, obligation registry, typed graphs, proof and composition,
trust and provenance closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These
failures do not invalidate a truthful self-tested `planned` intake.
