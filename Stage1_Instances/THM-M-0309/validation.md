# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`).

All commands ran from the isolated worker clone on 2026-07-13 in timezone `Asia/Shanghai`.
Validation covers target membership, the planned dossier and open DAG, JSON and scoped invariants,
source-record discrimination, adjacent pinned Lean APIs, prohibited constructs, and whitespace.
The automation-provided `.lake` symlink and canonical pinned artifacts were used read only. No Lake
update or build, dependency clone or fetch, or `.lake` modification was performed.

No canonical proposition has been selected. The Lean probe is substrate evidence only and neither
elaborates nor proves the Rellich-Kondrachov target.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0309` | 0 | rank 1050, planned, `L0/rework_required`, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read only |
| `git blame -L 2216,2221 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa...` |
| `python3 -m json.tool Stage1_Instances/THM-M-0309/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0309/task-dag.json` | 0 | valid JSON |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0309/IntakeProbe.lean)` | 0 | six `L^p`, compact-operator, bounded-image, and Sobolev-inequality API checks elaborated; no target theorem was stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `rg -nil --glob '*.lean' 'Rellich\|Kondrachov\|RellichKondrachov' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match result; bounded pinned-mathlib name search only, not a comprehensive anchor audit |
| `sha256sum` on the toolchain, Lake lock, assurance inputs, and three probed mathlib modules | 0 | digests recorded in `instance.json` and `intake-receipt.json` |
| `python3 -B Stage1_Instances/THM-M-0309/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned H5/M4/R4 boundary, null formal target, exact inventory, source hashes, packet agreement, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0309` | 1 | expected no-match result; no prohibited proof or declaration construct in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and `.stage1-worker-selftest.json` | 0 | no whitespace diagnostics; exit 1 with empty output from each no-index comparison is the expected content-difference result |
| `git diff --check -- Stage1_Instances/THM-M-0309 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; untracked files are covered by the preceding per-file checks |

Known downstream failures remain deliberately open: an approved immutable source and duplicate-ID
decision; exact mathematical statement, definitions, assumptions, endpoints, and independent
review; canonical Lean target, minimal imports, expression/environment fingerprints, transports,
and mutation tests; formal anchor and terminal-body audit; obligation and graph freezes; proof and
composition; trust closure; hermetic replay; deterministic evidence bundle; independent release
verification; and master acceptance. They prevent statement and theorem completion but do not
invalidate this truthful `planned` intake.
