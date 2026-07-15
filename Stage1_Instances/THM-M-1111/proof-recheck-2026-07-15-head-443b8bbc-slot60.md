# THM-M-1111 proof phase blocked at `443b8bbc`

Item: `S56-M-1111-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1111-S-DEFS` fails. The frozen declaration
`TaoVuFourMomentTarget` accepts an arbitrary `FourMomentSemantics`, but the structure imposes no
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

The latest integrated blocker packet is based on `f94e9d38`. The statement, countermodel,
conditional composition, statement metadata, anchor audit, obligation registry, and typed graphs
are byte-unchanged from that base through `443b8bbc`. Their exact hashes and the structured results
below are recorded in the companion JSON packet.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1111` | 0 | rank 551; planned hard-mathlib lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1111/check_statement.py` | 0 | structural statement checks passed; SHA-256 `1b569042...68ebc` |
| `python3 Stage1_Instances/THM-M-1111/check_anchor_audit.py` | 0 | candidate boundary, four Lean probes, and pinned mathlib revision passed |
| `python3 Stage1_Instances/THM-M-1111/check_obligation_tree.py` | 0 | 19 obligations and 46 typed edges passed; root remains open M3 |
| isolated pinned `lean --trust=0 -j1 -t0` replay below | 0 | statement, exact countermodel, and conditional composition elaborated; both theorem axiom reports are `[propext, Classical.choice, Quot.sound]` |
| prohibited-token scan over owned `*.lean` | 1 | expected no-match exit; no prohibited proof escape found |
| scoped relevant-input diff from `f94e9d38` to `443b8bbc` | 0 | all seven proof-relevant inputs are byte-unchanged |
| JSON parse and scoped invariant assertions | 0 | item/base, blocked open state, unchanged debt, checked refutation, false completion fields, empty receipts, and absent self-test agree |
| `git diff --no-index --check /dev/null` on each packet file, accepting expected diff exit 1 | 0 | both new files differ from `/dev/null` with no whitespace diagnostic |
| `git diff --check -- Stage1_Instances/THM-M-1111` | 0 | no scoped whitespace errors after adding this packet |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase emitted no completion manifest |

The requested `lake env` discovery was attempted first, but the shared canonical `.lake` currently
contains an incomplete `flt-regular` checkout (`HEAD` is `refs/heads/.invalid`). `lake env` therefore
failed before launching Lean. No update, build, clone, fetch, checkout, or other `.lake` mutation was
performed. The narrow replay instead invoked the toolchain pinned by `lean-toolchain` directly and
used the already-built libraries in the canonical `.lake` read-only:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1111-slot60-head443b8bbc.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1111/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1111/ProofBlocker.lean "$tmp/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1111/ObligationTree.lean "$tmp/ObligationTree.lean"
lean=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lake_root="$root/Formalizations/Lean/.lake"
lean_path="$lake_root/packages/mathlib/.lake/build/lib/lean:$lake_root/packages/batteries/.lake/build/lib/lean:$lake_root/packages/Qq/.lake/build/lib/lean:$lake_root/packages/aesop/.lake/build/lib/lean:$lake_root/packages/proofwidgets/.lake/build/lib/lean:$lake_root/packages/importGraph/.lake/build/lib/lean:$lake_root/packages/LeanSearchClient/.lake/build/lib/lean:$lake_root/packages/plausible/.lake/build/lib/lean:$lake_root/packages/Cli/.lake/build/lib/lean:$lake_root/packages/checkdecls/.lake/build/lib/lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300 "$lean" --trust=0 -j1 -t0 \
  -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 "$lean" --trust=0 -j1 -t0 \
  -R "$tmp" -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 "$lean" --trust=0 -j1 -t0 \
  -R "$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
```

Lean was `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; pinned mathlib was
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The replay used no network and temporary Lean objects
were removed by the shell trap. The automation-provided untracked `.lake` symlink was reused
read-only.

## Retry accounting and boundary

Sixteen earlier same-day proof-recheck packets are integrated, while the authoritative proof node
still records `attempts=0` and `children=[]`. Blueprint section 10.2 requires splitting after five
unresolved execution ticks rather than repeatedly assigning the same oversized item. Only the
master may reconcile or split the authoritative DAG, so this worker records the mismatch without
editing the DAG or checklist.

Reopen the statement phase. Replace the arbitrary interface with a fixed, source-faithful model of
random Hermitian matrices, or constrain it with noncircular source-justified laws that exclude the
countermodel and support the comparison estimate. Accept a new target fingerprint, then refreeze
the anchor audit and obligation denominator before retrying proof work.

No statement, positive proof body, typed graph, authoritative state, or dependency was changed. The
proof item remains `[ ]`; root closure, validation, release, audit completion, theorem completion,
and master acceptance remain open. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
