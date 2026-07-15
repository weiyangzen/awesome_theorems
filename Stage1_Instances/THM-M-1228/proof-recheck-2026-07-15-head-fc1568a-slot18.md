# THM-M-1228 proof-phase recheck at `fc1568a` (slot 18)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `fc1568a2997ca815b767b8cc172f3d4d339bf3b9`

Base tree: `635319193989301e577a430446e682952c51c538`

## Verdict

`blocked`. The positive proof deliverable cannot truthfully be completed from
the frozen target. Its exact declaration is the family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and the three predicates in `CKNSourceSemantics` have no laws connecting
suitability to regularity or parabolic measure. The tracked, placeholder-free
`ProofBlocker.lean` selects a permitted interpretation with suitability true,
regularity false, and the measure-zero predicate false. A trust-zero replay
checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with `[propext, Classical.choice, Quot.sound]`. Thus a proof uniform over the
frozen interface would contradict a kernel-checked countermodel. This
diagnoses the current formal encoding; it neither proves nor refutes the
mathematical Caffarelli-Kohn-Nirenberg theorem. Picking favorable semantics,
assuming the desired per-solution conclusion, or replacing the parabolic
measure by ambient Hausdorff measure would substitute a different theorem and
was not done.

The authoritative predecessor `S56-M-1228-OBLIGATION_TREE` is still only
provisional `[_]`, not master-accepted `[x]`. Its registry has no closed
obligations. `ObligationTree.root_compose` only consumes the complete analytic
per-solution result as a premise. The open root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

Pinned mathlib has adjacent distribution, smoothness, Lp, and ambient
Hausdorff APIs, but no suitable weak Navier-Stokes, parabolic-Hausdorff,
epsilon-regularity, or terminal CKN theorem. The historical `S1_M_156` file
stores the essential analytic conclusions in package fields. The immutable
anchor audit likewise supplies no exact positive terminal body.

There were already 34 JSON and 34 Markdown recheck packets at this base, while
the authoritative DAG still records `attempts: 0` and `children: []`. This is
well beyond the five-tick split threshold. The master must reconcile the
repeated packets and split statement repair from the four analytic cut
obligations rather than schedule the identical proof attempt again.

The vector remains `H1/M4/R4`; lifecycle remains `planned`; the item remains
`[ ]`. No positive proof body, closed obligation, accepted receipt, audit
completion, theorem completion, or master acceptance is claimed.

## Validation

Commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink reused the canonical pinned artifacts
read-only. No Lake update/build, dependency clone/fetch, network action, or
`.lake` mutation was performed. The trust-zero replay copied the three Lean
inputs to a temporary directory inside the worker root, compiled there, and
removed the directory on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed; output SHA-256 `73708731cbfd94064650789f0228bf38b3275391c05f0fb8cdb8ee55ff370e4b`. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required; output SHA-256 `9fa145ec708bbcaf0debf482565053b30bb5a2117b828ba306426c6c85c92eec`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; output SHA-256 `2715238bc66d8700932a347f6ca96eba1f2b3692c356e2b8b92bd82b517019ca`. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; the validator reports four killed mutations; output SHA-256 `0bc672d28f7864c29e9a32b03667837275aa2eb8c40e06c449899e2a8e68eaa8`. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree; output SHA-256 `ba020c4e8e152700dce44da7be2f08360c54c6f1818679ffdd937013f7c7ddd2`. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | 15 obligations, 31 typed edges, denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root remains open at M4; output SHA-256 `c6056d142306968fd9db211ee2082f94e0b38cd6f1f4583b31d1f8ccd25bdffa`. |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Scoped `lake env` resolution followed by `lean --trust=0 -t0` on temporary `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` | 0 | The statement, both countermodel theorems, and conditional composition elaborated; proof declarations reported only `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration token. |
| `git diff --exit-code c45f3c70..HEAD -- <proof-relevant inputs>` | 0 | Statement, blocker, composition, registry, graphs, anchor audit, and validation specs are unchanged. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The replay stdout SHA-256 values were
`e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
(statement),
`392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
(countermodel), and
`c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
(composition); all three stderr streams were empty. The Lean executable SHA-256
was `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The pinned mathlib revision/tree were
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

The exact successful replay core was:

```bash
TMP=$(mktemp -d .thm-m-1228-fc1568a-XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-1228/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-1228/ProofBlocker.lean "$TMP/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1228/ObligationTree.lean "$TMP/ObligationTree.lean"
LEAN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$LEAN_PATH" "$LEAN" --trust=0 -t0 \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$PWD/$TMP:$LEAN_PATH" "$LEAN" --trust=0 -t0 \
  "$TMP/ProofBlocker.lean"
LEAN_PATH="$LEAN_PATH" "$LEAN" --trust=0 -t0 \
  "$TMP/ObligationTree.lean"
```

An initial harness setup placed the copies directly under `/tmp`; Lean exited
1 because the input was outside the repository root, so `ProofBlocker.lean`
then could not import `Statement`. This was a harness-path error, not accepted
elaboration evidence. The in-root replay above corrected it and all three
commands exited 0.

## Retry Condition

Master-reconcile the repeated attempts and predecessor state. Reopen and
version the statement around fixed, source-faithful definitions of suitable
weak Navier-Stokes solutions, regular points, and one-dimensional parabolic
Hausdorff measure. Repair the statement-mutation and per-node validation
coverage, freeze a corrected split registry, and then implement locally or
immutably pin exact compatible bodies for the four cut obligations with
checked transports, composition, trust, and terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
