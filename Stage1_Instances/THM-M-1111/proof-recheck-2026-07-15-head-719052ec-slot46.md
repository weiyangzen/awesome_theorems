# THM-M-1111 proof phase blocked at `719052ec`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `719052ec5fae5190f38e013d646fd7461d29be5d`

Base tree: `a8de041884ae39d41031493cb436b3e4a66bbfa0`

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1111-S-DEFS` fails. The frozen declaration
`TaoVuFourMomentTarget` accepts an arbitrary `FourMomentSemantics`, but that structure imposes no
laws on `powerBound` or its other semantic operations. The placeholder-free theorem
`not_taoVuFourMomentTarget_counterSemantics` supplies an admissible instance with `Unit` carriers,
all hypothesis predicates true, both expected statistics zero, and `powerBound` constantly `-1`.
At `epsilon = 1/2`, `k = C = C' = 1`, `n = 2 * (N + 1)`, and index `N + 1`, every premise holds
while the conclusion reduces to `0 <= -1`. Pinned Lean checks the negation of the exact target.

This refutes the abstract encoding, not the Tao--Vu Four Moment Theorem. A positive proof body for
the frozen root would be inconsistent. Selecting a favorable semantics, adding the comparison as
an assumption, or using `FourMomentComparisonPackage` (definitionally the open root) would
specialize, circularly assume, or substitute the theorem and is not permitted proof work.

## Current-base evidence

The latest integrated THM-M-1111 blocker packet was recorded against base `d5ab961c` and integrated
in `7505614b`. The statement, countermodel, conditional composition, statement metadata, anchor
audit, obligation registry, and typed graphs are byte-unchanged from that base through `719052ec`.
Their exact hashes and structured results are recorded in the companion JSON packet.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned; hard-mathlib lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | structural statement checks passed; SHA-256 `1b569042...68ebc` |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | candidate boundary, four Lean probes, and pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3 |
| isolated `lake env` Lean replay below | 0 | statement, exact countermodel, and conditional composition elaborated at trust level zero; both theorem axiom reports are `[propext, Classical.choice, Quot.sound]` |
| prohibited-token scan over owned `*.lean` | 1 | expected no-match exit; no proof escape found |
| scoped relevant-input diff from `d5ab961c` to `719052ec` | 0 | all seven proof-relevant inputs are unchanged |
| JSON parse and scoped invariant assertions | 0 | item/base, blocked state, unchanged debts, checked refutation, false completion fields, empty receipts, and absent self-test agree |
| `git diff --no-index --check /dev/null` on both packet files, accepting expected diff exit 1 | 0 | both files differ from `/dev/null` with no whitespace diagnostic |
| `git diff --check -- Stage1_Instances/THM-M-1111` | 0 | no scoped whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase emitted no completion manifest |

The narrow replay used only existing pinned artifacts:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1111-proof-recheck-head719052ec-slot46.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1111/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1111/ProofBlocker.lean "$tmp/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1111/ObligationTree.lean "$tmp/ObligationTree.lean"
cd "$root/Formalizations/Lean"
lean_path=$(lake env printenv LEAN_PATH)
lean=$(lake env which lean)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
```

Lean was `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided untracked `.lake` symlink was
reused read-only. The replay used no network; no `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation occurred. Temporary Lean objects were created under `/tmp` and
removed. This is narrow nonrelease corroboration, not release evidence.

## Retry accounting

Twenty-three earlier current-day proof-recheck packets are already integrated, but the authoritative
proof node still records `attempts=0` and `children=[]`. Their repeated unchanged assignments are
strong evidence that the integration lane must reconcile whether the five-tick threshold in
blueprint section 10.2 has been reached and then split or stop rescheduling the item. Only the
integration lane may edit the authoritative DAG/checklist, so this worker records the mismatch
without changing either. This twenty-fourth unchanged blocker recheck is the mandatory
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
