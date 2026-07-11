# Source-statement crosswalk

| Claim component | Source/discovery anchor | Candidate formal component | Intake assessment |
|---|---|---|---|
| "Different domains" | Stage0 says only `不同区域特征值的比较` and attributes the result generically to many mathematicians | nested domains `Omega1 subset Omega2` | Candidate interpretation, not source-verified |
| Eigenvalues | Stage0 does not identify an operator or boundary condition | ordered variational eigenvalues of the Dirichlet Laplacian | Dirichlet is essential: no analogous unrestricted Neumann domain-monotonicity claim is adopted |
| Direction | The Rayleigh-Ritz/min-max argument enlarges the trial space when the Dirichlet domain is enlarged | `lambda k Omega2 <= lambda k Omega1` | Mathematical orientation fixed provisionally |
| Multiplicity/index | Standard min-max ordering counts multiplicity | positive index `k` | Lean natural-number offset remains open |
| Domain assumptions | Discreteness normally follows from the bounded-domain Sobolev setup | bounded open Euclidean domains with conditions sufficient for compact embedding | Exact weakest assumptions are intentionally not asserted |

## Discovery bibliography

- R. Courant and D. Hilbert, *Methods of Mathematical Physics*, Volume I, Wiley-Interscience,
  1953 English edition, Chapter VI (variational methods and eigenvalue problems). This is a
  classical primary mathematical source family, but the exact section/page supporting the adopted
  domain statement has not yet been checked against an immutable scan.
- E. B. Davies, *Spectral Theory and Differential Operators*, Cambridge University Press, 1995,
  Chapter 4 (variational eigenvalue methods). This is a secondary discovery source, not H0 evidence.

No primary-source theorem/page/assumption/errata receipt is claimed. Before the statement phase can
freeze an exact root, review must either (a) locate a primary pinpoint that matches the adopted
Dirichlet domain-monotonicity claim, including regularity and indexing, or (b) reject this reading
and return the target for metadata disambiguation. A search for a Lean declaration also belongs to
the later anchor-audit phase and receives no credit here.
