# Intake validation

## Boundary

This is nonrelease evidence for the `planned` intake node only. The worker clone began at commit
`10064cd912bf0d94ab6c8d818dd3a30551a921cd`, tree
`f7483f57d60b00edad176cef2fa658a87622982d`, with only the automation-provided
`Formalizations/Lean/.lake` link untracked. That link resolves to the canonical pinned dependency
artifacts and was used read-only. No `lake update`, `lake build`, clone, fetch, dependency edit, or
other `.lake` mutation was performed.

The Lean probe authenticates adjacent interfaces only. It does not elaborate a canonical target or
prove structural stability. The receipt is unsigned and non-content-addressed; only the integration
lane can rerun the checks and accept the node.

## Commands and results

All commands were run from the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1366` | 0 | rank 976; planned; L0/rework required; no legacy slot; legacy artifacts unaccepted; theorem complete false |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 | commit and tree shown above |
| `git blame -L 9957,9962 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over the manifest, blueprint, DAG, skill, guidelines, source corpus, Stage0, toolchain, lockfile, and pinned `Flow.lean` | 0 | hashes agree with `instance.json` and `intake-receipt.json` |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake 5.0.0-src+98dc76e; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-1366/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | eight adjacent flow/homeomorphism/conjugacy interfaces elaborated; no target theorem declared |
| bounded `rg -n -i --glob '*.lean' 'structural.?stabil\|rough.?system\|Andronov\|Peixoto\|Morse.?Smale'` over repo-local Lean and pinned mathlib | 1 | expected no match; intake discovery only, not the downstream exhaustive anchor audit |
| Crossref lookup of `10.1201/9780367813758-12` | 0 | returned a 2019 secondary selected-works chapter record, not an inspected 1937 primary theorem; no source credit |
| `python3 -m json.tool` on the three owned JSON files and the worker packet | 0 | all parsed as JSON |
| `PYTHONPYCACHEPREFIX=<temporary-cache> python3 -m py_compile Stage1_Instances/THM-M-1366/check_intake.py` | 0 | scoped validator compiled without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-1366/check_intake.py` | 0 | planned intake invariants, exact nine-file inventory, source pins, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1366/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | worker handoff agrees with the provisional receipt and scoped artifacts |
| prohibited Lean escape scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` | 1 | expected no match |
| `git diff --check -- Stage1_Instances/THM-M-1366 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace diagnostics; these new paths are untracked, so this command alone does not inspect their content |
| per-file `git diff --no-index --check /dev/null <untracked-file>` over the nine owned files and worker packet | 1 for each invocation | expected `1` means a new-file diff was found; no whitespace diagnostics were printed, and the scoped validator independently checked final newlines and trailing whitespace |

## Result

The intake deliverable is self-tested and may be proposed as worker state `[_]`. Its provisional
vector remains `[H5, M4, R4]`. For this intake node, the first unmet acceptance gate is independent
integration-lane replay and master acceptance of a node-specific receipt. Separately, the first
mathematical hard stop for tree construction and dependent statement work is the missing stable
source proposition and canonical Lean target. Source/formal anchor audit, obligation freeze, proof,
trust closure, readable reconstruction, hermetic validation, and release all remain downstream.
Consequently `audit_complete=false` and `theorem_complete=false`.
