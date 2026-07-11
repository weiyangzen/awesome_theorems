# Scope map

| Surface | Intake scope | Boundary |
|---|---|---|
| Canonical root | Dense torsion in a closed subvariety of an abelian variety forces a finite union of torsion cosets | Human scope frozen; formal target open |
| Base | Algebraically closed field of characteristic zero | Positive characteristic is excluded; exact Lean typeclasses open |
| Ambient object | Abelian variety `A` | A general semiabelian variety is a later generalization, not silently included |
| Subobject | Zariski-closed subvariety `X` | Reduced/irreducible conventions and scheme-versus-variety encoding require statement audit |
| Torsion | Points killed by some positive integer multiplication map | Exact point and scalar-action API open |
| Density | Torsion intersection is Zariski dense in `X` | Closure/subspace formulation and empty-space behavior require checked transport |
| Conclusion | Finite union of translates `a + B`, with `a` torsion and `B` an abelian subvariety | Containment versus equality formulations require proof of equivalence |
| Curve formulation | A curve embedded in its Jacobian has only finitely many torsion points unless it is a torsion coset | Special case only; not substituted for the root |

Degenerate cases stay visible. The empty subvariety, a point, the whole abelian variety, reducible
`X`, the zero-dimensional abelian variety, and repeated or empty finite unions must be tested when
the Lean statement is selected. Intake assigns none of these proof credit or exclusion status.

The expected foundation surface includes algebraic geometry, group schemes or an equivalent
abelian-variety model, Zariski topology, finite unions, and torsion points. Availability in the
pinned Lean environment is deliberately not inferred from mathematical notation.

