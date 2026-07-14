# THM-M-0600 proof recheck at current base

Item: `S56-M-0600-PROOF`

Intent: `prove`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

## Verdict

`blocked`. No eligible placeholder-free proof body inhabits the exact target
`Stage1Instances.THM_M_0600.MorseLemmaTarget`. This run adds no proof body,
closes no frozen obligation, and leaves the item `[ ]`. The lifecycle remains
`planned`; the root vector remains `[H1, M3, R3]`.

The local theorem
`Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine` is a genuine checked
child-to-root composition, but it consumes the open proposition
`MorseNormalFormEngine`. It therefore cannot be credited as an unconditional
Morse-lemma proof. The frozen remaining root cut is `M0600-T-ENGINE`, whose
first central unavailable analytic package is `M0600-L-SPLITTING`.

Focused current-base searches found no `Proof.lean`, proof receipt, or engine
inhabitant in this dossier, repository-local Lean outside the dossier, any of
the rev-5.6 worker clones, or the pinned mathlib source. Pinned mathlib provides
quadratic-form diagonalization, signature accounting, and smooth local-inverse
ingredients only. It has no nonlinear smooth Taylor/splitting construction or
exact Morse normal-form theorem.

Closing the engine requires the frozen zero-dimensional branch, chart and
derivative transports, smooth second-order factorization, Sylvester and index
bridges, parameterized splitting, finite induction, inverse-function step,
construction of every `SmoothLocalCoordinates` field, and neighborhood-wide
identity. Assuming the engine, stopping at Hessian diagonalization or a Taylor
approximation, or weakening the neighborhood identity would add a hidden
premise or substitute another theorem. No such shortcut was introduced.

The proof inputs are unchanged since the previous recheck at `3b741f76`: the
only dossier changes between that base and this base are that recheck's
Markdown and JSON records. `Statement.lean`, `ObligationTree.lean`, the frozen
registry and graphs, validation specifications, and dependency pins retain
their recorded hashes.

## Narrow Validation

All checks ran in this automation clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
request, or `.lake` mutation was performed. Temporary Lean output was written
under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0600` | 0 | Rank 638; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0600/check_obligation_tree.py` | 0 | 18 obligations and 44 typed edges passed; denominator `071b0844...e93f981`; root open M3 and engine M4. |
| Isolated `lake env lean --trust=0 -t0` replay shown below | 0 | `Statement.lean` and `ObligationTree.lean` elaborated; the conditional composer reported exactly `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` was 312,040 bytes. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0600/AnchorAudit.lean` | 0 | The three pinned ingredient type probes elaborated without diagnostics. |
| Exact Morse-lemma spelling scan over pinned mathlib `*.lean` | 1, expected | No exact Morse-lemma source was found. |
| Exact target/engine declaration scan over repo-local Lean outside this dossier | 1, expected | No reusable target or engine declaration was found. |
| Bounded scan of rev-5.6 worker clones for `THM-M-0600/Proof.lean` | 0 | Count `0`; no worker proof candidate was present. |
| Prohibited-device scan over owned Lean source | 1, expected | No `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe/extern escape, or `implemented_by` occurred. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | Pinned revision `8a178386...ea95`, tree `bdc39a31...1c2b`, package worktree clean. |
| `python3 -m json.tool Stage1_Instances/THM-M-0600/proof-recheck-2026-07-15-head-5558ec5b-slot74.json` | 0 | The structured current-base blocker parsed successfully. |
| Per-file `git diff --no-index --check /dev/null <new-artifact>` | 1 each, expected | Both new-file difference exits had empty diagnostic output; neither artifact has a whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test is absent because the proof phase is blocked. |

Exact isolated replay, from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-0600-slot74.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-0600"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-0600/Statement.olean" \
  ../../Stage1_Instances/THM-M-0600/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP/Stage1_Instances/THM-M-0600" \
  timeout 300 lake env lean --trust=0 -t0 \
  -R ../../Stage1_Instances/THM-M-0600 \
  ../../Stage1_Instances/THM-M-0600/ObligationTree.lean
```

## Retry Condition

Resume after implementing the frozen smooth Taylor, parameterized splitting,
induction, inverse, normal-coordinate, and identity packages without
placeholders, or after identifying an immutable compatible Lean 4 Morse-lemma
body that can be pinned, exact-type transported, kernel-checked, and
provenance-audited without changing the dependency lock.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-0600-PROOF`, propose provisional or accepted state, or
support audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance. Because the assigned proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.
