# Anchor-audit validation record

Item: `S56-M-0586-ANCHOR_AUDIT`  
Base revision: `6ba79369e24bfba400ebdfd7dbacd4fd64e18d2c`

## Result

The exact local artifact remains the proposition
`Stage1Instances.THMM0586.HighDimensionalPoincareTarget`, not a proof declaration. Pinned mathlib
at `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the manifold, sphere, homotopy, and
homeomorphism substrate. Its apparent terminal name
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` occurs under `proof_wanted`, however, and
is not exported as an environment constant. It is therefore a statement anchor, not an upstream
theorem eligible for a wrapper.

The credible external candidate inspected was
`lean-dojo/LeanMillenniumPrizeProblems@540da94826f70f3edf4d4fc66ce6cda20e903f61`.
Its `GeneralizedPoincareConjecture` is a proposition definition. Its explicit proof bodies establish
a discrete-space bridge and the generalized conjecture only at `n = 0`, not the selected `n >= 5`
target. The source blob, bytes, toolchain, and Apache-2.0 license were checked at that immutable
revision. Adding it as a dependency would introduce a Lean 4.26 toolchain mismatch without adding
a terminal proof.

Consequently the exact root remains `M4` with `formalization_debt`. There is no discovered
`repo_local_integration_debt`, because neither audited upstream supplies a terminal high-dimensional
proof to integrate. This is a completed bounded anchor-audit node pending master acceptance, not
full audit completion, theorem completion, or a claim of exhaustive global absence.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Lean used only the existing pinned `.lake`
artifacts. No dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0586/AnchorAudit.lean` | 0 | eight usable pinned mathlib declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0586/Statement.lean` | 0 | exact statement and checked broader-to-selected transport re-elaborated |
| expected-failure probe: import the Poincare module then `#check ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` | 1 | `unknown constant`; confirms the `proof_wanted` marker is not an exported proof declaration |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | audit invariants, exact statement hash, marker boundary, eight probes, and installed mathlib HEAD agreed |
| `rg -l -i 'h.?cobord\|s.?cobord\|surgery exact\|generalized poincar\|poincare conjecture\|nonempty_homeomorph_sphere' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | only `Mathlib/Geometry/Manifold/PoincareConjecture.lean` matched in pinned mathlib source |
| immutable GitHub API/raw inspection of `LeanMillenniumPrizeProblems@540da948...` | 0 | source blob `4ef88f...`, source SHA-256 `045a97...`, Lean 4.26 toolchain, dimension-zero proof only |
| `curl ... 'https://api.github.com/search/repositories?q=%22Poincare+conjecture%22+Lean&per_page=10'` | 0 | `total_count=0`, complete response; SHA-256 `08c082...`; bounded discovery evidence only |
| GitHub REST code search | 401 | authentication unavailable; no negative result claimed from this lane |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | rank 117, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0586` | 0 | no whitespace errors |

## Open integration gate

Reopen integration only for a concrete proof-bearing Lean 4 declaration at an immutable revision.
It must match the exact target through a checked transport and pass proof-body, placeholder, axiom,
unsafe/oracle, dependency, toolchain, and license checks. Until then no `M0-L`, `M0-W`, `M0-P`, or
theorem-completion credit is valid.
