# THM-M-1111 proof phase blocked at `20654453`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `20654453ac1080d53ecc931e38e042eddd8eb21d`

Base tree: `9e00bb6bdd01837c1c3da9fd284ae8a2767303ec`

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1111-S-DEFS` fails. The frozen declaration
`TaoVuFourMomentTarget` accepts an arbitrary `FourMomentSemantics`, but the structure imposes no
laws on `powerBound` or its other semantic operations. The placeholder-free theorem
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
not master-accepted `[x]`. Neither failure is repaired in this proof-only worker.

## Current-base evidence

The immediately preceding slot40 blocker packet, based on `87ffd1ca`, was integrated by the current
base. A scoped diff confirms that the statement, countermodel, conditional composition, statement
metadata, anchor audit, obligation registry, and typed graphs remain byte-unchanged at `20654453`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | Rank 551; planned; hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | Structural statement checks passed; SHA-256 `1b569042...68ebc`. |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | Candidate boundary, four Lean probes, and pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3. |
| Isolated pinned `lake env lean` replay below | 0 | Statement, exact countermodel, and conditional composition elaborated at trust level zero; theorem axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground 300 lake env lean --trust=0 -j1 -t0 ../../Stage1_Instances/THM-M-1111/AnchorAudit.lean` | 0 | Supporting probes elaborated; no retained candidate claims a terminal exact proof. |
| Prohibited-token scan over owned `*.lean` | 1 | Expected no-match exit; no proof escape was found. |
| Pinned-package keyword search | 0 | Only an unrelated Tao-Vu bibliography citation matched; no Four Moment theorem was found. |
| Scoped relevant-input diff from `87ffd1ca` to `20654453` | 0 | All seven proof-relevant inputs are unchanged. |
| Packet JSON/invariant checks and scoped whitespace checks | 0 | The structured blocker fields and both new files passed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The narrow replay used only existing pinned artifacts:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1111
tmp=$(mktemp -d /tmp/s56m1111-20654453-slot40.XXXXXX)
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

Lean was `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The replay produced stable object hashes
`2e66135e...907c03` for the statement, `4324624e...54b80e5` for the countermodel, and
`6b2bde0e...fe50534` for the conditional composition. The automation-provided untracked `.lake`
symlink was reused read-only. No network, update, build, clone, fetch, checkout, or `.lake` mutation
was used. Temporary Lean objects were written under `/tmp` and removed. This is narrow nonrelease
corroboration, not validation or release evidence.

## Retry accounting

Fifty earlier proof-recheck packet pairs dated 2026-07-15 are integrated, but the authoritative
proof node still records `attempts=0` and `children=[]`. Blueprint section 10.2 requires an
unresolved item to be split after five execution ticks. Only the integration lane may edit the
authoritative DAG or checklist, so this worker records the mismatch without changing either. This
fifty-first unchanged blocker recheck is the scheduler-required target-scoped handoff, not proof
progress.

## Retry and boundary

Reopen the statement phase and replace the arbitrary interface with a fixed, source-faithful model
of random Hermitian matrices, or add noncircular source-justified laws that rule out the countermodel
and support the comparison estimate. Accept a new statement fingerprint, then refreeze and rerun
the anchor audit, obligation registry, typed graphs, and all downstream phases. The integration lane
must also split, redirect, or stop repeatedly scheduling the unchanged proof item.

The root vector remains `H2 / M3 / R3`; no proof body, graph edge, composition certificate, debt
state, or accepted receipt changed. The remaining cut set is the statement phase,
`M1111-S-DEFS`, and `M1111-ROOT`. The existing `instance.json`, `task-dag.json`, and typed graph
contain stale/conflicting projections which only the appropriate upstream and integration phases
may reconcile.

This packet claims only a current-base proof blocker. It claims no proof completion, validation,
release, master acceptance, audit completion, or theorem completion. Because the assigned phase is
not genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.
