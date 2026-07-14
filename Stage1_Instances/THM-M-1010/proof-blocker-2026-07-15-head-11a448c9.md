# THM-M-1010 proof recheck at `11a448c9`

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T05:58:58+08:00`

Base revision: `11a448c97289d30fe7c8c05dbac5a283a9d00896`

Base tree: `a79f60552d328e98302026909ec6676cb6cd6ea2`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_1010.Target`. The root vector remains
`[H1, M3, R3]`, and the proof item remains `[ ]`.

The root requires a common-space realization for every weakly convergent
sequence of probability measures on every Polish space, with exact laws and
full-sequence almost-sure convergence. The checked bodies currently available
under the owned path do not prove that claim:

- `ObligationTree.target_of_couplingPackage` consumes an assumed
  `CouplingPackage S`; it checks final composition but does not construct the
  package.
- `representation_of_constant_laws` and `target_for_constant_sequence` prove
  only the constant-law boundary case.

The first unavailable construction is `M1010-N-PARTITIONS`, and the resulting
root-blocking node is `M1010-C-COUPLING`. Pinned mathlib supplies a measurable
small-diameter partition, weak-convergence and Levy-Prokhorov interfaces,
single-law realization on the unit interval, and a.e. subsequence extraction
after common-space convergence in measure. It does not supply refining
null-boundary partitions or a compatible realization of all prescribed laws
whose full sequence converges almost surely.

In particular, applying `Measure.exists_measurable_map_eq` separately to each
law proves exact marginals but creates no convergence relation among the
selected maps. A measurable equivalence with a real subset also cannot
transport the conclusion because it need not preserve the Polish topology.
The only immutable external candidate recorded by the owned audit is
Real-only and terminates in `by sorry`; it is both a target mismatch and an
ineligible placeholder.

The frozen remaining root cut set is `M1010-N-PARTITIONS`,
`M1010-C-INTERVAL`, `M1010-L-MEASURABLE`, `M1010-L-LAWS`, and
`M1010-L-AE-STABILIZE`. Those leaves must close before the internal metric-
convergence and coupling nodes, followed by the checked composer, can close
the exact root.

Because the requested proof phase is incomplete, no proof receipt or
`.stage1-worker-selftest.json` is emitted. Retry requires placeholder-free
implementations of the five frozen leaves, or an immutable exact Polish-space
Lean 4 proof that can be pinned and checked.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed. Generated
Lean outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `11a448c97289d30fe7c8c05dbac5a283a9d00896`, tree `a79f60552d328e98302026909ec6676cb6cd6ea2`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at the L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned hard-mathlib anchor/wrapper lane; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `8cf08f66...16016`; conditional composer axioms are `propext`, `Classical.choice`, and `Quot.sound`; root explicitly remains open at M3. |
| Isolated pinned three-module replay shown below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated with `--trust=0 -t0`; the conditional composer and both constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Log hashes were `e3b0c442...b855`, `cbee87b9...9abb`, and `940c65d9...9673`; temporary statement/tree object hashes were `2675f2bc...3df` and `a11e8641...ca7`. |
| Prohibited-construct scan over owned `*.lean` files | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle construct, or equivalent declaration form was found. |
| `rg -ni 'skorokhod\|skorohod' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '*.md' --glob '*.tex'` | 1 expected | No match in the complete pinned dependency source tree. |
| Pinned tool and dependency identity checks | 0 | Lean `4.29.0` commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree; toolchain and manifest hashes match the statement receipt. |
| Root-input freshness against bases `d3d4bc99` and `00f98378` | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and all listed structured root inputs are byte-unchanged; later integrations added blocker evidence only. |

Exact prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1010 --glob '*.lean'
```

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1010"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1010-proof-slot42-11a448c9.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"
lean_bin=$(cd "$lean_root" && timeout 120 lake env which lean)
lean_path=$(cd "$lean_root" && timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean_bin" --trust=0 -t0 \
  -R "$repo" -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean_bin" --trust=0 -t0 \
  -R "$repo" -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  "$target/ObligationTree.lean" >"$tmp/obligation.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean_bin" --trust=0 -t0 \
  -R "$repo" "$target/Proof.lean" >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/obligation.log" "$tmp/proof.log" \
  "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean"
```

This is current-base nonrelease blocker evidence only. It is not a proof
receipt, does not satisfy `S56-M-1010-PROOF`, proposes no checklist
transition, and makes no audit-completion, theorem-completion, validation,
release, or master-acceptance claim.
