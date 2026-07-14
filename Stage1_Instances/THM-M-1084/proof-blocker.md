# THM-M-1084 proof-phase blocker

## Verdict

`S56-M-1084-PROOF` now has self-tested partial proof progress, but the exact root remains blocked.
`GaussianMGFBridge.lean` closes the frozen Gaussian-to-sub-Gaussian MGF leaf at the exact canonical
distance, while `CoveringNets.lean` implements positive-radius finite-cover existence, attainment of
the custom natural covering number, and its positivity on nonempty spaces. The worker packet
proposes `[_]` only for this proof-phase contribution. The canonical target remains
`Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget` with root machine state `M3`.

## First failed gate

The first failed proof gate is exact repo-local kernel closure for the two frozen root-cut
obligations:

- `M1084-T-INTEGRABLE`: integrability of the samplewise based supremum;
- `M1084-T-ENTROPY`: the constant-12 open-ball entropy-integral inequality.

The new local bodies do not construct chaining parent maps, control a finite maximum, prove the
constant-12 sum-to-integral comparison, or pass from countable approximants to the sample
supremum. Thus they do not inhabit either terminal root-cut package. The pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` still contains no Dudley or generic-chaining
expected-supremum theorem. The only audited substantive terminal candidate is
`YuanheZ/lean-stat-learning-theory` at commit
`be5d5a8a1a1f46f2ec9502980ff10a39e17e3820`, declaration `SLT.dudley`. It is not in the local Lake
dependency closure and does not prove the frozen proposition: it assumes a sub-Gaussian MGF
process, sample continuity, measurability, and exponential integrability; uses closed-ball
`WithTop` covering numbers; has constant `12 * sqrt 2 * sigma`; and does not supply the required
supremum-integrability conjunct. Consequently an import or wrapper would be both unavailable and a
statement substitution.

The exact local declaration
`Stage1Instances.THM_M_1084.Proof.increment_hasSubgaussianMGF` proves
`HasSubgaussianMGF (X_s-X_t) (toNNReal (dist s t)^2) mu` from the frozen Gaussian, centering, and
canonical-distance premises. Its MGF identity and scalar Gaussian bridge are sorry-free and use
only `propext`, `Classical.choice`, and `Quot.sound`. The finite-net bodies have the same axiom
profile. These are real proof bodies, not assumptions, but they do not close the root.

The existing theorem
`Stage1Instances.THM_M_1084.root_of_integrability_and_entropy_packages` is only a checked
child-to-parent composition term. Its two arguments are the open packages above, so it is not a
proof body for either child or for the root.

## Required reopen condition

Continue proof execution through one of these routes:

1. a compatible immutable Dudley implementation is already present in the pinned dependency
   closure, together with checked bridges for Gaussian MGF, covering-number and endpoint
   normalization, the exact constant, sample separability, and supremum integrability; or
2. extend the now-implemented Gaussian-MGF and finite-net foundations with substantive local bodies
   for `M1084-C-CHAIN`, `M1084-L-MAX-INCREMENT`, `M1084-L-DYADIC-SUM`, and `M1084-L-LIMIT`, then
   derive both terminal packages.

Fetching or changing `.lake` was prohibited for this worker and was not attempted.

## Validation record

Environment for the current partial proof: repository base
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`, Lean
`leanprover/lean4:v4.29.0`, pinned mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, validation date `2026-07-15`.

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
| `bash Stage1_Instances/THM-M-1084/check_proof.sh` | 0 | Isolated `--trust=0` elaboration passed for the exact Gaussian-MGF and finite-net bodies; seven gate-audited declarations were sorry-free and each axiom set was a subset of `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n -i 'dudley\|chaining_bound\|entropy.*bound\|subGaussian.*sup' Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances --glob '*.lean'` | 0 | Only this target's Dudley dossier and an unrelated topological-entropy result matched; no pinned terminal theorem was found. |

These commands self-test substantive partial proof work and justify only a provisional worker
`[_]` handoff for this proof phase. They do not justify root `M0-*`, validation, release, audit
completion, master acceptance, or theorem completion.
