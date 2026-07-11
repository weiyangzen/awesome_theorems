# Statement validation record

Item: `S56-M-0414-STATEMENT`  
Base revision: `4fe349b4364c7aee03dbe67f21b7a631e12042da`

## Frozen target

`Stage1Instances.THM_M_0414.IdealUniqueFactorizationTarget` quantifies over an arbitrary
commutative Dedekind domain. It states both the `UniqueFactorizationMonoid (Ideal R)` interface and
the explicit `finprod` factorization of each nonzero ideal by its height-one prime-power
components. Its sole direct import is `Mathlib.RingTheory.DedekindDomain.Factorization`.

The target includes the unit ideal as the empty-product boundary and excludes the zero ideal. This
resolves the intake prose's internal conflict between "proper" and its explicit demand to test the
unit ideal. Fractional ideals are not part of the root. `HistoricalCandidateShape` directly
transcribes the historical `S1_M_069.StatementShape`, with a checked definitional iff; no historical
proof credit is accepted here.

## Commands and results

All commands ran inside this worker clone on 2026-07-12. Lean commands ran from
`Formalizations/Lean` using the existing pinned Lake environment. No update, build, clone, fetch,
or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0414/Statement.lean` | 0 | canonical target, checked historical-shape identity, four mutations, and unit boundary elaborated; explicit expression printed |
| `python3 ../../Stage1_Instances/THM-M-0414/check_statement.py` | 0 | expression SHA-256 `de0c201f670ebcc5d4da370f9d5871c131e333652cff7a4dfb903d75e245b005`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0414/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `7fe066...486d`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0414` | 0 | rank 69, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects removal of ideal nonzeroness,
specialization of the arbitrary domain to `Int`, relocation of nonzeroness outside the ideal
binder, and exclusion of the unit ideal. `unitIdealBoundary` is a kernel-checked exercise of the
selected empty-product case. These checks establish statement distinction, not the truth or proof
closure of the mutated propositions.

This is statement-only evidence pending master acceptance. It does not advance the anchor-audit,
obligation-tree, proof, validation, or release nodes and does not claim theorem completion.
