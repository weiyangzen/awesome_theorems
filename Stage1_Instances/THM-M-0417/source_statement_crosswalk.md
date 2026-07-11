# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Centrally symmetric convex body contains a nonzero lattice point above the `2^n` covolume threshold | H. Minkowski, *Geometrie der Zahlen*, Teubner, Leipzig, 1896 | `MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure` | Foundational primary monograph identified, but edition-specific theorem/page, premise mapping, and errata review are not yet accepted: `H1` |
| Strict volume inequality | Classical open-threshold form of the convex body theorem | hypothesis `mu F * 2 ^ finrank R E < mu s` | Candidate correspondence; exact coercions and measure assumptions require elaboration |
| Central symmetry and convexity | Body is convex and symmetric about the origin | `forall x in s, -x in s` and `Convex R s` | Direct candidate encoding; measurability/regularity consequences must be checked |
| Lattice covolume | Volume of a fundamental parallelepiped/domain | `IsAddFundamentalDomain L F mu` and `mu F` | Object-model crosswalk is not yet a checked equivalence to a full-rank lattice formulation |
| Closed boundary equality form | Standard compact-body extension at equality | `MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_le_measure` | Separate candidate with compactness, discrete topology, and nontriviality hypotheses; not silently substituted for the root |

The repository's legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_072.lean` supplies useful declaration names and a
candidate wrapper, but rev-5.6 treats it only as discovery evidence. The statement phase must inspect
the actual pinned declaration type, serialize its normalized expression, check any lattice/covolume
transport, and mutation-test dimension, symmetry, convexity, inequality, and boundary hypotheses.

No `H0` claim is made. Source audit still requires an immutable scan or edition hash, exact
theorem/page location, assumption-by-assumption mapping, corrections/errata search, and independent
review. The number-field "Minkowski bound" declarations in the legacy file are downstream results
and are outside this convex-body root unless a later graph records an explicit bridge.
