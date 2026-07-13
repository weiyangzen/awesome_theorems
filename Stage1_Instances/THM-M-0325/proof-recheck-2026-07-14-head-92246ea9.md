# THM-M-0325 proof-phase recheck at `92246ea9`

Item: `S56-M-0325-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`

Base tree: `bd58be98bf3046078c016d44fb4a677ea231cb23`

## Verdict

`blocked`. No placeholder-free proof body for the exact frozen finite real
Grothendieck inequality exists in the repository or pinned dependency closure.
The root remains `[H2, M3, R4]`, its minimal open cut remains
`M0325-T-PACKAGE`, and no obligation is newly closed.

`ObligationTree.lean` defines `GrothendieckProofPackage` as the canonical
target and proves only `target_of_proofPackage package := package`. That is a
checked conditional identity, not a construction of `package`. Returning it,
postulating the package, or assuming any analytic child would replace the
required proof with an unproved premise.

Pinned mathlib exposes generic projective and injective tensor-seminorm
substrate, but not the missing estimate. Searches found no Grothendieck
constant, Krivine transform, correlated Gaussian-sign identity, or arcsine
expectation theorem. A genuine implementation still needs the frozen
finite-span and Gram reductions, real transform and universal bound, random
rounding, measurability and integrability, pointwise scalar application,
expectation estimate, and terminal package.

This claim is scheduler retry `5`. Rev-5.6 section 10.2 says that after five
unresolved execution ticks the item must be split rather than assigned again
as one oversized task. This worker is forbidden to edit the authoritative DAG
or generated checklist, so the recheck requests master-side child nodes for
the eight open frozen obligations listed in the structured artifact.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, or release is claimed.
Because the positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks used the existing pinned Lake closure. No `lake update`, `lake
build`, dependency clone/fetch, network validation, or `.lake` mutation was
performed. The automation-provided untracked `.lake` symlink makes this
nonrelease evidence. Temporary Lean objects were isolated under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Structured source hashes and pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open `M3`, analytic package `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and conditional composition elaborated. `target_of_proofPackage` reports only `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned mathlib Grothendieck/Krivine/correlated-sign search recorded in the structured artifact | 0 | Sole match: an unrelated Hermite-polynomial comment saying "up to sign"; no candidate declaration. |
| Pinned probability/measure-theory rounding-identity search recorded in the structured artifact | 0 | Three generic prose matches about integral signs; no analytic rounding identity. |
| Pinned `PiTensorProduct` declaration search recorded in the structured artifact | 0 | Only generic tensor-seminorm substrate; no reverse universal-constant estimate. |
| Scoped prohibited-token scan recorded in the structured artifact | 1 | Expected no-match; no prohibited construct in owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/proof-blocker.json` | 0 | The tracked structured blocker remains valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/proof-recheck-2026-07-14-head-92246ea9.json` plus scoped hash/status assertions | 0 | Current-base blocker JSON parsed and all frozen input hashes, open-state booleans, retry count, split request, and changed paths matched. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git diff --check -- Stage1_Instances/THM-M-0325 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null` for both new artifacts | 0 / 1 expected | No whitespace diagnostics; `--no-index` returns the expected difference code for each new file. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  ObligationTree.lean
```

Pinned inputs include `Statement.lean` SHA-256 `a24ef5cd...98eb1e`,
`ObligationTree.lean` `224e289b...0abf8`, `obligation-registry.json`
`9afd6408...a9587b`, `typed-graphs.json` `420e72de...a0f8b`, and
`lake-manifest.json` `321626c8...2d81`.

## Retry Condition

Do not schedule the same root-sized proof item again. First split it into
dependency-legal child nodes for `M0325-N-FINITE-SPAN`, `M0325-N-GRAM`,
`M0325-K-TRANSFORM`, `M0325-R-RANDOM`, `M0325-B-MEASURABLE`,
`M0325-B-SCALAR`, `M0325-L-EXPECTATION`, and `M0325-T-PACKAGE`. Resume a child
only when an exact placeholder-free body can be implemented or immutably
pinned and checked.
