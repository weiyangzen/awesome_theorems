# THM-M-1228 proof-phase recheck at `19eddccb` (slot 18)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `19eddccb8988b4da9e007b60f4a25b6806877160`

Base tree: `1b5d55ad37802063bf31881e5e06faa0410bf21c`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the frozen target.
Its exact declaration is a family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

whose three semantic predicates are unconstrained. The tracked,
placeholder-free `ProofBlocker.lean` selects a permitted interpretation with
suitability true, regularity false, and the claimed measure-zero predicate
false. A trust-zero Lean replay checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with `[propext, Classical.choice, Quot.sound]`. A proof uniform in the semantic
interface would therefore contradict a kernel-checked countermodel. This
diagnoses the current formal interface; it neither proves nor refutes the
mathematical Caffarelli-Kohn-Nirenberg theorem. Choosing favorable semantics,
assuming the per-solution conclusion, or replacing parabolic with Euclidean
Hausdorff measure would substitute a different theorem and was not done.

The authoritative dependency `S56-M-1228-OBLIGATION_TREE` is also only
provisional `[_]`, not master-accepted `[x]`. `ObligationTree.root_compose`
merely consumes the complete analytic conclusion as `perSolution`. The frozen
root cut remains open with no positive terminal bodies:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

The pinned mathlib scan found no CKN partial-regularity, suitable weak
Navier-Stokes, parabolic-Hausdorff, or epsilon-regularity theorem to import.
The historical `S1_M_156` surface stores the essential analytic claims as
package fields; the immutable anchor audit likewise remains at `M4` with no
exact external terminal body.

All proof-relevant inputs are unchanged since the checked countermodel was
added at base `c45f3c70`. Two predecessor defects still fail closed:
`check_statement.py` reports the spatial-dimension mutation without elaborating
or comparing it, and all 15 node validation recipes compile only the
conditional `ObligationTree.lean` harness rather than the analytic nodes they
claim to cover.

There were already 33 JSON and 33 Markdown proof-recheck packets before this
run, but the authoritative DAG still says `attempts: 0` and `children: []`.
This exceeds the five-tick split threshold. The master must reconcile these
packets and split the statement repair and analytic work rather than schedule
another identical proof attempt.

The frozen vector remains `H1/M4/R4`; the item remains `[ ]`. No proof body,
closed obligation, receipt, audit completion, theorem completion, or master
acceptance is claimed.

## Validation

Commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink reused canonical pinned artifacts
read-only. No Lake update/build, dependency clone/fetch, checkout, network
action, or `.lake` mutation was performed. The trust-zero replay copied inputs
below `/tmp`, wrote its `.olean` there, and removed temporary output on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed; output SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required; output SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; output SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; output SHA-256 `915e7167391aba59f968d010a81196a2df89f22d6c290d5e1a9152260b623b05`. The mutation defect above remains. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts`; output SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | 15 obligations, 31 typed edges, denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; output SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Narrow `lake env lean --trust=0 -t0` replay | 0 | Statement, both countermodel theorems, and conditional composition elaborated; proof declarations report `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan of target Lean files | 1 | Expected no-match for `sorry`, `admit`, `axiom`, `sorryAx`, and `unsafe`. |
| Pinned mathlib subject scan | 1 | Expected no-match; no exact terminal candidate found. |
| `git diff --exit-code c45f3c70..HEAD -- <proof-relevant inputs>` | 0 | Statement, countermodel, composition, registry, graphs, anchor audit, and validation specs are unchanged. |
| Pin checks | 0 | mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular commit `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |

The replay used `lake env` only to resolve the pinned Lean executable and
`LEAN_PATH`, then compiled temporary copies with `--trust=0 -t0`. Stable output
SHA-256 values were `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
(statement), `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
(countermodel), and `c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
(composition); each stderr was empty. The temporary `Statement.olean` hash was
`9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`.

## Retry Condition

The master must reconcile the repeated attempts and repair or accept the
predecessor as appropriate. Reopen and version the statement around fixed,
source-faithful definitions of suitable weak Navier-Stokes solutions, regular
points, and one-dimensional parabolic Hausdorff measure; repair the mutation
and validation recipes; and freeze a corrected, split registry. Then implement
placeholder-free local bodies or immutably pin exact compatible bodies for all
four cut obligations with checked transports, composition, trust, and
terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
