# THM-M-1084 proof-phase blocker

## Verdict

`S56-M-1084-PROOF` is blocked and remains unclaimed. No exact proof body was added, and no
`.stage1-worker-selftest.json` is emitted. The canonical target remains
`Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget` with root machine state `M3`.

## First failed gate

The first failed proof gate is exact repo-local kernel closure for the two frozen root-cut
obligations:

- `M1084-T-INTEGRABLE`: integrability of the samplewise based supremum;
- `M1084-T-ENTROPY`: the constant-12 open-ball entropy-integral inequality.

The pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains Gaussian-process,
covering-number, and finite-pair-reduction substrate, but a scoped source search found no Dudley or
generic-chaining expected-supremum theorem. The only audited substantive Lean candidate is
`YuanheZ/lean-stat-learning-theory` at commit
`be5d5a8a1a1f46f2ec9502980ff10a39e17e3820`, declaration `SLT.dudley`. It is not in the local Lake
dependency closure and does not prove the frozen proposition: it assumes a sub-Gaussian MGF
process, sample continuity, measurability, and exponential integrability; uses closed-ball
`WithTop` covering numbers; has constant `12 * sqrt 2 * sigma`; and does not supply the required
supremum-integrability conjunct. Consequently an import or wrapper would be both unavailable and a
statement substitution.

The existing theorem
`Stage1Instances.THM_M_1084.root_of_integrability_and_entropy_packages` is only a checked
child-to-parent composition term. Its two arguments are the open packages above, so it is not a
proof body for either child or for the root.

## Required reopen condition

Resume proof execution only after one of these conditions holds:

1. a compatible immutable Dudley implementation is already present in the pinned dependency
   closure, together with checked bridges for Gaussian MGF, covering-number and endpoint
   normalization, the exact constant, sample separability, and supremum integrability; or
2. the frozen native obligations `M1084-N-GAUSSIAN-MGF` through `M1084-L-LIMIT` receive substantive
   local Lean proof bodies, from which both terminal packages can be derived.

Fetching or changing `.lake` was prohibited for this worker and was not attempted.

## Validation record

Environment: repository base `d83bcd9bb91558d5f3e2cd99f964cc161d7a0cc5`, Lean
`leanprover/lean4:v4.29.0`, pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, validation date `2026-07-12`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed for 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed; ranks are 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1084` | 0 | Confirmed rank 526, planned lifecycle, and `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1084/check_statement.py` | 0 | Exact statement elaborated; three structural mutations were rejected and the singleton boundary proof checked. |
| `python3 Stage1_Instances/THM-M-1084/check_anchor_audit.py` | 0 | Pinned substrate and immutable external near-candidate audit passed, with fail-closed status. |
| `python3 Stage1_Instances/THM-M-1084/check_obligation_tree.py` | 0 | Sixteen-node, 36-edge registry passed; output explicitly reports root open and both terminal packages `M4`. |
| `lake env lean Stage1_Instances/THM-M-1084/Statement.lean` (from `Formalizations/Lean`, using the corresponding relative path) | 0 | The canonical target elaborated with one unused-variable linter warning. |
| `lake env lean Stage1_Instances/THM-M-1084/AnchorAudit.lean` (from `Formalizations/Lean`, using the corresponding relative path) | 0 | All six pinned mathlib declaration probes and both fail-closed audit theorems elaborated. |
| Copy `Statement.lean` and `ObligationTree.lean` to a temporary directory under `Formalizations/Lean`, compile `Statement.olean`, then run `LEAN_PATH=<temporary>:$(lake env printenv LEAN_PATH) lake env lean <temporary>/ObligationTree.lean` | 0 | The conditional composition theorem elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. Temporary files were removed. |
| `rg -n -i 'dudley\|chaining_bound\|entropy.*bound\|subGaussian.*sup' Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances --glob '*.lean'` | 0 | Only this target's Dudley dossier and an unrelated topological-entropy result matched; no pinned terminal theorem was found. |

These commands validate the blocker and prerequisite artifacts only. They are not proof-phase
self-test evidence and do not justify `[_]`, `M0-*`, audit completion, or theorem completion.
