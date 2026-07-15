# THM-M-1228 proof-phase recheck at `8f3190fe` (slot 12)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `8f3190fed598f6cb4547035d0d96d460ba5fc5cc`

Base tree: `d8ca24ac4a840d07b81dcc099a4d31023046d649`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen
target. The canonical declaration is the family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and `CKNSourceSemantics` gives no laws connecting its three predicate fields.
The tracked, placeholder-free `ProofBlocker.lean` chooses an allowed
interpretation with suitability true, regularity false, and the measure-zero
predicate false. A trust-zero Lean replay checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with `[propext, Classical.choice, Quot.sound]`. A proof uniform over the frozen
interface would contradict this kernel-checked countermodel. This is a defect
in the present formal interface; it neither proves nor refutes the mathematical
Caffarelli-Kohn-Nirenberg theorem. Choosing favorable semantics, assuming the
per-solution conclusion, replacing parabolic measure with ambient Hausdorff
measure, or proving a smooth or two-dimensional substitute was not done.

The authoritative predecessor `S56-M-1228-OBLIGATION_TREE` remains provisional
`[_]`, not master-accepted `[x]`. Its registry has no terminal analytic proof
bodies. `ObligationTree.root_compose` only consumes the full per-solution
conclusion as a premise. The frozen open root cut is unchanged:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

Pinned mathlib has adjacent Sobolev and ambient Hausdorff infrastructure but no
suitable weak Navier-Stokes, parabolic-Hausdorff, epsilon-regularity, or exact
terminal CKN theorem. The historical `S1_M_156` surface stores essential
analytic conclusions as package fields and provides no terminal proof body.
The immutable anchor audit likewise remains at `M4` with no exact positive
body.

There were already 37 JSON and 37 Markdown proof-recheck packets before this
run, while the authoritative DAG still records `attempts: 0` and `children: []`.
This exceeds the five-tick split threshold. The master must reconcile these
packets and split statement repair from the four analytic cut obligations
rather than schedule another identical attempt.

The root vector stays `H1/M4/R4`; lifecycle stays `planned`; the item stays
`[ ]`. No positive proof body, closed obligation, accepted receipt, audit
completion, theorem completion, or master acceptance is claimed.

## Validation

Commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink reused the canonical pinned artifacts
read-only. No Lake update/build, dependency clone/fetch, network action, or
`.lake` mutation was performed. The trust-zero replay used a temporary
directory under the worker root and removed it.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed; stdout SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required; stdout SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; stdout SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `LAKE_NO_UPDATE=1 timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; stdout SHA-256 `915e7167391aba59f968d010a81196a2df89f22d6c290d5e1a9152260b623b05`. |
| `LAKE_NO_UPDATE=1 timeout 300 python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree; stdout SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `LAKE_NO_UPDATE=1 timeout 300 python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | 15 obligations, 31 typed edges, denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root remains open at M4; stdout SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. |
| `(cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 60 lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Scoped `lake env` resolution followed by `lean --trust=0 -t0` on isolated copies of `Statement.lean` and `ProofBlocker.lean` | 0 | The exact statement and both countermodel theorems elaborated; both negative declarations reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration token. |
| `git diff --exit-code c45f3c709..HEAD -- <proof-relevant inputs>` | 0 | Statement, countermodel, composition, registry, graphs, anchor audit, and validation specs are unchanged. |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-8f3190fe-slot12.json >/dev/null` | 0 | The current-base structured blocker is valid JSON. |
| Scoped blocker invariant check | 0 | Identity, base revision/tree, blocked verdict, `[ ]` state, unchanged cut, false completion fields, empty receipts, changed paths, repeat counts, and self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in the scoped tracked diff. |
| `git diff --no-index --check /dev/null <new packet>` | 1 each | Expected content-difference exits with empty stdout/stderr for both new files, so neither has whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful trust-zero replay core was:

```bash
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d "$ROOT/.thm-m-1228-lean.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" "$TMP"/
LEAN_BIN=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  lake env printenv LEAN_PATH)
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 timeout 300 "$LEAN_BIN" \
  --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 timeout 300 "$LEAN_BIN" \
  --trust=0 -t0 --root="$TMP" "$TMP/ProofBlocker.lean"
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- countermodel stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- each stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`

Two predecessor evidence defects remain fail-closed. `check_statement.py`
incidentally elaborates the whole source, but does not print, extract, or
compare `MutationChangedSpatialDimension`, although it adds that name to
`killed_mutations`. All fifteen structured node recipes invoke the conditional
`ObligationTree.lean` harness and therefore do not validate analytic proof
bodies for the nodes they name. A proof worker may not rewrite those
predecessor artifacts or the authoritative DAG.

## Retry Condition

Master-reconcile the repeated attempts and predecessor state. Reopen and
version the statement around fixed, source-faithful definitions of suitable
weak Navier-Stokes solutions, regular points, and one-dimensional parabolic
Hausdorff measure. Repair mutation and per-node validation coverage, freeze a
corrected split registry, then implement locally or immutably pin exact bodies
for all four cut obligations with checked transports, composition, trust, and
terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
