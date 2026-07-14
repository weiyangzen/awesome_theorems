# THM-M-1010 proof recheck at `00f98378`

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T05:39:30+08:00`

Base revision: `00f98378e8c1c63097871ae62aeed895d83b0cb4`

Base tree: `4f2396db6d6d1c2b9948f401079f136dd0ed8f16`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_1010.Target`. The root vector remains
`[H1, M3, R3]`, and the proof item remains `[ ]`.

The exact root quantifies over every weakly convergent sequence of probability
measures on every Polish space. The existing declarations do not close it:

- `ObligationTree.target_of_couplingPackage` consumes an assumed
  `CouplingPackage S`; it is conditional composition, not a construction.
- `representation_of_constant_laws` and `target_for_constant_sequence` prove
  only the constant-law boundary case.

The first unavailable construction is `M1010-N-PARTITIONS`, and the resulting
root-blocking node is `M1010-C-COUPLING`. Pinned mathlib supplies individual
law realizations on the unit interval, measurable small-diameter partitions,
Portmanteau mass convergence at null frontiers, product/disintegration
machinery, and a.e. subsequence extraction from an already common-space
convergence-in-measure hypothesis. It does not supply refining null-boundary
partitions and a compatible allocation of all prescribed laws whose full
sequence converges almost surely.

In particular, applying `Measure.exists_measurable_map_eq` independently to
each law proves exact marginals but gives no convergence relationship between
the selected maps. A Borel equivalence with a real subset also cannot
transport the conclusion because it need not preserve the Polish topology.
The only immutable external candidate recorded by the owned audit is Real-only
and terminates in `by sorry`; it is both a theorem mismatch and an ineligible
placeholder.

The frozen remaining root cut set is `M1010-N-PARTITIONS`,
`M1010-C-INTERVAL`, `M1010-L-MEASURABLE`, `M1010-L-LAWS`, and
`M1010-L-AE-STABILIZE`. Those leaves must close before the internal metric-
convergence and coupling nodes, followed by the already checked composer, can
close the exact root.

Because the requested positive proof phase is incomplete, no proof receipt or
`.stage1-worker-selftest.json` is emitted. Retry requires a placeholder-free
implementation of those five leaves, or an immutable exact Polish-space Lean
4 proof that can be pinned and checked.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed. Generated
Lean outputs were directed to `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `00f98378e8c1c63097871ae62aeed895d83b0cb4`, tree `4f2396db6d6d1c2b9948f401079f136dd0ed8f16`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at the L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned hard-mathlib anchor/wrapper lane; theorem incomplete. |
| isolated pinned three-module replay shown below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated with `--trust=0`; the conditional composer and two constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `timeout 240 python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 124 | Structural assertions reached the nested Lean check, which timed out without output under severe host-wide Lean process saturation; the equivalent narrower three-module replay succeeded. |
| prohibited-construct scan over owned `*.lean` files | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle construct, or equivalent declaration form was found. |
| pinned package-source scan for `skorokhod\|skorohod` | 1 expected | No match in the complete pinned dependency source tree. |
| direct pinned tool and dependency identity checks | 0 | Lean `4.29.0` commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree. |
| `python3 -m json.tool Stage1_Instances/THM-M-1010/proof-blocker-2026-07-15-head-00f98378.json` | 0 | The fresh structured blocker parses as JSON. |
| whitespace checks for both fresh blocker artifacts | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the proof phase is blocked. |

Exact prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1010 --glob '*.lean'
```

Exact Lean replay shape:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1010-proof-slot41.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH_PINNED=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_PINNED" "$LEAN_BIN" --trust=0 -t0 -R "$PWD" \
  -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  Stage1_Instances/THM-M-1010/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$LEAN_PATH_PINNED" "$LEAN_BIN" --trust=0 -t0 -R "$PWD" \
  -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  Stage1_Instances/THM-M-1010/ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$LEAN_PATH_PINNED" "$LEAN_BIN" --trust=0 -t0 -R "$PWD" \
  Stage1_Instances/THM-M-1010/Proof.lean
```

This is current-base blocker evidence only. It is not a proof receipt, does
not satisfy `S56-M-1010-PROOF`, proposes no checklist transition, and makes
no audit-completion, theorem-completion, validation, release, or master-
acceptance claim.
