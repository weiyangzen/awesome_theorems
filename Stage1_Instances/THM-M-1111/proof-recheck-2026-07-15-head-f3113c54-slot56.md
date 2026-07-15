# THM-M-1111 proof phase blocked at `f3113c54`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `f3113c54b9f211684b537a151ecc735272dae987`

Base tree: `d2c746871998c8c43a491e60488882e7711e9b6a`

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

The immediately preceding blocker packet, based on `61f7b690`, was integrated by the current base.
A scoped `git diff --exit-code` shows that the statement, countermodel, conditional composition,
statement metadata, anchor audit, obligation registry, and typed graphs are byte-unchanged through
`f3113c54`. Their exact hashes and structured results are in the companion JSON packet.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | Rank 551; planned; hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | Structural statement checks passed; SHA-256 `1b569042...68ebc`. |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | Candidate boundary, four Lean probes, and pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3. |
| Isolated pinned `lake env lean` replay below | 0 | Statement, exact countermodel, and conditional composition elaborated at trust level zero; theorem axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `cd Formalizations/Lean && timeout --foreground 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1111/AnchorAudit.lean` | 0 | Supporting probes elaborated; no retained candidate claims a terminal exact proof. |
| Fixed-string/regex anchor search over pinned dependency Lean sources | 0 | The sole match was an unrelated Tao--Vu bibliography citation; no exact target anchor was found. |
| Prohibited-token scan over owned `*.lean` | 1 | Expected no-match exit; no proof escape was found. |
| Scoped relevant-input diff from `61f7b690` to `f3113c54` | 0 | All seven proof-relevant inputs are unchanged. |
| JSON parse and scoped invariant assertions | 0 | Item/base, blocked state, false completion fields, empty receipts, changed paths, and retry ordinal agree. |
| `git diff --no-index --check /dev/null` on both new packet files, accepting expected diff exit 1 | 0 | Both files differ from `/dev/null` with no whitespace diagnostic. |
| `git diff --check -- Stage1_Instances/THM-M-1111` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Incomplete proof phase emitted no completion manifest. |

The narrow replay used only existing pinned artifacts:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1111-lake-env-head-f3113c54-slot56.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1111/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1111/ProofBlocker.lean "$tmp/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1111/ObligationTree.lean "$tmp/ObligationTree.lean"
cd "$root/Formalizations/Lean"
base_lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" timeout --foreground 300 lake env lean \
  --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout --foreground 300 lake env lean \
  --trust=0 -t0 -R "$tmp" -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout --foreground 300 lake env lean \
  --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
```

Lean was `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided untracked `.lake` symlink
was reused read-only. No network was used. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation occurred. Temporary Lean objects were created under `/tmp` and
removed. This is narrow nonrelease corroboration, not validation or release evidence.

## Retry accounting

Thirty-six earlier current-day proof-recheck packets are already integrated, but the authoritative
proof node still records `attempts=0` and `children=[]`. Blueprint section 10.2 requires splitting
an item after five unresolved execution ticks rather than repeatedly assigning the same oversized
work. Only the integration lane may edit the authoritative DAG/checklist, so this worker records
the mismatch without changing either. This thirty-seventh unchanged blocker recheck is the
mandatory target-scoped scheduler handoff, not a new proof attempt or proof-progress claim.

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
