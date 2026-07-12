# Intake validation

Base revision: `1f79a3f74a8e206d44c27513f4016a26dd7050e3` (tree
`5024086eeb6994ff53242ac82b32b2d9af8b2462`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, pinned
environment identity, a narrow Lean API probe, bounded local name searches, proof-escape hygiene,
and whitespace. The source record is not a proposition, so elaborating a purported canonical Lean
target would invent missing mathematics. `IntakeProbe.lean` therefore checks only possible
substrate; it introduces no theorem and supplies no statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1411` | 0 | rank 910, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1411/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1411/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1411/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after worker manifest finalization |
| `python3 Stage1_Instances/THM-M-1411/check_intake.py` | 0 | target identity, H5/M4/R4 planned boundary, null target, empty accepted state, artifact inventory, and six open tasks agree |
| `python3 -m py_compile Stage1_Instances/THM-M-1411/check_intake.py` | 0 | intake validator compiles |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1411/IntakeProbe.lean)` | 0 | eight pinned flow, invariant-set, fixed/periodic-point, manifold-derivative, and tangent-map API checks elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| bounded exact-topic search under pinned `Mathlib/Dynamics` | 1 | expected no-match exit; no hyperbolic-dynamics, hyperbolicity, uniformly-hyperbolic, Anosov, or Axiom A name found; intake discovery only |
| bounded broad `hyperbolic\|anosov` search under pinned mathlib | 0 | hits concern hyperbolic geometry/trigonometry, an ODE comment, and `Matrix.IsHyperbolic`; none identifies this target |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, or `constant` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1411 .stage1-worker-selftest.json` plus `git diff --check --no-index /dev/null <owned-file>` and owned-file invariants | 0 / 1 | no whitespace diagnostics; no-index exit 1 means the new file differs from `/dev/null`, while the validator independently checks every untracked owned file |

Known downstream failures remain deliberately open: an approved target correction with immutable
primary-source theorem identity and independent review; exact binders, hypotheses, conclusion, and
boundary cases; canonical Lean elaboration, expression/environment fingerprints, checked
transports, and mutations; immutable formal anchor audit; discovery and obligation freezes; proof
and composition; hermetic replay; deterministic evidence bundling; independent release
verification; and master acceptance. These block ordinary theorem execution and completion but do
not invalidate a truthful, self-tested `planned` intake.
