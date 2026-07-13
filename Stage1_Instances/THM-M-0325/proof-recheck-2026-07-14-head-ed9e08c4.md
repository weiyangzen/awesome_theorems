# THM-M-0325 proof-phase recheck at `ed9e08c4`

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-14T03:45:00+08:00`

Base revision: `ed9e08c4aa5d18cb58fa54e74867f38999a92a14`

Base tree: `41384c2a54f3f02cffd5aa5c92555706fc748659`

## Verdict

`blocked`. The frozen proposition is the full finite real Grothendieck
inequality. No placeholder-free body inhabiting
`GrothendieckInequalityTarget` exists in the repository or pinned dependency
closure. The root remains `[H2, M3, R4]`, its minimal open cut is
`M0325-T-PACKAGE`, and no obligation is newly closed.

`ObligationTree.lean` defines `GrothendieckProofPackage` to be the canonical
target and proves only `target_of_proofPackage package := package`. This is a
checked conditional identity, not a construction of `package`. Returning it,
postulating the package, or assuming an analytic child would substitute an
unproved premise for the requested theorem.

Pinned mathlib has generic projective and injective `PiTensorProduct`
seminorms, but its source contains no Grothendieck inequality, Krivine
transform, random-rounding, correlated-sign, or arcsine-expectation
declaration. The audited comparison has direction `injectiveSeminorm <=
projectiveSeminorm`; it is not the missing universal scalar-to-Hilbert bound.
Repository history likewise contains only statement, intake, and evidence
commits, not a lost terminal proof body.

A genuine implementation still requires the frozen finite-span and Gram
reductions, the real Grothendieck/Krivine transform and universal bound,
correlated random-sign rounding, measurability and integrability, pointwise
use of the scalar premise, the expectation estimate, and terminal package
assembly. The first unavailable substantive gate is therefore
`M0325-K-TRANSFORM`.

The dossier already records at least five unresolved execution ticks.
Rev-5.6 section 10.2 therefore requires a split rather than another unchanged
root-sized assignment. The worker cannot edit the authoritative DAG or
generated checklist, so the retry condition is a master-side split into the
eight frozen analytic obligations. The item remains `[ ]`; no proof receipt,
provisional state, audit completion, or theorem completion is claimed. Because
the proof deliverable is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All Lean checks reused the existing pinned Lake closure. No `lake update`,
`lake build`, dependency clone/fetch, network request, or `.lake` mutation was
performed. The automation-provided untracked `.lake` symlink makes this
nonrelease evidence. Temporary Lean sources and objects lived under `/tmp` and
were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Structured anchor invariants and pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open `M3`, analytic package `M4`. |
| Isolated `lake env lean --trust=0 -t0` on `Statement.lean` | 0 | The exact target elaborated and printed. |
| Isolated `lake env lean --trust=0 -t0` on `ObligationTree.lean` | 0 | Conditional composition elaborated; its axioms were `propext`, `Classical.choice`, and `Quot.sound`. |
| Isolated `lake env lean --trust=0 -t0` on `AnchorAudit.lean` | 0 | Five tensor-seminorm declarations elaborated; the comparison wrapper had the same three axioms. |
| Pinned mathlib search for Grothendieck/Krivine/rounding/correlated-sign/arcsine-expectation terms | 1 | Expected no-match; no candidate declaration or comment occurred. |
| Repository and historical source search | 0 | Only the target, historical audit metadata, and statement/evidence commits matched; no terminal body. |
| Prohibited-token scan over owned Lean files | 1 | Expected no-match; no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe, opaque, extern, implementation override, or native-decision shortcut. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The exact isolated recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-head-ed9e08c4.XXXXXX)
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

`check_statement.py` was not rerun to completion: it creates target-local
temporary sources, and the shared worker host was heavily contended. The exact
`Statement.lean` was independently elaborated at trust level zero. The frozen
prior mutation receipt remains prerequisite input evidence, not a new proof
acceptance claim.

## Retry Condition

Do not schedule the same oversized root proof item again. First create
dependency-legal child nodes for `M0325-N-FINITE-SPAN`, `M0325-N-GRAM`,
`M0325-K-TRANSFORM`, `M0325-R-RANDOM`, `M0325-B-MEASURABLE`,
`M0325-B-SCALAR`, `M0325-L-EXPECTATION`, and `M0325-T-PACKAGE`. Resume a child
only when its exact placeholder-free body can be implemented or immutably
pinned, transported, and kernel-checked.
