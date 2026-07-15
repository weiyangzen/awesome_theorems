# THM-M-1108 proof-phase recheck at c887c8e5 (slot58)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15T18:49:15+08:00` (`Asia/Shanghai`)

Base revision: `c887c8e5d7afe589d4b90386654421a60e998f51`

Base tree: `7a1298612a32286e2a542ffc410cf4de9bb1fabd`

## Verdict

`blocked`; no placeholder-free proof body was added, no frozen obligation was
newly closed, and no proof credit or state transition is claimed.

The exact target remains
`Stage1Instances.THM_M_1108.CanonicalStatement`, the full Baik--Deift--Johansson
limit for the normalized longest increasing subsequence. The checked declaration
`canonicalStatement_of_poissonized_depoissonized` has body
`hTransfer hPoissonized`: it consumes explicit inhabitants of
`PoissonizedAsymptotics` and `DePoissonizationTransfer` and constructs neither
premise. It is a valid conditional composition certificate, not a proof of the
root.

No proof input changed at this base. The only target changes since the preceding
`d5771f24` blocker base are the integration of two earlier blocker-record pairs;
the seven frozen input hashes and both environment-pin hashes remain unchanged.
Fresh repository-local and history searches found no root or terminal body.
The pinned closure supplies permutations, Young diagrams, CDFs, Poisson PMFs,
and nearby limit infrastructure, but no checked Robinson--Schensted/LIS identity,
Tracy--Widom or Painleve development, Toeplitz determinant asymptotics,
Riemann--Hilbert steepest descent, uniform edge estimates, or
de-Poissonization theorem. The prerequisite immutable external audit likewise
found no compatible Lean 4 BDJ proof to pin.

The first unavailable frozen mathematical package is `M1108-C-RSK`. The
immediate root cut remains:

- `M1108-T-POISSONIZED`
- `M1108-T-DEPOISSONIZE`

Assuming either terminal package, declaring an analytic axiom, weakening the
target, or presenting the conditional composer as unconditional BDJ would
violate the assigned deliverable. The root stays `[H2, M3, R3]`, with
`root_closed=false`, `proof_phase_complete=false`, and
`theorem_complete=false`.

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
| Isolated temporary-copy replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` through `lake env lean`, with `--trust=0` and `-t0` | 0 | Replay exits were `0/0/0`; all modules elaborated. The exact-statement transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle, external implementation, or equivalent prohibited construct was found. |
| Repository-local exact-interface scan outside this target and `.lake` | 1 | Expected no-match exit; no reusable exact declaration was found. |
| `git rev-list --all --objects` target-proof-module scan | 1 | Expected no-match exit; repository history contains no `Proof*.lean` module for this target. |
| `git log --all --oneline -S'PoissonizedAsymptotics' -- '*.lean'` | 0 | The only history hit is the original dossier integration at `d021f1111`; no later proof implementation exists. |
| `git diff --name-status d5771f24...HEAD -- Stage1_Instances/THM-M-1108` | 0 | Only the `head-8400eb33-slot37` and `head-d5771f24-slot37` blocker pairs were integrated; no proof input changed. |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...eea95`; tree `bdc39a31...242c19e5c2b`. |
| `sha256sum` over seven frozen target inputs and two environment pins | 0 | Every digest matched the accompanying JSON record. |
| `python3 -m json.tool Stage1_Instances/THM-M-1108/proof-recheck-2026-07-15-head-c887c8e5-slot58.json` | 0 | The current-base blocker record parsed successfully. |
| `git diff --check -- Stage1_Instances/THM-M-1108 .stage1-worker-selftest.json` | 0 | No tracked whitespace errors. |
| `git diff --no-index --check /dev/null` applied separately to both new blocker artifacts | 1 | Expected new-file diff exits with empty diagnostics; neither artifact has a whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The proof-incomplete run has no self-test manifest. |

The exact trust-zero replay command was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1108-slot58-headc887c8e5-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1108/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1108/ObligationTree.lean "$tmp/ObligationTree.lean"
cp Stage1_Instances/THM-M-1108/AnchorCandidates.lean "$tmp/AnchorCandidates.lean"
cd Formalizations/Lean
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/AnchorCandidates.lean"
```

It completed with `STATEMENT_EXIT=0`, `OBLIGATION_EXIT=0`,
`ANCHOR_EXIT=0`, and `REPLAY_EXIT=0`. The word `sorry` printed for
`Statement.lean` occurs only in Lean's diagnostic rendering of the four
expected `#check_failure` mutation probes; no admitted proof occurs in source.

## Reopen And Scheduling Condition

Implement both frozen terminal packages and their child obligations without
placeholders, or provide an immutable compatible Lean 4 BDJ proof for pinned
exact-type integration with full provenance, dependency, trust, and license
validation.

Thirty prior blocker recheck pairs existed at this base. Blueprint section
10.2 says that after five unresolved execution ticks the item must be split
rather than retried unchanged. The master/scheduler must reconcile the
authoritative `attempts=0` / `children=[]` metadata and create dependency-legal
child tasks beginning with `M1108-C-RSK`; this worker may not edit the
authoritative DAG.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
