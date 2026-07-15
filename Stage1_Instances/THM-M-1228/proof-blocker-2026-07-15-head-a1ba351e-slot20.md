# THM-M-1228 proof-phase blocker at `a1ba351e` (slot 20)

Item: `S56-M-1228-PROOF`

Recorded: 2026-07-15 (Asia/Shanghai)

Base revision: `a1ba351e42fd9eefe315119ef09c0b958358bb8e`

Base tree: `eed1b90627305460f9cee46277fc7c0cb235d1df`

## Verdict

`blocked`. An exact positive proof cannot be implemented or imported for the
current frozen target. Its canonical declaration is the family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

but the three predicates in `CKNSourceSemantics` have no laws connecting
suitability, regularity, and parabolic measure. The tracked, placeholder-free
`ProofBlocker.lean` specializes this permitted interface with suitability true,
regularity false, and the measure-zero predicate false. Pinned Lean checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

at trust level zero. Thus any proof uniform over the current semantic interface
would contradict a kernel-checked countermodel. This diagnoses the formal
encoding; it neither proves nor refutes the genuine mathematical
Caffarelli-Kohn-Nirenberg theorem. Choosing favorable semantics, assuming the
per-solution conclusion, substituting ambient Hausdorff measure, or proving a
smooth, two-dimensional, or global-regularity result would change the target
and was not done.

The required predecessor `S56-M-1228-OBLIGATION_TREE` is still provisional
`[_]`, not master-accepted `[x]`. Its registry has no closed obligations, and
`ObligationTree.root_compose` consumes the complete per-solution analytic
conclusion as a premise. The frozen open root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

Pinned mathlib contains adjacent distribution, smoothness, Lp, and ambient
Hausdorff APIs but no suitable weak Navier-Stokes, parabolic-Hausdorff,
epsilon-regularity, or exact terminal CKN theorem. The historical `S1_M_156`
surface stores essential analytic conclusions as package fields; the immutable
external audit likewise found no eligible body to import.

Before this run, 47 JSON and 47 Markdown proof-recheck packets already existed,
while the authoritative DAG still records `attempts: 0` and `children: []`.
This is beyond the five-unresolved-tick split threshold in section 10.2 of the
rev-5.6 standard. The integration lane must reconcile these attempts and split
the repair and analytic cut obligations instead of dispatching another
unchanged monolithic proof task.

Lifecycle remains `planned`, the frozen root vector remains `H1/M4/R4`, and the
proof item remains `[ ]`. No positive proof body, closed obligation, provisional
or accepted receipt, audit completion, theorem completion, or master acceptance
is claimed. Because the requested proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this automation clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only and points to the
canonical pinned artifacts. No Lake update/build, dependency clone/fetch,
network action, checkout, ref mutation, or `.lake` write was performed. Lean
outputs were isolated in a temporary directory under `/tmp` and removed by a
shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets; output SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets at ranks 1 through 1546; output SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; output SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, pinned mathlib, and four immutable external-tree receipts agree; output SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | Passed 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root remains M4 with the four-obligation cut; output SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. |
| Isolated pinned `lake env` resolution followed by `lean --trust=0 -t0` replay | 0 | `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` elaborated. The two negative declarations and conditional composer report only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-construct scan over owned `*.lean` files | 1 expected | No `sorry`, `admit`, bodyless `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token was found. |
| `git diff --exit-code c45f3c709..HEAD -- <proof-relevant inputs>` | 0 | Statement, countermodel, composition harness, registry, typed graphs, anchor audit, and validation specs are unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent, as required for a blocked phase. |

The successful replay core was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d /tmp/thm-m-1228-proof-a1ba351e.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 120s lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 120s lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" \
  "$TARGET/ObligationTree.lean" "$TMP"/
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ProofBlocker.lean"
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 600s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- countermodel stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- composition stdout: `c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
- every stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`

The environment was Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

The integration lane must reconcile the repeated attempts and predecessor
state, reopen and version the statement around fixed source-faithful analytic
definitions, repair statement-mutation and per-node validation coverage, and
freeze a corrected split registry. Execution can then resume only after local
implementations or an immutable compatible dependency supplies exact bodies
for every cut obligation with checked transports, composition, trust, and
terminal-body provenance.
