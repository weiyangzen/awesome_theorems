# THM-M-1108 proof-phase recheck at 6bf9ee93 (slot38)

Item: `S56-M-1108-PROOF`

Recheck date: `2026-07-16T05:00:00+08:00` (`Asia/Shanghai`)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No placeholder-free body inhabiting the exact target
`Stage1Instances.THM_M_1108.CanonicalStatement` exists in the owned source,
repository-local Lean source, all-ref target history, or the locally available
pinned dependency closure. This recheck adds no Lean proof body, closes no
obligation, and makes no proof-completion claim.

The mandatory schema `stage1-dependency-reuse-ledger/1.1` ledger was created
before any proof implementation was considered. It binds the exact v2 theorem
DAG digest `73e99d22...40eca`, dependency context `068170c7...c5c`, and base
revision. The authoritative v2 node has no direct hard parents, transitive hard
ancestors, incoming hard edges, reuse hints, or shared groups. Its complete
audited closure, inspections, decisions, and unresolved compatibility sets are
therefore all empty. The repository validator accepts the ledger.

The only checked child-to-root declaration is
`canonicalStatement_of_poissonized_depoissonized`. Its body is
`hTransfer hPoissonized`, so it consumes `PoissonizedAsymptotics` and
`DePoissonizationTransfer` as premises and constructs neither. The immediate
root cut remains `M1108-T-POISSONIZED` plus `M1108-T-DEPOISSONIZE`.

The first unavailable frozen package is `M1108-C-RSK`: the pinned closure has
permutations, Young diagrams, and semistandard tableaux, but no checked
Robinson--Schensted correspondence with the LIS/first-row identity required by
the frozen Poissonized route. The Toeplitz-determinant, Riemann--Hilbert
steepest-descent, Hastings--McLeod/Painleve II, uniform edge-error,
Poissonized-limit, monotonicity/tail, and de-Poissonization bodies also remain
absent. The prerequisite immutable anchor audit identifies no compatible Lean
4 proof to pin or import.

Assuming either terminal package, introducing an analytic axiom, weakening the
statement, substituting a random-matrix Tracy--Widom result, or presenting the
conditional composer as the BDJ theorem would violate the frozen target and
Blueprint section 10.8. No such shortcut was added.

The frozen registry and typed graph project `[H2, M3, R3]`, while the older
planned instance and anchor-audit projections record `[H2, M4, R4]`. That
pre-existing projection conflict requires master reconciliation. Every
projection leaves the root open, and this proof recheck proposes no debt
transition.

## Narrow Validation Evidence

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Temporary replay files and
objects lived only under `/tmp` and were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard validation completed successfully. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, all 10822 legacy states, 2 hard edges, 5 hints, 310 shared groups, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | Rank 548; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open at M3. |
| Direct `validate_dependency_reuse_ledger(...)` call | 0 | Schema 1.1 empty audited closure passed against exact graph digest and base revision. |
| Isolated temporary-copy replay below | 0 | All three owned Lean modules elaborated under `lake env lean --trust=0 -t0`; checked bodies report only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan below | 1 | Expected no-match exit; no prohibited construct occurs in an owned Lean file. |
| Pinned-package topical scan below | 1 | Expected no-match exit; no theorem-level terminal candidate was found. |
| Repository-local exact-interface scan below | 1 | Expected no-match exit; no reusable exact declaration was found outside this dossier. |
| All-ref target `Proof*.lean` history scan below | 1 | Expected no-match exit; no target proof module exists to recover. |
| Toolchain and dependency identity checks | 0 | Lean `4.29.0` at `98dc76e3...6740`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`. |
| JSON parsing and scoped blocker assertions | 0 | Both structured artifacts parsed; item/base/state/completion and empty-ledger invariants passed. |
| `git diff --check` | 0 | No whitespace error was reported. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The manifest is absent, as required for an incomplete proof deliverable. |

The exact trust-zero replay was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1108-slot38-head6bf9ee93-replay.XXXXXX)
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

The exact ledger validation was:

```bash
python3 - <<'PY'
from pathlib import Path
from scripts.stage1_execution_cron import validate_dependency_reuse_ledger

validate_dependency_reuse_ledger(
    Path('Stage1_Instances/THM-M-1108/dependency-reuse-ledger.json'),
    'THM-M-1108',
    expected_observed_graph_sha256=
        '73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca',
    expected_repository_revision=
        '6bf9ee93a322e7d25cf9249226222095f95d1cff',
)
print('dependency reuse ledger: ok')
PY
```

The exact source and candidate scan was:

```bash
set +e
pattern='(^|[^[:alnum:]_])(sorry|admit|sorryAx|implemented_by|native_decide|unsafe|extern|run_tac)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|constant|opaque)[[:space:]]'
rg -n --glob '*.lean' "$pattern" Stage1_Instances/THM-M-1108
s1=$?
rg -n -i --glob '*.lean' '\b(baik|deift|johansson|tracy[-_ ]?widom|painlev(e|ee)|hastings[-_ ]?mcleod|robinson[-_ ]?schensted|schensted|longest[-_ ]?increasing[-_ ]?subsequence|riemann[-_ ]?hilbert|toeplitz determinant|fredholm determinant|airy kernel|de[-_ ]?poissonization)\b' Formalizations/Lean/.lake/packages
s2=$?
rg -n --glob '*.lean' '\b(normalizedLISCDF|IsTracyWidomCDF|PoissonizedAsymptotics|DePoissonizationTransfer|poissonizedLISCDF|lisLength)\b' . --glob '!Stage1_Instances/THM-M-1108/**' --glob '!Formalizations/Lean/.lake/**' --glob '!.git/**'
s3=$?
git rev-list --all --objects | rg -i 'Stage1_Instances/THM-M-1108/(proof[^/]*\.lean|.+/proof[^/]*\.lean)$'
s4=$?
printf 'SCAN_EXITS prohibited=%s topical=%s exact_interface=%s history_proof=%s\n' \
  "$s1" "$s2" "$s3" "$s4"
test "$s1" -eq 1 && test "$s2" -eq 1 && test "$s3" -eq 1 && test "$s4" -eq 1
```

The word `sorry` printed while replaying `Statement.lean` is Lean's diagnostic
rendering inside four expected `#check_failure` mutation probes. It is not
source syntax or an admitted proof; the token-anchored scan confirms this.

## Reopen And Scheduling Condition

Implement both frozen terminal packages and their child obligations without
placeholders, or provide an immutable compatible Lean 4 BDJ proof for pinned
exact-type integration with complete provenance, dependency, trust, and
license validation.

Thirty-nine blocker recheck pairs predated this attempt. Blueprint section
10.2 requires splitting after five unresolved execution ticks instead of
dispatching the same oversized item again. The master/scheduler must reconcile
retry accounting and create dependency-legal child tasks beginning with
`M1108-C-RSK`; this worker may not edit the authoritative DAG, whose assigned
row still records `attempts=0` and `children=[]`.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1108-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. `accepted_receipt_ids=[]`. Because the assigned proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.
