# THM-M-1228 proof-phase blocker at `d71fe284` (slot 17)

Item: `S56-M-1228-PROOF`

Recorded: `2026-07-16T00:56:49+08:00` (Asia/Shanghai)

Base revision: `d71fe284446b9f58daa00496a4e6530a42136324`

Base tree: `a73161e038e592f66fb80c29bf13672d58f60c64`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen
target. The canonical declaration is the family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and `CKNSourceSemantics` supplies no laws connecting its three predicate
fields. The tracked, placeholder-free `ProofBlocker.lean` selects an allowed
interpretation in which suitability is true, regularity is false, and the
measure-zero predicate is false. Pinned Lean 4.29.0 at trust level zero checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with only `[propext, Classical.choice, Quot.sound]`. A proof uniform over the
frozen interface would therefore contradict a kernel-checked countermodel.
This exposes an encoding blocker; it does not refute every specialization or
the mathematical Caffarelli-Kohn-Nirenberg theorem. Choosing favorable
predicates, storing the conclusion in a structure field, replacing parabolic
measure by ambient Hausdorff measure, or proving a smooth or two-dimensional
result would change the theorem and was not done.

The required predecessor `S56-M-1228-OBLIGATION_TREE` remains provisional
`[_]`, not master-accepted `[x]`. Its only named terminal body is
`ObligationTree.root_compose`, which assumes the complete per-solution
analytic conclusion. The frozen root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

Pinned mathlib has adjacent distribution, Lp, smoothness, Sobolev, and ambient
Hausdorff infrastructure, but no suitable weak Navier-Stokes definition,
parabolic Hausdorff theory, epsilon-regularity body, or terminal CKN
declaration. The four recorded immutable external trees have different
targets or unacceptable proof boundaries. Historical `S1_M_156` stores
central analytic claims as package fields and supplies no eligible terminal
body; `THM-M-1248` is the unrelated weighted interpolation theorem. There is
therefore no exact candidate to pin, import, or wrap.

The predecessor artifacts also expose proof-phase validation debt:

- `check_statement.py` reports `MutationChangedSpatialDimension` killed but
  does not include it in the declarations that it elaborates and compares.
- All 15 node recipes invoke the same `ObligationTree.lean` harness; the
  conditional composer assumes the whole per-solution analytic conclusion.
- The harness repeats the statement interface rather than importing it, and
  no checked harness-to-canonical transport is present.
- `README.md` still contains a stale intake verdict predating the elaborated
  statement and disagrees with the later `R4` graph classification.

These findings do not change the first failed proof gate, which is
`M1228-S-CONCRETE`; they prevent any positive proof or validation credit from
being inferred from the predecessor checks.

Before this run, the target already contained 47 JSON and 47 Markdown proof
recheck packets, seven dated JSON blocker packets, and five dated Markdown
blocker packets. The authoritative DAG still records `attempts: 0` and
`children: []`. This exceeds the five-unresolved-tick split rule in section
10.2 of the rev-5.6 blueprint. The master must reconcile the repeated evidence,
version the defective statement/registry, and split statement repair from the
analytic obligations instead of dispatching this same monolithic proof task
again.

Lifecycle remains `planned`; the root remains `H1/M4/R4`; the proof item stays
`[ ]`. No positive proof body, closed analytic obligation, receipt, audit
completion, theorem completion, or master acceptance is claimed. Because the
assigned phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only and points to the
canonical pinned artifacts. No Lake update/build, dependency clone/fetch,
network action, checkout, ref mutation, or `.lake` write was performed. Lean
outputs were isolated under `/tmp` and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 targets; stdout SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546; stdout SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; stdout SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `LAKE_NO_UPDATE=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Canonical expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; stdout SHA-256 `915e7167391aba59f968d010a81196a2df89f22d6c290d5e1a9152260b623b05`. Its dimension-mutation coverage claim is limited as recorded above. |
| `LAKE_NO_UPDATE=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, the mathlib pin, and four immutable-tree receipts agree; stdout SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `LAKE_NO_UPDATE=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | Passed 15 obligations and 31 typed edges; the root stays M4 with the four-obligation cut; stdout SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. This structural pass does not validate analytic bodies. |
| Isolated scoped `lake env` resolution followed by `lean --trust=0 -t0` replay | 0 | `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` elaborated. The two countermodel theorems and conditional composer report `[propext, Classical.choice, Quot.sound]`. |
| Token-anchored prohibited-construct scan over owned `*.lean` files | 0 | The wrapper proved that no `sorry`, `admit`, bodyless `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `extern`, or `native_decide` token matched. |
| `git diff --exit-code c45f3c709..HEAD -- <proof-relevant inputs>` | 0 | Statement, countermodel, composition harness, registry, graphs, anchor audit, and validation specs are unchanged. |
| Repo/pinned search for `CaffarelliKohnNirenbergTarget`, `Caffarelli.Kohn.Nirenberg`, `SuitableWeakSolution`, and `ParabolicHausdorff` | 0 | 112 lines in nine files, limited to this dossier, the nonterminal historical surface, and the neighboring unrelated THM-M-1248 dossier; no exact positive body appears. Search-output SHA-256 `067719bdf76d72193466cf28d8eff2d969c5c8cd83e94334c32c57e6cc5a602c`. |
| `git log --all -- Stage1_Instances/THM-M-1228/Proof.lean` | 0 | Empty output; repository history contains no positive proof module for this target. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent, as required for this blocked phase. |

The exact trust-zero replay core was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d /tmp/thm-m-1228-proof-d71fe284-slot17.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --foreground --kill-after=5s 120s lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --foreground --kill-after=5s 120s lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" \
  "$TARGET/ObligationTree.lean" "$TMP"/
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/ProofBlocker.olean" "$TMP/ProofBlocker.lean"
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
```

Replay stdout SHA-256 values were
`e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
for the statement,
`392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
for the countermodel, and
`c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
for conditional composition. Every stderr stream was empty. Temporary olean
SHA-256 values were `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`,
`a500a9ba8d428258ec8ff7aea230c345c636dcd8ae2ac94c769b55c1f2571d8f`,
and `f8a03c63f7bee9b4e5babfe68093df5ccbca2d400bec42849a0766b0418cae77`.
The Lean executable SHA-256 is
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`;
the pinned mathlib commit/tree is
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

The master must reopen and version the target around fixed, source-faithful
definitions of suitable weak solutions, regular points, and one-dimensional
parabolic Hausdorff measure; repair and re-freeze the obligation registry; and
split the proof work. Execution can resume only after placeholder-free local
implementations or an immutable compatible dependency supplies exact bodies
for concrete semantics, epsilon regularity, covering, and measure, with
checked transport, node-specific validation, composition, trust, and
terminal-body provenance.
