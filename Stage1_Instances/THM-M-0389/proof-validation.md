# THM-M-0389 proof-phase validation

- Item: `S56-M-0389-PROOF`
- Base revision: `8f566755a28459bda22aa05071d96cc391ef0db6`
- Proof declaration: `Stage1Instances.THM_M_0389.integerMarkovClassification`
- Exact target: `Stage1Instances.THM_M_0389.IntegerMarkovClassification`
- Result: the local proof body elaborates under the pinned Lean 4.29.0/mathlib environment.
- Kernel dependency report: `[propext, Classical.choice, Quot.sound]`; no `sorryAx`.

## Commands and results

Run from `Formalizations/Lean`:

```text
$ lake env lean -R ../../Stage1_Instances/THM-M-0389 ../../Stage1_Instances/THM-M-0389/Proof.lean
'Stage1Instances.THM_M_0389.integerMarkovClassification' depends on axioms: [propext, Classical.choice, Quot.sound]
exit 0
```

The proof is constructive at the theorem level apart from standard mathlib
classical/quotient foundations. It proves the zero-coordinate branch, sign
normalization through absolute values, ordered positive Vieta descent by a
strict additive-height measure, permutation transport, and exact root
composition. `Proof.lean` repeats the frozen statement vocabulary because the
owned dossier is outside the Lake source root; the declarations and root type
are textually identical to `Statement.lean` and remain in the same namespace.

This is proof-phase evidence only. Hermetic replay, source/readability review,
independent validation, and release acceptance belong to later nodes and are
not claimed here.
