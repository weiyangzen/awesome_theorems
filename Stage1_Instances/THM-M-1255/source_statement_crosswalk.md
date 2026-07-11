# Source-statement crosswalk

| Claim component | Human source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Existence of a fundamental solution for every nonzero constant-coefficient operator | L. Ehrenpreis, *Solution of some problems of division. Part I. Division by a polynomial of derivation*, American Journal of Mathematics 76 (1954), 883-903 | `PolynomialStatementShape` | Primary paper identified bibliographically; theorem/page premise mapping and errata audit are not accepted, so status is `H1` |
| Independent existence route | B. Malgrange, *Existence et approximation des solutions des equations aux derivees partielles et des equations de convolution*, Annales de l'Institut Fourier 6 (1955-1956), 271-355 | future construction behind `FundamentalSolutionConstruction` | Primary paper identified; exact theorem numbering, hypotheses, and edition scan hash remain open |
| Operator encoded by a polynomial symbol | Constant coefficients identify `P(D)` with a polynomial in commuting partial derivatives | `MvPolynomial ι ℂ` plus `PolynomialDifferentialOperatorAction` | Candidate action is only an interface; commutation and the canonical algebra morphism are not constructed |
| Fundamental-solution equation | Distributional identity `P(D)E = δ` | `PolynomialFundamentalSolution` / `FundamentalSolution` | Equation shape is plausible, but Fourier/sign conventions and exact elaboration are deferred |
| Distribution class | Classical theorem asserts a distributional fundamental solution | legacy candidate concludes `TemperedDist ι` | This strengthening is not source-equivalent by assertion alone; it must be sourced and proved or the canonical target must use general distributions |
| Scalar field | Classical statements commonly cover real or complex constant coefficients | legacy candidate uses `MvPolynomial ι ℂ` on a real domain | Exact source scope and checked real/complex transport remain open |

Repository discovery wording appears at `Docs/researches/math_theorems.md:9178` and the historical
candidate implementation at `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_160.lean`. Neither is
accepted as a primary-source receipt or as rev-5.6 machine evidence.

No `H0` claim is made. The source audit must obtain immutable scans or edition hashes, pinpoint the
exact theorem statements and assumptions, check corrections and errata, map each premise to the
frozen Lean binders, and receive independent review. The statement phase must resolve the tempered
versus general distribution mismatch before any proof search can earn root credit.
