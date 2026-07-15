# THM-M-1228 proof-phase recheck at `69f012f9` (slot 16)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `69f012f979c7114db1ee4a877c5742d4742cadba`

Base tree: `a4415d1a7f473d7540904dd4fd84d17ac0f99820`

## Verdict

`blocked`. No placeholder-free positive proof body can inhabit the exact frozen
target without changing its meaning. Its declaration is the family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and the three predicate fields of `CKNSourceSemantics` have no laws connecting
suitability to regularity or parabolic measure. A premise-free theorem with a
parameter `S : CKNSourceSemantics` would be universally generalized. The
tracked, placeholder-free `ProofBlocker.lean` selects a permitted semantics in
which suitability is true and the required measure-zero predicate is false.
Fresh trust-zero Lean replay checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with `[propext, Classical.choice, Quot.sound]`. This refutes only the arbitrary-
semantics universal closure, not the mathematical Caffarelli-Kohn-Nirenberg
theorem. Selecting favorable semantics, assuming the per-solution conclusion,
storing that conclusion as a structure field, or replacing parabolic with
ambient Euclidean Hausdorff measure would substitute a different theorem and
was not done.

The proof dependency is also unfinished. The authoritative DAG records
`S56-M-1228-OBLIGATION_TREE` as provisional `[_]`, not master-accepted `[x]`.
Its registry assigns no terminal body to the root or the four-obligation cut:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

`ObligationTree.root_compose` merely consumes the complete per-solution
analytic conclusion as a premise. Pinned mathlib contains adjacent
distribution, smoothness, Lp, ambient Hausdorff, and covering APIs, but no
suitable weak Navier-Stokes semantics, parabolic Hausdorff measure,
epsilon-regularity theorem, bad-cylinder estimate, or terminal CKN body. The
historical `S1_M_156` surface stores essential conclusions in package fields,
and the immutable external audit supplies no exact compatible proof to pin.

The predecessor evidence also remains fail-closed: `check_statement.py`
reports the spatial-dimension mutation killed without elaborating or comparing
that declaration, all fifteen node recipes point at the same conditional
composition harness, and the intake discovery-protocol hash is null. A proof
worker may not rewrite those predecessor artifacts or the authoritative DAG.

There were already 46 JSON and 46 Markdown recheck packets plus three proof-
attempt Markdown records before this run, while the DAG still reports zero
proof attempts and no children. This exceeds the section 10.2 five-tick split
threshold. The master must reconcile these packets and split statement repair
from the analytic obligations instead of scheduling the same monolithic proof
task again.

The lifecycle stays `planned`, the vector stays `H1/M4/R4`, and the assigned
item stays `[ ]`. No positive body, closed obligation, receipt, audit
completion, theorem completion, or master acceptance is claimed.

## Validation

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink targets the canonical pinned artifacts and
was treated read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, ref repair, network action, or `.lake` mutation was performed. The
trust-zero replay copied three owned Lean inputs to a temporary directory under
the worker root and removed all temporary output on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets; stdout SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546; stdout SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; stdout SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `timeout --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; validator reports four mutations killed; stdout SHA-256 `915e7167391aba59f968d010a81196a2df89f22d6c290d5e1a9152260b623b05`. Its spatial-dimension coverage defect remains as described above. |
| `timeout --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree; stdout SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `timeout --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | Passed 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root remains M4; stdout SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. |
| `(cd Formalizations/Lean && LAKE_NO_UPDATE=1 lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Scoped pinned `lake env` resolution and `lean --trust=0 -t0` replay | 0 | `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` elaborated; both negative declarations and conditional composition report only `[propext, Classical.choice, Quot.sound]`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | Pinned mathlib tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | Manifest-pinned revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |
| Token-anchored prohibited-construct scan over owned Lean files | 1 expected | No `sorry`, `admit`, bodyless `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token was found. |
| `python3 -m json.tool <this JSON packet>` and blocker invariant assertions | 0 | JSON parsed; identity, base, blocked verdict, `[ ]` state, unchanged vector, false completion fields, empty receipts, root cut, changed paths, and self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in tracked owned-path differences. |
| `git diff --no-index --check /dev/null <each new packet>` | 1 expected each | Both commands produced empty output; exit 1 records content differences, not whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful replay core was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d "$ROOT/.thm-m-1228-69f012f9-XXXXXX")
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 60s lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 60s lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" \
  "$TARGET/ObligationTree.lean" "$TMP"/
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ProofBlocker.lean"
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- blocker stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- composition stdout: `c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
- every stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`

## Retry Condition

The master must reconcile the repeated packets and predecessor state, then
reopen and version the statement around fixed, source-faithful definitions of
suitable weak Navier-Stokes solutions, regular points, and one-dimensional
parabolic Hausdorff measure. Complete the source and mutation gates, freeze a
corrected registry with node-accurate recipes, and split the repair plus four
analytic cut obligations into dependency-legal children. Then implement local
placeholder-free bodies or immutably pin exact compatible bodies, with checked
transports, composition, trust, and terminal-body provenance.

Because the assigned positive proof phase is not genuinely self-tested
complete, `.stage1-worker-selftest.json` is deliberately absent.
