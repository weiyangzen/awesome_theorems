# Statement validation record

Item: `S56-M-0468-STATEMENT`  
Base revision: `eb5c892a92c1c04b8fef2fcfa1216419112ad294`

## Frozen target

`Stage1Instances.THM_M_0468.BogomolovTarget` formalizes the exact
Ullmo--Zhang claim selected by intake. It quantifies over typed semantic data
for an abelian variety over a number field, an ample symmetric line bundle and
its canonical height, and a closed geometrically integral subvariety. For every
positive real threshold, its `<=` small-height locus must be Zariski dense
exactly when the subvariety is a torsion translate of an abelian subvariety.

Pinned mathlib does not expose the necessary abelian-variety, Neron--Tate
height, or subvariety foundations. `BogomolovData` makes those notions explicit
as typed operations and predicates without inserting the theorem as a field.
The direct import `Mathlib.Data.Real.Basic` is the smallest tested pinned import
needed for the real-valued height threshold.

## Commands and results

Commands ran inside this worker clone on 2026-07-12. Lean commands ran from
`Formalizations/Lean` using the existing pinned `.lake` environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0468/Statement.lean` | 0 | target, exact-type fixture, and four mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0468/check_statement.py` | 0 | expression SHA-256 `def6574c...fa0e`; all four mutations distinguished; mathlib revision `8a178386...a95` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0468/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `84151eb9...bc8c`, `651c8acc...1d2`, and `321626c8...d81` |

This is statement-only evidence pending master acceptance. It supplies no
proof, source or anchor acceptance, obligation closure, or release evidence.
