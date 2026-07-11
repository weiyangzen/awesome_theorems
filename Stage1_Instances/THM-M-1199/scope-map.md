# Scope map

## Preserved source scope

- Subject: shock waves associated with conservation-law equations.
- Historical attribution: multiple mathematicians in the twentieth century.
- Mathematical setting: differential equations / partial differential equations.
- Claimed status: the repository metadata says `已验证`, an untrusted screening label.

This is all the scope supported by the repository record. In particular, the record does not say
whether it means existence, admissibility, propagation, uniqueness, stability, or a jump law.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze: scalar versus system; spatial
dimension; time and space domains; state and codomain; flux regularity and convexity or hyperbolicity;
weak/distributional solution definition; initial/boundary data and regularity; shock geometry;
entropy/admissibility condition; conclusion and quantifiers; local/global time range; uniqueness
class; and all degenerate or boundary cases. Units, universes, foundation, computation, and TCB
profiles must then be fixed for the canonical Lean expression.

## Explicit exclusions

- `THM-M-1200`'s Rankine-Hugoniot jump condition as a substitute for this broader label.
- A Burgers-equation example, Riemann problem, Lax shock, entropy inequality, or existence theorem
  selected merely because it is convenient to formalize.
- Numerical shock-capturing behavior or empirical fluid phenomena.
- The metadata label `已验证` as primary-source, statement, or kernel evidence.
- `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_142.lean`: that file is explicitly about
  `THM-M-1314` (the Penrose inequality), so its slot number supplies no evidence for this target.
