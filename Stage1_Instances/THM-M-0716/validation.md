# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`136ebf643dcdcbc42cef34e415177189578060ef`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, or proof is claimed. The existing canonical `.lake` symlink was
used read-only; no dependency update, build, fetch, or clone was run. The preflight worktree had the
symlink itself as the sole untracked entry: `?? Formalizations/Lean/.lake`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0716` | 0 | rank 755; planned; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` | 0 | preflight showed only the existing untracked canonical `.lake` symlink |
| `git rev-parse HEAD` | 0 | `136ebf643dcdcbc42cef34e415177189578060ef` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-0716/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0716/task-dag.json` | 0 | open task DAG JSON is syntactically valid |
| scoped Python intake assertions | 0 | `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0716/IntakeProbe.lean)` | 0 | seven pinned computability APIs elaborated, including the primitive-to-computable bridge |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0716 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0716` | 0 | no output |

Known downstream failures are intentionally open: exact primary-source selection and independent
review, canonical statement elaboration and mutation tests, obligation and discovery freezes,
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion
but do not invalidate this truthful `planned` intake.
