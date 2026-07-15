# THM-M-1108 proof-phase recheck at d5771f24

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `d5771f240b8fe26277d018c90fec963af76ed7f2`

Base tree: `f274a52fcf9e5edcd6b8f8dd43726122a041af50`

## Verdict

`blocked`. No placeholder-free body inhabiting
`Stage1Instances.THM_M_1108.CanonicalStatement` exists in this target, the
repository-local Lean source outside this target, repository history, or the
pinned mathlib closure. This recheck adds no Lean source or proof body and
closes no obligation. The lifecycle remains `planned`, and the root vector
remains `[H2, M3, R3] -> [H2, M3, R3]`.

`ObligationTree.lean` contains the genuine checked composition
`canonicalStatement_of_poissonized_depoissonized`. Its premises are
`PoissonizedAsymptotics` and `DePoissonizationTransfer`; it constructs neither.
The immediate open root cut therefore remains `M1108-T-POISSONIZED` plus
`M1108-T-DEPOISSONIZE`.

The first unavailable frozen package is `M1108-C-RSK`: neither the current
repository nor pinned mathlib contains a checked Robinson--Schensted
correspondence with the required LIS/first-row identity. The later Toeplitz
determinant, Riemann--Hilbert steepest-descent, Hastings--McLeod/Painleve-II,
uniform-edge-error, Poissonized-limit, monotonicity/tail, and
de-Poissonization bodies are absent as well. The prerequisite immutable anchor
audit identified no compatible Lean 4 theorem to pin or import.

The latest target change before this base, at `8400eb33`, added only the prior
proof-recheck Markdown and JSON. No target input has changed since then. All
seven frozen input hashes and both environment-pin hashes match the preceding
records. A current exact-interface scan and all-ref history scan likewise found
no reusable or deleted proof module.

Assuming either terminal package, introducing an analytic axiom, weakening the
target, or reporting the conditional composer as the BDJ proof would be a
placeholder or substituted theorem. No such declaration was added.

## Failed Gate And Retry

The first failed implementation gate is `M1108-C-RSK`. Resume after
dependency-legal child work implements the frozen combinatorial and analytic
packages without placeholders, or after an immutable compatible Lean 4 BDJ
proof becomes available for pinned exact-type integration with complete
terminal-body, dependency, trust, license, and provenance validation.

Twenty-eight proof-blocker/recheck pairs already existed at this base. Under
Blueprint section 10.2, the master/scheduler must stop retrying this oversized
item unchanged, reconcile the authoritative `attempts=0` / `children=[]`
metadata, and split execution beginning with `M1108-C-RSK`. This worker is
forbidden to edit the authoritative DAG.

## Validation

All checks ran in this worker clone against the automation-provided pinned Lake
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
| Isolated temporary-copy three-module `lake env lean` replay below, with `--trust=0` and `-t0` | 0 | `Statement.lean`, `ObligationTree.lean`, and `AnchorCandidates.lean` elaborated with exits `0/0/0`; the checked transport and conditional composer reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle, external implementation, or equivalent prohibited construct was found. |
| Pinned-package topical source scan | 1 | Expected no-match exit across every package named by `lake-manifest.json`; no BDJ, Tracy--Widom, Painleve, Hastings--McLeod, LIS, Riemann--Hilbert, Robinson--Schensted, de-Poissonization, or Airy-kernel terminal declaration was found. |
| Repository-local exact-interface scan outside this target and `.lake` | 1 | Expected no-match exit; no declaration of `normalizedLISCDF`, `IsTracyWidomCDF`, `poissonizedLISCDF`, `PoissonizedAsymptotics`, or `DePoissonizationTransfer` was found. |
| `git rev-list --all --objects` target-proof-module scan | 1 | Expected no-match exit; repository history contains no `Proof*.lean` module for this target. |
| `git log --all --oneline -S'PoissonizedAsymptotics' -- '*.lean'` | 0 | The only history hit is the original dossier integration at `d021f1111`; no later proof implementation exists. |
| `git diff --name-status 8400eb33...d5771f24 -- Stage1_Instances/THM-M-1108` | 0 | Empty output; no target input changed after the preceding recheck was integrated. |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Mathlib revision `8a178386...eea95`; tree `bdc39a31...242c19e5c2b`. |
| `sha256sum` over seven frozen target inputs and two environment pins | 0 | Every digest matched the values in the accompanying JSON record. |

The isolated replay command was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1108-slot37-headd5771f24-replay.XXXXXX)
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

The word `sorry` in `Statement.lean` diagnostics is Lean's rendering inside
four expected `#check_failure` probes; it is not source syntax or an admitted
proof. The token-anchored source scan establishes that distinction.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
