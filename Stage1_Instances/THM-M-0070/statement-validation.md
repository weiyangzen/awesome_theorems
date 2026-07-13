# Statement validation record

Item: `S56-M-0070-STATEMENT`
Base revision: `0d2c3bdcd192266bc255ac3d5186da604517145a`; base tree:
`eafbcb48efd51d9cda34f0fc1afe780434abad64`.

## Frozen target

`Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget` freezes the inspected primary root: for
every `G : Type u` with `[Group G] [Finite G]`, `Odd (Nat.card G)` implies `IsSolvable G`.
Finiteness remains explicit, the order is the carrier cardinality, and no nontriviality,
commutativity, simplicity, or fixed-order premise is added.

The two direct imports are `Mathlib.GroupTheory.Solvable` and
`Mathlib.SetTheory.Cardinal.Finite`. Deleting either one makes the complete module fail to
elaborate. `Mathlib.Algebra.Group.PUnit` is deliberately absent; the order-one boundary is checked
generically, so a convenience type does not broaden the canonical import surface.

Three `Iff` witnesses check the `Finite`/`Nat.card` to `Fintype`/`Fintype.card` transport,
factorization oddness to congruence modulo two, and `IsSolvable` to the explicit eventual-bottom
derived-series witness.

## Commands and results

All Lean commands ran from `Formalizations/Lean` with the existing pinned Lake environment. The
automation-provided `.lake` link and canonical dependencies were used read-only. No `lake update`,
`lake build`, clone, fetch, or dependency mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, contiguous ranks, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0070` | 0 | rank 1101; planned; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0070/Statement.lean` | 0 | exact target, three checked transports, four mutation rejections, two boundary implications, axiom reports, and explicit expression elaborated |
| `python3 -B ../../Stage1_Instances/THM-M-0070/check_statement.py` | 0 | fingerprints, both import deletion tests, mutations, witnesses, structured records, item identity, base, toolchain, and mathlib pins agreed |
| `python3 -B Stage1_Instances/THM-M-0070/check_intake.py` | 1 (known historical failure) | the inherited intake checker hardcodes the pre-integration intake task state and nine-file intake inventory; it is historical snapshot evidence and was not weakened by this statement phase |
| `python3 -m json.tool` on finalized owned JSON and worker packet | 0 | all structured artifacts are valid JSON |
| scoped prohibited-declaration scan over owned Lean | 1 (expected no match) | no prohibited declaration or placeholder token found |
| `git diff --check -- Stage1_Instances/THM-M-0070 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

## Mutation and boundary record

The mutation suite removes the oddness premise, narrows arbitrary groups to commutative groups,
moves oddness from an antecedent into the conclusion, and substitutes even for odd order. Lean
rejects each relevant false substitution, and the checker independently requires five distinct
fully explicit expressions.

The order-one implication applies the canonical target after rewriting the group cardinality to
one. The commutative-group implication specializes the unrestricted group binder. They confirm
included surfaces without proving or inhabiting the root target.

## Status boundary

This is provisional worker statement evidence pending master acceptance. The primary proof/source
audit, immutable formal anchor audit, obligation registry, proof, composition, readable
reconstruction, hermetic replay, independent validation, release, audit completion, and theorem
completion remain open.
