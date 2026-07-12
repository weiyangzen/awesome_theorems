# Intake validation

Base revision: `560c2540d43ab8a1495ff6772047b9ec8ea0f708`.

Validation date: 2026-07-12 (Asia/Shanghai). This validation is limited to manifest membership,
planned-dossier invariants, pinned ingredient elaboration, JSON syntax, and whitespace. It does not
establish an exact Lean statement or any proof closure.

The preflight worktree contains the existing untracked `Formalizations/Lean/.lake` artifact. It was
used read-only. No `lake update`, `lake build`, clone, fetch, or dependency mutation was run.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0665` | exit 0; rank 709, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | exit 0; pre-existing untracked `Formalizations/Lean/.lake` recorded |
| `git rev-parse HEAD` | exit 0; base revision recorded above |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean version and commit recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0665/IntakeProbe.lean` | exit 0; all six pinned ingredient types printed |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both files parsed |
| scoped Python intake assertions | exit 0; planned lifecycle, empty accepted states, open ordered DAG, and fail-closed debt vector verified |
| `rg -n '\\b(sorry|admit|axiom)\\b' Stage1_Instances/THM-M-0665 --glob '*.lean'` | exit 1 as expected; no forbidden Lean declaration or placeholder token found |
| `git diff --check -- Stage1_Instances/THM-M-0665 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

Independent primary-source inspection and review, exact Lean elaboration and mutation tests,
formal-candidate audit, obligation registry, proof, trust closure, hermetic replay, readable
reconstruction, and independent verification remain open. These downstream gates prevent audit and
theorem completion but do not invalidate this planned intake.
