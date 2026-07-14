# THM-M-1111 proof-phase recheck at `fb0fd5be`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1111-S-DEFS` fails. The frozen declaration
`TaoVuFourMomentTarget` accepts an arbitrary `FourMomentSemantics`, but that structure places no
laws on `powerBound` or its other semantic operations. The placeholder-free theorem
`not_taoVuFourMomentTarget_counterSemantics` supplies a lawful instance with `Unit` carriers, all
hypothesis predicates true, both statistics zero, and `powerBound` constantly `-1`. At
`epsilon = 1/2`, `k = C = C' = 1`, `n = 2 * (N + 1)`, and index `N + 1`, the target conclusion is
`0 <= -1`. Pinned Lean checks the negation of the exact frozen target.

This refutes the abstract encoding, not the Tao--Vu Four Moment Theorem. A positive body for the
current root would be inconsistent. Choosing a favorable `FourMomentSemantics`, asserting the
comparison estimate as a field, or proving the existing `FourMomentComparisonPackage` wrapper
would substitute or circularly assume the theorem and is not permitted proof work.

## Current-base evidence

The prior integrated blocker packet was based on `a1a7e939`. A scoped `git diff --exit-code` shows
that `Statement.lean`, `ProofBlocker.lean`, `ObligationTree.lean`, `statement.json`,
`anchor-audit.json`, `obligation-registry.json`, and `typed-graphs.json` are byte-unchanged from that
base through `fb0fd5be`. Their current SHA-256 hashes, exact commands, exits, environment, and
structured status fields are recorded in the companion JSON packet.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned; hard-mathlib lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | target fragments and mutations passed; statement SHA-256 `1b569042...68ebc` |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | candidate boundary, Lean probes, and pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3 |
| isolated `lake env lean --trust=0 -t0` replay below | 0 | statement, exact countermodel, and conditional composition elaborated; both theorems reported `[propext, Classical.choice, Quot.sound]` |
| prohibited-token scan over owned `*.lean` | 1 | expected no-match exit; no proof escape found |
| scoped relevant-input diff from `a1a7e939` to `fb0fd5be` | 0 | all seven proof-relevant inputs are unchanged |
| JSON parse and scoped invariant assertions | 0 | item/base, blocked state, unchanged debts, checked refutation, false completion fields, empty accepted receipts, and absent-self-test declaration agree |
| `git diff --no-index --check /dev/null` on each new packet file, accepting expected diff exit 1 | 0 | both files differ from `/dev/null` with no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase emitted no completion manifest |

The isolated replay used existing pinned artifacts only:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1111-proof-recheck-current.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1111/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1111/ProofBlocker.lean "$tmp/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1111/ObligationTree.lean "$tmp/ObligationTree.lean"
cd "$root/Formalizations/Lean"
lean_path=$(lake env printenv LEAN_PATH)
lean=$(lake env which lean)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 180 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
```

Lean was `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The automation-provided untracked `.lake` symlink was
reused read-only. The kernel replay used no network; no `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation occurred. An independent auxiliary inspection fetched the
dossier-pinned arXiv v10 PDF into temporary storage and confirmed its recorded SHA-256; it did not
change the repository or dependencies and was not needed for the countermodel result. Temporary
Lean objects were removed by the shell trap.

## Retry and boundary

Reopen the statement phase and replace the arbitrary interface with a fixed, source-faithful model
of random Hermitian matrices, or add independently justified noncircular laws that rule out the
countermodel and support the comparison estimate. Then accept a new target fingerprint, refreeze
the anchor audit and obligation denominator, and rerun every downstream phase.

No statement, proof body, typed graph, authoritative state, or dependency was changed. The proof
item remains `[ ]`; root, validation, release, audit completion, and theorem completion remain open.
Because the assigned proof phase is not complete, `.stage1-worker-selftest.json` is deliberately
absent.
