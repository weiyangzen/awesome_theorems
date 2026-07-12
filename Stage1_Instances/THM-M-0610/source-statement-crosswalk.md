# Source-statement crosswalk

The authoritative repository phrase is `三维流形的不变量` (`an invariant of
three-dimensional manifolds`). It names neither the class of manifolds nor the
invariant's exact codomain and equivalence relation. Its `已验证` metadata is
explicitly untrusted under rev-5.6. The integral-homology-sphere formulation
below is a conservative intake interpretation anchored to the title and
described scope of Floer's original construction; it is not yet an H0
source-verified statement.

| ID | Claim component | Repository anchor | Primary-source discovery anchor | Intake assessment |
|---|---|---|---|---|
| `SRC-M0610-ROOT` | Instanton Floer homology gives a 3-manifold invariant | `Docs/researches/math_theorems.md`, entry `瞬子弗洛尔同调`; projected as `THM-M-0610` in `Docs/Stage0_Blueprint.md` | Andreas Floer, *An instanton-invariant for 3-manifolds*, Communications in Mathematical Physics 118 (1988), 215-240, DOI `10.1007/BF01218578` | Named primary construction source located; immutable capture, pinpoint theorem/page mapping, assumptions, corrections, and independent review remain open |
| `SRC-M0610-DOM` | The conservative historical domain is closed oriented integral homology 3-spheres | Repository says only "three-dimensional manifolds" | Floer's paper is the primary source to inspect for its exact homology-sphere and orientation hypotheses | Domain is a proposed narrowing needed to avoid a false universal claim; exact source clauses are not yet accepted |
| `SRC-M0610-DATA` | The construction uses SU(2) instanton/gauge-theoretic data and a relative grading | Not specified | Floer's 1988 construction is the discovery anchor | Bundle, reducible-connection, grading, and coefficient conventions need section-level crosswalk |
| `SRC-M0610-CPLX` | A differential defined using instanton trajectories yields a homology object | Not specified | Same primary paper | The analytic, transversality, compactness, orientation, and `d^2 = 0` boundaries have not been audited and receive no proof credit |
| `SRC-M0610-CHOICE` | The homology is independent of allowed auxiliary choices | Implicit in "invariant" | Same primary paper | Exact continuation result and whether the induced equivalence is canonical must be located and reviewed |
| `SRC-M0610-DIFF` | Orientation-preserving diffeomorphic inputs have equivalent instanton Floer homology | Implicit in "3-manifold invariant" | Same primary paper | The covariance, grading behavior, and orientation convention are open statement decisions |
| `SRC-M0610-MACHINE` | A public Lean 4 theorem closes this exact root | Metadata says only `已验证` without an artifact | None accepted at intake | No Lean module, declaration, proof body, immutable external pin, axiom report, or kernel receipt has been found or audited |

## Statement decisions passed forward

The statement phase must first resolve the repository phrase against the
primary source. It must then fix the manifold domain; smooth and orientation
structures; homology-sphere predicate; gauge group and bundle; treatment of
reducibles; coefficients and relative grading; auxiliary-choice parameters;
and the exact isomorphism, equivalence, or functoriality conclusion. The
well-definedness clause and diffeomorphism-invariance clause must both survive
in the formal target unless source audit establishes a different exact root.
Every alternate variant requires a checked directional transport.

This table is discovery evidence only. It does not claim that the cited paper
was inspected page by page in this clone, that no erratum exists, or that a
formal proof exists. The human axis remains `H1`, and the machine axis remains
`M4`.
