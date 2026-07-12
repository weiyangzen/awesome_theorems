# Intake validation

## Boundary

This is nonrelease evidence for the `planned` intake node only. The worker clone began at commit
`d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`, tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`, with only the automation-provided
`Formalizations/Lean/.lake` link untracked. That link resolves to the canonical pinned dependency
artifacts and was used read-only. No `lake update`, `lake build`, clone, fetch, dependency edit, or
other `.lake` mutation was performed.

The Lean probe authenticates adjacent fixed-point and homotopy interfaces only. It does not
elaborate a canonical Nielsen target or prove any fixed-point-class result. The receipt is unsigned
and non-content-addressed; only the integration lane can rerun these checks and accept the node.

## Commands and results

All commands were run from the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0642` | 0 | rank 1059; planned; L0/rework required; no legacy slot; legacy artifacts unaccepted; theorem complete false |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | commit and tree shown above |
| `git blame -L 4755,4760 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over the manifest, blueprint, DAG, skill, guidelines, source corpus, Stage0, toolchain, lockfile, and pinned fixed-point/homotopy sources | 0 | hashes agree with `instance.json` and `intake-receipt.json` |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake 5.0.0-src+98dc76e; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0642/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | eight adjacent fixed-point, closedness, continuous-map, homotopy, and relative-homotopy interfaces elaborated; no target theorem declared |
| `rg -n -i --glob '*.lean' 'Nielsen.?fixed\|fixed.?point.?class\|Nielsen.?number\|Reidemeister.?class' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive` | 1 | expected no match; intake discovery only, not the downstream exhaustive anchor audit |
| four `curl -L --max-time 20 -sS https://api.crossref.org/works/<DOI>` calls for `10.1007/bf01457977`, `10.1007/bf01563622`, `10.1090/conm/014`, and `10.1090/conm/014/01` | 0 | two primary and one secondary bibliographic leads identified; exact response hashes are in `intake-receipt.json`; no proposition or source credit assigned |
| `curl -L --max-time 20 -sS 'https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN235181684_0082/manifest?version=7a696723'` and `curl -L --max-time 30 -sS https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0082/LOG_0012.pdf` | 0 | stable IIIF record and 12-page primary scan located; hashes recorded in the receipt; no theorem-level transcription or review admitted |
| `python3 -m json.tool` on the three owned JSON files and worker packet | 0 | valid JSON |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile Stage1_Instances/THM-M-0642/check_intake.py` | 0 | scoped validator compiled without generated owned files |
| `python3 -B Stage1_Instances/THM-M-0642/check_intake.py` | 0 | planned intake invariants, exact nine-file inventory, source pins, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0642/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | worker handoff agrees with the provisional receipt and scoped artifacts |
| prohibited Lean escape scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` | 1 | expected no match |
| `git diff --check -- Stage1_Instances/THM-M-0642 .stage1-worker-selftest.json` plus direct trailing-whitespace/final-newline checks in `check_intake.py` | 0 | no whitespace diagnostics; direct checks cover all nine owned files and the root worker packet |

## Result

The intake deliverable is self-tested and may be proposed as worker state `[_]`. Its provisional
vector remains `[H5, M4, R4]`. The first unmet completion gate is independent integration-lane
review and master acceptance of a node-specific receipt. Exact source/proposition selection,
canonical Lean elaboration, source/formal anchor audit, obligation freeze, proof, trust closure,
readable reconstruction, hermetic validation, and release all remain downstream. Consequently
`audit_complete=false` and `theorem_complete=false`.
