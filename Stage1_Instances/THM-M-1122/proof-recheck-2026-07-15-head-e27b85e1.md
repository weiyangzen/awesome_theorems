# THM-M-1122 proof-phase recheck at current base

Item: `S56-M-1122-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `e27b85e1503047c5e4bd8d5410b6fba5c4dda896`

Base tree: `29c625431b9c241bce6286123205defcbd1e7f7e`

## Verdict

`blocked`. No placeholder-free positive proof can inhabit the frozen target uniformly over its
explicit parameters. The repo-local declaration

```text
Stage1Instances.THM_M_1122.proofPhaseCountermodel :
  Not (SchrammLoewnerEvolutionTarget
    (Measure.dirac ()) (Measure.dirac false) True
    (fun _ : Unit => true)
    (fun _ : Bool -> Real -> Unit => True)
    (fun _ : NegativeTime -> Unit => fun _ : Bool => True))
```

kernel-checks at trust level zero. It instantiates the arbitrary Brownian and Loewner predicates as
always true, takes the LERW-side curve to be constantly `true`, and takes the Brownian-side trace to
be the identity on `Bool`. Under Dirac measures at `()` and `false`, the target would identify those
laws. Applying `IdentDistrib.measure_preimage_eq` to the measurable singleton `{true}` reduces that
claim to zero equaling one.

This refutes only the frozen abstract encoding, not Schramm's mathematical theorem. The interface
predicates do not connect the arbitrary curves to source-faithful LERW, circle Brownian, or radial
Loewner constructions. Supplying `ConditionalIdentification` as an extra premise would assume the
required conclusion and strengthen the theorem, so the checked transport in `ObligationTree.lean`
does not provide root proof credit.

The exact root stays open at `M3`; the frozen proof cut is `M1122-L-IDENTIFICATION`. No positive proof
body, obligation closure, receipt, debt-vector transition, audit completion, validation completion,
release result, or theorem-completion claim is made. The item remains `[ ]`. Because the assigned
phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed semantic gate is exact-target consistency/provability at
`M1122-S-INTERFACES`: the frozen target permits a kernel-checked finite countermodel. In addition,
the authoritative prerequisite `S56-M-1122-OBLIGATION_TREE` remains worker-provisional `[_]`, not
master-accepted `[x]`.

Retry only after reopening the statement phase, replacing the opaque interfaces with fixed,
source-faithful definitions and sufficient noncircular hypotheses, accepting a new statement
fingerprint, and freezing a new obligation-registry version. The statement, anchor-audit, and
obligation-tree phases must then be rerun before positive proof execution resumes.

## Validation

All checks ran in this worker clone using the existing pinned Lake artifacts. The pre-existing
untracked `Formalizations/Lean/.lake` symlink points to the canonical pinned cache, so this packet is
nonrelease evidence. No `lake update`, `lake build`, dependency clone/fetch, network action, or
`.lake` mutation was performed. Lean outputs were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1122` | 0 | Rank 562; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1122/check_obligation_tree.py` | 0 | 11 obligations and 19 typed edges passed; denominator `1d0de239...863fd`; root open at M3 and `ConditionalIdentification` M4. |
| Narrow `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and negative declaration elaborated; the countermodel reports `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan over `Statement.lean` and `ProofCountermodel.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, unsafe/oracle escape, or `native_decide` occurs. |
| `git diff --check -- Stage1_Instances/THM-M-1122` | 0 | No tracked whitespace errors before adding this packet. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists for the blocked phase. |

The narrow current-base replay, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1122
tmp=$(mktemp -d /tmp/s56m1122-e27b85e1.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ProofCountermodel.lean" "$tmp/"
cd "$repo/Formalizations/Lean"
base_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" "$tmp/ProofCountermodel.lean"
```

The temporary `Statement.olean` had SHA-256
`88f36fe6436c03754a145ec6c4958e668428a969a6ac2c5d9b30af2240fc6578`. Lean emitted only the
non-failing `unnecessarySimpa` linter warning in addition to the axiom report.
