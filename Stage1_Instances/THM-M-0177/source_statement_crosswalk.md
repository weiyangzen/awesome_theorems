# Source-statement crosswalk

| Claim component | Human source anchor | Lean target candidate | Intake assessment |
|---|---|---|---|
| Proper pushforward and Todd-corrected Chern character commute | P. Berthelot, A. Grothendieck, L. Illusie, *Theorie des intersections et theoreme de Riemann-Roch*, SGA 6, Lecture Notes in Mathematics 225, Springer (1971), Expose III | A future theorem over schemes, K-theory, and rational Chow groups | Primary source volume and expose identified; exact theorem/page, assumptions, edition hash, and errata mapping remain open, so no `H0` claim |
| Smooth-source/target vector-bundle formula | W. Fulton, *Intersection Theory*, 2nd ed., Springer (1998), Chapter 15, especially the Grothendieck-Riemann-Roch discussion | `ch (f_! E) * td(T_Y) = f_* (ch(E) * td(T_X))` | Standard readable formulation; pinpoint proposition/theorem and convention audit remain open |
| K-theoretic pushforward | Alternating sum of higher direct images in the classical formula | Future `K0`/`G0` proper-pushforward construction | Must not be replaced by ordinary function pushforward; existence and well-definedness are open |
| Chow-theoretic pushforward | Proper pushforward on cycles modulo rational equivalence | Future rational Chow-group map | Rational coefficients, grading, and completion/truncation conventions must be frozen |
| Chern character and Todd correction | Characteristic classes associated to `E`, `T_X`, and `T_Y` | Future characteristic-class API | No repository-local or upstream Lean declaration is asserted at intake |

The source label `已验证` means only that the metadata classified the human theorem as established.
It is not evidence of a Lean 4 formalization. The statement phase must choose the precise classical
generality, inspect available pinned APIs, elaborate the exact target, and mutation-test properness,
smoothness, quasi-projectivity, rational coefficients, binder order, and identity-morphism behavior.

Discovery links, not immutable evidence receipts:

- SGA 6 bibliographic record: <https://link.springer.com/book/10.1007/BFb0066283>
- Fulton, *Intersection Theory*: <https://link.springer.com/book/10.1007/978-1-4612-1700-8>

Required later source work includes scans or immutable source hashes, exact theorem/page crosswalk,
notation and hypothesis comparison, corrections/errata search, and independent review.
