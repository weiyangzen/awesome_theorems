# THM-M-0325 proof-phase recheck at `11a448c9`

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-15` (`Asia/Shanghai`)

Base revision: `11a448c97289d30fe7c8c05dbac5a283a9d00896`

Base tree: `a79f60552d328e98302026909ec6676cb6cd6ea2`

## Verdict

`blocked`. The frozen proposition is the full finite real Grothendieck
inequality. No placeholder-free Lean body inhabiting
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

Pinned mathlib supplies finite-span, Gram, Gaussian, integration, and
projective/injective tensor-seminorm infrastructure. The historical
`S1_M_214.lean` module also proves elementary bounds, rank-one and one-row or
one-column special cases, and structural wrappers. Neither source contains the
real Grothendieck/Krivine transform and universal coefficient bound, the
correlated Gaussian-sign identity, the expectation estimate, or a terminal
Grothendieck inequality. The first unavailable substantive gate is
`M0325-K-TRANSFORM`. The other open analytic obligations are
`M0325-N-FINITE-SPAN`, `M0325-N-GRAM`, `M0325-R-RANDOM`,
`M0325-B-MEASURABLE`, `M0325-B-SCALAR`, `M0325-L-EXPECTATION`, and
`M0325-T-PACKAGE`.

Since the preceding proof recheck, this target changed only by integration of
that recheck's JSON and Markdown blocker evidence. No owned Lean proof source,
obligation registry, typed graph, validation spec, dependency lock, or
toolchain pin changed. Repository history contains no lost terminal body for
the exact local target names.

Nine prior tracked unresolved proof-recheck pairs existed before this run.
Rev-5.6 section 10.2 requires a split after five unresolved execution ticks,
but the authoritative DAG still records zero attempts and no children. This
worker may not edit the DAG or generated checklist. The master must therefore
split this oversized proof item into dependency-legal children before another
proof attempt.

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
| Isolated `lake env` Lean replay with `--trust=0 -t0` of `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` | 0 | Exact target, conditional composition, and five tensor-seminorm anchors elaborated. Both axiom reports listed only `propext`, `Classical.choice`, and `Quot.sound`. The olean hashes were `5da713d6...cdd7d`, `6588e3bc...d2a`, and `7e864ef4...d1d0`. |
| Pinned-closure search for analytic Grothendieck/Krivine, Gaussian-sign or hyperplane/random rounding, and arcsine expectation/correlation | 1 | Expected no-match across all already-pinned Lake packages. |
| `git log --all -S'<exact local target name>' --format='%H %s' -- '*.lean'` | 0 | Only statement, intake, obligation-tree, and evidence history was found; no lost terminal proof body. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match; no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe, opaque, extern, implementation override, or native-decision shortcut. |
| Sourcegraph global archived/forked Lean search for Grothendieck inequality/Krivine | 0 | 33 matches in one repository, all unrelated Lean compiler tests for a Krivine abstract machine or reduction; no analytic theorem appeared. |
| GitHub repository search for `Grothendieck inequality Lean` | 0 | `total_count=0`, `incomplete_results=false`; bounded discovery evidence only. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386...a95`; tree `bdc39a31...2c2b`; dependency tree clean. |
| `git diff --check -- Stage1_Instances/THM-M-0325/proof-recheck-2026-07-15-head-11a448c9.{json,md}` | 0 | No whitespace errors. |

The isolated replay was:

```bash
set -u
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-head11a448c9.XXXXXX)
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
