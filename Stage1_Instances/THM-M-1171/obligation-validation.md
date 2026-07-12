# THM-M-1171 obligation-tree validation

Item: `S56-M-1171-OBLIGATION_TREE`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes 18 canonical obligations: 16 semantic machine obligations and two
informational source/provenance overlays. The Fourier-multiplier route explicitly separates
test-function normalization, Fourier derivative identities, the homogeneous multiplier,
strong `L^p` boundedness, zero-frequency handling, component estimates, Frechet-derivative and
trace transports, finite-dimensional operator-norm assembly, and root composition. Every leaf has
an explicit four-step semantic ledger, below the 100-step split threshold.

The validator recomputed denominator SHA-256
`b3c709ee6627b5d79f2dfe5d79cc0a7b828cd418b85f1dd9312cc6350fe1fc10`, checked the
one-to-one registry/node mapping, all seven graph types and reciprocal edge indexes, root
reachability, uniqueness, leaf budgets, and the fail-closed closure record. There are 59 typed
edges. The root remains open at `M4`; all proof-body fields are null.

Lean reused the existing pinned artifacts. No dependency update, fetch, clone, build, or `.lake`
mutation was performed.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1171/build_obligation_artifacts.py` | 0 | generated 18 obligations; denominator digest `b3c709ee...1fc10` |
| `python3 Stage1_Instances/THM-M-1171/check_obligation_tree.py` | 0 | `PASS THM-M-1171 obligation tree: 18 obligations, 59 typed edges`; root open M4 |
| `python3 -m json.tool Stage1_Instances/THM-M-1171/obligation-registry.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1171/typed-graphs.json >/dev/null` | 0 | valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1171/Statement.lean)` | 0 | exact target and checked definitional transport re-elaborated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1171` | 0 | rank 372, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1171 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Validated content hashes:

```text
f242b01b394a8204269f8bb11a146040b2c4ce12b35dd719c2e5e934637556b0  obligation-registry.json
ced3a88d0ae8aefefa4c12e43ad68475de9c6c16a04ed7ac0dc851433ccab24b  typed-graphs.json
```

## Status boundary

This self-test establishes only the architecture freeze. A planned formal target is not an
elaborated declaration, and a semantic ledger is not proof closure. The critical open cut is
`M1171-L-MIHLIN`, `M1171-L-FOURIER-DERIV`, and `M1171-L-LP-ASSEMBLY`. No proof body, composition
certificate, H0/R0 review, audit completion, release evidence, or theorem completion is claimed.
Master acceptance remains required.
