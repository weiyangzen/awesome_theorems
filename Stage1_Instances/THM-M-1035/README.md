# THM-M-1035 rev-5.6 intake

This is the `planned` dossier for the repository claim "Stratonovich integral", described only as
"another definition of stochastic integral". That wording names a construction, not a unique
theorem. Intake therefore freezes the ambiguity rather than silently selecting an existence,
conversion, or chain-rule theorem.

## Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Objects | probability space; real stochastic integrand and integrator; time partitions | filtrations, regularity, and process classes are unspecified |
| Construction | symmetric/midpoint sums and their limit | partition model and convergence mode are unspecified |
| Existence | convergence under suitable semimartingale/integrability assumptions | no exact assumptions are sourced |
| Conversion | relation to the Ito integral and quadratic covariation | possible theorem, not implied uniquely by the source wording |
| Calculus | Stratonovich chain rule | possible consequence, not the frozen root |
| Lean | legacy `S1_M_228.StatementShape` and finite-sum skeleton | discovery input only; abstract `Prop` fields do not formalize the construction |

The next statement phase must first obtain or select an authoritative exact claim, then freeze
ordered binders, hypotheses, convergence, equality conventions, and degenerate cases. It must not
credit the legacy data package as closure.

## Intake verdict

Lifecycle is `planned`; root vector is `[H3, M3, R3]`. The source-identification/exact-statement
gate is the first open gate. No theorem completion, Lean elaboration, or historical proof credit is
claimed.
