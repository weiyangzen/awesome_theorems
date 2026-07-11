# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Global-Lipschitz SDE theorem | B. Oksendal, *Stochastic Differential Equations: An Introduction with Applications*, 6th ed., Springer (2003), Chapter 5, section 5.2 | explicit coefficient predicates over finite-dimensional real spaces | Bibliographic anchor located; exact theorem number, wording, and assumptions require primary-copy verification |
| Existence of a strong solution | same candidate source section | a witness process with adaptedness, integrability, and the integral equation | Exact filtration, initial-variable, and stochastic-integral conventions remain open |
| Uniqueness | same candidate source section | equality up to indistinguishability of any two solutions with the same initial variable and Brownian driver | Must not be replaced by uniqueness in law or pointwise equality at each fixed time |
| Historical Lean boundary | repository `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_229.lean` | abstract structures culminating in `ExistsUniqueStrongSolution` | Discovery only: abstract hypothesis fields and an assumed integral interface do not establish the classical analytic theorem |

The repository description is only `SDE的解的存在唯一性` (existence and
uniqueness of solutions of SDEs). It does not select a theorem among global
Lipschitz, local Lipschitz with non-explosion, one-dimensional specialized, weak,
or martingale-problem variants. This intake therefore records the standard
global-Lipschitz formulation as a candidate rather than pretending it is frozen.

The statement phase must verify a primary copy and pinpoint the theorem, edition,
assumptions, and errata; choose state/noise dimensions and time domain; distinguish
strong existence, pathwise uniqueness, and uniqueness in law; and serialize and
mutation-test the normalized Lean expression. The adjacent manifest items for
strong/weak solutions and Yamada-Watanabe must not be folded into this target.

Discovery link (not an immutable evidence receipt): Oksendal book DOI
<https://doi.org/10.1007/978-3-642-14394-6>.

No `H0` or exact-statement claim is made. Edition-file hashes, pinpoint pages,
assumption mapping, errata search, and independent review remain open.
