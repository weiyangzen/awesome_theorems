# THM-M-0325 proof-phase recheck at `18ff7447`

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-14T04:30:00+08:00`

Base revision: `18ff7447208231633bf2e01e8aad3111af56531a`

Base tree: `9ea9aab30253e72b62ef25c80e17b575356fb7b6`

## Verdict

`blocked`. The frozen proposition is the full finite real Grothendieck
inequality. No placeholder-free body inhabiting
`GrothendieckInequalityTarget` in the repository or pinned dependency closure,
and the bounded public Lean searches recorded by the prerequisite audit expose
no compatible terminal theorem to pin. The root remains `[H2, M3, R4]`; its
minimal open cut is `M0325-T-PACKAGE`; no obligation is newly closed.

`ObligationTree.lean` defines `GrothendieckProofPackage` to be the canonical
target and proves only `target_of_proofPackage package := package`. That term is
a checked conditional identity, not a construction of `package`. Returning it,
postulating the package, or assuming any analytic child would replace the
requested theorem with an unproved premise.

Pinned mathlib supplies finite-span, Gram-matrix, Gaussian, arcsine, and generic
projective/injective tensor-seminorm infrastructure. It does not supply the
real Grothendieck/Krivine transform with a universal bound, the correlated
Gaussian-sign identity, or a terminal Grothendieck inequality. In particular,
`PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm` is not the frozen
scalar-to-Hilbert estimate. The first unavailable substantive gate is therefore
`M0325-K-TRANSFORM`. The finite-span and Gram reductions, random rounding,
measurability and integrability, scalar-bound application, expectation estimate,
and final proof package also remain open.

The dossier now contains six tracked unresolved root-sized proof rechecks,
including this one. Although the authoritative DAG still records zero attempts,
the five immutable prior recheck artifacts are evidence of five execution
ticks. Rev-5.6 section 10.2 requires an item to be split after five unresolved
ticks rather than sent through the same oversized task again. This worker
cannot edit the authoritative DAG or generated checklist. The retry condition
is therefore a master-side split into the eight frozen analytic obligations
listed below.

The assigned proof phase is not complete. The item remains `[ ]`; this artifact
is blocker evidence, not a proof receipt, and it supports no provisional state,
audit completion, validation completion, release, or theorem completion.
Because the proof deliverable is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Narrow Validation

All checks reused the automation-provided canonical pinned Lake closure. No
`lake update`, `lake build`, dependency clone/fetch, network request, or
dependency write was performed. The untracked `.lake` symlink makes this
nonrelease evidence. Trust-zero Lean outputs were isolated under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Structured anchor invariants passed at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open `M3`, analytic package `M4`. |
| `LEAN_NUM_THREADS=1 timeout 300 python3 Stage1_Instances/THM-M-0325/check_statement.py` | 0 | Exact expression hash `b4daa662...cf82`; all four structural mutations were distinguished; pinned toolchain and mathlib revision matched. |
| Isolated `lake env` Lean `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` | 0 | Exact target, conditional composition, and five tensor-seminorm anchor declarations elaborated. Both axiom reports listed only `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned mathlib search for Grothendieck inequality/constant, Krivine, random rounding, Gaussian-sign, and arcsine-expectation terms | 0 | Sole match was an unrelated Hermite-polynomial comment containing “up to sign”; no terminal or analytic-rounding declaration was found. |
| `git log --all -S'GrothendieckInequalityTarget' --format='%H %s' -- '*.lean'` and the corresponding search for `GrothendieckInequalityWithConstant` | 0 | Only statement/intake/evidence history was found; no lost terminal proof body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe, opaque, extern, implementation override, or native-decision shortcut. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The isolated replay was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-head-18ff7447.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/AnchorAudit.lean" "$tmp/"
cd "$tmp"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 300 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/AnchorAudit.olean" \
  "$tmp/AnchorAudit.lean"
```

## Retry Condition

Do not schedule the same root-sized proof item again. First create
dependency-legal child nodes for `M0325-N-FINITE-SPAN`, `M0325-N-GRAM`,
`M0325-K-TRANSFORM`, `M0325-R-RANDOM`, `M0325-B-MEASURABLE`,
`M0325-B-SCALAR`, `M0325-L-EXPECTATION`, and `M0325-T-PACKAGE`. Resume a child
only when its exact placeholder-free body can be implemented or an immutable
compatible Lean 4 body can be pinned, exact-type transported, and kernel
checked.
