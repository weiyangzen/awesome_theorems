# THM-M-0958 statement validation

Item: `S56-M-0958-STATEMENT`

Base revision: `c79ae75db8880483f10bba17c9bc9dd91a9febcf` (tree
`375fa18a4f8afa63bb51d8b05fb4c804f3bb1240`). Validation date: 2026-07-13
(`Asia/Shanghai`).

## Frozen target

`Stage1Instances.THM_M_0958.ElkinConstructionTarget` selects Michael Elkin's arXiv
`0801.4310v1`, equation (5), with the definitions immediately preceding it. The root expands the
source's `Omega` convention into a positive universal real constant `c`, a positive natural
threshold `N`, and every `n >= N`. Its conclusion is the exact one-based extremal lower bound

```text
c * ((n / 2^(2 * sqrt(2) * sqrt(log_2 n))) * (log_2 n)^(1/4))
  <= nu(n).
```

The Lean root represents `nu(n)` by `addRothNumber (Finset.Ico 1 (n + 1))`, coerced to `Real`.
Every logarithm is `Real.logb 2`; the fourth-root exponent is explicitly `Real`. A checked iff
expands the attained extremum into a source-interval `Finset` witness whose distinct-triple
predicate is itself checked equivalent to `ThreeAPFree`. A second checked iff translates the
one-based interval to mathlib's zero-based `rothNumberNat n`.

The root is asymptotic, as the paper's definition requires. It does not silently strengthen the
claim to every positive `n`. `n = 0` and `n = 1` totalized expression and interval behavior are
kernel-checked separately, and the threshold itself remains included by `N <= n`.

## Lean boundary

The deletion-minimal direct imports are:

- `Mathlib.Combinatorics.Additive.AP.Three.Defs`
- `Mathlib.Analysis.SpecialFunctions.Log.Base`

Deleting either import makes the exact statement fixture fail. The proof-bearing and broader
`Mathlib.Combinatorics.Additive.AP.Three.Behrend` module is not imported. The fully explicit root
expression has SHA-256 `bc0d841038cdbcd4960581583c4ddfb7004d7ad38cf6432ab4803e9908f8f59c`;
the statement bundle has SHA-256
`0e90ce5bcd0b934e585b550f8f9c465fd4c7d1ca2f01011f40d2c52e60e9a402`.

Four elaborated mutations remove positivity of the universal constant, change the index domain to
integers, move the constant inside the index binder, or omit the interval's inclusive upper
endpoint. Lean rejects definitional equality with each mutation, and the checker confirms four
distinct explicit expression fingerprints. These are identity tests, not assertions that every
changed proposition is false.

The checked predicate, interval, extremal-witness, and boundary witnesses report only `propext`,
`Classical.choice`, and `Quot.sound`. No `sorry`, `admit`, `sorryAx`, custom axiom, bodyless
declaration, `opaque`, or `unsafe` escape is present.

## Commands and results

Commands run inside this isolated worker clone. The automation-provided canonical `.lake` symlink
was used read-only. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0958` | 0 | rank 1492, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `python3 scripts/stage1_execution_cron.py --validate-only` | 0 | 10,822 execution items across 1,546 targets; DAG, state, budgets, and todo validated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0958/Statement.lean` | 0 | exact root, transports, mutations, boundaries, axiom reports, and explicit expression elaborated |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0958/check_statement.py` | 0 | expression, source, bundle, mutation, import-deletion, and pin checks passed |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package stayed clean |

The final receipt records structured artifact, worker packet, prohibited-construct, source-pin,
and whitespace checks. This warm shared-cache result is nonrelease worker evidence, not a hermetic
or independent-runner attestation.

## Source and status boundary

The official SODA and journal metadata and abstracts preserve the headline formula, but their full
bodies were not compared. The journal is substantially longer and advertises added
discrete-geometry content, so whole-edition identity is not claimed. Complete edition comparison,
lawful durable admission, correction and errata review, source-to-obligation mapping, and
independent review remain H1 debt.

This phase freezes and elaborates the exact statement only. The intake and statement receipts
remain provisional pending dependency-ordered master acceptance. Anchor and terminal proof-body
audit, obligation freeze, proof, composition, readable reconstruction, hermetic replay,
independent verification, release, audit completion, and theorem completion remain open.
