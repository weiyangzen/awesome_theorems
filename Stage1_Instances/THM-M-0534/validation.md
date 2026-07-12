# Intake validation

Base revision: `9c62e277cad936290d63af79d788d97dd17bf4cf`.

Validation ran on 2026-07-12 in the worker clone. It is limited to manifest consistency, dossier
structure and invariants, and an elaboration-only probe of relevant pinned Lean interfaces. The
existing `.lake` symlink and dependencies were used read-only; no update, build, clone, or fetch was
run. Because the exact source variant is still open, the probe is not a canonical statement or
kernel-proof result for this target.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0534` | 0 | Rank 591, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0534/IntakeProbe.lean)` | 0 | All six pinned declarations elaborated and their types were printed |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | 0 | Both JSON artifacts parsed |
| scoped Python intake assertions | 0 | `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0534 .stage1-worker-selftest.json` | 0 | No output |

An initial combined invocation incorrectly ran the three repository Python commands from
`Formalizations/Lean`; each exited 2 because the relative script path did not exist there. They were
rerun from the repository root with exit 0 as recorded above. This operator path error did not
mutate inputs or dependencies.

## Known downstream failures

Exact primary-source selection and independent review, the topological specialization decision,
canonical Lean target and mutation tests, terminal-body/axiom anchor audit, obligation registry,
proof, hermetic replay, and independent release validation remain open. They prevent theorem
completion but do not invalidate this `planned` intake. Accepted receipt IDs: none. First downstream
gate: `S56-M-0534-STATEMENT`. Remaining root cut set begins with exact source identity and statement
elaboration.
