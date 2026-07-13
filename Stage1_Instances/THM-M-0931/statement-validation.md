# THM-M-0931 statement validation

Item: `S56-M-0931-STATEMENT`. Base revision:
`1168265f6eea33d947ff470fad2ca6fff9e1130b`; base tree:
`0d35608cbc6e281a3d9935d452cf33c88c32aa7e`.

## Frozen target

`Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget` states that for every positive `n`, a
multiset of exactly `2 * n - 1` integers contains a submultiset of exactly `n` occurrences whose
sum is divisible by `n`. `Multiset Int` retains repeated and negative inputs and makes selection
of occurrences explicit. The exact input cardinality follows the inspected 1961 theorem sentence;
the proof's indexed occurrences support the multiset reading of its historical set terminology.

The sole direct import is `Mathlib.Data.ZMod.Basic`. It supports both the integer-divisibility root
and the checked residue formulation while avoiding the proof-bearing
`Mathlib.Combinatorics.Additive.ErdosGinzburgZiv` module. Import deletion makes `Multiset` unknown.

## Commands and results

All commands ran in this worker clone on 2026-07-13 (Asia/Shanghai). Lean commands used the
existing pinned Lake environment read-only. No update, build, dependency clone/fetch, or `.lake`
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0 / rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0931` | 0 | rank 1470, planned, no legacy slot, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0931/Statement.lean` | 0 | target, two checked transports, four expected mutation identity failures, axiom reports, and explicit expression elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0931/check_statement.py` | 0 | expression SHA-256 `b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a`; source/output hashes, one deletion probe, four mutation fingerprints, authority item, task dependency, and pins agree |
| deletion probe without `Mathlib.Data.ZMod.Basic` | 1 expected | `Multiset` is unknown; the sole import is necessary |
| `python3 -m json.tool` over the statement metadata, provisional receipt, and worker packet | 0 | all structured artifacts are valid JSON |
| prohibited-construct scan over target-owned Lean files | 1 expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0931 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics |

## Transports and mutations

`atLeastCountTarget_implies_erdosGinzburgZivTarget` checks the equality-to-lower-bound
specialization from the proposition shape of pinned `Int.erdos_ginzburg_ziv_multiset`. It does not
import that declaration or credit its proof. `erdosGinzburgZivTarget_iff_residueTarget` uses
`ZMod.intCast_zmod_eq_zero_iff_dvd` while retaining the same integer multisets and binders.

The validator serializes the root and each mutation under explicit/universe options and requires
distinct SHA-256 fingerprints. Lean also rejects definitional identity after removing positivity,
changing integer inputs to naturals, changing the universally bound modulus to an existential one,
or broadening exact input cardinality to an at-least bound. This tests statement identity, not
logical independence of the variants.

## Status boundary

This is statement-only worker evidence pending dependency-ordered master acceptance. The intake
receipt itself remains provisional `[_]`; therefore this downstream proposal cannot be accepted
first. The intake checker binds its historical snapshot and is not reused as statement evidence.
Independent source review, anchor audit, obligation registry, proof, composition, trust
closure, readable reconstruction, hermetic validation, release, audit completion, and theorem
completion remain open.
