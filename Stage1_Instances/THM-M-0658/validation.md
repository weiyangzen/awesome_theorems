# Intake validation

Base revision: `734cdf53ab1cc41c766d2a40058a1929f6e1311a`.

Validation date: 2026-07-12 (Asia/Shanghai). This evidence covers only manifest membership, the
planned dossier's structure and fail-closed invariants, JSON syntax, whitespace, and a narrow Lean
elaboration probe of already pinned model-theory ingredients. It is not the statement gate and
does not establish a theorem proposition or proof.

The preflight worktree contained the existing untracked `Formalizations/Lean/.lake` link. Its
canonical target was used read-only. No `lake update`, `lake build`, clone, fetch, or dependency
mutation was run.

## Environment fingerprint

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0658` | exit 0; rank 703, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| repository search for `THM-M-0658`, the Chinese title, Shelah stability, and the 1978 record | exit 0; found the underspecified catalog record and no target-specific dossier or exact proposition |
| pinned-mathlib search for model-theoretic Shelah, stable theory, stability theory, order property, forking, and superstability | exit 1 for the theorem-specific search; no matching model-theory API was located |
| inspection of `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_299.lean` | exit 0; different target `THM-M-0660`, with an explicitly limited type-counting proxy and open parameter/model scope |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0658/IntakeProbe.lean` | exit 0; theory, model, completeness, complete-type, type-space, and formula/sentence ingredients elaborated |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | exit 0; both are valid JSON |
| scoped dossier assertions and forbidden Lean-token scan | exit 0; seven declared artifacts present, planned lifecycle, empty accepted state, all downstream tasks open, and no `sorry`, `admit`, or `axiom` in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0658 .stage1-worker-selftest.json` | exit 0; no output |

One initial combined validation command changed into `Formalizations/Lean` without a subshell, so
its subsequent root-relative JSON and search paths failed and the final `git -C` path was invalid.
No files or dependencies were changed by that attempt. The corrected subshell command above was
then run and exited 0; only the corrected results are used as positive evidence.

## Status boundary

The first open downstream gate is exact source-statement identity. Primary-source selection and
review, canonical Lean elaboration and fingerprint, transports and mutations, formal-candidate
audit, obligation registry, proof, source/readability review, hermetic replay, and independent
verification all remain open. These prevent audit and theorem completion but do not invalidate a
self-tested planned intake.
