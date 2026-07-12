# Intake validation

Base revision: `c2467750f2cdb3960045c83e819d96687253303d` (tree
`0f79eb697267dc28b29d41a1e282f319d758a2ac`). The initial worktree contained only the
automation-provided untracked `Formalizations/Lean/.lake` link; it was reused read-only and not
modified. No dependency update, build, clone, or fetch command was run.

This validation covers manifest and DAG identity, dossier structure, JSON integrity, source and
environment pins, the six-task open workflow, prohibited constructs, and a narrow pinned Lean API
probe. Because the repository record does not identify a binder-complete proposition, no canonical
target, expression fingerprint, mutation result, obligation, or proof is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard ok: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0643` | 0 | rank 1060, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git status --short --untracked-files=all` before edits | 0 | only `Formalizations/Lean/.lake`; preserved |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib `8a178386ffc0...`, tree `bdc39a312320...`; package worktree clean |
| `rg -n -i --glob '*.lean' 'Nielsen.?fixed\|fixed.?point.?class\|Nielsen.?number\|Reidemeister.?class\|Wecken' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Archive` | 1 | expected no match; bounded intake observation only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0643/IntakeProbe.lean)` | 0 | all eight adjacent fixed-point/homotopy interfaces elaborated; stdout SHA-256 `728b8fb2758e...` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | 0 | all four are valid JSON |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile Stage1_Instances/THM-M-0643/check_intake.py` | 0 | scoped validator compiled without an owned cache file |
| `python3 -B Stage1_Instances/THM-M-0643/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | planned intake invariants, exact nine-file inventory, pins, packet, and six open tasks agree |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0643` | 1 | expected no match |
| `git diff --check -- Stage1_Instances/THM-M-0643 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; the scoped checker also checks final newlines and trailing whitespace |

## Result

The intake deliverable is self-tested and may be proposed as worker state `[_]`. Its provisional
vector is `[H1, M4, R4]`. The named primary Wecken series supports a published-family source lead,
but the first unmet completion gate is integration-lane review and master acceptance of a
node-specific intake receipt. Exact proposition/source admission, canonical Lean elaboration and
mutations, formal anchor audit, obligation freeze, proof, trust closure, readable reconstruction,
hermetic replay, independent validation, and release remain downstream. Consequently
`audit_complete=false` and `theorem_complete=false`.
