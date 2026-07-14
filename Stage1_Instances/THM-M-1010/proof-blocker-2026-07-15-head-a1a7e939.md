# THM-M-1010 proof recheck at `a1a7e939`

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T05:01:35+08:00`

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_1010.Target`. The root vector remains
`[H1, M3, R3]`, and the proof item remains `[ ]`.

The repo-local declarations remain substantive but nonterminal:

- `ObligationTree.target_of_couplingPackage` is checked composition from an
  assumed `CouplingPackage S`; it does not construct that package.
- `representation_of_constant_laws` and `target_for_constant_sequence` prove
  the constant-law boundary only.

The first unavailable construction is `M1010-N-PARTITIONS`, and the resulting
root-blocking node is `M1010-C-COUPLING`. Pinned mathlib supplies small
measurable partitions, Portmanteau mass convergence at null frontiers,
one-law realization on the unit interval, product and disintegration APIs,
and a.e. subsequence extraction from an already common-space convergence-in-
measure hypothesis. It does not supply refining null-boundary partitions and
a compatible allocation of every prescribed law whose full sequence
converges almost surely.

In particular, applying `Measure.exists_measurable_map_eq` independently to
each law establishes exact marginals but no relationship among the chosen
maps. A measurable Borel equivalence with a real subset also cannot transport
the desired convergence because it need not preserve the Polish topology.
The sole immutable external candidate recorded by the owned audit is
Real-only and ends in `by sorry`; it is both a statement mismatch and an
ineligible placeholder.

The frozen remaining root cut set is `M1010-N-PARTITIONS`,
`M1010-C-INTERVAL`, `M1010-L-MEASURABLE`, `M1010-L-LAWS`, and
`M1010-L-AE-STABILIZE`. Closing these leaves discharges the internal metric-
convergence and coupling nodes; the already checked composer can then close
the exact root.

Because the requested positive proof phase is not complete, no proof receipt
or `.stage1-worker-selftest.json` is emitted. The retry condition is a
placeholder-free implementation of those five leaves, or an immutable exact
Polish-space Lean 4 proof that can be pinned and checked.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed. Generated
Lean outputs were directed to `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `a1a7e939e58f103f5ff5d23af51437fa8658aa04`, tree `d881fd9641fa3e5f3ebe5082b35672981e90adcf`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at the L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; planned hard-mathlib anchor/wrapper lane; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `8cf08f66...16016`; conditional composer reports `propext`, `Classical.choice`, and `Quot.sound`; root explicitly remains open at M3. |
| isolated pinned `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | terminated | The direct replay did not finish amid severe host-wide Lean process saturation and was terminated by the worker without a captured normal exit, output, or retained artifact. The structural validator independently completed its nested pinned check of `ObligationTree.lean`; a current-run full replay of `Proof.lean` remains a known validation failure. |
| prohibited-construct scan over owned `*.lean` files | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle construct, or equivalent declaration form was found. |
| pinned package-source scan for `skorokhod|skorohod` | 1 expected | No match in the complete pinned dependency source tree. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...ab16740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}; git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | Pinned mathlib `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree. |
| `python3 -m json.tool Stage1_Instances/THM-M-1010/proof-blocker-2026-07-15-head-a1a7e939.json` | 0 | The fresh structured blocker parses as JSON. |
| no-index whitespace checks for both fresh blocker artifacts | 0 | Both fresh files differ from `/dev/null` and have no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the proof phase is blocked. |

Exact prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1010 --glob '*.lean'
```

This is current-base blocker evidence only. It is not a proof receipt, does
not satisfy `S56-M-1010-PROOF`, proposes no checklist transition, and makes
no audit-completion, theorem-completion, validation, release, or master-
acceptance claim.
