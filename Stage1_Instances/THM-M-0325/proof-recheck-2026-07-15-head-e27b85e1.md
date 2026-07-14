# THM-M-0325 proof-phase recheck at `e27b85e1`

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-15T05:24:26+08:00`

Base revision: `e27b85e1503047c5e4bd8d5410b6fba5c4dda896`

Base tree: `29c625431b9c241bce6286123205defcbd1e7f7e`

## Verdict

`blocked`. The frozen proposition is the full finite real Grothendieck
inequality. No placeholder-free body inhabiting
`GrothendieckInequalityTarget` exists in the repository or the pinned dependency
closure. The root remains `[H2, M3, R4]`; its minimal open cut is
`M0325-T-PACKAGE`; no obligation is newly closed.

`ObligationTree.lean` defines `GrothendieckProofPackage` to be the canonical
target and proves only `target_of_proofPackage package := package`. That term is
a checked conditional identity, not a construction of `package`. Returning it,
postulating the package, or assuming an analytic child would replace the
requested theorem with an unproved premise.

Pinned mathlib supplies generic finite-span, Gram, Gaussian, arcsine, and
projective/injective tensor-seminorm infrastructure. It does not supply the real
Grothendieck/Krivine transform with its universal coefficient bound, orthogonal
unit-vector augmentation, the correlated Gaussian-sign identity, or a terminal
Grothendieck inequality. In particular,
`PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm` is not the frozen
scalar-to-Hilbert estimate. The first unavailable substantive gate is
`M0325-K-TRANSFORM`. Finite-span and Gram reductions, random rounding,
measurability and integrability, scalar-bound application, expectation
assembly, and the final proof package also remain open.

A compatible mathematical route is Krivine's transform and Gaussian
hyperplane rounding. Implementing it needs new tensor power-series estimates,
orthogonal augmentation for subunit vectors, the arcsine expectation identity,
and measure-theoretic assembly. Those are exactly the absent frozen analytic
leaves; describing that route is not a Lean proof body.

Since the preceding recheck base `a1a7e939`, this target changed only by adding
that recheck's JSON and Markdown evidence. No Lean proof source or pinned
dependency changed. A bounded local search across every already-pinned Lake
package again found no compatible analytic or terminal body. Repository history
contains only the statement, intake, obligation-tree, and evidence commits for
the exact local names; it contains no lost proof body.

Seven earlier tracked unresolved root-sized proof rechecks already existed
before this one. Rev-5.6 section 10.2 requires a split after five unresolved
execution ticks rather than another request to solve the same oversized task.
The authoritative DAG still records zero attempts and no children, but this
worker may not edit that DAG or the generated checklist. The retry condition
remains a master-side split into the eight frozen analytic obligations below.

The assigned proof phase is not complete. The item remains `[ ]`; this artifact
is blocker evidence, not a proof receipt, and supports no provisional state,
audit completion, validation completion, release, or theorem completion.
Because the proof deliverable is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Narrow Validation

All checks reused the automation-provided canonical pinned Lake closure. No
`lake update`, `lake build`, dependency clone/fetch, or dependency write was
performed. The untracked `.lake` symlink makes this nonrelease evidence.
Trust-zero Lean outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Structured anchor invariants passed at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open `M3`, analytic package `M4`. |
| `LEAN_NUM_THREADS=1 timeout 300 python3 Stage1_Instances/THM-M-0325/check_statement.py` (two concurrent attempts) | 124 | Both were terminated after exceeding the intended bound under shared-host Lean contention and emitted no result. Target-local temporary sources and orphaned Lean processes were removed; no mutation receipt is claimed. |
| Isolated pinned Lean `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` | 0 | Exact target, conditional composition, and five tensor-seminorm anchors elaborated. Both axiom reports listed only `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-closure search for analytic Grothendieck/Krivine, random or hyperplane rounding, correlated signs, and arcsine expectation | 1 | Expected no-match across all already-pinned Lake packages. |
| `git log --all -S'<local Grothendieck target>' --format='%H %s' -- '*.lean'` | 0 | Only statement, intake, obligation-tree, and evidence history was found; no lost terminal body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match; no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe, opaque, extern, implementation override, or native-decision shortcut. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The mutation harness creates five target-local temporary copies and invokes
`lake env lean` once for each expression. Its two concurrent bounded attempts
did not finish on the heavily contended shared host. They were terminated and
their temporary files and orphaned processes were removed. The trust-zero replay
below independently elaborated the unchanged exact statement; the earlier
immutable mutation receipt is retained only as input evidence.

The isolated replay was:

```bash
set -u
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-direct-head-e27b85e1.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/AnchorAudit.lean" "$tmp/"
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 600 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 600 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 600 \
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
