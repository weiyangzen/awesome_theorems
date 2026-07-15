# THM-M-1108 proof-phase recheck at 443b8bbc (slot59)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T12:05:00+08:00` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No placeholder-free proof body inhabiting the exact target
`Stage1Instances.THM_M_1108.CanonicalStatement` was found in the owned source,
the repository-local Lean sources outside this dossier, or the pinned mathlib
closure. This recheck adds no Lean proof body and closes no obligation. The
lifecycle remains `planned`, and the observed proof-architecture root vector
remains `[H2, M3, R3] -> [H2, M3, R3]`.

The only checked child-to-root declaration is
`canonicalStatement_of_poissonized_depoissonized`. It consumes
`PoissonizedAsymptotics` and `DePoissonizationTransfer` as premises; neither
proposition has an inhabitant in the validation closure. The immediate root cut
therefore remains `M1108-T-POISSONIZED` plus `M1108-T-DEPOISSONIZE`.

The first unavailable frozen package is `M1108-C-RSK`: the scoped repository
and pinned-mathlib searches found no checked Robinson-Schensted correspondence
with the required LIS/first-row identity. The later Toeplitz-determinant,
Riemann-Hilbert steepest-descent, Hastings-McLeod/Painleve-II, uniform-error,
Poissonized-limit, monotonicity/tail, and de-Poissonization bodies remain absent.
The prerequisite immutable anchor audit identifies no compatible Lean 4 proof
to pin or import.

Relative to base `a23d86cd84f03c26102b43c6b1b3b6d0a7a31e61`, the
current base added only the preceding slot67 blocker Markdown and JSON under
this target. `Statement.lean`, `ObligationTree.lean`, the frozen registry and
typed graphs, the anchor audit, and the validation specifications are unchanged.
Fresh repository-local and pinned-mathlib scans found no new proof candidate.

Assuming either terminal package, introducing an analytic axiom, weakening the
target, or presenting the conditional composer as BDJ would be a prohibited
placeholder or theorem substitution. No such declaration was added.

An independent trust-zero semantic probe also established
`not_zero_cdf : not (IsTracyWidomCDF (fun _ => 0))` from the defining
exponential field and `Real.exp_ne_zero`. This rules out the most obvious zero
model but does not prove the model predicate empty and supplies no root proof.
No justified inconsistency or vacuity was found.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`: no compatible body was
found in the scoped local searches. Resume only after the frozen combinatorial
and analytic packages are implemented without placeholders, or after an
immutable compatible Lean 4 BDJ proof becomes available for exact-type,
terminal-body, dependency, trust, license, and provenance validation in the
pinned environment.

The prescribed `lake env lean` entry point is additionally blocked on this
base because the automation-provided shared `.lake/packages/flt-regular` checkout
has an invalid `HEAD`. It was not repaired or fetched because the worker must
not mutate `.lake`. This environment fault is not the mathematical proof
blocker: a trust-zero direct Lean replay against the existing pinned mathlib
object paths still elaborated all three target modules.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink was treated as read-only. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary Lean objects were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 1 | Lake rejected the shared `flt-regular` package because its `HEAD` cannot be resolved; no elaboration ran through this entry point. |
| Isolated temporary-copy three-module direct Lean replay shown below, using the pinned toolchain binary and existing Lake object paths with `--trust=0` and `-t0` | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` elaborated. The exact statement transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Independent temporary `not_zero_cdf` semantic probe with the same direct trust-zero environment | 0 | The zero function cannot satisfy `IsTracyWidomCDF`; this closes no frozen obligation and gives no vacuity proof. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| Pinned-mathlib topical source scan | 1 | Expected no-match exit; no BDJ, Tracy-Widom, Painleve, Hastings-McLeod, LIS, Riemann-Hilbert, Robinson-Schensted, or de-Poissonization terminal declaration was found. |
| Repository-local exact-interface scan outside this owned target and `.lake` | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `poissonizedLISCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |
| `git diff --name-status HEAD^..HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only the preceding `head-a23d86cd-slot67` blocker pair was added; no proof input changed. |

The direct replay used the pinned Lean 4.29.0 binary and an explicit
`LEAN_PATH` consisting of the toolchain library plus the existing pinned
mathlib dependency object directories. It copied `Statement.lean`,
`ObligationTree.lean`, and `AnchorCandidates.lean` into a fresh `/tmp`
directory, compiled the statement to a temporary `Statement.olean`, elaborated
the other two modules, printed exits `0/0/0`, and removed the directory.

The word `sorry` printed during `Statement.lean` elaboration is Lean's
diagnostic rendering inside four expected `#check_failure` mutation probes. It
is not source syntax or an admitted proof; the token-anchored source scan
confirms that distinction.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
