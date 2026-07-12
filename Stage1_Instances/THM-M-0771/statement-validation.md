# Statement validation record

Item: `S56-M-0771-STATEMENT`  
Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`

## Frozen target

`Stage1Instances.THM_M_0771.WellOrderingTarget` quantifies over every `alpha : Type u` and asks
for a binary relation carrying `IsWellOrder alpha r`. In pinned mathlib, `IsWellOrder` combines
well-foundedness with trichotomy and supplies the strict-order laws. Thus the target means that
every carrier admits a strict well-order, without assuming an existing order or excluding the
empty carrier.

`wellOrderingTarget_iff_bundled` checks both directions between this canonical relation surface and
the bundled formulation `forall alpha, exists _ : LinearOrder alpha, WellFoundedLT alpha`. The sole
direct import is `Mathlib.Order.RelClasses`; in particular, the mathlib module containing the
well-order construction and `exists_wellOrder` is not imported. This keeps statement elaboration
separate from later anchor and proof credit.

## Commands and results

All commands ran inside this worker clone. Lean used the existing pinned `.lake` closure read-only;
no update, build, clone, fetch, or dependency mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0771/Statement.lean` | 0 | exact target, three checked transports, four structural mutation declarations, and empty/singleton boundary fixtures elaborated; explicit target printed; transport axioms were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0771/check_statement.py` | 0 | expression SHA-256 `adeed39bf6f748a2f9deb3f75399b41e073f2edb84be65dad243c1aae11dfecd`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0771/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `9f09f7d9...f86653`, `651c8acc...b1d2`, and `321626c8...2d81`, matching `statement.json` |

## Mutation and status boundary

The validator serializes the fully explicit target and distinguishes mutations that remove
well-foundedness, remove linearity, restrict the theorem to inhabited types, or replace the
arbitrary carrier by `Nat`. Kernel-checked fixtures confirm that empty and singleton carriers are
included. These checks establish statement identity and encoding transport, not truth of the root.

This node is self-tested pending master acceptance. Primary-source acceptance, anchor/proof-body
provenance, transitive trust closure, M0, audit completion, and theorem completion remain open.
