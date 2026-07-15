# THM-M-1108 proof-phase recheck at 1bd31e01 (slot61)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T07:59:50+08:00` (`Asia/Shanghai`)

Base revision: `1bd31e0190d9876c44cc5b7200e07a90c43662eb`

Base tree: `50ea1b05b3ad98c930290a5908f50ae3b5b402cf`

## Verdict

`blocked`. No placeholder-free proof body inhabiting the exact target
`Stage1Instances.THM_M_1108.CanonicalStatement` was found in the owned source,
the scoped repository-local Lean sources outside this dossier, or the pinned
mathlib closure. This recheck adds no Lean proof body and closes no obligation.
The lifecycle remains `planned`, and the root vector remains
`[H2, M3, R3] -> [H2, M3, R3]`.

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

Since base `78df0e1c`, the only changes under this target are the preceding
slot61 proof-recheck Markdown and JSON. The statement, obligation interfaces,
frozen registry, typed graphs, anchor audit, and validation specifications retain
their recorded hashes. Fresh repo-local and pinned-mathlib scans found no new
proof candidate. Assuming either terminal package, introducing an analytic axiom,
weakening the target, or presenting the conditional composer as BDJ would be a
prohibited placeholder or theorem substitution. No such declaration was added.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`: no compatible body was
found in the scoped local searches. Resume only after the frozen combinatorial
and analytic packages are implemented without placeholders, or after an
immutable compatible Lean 4 BDJ proof becomes available for exact-type,
terminal-body, dependency, trust, license, and provenance validation in the
pinned environment.

## Validation

All commands ran in this worker clone using the automation-provided pinned Lake
artifacts. The pre-existing untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network operation, or `.lake` mutation was performed. Temporary Lean objects
were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| Isolated temporary-copy three-module `lake env lean` replay shown below, with `--trust=0` and `-t0` | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` elaborated. The exact statement transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| Pinned-mathlib topical source scan | 1 | Expected no-match exit; no BDJ, Tracy-Widom, Painleve, Hastings-McLeod, LIS, Riemann-Hilbert, Robinson-Schensted, or de-Poissonization terminal declaration was found. |
| Repo-local exact-interface scan outside this owned target and `.lake` | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `poissonizedLISCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |
| `git diff --name-status 78df0e1ce628d7e18e48441678ad85f9552d1b77..HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only the preceding `head-78df0e1c-slot61` blocker pair was added; no proof input changed. |

The isolated module replay was the following command. It printed
`REPLAY_EXIT=0` and exited with status 0:

```bash
set -uo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot61-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/{Statement,ObligationTree,AnchorCandidates}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
base=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
status=0
LEAN_NUM_THREADS=1 LEAN_PATH="$base" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" || status=$?
if [ "$status" -eq 0 ]; then
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 300 "$lean" --trust=0 -t0 \
    --root="$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" || status=$?
fi
if [ "$status" -eq 0 ]; then
  LEAN_NUM_THREADS=1 LEAN_PATH="$base" timeout 300 "$lean" --trust=0 -t0 \
    --root="$tmp" "$tmp/AnchorCandidates.lean" || status=$?
fi
cd "$repo"
printf 'REPLAY_EXIT=%s\n' "$status"
exit "$status"
```

The word `sorry` printed during `Statement.lean` elaboration is Lean's diagnostic
rendering inside four expected `#check_failure` mutation probes. It is not source
syntax or an admitted proof; the token-anchored source scan confirms that
distinction.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
