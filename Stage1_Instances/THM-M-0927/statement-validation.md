# THM-M-0927 statement validation

Item: `S56-M-0927-STATEMENT`

Base revision: `27400857bccc93638c97e9c65859ddf5d5b5f4da` (tree
`3762537e0e5ae46cd70b086da49a69e2fd7b275c`)

## Frozen target

`Stage1Instances.THM_M_0927.BinetFormulaTarget` states DLMF 26.11.7 exactly: for every
`n : Nat`, the real coercion of the zero-based `Nat.fib n` equals

```text
((1 + sqrt 5)^n - (1 - sqrt 5)^n) / (2^n * sqrt 5).
```

This is the sole formula-level authoritative lead preserved at intake. Selecting it resolves the
formal statement surface without upgrading the historical Binet/1843 attribution or source status
beyond H1. The checked iff declarations cover function equality and the equivalent local
characteristic-root spelling.

The canonical target uses exactly two direct definition imports:
`Mathlib.Data.Nat.Fib.Basic` and `Mathlib.Data.Real.Sqrt`. Removing either from a target-only
fixture makes elaboration fail. The proof-bearing `Mathlib.NumberTheory.Real.GoldenRatio` module is
not imported, invoked, or credited by this phase.

## Commands and results

All commands ran inside this worker clone. The automation-provided canonical `.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0927` | 0 | rank 1546, planned, no legacy slot, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0927/Statement.lean)` | 0 | exact target, two checked iff transports, four expected mutation type rejections, five boundary/mutation witnesses, axiom reports, and explicit expression elaborated |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC python3 -B ../../Stage1_Instances/THM-M-0927/check_statement.py --worker-packet ../../.stage1-worker-selftest.json)` | 0 | expression SHA-256 `0a05e8c4...5a2f`; source `72172fb6...d8d`; mutations, import deletion, records, receipt, packet, pins, and fingerprints agreed |
| `python3 -m json.tool` over the statement record, receipt, instance, task DAG, and worker packet | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0927-pycache python3 -m py_compile Stage1_Instances/THM-M-0927/check_statement.py` | 0 | validator compiled without generated files under the owned path |
| scoped prohibited-construct scan over `Statement.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom/bodyless/opaque/unsafe declaration, TODO, FIXME, or placeholder marker |
| `git diff --check -- Stage1_Instances/THM-M-0927 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The historical intake checker is stale after scheduler integration and statement reconciliation: it
expects the old `[ ]` intake projection, old authority hashes, null target, and intake-only file
inventory. It is preserved as historical code and currently exits nonzero. Current statement replay
authority is `check_statement.py` plus `statement-receipt.json`; the immutable intake receipt remains
unaccepted historical evidence.

## Mutation and boundary policy

The canonical target has no antecedent to remove. The removed-contract mutation therefore deletes
the conjugate-root contribution; `removed_conjugate_mutation_is_false` kernel-refutes it at zero.
The domain mutation restricts the index to `Fin 10`, the
binder-scope mutation replaces `forall n` by `exists n`, and the boundary mutation adds `1 <= n`.
Each receives an expected exact-type rejection and has a distinct explicit expression.

The zero- and one-index radical equations kernel-check, `sqrt_five_ne_zero` checks the denominator,
and the finite-domain witness shows that index ten remains in the canonical scope. Checked
transports and arithmetic boundaries report only `propext`, `Classical.choice`, and `Quot.sound` or
no axioms. These are statement-level observations, not proof-body or transitive trust closure.

## Status boundary

This is provisional statement evidence pending dependency-ordered master acceptance. Historical
source fidelity and H0 review, formal-anchor and terminal-body provenance audit, obligation freeze,
proof, composition, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, release, audit completion, and theorem completion remain open.
