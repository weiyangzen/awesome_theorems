# Source-statement crosswalk

Statement-phase status: blocked. The repository source record supplies only "duality for subspaces
in a sphere". The intake's compact, locally contractible, singular-theory variant is a conservative
scope choice, not an immutable source pinpoint that fixes one proposition. The mappings below are
discovery inputs and receive no canonical statement, transport, proof, or acceptance credit.

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Sphere-subspace duality | J. W. Alexander, *A proof and extension of the Jordan-Brouwer separation theorem*, Transactions AMS 23 (1922), pp. 333-349 | no terminal declaration identified | Historical primary-source discovery anchor; theorem numbering, hypotheses, coefficient conventions, and errata remain unaudited, so no `H0` claim |
| Modern compact locally contractible formulation | E. H. Spanier, *Algebraic Topology* (McGraw-Hill, 1966), Chapter 6, duality section | future canonical expression | Secondary formulation anchor only; exact edition/page/theorem crosswalk must be checked before source acceptance |
| Complement object | Same duality statement, `S^n \ A` | `Stage1Instances.THM_M_0548.SphereSubsetComplement` | Target-owned boundary object elaborates; it is substrate only, not the duality theorem |
| Complement reduced homology | Degree `n-i-1` side of the theorem | singular homology APIs imported by legacy `S1_M_120.lean` | Candidate API only; the legacy declaration uses unreduced homology and therefore is not an exact root |
| Subspace reduced cohomology | Degree `i` side of the theorem | none located at intake | Required semantic component is absent from the legacy shape, which accepts an arbitrary supplied object |
| Duality and naturality | Isomorphism, with admissible-map compatibility in the natural version | legacy `AlexanderDualityData.dualityIso` | Merely a structure field supplied by a caller, not a constructed theorem or naturality certificate |

The repository source record says only "a duality for subspaces in a sphere" and labels it verified.
That wording does not choose between the arbitrary compact/Cech theorem and the locally
contractible/singular theorem, nor does it fix coefficients or grading. This intake conservatively
freezes the locally contractible singular version and records the other formulation as excluded
until checked transport is available.

Discovery links, not immutable evidence receipts:

- Alexander bibliographic record: <https://doi.org/10.1090/S0002-9947-1922-1501205-Alexander>
- Legacy Lean discovery artifact: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_120.lean`

The unresolved premise mapping includes the coefficient system, compact versus closed versus
arbitrary compact domain, local contractibility, grading category, reduced-theory definitions,
naturality scope, and all degenerate cases. These choices materially change the proposition. The
legacy structure's caller-supplied cohomology object and isomorphism cannot resolve any of them.
The statement validator therefore reports `phase_accepted=false` and transfers no legacy credit.

Required follow-up is a scan-backed primary-source pinpoint, correction/errata search, exact
coefficient and reduced-grading comparison, actual Lean declaration inspection, and independent
review. No source fidelity beyond `H1` and no machine closure are claimed.
