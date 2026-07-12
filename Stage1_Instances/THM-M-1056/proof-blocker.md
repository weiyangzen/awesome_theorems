# THM-M-1056 proof-phase blocker

Item: `S56-M-1056-PROOF`  
Base revision: `3b63151e2ffc641581291b8b5a468cc84c49054a`  
Attempt date: 2026-07-12 (Asia/Shanghai)

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body was
added, no frozen obligation was marked closed, and no worker self-test manifest
was written.

The exact target requires a measurable invariant Lyapunov splitting for every
finite-dimensional real invertible cocycle satisfying the forward and inverse
log-integrability hypotheses. The existing `ObligationTree.lean` proves only
conditional composition: `root_of_oseledetsCorePackage` takes the complete
`OseledetsCorePackage` as a premise. Consequently that declaration cannot supply
proof credit for the target.

The first failed root cut is `M1056-T-CORE`. Its unresolved root-critical
children include:

- `M1056-L-KINGMAN`: an exact integrable subadditive ergodic theorem;
- `M1056-C-FORWARD-FLAG` and `M1056-C-BACKWARD-FLAG`: measurable two-sided
  Lyapunov filtrations;
- `M1056-L-TRANSVERSAL` and `M1056-C-PROJECTIONS`: a measurable direct-sum
  splitting and strongly measurable complementary projections;
- `M1056-L-EQUIVARIANCE` and `M1056-L-GROWTH`: intertwining and simultaneous
  vector-growth limits on one conull set;
- `M1056-N-COORDINATES`: transport from matrix/Euclidean formulations to the
  frozen arbitrary finite-dimensional normed Borel fiber.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` has no named
Oseledets or Kingman terminal declaration. The immutable external candidate
audited in `anchor-audit.md`,
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`,
does not inhabit the frozen target: it is matrix/Euclidean and submodule based,
has no checked projection/coordinate transport, and requires Lean `4.30.0-rc2`
with a different mathlib revision. Fetching or rebuilding that moving dependency
would also violate the worker validation policy. It therefore remains an
anchor-only `E3` candidate rather than an imported proof body.

## Validation evidence

Commands ran in the worker clone using the pre-existing canonical pinned
`.lake` symlink. No `lake update`, `lake build`, clone, fetch, or dependency
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Confirmed rank 248, `planned`, `rework_required: true`, and `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | Passed 19 frozen obligations and 49 typed edges; reported root open at M3 and the Oseledets core at M4. |
| `rg -n '\\b(sorry\|admit\|axiom)\\b\|sorryAx' Stage1_Instances/THM-M-1056 --glob '*.lean'` | 1 | No prohibited proof token occurs in the owned Lean sources; exit 1 means no match. |
| `rg -n -i '(^\|[^A-Za-z])(oseledets\|multiplicative ergodic\|kingman)([^A-Za-z]\|$)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No named terminal Oseledets or Kingman declaration was found; exit 1 means no match. |
| pinned `lake env which lean`/`printenv LEAN_PATH`, then isolated `lean -o /tmp/THM-M-1056-Statement.olean Statement.lean` and `lean ObligationTree.lean` | 0 | The exact statement and conditional composition elaborated; only unused-binder warnings were emitted. `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. Temporary output was removed. |

The pre-existing untracked `Formalizations/Lean/.lake` symlink makes this
nonrelease evidence and was not modified by this worker.

## Required unblock condition

Provide placeholder-free Lean bodies at the frozen types for the Kingman,
two-sided flag, transversality, measurable-projection, equivariance, growth, and
coordinate-transport branches, or import an immutable dependency with checked
exact transports and a compatible pinned toolchain. Then construct
`OseledetsCorePackage` without assuming it and re-run exact-type, axiom,
placeholder, provenance, and composition checks. Until then the root remains
open at `[H1, M3, R3]`, and this proof item cannot truthfully receive `[_]` or
theorem-completion credit.
