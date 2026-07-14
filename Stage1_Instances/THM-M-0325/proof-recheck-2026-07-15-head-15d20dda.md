# THM-M-0325 proof-phase recheck at `15d20dda`

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-15` (`Asia/Shanghai`)

Base revision: `15d20dda8662e4144f32be899edc174f7a431574`

Base tree: `b39eec687e4f172c4ce04e08a255e593a428cf95`

## Verdict

`blocked`. The frozen proposition is the full finite real Grothendieck
inequality. No placeholder-free Lean body inhabiting
`Stage1Instances.THM_M_0325.GrothendieckInequalityTarget` exists in the
repository or the pinned dependency closure. The root remains
`[H2, M3, R4]`; its minimal open cut is `M0325-T-PACKAGE`; no obligation is
newly closed.

`ObligationTree.lean` defines `GrothendieckProofPackage` to be the canonical
target and proves only `target_of_proofPackage package := package`. This is a
checked conditional identity, not a construction of the package. Returning
that identity, postulating the package, or assuming an analytic child would
replace the required proof body with an unproved premise.

Pinned mathlib supplies generic finite-dimensional, Gaussian, integration,
and tensor-seminorm infrastructure, but not the real Grothendieck/Krivine
transform, its universal coefficient bound, correlated Gaussian-sign
rounding, the inverse-sine expectation identity, or a terminal Grothendieck
inequality. The first unavailable substantive gate is
`M0325-K-TRANSFORM`. The other open analytic obligations are
`M0325-N-FINITE-SPAN`, `M0325-N-GRAM`, `M0325-R-RANDOM`,
`M0325-B-MEASURABLE`, `M0325-B-SCALAR`, `M0325-L-EXPECTATION`, and
`M0325-T-PACKAGE`.

Since the immediately preceding recheck at `11a448c9`, the only change under
this target is integration of that recheck's JSON and Markdown blocker
evidence. No owned Lean source, registry, typed graph, validation spec,
dependency lock, toolchain pin, or pinned package changed. Repository history
and a current search of every pinned Lake package expose no compatible
terminal body.

Ten prior tracked unresolved proof-recheck pairs exist before this run.
Rev-5.6 section 10.2 requires a split after five unresolved execution ticks,
but the authoritative DAG still records zero attempts and no children. This
worker may not edit the DAG or generated checklist. The master must split this
oversized proof item into dependency-legal children before another root-sized
proof attempt.

The proof phase is incomplete and the item remains `[ ]`. This file and its
JSON companion are blocker evidence, not a proof receipt. They support no
provisional state, validation completion, release, or theorem completion.
Therefore `.stage1-worker-selftest.json` is deliberately absent.

## Narrow Validation

All local checks reused the automation-provided canonical pinned Lake closure.
No `lake update`, `lake build`, dependency clone/fetch, or dependency write was
performed. The untracked `.lake` symlink makes this warm worker evidence
nonrelease. Trust-zero Lean outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Structured anchor invariants passed at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open `M3`, analytic package `M4`. |
| Isolated `lake env` Lean replay with `--trust=0 -t0` of `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` | 0 | Exact target, conditional composition, and five tensor-seminorm anchors elaborated. Both axiom reports listed only `propext`, `Classical.choice`, and `Quot.sound`. The olean hashes were `5da713d6...cdd7d`, `6588e3bc...d2a`, and `7e864ef4...d1d0`. |
| `LEAN_NUM_THREADS=1 timeout 300 python3 Stage1_Instances/THM-M-0325/check_statement.py` | 124 | The mutation checker did not finish within 300 seconds under concurrent worker load. Its five direct elaborations are redundant with the unchanged statement hashes and the successful trust-zero canonical replay; this timeout is recorded as a known validation limitation, not hidden. |
| Pinned-closure search for analytic Grothendieck/Krivine, Gaussian-sign, inverse-sine expectation, or hyperplane-rounding bodies | 0 | The only match was an unrelated polynomial Hermite/Gaussian comment; no terminal theorem or needed analytic body matched. |
| Repository-history search for the exact local target/package names | 0 | Only statement, intake, obligation-tree, and evidence history was found; no lost terminal proof body. |
| Prohibited-mechanism scan over owned Lean sources | 1 | Expected no-match; no `sorry`, `admit`, `sorryAx`, axiom/constant/unsafe declaration, `opaque`, `extern`, implementation override, or native-decision shortcut occurred. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386...a95`; tree `bdc39a31...2c2b`; dependency tree clean. |

The isolated kernel replay was:

```bash
set -u
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-head15d20dda.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
lean=$(cd "$lean_root" && timeout 120 lake env which lean)
lean_path=$(cd "$lean_root" && timeout 120 lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/AnchorAudit.lean" "$tmp/"
cd "$tmp"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 600 \
  "$lean" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 600 \
  "$lean" --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 600 \
  "$lean" --trust=0 -t0 --root="$tmp" -o "$tmp/AnchorAudit.olean" \
  "$tmp/AnchorAudit.lean"
```

## Retry Condition

Do not schedule the same root-sized proof item again. First create
dependency-legal child nodes for `M0325-N-FINITE-SPAN`, `M0325-N-GRAM`,
`M0325-K-TRANSFORM`, `M0325-R-RANDOM`, `M0325-B-MEASURABLE`,
`M0325-B-SCALAR`, `M0325-L-EXPECTATION`, and `M0325-T-PACKAGE`. Resume a
child only when its exact placeholder-free body can be implemented or an
immutable compatible Lean 4 body can be pinned, exact-type transported, and
kernel checked.
