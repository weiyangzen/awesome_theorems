# THM-M-0325 proof-phase recheck at `ed959a5a`

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-15T05:41:34+08:00`

Base revision: `ed959a5a318a6244a0a9b53d335b24d0198860f7`

Base tree: `ad80b5a6c5620daa66871bb3bbb0109f03b62d90`

## Verdict

`blocked`. The frozen target is the full finite real Grothendieck inequality.
No placeholder-free Lean body inhabiting
`Stage1Instances.THM_M_0325.GrothendieckInequalityTarget` exists in the
repository or the pinned dependency closure, and fresh bounded public search
did not expose an immutable compatible theorem to pin. The root remains
`[H2, M3, R4]`; its minimal open cut is `M0325-T-PACKAGE`; no obligation is
newly closed.

`ObligationTree.lean` defines `GrothendieckProofPackage` to be the canonical
target and proves only `target_of_proofPackage package := package`. This is a
checked conditional identity, not a construction of `package`. Returning it,
postulating the package, or assuming an analytic child would replace the
required proof body with an unproved premise.

Pinned mathlib supplies generic finite-span, Gram, Gaussian, inverse-sine, and
projective/injective tensor-seminorm infrastructure. It does not supply the
real Grothendieck/Krivine transform and universal coefficient bound,
orthogonal augmentation for subunit vectors, correlated Gaussian-sign
identity, expectation estimate, or terminal Grothendieck inequality. In
particular, `PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm` has the
wrong role for the frozen scalar-to-Hilbert estimate. The first unavailable
substantive gate is `M0325-K-TRANSFORM`. The finite-span and Gram reductions,
random rounding, measurability and integrability, scalar-bound application,
expectation assembly, and final proof package also remain open.

A compatible mathematical route is Krivine's tensor-power transform followed
by Gaussian hyperplane rounding. Formalizing that route requires exactly the
absent analytic leaves above. A prose description is not a Lean proof body.

Since the preceding proof recheck, this target changed only by integration of
that recheck's JSON and Markdown evidence. No owned Lean proof source,
obligation registry, graph, validation spec, dependency lock, or toolchain pin
changed. Repository history contains only statement, intake, obligation-tree,
and evidence work for the exact local target names; it contains no lost proof
body.

Eight earlier tracked unresolved proof-recheck pairs existed before this run.
Rev-5.6 section 10.2 requires a split after five unresolved execution ticks.
The authoritative DAG nevertheless still records zero attempts and no
children. This worker may not edit that DAG or the generated checklist, so the
retry condition remains a master-side split into the eight frozen analytic
obligations listed below.

The proof phase is incomplete and the item remains `[ ]`. This file and its
JSON companion are blocker evidence, not a proof receipt; they support no
provisional state, audit completion, validation completion, release, or theorem
completion. Therefore `.stage1-worker-selftest.json` is deliberately absent.

## Narrow Validation

All local checks reused the automation-provided canonical pinned Lake closure.
No `lake update`, `lake build`, dependency clone/fetch, or dependency write was
performed. The untracked `.lake` symlink makes this nonrelease evidence.
Trust-zero Lean outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Structured anchor invariants passed at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open `M3`, analytic package `M4`. |
| Isolated `lake env` Lean `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` | 0 | Exact target, conditional composition, and five tensor-seminorm anchors elaborated. Both axiom reports listed only `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-closure search for analytic Grothendieck/Krivine, random or hyperplane rounding, correlated signs, and inverse-sine expectation | 1 | Expected no-match across all already-pinned Lake packages. |
| `git log --all -S'<exact local target name>' --format='%H %s' -- '*.lean'` | 0 | Only statement, intake, obligation-tree, and evidence history was found; no lost terminal proof body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match; no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe, opaque, extern, implementation override, or native-decision shortcut. |
| Sourcegraph global archived/forked Lean search for Grothendieck inequality/Krivine | 0 | The only matches were unrelated Krivine abstract-machine/compiler tests; no analytic theorem appeared. |
| GitHub repository search for `Grothendieck inequality Lean` | 0 | `total_count=0`; bounded discovery evidence only. GitHub code search returned HTTP 403 and grep.app returned HTTP 429, both recorded as access limits rather than absence evidence. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386...a95`; tree `bdc39a31...2c2b`; dependency tree clean. |

The isolated replay was:

```bash
set -u
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-headed959a5a.XXXXXX)
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
`M0325-B-SCALAR`, `M0325-L-EXPECTATION`, and `M0325-T-PACKAGE`. Resume a child
only when its exact placeholder-free body can be implemented or an immutable
compatible Lean 4 body can be pinned, exact-type transported, and kernel
checked.
