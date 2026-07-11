# Scope map

| Surface | Frozen intake scope | Open decision for statement phase |
|---|---|---|
| Base field | Nonarchimedean local field `K` | Include both mixed and equal characteristic, or restrict to finite extensions of `Q_p` |
| Extensions | Finite abelian `L/K`, considered up to `K`-isomorphism | Exact Lean structure and universe policy |
| Multiplicative group | Topological group `K^times` | Coercions and topology instance used by the canonical expression |
| Norm subgroup | Image `N_{L/K}(L^times)` in `K^times` | Confirm the field norm on units has the required topological API |
| Finite-level reciprocity | Surjection `K^times -> Gal(L/K)` with norm kernel | Arithmetic versus geometric Frobenius normalization |
| Classification | Finite abelian extensions correspond contravariantly to open finite-index subgroups | Equality versus isomorphism classes and tower functoriality |
| Boundary cases | Trivial extension corresponds to `K^times` | Mutation tests for omitted openness, finite index, and abelianness |
| Absolute form | Not part of the frozen root | May be a checked consequence only after inverse-limit topology is available |

The repository phrase “abelian extensions of local fields” is too short to choose a characteristic
scope or reciprocity convention. Those are explicit blockers, not licenses to substitute a more
convenient theorem. The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_076.lean`
is discovery evidence only under the uniform L0 rework rule.
