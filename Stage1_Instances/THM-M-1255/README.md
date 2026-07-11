# THM-M-1255 rev-5.6 intake

This is the `planned` rev-5.6 instance for the Malgrange-Ehrenpreis theorem. The exact normalized
Lean statement is now self-tested pending master acceptance. The historical
`S1_M_160.lean` module is discovery input only and supplies no inherited proof credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact human root | Every nonzero constant-coefficient linear differential operator has a fundamental solution | Source edition, pinpoint, assumptions, and errata review remain open |
| Domain | Finite-dimensional real coordinate space; complex-valued distributions | The legacy candidate uses tempered distributions, a potentially stronger codomain requirement that must be justified |
| Symbol | Nonzero multivariate polynomial over `ℂ` | Real-versus-complex coefficient transport remains to be frozen |
| Equation | `P(D) E = δ₀` in the distributional sense | Sign and Fourier normalization require checked statement-phase tests |
| Lean object layer | `MvPolynomial`, Euclidean space, Dirac delta, distribution derivatives, polynomial action | The legacy action is a contract, not the canonical constructed calculus |
| Degenerate cases | Zero operator excluded; nonzero constants and zero-dimensional space retained | Boundary mutation tests are deferred |
| Foundations | Lean kernel and pinned mathlib with explicit classical/choice/quotient policy | Fingerprint and closure audit remain open |

The structured binder and hypothesis inventory is in `intake.json`. Source-to-claim differences are
made explicit in `source_statement_crosswalk.md`; notably, the classical distribution conclusion
must not be silently substituted by the legacy tempered-distribution target.

## Statement phase

`Statement.lean` freezes `MalgrangeEhrenpreisTarget`: every finite coordinate type existentially
admits a polynomial differential action for which every nonzero complex polynomial has a tempered
fundamental solution. `statement.json` records the explicit elaborated-expression digest, pinned
environment, binder order, boundary cases, and mutation results. This statement phase supplies no
proof and does not resolve the primary-source status of the tempered-distribution strengthening.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The next phase must audit primary sources and Lean
anchors, freeze typed obligation graphs, close proof bodies, and run the full release protocol.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact statement gate. No theorem completion, Lean closure, or source fidelity is claimed.

## Validation

On base revision `61369637c5db864082a624c34c62a91e6741f9da`, the commands and results in
`validation.md` establish manifest consistency, JSON validity, and dossier-local integrity only.
