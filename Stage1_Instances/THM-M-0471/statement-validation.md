# Statement validation

Item: `S56-M-0471-STATEMENT`
Base revision: `902d9ce008e88a35a2307c85355560a230cc33c2`

## Frozen target

`Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget` freezes the conservative scope
selected at intake: for each `n : Nat` with `1 < n`, there is a nonempty list whose members are
prime and whose product is `n`, and every other prime list with product `n` is a permutation of it.
This preserves multiplicity and uniqueness up to order. It does not broaden the claim to zero, one,
or negative integers, and it does not substitute a sorted-list or prime-exponent statement.

The only direct import is `Mathlib.Data.Nat.Prime.Defs`. Its pinned public dependency closure
supplies `List.prod` and `List.Perm`; removing the import makes `Nat.Prime` unavailable. The
proof-bearing `Mathlib.Data.Nat.Factors` module is deliberately not imported. The direct expansion
transport elaborates and reports only `propext`. Four explicit mutations distinguish removal of
`1 < n`, a change to the integer domain, a moved existential binder, and exclusion of `n = 2`.
`two_boundary_in_domain` separately kernel-checks that the least intended input satisfies the
canonical antecedent.

## Commands and results

Commands use the automation-provided canonical `.lake` symlink read-only. No update, build, fetch,
clone, or dependency mutation is performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, contiguous ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0471` | 0 | rank 1353, planned, no accepted legacy artifacts, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0471/Statement.lean)` | 0 | exact target, checked expansion transport, four mutation propositions, `n = 2` boundary antecedent, axiom report, and explicit target elaborated |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0471/check_statement.py)` | 0 | expression, source, and Lean-output fingerprints agree; all four mutations differ; omitting the sole import fails |

The receipt records the final structured, Python, prohibited-construct, source-pin, artifact, and
whitespace checks. This warm shared-cache result is nonrelease worker evidence, not a hermetic or
independent-runner attestation.

## Status boundary

This phase freezes and elaborates the exact target only. Pinpoint primary-source fidelity,
candidate and terminal proof-body provenance, the obligation registry, proof and composition,
readable reconstruction, hermetic replay, deterministic bundling, independent verification,
release, and master acceptance remain open. No `H0`, accepted `M0`, `R0`, audit completion, or
theorem completion is claimed.
