# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Harnack control for nonnegative solutions of uniformly elliptic nondivergence equations with measurable coefficients | N. V. Krylov and M. V. Safonov, "A certain property of solutions of parabolic equations with measurable coefficients," *Izvestiya Akademii Nauk SSSR. Seriya Matematicheskaya* 44 (1980), 161-175; English translation, *Mathematics of the USSR-Izvestiya* 16 (1981), 151-164 | No declaration identified or credited | Primary theorem-family source located, but the paper is parabolic and cannot by itself silently fix the elliptic root |
| Standard elliptic interior formulation | D. Gilbarg and N. S. Trudinger, *Elliptic Partial Differential Equations of Second Order*, 2nd ed., Springer, 1983, Chapter 9 (strong solutions and Harnack inequality) | Future explicit Lean proposition over a ball | Secondary formulation anchor only; exact theorem number/page, printing, coefficient conventions, and errata require audit |
| Uniform ellipticity | Eigenvalue/quadratic-form bounds `lambda |xi|^2 <= xi^T A(x) xi <= Lambda |xi|^2` almost everywhere | Candidate predicate on a measurable self-adjoint operator field | Matrix/operator representation and symmetry convention are unresolved |
| Solution semantics | Strong `W^{2,n}` solution is the conservative provisional choice suggested by the monograph context | Candidate Sobolev/a.e. equation encoding | Classical, viscosity, and strong formulations are not interchangeable without checked bridges |
| Interior estimate | After normalizing geometry, `sup_(B_1/2) u <= C inf_(B_1/2) u` | Candidate `sSup`/`sInf` or extrema statement | Constant dependencies, representative regularity, and pointwise versus essential bounds remain open |

The target name alone is underdetermined: "Krylov-Safonov Harnack inequality"
can denote elliptic or parabolic results and can be stated for strong, viscosity,
or other generalized solutions. This dossier deliberately chooses an elliptic,
nondivergence, leading-coefficient-only scope consistent with the manifest's
elliptic neighborhood, but records that choice as provisional until the
statement phase completes a pinpoint source audit and Lean elaboration.

Discovery links (not immutable evidence receipts):

- Krylov-Safonov article DOI: <https://doi.org/10.1070/IM1981v016n01ABEH001283>
- Gilbarg-Trudinger, Springer DOI: <https://doi.org/10.1007/978-3-642-61798-0>

No `H0` or machine-closure claim is made. Required follow-up: acquire a fixed
edition/scan, record exact theorem/page and assumptions, check corrections and
errata, decide the solution class, map each premise to the Lean binders, and
obtain independent review.

