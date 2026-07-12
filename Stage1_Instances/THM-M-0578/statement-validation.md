# Statement validation record

Item: `S56-M-0578-STATEMENT`  
Base revision: `65f25d08d2043f95837c8686cce016cee3fe3d0e`

## Frozen target

`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` asserts the existence of a smooth
seven-manifold homeomorphic to the unit sphere in `EuclideanSpace Real (Fin 8)` for which the type
of infinity-smooth diffeomorphisms to that sphere is empty. Its sole direct import is
`Mathlib.Geometry.Manifold.PoincareConjecture`.

The choice resolves the intake ambiguity using two concordant records: Milnor's cited 1956 result
is about manifolds homeomorphic to the 7-sphere, and the repository contains a second entry for the
same named theorem saying `七维怪球的存在` ("existence of a seven-dimensional exotic sphere").
Mathlib's identically shaped `exists_homeomorph_isEmpty_diffeomorph_sphere_seven` is declared
`proof_wanted`; it is statement discovery only, not proof evidence.

## Commands and results

Commands ran in this worker clone using the existing pinned Lake environment. No dependency update,
fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0578/Statement.lean` | 0 | canonical target, direct-shape iff, and four structural mutations elaborated; explicit canonical expression printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0578/check_statement.py` | 0 | expression SHA-256 `c9d29902fc3b1bd25c4a83aa5daaa4ce201798576d7b5e16e9bbc05e76a9d32c`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0578/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `676bf4...9a72`, `651c8a...1d2`, and `321626...5b2`, matching `statement.json` |

Changing the dimension, dropping homeomorphism, dropping the smooth-manifold structure, and
replacing `IsEmpty Diffeomorph` by `Nonempty Diffeomorph` all produce distinct elaborated
expressions. The statement remains unproved and theorem completion remains false. Master
acceptance and all dependent phases are outstanding.
