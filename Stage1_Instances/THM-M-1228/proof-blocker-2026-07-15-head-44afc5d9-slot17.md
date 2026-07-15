# THM-M-1228 proof-phase blocker at `44afc5d9` (slot 17)

Item: `S56-M-1228-PROOF`

Recorded: 2026-07-15 (Asia/Shanghai)

Base revision: `44afc5d93ff24855c0f4cc5ae48f4b6be094a08e`

Base tree: `4fbba127c10efa3d76cb99767630cf3034a84ada`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target.
The canonical declaration is a family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

whose parameter contains three unconstrained predicates. There are no laws
connecting suitability, regularity, and parabolic measure zero. The tracked,
placeholder-free `ProofBlocker.lean` chooses an allowed interpretation with
suitability true, regularity false, and measure zero false. Pinned Lean 4.29.0
at trust level zero checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

Both declarations report only `propext`, `Classical.choice`, and `Quot.sound`.
Thus a proof uniform over the frozen interface would contradict a
kernel-checked countermodel. This exposes an encoding blocker; it does not
prove or refute the source-faithful Caffarelli-Kohn-Nirenberg theorem. Picking
favorable predicates, storing the conclusion as a field, replacing parabolic
measure by ambient Hausdorff measure, or proving a smooth or two-dimensional
result would substitute a different theorem and was not done.

The required predecessor `S56-M-1228-OBLIGATION_TREE` remains provisional
`[_]`, not master-accepted `[x]`. Its only terminal body is the conditional
composer `root_compose`, which assumes the complete per-solution analytic
conclusion. The frozen open root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

The pinned audit finds adjacent distribution, smoothness, Lp, and ambient
Hausdorff infrastructure, but no suitable weak Navier-Stokes definition,
parabolic-Hausdorff theory, epsilon-regularity theorem, or terminal CKN proof.
The four immutable external trees contain different targets or inadmissible
proof boundaries. Historical `S1_M_156` stores the missing analytic results as
package fields and therefore supplies no terminal proof body.

Before this run there were already 47 JSON and 47 Markdown proof-recheck
packets, while the authoritative DAG still recorded `attempts: 0` and no
children. This exceeds the five-unresolved-tick split rule in section 10.2 of
the rev-5.6 standard. The master must reconcile the repeated evidence and
split statement repair from the analytic obligations rather than schedule the
same monolithic proof item again.

Lifecycle remains `planned`; the root remains `H1/M4/R4`; the proof item stays
`[ ]`. No proof body, closed analytic obligation, receipt, audit completion,
theorem completion, or master acceptance is claimed. Because the requested
proof phase is not genuinely complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only and points to the
canonical pinned artifacts. No Lake update/build, dependency clone/fetch,
network action, checkout, ref mutation, or `.lake` write was performed. Lean
outputs were isolated in a fresh worker-root temporary directory and removed
by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 targets; stdout SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546; stdout SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; stdout SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `LAKE_NO_UPDATE=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Canonical expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; stdout SHA-256 `915e7167391aba59f968d010a81196a2df89f22d6c290d5e1a9152260b623b05`. |
| `LAKE_NO_UPDATE=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree; stdout SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `LAKE_NO_UPDATE=1 timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | Passed 15 obligations and 31 typed edges; root stays M4 with the four-obligation cut; stdout SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. |
| Scoped `lake env` resolution followed by `lean --trust=0 -t0` replay | 0 | `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` elaborated; both countermodel theorems and the conditional composer report `[propext, Classical.choice, Quot.sound]`. |
| Token-anchored prohibited-construct scan over owned `*.lean` files | 0 | The wrapper proved no `sorry`, `admit`, bodyless `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token matched. |
| `git diff --exit-code c45f3c709..HEAD -- <proof-relevant inputs>` | 0 | Statement, countermodel, composition harness, registry, graphs, anchor audit, and validation specs are unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent, as required for this blocked phase. |

The successful pinned replay was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d "$ROOT/.thm-m-1228-proof-44afc5d9.XXXXXX")
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
for composition. Every stderr stream had the empty-file SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The Lean executable SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.

## Retry Condition

The master must reopen and version the target around fixed, source-faithful
definitions of suitable weak solutions, regular points, and one-dimensional
parabolic Hausdorff measure; repair and re-freeze the registry; and split the
proof work. Execution can resume only after local implementations or an
immutable compatible dependency supplies exact bodies for concrete semantics,
epsilon regularity, covering, and measure, with checked transport,
composition, trust, and terminal-body provenance.
