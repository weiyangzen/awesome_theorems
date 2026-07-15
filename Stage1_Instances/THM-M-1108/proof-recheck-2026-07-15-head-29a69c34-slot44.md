# THM-M-1108 proof-phase recheck at 29a69c34 (slot44)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T14:38:10+08:00` (`Asia/Shanghai`)

Base revision: `29a69c34f06bf3444399287853ea7806767d0944`

Base tree: `de0efce35b6fcc6f851b9c2e643d61ec49d831e0`

## Verdict

`blocked`; no proof body was added, no frozen obligation newly closed, and no
proof credit or state transition is claimed.

The exact target remains
`Stage1Instances.THM_M_1108.CanonicalStatement`, the full Baik--Deift--Johansson
limit for the normalized longest increasing subsequence. The checked
declaration `canonicalStatement_of_poissonized_depoissonized` has body
`hTransfer hPoissonized`: it consumes explicit inhabitants of
`PoissonizedAsymptotics` and `DePoissonizationTransfer` and constructs neither
premise. It is a valid conditional composition certificate, not a proof of the
root.

No target file changed between the preceding integrated recheck at target
revision `860fc1b5` and this base. Statement, obligation-tree, registry, graph,
anchor-audit, and validation-specification hashes remain unchanged.

Independent proof and analogue searches found no repo-local or pinned-mathlib
terminal body. Mathlib supplies permutations, Young diagrams, CDFs, Poisson
infrastructure, derivatives, and integrals, but no checked
Robinson--Schensted/LIS identity, Tracy--Widom or Painleve development,
Toeplitz-determinant asymptotics, Riemann--Hilbert steepest descent, uniform
edge estimates, or de-Poissonization theorem. The prerequisite immutable
external audit likewise found no compatible Lean 4 BDJ proof to pin.

The first unavailable frozen mathematical package is `M1108-C-RSK`. The
immediate root cut remains:

- `M1108-T-POISSONIZED`
- `M1108-T-DEPOISSONIZE`

No sound logical shortcut was found. The target is not definitionally true,
the model predicate is not known inconsistent, and the value at `N = 0` is
only a finite initial term irrelevant to an `atTop` limit. Assuming either
terminal package, declaring an axiom, weakening the target, or presenting the
conditional composer as an unconditional theorem would violate the assigned
deliverable. The root stays `[H2, M3, R3]`, with `root_closed=false`,
`proof_phase_complete=false`, and `theorem_complete=false`.

## Narrow Validation Evidence

All checks ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was treated as read-only. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or `.lake` mutation
was performed. Temporary replay files and objects were created only under
`/tmp` and removed.

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
| `git diff --name-status 860fc1b5...HEAD -- Stage1_Instances/THM-M-1108` | 0 | No output; no target file changed since the preceding integrated recheck. |
| `python3 -m json.tool Stage1_Instances/THM-M-1108/proof-recheck-2026-07-15-head-29a69c34-slot44.json` | 0 | The current-base structured blocker artifact is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json` | 0 | No whitespace errors were reported. |

The exact trust-zero replay command was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot44-head29a69c34-replay.XXXXXX)
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
proof occurs in source.

## Reopen And Scheduling Condition

Implement both frozen terminal packages and their child obligations without
placeholders, or provide an immutable compatible Lean 4 BDJ proof for pinned
exact-type integration with full provenance, dependency, trust, and license
validation.

Eighteen blocker rechecks existed at this base. Blueprint section 10.2 says
that after five unresolved execution ticks the item must be split rather than
retried unchanged. The master/scheduler should create dependency-legal child
tasks beginning with `M1108-C-RSK`; this worker may not edit the authoritative
DAG.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
