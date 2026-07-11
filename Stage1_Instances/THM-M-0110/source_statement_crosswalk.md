# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Positive line bundle/canonical bundle cohomology vanishes in positive degree | K. Kodaira, "On a differential-geometric method in the theory of analytic stacks," *Proceedings of the National Academy of Sciences* 39 (1953), 1268-1273 | `AwesomeTheorems.Stage1.S1_M_034.StatementShape` | Primary historical discovery anchor; theorem/page premises and errata are not yet independently audited |
| Algebraic smooth-projective characteristic-zero form | R. Hartshorne, *Algebraic Geometry* (Springer GTM 52, 1977), Chapter III, Corollary 7.15 | same provisional target | Precise secondary reference for the selected algebraic scope; not a primary-source H0 receipt |
| Dual negative-line-bundle form | Hartshorne, Chapter III, Corollary 7.15, together with the surrounding Serre-duality development | no credited declaration | Equivalence requires a checked Lean transport and exact dimension/index conventions |
| Analytic versus algebraic formulations | Historical analytic formulation versus the selected algebraic formulation | none | A GAGA/comparison bridge is required; wording similarity is not proof of equivalence |

The repository metadata phrase "cohomology vanishing for a positive line bundle" omits the base
field, smoothness, projectivity/compactness, canonical-bundle twist, and degree range. It is
therefore insufficient as an exact statement. The algebraic formulation above is selected for the
statement phase because it matches the repository's Lean 4 scheme/sheaf lane, not because its
equivalence to every historical formulation has already been checked.

No `H0` or machine-proof claim is made. The source audit must obtain immutable scans or editions,
hash them, pinpoint hypotheses and conclusions, check corrections/errata and characteristic
assumptions, and obtain independent review.
