# Statement validation record

Item: `S56-M-0418-STATEMENT`  
Base revision: `7fe8e74dc1d7b1678d428039fd13be71de273dd8`

## Frozen target

`Stage1Instances.THM_M_0418.MinkowskiIdealClassBound` is the representative-form claim selected
at intake. It quantifies over an arbitrary universe-polymorphic number field and every class in the
class group of its ring of integers. Its witness is a nonzero integral ideal, its orientation is
`ClassGroup.mk0 I = C`, and its norm has a weak upper bound by the explicit real Minkowski constant.

The only direct import is `Mathlib.NumberTheory.NumberField.ClassNumber`. The local
`PinnedMathlibSourceShape` is the literal proposition exposed by
`NumberField.exists_ideal_in_class_of_norm_le` at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the kernel-checked transport is definitional. This
statement node does not invoke or credit that theorem's proof.

## Commands and results

Commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned Lake environment; no dependency update or download was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0418/Statement.lean` | 0 | canonical target, literal-source transport, four mutation fixtures, and pinned declaration elaborated; explicit target printed (one expected unused-variable linter warning in a mutation) |
| `python3 ../../Stage1_Instances/THM-M-0418/check_statement.py` | 0 | expression SHA-256 `d47f228d8edd29ddabc2cc6189f476d231e1a49870e134db0b83095cd3db1081`; all four mutations distinguished; toolchain and mathlib pin matched |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0418/Statement.lean lean-toolchain lake-manifest.json` | 0 | statement `84b8b5...aabc`, toolchain `651c8a...b1d2`, manifest `321626...b2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0418` | 0 | rank 73, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and distinguishes inversion of the represented
class, replacement of `<=` by `<`, loss of the nonzero representative/class equation, and deletion
of the degree and complex-place factors. Degree-one and totally real fields are deliberately not
excluded. The nonzero witness is encoded by `(Ideal (RingOfIntegers K))^0`, and the weak endpoint is
retained exactly.

This is statement-only evidence pending master acceptance. It does not establish source fidelity,
proof closure, provenance, trust closure, or theorem completion.
