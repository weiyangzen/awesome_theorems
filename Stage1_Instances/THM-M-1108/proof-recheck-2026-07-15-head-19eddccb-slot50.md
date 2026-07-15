# THM-M-1108 proof-phase recheck at 19eddccb (slot50)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T15:52:28+08:00` (`Asia/Shanghai`)

Base revision: `19eddccb8988b4da9e007b60f4a25b6806877160`

Base tree: `1b5d55ad37802063bf31881e5e06faa0410bf21c`

## Verdict

`blocked`; no proof body was added, no frozen obligation was newly closed, and no proof credit or
state transition is claimed.

The exact target remains `Stage1Instances.THM_M_1108.CanonicalStatement`, the full
Baik--Deift--Johansson pointwise limit for the normalized longest increasing subsequence of a
uniform permutation. The checked declaration
`canonicalStatement_of_poissonized_depoissonized` has body `hTransfer hPoissonized`. It consumes
inhabitants of `PoissonizedAsymptotics` and `DePoissonizationTransfer` and constructs neither, so it
is a conditional composition certificate rather than a proof of the root.

Since the preceding recheck at `431e77db`, only that recheck's Markdown and JSON records were added
under this target. The statement, conditional proof interface, obligation registry, typed graphs,
anchor audit, and validation specifications retain their recorded hashes. Fresh scoped searches
found no repo-local or pinned-mathlib proof of either terminal package. The pinned closure provides
permutations, Young diagrams and tableaux, CDFs, Poisson limits, derivatives, integrals, and filters,
but no checked RSK/LIS identity, Tracy--Widom/Painleve development, Toeplitz asymptotics,
Riemann--Hilbert analysis, uniform edge estimate, or de-Poissonization theorem. Repository history
contains no earlier `Proof.lean` for this target, and the immutable anchor audit has no compatible
external Lean 4 proof to pin.

The first unavailable frozen package is `M1108-C-RSK`. The immediate root cut remains:

- `M1108-T-POISSONIZED`
- `M1108-T-DEPOISSONIZE`

Assuming a terminal package, adding an axiom, weakening the proposition, or presenting the
conditional composer as the BDJ theorem would violate the assigned deliverable. The root remains
`[H2, M3, R3]`, with `root_closed=false`, `proof_phase_complete=false`, and
`theorem_complete=false`.

## Narrow Validation Evidence

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was treated as read-only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary replay files and objects lived only under `/tmp` and were removed.

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
| All-ref repository-history scan for a target `Proof*.lean` | 1 | Expected no-match exit; no historical proof module exists for this target. |
| `git diff --name-status 431e77db6367a2eda83060b7212cb490d11ca39f..HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only the preceding `head-431e77db-slot50` blocker pair was added; no proof input changed. |
| `sha256sum` over the statement, proof interface, registry, graphs, anchor audit, and validation specs | 0 | Hashes match the structured companion artifact. |

The exact trust-zero replay command was:

```bash
set -uo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot50-head19eddccb-replay.XXXXXX)
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

Each module exited `0`. The word `sorry` in the `Statement.lean` diagnostic output is Lean's
rendering inside four expected `#check_failure` mutation probes; it is not source syntax or an
admitted proof, as the token-anchored source scan confirms.

## Reopen And Scheduling Condition

Implement both frozen terminal packages and their child obligations without placeholders, or
provide an immutable compatible Lean 4 BDJ proof for pinned exact-type integration with complete
provenance, dependency, trust, and license validation.

Twenty-three blocker rechecks predated this attempt. Blueprint section 10.2 requires splitting
after five unresolved execution ticks rather than retrying the same oversized item. The
master/scheduler should reconcile retry accounting and create dependency-legal child tasks
beginning with `M1108-C-RSK`; this worker may not edit the authoritative DAG, whose row still says
`attempts=0` and `children=[]`.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1108-PROOF`, change task state, or claim audit completion, theorem completion, validation,
release, receipt acceptance, or master acceptance. `accepted_receipt_ids=[]`. Because the assigned
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
