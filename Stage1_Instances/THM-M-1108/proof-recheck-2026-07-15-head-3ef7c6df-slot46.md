# THM-M-1108 proof-phase recheck at 3ef7c6df (slot46)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `3ef7c6dff0c66bc8c02e842f4cea6b9936349094`

Base tree: `58db6c40c0fa9186c4a56a022a6a37d1c2be551b`

## Verdict

`blocked`; no proof body was added, no frozen obligation newly closed, and no
proof credit or state transition is claimed.

The exact target remains
`Stage1Instances.THM_M_1108.CanonicalStatement`, the Baik--Deift--Johansson
limit for the normalized longest increasing subsequence. The checked theorem
`canonicalStatement_of_poissonized_depoissonized` has body
`hTransfer hPoissonized`: it consumes explicit inhabitants of
`PoissonizedAsymptotics` and `DePoissonizationTransfer` and constructs neither.
It is a valid conditional composition certificate, not a proof of the root.

Fresh scoped searches found no repo-local or pinned-mathlib body for either
terminal package. Mathlib supplies nearby permutation, Young-diagram, CDF,
Poisson, derivative, and integral infrastructure, but not the required
Robinson--Schensted/LIS identity, Tracy--Widom/Painleve development,
Toeplitz-determinant asymptotics, Riemann--Hilbert analysis, uniform edge
estimates, or de-Poissonization theorem. The immutable anchor audit likewise
contains no compatible external Lean 4 BDJ proof to pin or import.

The first unavailable frozen package is `M1108-C-RSK`. The immediate root cut
remains:

- `M1108-T-POISSONIZED`
- `M1108-T-DEPOISSONIZE`

No sound shortcut is available: the target is not definitionally true, the
Tracy--Widom predicate is not known inconsistent, and a finite initial value is
irrelevant to an `atTop` limit. Assuming a terminal package, adding an axiom,
weakening the proposition, or presenting the conditional composer as the BDJ
theorem would violate the assigned deliverable. The root remains
`[H2, M3, R3]`, with `root_closed=false`, `proof_phase_complete=false`, and
`theorem_complete=false`.

## Narrow Validation Evidence

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or `.lake` mutation
was performed. Temporary replay files and objects lived only under `/tmp` and
were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546, all L0/rework-required, passed. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned lifecycle; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3 and both terminal packages open at M4. |
| Isolated temporary-copy replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` using `lake env lean`, `--trust=0`, and `-t0` | 0 | Replay exits were `0/0/0`; all modules elaborated. The exact-statement transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom-like bodyless declaration, unsafe/oracle, or equivalent prohibited construct was found. |
| Pinned-mathlib topical source scan | 1 | Expected no-match exit; no relevant theorem-level terminal declaration was found. |
| Repository-local exact-interface scan outside this target and `.lake` | 1 | Expected no-match exit; no reusable exact declaration was found. |
| `git diff --name-status 29a69c34...HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only the two preceding integrated blocker pairs were added; no statement, proof interface, registry, graph, audit, or validation input changed. |

The exact trust-zero replay command was:

```bash
set -uo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot46-head3ef7c6df-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/{Statement,ObligationTree,AnchorCandidates}.lean "$tmp"/
cd Formalizations/Lean
base=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 300 lake env lean \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 \
  --root="$tmp" "$tmp/AnchorCandidates.lean"
cd "$repo"
```

The word `sorry` printed for `Statement.lean` occurs only in Lean's diagnostic
rendering of the four expected `#check_failure` mutation probes; no admitted
proof occurs in source, as the token-anchored scan confirms.

## Reopen And Scheduling Condition

Implement both frozen terminal packages and their child obligations without
placeholders, or provide an immutable compatible Lean 4 BDJ proof for pinned
exact-type integration with complete provenance, dependency, trust, and
license validation.

Twenty blocker rechecks predated this attempt. Blueprint section 10.2 requires
splitting after five unresolved execution ticks instead of retrying an item
unchanged. The master/scheduler should create dependency-legal child tasks
beginning with `M1108-C-RSK`; this worker is not authorized to edit the
authoritative DAG. The authoritative row still records `attempts=0` and an
empty child list, so its retry accounting does not reflect the twenty
integrated blocker packets and must be reconciled by the master.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
