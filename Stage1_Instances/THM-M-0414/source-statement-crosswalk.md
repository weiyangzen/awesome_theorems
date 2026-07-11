# Source-statement crosswalk

## Source boundary

A standard primary-source candidate is Richard Dedekind's ideal theory as presented in a stable
edition of a modern algebraic-number-theory text. The repository currently supplies no edition,
theorem number, page, or source snapshot. The statement phase must choose and inspect such an
edition, record the exact theorem and definitions, and check errata. Until then this dossier is
`H2`, not `H0`; the citation class is deliberately a discovery direction rather than invented
bibliographic precision.

## Crosswalk

| Metadata/source component | Frozen mathematical meaning | Lean-side consequence | Intake disposition |
|---|---|---|---|
| "Dedekind domain" | domain satisfying the source's Dedekind hypotheses | reconcile with `[CommRing R] [IsDedekindDomain R]` and any nontriviality convention | included, exact encoding pending |
| "ideal" | nonzero integral ideal; the unit has empty factorization | binder `I : Ideal R` with `I != 0` | included and elaborated |
| "factorization" | finite product of nonzero prime ideals | choose explicit factors/exponents or checked `finprod` transport | included |
| "unique" | prime multiplicities agree; order irrelevant | state equality in a canonical finitely supported representation or prove equivalence to UFM | included |
| unit ideal | empty product | `unitIdealBoundary` | included and kernel checked |
| zero ideal | not covered by the classical claim | mutation test removal of `I != 0` | excluded |
| fractional ideals | integer-valued exponents | separate strengthening only | excluded from root |

## Lean discovery input

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_069.lean` imports
`Mathlib.RingTheory.DedekindDomain.Factorization` and points to
`Ideal.finprod_heightOneSpectrum_factorization` and the ideal unique-factorization instance. This
is credible candidate machinery, but intake does not accept its statement equivalence, proof body,
axiom profile, provenance, or dependency closure. Those belong to the statement and anchor-audit
nodes at the repository-pinned revisions.
