# THM-M-1111 proof-phase recheck at `5bb51543`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `5bb515438bd0e1d53584e5243c5d434dfde7158e`

Base tree: `8055b8d863f0978f110a628ab3ccc7ab1e146b12`

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1111-S-DEFS` fails. The frozen declaration
`TaoVuFourMomentTarget` accepts an arbitrary `FourMomentSemantics`, but that structure places no
laws on `powerBound` or its other semantic operations. The placeholder-free theorem
`not_taoVuFourMomentTarget_counterSemantics` supplies a lawful instance with `Unit` carriers, all
hypothesis predicates true, both statistics zero, and `powerBound` constantly `-1`. At
`epsilon = 1/2`, `k = C = C' = 1`, `n = 2 * (N + 1)`, and index `N + 1`, every premise holds while
the conclusion reduces to `0 <= -1`. Pinned Lean checks the negation of the exact frozen target.

This refutes the abstract encoding, not the Tao--Vu Four Moment Theorem. A positive body for the
current root would be inconsistent. Choosing a favorable `FourMomentSemantics`, adding the desired
comparison as an assumption, or using the existing `FourMomentComparisonPackage` wrapper would
specialize, circularly assume, or substitute the theorem and is not permitted proof work.

## Current-base evidence

The prior integrated blocker packet was based on `6da5c027`. A scoped `git diff --exit-code` shows
that `Statement.lean`, `ProofBlocker.lean`, `ObligationTree.lean`, `statement.json`,
`anchor-audit.json`, `obligation-registry.json`, and `typed-graphs.json` are byte-unchanged through
the current base. Their current SHA-256 hashes, exact command results, environment, and structured
status fields are recorded in the companion JSON packet.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned; hard-mathlib lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | structural statement checks passed; SHA-256 `1b569042...68ebc` |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | candidate boundary, four Lean probes, and pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3 |
| isolated `lake env lean --trust=0 -t0` replay below | 0 | statement, exact countermodel, and conditional composition elaborated; both theorem axiom reports are `[propext, Classical.choice, Quot.sound]` |
| prohibited-token scan over owned `*.lean` | 1 | expected no-match exit; no proof escape found |
| scoped relevant-input diff from `6da5c027` to `5bb51543` | 0 | all seven proof-relevant inputs are unchanged |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase emitted no completion manifest |

The isolated replay used existing pinned artifacts only:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1111-slot65-head5bb51543.XXXXXX)
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
or `.lake` mutation occurred. Temporary Lean objects were created under `/tmp` and removed.

The auxiliary checks were run exactly as follows. The `rg` exit `1` is the expected no-match
result; the other two commands returned `0`.

```bash
rg --pcre2 -n \
  '(?x)(^|\s)(sorry|admit|sorryAx|native_decide|implemented_by|axiom|opaque|constant|unsafe|external)(\s|$)' \
  Stage1_Instances/THM-M-1111 --glob '*.lean'
git diff --exit-code 6da5c027e3ced79acf5af10230bfd1b825e3d40e..HEAD -- \
  Stage1_Instances/THM-M-1111/Statement.lean \
  Stage1_Instances/THM-M-1111/ProofBlocker.lean \
  Stage1_Instances/THM-M-1111/ObligationTree.lean \
  Stage1_Instances/THM-M-1111/statement.json \
  Stage1_Instances/THM-M-1111/anchor-audit.json \
  Stage1_Instances/THM-M-1111/obligation-registry.json \
  Stage1_Instances/THM-M-1111/typed-graphs.json
test ! -e .stage1-worker-selftest.json
```

## Retry accounting

Ten earlier current-day proof-recheck packets are already integrated, but the authoritative proof
node still records `attempts=0` and `children=[]`. Blueprint section 10.2 requires splitting an item
after five unresolved execution ticks rather than repeatedly assigning the same oversized work.
Only the integration lane may edit the authoritative DAG/checklist, so this worker records the
mismatch without changing either. This eleventh unchanged assignment cannot close the proof node.

## Retry and boundary

Reopen the statement phase and replace the arbitrary interface with a fixed, source-faithful model
of random Hermitian matrices, or constrain the generic interface with noncircular source-justified
laws that rule out the countermodel and support the comparison estimate. Accept a new statement
fingerprint, then refreeze the anchor audit and obligation denominator before retrying proof work.

No statement, positive proof body, typed graph, authoritative state, or dependency was changed. The
proof item remains `[ ]`; root, validation, release, audit completion, theorem completion, and master
acceptance remain open. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
