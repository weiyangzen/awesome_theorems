# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Suitable weak solutions of three-dimensional incompressible Navier-Stokes | L. Caffarelli, R. Kohn, and L. Nirenberg, *Partial regularity of suitable weak solutions of the Navier-Stokes equations*, Communications on Pure and Applied Mathematics 35 (1982), 771-831 | `CKNSourceSemantics.IsSuitableWeakSolution` over concrete three-dimensional `SolutionData` | Exact logical slot elaborated; concrete distributional, integrability, local-energy, page/theorem, and fidelity transport remain open |
| Local epsilon-regularity/decay mechanism | Same paper; detailed lemma-to-node mapping pending | legacy quantitative and compactness package declarations | Candidate architecture only; abstract proposition fields are not proofs |
| Parabolic singular-set conclusion | Same paper's partial-regularity result | legacy `CaffarelliKohnNirenbergPackage` and `StatementShape` | Candidate shape does not concretely encode/prove the terminal parabolic measure statement |
| One-dimensional parabolic Hausdorff measure zero | Same primary result, with the paper's parabolic geometry | `CKNSourceSemantics.ParabolicHausdorffOneMeasureZero` in the elaborated root | Logical conclusion is frozen; concrete parabolic construction and source transport remain open, and Euclidean `Measure.hausdorffMeasure` is excluded |
| Regularity away from the singular set | Same source, using its definition of regular point | `CKNSourceSemantics.RegularAt` and `SingularSet` | Domain-restricted complement is elaborated; the source definition and concrete transport require audit |

The repository metadata phrase "partial regularity of weak solutions" is too
short to serve as an exact statement. Intake resolves it to the classical CKN
theorem about **suitable** weak solutions in three spatial dimensions and keeps
the local hypotheses, regular-point definition, and parabolic Hausdorff
construction open rather than inventing them.

Primary discovery identifier (not an immutable evidence receipt):

- DOI: <https://doi.org/10.1002/cpa.3160350604>

No `H0` claim is made. The source audit must obtain a fixed edition, record exact
definition/theorem/pages and every assumption, check corrections or errata, map
each premise and conclusion to canonical Lean nodes, and receive independent
review. The existing `S1_M_156.lean` file is historical discovery input only.
