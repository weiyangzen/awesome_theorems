# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Interior regularity criterion for weak Navier-Stokes solutions | James Serrin, *On the interior regularity of weak solutions of the Navier-Stokes equations*, Archive for Rational Mechanics and Analysis 9 (1962), 187-195, DOI `10.1007/BF00253344` | legacy `AwesomeTheorems.Stage1.S1_M_157.StatementShape` | Primary paper identified, but theorem/page premise mapping, edition capture, and errata review are not accepted: `H1` |
| Mixed velocity integrability | Classical Prodi-Serrin hypothesis `u in L^q_t L^p_x` | `SerrinWeakSolutionInput.serrinMixedIntegrability : Prop` | Opaque field does not encode a mixed norm and cannot pass exact-statement equivalence |
| Scaling regime | In dimension three, `2/q + 3/p <= 1`, conventionally with `p > 3` in the classical non-endpoint form | `SerrinExponentCondition n p q` | Candidate generalizes dimension and uses finite real exponents; no checked transport to the primary statement |
| Weak-solution assumptions | Distributional equation, incompressibility, energy-class data, and domain conditions must match the selected source theorem | proposition fields of `SerrinWeakSolutionInput` | Names preserve intended slots but are not definitions or evidence that the PDE assumptions hold |
| Regularity conclusion | Interior regularity of velocity (and any pressure consequence explicitly supported by the selected formulation) | `Nonempty (SerrinRegularityConclusion X)` | Candidate package contains proof-carrying opaque propositions and `ContDiffOn`; source equivalence is unproved |

The title-level source establishes which historical result is intended, not an
`H0` crosswalk. The statement phase must inspect an immutable scan, record the
exact theorem and page wording, map every premise, decide endpoint and domain
conventions, and review corrections and later reformulations.

The repository's historical `S1_M_157.lean` is especially not a terminal
formalization: its weak equation, energy inequality, and mixed-integrability
conditions are proposition-valued fields supplied by the input. Its useful
role here is to expose missing object models and likely binders. No theorem
closure, checked alternate encoding, or external anchor credit is inherited.

Discovery link (not an immutable evidence receipt):

- Springer DOI landing page: <https://doi.org/10.1007/BF00253344>
