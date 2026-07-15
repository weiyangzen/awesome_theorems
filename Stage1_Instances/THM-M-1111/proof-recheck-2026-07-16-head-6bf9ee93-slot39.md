# THM-M-1111 proof phase blocked at `6bf9ee93`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Dependency and reuse audit

The required schema-1.1 ledger binds theorem-DAG digest `73e99d22...0eca`, target context digest
`068170c7...5c5c`, and this exact base revision. The v2 node has no direct hard parent, transitive hard
ancestor, incoming hard edge, reuse hint, or shared group. Consequently its complete inspection and
decision closure is empty, and there are no unresolved compatibility obligations. The repository
validator accepted [the ledger](dependency-reuse-ledger.json). No result was reused and no proof
credit was transferred.

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1111-S-DEFS` fails. The frozen declaration
`TaoVuFourMomentTarget` accepts an arbitrary `FourMomentSemantics`, but the structure imposes no laws
on `powerBound` or its other semantic operations. The placeholder-free theorem
`not_taoVuFourMomentTarget_counterSemantics` supplies an admissible instance with `Unit` carriers,
all hypothesis predicates true, both expected statistics zero, and `powerBound` constantly `-1`.
At `epsilon = 1/2`, `k = C = C' = 1`, `n = 2 * (N + 1)`, and index `N + 1`, every premise holds
while the conclusion reduces to `0 <= -1`. Pinned Lean checks the negation of the exact target at
this instance.

This refutes the abstract encoding, not the Tao-Vu Four Moment Theorem for a future source-faithful
semantics. A generic positive proof body for the frozen target family would be inconsistent.
Selecting a favorable semantics, adding the comparison as an assumption, or using
`FourMomentComparisonPackage` (definitionally the open root) would specialize, circularly assume,
or substitute the assigned theorem and is not permitted proof work.

The workflow prerequisite is independently unfinished: `S56-M-1111-OBLIGATION_TREE` remains `[_]`,
not master-accepted `[x]`. Neither failure is repairable in this proof-only worker.

## Current-base evidence

The proof-relevant statement, countermodel, conditional composition, statement metadata, anchor
audit, obligation registry, and typed graphs are byte-unchanged from the preceding integrated
blocker packet at `20654453`. This worker performed a fresh trust-zero replay against only the
existing pinned artifacts.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | All 1546 nodes, 10822 retained phase states, typed v2 edges, and acyclicity passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | Rank 551; planned; hard-mathlib lane; theorem incomplete. |
| Schema-1.1 `validate_dependency_reuse_ledger` with exact graph/base constraints | 0 | Empty dependency, inspection, decision, and unresolved-obligation closure passed. |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | Structural statement checks passed; SHA-256 `1b569042...68ebc`. |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | Candidate boundary, four Lean probes, and pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3. |
| Isolated pinned `lake env` / `lean --trust=0 -j1 -t0` replay below | 0 | Statement, exact countermodel, and conditional composition elaborated; theorem axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan over owned `*.lean` | 1 | Expected no-match exit; no proof escape was found. |
| Pinned-package keyword search | 0 | Only an unrelated Tao-Vu bibliography citation matched; no Four Moment theorem was found. |
| Scoped relevant-input diff from `20654453` to `6bf9ee93` | 0 | All seven proof-relevant inputs are unchanged. |

The narrow replay used only existing pinned artifacts:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1111
tmp=$(mktemp -d /tmp/s56m1111-6bf9ee93-slot39.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ProofBlocker.lean" \
  "$target/ObligationTree.lean" "$tmp/"
cd "$repo/Formalizations/Lean"
timeout --foreground 60 lake env lean --version
lean=$(timeout --foreground 60 lake env which lean)
base_path=$(timeout --foreground 60 lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout --foreground 300 \
  "$lean" --trust=0 -j1 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 300 \
  "$lean" --trust=0 -j1 -t0 --root="$tmp" -o "$tmp/ProofBlocker.olean" \
  "$tmp/ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 300 \
  "$lean" --trust=0 -j1 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ProofBlocker.olean" \
  "$tmp/ObligationTree.olean"
```

Lean was `4.29.0` at commit `98dc76e3...6740`; pinned mathlib was `8a178386...eea95`
(tree `bdc39a31...d2b`). The replay produced object hashes `2e66135e...907c03` for the statement,
`4324624e...54b80e5` for the countermodel, and `6b2bde0e...fe50534` for the conditional composition.
The automation-provided untracked `.lake` symlink was reused read-only. No network, update, build,
clone, fetch, checkout, or `.lake` mutation was used. Temporary Lean objects were written under
`/tmp` and removed. This is narrow nonrelease corroboration, not validation or release evidence.

`python3 Docs/tools/check_stage1_standard.py` was also started, but its long cron-unit-test subcheck
was interrupted and is deliberately not claimed as passing on this base. The targeted structural,
ledger, and kernel checks listed above passed.

## Retry accounting

Fifty-one earlier proof-recheck packet pairs are integrated, but the authoritative proof node still
records `attempts=0` and `children=[]`. Blueprint section 10.2 requires an unresolved item to be split
after five execution ticks. Only the integration lane may edit the authoritative DAG or checklist,
so this worker records the mismatch without changing either. This packet adds the newly mandatory v2
dependency ledger and current-base blocker evidence; it is not positive proof progress.

## Retry and boundary

Reopen the statement phase and replace the arbitrary interface with a fixed, source-faithful model
of random Hermitian matrices, or add noncircular source-justified laws that rule out the countermodel
and support the comparison estimate. Accept a new statement fingerprint, then refreeze and rerun the
anchor audit, obligation registry, typed graphs, and all downstream phases. The integration lane must
also split, redirect, or stop repeatedly scheduling the unchanged proof item.

The root vector remains `H2 / M3 / R3`; no positive proof body, graph edge, composition certificate,
debt state, or accepted receipt changed. The remaining cut set is the statement phase,
`M1111-S-DEFS`, and `M1111-ROOT`. Existing structured projections require upstream and integration
reconciliation after statement repair.

This packet claims only a current-base proof blocker. It claims no proof completion, validation,
release, master acceptance, audit completion, or theorem completion. Because the assigned phase is
not genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.
