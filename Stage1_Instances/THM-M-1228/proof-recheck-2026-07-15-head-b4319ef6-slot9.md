# THM-M-1228 proof-phase recheck at `b4319ef6` (slot 9)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `b4319ef6d039de12cec559f173287d541c238d70`

Base tree: `0b0762ebd01405d33218c3bcbcb24d4544b0fad0`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the frozen target.
The canonical declaration is the family

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
per-solution conclusion, or replacing parabolic measure with ambient
Hausdorff measure would substitute a different theorem and was not done.

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
terminal CKN theorem. The historical `S1_M_156` surface stores the essential
analytic conclusions in package fields and provides no proof provenance. The
immutable anchor audit likewise remains at `M4` with no exact positive body.

There were already 35 JSON and 35 Markdown proof-recheck packets before this
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
`.lake` mutation was performed. The trust-zero replay compiled copies in a
temporary directory under this worker root and removed all temporary output.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed; stdout SHA-256 `5f0a7ade2c83d37f8fffdf1c9851d7e52cd47e4240bcbcba2ef2457e89606aaf`. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required; stdout SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete; stdout SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; stdout SHA-256 `915e7167391aba59f968d010a81196a2df89f22d6c290d5e1a9152260b623b05`. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree; stdout SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | 15 obligations, 31 typed edges, denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root remains open at M4; stdout SHA-256 `13bbb5f7f7cfcb0cd9eacb53b0fcf6a5d81cd90620bf01bf68d08e029a3e035b`. |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Scoped `lake env` resolution followed by `lean --trust=0 -t0` on temporary copies of `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` | 0 | The statement, both countermodel theorems, and conditional composition elaborated; proof declarations reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration token. |
| `git diff --exit-code c45f3c70..HEAD -- <proof-relevant inputs>` | 0 | Statement, countermodel, composition, registry, graphs, anchor audit, and validation specs are unchanged. |

The replay stdout SHA-256 values were
`e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
(statement),
`392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
(countermodel), and
`c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
(composition); every stderr stream was empty. The run-local `Statement.olean`
SHA-256 was
`b1c2031bd29b9df24795f0ee1731bba29d44477d7ef7f19685ffdafa96bdda66`;
this warm artifact hash is not deterministic release evidence. The Lean
executable SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
Pinned mathlib revision/tree were
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; pinned `flt-regular` was
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`.

The successful replay core was:

```bash
TMP=.thm-m-1228-b4319ef6-slot9-hash
mkdir "$TMP"
cp Stage1_Instances/THM-M-1228/{Statement.lean,ProofBlocker.lean,ObligationTree.lean} "$TMP"/
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_PATH="$LP" "$LEAN" --trust=0 -t0 -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$PWD/$TMP:$LP" "$LEAN" --trust=0 -t0 "$TMP/ProofBlocker.lean"
LEAN_PATH="$LP" "$LEAN" --trust=0 -t0 "$TMP/ObligationTree.lean"
rm -rf "$TMP"
```

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
