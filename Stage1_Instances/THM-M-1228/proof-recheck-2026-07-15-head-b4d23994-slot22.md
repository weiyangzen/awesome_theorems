# THM-M-1228 proof-phase recheck at `b4d23994` (slot 22)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa`

Base tree: `5f13e0e86bde3bcaaef38b979819490c648166e3`

## Verdict

`blocked`. No placeholder-free positive proof body can inhabit the exact
frozen target without changing its meaning. The canonical declaration has
type

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and the three fields of `CKNSourceSemantics` are unconstrained predicates. A
premise-free declaration parameterized by `S : CKNSourceSemantics` would prove

```text
forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S.
```

The tracked, placeholder-free `ProofBlocker.lean` selects a permitted
interpretation in which suitability is true and the required measure-zero
predicate is false. Trust-zero Lean replay checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with only `[propext, Classical.choice, Quot.sound]`. This refutes the universal
closure of the arbitrary semantic interface, not the mathematical
Caffarelli-Kohn-Nirenberg theorem. Selecting favorable semantics, assuming the
per-solution conclusion, storing that conclusion in a structure field, or
replacing parabolic by Euclidean Hausdorff measure would prove a substituted
theorem and was not done.

The proof dependency is unfinished: the authoritative DAG records
`S56-M-1228-OBLIGATION_TREE` as provisional `[_]`, not accepted `[x]`. Its
registry assigns no positive proof body to the root or the frozen root cut:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

`ObligationTree.root_compose` is only a conditional binder-assembly theorem;
it assumes the complete per-solution analytic conclusion. The bounded anchor
audit still locates no exact terminal body in the repository, pinned dependency
closure, or four immutable external trees. Proof-relevant inputs have not
changed since `c45f3c709`, and repository history contains no target-local
`Proof.lean`, so no new candidate has entered the closure.

Two predecessor evidence defects remain fail-closed. `check_statement.py`
reports `MutationChangedSpatialDimension` as killed without actually comparing
that declaration. All fifteen structured node recipes invoke the same
conditional `ObligationTree.lean` harness, which contains no analytic proof
bodies and cannot validate the analytic nodes it names. A proof worker may not
rewrite those predecessor artifacts, the authoritative DAG, or the generated
checklist.

There were already 45 JSON and 45 Markdown proof-recheck packets before this
run, while the DAG still records zero proof attempts and no children. This is
beyond the rev-5.6 five-tick split threshold. The master must reconcile these
packets and split statement repair from the four analytic obligations rather
than schedule another identical oversized proof attempt.

The vector remains `H1/M4/R4`; lifecycle remains `planned`; the assigned item
remains `[ ]`. No positive proof body, closed obligation, accepted receipt,
audit completion, theorem completion, or master acceptance is claimed.

## Validation

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was reused
read-only. No Lake update/build, dependency clone/fetch, network action, or
`.lake` mutation was performed. The narrow replay copied its two Lean inputs
to `/tmp` and removed all temporary output on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)`; stdout SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)`; stdout SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete; stdout SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; toolchain and mathlib pin agree; stdout SHA-256 `915e7167391aba59f968d010a81196a2df89f22d6c290d5e1a9152260b623b05`. Its spatial-dimension mutation claim remains underchecked as described above. |
| `timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts`; stdout SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut; stdout SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. |
| `(cd Formalizations/Lean && LAKE_NO_UPDATE=1 lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Narrow `lake env lean --trust=0 -t0` replay below | 0 | The exact statement and both negative declarations elaborated; both declarations reported `[propext, Classical.choice, Quot.sound]`. |
| Token-anchored prohibited-construct scan over owned Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless `axiom`, or `unsafe` token was found. |
| `git log --all -- Stage1_Instances/THM-M-1228/Proof.lean` | 0 | Empty output; repository history contains no positive target proof file. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse 'HEAD^{tree}'` | 0 | `32c9eace926573a9981787ae97643e520353c893` |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-b4d23994-slot22.json` | 0 | The current-base structured blocker parses as JSON. |
| Scoped blocker invariant check | 0 | Identity, base revision/tree, blocked verdict, `[ ]` state, unchanged H1/M4/R4 vector, false completion fields, empty receipts, root cut, changed paths, and self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in the scoped tracked diff; the fresh untracked packets were checked separately. |
| `git diff --no-index --check /dev/null <each fresh packet>` | 1 expected each | Both content-difference exits produced zero diagnostic bytes; neither fresh file has a whitespace error. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful narrow replay was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d /tmp/thm-m-1228-proof-b4d23994.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --foreground --kill-after=5s 60s lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --foreground --kill-after=5s 60s lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" "$TMP"/
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ProofBlocker.lean"
```

Replay stdout SHA-256 values were
`e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
(statement) and
`392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
(countermodel). Each stderr SHA-256 was
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The temporary `Statement.olean` SHA-256 was
`9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`;
the Lean executable SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.

Input SHA-256 values:

- `Statement.lean`: `e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`
- `ProofBlocker.lean`: `b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`
- `ObligationTree.lean`: `850cb3402e9c9c91fee41fefd6264f30681a172cc87757b29ed1c33beec34fe7`
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `anchor-audit.json`: `8d18f2332859b387552de7370c72674407d61f7260eb4dd476856694f7a7ba32`
- `validation-specs.json`: `8bc384e7935c1728f703811336580989e3b59f78317c67e6cd9914d5145b318b`

## Retry Condition

Master-reconcile the repeated attempts and predecessor state. Reopen and
version the statement around fixed, source-faithful definitions of suitable
weak Navier-Stokes solutions, regular points, and one-dimensional parabolic
Hausdorff measure. Repair the mutation and node-validation coverage, freeze a
corrected split registry, then implement locally or immutably pin exact bodies
for all four root-cut obligations with checked transports, composition, trust,
and terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
