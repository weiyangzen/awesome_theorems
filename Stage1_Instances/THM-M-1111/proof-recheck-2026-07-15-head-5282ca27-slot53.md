# THM-M-1111 proof phase blocked at `5282ca27`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `5282ca2773644716295f6f2c45f05b380aaa99a2`

Base tree: `ef4d75f68b707c441252dd5a67d8db151b5b4af3`

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1111-S-DEFS` fails. The frozen declaration
`TaoVuFourMomentTarget` accepts an arbitrary `FourMomentSemantics`, but that structure imposes no
laws on `powerBound` or its other semantic operations. The placeholder-free theorem
`not_taoVuFourMomentTarget_counterSemantics` supplies an admissible instance with `Unit` carriers,
all hypothesis predicates true, both expected statistics zero, and `powerBound` constantly `-1`.
At `epsilon = 1/2`, `k = C = C' = 1`, `n = 2 * (N + 1)`, and index `N + 1`, every premise holds
while the conclusion reduces to `0 <= -1`. Pinned Lean checks the negation of the exact target at
this instance.

This refutes the abstract encoding, not the Tao--Vu Four Moment Theorem for a future source-faithful
semantics. A generic positive proof body for the frozen target family would be inconsistent.
Selecting a favorable semantics, adding the comparison as an assumption, or using
`FourMomentComparisonPackage` (definitionally the open root) would specialize, circularly assume,
or substitute the theorem and is not permitted proof work.

## Current-base evidence

The latest integrated blocker packet is based on `9254a0ec`. A scoped `git diff --exit-code` shows
that the statement, countermodel, conditional composition, statement metadata, anchor audit,
obligation registry, and typed graphs are byte-unchanged from that base through `5282ca27`. Their
exact hashes and structured results are recorded in the companion JSON packet.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned; hard-mathlib lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | structural statement checks passed; SHA-256 `1b569042...68ebc` |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | candidate boundary, four Lean probes, and pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3 |
| `cd Formalizations/Lean && lake env lean --version` plus path discovery | 0 | Lean 4.29.0 at commit `98dc76e3...`; existing pinned library paths resolved |
| isolated pinned `lake env` replay below | 0 | statement, exact countermodel, and conditional composition elaborated at trust level zero; both theorem axiom reports are `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1111/AnchorAudit.lean` | 0 | supporting probes elaborated; local audit declarations reject terminal proof closure |
| fixed-string exact-anchor search over pinned dependency Lean sources | 0 | the sole match was an unrelated Tao--Vu bibliography citation; no exact target anchor was found |
| prohibited-token scan over owned `*.lean` | 1 | expected no-match exit; no proof escape found |
| scoped relevant-input diff from `9254a0ec` to `5282ca27` | 0 | all seven proof-relevant inputs are unchanged |
| JSON parse and scoped invariant assertions | 0 | item/base, blocked state, unchanged debts, checked refutation, false completion fields, empty receipts, and absent self-test agree |
| `git diff --no-index --check /dev/null` on both new packet files, accepting expected diff exit 1 | 0 | both files differ from `/dev/null` with no whitespace diagnostic |
| `git diff --check -- Stage1_Instances/THM-M-1111` | 0 | no scoped whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase emitted no completion manifest |

The narrow replay used only existing pinned artifacts:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m1111-proof-slot53.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1111/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1111/ProofBlocker.lean "$tmp/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1111/ObligationTree.lean "$tmp/ObligationTree.lean"
LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
export LEAN_PATH="$LEAN_PATH_BASE:$tmp"
(
  cd "$tmp"
  timeout --foreground 120 "$LEAN" --trust=0 -j1 -t0 Statement.lean -o Statement.olean
  timeout --foreground 120 "$LEAN" --trust=0 -j1 -t0 ProofBlocker.lean -o ProofBlocker.olean
  timeout --foreground 120 "$LEAN" --trust=0 -j1 -t0 ObligationTree.lean -o ObligationTree.olean
)
```

Lean was `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided untracked `.lake` symlink was
reused read-only. No network was used. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation occurred. Temporary Lean objects were created under `/tmp` and
removed. This is narrow nonrelease corroboration, not validation or release evidence.

## Retry accounting

Twenty-eight earlier current-day proof-recheck packets are already integrated, but the authoritative
proof node still records `attempts=0` and `children=[]`. Blueprint section 10.2 requires splitting
an item after five unresolved execution ticks rather than repeatedly assigning the same oversized
work. Only the integration lane may edit the authoritative DAG/checklist, so this worker records
the mismatch without changing either. This twenty-ninth unchanged blocker recheck is the mandatory
target-scoped scheduler handoff, not a new proof attempt or proof-progress claim.

## Retry and boundary

Reopen the statement phase and replace the arbitrary interface with a fixed, source-faithful model
of random Hermitian matrices, or add noncircular source-justified laws that rule out the countermodel
and support the comparison estimate. Accept a new statement fingerprint, then refreeze the anchor
audit and obligation denominator before retrying proof work. The master must also split or stop
rescheduling this proof item under section 10.2.

No statement, positive proof body, typed graph, authoritative state, or dependency was changed. The
proof item remains `[ ]`; root, validation, release, audit completion, theorem completion, and master
acceptance remain open. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
