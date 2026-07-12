# THM-M-0012 Intake Validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). The initial worktree contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts.
It was used read-only, so this packet is nonrelease evidence. No `lake update`, `lake build`, clone,
fetch, or dependency mutation was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0012` | 0 | rank 1062, planned, no legacy slot, theorem_complete false |
| `git status --short` | 0 | initial status contained only the pre-existing `.lake` symlink |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree match this record |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a178386...a95`, tree `bdc39a31...c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0012/IntakeProbe.lean)` | 0 | printed the exact types of seven complex-polynomial and algebraic-closedness candidate APIs; no diagnostics |
| `python3 -m json.tool` on the structured owned JSON artifacts and worker packet | 0 | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0012-pycache python3 -m py_compile Stage1_Instances/THM-M-0012/check_intake.py` | 0 | scoped validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0012/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, exact artifact inventory, packet agreement, and six open tasks pass |
| `python3 -B Stage1_Instances/THM-M-0012/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over the owned Lean probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` over all new files | 0 aggregate after treating exit 1 as the expected new-file difference | no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0012 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Evidence boundary

The Lean command checks only that the named pinned types and declarations elaborate. It does not
freeze or mutation-test a canonical target, establish a normalized-expression fingerprint, inspect
terminal proof provenance or axioms, or credit `Complex.exists_root` to this target. The source
edition and independent review, statement gate, full anchor audit, obligation registry and typed
graphs, proof/composition gates, hermetic replay, deterministic release bundle, and independent
verification all remain open. These boundaries prevent audit and theorem completion but do not
invalidate the self-tested `planned` intake.
