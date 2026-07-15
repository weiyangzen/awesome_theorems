# THM-M-1108 proof-phase recheck at 3c3068d5 (slot31)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T12:26:53+08:00` (`Asia/Shanghai`)

Base revision: `3c3068d5f6ad9d773ce52d46d68a43c2a9272683`

Base tree: `f9413d0895f280a855bb16104daf0403d51a24fb`

## Verdict

`blocked`. No placeholder-free proof body for the exact target
`Stage1Instances.THM_M_1108.CanonicalStatement` exists in the owned source,
the repository-local Lean sources outside this dossier, or the pinned mathlib
closure. This attempt adds no Lean proof body, closes no obligation, and leaves
the lifecycle `planned` and root vector `[H2, M3, R3]` unchanged.

The checked declaration
`canonicalStatement_of_poissonized_depoissonized` is only a conditional
composer: it consumes both `PoissonizedAsymptotics` and
`DePoissonizationTransfer`. Neither proposition has an inhabitant in the
validation closure. The immediate root cut therefore remains
`M1108-T-POISSONIZED` plus `M1108-T-DEPOISSONIZE`.

The first unavailable frozen package is `M1108-C-RSK`. Current scoped searches
found no Robinson--Schensted construction with the required LIS/first-row
identity. The Toeplitz-determinant, Riemann--Hilbert, Hastings--McLeod/
Painleve-II, uniform-error, Poissonized-limit, monotonicity/tail, and
de-Poissonization bodies are also absent. The immutable anchor audit supplies
no compatible external Lean 4 proof to pin or import.

The current base differs from the previous recheck base `574eca43...` only by
the integration of that recheck pair under this target. `Statement.lean`,
`ObligationTree.lean`, the frozen registry and graphs, the anchor audit, and the
validation specifications retain their recorded hashes. Independent reviews
of the statement and prior trust-zero semantic probes found no sound vacuity or
inconsistency route.

Assuming a terminal package, adding an analytic axiom, weakening the target,
or presenting the conditional composer as BDJ would violate the frozen target
and the no-placeholder rule. None was added.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`. Resume after the frozen
combinatorial and analytic packages are implemented without placeholders, or
after an immutable compatible Lean 4 BDJ proof becomes available for exact-
type, terminal-body, dependency, trust, license, and provenance validation.

The prescribed root-project `lake env lean` entry point is independently
blocked because the shared read-only `.lake/packages/flt-regular` checkout has
`HEAD` set to `refs/heads/.invalid`. It was not repaired or fetched. This
environment defect is not the mathematical blocker: a direct trust-zero replay
with the pinned Lean binary and existing pinned object paths elaborated all
three target modules.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink was treated read-only. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or `.lake` mutation
was performed. Temporary Lean files and objects were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| `cd Formalizations/Lean && timeout 15s lake env lean --version` | 1 | Lake rejected the shared `flt-regular` checkout because its `HEAD` cannot be resolved; Lean was not invoked through this entry point. |
| Isolated temporary-copy direct replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` using pinned Lean 4.29.0, existing Lake object paths, `--trust=0`, and `-t0` | 0 | Replay exits were `0/0/0`; all modules elaborated, and the transport/composer axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom-like bodyless declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| Pinned-mathlib topical source scan | 1 | Expected no-match exit; no BDJ, Tracy--Widom, Painleve, Hastings--McLeod, LIS, Riemann--Hilbert, Robinson--Schensted, or de-Poissonization terminal declaration was found. |
| Repository-local exact-interface scan outside this owned target and `.lake` | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `poissonizedLISCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |
| `git diff --name-status 574eca43...HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only the preceding `head-574eca43-slot59` blocker pair was added; no proof input changed. |

The direct replay copied the three target modules into a fresh `/tmp`
directory, used the pinned Lean binary with explicit paths to the existing
root, mathlib, and dependency object directories, compiled a temporary
`Statement.olean`, elaborated the remaining modules, and removed the directory.

The word `sorry` printed during `Statement.lean` elaboration is Lean's
diagnostic rendering inside the four expected `#check_failure` mutation probes.
It is not source syntax or an admitted proof; the token-anchored source scan
confirms that distinction.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
